import ctypes
from ctypes import *
import time
import random
import operator
from classTestEvb import *
import sys

#==============================================================================
#Test times
#==============================================================================
wr_and_rd_times  = 1000
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
testEvb.Sfp_Factory_Pwd_Entry(user_password_type)
time.sleep(1)
#########################################################
#               Command Sevices
#########################################################
# Read firmware version
strCmdIn = create_string_buffer(b'MCU_GET_VERSION()')
strCmdOutBuff = ctypes.c_ubyte*64
strCmdOut = strCmdOutBuff()
strFwVer = []
retStauts = _cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
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
print("A0 Direct High Write and Read stress test, start time : {}".format(dateTime))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nA0 Direct High Write and Read stress test, start time : {}".format(dateTime))
f.write("\n****************************************************************************")
print("{}".format(testTitle))
f.write('\n'+testTitle)

A0RawDataBuff = ctypes.c_ubyte*128
A0RawReadByte = A0RawDataBuff()
f.write("\nA0 Direct High raw data: \n")
Res = 0xFF
Res = _ateapidll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[0], 128, 128, A0RawReadByte)
if 0 == Res:
    for item in range(128):
        #print("0x{0:X}".format(randomReadByte[i1]), end=' ')
        f.write(str(hex(A0RawReadByte[item]))+',')
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
    testEvb.Sfp_Factory_Pwd_Entry(user_password_type)
    time.sleep(1)

   
    A0WriteDataBuff = [0x00] * 128
    A0WriteDataBuff = random_int_list(0, 256, 128)
    A0WriteByte = (c_ubyte * 128)(*A0WriteDataBuff)

    f.write('write :\n')
    for item in range(128):
        f.write(str(hex(A0WriteByte[item]))+',')
    f.write('\n')
    _ateapidll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[0], 128, 128, byref(A0WriteByte))
    time.sleep(1)

    testEvb.AteAllPowerOff()
    time.sleep(1)

    testEvb.AteAllPowerOn()
    time.sleep(1)

    A0ReadDataBuff = ctypes.c_ubyte * 128
    randomReadByte = A0ReadDataBuff()
    _ateapidll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[0], 128, 128, randomReadByte)

    f.write('read :\n')
    for item in range(128):
        f.write(str(hex(randomReadByte[item]))+',')
    f.write('\n')

    wr_and_rd_success = 0
    
    for item in range(128):
        if randomReadByte[item] == A0WriteByte[item]:
            wr_and_rd_success += 1


    if wr_and_rd_success == 128:
        totalSuccess += 1
        f.write('Round.{}: A0 Direct High write data equal read data.'.format(times)+'\n\n')
        print("Round.{} A0 Direct High write data equal read data.".format(times))
    else:
        f.write('Round.{}: A0 Direct High write data not equal read data.'.format(times)+'\n\n')
        print('Round.{}: A0 Direct High write data not equal read data.'.format(times)+'\n\n')

    testEvb.AteAllPowerOff()
    time.sleep(1)

if wr_and_rd_times == totalSuccess:
    print('A0 Direct High write and read data {} times PASS !'.format(wr_and_rd_times))
    f.write('A0 Direct High write and read data {} times PASS !'.format(wr_and_rd_times))
else:
    print('A0 Direct High write and read data {} times FAIL !'.format(wr_and_rd_times))
    f.write('A0 Direct High write and read data {} times FAIL !'.format(wr_and_rd_times))
f.write('\n')

#restore A0 Direct
testEvb.AteAllPowerOn()
time.sleep(2)
testEvb.Sfp_Factory_Pwd_Entry(user_password_type)
time.sleep(1)
_ateapidll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[0], 128, 128, byref(A0RawReadByte))
time.sleep(1)
A0ReadDataBuff = ctypes.c_ubyte * 128
randomReadByte = A0ReadDataBuff()
_ateapidll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[0], 128, 128, randomReadByte)
if True == operator.eq(A0RawDataBuff, A0ReadDataBuff):
    f.write('A0 Direct High restore success.' + '\n')
    print("A0 Direct High restore success.")
else:
    f.write('A0 Direct High restore fail.' + '\n')
    print("A0 Direct High restore fail.")

dateTime = time.strptime(time.asctime())
dateTime = "{:4}-{:02}-{:02} {:02}:{:02}:{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
print("\n****************************************************************************")
print("A0 Direct High Write and Read stress test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nA0 Direct High Write and Read stress test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
f.write("\n****************************************************************************")
testEvb.AteAllPowerOff()

f.close()

