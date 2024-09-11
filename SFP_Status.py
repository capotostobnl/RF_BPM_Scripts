"""Print SFP Parameters to terminal for SR
Updated 9/11/2024 M. Capotosto"""
#!/usr/bin/python

from epics import caget
#from subprocess import call
import time
bpm_cnt = [6,8,8,10,9,6,10,8,6,8,8,10,6,6,6,8,9,8,10,8,8,6,9,6,6,6,8,8,6,10]
#cell = raw_input("Cell (add zero if needed) =  ")
for cell in range(1,31):
   for bpm in range(1,bpm_cnt[cell-1]+1):
      try:
        cstr = str(cell)
        if len(cstr) < 2:
           cstr = "0" + cstr
        #pvLinkStatusCW = 'SR:C'+cstr+'-BI{BPM:'+str(bpm)+'}Sdi:CW-Link-I'
        #call(["caget",pvLinkStatusCW,"1"])
        print(caget('SR:C'+cstr+'-BI{BPM:'+str(bpm)+'}Sdi:CW-Link-I'))
        
        print("BPM: ", cstr, "-", str(bpm), "LinkStatusCW: ", caget('SR:C'+cstr+'-BI{BPM:'+str(bpm)+'}Sdi:CW-Link-I') )
        time.sleep(0.1)
        print("BPM: ", cstr, "-", str(bpm), "pvLinkStatusCW: ", caget('SR:C'+cstr+'-BI{BPM:'+str(bpm)+'}Sdi:CW-Link-I') )
        time.sleep(0.1)
        print("BPM: ", cstr, "-", str(bpm), "pvLinkStatusCCW: ", caget('SR:C'+cstr+'-BI{BPM:'+str(bpm)+'}Sdi:CCW-Link-I') )
        time.sleep(0.1)
        print("BPM: ", cstr, "-", str(bpm), "pvLinkLossCW: ", caget('SR:C'+cstr+'-BI{BPM:'+str(bpm)+'}Sdi:Cw-LossCnt-I') )
        time.sleep(0.1)
        print("BPM: ", cstr, "-", str(bpm), "pvLinkLossCCW: ", caget('SR:C'+cstr+'-BI{BPM:'+str(bpm)+'}Sdi:CCw-LossCnt-I') )
        time.sleep(0.1)
        print("BPM: ", cstr, "-", str(bpm), "pvCRCErrorCW: ", caget('SR:C'+cstr+'-BI{BPM:'+str(bpm)+'}Sdi:CW_CrcErrorCnt-I') )
        time.sleep(0.1)
        print("BPM: ", cstr, "-", str(bpm), "pvCRCErrorCCW: ", caget('SR:C'+cstr+'-BI{BPM:'+str(bpm)+'}Sdi:CCW_CrcErrorCnt-I') )
        time.sleep(0.1)
        print("BPM: ", cstr, "-", str(bpm), "pvLocalPacketCW: ", caget('SR:C'+cstr+'-BI{BPM:'+str(bpm)+'}Sdi:CW_LbLoPacketTO-I') )
        time.sleep(0.1)
        print("BPM: ", cstr, "-", str(bpm), "pvLocalPacketCCW: ", caget('SR:C'+cstr+'-BI{BPM:'+str(bpm)+'}Sdi:CCW_LbLoPacketTO-I') )
        time.sleep(0.1)
        print("BPM: ", cstr, "-", str(bpm), "pvRemotePacketCW: ", caget('SR:C'+cstr+'-BI{BPM:'+str(bpm)+'}Sdi:CW_RePacketTO-I') )
        time.sleep(0.1)
        print("BPM: ", cstr, "-", str(bpm), "pvRemotePacketCCW: ", caget('SR:C'+cstr+'-BI{BPM:'+str(bpm)+'}Sdi:CCW_RePacketTO-I') )
        time.sleep(0.1)
        print("BPM: ", cstr, "-", str(bpm), "pvSFPPowerCW: ", caget('SR:C'+cstr+'-BI{BPM:'+str(bpm)+'}SFP1:RxPow-I') )
        time.sleep(0.1)
        print("BPM: ", cstr, "-", str(bpm), "pvSFPPowerCCW: ", caget('SR:C'+cstr+'-BI{BPM:'+str(bpm)+'}SFP2:RxPow-I') )
        time.sleep(0.1)
        print("BPM: ", cstr, "-", str(bpm), "pvEVRSFPPower: ", caget('SR:C'+cstr+'-BI{BPM:'+str(bpm)+'}SFP0:RxPow-I') )
        time.sleep(0.1)
      except:
        pass
