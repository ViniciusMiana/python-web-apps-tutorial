#!/usr/bin/python

import re
import sys
import csv
import json
import sqlite3
from twisted.web import server, resource
from twisted.internet import task, reactor
from twisted.python import log
from database import MyServiceDatabase

from httplib import HTTPConnection

class MyServiceSettings(resource.Resource):
    """Handle /setting requests"""
    isLeaf = True

    def __init__(self):
        self.db = MyServiceDatabase()

    def render_PUT(self, request):
        """Handle /setting/SETTING_NAME request. Body must be a json {"value": "SETTING_VALUE"} """
        request.setHeader("content-type", "application/json")

        result = {"status": "ok"}

        resetting = re.match("/setting/(.*)", request.uri)
        if resetting is None:
            result = {"status": "error", "message": "no setting requested"}
            return json.dumps(result)

        try:
            setting = resetting.groups()[0]
            data = json.loads(request.content.read())

            value = data["value"]

            self.db.update_setting(setting, value)
        except (TypeError, ValueError, KeyError) as e:
            result = {"status": "error", "message": e.message}

        return json.dumps(result)

    def render_GET(self, request):
        """Handle /setting or /setting/SETTING_NAME request"""
        request.setHeader("content-type", "application/json")

        result = {"status": "ok"}

        setting = None
        resetting = re.match("/setting/(.+)", request.uri)

        if resetting is not None:
            setting = resetting.groups()[0]

        if setting is None:
            settings = self.db.list_settings()

            result["settings"] = settings
            return json.dumps(result)

        try:

            result["value"] = self.db.get_setting(setting)

        except (TypeError, ValueError, KeyError) as e:
            result = {"status": "error", "message": e.message}

        return json.dumps(result)


class MyServiceStocks(resource.Resource):
    """Handle /stock requests"""
    isLeaf = True

    def __init__(self):
        self.db = MyServiceDatabase()

    def render_POST(self, request):
        """Handle /stock/STOCK_NAME request"""

        request.setHeader("content-type", "application/json")

        result = {"status": "ok"}

        stock = None
        restock = re.match("/stock/(.+)", request.uri)

        if restock is not None:
            stock = restock.groups()[0]

        if stock is None:
            result = {"status": "error", "message": "no stock requested"}
            return json.dumps(result)

        try:
            self.db.add_stock(stock)
        except (TypeError, ValueError, KeyError, sqlite3.IntegrityError) as e:
            result = {"status": "error", "message": e.message}

        return json.dumps(result)

    def render_DELETE(self, request):
        """Handle /stock/STOCK_NAME request"""

        request.setHeader("content-type", "application/json")

        result = {"status": "ok"}

        stock = None
        restock = re.match("/stock/(.+)", request.uri)

        if restock is not None:
            stock = restock.groups()[0]

        if stock is None:
            result = {"status": "error", "message": "no stock requested"}
            return json.dumps(result)

        self.db.remove_stock(stock)

        return json.dumps(result)

    def render_GET(self, request):
        """Handle /stock or /stock/STOCK_NAME request"""

        request.setHeader("content-type", "application/json")

        result = {"status": "ok"}

        stock = None
        restock = re.match("/stock/(.+)", request.uri)

        if restock is not None:
            stock = restock.groups()[0]

        if stock is None:
            result["stocks"] = self.db.list_stocks()
            return json.dumps(result)

        try:
            result["last_price"] = self.db.get_stock_price(stock)

        except (TypeError, ValueError, KeyError) as e:
            result = {"status": "error", "message": e.message}

        return json.dumps(result)


def update_stock():
    """Called in loop to update stocks values"""
    db = MyServiceDatabase()
    stocks = db.list_stocks()

    conn = HTTPConnection("download.finance.yahoo.com")
    conn.request("GET", "/d/quotes.csv?s={0}&f=sl1".format("+".join([x["symbol"] for x in stocks])))

    response = conn.getresponse()

    if response.status != 200:
        return

    for row in csv.reader(response.read().split("\n")):
        if len(row) > 1:
            db.update_stock(row[0], row[1])

def main():
    """Main entry point"""
    root = resource.Resource()

    root.putChild("setting", MyServiceSettings())
    root.putChild("stock", MyServiceStocks())
    factory = server.Site(root)

    log.startLogging(sys.stdout)

    us = task.LoopingCall(update_stock)
    us.start(30, now=True)

    reactor.listenTCP(8080, factory)
    reactor.run()
    return 0

if __name__ == "__main__":
    sys.exit(main())
