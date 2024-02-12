"""Script sets PDU PVs ON for SR"""
#!/usr/bin/python

from epics import caput

cells = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30"]
bpms = [7,9,9,11,10,7,11,9,7,9,9,11,7,7,7,9,10,9,11,7,9,7,10,7,7,7,7,9,7,11]


for dex, cell in enumerate(cells):
    for bpm in range(1,7):
        cstr = str(cell)
        ptp = 'SR:C'+cstr+'-CS{PDU:RGD1A}Cmd:Outlet'+str(bpm+1)+'-Sel'
        caput(ptp, 'On')

    if (bpms[dex] == 9):
        cstr = str(cell)
        ptp = 'SR:C'+cstr+'-CS{PDU:RGD1A}Cmd:Outlet8-Sel'
        caput(ptp, 'On')
        ptp = 'SR:C'+cstr+'-CS{PDU:RGD1B}Cmd:Outlet1-Sel'
        caput(ptp, 'On')

    if (bpms[dex] == 10):
        if cell == "23":
            cstr = str(cell)
            ptp = 'SR:C'+cstr+'-CS{PDU:RGD1A}Cmd:Outlet8-Sel'
            caput(ptp, 'On')
            ptp = 'SR:C'+cstr+'-CS{PDU:RGD1B}Cmd:Outlet2-Sel'
            caput(ptp, 'On')
            ptp = 'SR:C'+cstr+'-CS{PDU:RGD1B}Cmd:Outlet3-Sel'
            caput(ptp, 'On')
        else:
            cstr = str(cell)
            ptp = 'SR:C'+cstr+'-CS{PDU:RGD1A}Cmd:Outlet8-Sel'
            caput(ptp, 'On')
            ptp = 'SR:C'+cstr+'-CS{PDU:RGD1B}Cmd:Outlet1-Sel'
            caput(ptp, 'On')
            ptp = 'SR:C'+cstr+'-CS{PDU:RGD1B}Cmd:Outlet2-Sel'
            caput(ptp, 'On')

    if (bpms[dex] == 11):
        for bpm in range(1,5):
            if (cell == "04") or (cell == "30"):
                cstr = str(cell)
                ptp = 'SR:C'+cstr+'-CS{PDU:RGD2A}Cmd:Outlet'+str(bpm)+'-Sel'
                caput(ptp, 'On')
            elif (cell == "12"):
                cstr = str(cell)
                ptp = 'SR:C'+cstr+'-CS{PDU:RGD1B}Cmd:Outlet'+str(bpm)+'-Sel'
                caput(ptp, 'On')
            else:
                cstr = str(cell)
                ptp = 'SR:C'+cstr+'-CS{PDU:RGD2}Cmd:Outlet'+str(bpm)+'-Sel'
                caput(ptp, 'On')
