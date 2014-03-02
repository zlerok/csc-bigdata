import sys
from SocketServer import TCPServer
import urllib2
from SimpleHTTPServer import SimpleHTTPRequestHandler
from datetime import datetime
from time import sleep
from threading import Thread


if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8000
    
MASTER_ADRESS = "127.0.0.1" 

server_adress =  (MASTER_ADRESS, port)
MASTER_ADRESS = MASTER_ADRESS  + ':' + str(port)  

REPLICS = ["127.0.0.1:8001", "127.0.0.1:8002", "127.0.0.1:8003"]
MAIN_REPLICA = None

class MasterHandler(SimpleHTTPRequestHandler):
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


def setMainReplica():
        global REPLICS
        global MAIN_REPLICA      
        #check current MAIN_REPLICA
        #return if answer
        if MAIN_REPLICA is not None:
            try:
                req = urllib2.Request("http://" + MAIN_REPLICA + "/set-new-ticket")
                req.add_header("referer", MASTER_ADRESS)
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
                req.add_header("referer", MASTER_ADRESS)
                
                response = urllib2.urlopen(req)
                if response.getcode() == 200:
                    MAIN_REPLICA = replic_adress
                    return
            except:
                pass
        MAIN_REPLICA = None


def clock():
    while True:
        setMainReplica()
        sleep(50)

httpd = TCPServer(server_adress, MasterHandler)
print "Master serving HTTP on port", port

t = Thread(target=clock)
t.daemon = True
t.start()
setMainReplica()

httpd.serve_forever()
