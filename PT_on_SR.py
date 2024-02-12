"""Turn on SR Pilot Tone"""
#!/usr/bin/python

from subprocess import call
#from epics import caput

cells = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30"]
bpms = [7,9,9,11,10,7,11,9,7,9,9,11,7,7,7,9,10,9,11,9,9,7,10,7,7,7,9,9,7,11]


for dex, cell in enumerate(cells):
    for bpm in range(1,bpms[dex]):
        cstr = str(cell)
        ptp = 'SR:C'+cstr+'-BI{BPM:'+str(bpm)+'}Rf:PtPwr-SP'
        #caput(ptp, 1)
        call(["caput",ptp,"1"])
        ptf = 'SR:C'+cstr+'-BI{BPM:'+str(bpm)+'}Rf:PtFreq-SP'
        #caput(ptf, 1)
        call(["caput",ptf,"1"])
        rfg = 'SR:C'+cstr+'-BI{BPM:'+str(bpm)+'}Gain:RfAtte-SP'
        #caput(rfg, 0)
        call(["caput",rfg,"1"])
        ptg = 'SR:C'+cstr+'-BI{BPM:'+str(bpm)+'}Gain:PtAtte-SP'
        #caput(ptg, 0)
        call(["caput",ptg,"1"])

#call(["caput","LN-BI{BPM:"+str(y)+"}Rf:PtPwr-SP", "1"])
