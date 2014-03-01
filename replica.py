import sys
import SocketServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from datetime import datetime, timedelta

TICKET = 0
TICKET_LIVE_TIME = timedelta(seconds = 55)
MASTER_ADRESS = "127.10.0.1:8000"

class ReplicaHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        try:
            global TICKET
            if self.path == "/write":
                answer = "KO" if TICKET < datetime.now() else "OK"
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(answer)
                       #         '<br />TICKET : ' + TICKET.strftime("%d/%m/%y %H:%M") + 
                        #        '<br />now : ' + datetime.now().strftime("%d/%m/%y %H:%M")) 
                #print 'GET : ' + TICKET.strftime("%d/%m/%y %H:%M")
            elif self.path == "/set-new-ticket":    
                TICKET = datetime.now() + TICKET_LIVE_TIME
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
            else:                 
                SimpleHTTPRequestHandler.do_GET(self)
        except IOError:
            self.send_error(404,"File Not Found: %s" % self.path)
     
 #   def do_POST(self):
 #       try:
 #           global TICKET
 #           if self.path == "/set-new-ticket":
 #               content_len = int(self.headers.getheader('content-length'))
 #               post_str = self.rfile.read(content_len)
 #               TICKET = datetime.strptime(post_str, "%d/%m/%y %H:%M")      
 #               #print 'POST : ' + TICKET.strftime("%d/%m/%y %H:%M")
 #       except Exception:
 #           self.send_error(404,"File Not Found: %s" % self.path)


if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8001
server_address = ('127.10.0.1', port)

httpd = SocketServer.TCPServer(("", port), ReplicaHandler)
print "Replica serving HTTP on port", port
httpd.serve_forever()
