"""BPM Class
Updated to Python3 1/31/2024 M. Capotosto"""
#!/usr/bin/python
import socket
import sys
import binascii
import struct
import time
import telnetlib
import re
from io import StringIO
from select import select
from bpm_addresses import *

def print_status_header():
    '''Prints BPM Status header'''
    print()
    print("bpm     ip               moxa              mode     fpga_ver  ublz_ver PLL Lock")
    print("-------------------------------------------------------------------------------")


def spinning(timeout):
    round = 0
    type = 0
    while round != timeout:

        if type == 0:
            sys.stdout.write("\b/")
        if type == 1:
            sys.stdout.write("\b-")
        if type == 2:
            sys.stdout.write("\b\\")
        if type == 3:
            sys.stdout.write("\b|")
        type += 1
        if type == 4:
            type = 0
            round += 1
            sys.stdout.write("\b*|")
        sys.stdout.flush()
        time.sleep(0.25)
    #print"\b\b  Done"
    #print


def prompt(timeout):
    sys.stdout.write(">")
    sys.stdout.flush()

    rlist, _, _ = select([sys.stdin], [], [], timeout)

    sys.stdout.write("\b\b")
    sys.stdout.flush()
    if rlist:
        s = str(sys.stdin.readline())
        return s.strip("\r\n")
    else:
        return


class Bpm():
    def __init__(self,addr):
        self.ip_connected = False
        self.moxa_connected = False
        self.ip_addr = addr[0]
        self.moxa_addr = addr[1]
        self.moxa_port = addr[2]
        self.prefix = addr[3]
        self.stat = "undefined"
        self.mode = "???"
        self.ublz_ver = -1
        self.SN = -1
        self.ecodeval = ""
        self.ecodeset = ""
        self.area = ""
        self.eeaddr = ""
        self.eeval = ""
        self.cmdval = ""
        self.ee_r = []
        #connect to moxa
        #self.moxa_connect()
        # connect to socket
        #self.ip_connect()

        #if self.ip_connected and self.moxa_connected:
	#    pass
            #print "Socket Connected: %s\tMoxa Connected:%s:%s" % (addr[0],addr[1],addr[2])


    def moxa_connect(self):
        """connect to moxa"""
        try:
            self.tn = telnetlib.Telnet(self.moxa_addr,self.moxa_port,4)
            self.moxa_connected = True
        except:
            print("connect to ",self.prefix," failed")


    def ip_connect(self):
        '''connect to socket'''
        attempts = 0
        while not self.ip_connected and attempts < 3:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            bpm_address = (self.ip_addr, 65000)
            attempts += 1
            try:
                self.sock.settimeout(2)
                self.sock.connect(bpm_address)
                self.ip_connected = True
                #print "ip=%s connected" % self.ip_addr
            except: #self.socket.error, msg:
                time.sleep(1)
                if self.sock:
                    self.sock.close()
                   #print "ip=%s not connected" % self.ip_addr
                   #print "Could not open socket: "  #%s " % msg

    def ip_close(self):
        '''Close socket'''
        if self.ip_connected:
            self.sock.close()
            self.ip_connected = False


    def moxa_close(self):
        '''Close moxa connection'''
        if self.moxa_connected:
            self.tn.close()
            self.moxa_connected = False

    def __del__(self):
        #print "Goodbye"
        if self.moxa_connected:
            self.tn.close()
        if self.ip_connected:
            self.sock.close()

    def read_mode(self):
        '''Read if BPM is in App or UPGRADE Modes'''
        if self.moxa_connected:
            self.tn.write(b"\r\n")
            time.sleep(0.2)
            resp = self.tn.read_very_eager()
            if resp.find(b"SR:") != -1:
                self.area = "SR"
            elif resp.find(b"BOOST") != -1:
                self.area = "BOOST"
            elif resp.find(b"LTB") != -1:
                self.area = "LTB"
            elif resp.find(b"LINAC") != -1:
                self.area = "LINAC"
            elif resp.find(b"BTS") != -1:
                self.area = "BTS"
            elif resp.find(b"FirmwareUpgrade") != -1:
                self.area = "upgrade"
            else:
                self.area = "???"
            if resp.find(b"SR:") != -1 or resp.find(b"BOOST") != -1 or \
               resp.find(b"LTB:") != -1 or resp.find(b"LINAC:") != -1 or \
               resp.find(b"BTS:") != -1:
                self.mode = "app"
            elif resp.find(b"FirmwareUpgrade") != -1:
                self.mode = "upgrade"
            else:
                self.mode = "???"
        else:
            self.mode = "???"
        #time.sleep(1)

    def switch_mode(self,mode):
        '''Switch mode from APP to UPGRADE or vice versa'''
        if self.moxa_connected:
            #going to lose tcp connection
            self.ip_close()
            self.read_mode()
            if self.mode == "app"  and mode == "UPG":
                print ("In App mode.  Switching to Upgrade mode...")
                self.tn.write(b"reboot 1\r\n")
            if self.mode == "upgrade" and mode == "APP":
                print ("In Upgrade Mode.  Switching to APP mode...")
                self.tn.write(b"reboot app\r\n")

    def get_SN(self):
        '''Read Board S/N'''
        if self.moxa_connected:
            self.tn.write(b"\r\n")
            time.sleep(0.2)
            resp = self.tn.read_until('#',1)
            self.tn.write(b"ipget\r\n")
            time.sleep(0.2)
            resp = self.tn.read_until('?',1)
            self.tn.write(b"n\r\n")
            time.sleep(0.2)
            resp = self.tn.read_until('Board S/N:',1)
            resp = self.tn.read_until('\r\n',1)
            try:
                self.SN=int(resp)
            except:
                self.SN = -3
            resp = self.tn.read_until('#',1)
        else:
            self.SN = -2

