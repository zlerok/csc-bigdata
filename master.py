import sys
import SocketServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from datetime import datetime

MASTER_ADRESS = "127.10.0.1:8000"
REPLICS = [8001, 8002, 8003]
MAIN_REPLICA = REPLICS[0]

class MasterHandler(SimpleHTTPRequestHandler):

    def __init__(self, *args):
        #Start some timer(handler = setMainReplica()) 
        SimpleHTTPRequestHandler.__init__(self, *args)

    def do_GET(self):
        try:
            if self.path == "/get-write-replica":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(self.getMainReplica(self))
            else:                 
                SimpleHTTPRequestHandler.do_GET(self)
        except IOError:
            self.send_error(404,"File Not Found: %s" % self.path)

    @staticmethod
    def getMainReplica():
        global MAIN_REPLICA
        return 'Not ready yet' if MAIN_REPLICA is None else MAIN_REPLICA
        
    @staticmethod                    
    def setMainReplica():
        global REPLICS
        global MAIN_REPLICA
        #check current MAIN_REPLICA
        #return if answer
        #else loking for new MAIN_REPLICA, by checking REPLICS[] 
        #if find smbd MAIN_REPLICA = newMainReplica
        #else MAIN_REPLICA = None
        
if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8000
server_address = ('127.10.0.1', port)

httpd = SocketServer.TCPServer(("", port), MasterHandler)
print "Master serving HTTP on port", port
httpd.serve_forever()
