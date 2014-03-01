import sys
import SocketServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from datetime import datetime, timedelta




if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8001

if sys.argv[2:]:
    MASTER_ADRESS = sys.argv[2]
else:
    MASTER_ADRESS = "127.0.0.1:8000"

server_address = ('127.0.0.1', port)

TICKET_LIVE_TIME = timedelta(seconds = 55)
TICKET = datetime.now() - TICKET_LIVE_TIME 

class ReplicaHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        try:
            global TICKET
            global MASTER_ADRESS
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
                referer_url = self.headers.getheader('referer')
                print referer_url
                print MASTER_ADRESS
                if referer_url == MASTER_ADRESS:
                    TICKET = datetime.now() + TICKET_LIVE_TIME
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                else:
                    self.send_error(404,"File Not Found: %s" % self.path)
            else:                 
                SimpleHTTPRequestHandler.do_GET(self)
        except IOError:
            self.send_error(404,"File Not Found: %s" % self.path)
     


httpd = SocketServer.TCPServer(server_address, ReplicaHandler)
print "Replica serving HTTP on port", port
httpd.serve_forever()
