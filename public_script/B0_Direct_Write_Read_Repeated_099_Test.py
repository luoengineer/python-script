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
print("B0 Direct Write and Read stress test, start time : {}".format(dateTime))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nB0 Direct Write and Read stress test, start time : {}".format(dateTime))
f.write("\n****************************************************************************")
print("{}".format(testTitle))
f.write('\n'+testTitle)
B0RawDataBuff = ctypes.c_ubyte*128
B0RawReadByte = B0RawDataBuff()
f.write("B0 Direct raw data: \n")
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[2], 0, 128, B0RawReadByte)
if 0 == Res:
    for item in range(128):
        #print("0x{0:X}".format(randomReadByte[i1]), end=' ')
        f.write(str(hex(B0RawReadByte[item]))+',')
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
    Sfp_Factory_Pwd_Entry(user_password_type)
    time.sleep(1)

   
    B0WriteDataBuff = [0x00] * 128
    B0WriteDataBuff = random_int_list(0, 256, 128)
    B0WriteByte = (c_ubyte * 128)(*B0WriteDataBuff)

    f.write('write :\n')
    for item in range(128):
        f.write(str(hex(B0WriteByte[item]))+',')
    f.write('\n')
    testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, ComboSfpI2cAddr[2], 0, 128, byref(B0WriteByte))
    time.sleep(1)

    testEvb.AteAllPowerOff()
    time.sleep(1)

    testEvb.AteAllPowerOn()
    time.sleep(1)

    B0ReadDataBuff = ctypes.c_ubyte * 128
    randomReadByte = B0ReadDataBuff()
    testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[2], 0, 128, randomReadByte)

    f.write('read :\n')
    for item in range(128):
        f.write(str(hex(randomReadByte[item]))+',')
    f.write('\n')

    wr_and_rd_success = 0
    
    for item in range(128):
        if randomReadByte[item] == B0WriteByte[item]:
            wr_and_rd_success += 1


    if wr_and_rd_success == 128:
        totalSuccess += 1
        f.write('Round.{}: B0 write data equal read data.'.format(times)+'\n\n')
        print("Round.{} B0 write data equal read data.".format(times))
    else:
        f.write('Round.{}: B0 write data not equal read data.'.format(times)+'\n\n')
        print('Round.{}: B0 write data not equal read data.'.format(times)+'\n\n')

    testEvb.AteAllPowerOff()
    time.sleep(1)

if wr_and_rd_times == totalSuccess:
    print('B0 Direct write and read data {} times PASS !'.format(wr_and_rd_times))
    f.write('B0 Direct write and read data {} times PASS !'.format(wr_and_rd_times))
else:
    print('B0 Direct write and read data {} times FAIL !'.format(wr_and_rd_times))
    f.write('B0 Direct write and read data {} times FAIL !'.format(wr_and_rd_times))
f.write('\n')

#restore B0 Direct
testEvb.AteAllPowerOn()
time.sleep(2)
Sfp_Factory_Pwd_Entry(user_password_type)
time.sleep(1)
testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, ComboSfpI2cAddr[2], 0, 128, byref(B0RawReadByte))
time.sleep(1)
B0ReadDataBuff = ctypes.c_ubyte * 128
randomReadByte = B0ReadDataBuff()
testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[2], 0, 128, randomReadByte)
if True == operator.eq(B0RawDataBuff, B0ReadDataBuff):
    f.write('B0 Direct restore success.' + '\n')
    print("B0 Direct restore success.")
else:
    f.write('B0 Direct restore fail.' + '\n')
    print("B0 Direct restore fail.")

dateTime = time.strptime(time.asctime())
dateTime = "{:4}-{:02}-{:02} {:02}:{:02}:{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
print("\n****************************************************************************")
print("B0 Direct Write and Read stress test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nB0 Direct Write and Read stress test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
f.write("\n****************************************************************************")
testEvb.AteAllPowerOff()

f.close()

