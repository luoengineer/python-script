import ctypes
from ctypes import *
import time
import random
import operator
import sys
import os

path = os.path.dirname(os.path.dirname(__file__))
path = os.path.join(path, 'pyscriptlib')
sys.path.append(path)
from cmdServ import *
from classTestEvb import *

#==============================================================================
# Test times
#==============================================================================
#wr_and_rd_times  = 5
# user type for password
is_088_Module = 0
is_other_Module = 1
user_password_type = is_other_Module


#Product list
ComboSfpI2cAddr = [0xA0,0xA2,0xB0,0xB2,0xA4]
SfpI2cAddr = [0xA0,0xA2,0xA4]
XfpI2cAddr = [0xA0,0xA4]

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
def Sfp_User_Read_099Pwd_Entry():
    i2cWriteBuf = c_ubyte * 4
    user099Pwd = i2cWriteBuf(0x0B, 0x0C, 0x0D, 0x0E)
    testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 128, 4, byref(user099Pwd))

def Sfp_User_Write_099Pwd_Entry():
    i2cWriteBuf = c_ubyte * 4
    user099Pwd = i2cWriteBuf(0x0A, 0x0B, 0x0C, 0x0D)
    testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 128, 4, byref(user099Pwd))
    del i2cWriteBuf, user099Pwd

def read_back_password():
    i2cReadBuf = ctypes.c_ubyte*4
    i2cReadByte = i2cReadBuf()
    result_sum = 0
    Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 123, 4, i2cReadByte)
    if 0 == Res:
        for item in range(len(i2cReadByte)):
            if 0xFF == i2cReadByte[item]:
                print("A2[{}]=0x{:2X},{}".format(123 + item, i2cReadByte[item], 'ok'))
                #f.write("\nA2[{}]=0x{:2X},{}".format(123 + item, i2cReadByte[item], 'ok'))
                result_sum += 1
            else:
                print("A2[{}]=0x{:2X},{}".format(123 + item, i2cReadByte[item], 'error'))
                #f.write("\nA2[{}]=0x{:2X},{}".format(123 + item, i2cReadByte[item], 'error'))
    else:
        print("Read-back A2[123-126] fail ")
        #f.write("Read-back A2[123-126] fail ")
    if result_sum == 4:
        return "OK"
    else:
        return "FAIL"

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
reportName = strFwVer+'.report'
f = open(fileName, 'a+')
f_report = open(reportName, 'a+')
time.sleep(1)
print("\n****************************************************************************")
print("099 Read-back password test, start time : {}".format(dateTime))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\n099 Read-back password test, start time : {}".format(dateTime))
f.write("\n****************************************************************************")
f_report.write("\n****************************************************************************")
f_report.write("\n099 Read-back password test, start time : {}".format(dateTime))
f_report.write("\n****************************************************************************")
print("{}".format(testTitle))
f.write('\n'+testTitle)
f_report.write('\n'+testTitle+'\n')

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
f_report.write("\nno any passsword ...")
print("\nread back A2 123-126...")
f.write("\nread back A2 123-126...")
f_report.write("\nread back A2 123-126...")
if read_back_password() == "OK":
    f.write("\nOK")
    f_report.write("\nOK")
else:
    f.write("\nFAIL")
    f_report.write("\nFAIL")

#########################################################
#      write factory password read-back A2[123-126]
#########################################################
print("\nwrite factory passsword ...")
f.write("\nwrite factory passsword ...")
f_report.write("\nwrite factory passsword ...")
Sfp_Factory_Pwd_Entry(user_password_type)
print("\nread back A2 123-126...")
f.write("\nread back A2 123-126...")
f_report.write("\nread back A2 123-126...")
if read_back_password() == "OK":
    f.write("\nOK")
    f_report.write("\nOK")
else:
    f.write("\nFAIL")
    f_report.write("\nFAIL")

#clear any password
print("POR...")
f.write("POR...")
testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)

#########################################################
# write user password to A2[128-131] read-back A2[123-126]
#########################################################
#write user default read password
print("\nwrite 099 user-reading passsword ...")
f.write("\nwrite 099 user-reading passsword ...")
f_report.write("\nwrite 099 user-reading passsword ...")
Sfp_User_Read_099Pwd_Entry()
print("\nread back A2 123-126...")
f.write("\nread back A2 123-126...")
f_report.write("\nread back A2 123-126...")
if read_back_password() == "OK":
    f.write("\nOK")
    f_report.write("\nOK")
else:
    f.write("\nFAIL")
    f_report.write("\nFAIL")

#clear any password
testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)


#write user default write password
print("\nwrite 099 user-writing passsword ...")
f.write("\nwrite 099 user-writing passsword ...")
f_report.write("\nwrite 099 user-writing passsword ...")
Sfp_User_Write_099Pwd_Entry()
print("\nread back A2 123-126...")
f.write("\nread back A2 123-126...")
f_report.write("\nread back A2 123-126...")
if read_back_password() == "OK":
    f.write("\nOK")
    f_report.write("\nOK")
else:
    f.write("\nFAIL")
    f_report.write("\nFAIL")


dateTime = time.strptime(time.asctime())
dateTime = "{:4}-{:02}-{:02} {:02}:{:02}:{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
print("\n****************************************************************************")
print("099 Read-back password test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\n099 Read-back password test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
f.write("\n****************************************************************************")
f_report.write("\n****************************************************************************")
f_report.write("\n099 Read-back password test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
f_report.write("\n****************************************************************************")

testEvb.AteAllPowerOff()
f.close()
f_report.close()