#    def sw_mode_status(self,mode):
#        if mode == "UPG":
#

    def reboot(self):
        '''Reboot BPM into APP mode'''
        self.tn.write(b"\r\n")
        self.tn.read_until("#",1)
        self.tn.write(b"reboot app\r\n")

    def ecode(self):
        '''Set Event Code'''
        self.tn.write(b"\r\n")
        self.tn.read_until("#",1)
        stufftosend = (b"evr-set " + self.ecodeval + b" " + self.ecodeset + b"\r\n")
        self.tn.write(stufftosend)

    def eew(self):
        '''Write to EEPROM'''
        self.tn.write(b"\r")
        time.sleep(0.25)
        resp = self.tn.read_very_eager()
        #print self.moxa_port,resp
        self.tn.write(b"ee -w\r")
        time.sleep(0.25)
        resp = self.tn.read_very_eager()
        #print self.moxa_port,resp
        stufftosend = self.eeaddr + "\r"
        self.tn.write(stufftosend)
        time.sleep(0.25)
        resp = self.tn.read_very_eager()
        #print self.moxa_port,resp
        stufftosend = self.eeval + "\r"
        self.tn.write(stufftosend)
        time.sleep(0.25)
        resp = self.tn.read_very_eager()
        #print self.moxa_port,resp
        self.tn.write(b"y")
        time.sleep(0.25)
        self.tn.write(b"\r")

    def cmd(self):
        '''Write Command to BPM'''
        self.tn.write(b"\r")
        time.sleep(0.25)
        resp = self.tn.read_very_eager()
        stufftosend = self.cmdval + "\r"
        self.tn.write(stufftosend)

    def switch_mode_wait(self,mode):
        '''Switch between APP and UPGRADE Modes'''
        self.tn.write(b"\r\n")
        time.sleep(0.5)
        resp = self.tn.read_very_eager()
        self.read_mode()
        if self.mode == "app"  and mode == "UPG":
            print ("In App mode.  Switching to Upgrade mode...")
            self.ip_close() #going to lose ip connection
            self.tn.write(b"reboot 1\r\n")
            time.sleep(0.5)
            self.tn.read_until("FirmwareUpgrade->",10)
            self.ip_connect()
            self.tn.write(b"\r\n")
        elif self.mode == "upgrade"  and mode == "APP":
            print ("In Upgrade Mode.  Switching to APP mode...")
            self.ip_close()
            self.tn.write(b"reboot app\r\n")
            time.sleep(0.5)
            self.tn.read_until("SR:",15)
            time.sleep(3)
            self.ip_connect()
            self.tn.write(b"\r\n")
        else:
            print ("Current Mode = ", self.mode)


    def start_update(self,update_type):
        '''Firmware Update'''
        fpgabit_blksize = 18033 #blk size = 512bytes, total len = 9304576
        srec0_blksize   = 2579  #blk size = 512bytes, total len =
        srec1_blksize   = 2200

	# Update firmware
	#print "Downloading Firmware..."
        if update_type == "fpga":
            self.tn.write(b"bin\r\n")
            self.blksize = fpgabit_blksize
        elif update_type == "app":
            self.tn.write(b"srec\r\n")
            self.blksize = srec0_blksize
            self.tn.write(b"0\r\n")
        else:
            print("Invalid Update type")
            return "INV"
        self.blocks_rcvd = 0


    def check_update_download(self):
        '''Check update download status'''
        resp = self.tn.read_very_eager()
        if resp.find("Successfully done") == -1:
            self.blocks_rcvd += resp.count("#")
            perc_done = int(self.blocks_rcvd / float(self.blksize) * 100)
        #print str(perc_done) + " %\r",
        #sys.stdout.flush()
        #print "Blocks Received = " + str(blocks_rcvd)
        #time.sleep(1)
        else:
            perc_done = 100
        return perc_done

    def check_update_eraseflash(self):
        '''Check if flash erased successfully'''
        resp = self.tn.read_very_eager()
        if resp.find("Flash memory contents successfully") == -1:
            return False
        else:
            return True

    def check_update_progflash(self):
        '''Check if flash programmed successfully'''
        resp = self.tn.read_very_eager()
        if resp.find("!!!PASS...!!!") == -1:
            return False
        else:
            return True



