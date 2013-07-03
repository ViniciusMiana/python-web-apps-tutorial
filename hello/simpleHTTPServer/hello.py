import SimpleHTTPServer

import SocketServer

class MyService(SimpleHTTPServer.SimpleHTTPRequestHandler):

   def do_GET(self):

       self.send_response(200, "OK")

       self.send_header("Content-Type", "text/plain")

       self.end_headers()

       self.wfile.write("Hello {0}".format(self.path[1:]))


httpd = SocketServer.TCPServer(("", 8080), MyService)
httpd.serve_forever()
