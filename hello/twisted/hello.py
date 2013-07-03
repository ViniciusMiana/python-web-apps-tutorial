from twisted.web import server, resource
from twisted.internet import reactor

class MyServiceResource(resource.Resource):

   isLeaf = True

   numberRequests = 0

   def render_GET(self, request):

       request.setHeader("content-type", "text/plain")

       return "Hello {0}".format(request.path[1:])

if __name__ == "__main__":

   factory = server.Site(MyServiceResource())

   reactor.listenTCP(8080, factory)
   reactor.run()
