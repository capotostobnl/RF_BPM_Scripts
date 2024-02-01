"""Set Injector BBA Offsets
Updated 2/1/2024 M. Capotosto"""
#!/usr/bin/python

#Temporary
from subprocess import call
import time
x=0
#Set Kx, Ky
while x==0:
    x=1
    for z in range(1,6):
        strings = "LN-BI{BPM:"+str(z)+"}Kx-SP"
        call(["caput",strings,"14.37"])
        time.sleep(0.1)
        strings = "LN-BI{BPM:"+str(z)+"}Ky-SP"
        call(["caput",strings,"14.37"])
        time.sleep(0.1)

    bts_kx = ["9.93","14.55","14.55","14.55","14.55","14.55","14.55","14.55","11.37"]
    bts_ky = ["11.51","14.55","14.55","14.55","14.55","14.55","14.55","14.55","10.93"]
    for z in range(1,10):
        strings = "BTS-BI{BPM:"+str(z)+"}Kx-SP"
        call(["caput",strings,bts_kx[z-1]])
        time.sleep(0.1)
        strings = "BTS-BI{BPM:"+str(z)+"}Ky-SP"
        call(["caput",strings,bts_ky[z-1]])
        time.sleep(0.1)

    ltb_kx = ["14.55","18.37","14.55","14.55","14.55","14.55"]
    ltb_ky = ["14.55","17.19","14.55","14.55","14.55","14.55"]
    for z in range(1,7):
        strings = "LTB-BI{BPM:"+str(z)+"}Kx-SP"
        call(["caput",strings,ltb_kx[z-1]])
        time.sleep(0.1)
        strings = "LTB-BI{BPM:"+str(z)+"}Ky-SP"
        call(["caput",strings,ltb_ky[z-1]])
        time.sleep(0.1)

    ltb_bbax = ["0.00047015415","-0.1114028443","-0.614498999527","-0.151343830173",
                "-0.0751796312817","-0.233821214818"]
    ltb_bbay = ["0.0079767465","1.2553143615","-0.148847936542","-0.0394681509426",
                "-0.503520611148","0.363104914891"]
    for z in range(1,7):
        strings = "LTB-BI{BPM:"+str(z)+"}BbaXOff-SP"
        call(["caput",strings,ltb_bbax[z-1]])
        time.sleep(0.1)
        strings = "LTB-BI{BPM:"+str(z)+"}BbaYOff-SP"
        call(["caput",strings,ltb_bbay[z-1]])
        time.sleep(0.1)

    call(["caput","BR:IS-BI{BPM:2}Kx-SP","8.2405"])
    time.sleep(0.1)
    call(["caput","BR:IS-BI{BPM:2}Ky-SP","14.5161"])
    time.sleep(0.1)


    for z in range(1,8):
        strings = "BR:A1-BI{BPM:"+str(z)+"}Kx-SP"
        call(["caput",strings,"9.9331"])
        time.sleep(0.1)
        strings = "BR:A1-BI{BPM:"+str(z)+"}Ky-SP"
        call(["caput",strings,"11.5073"])
        time.sleep(0.1)

        strings = "BR:A2-BI{BPM:"+str(z)+"}Kx-SP"
        call(["caput",strings,"9.9331"])
        time.sleep(0.1)
        strings = "BR:A2-BI{BPM:"+str(z)+"}Ky-SP"
        call(["caput",strings,"11.5073"])
        time.sleep(0.1)

        strings = "BR:A3-BI{BPM:"+str(z)+"}Kx-SP"
        call(["caput",strings,"9.9331"])
        time.sleep(0.1)
        strings = "BR:A3-BI{BPM:"+str(z)+"}Ky-SP"
        call(["caput",strings,"11.5073"])
        time.sleep(0.1)

        strings = "BR:A4-BI{BPM:"+str(z)+"}Kx-SP"
        call(["caput",strings,"9.9331"])
        time.sleep(0.1)
        strings = "BR:A4-BI{BPM:"+str(z)+"}Ky-SP"
        call(["caput",strings,"11.5073"])
        time.sleep(0.1)

    call(["caput","BR:DS-BI{BPM:1}Kx-SP","8.2405"])
    time.sleep(0.1)
    call(["caput","BR:DS-BI{BPM:1}Ky-SP","14.5161"])
    time.sleep(0.1)

    call(["caput","BR:XS-BI{BPM:1}Kx-SP","8.2405"])
    time.sleep(0.1)
    call(["caput","BR:XS-BI{BPM:1}Ky-SP","14.5161"])
    time.sleep(0.1)

    call(["caput","BR:XS-BI{BPM:2}Kx-SP","8.2405"])
    time.sleep(0.1)
    call(["caput","BR:XS-BI{BPM:2}Ky-SP","14.5161"])
    time.sleep(0.1)

    call(["caput","BR:CS-BI{BPM:1}Kx-SP","8.2405"])
    time.sleep(0.1)
    call(["caput","BR:CS-BI{BPM:1}Ky-SP","14.5161"])
    time.sleep(0.1)

    call(["caput","BR:CS-BI{BPM:2}Kx-SP","8.2405"])
    time.sleep(0.1)
    call(["caput","BR:CS-BI{BPM:2}Ky-SP","14.5161"])
    time.sleep(0.1)

    call(["caput","BR:DS-BI{BPM:2}Kx-SP","8.2405"])
    time.sleep(0.1)
    call(["caput","BR:DS-BI{BPM:2}Ky-SP","14.5161"])
    time.sleep(0.1)

    call(["caput","BR:IS-BI{BPM:1}Kx-SP","8.2405"])
    time.sleep(0.1)
    call(["caput","BR:IS-BI{BPM:1}Ky-SP","14.5161"])
    time.sleep(0.1)

