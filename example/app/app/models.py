import simplejson as json
from httplib import HTTPConnection

class Stock():
    """Model for webservices stock data"""

    def list_stocks(self):
        """List all stocks from webserice"""
        conn = HTTPConnection("localhost", 8080)
        conn.request("GET", "/stock/")
        response = conn.getresponse()

        js = response.read()
        jsobj = json.loads(js)

        return jsobj["stocks"]

    def add_stock(self, stock):
        """Add a stock to webservice"""
        conn = HTTPConnection("localhost", 8080)
        conn.request("POST", "/stock/{0}".format(stock))
        response = conn.getresponse()

        if response.status != 200:
            raise Exception(response.read())
        return True


    def remove_stock(self, stock):
        """Remove a stock from webservice"""
        conn = HTTPConnection("localhost", 8080)
        conn.request("DELETE", "/stock/{0}".format(stock))
        response = conn.getresponse()
