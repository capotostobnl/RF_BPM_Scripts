"""Display BPM Status
1/29/2025 M. Capotosto"""
# !/usr/bin/python3

import sys
import time
from threading import Thread
from bpmclass import Bpm, print_status_header
from bpm_addresses import linbpm, ltbbpm, boobpm, bstbpm, \
    c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, \
    c14, c15, c16, c17, c18, c19, c20, c21, c22, c23, c24, \
    c25, c26, c27, c28, c29, c30 # noqa


def main():
    if len(sys.argv) < 2:
        print("Usage:  bpm_status [linac ltb booster sr [cell] all]")
        sys.exit(0)

    area = ["linac", "ltb", "booster", "bst", "sr", "all"]
    cellnum = 0

    if sys.argv[1] in area:
        if sys.argv[1] == "linac":
            drawOutputs("LINAC", 0, linbpm)
        elif sys.argv[1] == "ltb":
            drawOutputs("LTB", 0, ltbbpm)
        elif sys.argv[1] == "booster":
            drawOutputs("BOOSTER", 0, boobpm)
        elif sys.argv[1] == "bst":
            drawOutputs("BST", 0, bstbpm)
        elif sys.argv[1] == "sr":
            if len(sys.argv) == 3:
                cellnum = int(sys.argv[2])
                if cellnum > 0 and cellnum < 33:
                    # print "Cell Number : %d" % cellnum
                    drawOutputs("SR", cellnum, globals()['c' + sys.argv[2]])
                else:
                    print("Invalid Cell Number")
                    sys.exit(0)
            else:
                print("For SR, also enter Cell Number")
                sys.exit(0)
        elif sys.argv[1] == "all":
            cellnum = 1
            while (1):
                print("\n\n---------------------------------------------------"\
                      "---------------------------------------------------\n\n")
                drawOutputs("LINAC", 0, linbpm)
                print("\n\n----------------------------------------------------"\
                      "---------------------------------------------------\n\n")
                drawOutputs("LTB", 0, ltbbpm)
                print("\n\n-----------------------------------------------------"\
                      "--------------------------------------------------\n\n")
                drawOutputs("BOOSTER", 0, boobpm)
                print("\n\n------------------------------------------------------"\
                      "---------------------------------------------------\n\n")
                drawOutputs("BST", 0, bstbpm)
                print("\n\n------------------------------------------------------"\
                      "---------------------------------------------------\n\n")
                for cellnum in range(1, 31):
                    drawOutputs("SR", cellnum, globals()['c' + str(cellnum)])
                    print("\n\n---------------------------------------------------"\
                        "--------------------------------------------------------\
                          --\n\n")
                    cellnum += cellnum
                break
    else:
        print("Usage:  bpm_status [linac ltb booster bst sr]")
        sys.exit(0)

#    drawOutputs(cellnum, bpmlist)  # draw the formatted output status table


def drawOutputs(selectedArea, cellnum, bpmlist):
    printAreaHeader(selectedArea, cellnum)
    b = connectBPM(bpmlist)
    getStatus(bpmlist, b)


def printAreaHeader(selectedArea, cellnum):
    print("Area = ", selectedArea)
    if cellnum > 0:
        print("Cell = ", cellnum)


def connectBPM(bpmlist):
    # list of bpm objects
    b = []

    # create objects
    for bpm in range(len(bpmlist)):
        b.append(Bpm(bpmlist[bpm]))

    # Connect to moxa (seperate threads to speed things up)
    threads = []
    for bpm in range(len(bpmlist)):
        t = Thread(target=b[bpm].moxa_connect)
        t.start()
        threads.append(t)
    # wait for all threads to complete before continuing
    for i in threads:
        i.join()

    # Connect to sockets (seperate threads to speed things up)
    threads = []
    for bpm in range(len(bpmlist)):
        t = Thread(target=b[bpm].ip_connect)
        t.start()
        threads.append(t)
    # wait for all threads to complete before continuing
    for i in threads:
        i.join()
    return b


def getStatus(bpmlist, b):
    # get status
    threads = []
    for bpm in range(len(bpmlist)):
        t = Thread(target=b[bpm].get_status, args=(bpm,))
        threads.append(t)
        t.start()
        time.sleep(0.1)  # Delay to allow time for CAGet operation
    # wait for all threads to complete
    for i in threads:
        i.join()

    # print status
    print_status_header()
    for bpm in range(len(bpmlist)):
        print(b[bpm].stat)


if __name__ == "__main__":
    main()
