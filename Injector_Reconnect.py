"""Injector Reconnect script to toggle Waveform, 10Hz, and Control reconnect PVs
Updated 8/1/2025 M. Capotosto"""
#!/usr/bin/python

#from epics import caput

from subprocess import call
import time
pref = ["LN", "LTB", "BR:IS", "BR:A1", "BR:DS", "BR:A2", "BR:XS", "BR:A3", "BR:CS", "BR:A4", "BTS"]
bpm_cnt = [5, 6, 2, 7, 2, 7, 2, 7, 2, 7, 9]
#cell = raw_input("Cell (add zero if needed) =  ")
for cell in range(1,12):
   for bpm in range(1,bpm_cnt[cell-1]+1):
      try:
        cstr = str(cell) #cell string
        if len(cstr) < 2:
           cstr = "0" + cstr #if cell <10, append leading 0
        wfmR = pref[cell-1]+'-BI{BPM:'+str(bpm)+'}wfm-RECONNECT'
        call(["caput",wfmR,"1"])
        #caput(wfmR, 1)
        time.sleep(0.1)
        txR = pref[cell-1]+'-BI{BPM:'+str(bpm)+'}TX-RECONNECT'
        call(["caput",txR,"1"])
        #caput(txR, 1)
        time.sleep(0.1)
        rxR = pref[cell-1]+'-BI{BPM:'+str(bpm)+'}RX10Hz-RECONNECT'
        call(["caput",rxR,"1"])
        #caput(rxR, 1)
        time.sleep(0.1)
      except:
        pass
