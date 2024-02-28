"""Print value of Alarm Status for Injector BPMs
Updated 2/1/2024 M. Capotosto"""
#!/usr/bin/python

from subprocess import call

pref = ["LN", "LTB", "BR:IS", "BR:A1", "BR:DS", "BR:A2", "BR:XS", "BR:A3", "BR:CS", "BR:A4", "BTS"]
bpm_cnt = [5, 6, 2, 7, 2, 7, 2, 7, 2, 7, 9]

for cell in range(1,12):
   for bpm in range(1,bpm_cnt[cell-1]+1):
        cstr = str(cell)
        if len(cstr) < 2:
           cstr = "0" + cstr
        Status = pref[cell-1]+'-BI{BPM:'+str(bpm)+'}Alarm-Sts'
        call(["caget",Status])