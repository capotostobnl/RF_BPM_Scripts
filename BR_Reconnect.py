"""Booster Reconnect script to toggle Waveform, 10Hz, and Control reconnect PVs
Updated 2/12/2024 M. Capotosto"""
#!/usr/bin/python

#from epics import caput
from subprocess import call
import time
pref = ["BR:IS","BR:DS","BR:XS","BR:CS","BR:A1","BR:A2","BR:A3","BR:A4"]
bpm_cnt = [2,2,2,2,7,7,7,7]
#cell = raw_input("Cell (add zero if needed) =  ")
for cell in range(1,9):
   for bpm in range(1,bpm_cnt[cell-1]+1):
      try:
        cstr = str(cell)
        if len(cstr) < 2:
           cstr = "0" + cstr
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