#Set Bba values
    ln_bbax = ["0.0287821041","-0.0973749999","0.4268549583","0.0713667369","0.4983648204"]
    ln_bbay = ["0.3727871148","-0.2674428003","0.399940092","-0.2181965229","-0.4371263469"]
    for z in range(1,6):
        strings = "LN-BI{BPM:"+str(z)+"}BbaXOff-SP"
        call(["caput",strings,ln_bbax[z-1]])
        time.sleep(0.1)
        strings = "LN-BI{BPM:"+str(z)+"}BbaYOff-SP"
        call(["caput",strings,ln_bbay[z-1]])
        time.sleep(0.1)

    for z in range(1,10):
        strings = "BTS-BI{BPM:"+str(z)+"}BbaXOff-SP"
        call(["caput",strings,"0"])
        time.sleep(0.1)
        strings = "BTS-BI{BPM:"+str(z)+"}BbaYOff-SP"
        call(["caput",strings,"0"])
        time.sleep(0.1)

    call(["caput","BR:IS-BI{BPM:2}BbaXOff-SP","-0.140219912075"])
    time.sleep(0.1)
    call(["caput","BR:IS-BI{BPM:2}BbaYOff-SP","0.0180236227845"])
    time.sleep(0.1)

    br_a1_bbax = ["-0.102849038097","-0.129979227975","-0.0680155080704","0.0411592239094",
                  "-0.00271993745902","-0.0819695150261","-0.0397013273858"]
    br_a1_bbay = ["0.165690300789","-0.0345504527271","0.142366555027","-0.0715309609072",
                  "-0.173928575357","0.201784842255","-0.034041944682"]
    br_a2_bbax = ["0.294054285156","0.050083170889","0.387847278277","0.167252465211",
                  "-0.0554533853257","0.109171170631","0.235865911929"]
    br_a2_bbay = ["0.00590747902577","0.120241379225","0.215468467703","-0.0505114405736",
                  "0.290799605014","0.301140088275","-0.0164559935519"]
    br_a3_bbax = ["-0.013926336556","-0.0460273983497","0.200933035912","0.0411284645804",
                  "0.0580993394403","0.17604970466","-0.0210982718785"]
    br_a3_bbay = ["0.10224410635","0.369804386629","0.0889835727677","0.331063715198",
                  "0.102618460389","-0.0547637113908","0.0509669090125"]
    br_a4_bbax = ["-0.0666288446529","0.0970684043585","0.104765659853","0.186682446246",
                  "-0.156176033105","0.0829666412471","-0.00261307787501"]
    br_a4_bbay = ["-0.184239086531","0.113484997559","-0.0128779612529","-0.0875547536366",
                  "-0.00193496039279","0.154548290224","-0.070054789428"]
    for z in range(1,8):
        strings = "BR:A1-BI{BPM:"+str(z)+"}BbaXOff-SP"
        call(["caput",strings,br_a1_bbax[z-1]])
        time.sleep(0.1)
        strings = "BR:A1-BI{BPM:"+str(z)+"}BbaYOff-SP"
        call(["caput",strings,br_a1_bbay[z-1]])
        time.sleep(0.1)

        strings = "BR:A2-BI{BPM:"+str(z)+"}BbaXOff-SP"
        call(["caput",strings,br_a2_bbax[z-1]])
        time.sleep(0.1)
        strings = "BR:A2-BI{BPM:"+str(z)+"}BbaYOff-SP"
        call(["caput",strings,br_a2_bbay[z-1]])
        time.sleep(0.1)

        strings = "BR:A3-BI{BPM:"+str(z)+"}BbaXOff-SP"
        call(["caput",strings,br_a3_bbax[z-1]])
        time.sleep(0.1)
        strings = "BR:A3-BI{BPM:"+str(z)+"}BbaYOff-SP"
        call(["caput",strings,br_a3_bbay[z-1]])
        time.sleep(0.1)

        strings = "BR:A4-BI{BPM:"+str(z)+"}BbaXOff-SP"
        call(["caput",strings,br_a4_bbax[z-1]])
        time.sleep(0.1)
        strings = "BR:A4-BI{BPM:"+str(z)+"}BbaYOff-SP"
        call(["caput",strings,br_a4_bbay[z-1]])
        time.sleep(0.1)

    call(["caput","BR:DS-BI{BPM:2}BbaXOff-SP","0.090407291753"])
    time.sleep(0.1)
    call(["caput","BR:DS-BI{BPM:2}BbaYOff-SP","-0.100549378366"])
    time.sleep(0.1)

    call(["caput","BR:IS-BI{BPM:1}BbaXOff-SP","0.179780705471"])
    time.sleep(0.1)
    call(["caput","BR:IS-BI{BPM:1}BbaYOff-SP","-0.155852879961"])
    time.sleep(0.1)

    call(["caput","BR:CS-BI{BPM:1}BbaXOff-SP","-0.0842173786469"])
    time.sleep(0.1)
    call(["caput","BR:CS-BI{BPM:1}BbaYOff-SP","-0.0324316266639"])
    time.sleep(0.1)

    call(["caput","BR:CS-BI{BPM:2}BbaXOff-SP","-0.0183678439664"])
    time.sleep(0.1)
    call(["caput","BR:CS-BI{BPM:2}BbaYOff-SP","0.274806548987"])
    time.sleep(0.1)

    call(["caput","BR:DS-BI{BPM:1}BbaXOff-SP","0.090407291753"])
    time.sleep(0.1)
    call(["caput","BR:DS-BI{BPM:1}BbaYOff-SP","-0.100549378366"])
    time.sleep(0.1)

    call(["caput","BR:XS-BI{BPM:1}BbaXOff-SP","-0.112173597745"])
    time.sleep(0.1)
    call(["caput","BR:XS-BI{BPM:1}BbaYOff-SP","0.44243666677"])
    time.sleep(0.1)

    call(["caput","BR:XS-BI{BPM:2}BbaXOff-SP","0.0672990614957"])
    time.sleep(0.1)
    call(["caput","BR:XS-BI{BPM:2}BbaYOff-SP","0.070444132964"])
    time.sleep(0.1)
