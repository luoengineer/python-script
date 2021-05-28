import ctypes
from ctypes import *
import time
from cmdServ import cmdservdll, devUsbIndex, devSffChannel
from cmdServ import Sfp_Factory_Pwd_Entry, AteAllPowerOn, AteAllPowerOff, openUsbDevice
from cmdServ import getAdc0, adc02TempIndex


#Test times
#wr_and_rd_times  = 5
run_time_second = 120  # unit : s
# user type for password
is_088_Module = 0
is_other_Module = 1
user_password_type = is_other_Module

#Product list
ComboSfpI2cAddr = [0xA0,0xA2,0xB0,0xB2,0xA4]
SfpI2cAddr = [0xA0,0xA2,0xA4]
XfpI2dAddr = [0xA0,0xA4]

#load dll
objdll = ctypes.cdll.LoadLibrary(".\ATEAPI.dll")

#########################################################
#               Inner Funtion
#########################################################


#########################################################
#               Open USB Device
#########################################################
#TODO: How to config several usb device
openUsbDevice(devUsbIndex)

#########################################################
#               Slot Power On
#########################################################
AteAllPowerOn(devUsbIndex)
time.sleep(2)
#########################################################
#               Entry Password
#########################################################
Sfp_Factory_Pwd_Entry(user_password_type)
time.sleep(1)

#########################################################
#               Command Sevices
#########################################################
# Read firmware version
strCmdIn = create_string_buffer(b'MCU_GET_VERSION()')
strCmdOutBuff = ctypes.c_ubyte*64
strCmdOut = strCmdOutBuff()
strFwVer = []
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    strFwVer = [chr(strCmdOut[item]) for item in range(len(strCmdOut)) if 0 != strCmdOut[item]]
else:
    print("Can't get firmware version, stop test ! ")
    sys.exit()
strFwVer = ''.join(strFwVer)


#########################################################
#                 Open File
#########################################################
startTick = time.time()
endTick = startTick + run_time_second
#dateTime = time.strptime(time.asctime())
dateTime = time.strptime(time.asctime( time.localtime(startTick)))
dateTime = "{:4}-{:02}-{:02} {:02}:{:02}:{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
testTitle = strFwVer
fileName = strFwVer+'.txt'
f = open(fileName, 'a+')
time.sleep(1)
print("\n****************************************************************************")
print("EFM8LB11F16E PowOn Temperature test, start time : {}".format(dateTime))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nEFM8LB11F16E PowOn Temperature test, start time : {}".format(dateTime))
f.write("\n****************************************************************************")
print("{}".format(testTitle))
f.write('\n'+testTitle)

#########################################################
#               Get temperature index
#########################################################
#for cnt in range(wr_and_rd_times):
while time.time() < endTick:
    strCmdOutBuff = ctypes.c_ubyte*32
    strCmdOut = strCmdOutBuff()
    strCmdOut = getAdc0()
    if 0 != strCmdOut:
        print("\n\nADC 0(Hex):")
        f.write('\n\nMCU_GET_ADC 0 :')
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
    else:
        print("Can't get ADC 0 ")
        f.write("Can't get ADC 0 ")

    caseTemp = objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 96, 2, strCmdOut)
    print("\nA2[96-97] = 0x{:2X},0x{:2X}, Case temperature : {:3f}°".format(strCmdOut[0], strCmdOut[1], \
        (strCmdOut[0]*256+strCmdOut[1])/256))
    f.write("\nA2[96-97] = 0x{:2X},0x{:2X}, Case temperature : {:3f}°".format(strCmdOut[0], strCmdOut[1], \
        (strCmdOut[0] * 256 + strCmdOut[1]) / 256))



dateTime = time.strptime(time.asctime())
dateTime = "{:4}-{:02}-{:02} {:02}:{:02}:{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
print("\n****************************************************************************")
print("EFM8LB11F16E PowOn Temperature test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nEFM8LB11F16E PowOn Temperature test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
f.write("\n****************************************************************************")
AteAllPowerOff(devUsbIndex)
f.close()

