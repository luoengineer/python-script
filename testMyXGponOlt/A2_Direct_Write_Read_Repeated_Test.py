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
wr_and_rd_times  = 5
# user type for password
is_088_Module = 0
is_other_Module = 1
user_password_type = is_other_Module

userCode = 351
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
def random_int_list(start, stop, length):
  start, stop = (int(start), int(stop)) if start <= stop else (int(stop), int(start))
  length = int(abs(length)) if length else 0
  for i in range(length):
    yield random.randint(start, stop)

    
def Sfp_User_Pwd_Entry(userCode):
    i2cWriteBuf = c_ubyte * 4
    if 351 == userCode:
        factoryPwd = i2cWriteBuf(0xC0, 0x72, 0x61, 0x79)
    elif 1 == userCode:
        factoryPwd = i2cWriteBuf(0x58, 0x47, 0x54, 0x45)
    testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, 0xA2, 123, 4, byref(factoryPwd))
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
Sfp_User_Pwd_Entry(userCode)
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
print("A2 Direct Write and Read stress test, start time : {}".format(dateTime))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nA2 Direct Write and Read stress test, start time : {}".format(dateTime))
f.write("\n****************************************************************************")
f_report.write("\n****************************************************************************")
f_report.write("\nA2 Direct Write and Read stress test, start time : {}".format(dateTime))
f_report.write("\n****************************************************************************")
print("{}".format(testTitle))
f.write('\n'+testTitle)
f_report.write('\n'+testTitle+'\n')

A2RawDataBuff = ctypes.c_ubyte*96
A2RawReadByte = A2RawDataBuff()
f.write("\nA2 Direct raw data: \n")
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 0, 96, A2RawReadByte)
if 0 == Res:
    for item in range(96):
        #print("0x{0:X}".format(randomReadByte[i1]), end=' ')
        f.write(str(hex(A2RawReadByte[item]))+',')
else:
    f.write('read raw data fail.'+'\n')
    print('read raw data fail.' + '\n')
    f.close()
    sys.exit()

f.write('\n\n')
testEvb.AteAllPowerOff()

#Run test
totalSuccess = 0
for times in range(wr_and_rd_times):
    testEvb.AteAllPowerOn()
    time.sleep(2)
    Sfp_User_Pwd_Entry(userCode)
    time.sleep(1)

   
    A2WriteDataBuff = [0x00] * 96
    A2WriteDataBuff = random_int_list(0, 256, 96)
    #A2WriteDataBuff[92] = 0
    A2WriteByte = (c_ubyte * 96)(*A2WriteDataBuff)
    A2WriteByte[92] = 0

    f.write('write :\n')
    for item in range(96):
        f.write(str(hex(A2WriteByte[item]))+',')
    f.write('\n')
    testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 0, 96, byref(A2WriteByte))
    time.sleep(1)

    testEvb.AteAllPowerOff()
    time.sleep(1)

    testEvb.AteAllPowerOn()
    time.sleep(1)

    A2ReadDataBuff = ctypes.c_ubyte * 96
    randomReadByte = A2ReadDataBuff()
    testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 0, 96, randomReadByte)

    f.write('read :\n')
    for item in range(96):
        f.write(str(hex(randomReadByte[item]))+',')
    f.write('\n')

    wr_and_rd_success = 0
    
    for item in range(96):
        if randomReadByte[item] == A2WriteByte[item]:
            wr_and_rd_success += 1


    if wr_and_rd_success == 96:
        totalSuccess += 1
        f.write('Round.{}: A2 Direct write data equal read data, OK'.format(times)+'\n\n')
        print("Round.{} A2 Direct write data equal read data, OK".format(times))
    else:
        f.write('Round.{}: A2 Direct write data not equal read data, FAIL'.format(times)+'\n\n')
        print('Round.{}: A2 Direct write data not equal read data, FAIL'.format(times)+'\n\n')

    testEvb.AteAllPowerOff()
    time.sleep(1)

if wr_and_rd_times == totalSuccess:
    print('A2 Direct write and read data {} times PASS !'.format(wr_and_rd_times))
    f.write('A2 Direct write and read data {} times PASS !'.format(wr_and_rd_times))
    f_report.write('A2 Direct write and read data {} times PASS !'.format(wr_and_rd_times))
else:
    print('A2 Direct write and read data {} times FAIL !'.format(wr_and_rd_times))
    f.write('A2 Direct write and read data {} times FAIL !'.format(wr_and_rd_times))
    f_report.write('A2Direct write and read data {} times FAIL !'.format(wr_and_rd_times))
f.write('\n')
f_report.write('\n')

#restore A2 Direct
testEvb.AteAllPowerOn()
time.sleep(2)
Sfp_User_Pwd_Entry(userCode)
time.sleep(1)
testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 0, 96, byref(A2RawReadByte))
time.sleep(1)
A2ReadDataBuff = ctypes.c_ubyte * 96
randomReadByte = A2ReadDataBuff()
testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 0, 96, randomReadByte)
if True == operator.eq(A2RawDataBuff, A2ReadDataBuff):
    f.write('A2 Direct restore success.' + '\n')
    print("A2 Direct restore success.")
else:
    f.write('A2 Direct restore fail.' + '\n')
    print("A2 Direct restore fail.")

dateTime = time.strptime(time.asctime())
dateTime = "{:4}-{:02}-{:02} {:02}:{:02}:{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
print("\n****************************************************************************")
print("A2 Direct Write and Read stress test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nA2 Direct Write and Read stress test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
f.write("\n****************************************************************************")
f_report.write("\n****************************************************************************")
f_report.write("\nA2 Direct Write and Read stress test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
f_report.write("\n****************************************************************************")
testEvb.AteAllPowerOff()
f.close()
f_report.close()