#    def update(self,update_type):
#        fpgabit_blksize = 18033 #blk size = 512bytes, total len = 9304576
#        srec0_blksize   = 2579  #blk size = 512bytes, total len =
#        srec1_blksize   = 2200
#
#	# Update firmware
#	print "Downloading Firmware..."
#	if update_type == "fpga":
#	  self.tn.write("bin\r\n")
#	  blksize = fpgabit_blksize
#	elif update_type == "app":
#	  self.tn.write("srec 0\r\n")
#	  blksize = srec0_blksize
#	else:
#	  print "Invalid Update type"
#	  return "INV"
#
#        resp = ""
#        blocks_rcvd = 0
#
#        time.sleep(1)
#        while resp.find("Successfully done") == -1:
#            resp = self.tn.read_very_eager()
#            if len(resp) == 0:
#                print "Error: BPM not responding"
#                sys.exit()
#            blocks_rcvd += resp.count("#")
#            perc_done = int(blocks_rcvd / float(blksize) * 100)
#            print str(perc_done) + " %\r",
#            sys.stdout.flush()
#            #print "Blocks Received = " + str(blocks_rcvd)
#            time.sleep(1)
#
#
#        print "\r\n"
#        print "Erasing Flash..."
#        if len(self.tn.read_until("Flash memory contents successfully",300)) == 0:
#           print "Error : Erasing Flash"
#           flash_success = 0
#        else:
#           print "Flash Erased Successfully..."
#           flash_success = 1
#
#
#        print "Programming Flash..."
#        if len(self.tn.read_until("!!!PASS...!!!",60)) == 0:
#           print "Error : Programming Flash"
#           flash_success = 0
#        else:
#           print "Flash Programming Pass"
#           flash_success = 1

    def read_PLLock(self):
        '''Read PLL Lock Status'''
        self.ublz_io_status_reg = self.read_reg(3,15)
        self.PLLock = "F"
        if self.ip_connected:
            if self.ublz_io_status_reg & 2:
                self.PLLock = "T"
        else:
            self.PLLock = "F"
        return self.PLLock

    def read_fpgaver(self):
        '''Read FPGA Version'''
        self.fpga_ver = self.read_reg(3,51)
        return self.fpga_ver


    def read_ublzver(self):
        '''Read Microblaze Version'''
        self.read_mode()
        if self.mode == "app":
            self.ublz_ver = self.read_reg(6,113)
            return self.ublz_ver
        if self.mode == "upgrade":
            self.tn.write(b"ver\r\n")
            time.sleep(0.25)
            resp = self.tn.read_very_eager()
            idx = resp.find('.')
            #print resp
            #print "Index = %d" % idx
            #print "Version = %s" % resp[idx-2:idx+9]
            #print resp[idx+1:idx+2]
            if resp[idx+1:idx+3] == "11":
                self.ublz_ver = float(resp[idx-2:idx+3])
            else:
                self.ublz_ver = float(resp[idx-2:idx+9])



    def read_reg(self,opmode,address):
        """ Return the BPM firmware version via TCP/IP """
        # form the query packet to be sent to BPM
        if self.ip_connected:
            reg = -1
            #print "ip=%s\topmode=%d\taddr=%d" % (self.ip_addr,opmode,address)
            req_op = opmode
            req_addr = address
            req_len = 1
            req_data = 8
            command = (req_op, req_addr, req_len, req_data)
            packer = struct.Struct('>IIII')
            packed_data = packer.pack(*command)

            try:
                # Send data
                #print 'Sending "%s"' % binascii.hexlify(packed_data), command
                self.sock.sendall(packed_data)
                time.sleep(0.5)
                # Look for the response
                data_received = 0
                data_expected = 16
                data = self.sock.recv(16)
                #print 'Data received '
                amount_received = len(data)
                #print 'Bytes received %d' % amount_received
                #print 'received "%s"' % binascii.hexlify(data)
                reg = (struct.unpack('>I',data))[0]
                #print str(type(fpga_ver))
                #print 'received %d' % fpga_ver
            except:
                pass
                #print "Error sending"

            finally:
                #sock.close()
                return reg
        else:
            return -1




    def get_status(self,bpmnum):
        """ Get and Print basic status"""
        #print "bpmnum=%d" % bpmnum
        self.read_mode()
        self.read_fpgaver()
        self.read_ublzver()
        self.read_PLLock()

        #stat =  "%2s   " % (bpmnum+1)
        stat = f"{bpmnum + 1:2}"
        stat += f'\033[{92 if self.ip_connected else 91}mip={self.ip_addr}'
        stat += f'\033[{92 if self.moxa_connected else 91}mip={self.moxa_addr,":",self.moxa_port}'
        #if self.ip_connected:
        #    stat += "\033[92mip=%s   " % (self.ip_addr)
        #else:
        #    stat += "\033[91mip=%s   " % (self.ip_addr)
        #if self.moxa_connected:
        #    stat += "\033[92mmoxa=%s:%s   " % (self.moxa_addr,self.moxa_port)
        #else:
        #    stat += "\033[91mmoxa=%s:%s   " % (self.moxa_addr,self.moxa_port)
        stat += "\033[0m"
        stat += self.area + "\t"
        stat += str(self.fpga_ver) + "\t"
        stat += str(self.ublz_ver) + "\t"
        stat += self.PLLock + "\t"
        self.stat = stat
        return stat


    def sgain(self,data):
        """ send sgain file to bpm """
        self.tn.write(b"\r\n")
        time.sleep(0.25)
        resp = self.tn.read_until("#",1)
        self.tn.write(b"sgain\r\n")
        time.sleep(0.25)
        resp = self.tn.read_until(":",1)
        for c in range(len(data)):
            self.tn.write(data[c])
            time.sleep(0.01)
        time.sleep(0.25)
        resp = self.tn.read_until("OK...",1)
        self.gain = resp[-5:]

    def frsgain(self):
        """ read sgain data from bpm """
        self.tn.write(b"\r\n")
        time.sleep(0.25)
        self.tn.read_until("#",1)
        self.tn.write(b"frsgain\r\n")
        time.sleep(0.75)
        self.tn.read_until(b"------------------------------",1)
        self.tn.read_until(b"------------------------------",1)
        resp = self.tn.read_until(b"------------------------------",1)
        resp = resp[4:-31]
        resp = resp.replace(':',',')
        resp = resp.replace(' ','')
        resp = resp.replace('\n',',')
        resp = resp.replace('\r','')
        resp += "#"
        self.gain = resp

    def read_ee_r(self):
        """ read eeprom data from bpm """
        if self.moxa_connected:

            self.tn.write(b"\r\n")
            time.sleep(0.75)
            self.tn.read_until(b"#",1)
            self.tn.write(b"ee -r\r\n")
            time.sleep(1.25)
            resp = self.tn.read_until(b"#",1)
            bad_words = ['TBT:', 'ADC:','Get','bytes','trig'] #,'offset']
            buf = StringIO.StringIO(resp)
            resp2=''
            for line in buf:
                if not any(bad_word in line for bad_word in bad_words):
                    resp2=resp2+line

            # fancy number search pattern
            numeric_const_pattern = \
            '[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
            rx = re.compile(numeric_const_pattern, re.VERBOSE)

            hexnum = re.findall(r"0x[0-9a-f]+",resp2)
	    #numbers = re.findall(r"[-+]?\d*\.\d+|\d+", resp2)
            numbers = rx.findall(resp2)
	    #print numbers
            if len(numbers)>61:
                self.ee_r = [numbers[1],numbers[2],numbers[3],numbers[10],numbers[11],numbers[12],\
                    numbers[13],numbers[14],numbers[15],numbers[16],numbers[17],numbers[18],\
                    numbers[19],numbers[20],numbers[21],numbers[22],numbers[23],numbers[24],\
                    numbers[25],numbers[26],numbers[27],numbers[28],numbers[29],numbers[30],\
                    numbers[31],numbers[34],numbers[35],numbers[38],numbers[39],numbers[40],\
                    numbers[41],numbers[42],numbers[43],numbers[44],numbers[45],numbers[46],\
                    numbers[47],numbers[48],numbers[49],numbers[50],numbers[51],numbers[52],\
                    numbers[53],numbers[54],numbers[55],numbers[56],numbers[57],hexnum[0],\
                    numbers[60],numbers[61]]
            self.moxa_close()


