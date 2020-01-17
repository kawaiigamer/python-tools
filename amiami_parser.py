import time
import sys
import urllib.request
import socket
import re
print ("[" + time.strftime("%Y/%m/%d %H:%M:%S")+ "] " + "\n---------------------------")
Ttimeout = int(sys.argv[1]) if len (sys.argv) > 1 else 10
Patch   = str(sys.argv[2]) if len (sys.argv) > 2 else "http://www.amiami.jp/top/page/c/bishoujo.html"
Vaules = []
try:
  raw =  str ( urllib.request.urlopen( Patch,timeout = Ttimeout).read() )
  type = re.findall(re.compile("</font>(\d+,\d+)"),raw)
  Vaules = [int(x.replace(",","")) for x in type]
  S = sum(Vaules)
  print ("All: " + str(S ) + "円")
  print ("For: " + str ( len(Vaules) ) + " matches")
  print ("Srd: " + str ( S / len(Vaules)) + "円")
  print ("Min: " + str ( min(Vaules)) + "円")
  print ("Max: " + str ( max(Vaules)) + "円")
  print ("List:\n" + "\n".join ( str(x) for x in sorted(Vaules) ) )
except (urllib.request.URLError, socket.timeout) as e:
   print ("Parsing error Error " + e)
