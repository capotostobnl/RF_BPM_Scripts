"""Soft reboot of BPMs by Cell"""
#!/usr/bin/python

#from bpmclass import bpm
from bpmclass import *
from bpm_addresses import *
from select import select
import sys
import time
from threading import Thread





if len(sys.argv) < 2:
    print "Usage:  bpm_reboot [linac ltb booster bst sr]" 
    sys.exit(0)
  
area = ["linac","ltb","booster","bst","sr"]

if sys.argv[1] in area:
    if sys.argv[1] == "linac": 
       bpmlist = linbpm 
    elif sys.argv[1] == "ltb":
       bpmlist = ltbbpm       
    elif sys.argv[1] == "booster":
       bpmlist = boobpm 
    elif sys.argv[1] == "bst":
       bpmlist = bstbpm 
    elif sys.argv[1] == "sr":
       if len(sys.argv) == 3:
          cellnum = int(sys.argv[2])
          if cellnum > 0 and cellnum < 33:
              #print "Cell Number : %d" % cellnum 
              bpmlist = globals()['c'+ sys.argv[2]] #csrbpm
          else:
              print "Invalid Cell Number"
              sys.exit(0)
       else:
          print "For SR, also enter Cell Number"
          sys.exit(0)
else:
    print "Usage:  bpm_status [linac ltb booster bst sr]"
    sys.exit(0) 

print "Area = %s" % sys.argv[1] 
 

#list of bpm objects
b = []


print "BPM's in list %s" % len(bpmlist) 

# create objects
for bpm in range(len(bpmlist)):    b.append(Bpm(bpmlist[bpm]))
#print "objects created"
    
# connect to moxa
for bpm in range(len(bpmlist)):    b[bpm].moxa_connect()
#print "moxa's connected"


### Connect to sockets (seperate threads to speed things up)
##threads = []
##for bpm in range(len(bpmlist)):
##    t = Thread(target=b[bpm].ip_connect)
##    t.start()
##    threads.append(t)
### wait for all threads to complete before continuing
##for i in threads: 
##    i.join() 
###print "ip's connected"

# reboot
threads = []
for bpm in range(len(bpmlist)):   
    t = Thread(target=b[bpm].reboot)
    threads.append(t)
    t.start()
#wait for all threads to complete
for i in threads:
    i.join() 

print "bpm's rebooting... "
#wait for 30 seconds
#spinning(30)
#
#
#
## get status
#threads = []
#for bpm in range(len(bpmlist)):   
#    t = Thread(target=b[bpm].get_status,args=(bpm,))
#    threads.append(t)
#    t.start()
##wait for all threads to complete
#for i in threads:
#    i.join() 
#
##print "got status"
#
##print status
#print_status_header()
#for bpm in range(len(bpmlist)):
#    print b[bpm].stat
#
#
# without threads
#for bpm in range(0,len(bpmlist)):    b[bpm].ip_connect()
#
#print_status()
# 
