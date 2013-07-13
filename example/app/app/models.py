import simplejson as json
import urllib

class Stock():
    """Model for webservices stock data"""
    url = 'http://localhost:8080/stocks'

    def __init__(self, user, text, graphic, time):
        self.user = user
        self.text = text
        self.graphic = graphic
        self.time = time

    def list_stocks(self):
        data = urllib.urlopen(url)
        js = data.readlines()
        jsobj = json.loads(js[0])

        return jsobj["stocks"]
