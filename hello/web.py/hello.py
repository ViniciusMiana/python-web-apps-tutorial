import web

class MyService:

   def GET(self, name):

       return "Hello {0}".format(str(name))

urls = ( '/(.*)', 'MyService' )

app = web.application(urls, globals())

if __name__ == "__main__":
   app.run()
