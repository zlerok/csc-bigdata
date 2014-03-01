import sys
import SocketServer
import urllib2
from SimpleHTTPServer import SimpleHTTPRequestHandler
from datetime import datetime
#from time import time, sleep#gmtime, strftime
import time

import threading

#MASTER_ADRESS = "127.10.0.1"
REPLICS = ["127.0.0.1:8001", "127.0.0.1:8002", "127.0.0.1:8003"]
MAIN_REPLICA = None

class MasterHandler(SimpleHTTPRequestHandler):

 #   def __init__(self, *args):
 #       #Start some timer(handler = setMainReplica()) 
 #       #MasterHandler.setMainReplica()
 #       SimpleHTTPRequestHandler.__init__(self, *args)

    def do_GET(self):
        try:
            if self.path == "/get-write-replica":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                
                self.wfile.write(self.getMainReplica())
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
        if MAIN_REPLICA is not None:
            try:
                req = urllib2.Request("http://" + MAIN_REPLICA + "/set-new-ticket")
                response = urllib2.urlopen(req)
                if response.getcode() == 200:
                    return
            except:
                pass
          
        #else loking for new MAIN_REPLICA, by checking REPLICS[] 
        #if find smbd MAIN_REPLICA = newMainReplica
        for replic_adress in REPLICS:
            try:
                req = urllib2.Request("http://" + replic_adress + "/set-new-ticket")
                response = urllib2.urlopen(req)
                if response.getcode() == 200:
                    MAIN_REPLICA = replic_adress
                    return
            except:
                pass
        MAIN_REPLICA = None

def clock():
    while True:
        MasterHandler.setMainReplica()
        time.sleep(50)
    
if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8000
    
server_address = ('127.0.0.1', port)
httpd = SocketServer.TCPServer(("", port), MasterHandler)
print "Master serving HTTP on port", port

t = threading.Thread(target=clock)
t.daemon = True
t.start()

httpd.serve_forever()
