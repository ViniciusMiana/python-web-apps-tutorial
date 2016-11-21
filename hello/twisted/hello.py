from twisted.web import server, resource
from twisted.internet import reactor, endpoints

class MyServiceResource(resource.Resource):

   isLeaf = True


   def render_GET(self, request):

       request.setHeader("content-type", "text/plain")

       return "Hello {0}".format(request.path[1:])

if __name__ == "__main__":
   endpoints.serverFromString(reactor, "tcp:8080").listen(server.Site(MyServiceResource()))
   reactor.run()