if __name__ == "__main__":


    srcells = [c01, c02, c03, c04]

    #list of bpm objects
    b = []

    total = len(sys.argv)
    if total != 3:
        print("Usage:  bpm_class [status:update:mode]  <cell#> ")
        sys.exit(0)
    else:
        print("Mode = %s" % sys.argv[1])


    if sys.argv[1] == "status":
        if sys.argv[2].isdigit and int(sys.argv[2]) < 30 and int(sys.argv[2]) > 0:
            cellnum = int(sys.argv[2])
            cell = srcells[int(cellnum)]
            print("BPM's in cell", cellnum)

            #create objects, open connections
            for i in range(0,6):
                b.append(bpm(cell[i]))

            #print basic status
            print_status_header()
            for i in range(0,6):
                print(b[i].get_status())

        else:
            print("Invalid Cell Number")
    else:
        print("Invalid Option")



#    #switch to upgrade mode
#    sys.stdout.write( "Switching Cell to Upgrade Mode...  ")
#    for i in range(0,6):
#       b[i].switch_mode("UPG")
#    spinning(15)
#    print
#
#    #re-connect to socket
#    for i in range(0,6):
#      b[i].ip_connect()
#
#    #print basic status
#    print_status_header()
#    for i in range(0,6):
#       print b[i].get_status()
#
#
#    #update
#    print "Updating..."
#    for i in range(0,6):  b[i].start_update("app")
#    perc_done = [0,0,0,0,0,0]
#    while (sum(perc_done) < 600):
#         stat = ""
#         for i in range(0,6) : perc_done[i] = b[i].check_update_download()
#         for i in range(0,6) : stat += str(perc_done[i])+"%\t"
#         print stat + "\r",
#         sys.stdout.flush()
#         time.sleep(1)
#
#    print "Erasing Flash..."
#    while b[0].check_update_eraseflash() == False:
#          spinning(1)
#
#    print "Programming Flash..."
#    while b[0].check_update_progflash() == False:
#          spinning(1)
#
#
#
#
#    #switch to app mode
#    sys.stdout.write( "Switching Cell to App Mode...  ")
#    for i in range(0,6):
#       b[i].switch_mode("APP")
#    spinning(15)
#
#    #re-connect to socket
#    for i in range(0,6):
#      b[i].ip_connect()
#
#
#    #print basic status
#    print_status_header()
#    for i in range(0,6):
#       print b[i].get_status()
#
#
#



