import sys
import BaseHTTPServer
import SocketServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime


bilet = datetime(2005, 7, 14, 12, 30)   
master_addres = "127.10.0.1:8000"
class ReplicaHandler(SimpleHTTPRequestHandler):
     
    def __init__(self):
        self.bilet = datetime(2005, 7, 14, 12, 30)   
        self.master_addres = "127.10.0.1:8000"
        super(ReplicaHandler, self).__init__(*args)
        
    def do_GET(self):
        try:
            if self.path == "/write":
                answer = "KO" if bilet < datetime.now() else "OK"
                
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                tmp = bilet.strftime("%d/%m/%y %H:%M")
                self.wfile.write(answer + "   " + tmp) 
            else:                 
                SimpleHTTPRequestHandler.do_GET(self)
        except IOError:
            self.send_error(404,"File Not Found: %s" % self.path)
     
    def do_POST(self):
        try:
            #if self.path == "/take_new_bilet":
            #s = self.rfile.read()    
            content_len = int(self.headers.getheader('content-length'))
            post_str = self.rfile.read(content_len)
            bilet = datetime.strptime(post_str, "%d/%m/%y %H:%M")      
            print bilet
        except Exception:
            print "error"


if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8001
server_address = ('127.10.0.1', port)
Handler = ReplicaHandler

httpd = SocketServer.TCPServer(("", port), Handler)
print "Serving HTTP on", "port", "..."
httpd.serve_forever()
