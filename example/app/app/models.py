import simplejson as json
from httplib import HTTPConnection

class Stock():
    """Model for webservices stock data"""

    def list_stocks(self):

        conn = HTTPConnection("localhost", 8080)
        conn.request("GET", "/stock/")
        response = conn.getresponse()

        js = response.read()
        jsobj = json.loads(js)

        return jsobj["stocks"]
