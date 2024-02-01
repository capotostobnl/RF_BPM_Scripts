"""Change BPM bootup Mode for a cell
Updated to Python 3 Syntax, M. Capotosto 1/31/2024"""
#!/usr/bin/python

#from bpmclass import bpm
import sys
import time
from select import select
from bpmclass import *
from bpm_addresses import *
from threading import Thread





if len(sys.argv) < 2:
    print ("Usage:  bpm_chmode [upgrade app] [linac ltb booster bst sr [cell]]" )
    sys.exit(0)

area = ["linac","ltb","booster","bst","sr"]

if sys.argv[1] == "upgrade" or sys.argv[1] == "app":
    print ("Switching mode to ", sys.argv[1])
    newmode = sys.argv[1]
    if newmode == "upgrade":
        newmode = "UPG"
    elif newmode == "app":
        newmode = "APP"
else:
    print ("Usage:  bpm_chmode [upgrade app] [linac ltb booster bst sr [cell]]")
    sys.exit(0)



if sys.argv[2] in area:
    if sys.argv[2] == "linac":
        bpmlist = linbpm 
    elif sys.argv[2] == "ltb":
        bpmlist = ltbbpm       
    elif sys.argv[2] == "booster":
        bpmlist = boobpm 
    elif sys.argv[2] == "bst":
        bpmlist = bstbpm 
    elif sys.argv[2] == "sr":
        if len(sys.argv) == 4:
            cellnum = int(sys.argv[3])
            if cellnum > 0 and cellnum < 31:
                #print "Cell Number : %d" % cellnum 
                bpmlist = globals()['c'+ sys.argv[3]] #csrbpm
            else:
                print ("Invalid Cell Number")
                sys.exit(0)
        else:
            print ("For SR, also enter Cell Number")
            sys.exit(0)

else:
    print ("Usage:  bpm_status [linac ltb booster sr]")
    sys.exit(0) 

print ("Area =", sys.argv[2])
if sys.argv[2] == "sr":
    print ("Cell =", cellnum)


#list of bpm objects
b = []


#print "BPM's in list %s" % len(bpmlist)

# create objects
for bpm in range(len(bpmlist)):    b.append(Bpm(bpmlist[bpm]))
#print "objects created"

# connect to moxa
#for bpm in range(len(bpmlist)):    b[bpm].moxa_connect()
#print "moxa's connected"
threads = []
for bpm in range(len(bpmlist)):
    t = Thread(target=b[bpm].moxa_connect)
    t.start()
    threads.append(t)
# wait for all threads to complete before continuing
for i in threads:
    i.join()
#

# Connect to sockets (seperate threads to speed things up)
threads = []
for bpm in range(len(bpmlist)):
    t = Thread(target=b[bpm].ip_connect)
    t.start()
    threads.append(t)
# wait for all threads to complete before continuing
for i in threads:
    i.join()
#print "ip's connected"

# change mode
threads = []
for bpm in range(len(bpmlist)):
    t = Thread(target=b[bpm].switch_mode,args=(newmode,))
    threads.append(t)
    t.start()
#wait for all threads to complete
for i in threads:
    i.join()



# without threads
#for bpm in range(0,len(bpmlist)):    b[bpm].ip_connect()
#
#print_status()
