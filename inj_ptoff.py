"""Turn OFF Injector BPM Pilot Tone
Updated 1/31/2024 M. Capotosto"""
#!/usr/bin/python

from subprocess import call

for y in range(1,6):
    call(["caput","LN-BI{BPM:"+str(y)+"}Rf:PtPwr-SP", "0"])
    call(["caput","LN-BI{BPM:"+str(y)+"}Gain:PtAtte-SP", "31"])
    call(["caput","LN-BI{BPM:"+str(y)+"}DDR:WfmSel-SP", "1"])

for y in range(1,7):
    call(["caput","LTB-BI{BPM:"+str(y)+"}Rf:PtPwr-SP", "0"])
    call(["caput","LTB-BI{BPM:"+str(y)+"}Gain:PtAtte-SP", "31"])
    call(["caput","LTB-BI{BPM:"+str(y)+"}DDR:WfmSel-SP", "1"])

for x in range(1,5):
    for y in range(1,8):
        call(["caput","BR:A"+str(x)+"-BI{BPM:"+str(y)+"}Rf:PtPwr-SP", "0"])
        call(["caput","BR:A"+str(x)+"-BI{BPM:"+str(y)+"}Gain:PtAtte-SP", "31"])
        call(["caput","BR:A"+str(x)+"-BI{BPM:"+str(y)+"}DDR:WfmSel-SP", "1"])

for y in range(1,3):
    call(["caput","BR:IS-BI{BPM:"+str(y)+"}Rf:PtPwr-SP", "0"])
    call(["caput","BR:IS-BI{BPM:"+str(y)+"}Gain:PtAtte-SP", "31"])
    call(["caput","BR:IS-BI{BPM:"+str(y)+"}DDR:WfmSel-SP", "1"])

for y in range(1,3):
    call(["caput","BR:DS-BI{BPM:"+str(y)+"}Rf:PtPwr-SP", "0"])
    call(["caput","BR:DS-BI{BPM:"+str(y)+"}Gain:PtAtte-SP", "31"])
    call(["caput","BR:DS-BI{BPM:"+str(y)+"}DDR:WfmSel-SP", "1"])

for y in range(1,3):
    call(["caput","BR:XS-BI{BPM:"+str(y)+"}Rf:PtPwr-SP", "0"])
    call(["caput","BR:XS-BI{BPM:"+str(y)+"}Gain:PtAtte-SP", "31"])
    call(["caput","BR:XS-BI{BPM:"+str(y)+"}DDR:WfmSel-SP", "1"])

for y in range(1,3):
    call(["caput","BR:CS-BI{BPM:"+str(y)+"}Rf:PtPwr-SP", "0"])
    call(["caput","BR:CS-BI{BPM:"+str(y)+"}Gain:PtAtte-SP", "31"])
    call(["caput","BR:CS-BI{BPM:"+str(y)+"}DDR:WfmSel-SP", "1"])

for y in range(1,10):
    call(["caput","BTS-BI{BPM:"+str(y)+"}Rf:PtPwr-SP", "0"])
    call(["caput","BTS-BI{BPM:"+str(y)+"}Gain:PtAtte-SP", "31"])
    call(["caput","BTS-BI{BPM:"+str(y)+"}DDR:WfmSel-SP", "1"])


#LN-BI{BPM:1}DDR:WfmSel-SP