#    #get basic status
#    for i in range(0,6):
#        b[i].read_mode()
#        b[i].read_fpgaver()
#        b[i].read_ublzver()
#
#    #print ip and moxa information
#    print "bpm     ip                moxa              mode      fgga_ver  ublz_ver"
#    print "------------------------------------------------------------------------"
#
#    for i in range(0,6):
#	  stat =  "%s   " % (i)
#	  if b[i].ip_connected:
#	      stat += "\033[92mip=%s   " % (b[i].ip_addr)
#	  else:
#	      stat += "\033[91mip=%s   " % (b[i].ip_addr)
#	  if b[i].moxa_connected:
#	      stat += "\033[92mmoxa=%s:%s   " % (b[i].moxa_addr,b[i].moxa_port)
#	  else:
#	      stat += "\033[91mmoxa=%s:%s   " % (b[i].moxa_addr,b[i].moxa_port)
#	  stat += "\033[0m"
#	  #print mode
#	  stat += b[i].mode + "\t"
#	  stat += str(b[i].fpga_ver) + "\t"
#	  stat += str(b[i].ublz_ver) + "\t"
#	  print stat
#





    #print ip and moxa information
#    for i in range(0,6):
#          stat =  "bpm %s\t" % (i)
#          if b[i].ip_connected:
#              stat += "\033[92mip=%s\t" % (b[i].ip_addr)
#          else:
#              stat += "\033[91mip=%s\t" % (b[i].ip_addr)
#          if b[i].moxa_connected:
#              stat += "\033[92mmoxa=%s:%s\t" % (b[i].moxa_addr,b[i].moxa_port)
#          else:
#              stat += "\033[91mmoxa=%s:%s\t" % (b[i].moxa_addr,b[i].moxa_port)
#          print stat + "\033[0m"
#
#
#
#    #print mode (app or upgrade)
#    print ""
#    for i in range(0,6):
#          stat =  "bpm %s\tmode: " % (i)
#          if b[i].moxa_connected:
#              print stat + str(b[i].read_mode())



