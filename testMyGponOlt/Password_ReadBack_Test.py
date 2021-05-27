import ctypes
from ctypes import *
import time
import sys
from cmdServ import cmdservdll, Sfp_Factory_Pwd_Entry
from classTestEvb import *

#Test times
wr_and_rd_times  = 2
# user type for password
is_088_Module = 0
is_other_Module = 1
user_password_type = is_other_Module


#Product list
ComboSfpI2cAddr = [0xA0,0xA2,0xB0,0xB2,0xA4]
SfpI2cAddr = [0xA0,0xA2,0xA4]
XfpI2dAddr = [0xA0,0xA4]

devUsbIndex = 0
devSffChannel = 1
devSfpChannel = 2
#########################################################
#               create object
#########################################################
testEvb = cTestEvb(devUsbIndex)


#########################################################
#               Inner Funtion
#########################################################
def Sfp_User_Pwd_Entry():
    i2cWriteBuf = c_ubyte * 4
    userPwd = i2cWriteBuf(0x00, 000, 0x10, 0x11)
    testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 123, 4, byref(userPwd))
    del i2cWriteBuf, userPwd

def read_back_password():
    i2cReadBuf = ctypes.c_ubyte*4
    i2cReadByte = i2cReadBuf()
    Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 123, 4, i2cReadByte)
    if 0 == Res:
        for item in range(len(i2cReadByte)):
            if 0xFF == i2cReadByte[item]:
                print("A2[{}]=0x{:2X},{}".format(123 + item, i2cReadByte[item], 'ok'))
                f.write("\nA2[{}]=0x{:2X},{}".format(123 + item, i2cReadByte[item], 'ok'))
            else:
                print("A2[{}]=0x{:2X},{}".format(123 + item, i2cReadByte[item], 'error'))
                f.write("\nA2[{}]=0x{:2X},{}".format(123 + item, i2cReadByte[item], 'error'))
    else:
        print("Read-back A2[123-126] fail ")
        f.write("Read-back A2[123-126] fail ")

#########################################################
#               Open USB Device
#########################################################
testEvb.openUsbDevice()

#########################################################
#               Slot Power On
#########################################################
testEvb.AteAllPowerOn()
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
dateTime = time.strptime(time.asctime( time.localtime(startTick)))
dateTime = "{:4}-{:02}-{:02} {:02}:{:02}:{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
testTitle = strFwVer
fileName = strFwVer+'.txt'
f = open(fileName, 'a+')
time.sleep(1)
print("\n****************************************************************************")
print("Read-back password test, start time : {}".format(dateTime))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nRead-back password test, start time : {}".format(dateTime))
f.write("\n****************************************************************************")
print("{}".format(testTitle))
f.write('\n'+testTitle)

print("POR...")
f.write("POR...")
#clear any password
testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)

#########################################################
#      no any password read-back A2[123-126]
#########################################################
print("\nno any passsword ...")
f.write("\nno any passsword ...")

print("\nread back A2[123-126] ...")
f.write("\nread back A2[123-126] ...")
read_back_password()

#########################################################
#      write factory password read-back A2[123-126]
#########################################################
print("\nwrite factory passsword ...")
f.write("\nwrite factory passsword ...")
Sfp_Factory_Pwd_Entry(user_password_type)
print("\nread back A2[123-126] ...")
f.write("\nread back A2[123-126] ...")
read_back_password()

print("POR...")
f.write("POR...")
#clear any password
testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)

#write user default write password
print("\nwrite user passsword ...")
f.write("\nwrite user passsword ...")
Sfp_User_Pwd_Entry()
print("\nread back A2[123-126] ...")
f.write("\nread back A2[123-126] ...")
read_back_password()


dateTime = time.strptime(time.asctime())
dateTime = "{:4}-{:02}-{:02} {:02}:{:02}:{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
print("\n****************************************************************************")
print("Read-back password test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nRead-back password test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
f.write("\n****************************************************************************")

testEvb.AteAllPowerOff()
f.close()

