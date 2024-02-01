"""Pilot Tone Max Power Test
Updated 2/1/2024 M. Capotosto"""
#!/usr/bin/python

from subprocess import call #, check_output
#from epics import caput

cells = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16",
         "17","18","19","20","21","22","23","24","25","26","27","28","29","30"]
bpms = [7,9,9,11,10,7,11,9,7,9,9,11,7,7,7,9,10,9,11,9,9,7,10,7,7,7,9,9,7,11]

##Turn on PT in all cells, set PT ATT to 0, RF ATT to 0
for dex, cell in enumerate(cells):
    for bpm in range(1,bpms[dex]):
        cstr = str(cell)

        #Set Event Code 32
        evt = 'SR:C'+cstr+'-BI{BPM:'+str(bpm)+'}Trig:EventNo-SP'
        call(["caput",evt,"32"])

        #Set PT ON
        ptp = 'SR:C'+cstr+'-BI{BPM:'+str(bpm)+'}Rf:PtPwr-SP'
        call(["caput",ptp,"1"])

        #Set PT Freq
        ptf = 'SR:C'+cstr+'-BI{BPM:'+str(bpm)+'}Rf:PtFreq-SP'
        call(["caput",ptf,"1"])

        #Set PT Attenuator 0
        ptg = 'SR:C'+cstr+'-BI{BPM:'+str(bpm)+'}Gain:PtAtte-SP'
        call(["caput",ptg,"0"])

        #Set RF Atten
        rfg = 'SR:C'+cstr+'-BI{BPM:'+str(bpm)+'}Gain:RfAtte-SP'
        call(["caput",rfg,"0"])
