"""Script sets PDU PVs OFF for SR"""
#!/usr/bin/python

from epics import caput

cells = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30"]
bpms = [7,9,9,11,10,7,11,9,7,9,9,11,7,7,7,9,10,9,11,7,9,7,10,7,7,7,7,9,7,11]

for dex, cell in enumerate(cells):
    cstr = str(cell)
    for bpm in range(1,7):
        ptp = 'SR:C'+cstr+'-CS{PDU:RGD1A}Cmd:Outlet'+str(bpm+1)+'-Sel'
        caput(ptp, 1)


    if (bpms[dex] == 9):
        ptp = 'SR:C'+cstr+'-CS{PDU:RGD1A}Cmd:Outlet8-Sel'
        caput(ptp, 1)
        ptp = 'SR:C'+cstr+'-CS{PDU:RGD1B}Cmd:Outlet1-Sel'
        caput(ptp, 1)


    if (bpms[dex] == 10):
        if cell == "23":
            ptp = 'SR:C'+cstr+'-CS{PDU:RGD1A}Cmd:Outlet8-Sel'
            caput(ptp, 1)
            ptp = 'SR:C'+cstr+'-CS{PDU:RGD1B}Cmd:Outlet2-Sel'
            caput(ptp, 1)
            ptp = 'SR:C'+cstr+'-CS{PDU:RGD1B}Cmd:Outlet3-Sel'
            caput(ptp, 1)

        else:
            ptp = 'SR:C'+cstr+'-CS{PDU:RGD1A}Cmd:Outlet8-Sel'
            caput(ptp, 1)
            ptp = 'SR:C'+cstr+'-CS{PDU:RGD1B}Cmd:Outlet1-Sel'
            caput(ptp, 1)
            ptp = 'SR:C'+cstr+'-CS{PDU:RGD1B}Cmd:Outlet2-Sel'
            caput(ptp, 1)


    if (bpms[dex] == 11):
        for bpm in range(1,5):
            if (cell == "04") or (cell == "30"):
                ptp = 'SR:C'+cstr+'-CS{PDU:RGD2A}Cmd:Outlet'+str(bpm)+'-Sel'
                caput(ptp, 1)

            elif (cell == "12"):
                ptp = 'SR:C'+cstr+'-CS{PDU:RGD1B}Cmd:Outlet'+str(bpm)+'-Sel'
                caput(ptp, 1)

            else:
                ptp = 'SR:C'+cstr+'-CS{PDU:RGD2}Cmd:Outlet'+str(bpm)+'-Sel'
                caput(ptp, 1)


