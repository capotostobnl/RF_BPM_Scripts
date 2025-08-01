"""Toggle Waveform, Control, and 10Hz Reconnect PVs for SR
Updated 2/12/2024 to add C27 Hex ID BPMs M. Capotosto"""
#!/usr/bin/python

#from epics import caput
from subprocess import call
import time
bpm_cnt = [6,8,8,10,9,6,10,8,8,8,8,10,6,6,6,8,9,8,10,8,8,6,9,6,6,6,8,8,6,10]
#cell = raw_input("Cell (add zero if needed) =  ")
for cell in range(1,31):
   for bpm in range(1,bpm_cnt[cell-1]+1):
      try:
        cstr = str(cell)
        if len(cstr) < 2:
           cstr = "0" + cstr
        wfmR = 'SR:C'+cstr+'-BI{BPM:'+str(bpm)+'}wfm-RECONNECT'
        call(["caput",wfmR,"1"])
        #caput(wfmR, 1)
        time.sleep(0.1)
        txR = 'SR:C'+cstr+'-BI{BPM:'+str(bpm)+'}TX-RECONNECT'
        call(["caput",txR,"1"])
        #caput(txR, 1)
        time.sleep(0.1)
        rxR = 'SR:C'+cstr+'-BI{BPM:'+str(bpm)+'}RX10Hz-RECONNECT'
        call(["caput",rxR,"1"])
        #caput(rxR, 1)
        time.sleep(0.1)
      except:
        pass