#          else:
#              print stat + "Error Connecting to MOXA"
#
#
#
#    #print fpga version number
#    print ""
#    for i in range(0,6):
#          stat =  "bpm %s\tfpga version: " % (i)
#          if b[i].ip_connected:
#              print stat + str(b[i].read_fpgaver())
#          else:
#              print stat + "Error Connecting to IP"
#
#    #print ublz version number
#    print ""
#    for i in range(0,6):
#          stat =  "bpm %s\tublz version: " % (i)
#          if b[i].ip_connected:
#              print stat + str(b[i].read_ublzver())
#          else:
#              print stat + "Error Connecting to IP"
#




#    a.append(bpm(srbpm2))
#    a.append(bpm(srbpm3))


#    a[0] = bpm(srbpm1)
#    a[1] = bpm(srbpm2)
#    a[2] = bpm(srbpm3)

#    for i in range(0,7):
#        b.appendi] = bpm(c1[i])


#    b = bpm(addr)
#
#    if (b.moxa_connected and b.ip_connected) != True:
#        sys.exit(0)
#    for i in range(0,4):
#        print "Reading Mode"
#        mode = b.get_mode()
#        print "Mode = %s" % mode
#        #time.sleep(2)
#
#    fpgaver = b.read_reg(51)
#    print "FPGA ver = %d" % fpgaver
#
#    print "Switching Mode"
#    if mode == "UPG":
#        b.switch_mode("APP")
#    else:
#        b.switch_mode("UPG")
#
#    print "Reading Mode"
#    mode = b.get_mode()
#    print "Mode = %s" % mode
#
