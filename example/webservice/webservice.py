#!/usr/bin/python

import re
import sys
import json
from twisted.web import server, resource
from twisted.internet import reactor
from twisted.python import log
from database import MyServiceDatabase


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
        except (TypeError, ValueError, KeyError) as e:
            result = {"status": "error", "message": e.message}

        return json.dumps(result)

    def render_DELETE(self, request):
        """Handle /stock/STOCK_NAME request"""

        request.setHeader("content-type", "application/json")

        result = {"status": "ok"}

        try:
            data = json.loads(request.content.read())

            stock = data["stock"]

            self.db.remove_stock(stock)
        except (TypeError, ValueError, KeyError) as e:
            result = {"status": "error", "message": e.message}

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
            result["value"] = self.db.get_stock(stock)

        except (TypeError, ValueError, KeyError) as e:
            result = {"status": "error", "message": e.message}

        return json.dumps(result)


def main():
    """Main entry point"""
    root = resource.Resource()

    root.putChild("setting", MyServiceSettings())
    root.putChild("stock", MyServiceStocks())
    factory = server.Site(root)

    log.startLogging(sys.stdout)

    reactor.listenTCP(8080, factory)
    reactor.run()
    return 0

if __name__ == "__main__":
    sys.exit(main())
