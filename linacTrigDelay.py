"""Set LINAC BPM Trigger Delay
Created 7/31/2024 M. Capotosto"""
#!/usr/bin/python

from subprocess import call

for y in range(1,6):
    call(["caput","LN-BI{BPM:"+str(y)+"}Trig:AdcDelay-SP", "3784"])
