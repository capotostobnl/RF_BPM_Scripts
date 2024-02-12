import matplotlib.pyplot as plt
import scipy.signal as signal
import cothread
from cothread.catools import *
import numpy as np
import time
import sys
import tty
import termios
import select

datapts = 100000



def is_key_pressed():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])




def read_bpms(filename):
  bpms = []
  s = []
  bpmlist = open(filename)
  for line in bpmlist:
      values = line.split()
      if len(values) == 2 and values[0] != '#':
        bpms.append(values[0])
        s.append(values[1])
  print("Processing %d bpms" % len(bpms))
  return bpms, s



def set_pv(bpms,pvname,val):

   bpms_pv = []
   for i in range(len(bpms)):
       bpms_pv.append(bpms[i]+pvname)
   caput(bpms_pv,val)
 


def get_waveform(bpms,pvname,numpts):
  
  bpms_pv = []  
  waveform = np.zeros((len(bpms),1000))
  for i in range(len(bpms)):
     bpms_pv.append(bpms[i]+pvname)
  #print(bpms_pv)
  #cawaveform = caget(bpms_pv)
  #print("Type")  
  #print(type(cawaveform))
  #print("Len")
  #print(len(cawaveform))
  #waveform = caget(bpms_pv)
  #print("Values")
  #Some of the return lengths are 100k and some are 400k, so read one at a time and truncate
  print("Reading TbT data...") 
  for i in range(len(bpms)):  
    cawaveform = caget(bpms_pv[i])  
    #print(i)
    #print(cawaveform)
    cawaveformtrunc = cawaveform[0:1000] 
    #print(cawaveformtrunc)
    waveform[i] = np.array(cawaveformtrunc, dtype=np.float32)
    #print(waveform[i])
  print("Finished Reading TbT data...")
  
  #add a dummy offset
  for i in range(10,20):
     for j in range(5):
       waveform[i,j] = waveform[i,j] + 0 

  #waveform[20,2] = 0.0 
  return waveform 



def calc_stats(bpms,tbtsum):

  #calc stats
  tbts_std = []
  tbts_mean = []
  
  for i in range(len(bpms)):
     tbts_std.append(np.std(tbtsum[i])) 
     tbts_mean.append(np.mean(tbtsum[i])) 

  #print results 
  for i in range(len(bpms)):
     print('%d:  %s  mean:%f  std:%f'  % (i, bpms[i], tbts_mean[i], tbts_std[i]))

  return tbts_std, tbts_mean





def main():

  #bpms,s = read_bpms('bpm_list.txt')
  bpms,s = read_bpms('bpm_list_noids.txt')


  #set_pv(bpms,'Gain:PtAtte-SP',11)
  #set_pv(bpms,'Gain:RfAtte-SP',0)
  #set_pv(bpms,'DDR:WfmSel-SP','TBT Wfm')  #allows TbT waveform to be updated
  #set_pv(bpms,'Trig:TrigSrc-SP',0) #set to internal trigger source
  
  #set_pv(bpms,'Rf:PtPwr-SP',1)
  #set_pv(bpms,'Rf:PtFreq-SP',0)
  #set_pv(bpms,'Rf:PtFreq-SP',1)
  #set_pv(bpms,'ERec:TbtEnableLen-SP',10000)
  #set_pv(bpms,'Burst:TbtEnableLen-SP',100000)
  #caput('SR-BI{BPM}Evt:Single-Cmd',1)

  fig1,ax1 = plt.subplots(2,1)
  fig2,ax2 = plt.subplots()
  fig3,ax3 = plt.subplots()
  fig4,ax4 = plt.subplots()

  while True: 
    
     if is_key_pressed(): 
        if key == 'q':
           print("Exiting")
           break

     #caput('SR-BI{BPM}Evt:Single-Cmd',1)

     #trigcntold = caget('SR:C13-BI{BPM:1}Wfm:TxCnt-I')
     #time.sleep(1) 
     tbtsum = get_waveform(bpms,'Tbt-sum',50)
     tbts_std, tbts_mean = calc_stats(bpms,tbtsum)
 
     #plt.imshow(a, interpolation='nearest', aspect='auto')
     #plt.plot(np.transpose(tbtsum))
     ax1[0].clear()
     ax1[0].plot(tbts_std)
     ax1[0].set_xlabel('BPM #')
     ax1[0].set_ylabel('Sum RMS Noise')
     ax1[0].grid(True)
     ax1[1].clear()
     ax1[1].plot(tbts_mean) 
     ax1[1].set_xlabel('BPM #')
     ax1[1].set_ylabel('Sum Mean')
     ax1[1].grid(True)

     ax4.set_ylim(0,.0075)
     ax4.set_ylabel('Tbt Sum')
     ax4.set_xlabel('TbT Turn # after injection')
 
     ax4.grid(True)
     ax4.clear() 
     for i in range(len(bpms)):
         ax4.plot(tbtsum[i,0:12])
         


     ax2.clear()
     #ax2.hist2d(tbtsum)
     ax2.imshow(tbtsum[:,0:12], interpolation='none', aspect='auto',vmin=0,vmax=0.002) 
     #ax2.imshow(tbtsum[:,0:10], interpolation='nearest', aspect='auto') 
     ax2.grid(True)


     tbtsum_zs = np.zeros((len(bpms),50))

     #subtract the offset - use the first tbt sample as the baseline value.
     #print(tbtsum[:,0])
     print("Length of tbtsum")
     print(len(tbtsum))
     print("idx    name\t\tTurn0\t\tTurn1\t\tTurn2\t\tTurn3\t\tTurn4\t\tTurn5\t\tTurn6\t\tTurn7")
     for i in range(len(bpms)):     
        for j in range(50):
           tbtsum_zs[i,j] = tbtsum[i,j] - tbtsum[i,0]
        #print("%s  i: %d  j: %d  tbtsum: %f   tbtsum_zs: %f" % (bpms[i],i,j,tbtsum[i,j],tbtsum_zs[i,j]))
        print("%3d  %s :  %f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t"  % (i,bpms[i],tbtsum[i,0],tbtsum[i,1],tbtsum[i,2],tbtsum[i,3],tbtsum[i,4],tbtsum[i,5],tbtsum[i,6],tbtsum[i,7]))
 


     max = np.amax(tbtsum_zs)
     print("Max Value: %f" % (max))
     ax3.clear()
     ax3.set_ylabel("BPM #")
     ax3.set_xlabel("Turn # after injection")
     ax3.imshow(tbtsum_zs[:,0:12], interpolation='none', aspect='auto',vmin=0,vmax=.001) 
     #ax3.imshow(tbtsum[:,0:10], interpolation='nearest', aspect='auto') 
     ax3.grid(True)
  
 

     trigcntold = caget('SR:C13-BI{BPM:1}Wfm:TxCnt-I')
     while (caget('SR:C13-BI{BPM:1}Wfm:TxCnt-I') == trigcntold):
          print("Waiting for Trigger...") 
          fig1.canvas.draw()
          fig2.canvas.draw()
          fig3.canvas.draw()
          plt.pause(0.1)
          time.sleep(1)




     #plt.pause(0.1)
     #fig1.canvas.draw()
     #fig2.canvas.draw()
     #fig3.canvas.draw()

if __name__ == "__main__":
  main()
