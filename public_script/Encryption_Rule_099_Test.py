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
print("099 user encryption rule test, start time : {}".format(dateTime))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\n099 user encryption rule test, start time : {}".format(dateTime))
f.write("\n****************************************************************************")
f_report.write("\n****************************************************************************")
f_report.write("\n099 user encryption rule test, start time : {}".format(dateTime))
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
#               Read by no any password(default)
#########################################################
print("\nNot write password to check user Encryption area")
f.write("\nNot write password to check user Encryption  area")
f_report.write("\nNot write password to check user Encryption  area")
print("\nCheck A2 128-184...")
f.write("\nCheck A2 128-184...")
f_report.write("\nCheck A2 128-184...")
A2RawDataBuff = ctypes.c_ubyte*57
A2RawReadByte = A2RawDataBuff()
Res = 0xFF
result_sum = 0
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 128, 57, A2RawReadByte)
if 0 == Res:
    for item in range(len(A2RawReadByte)):
        if 0 == A2RawReadByte[item]:
            print('A2[{}]=0x{:0>2X},{}'.format(128 + item, A2RawReadByte[item], 'OK'))
            f.write('A2[{}]=0x{:0>2X},{}\n'.format(128 + item, A2RawReadByte[item], 'OK'))
            result_sum+=1
        else:
            print('A2[{}]=0x{:0>2X},{}'.format(128 + item, A2RawReadByte[item], 'Fail'))
            f.write('A2[{}]=0x{:0>2X},{}\n'.format(128 + item, A2RawReadByte[item], 'Fail'))
if result_sum == 57:
    f_report.write("\nA2 128-184 OK")
else:
    f_report.write("\nA2 128-184 FAIL")

print("\nCheck A2 232-247...")
f.write("\nCheck A2 232-247...")
f_report.write("\nCheck A2 232-247...")
A2RawDataBuff = ctypes.c_ubyte*16
A2RawReadByte = A2RawDataBuff()
Res = 0xFF
result_sum = 0
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 232, 16, A2RawReadByte)
if 0 == Res:
    for item in range(len(A2RawReadByte)):
        if 0 == A2RawReadByte[item]:
            print('A2[{}]=0x{:0>2X},{}'.format(232 + item, A2RawReadByte[item], 'OK'))
            f.write('A2[{}]=0x{:0>2X},{}\n'.format(232 + item, A2RawReadByte[item], 'OK'))
            result_sum += 1
        else:
            print('A2[{}]=0x{:0>2X},{}'.format(232 + item, A2RawReadByte[item], 'Fail'))
            f.write('A2[{}]=0x{:0>2X},{}\n'.format(232 + item, A2RawReadByte[item], 'Fail'))
if result_sum == 16:
    f_report.write("\nA2 232-247 OK")
else:
    f_report.write("\nA2 232-247 FAIL")

print("\nCheck open area : A2 185-231...")
f.write("\nCheck open area : A2 185-231...")
f_report.write("\nCheck open area : A2 185-231...")
A2RawDataBuff = ctypes.c_ubyte*47
A2RawReadByte = A2RawDataBuff()
Res = 0xFF
result_sum = 0
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 185, 47, A2RawReadByte)
if 0 == Res:
    for item in range(len(A2RawReadByte)):
        if 0 != A2RawReadByte[item]:
            print('A2[{}]=0x{:0>2X},{}'.format(185 + item, A2RawReadByte[item], 'OK'))
            f.write('A2[{}]=0x{:0>2X},{}\n'.format(185 + item, A2RawReadByte[item], 'OK'))
            result_sum += 1
        else:
            print('A2[{}]=0x{:0>2X},{}'.format(185 + item, A2RawReadByte[item], 'Fail'))
            f.write('A2[{}]=0x{:0>2X},{}\n'.format(185 + item, A2RawReadByte[item], 'Fail'))
if result_sum == 47:
    f_report.write("\nA2 185-231 OK")
else:
    f_report.write("\nA2 185-231 FAIL")
#########################################################
#               Read by user read password
#########################################################
print("\nInput user read password")
f.write("\nInput user read password\n")
f_report.write("\nInput user read password\n")
Sfp_User_Read_099Pwd_Entry()
time.sleep(1)

print("\nCheck open area : A2 185-231...")
f.write("\nCheck open area: A2 185-231...\n")
f_report.write("\nCheck open area: A2 185-231...\n")
A2RawDataBuff = ctypes.c_ubyte*47
A2RawReadByte = A2RawDataBuff()
Res = 0xFF
result_sum = 0
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 185, 47, A2RawReadByte)
if 0 == Res:
    for item in range(len(A2RawReadByte)):
        if 0 != A2RawReadByte[item]:
            print('A2[{}]=0x{:0>2X},{}'.format(185 + item, A2RawReadByte[item], 'OK'))
            f.write('A2[{}]=0x{:0>2X},{}\n'.format(185 + item, A2RawReadByte[item], 'OK'))
            result_sum += 1
        else:
            print('A2[{}]=0x{:0>2X},{}'.format(185 + item, A2RawReadByte[item], 'Fail'))
            f.write('A2[{}]=0x{:0>2X},{}\n'.format(185 + item, A2RawReadByte[item], 'Fail'))
if result_sum == 47:
    f_report.write("\nA2 185-231 OK\n")

print("\nRead A2 128-184...")
f.write("\nRead A2 128-184...\n")
f_report.write("\nRead A2 128-184...\n")
A2RawDataBuff = ctypes.c_ubyte*57
A2RawReadByte = A2RawDataBuff()
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 128, 57, A2RawReadByte)
if 0 == Res:
    for item in range(len(A2RawReadByte)):
       print('A2[{}]=0x{:0>2X}'.format(128 + item, A2RawReadByte[item]))
       f.write('A2[{}]=0x{:0>2X}\n'.format(128 + item, A2RawReadByte[item]))
       f_report.write('A2[{}]=0x{:0>2X}\n'.format(128 + item, A2RawReadByte[item]))

print("\nRead Encryption  area : A2 232-247...")
f.write("\nRead Encryption  area: A2 232-247...\n")
f_report.write("\nRead Encryption  area: A2 232-247...\n")
A2RawDataBuff = ctypes.c_ubyte*16
A2RawReadByte = A2RawDataBuff()
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 232, 16, A2RawReadByte)
if 0 == Res:
    for item in range(len(A2RawReadByte)):
        if 0 == A2RawReadByte[item]:
            print('A2[{}]=0x{:0>2X}'.format(232 + item, A2RawReadByte[item]))
            f.write('A2[{}]=0x{:0>2X}\n'.format(232 + item, A2RawReadByte[item]))
            f_report.write('A2[{}]=0x{:0>2X}\n'.format(232 + item, A2RawReadByte[item]))

#########################################################
#               Read by user write password
#########################################################
print("\nInput user write password")
f.write("\nInput user write password\n")
f_report.write("\nInput user write password\n")
Sfp_User_Write_099Pwd_Entry()
time.sleep(1)

print("\nCheck open area: A2 185-231...")
f.write("\nCheck open area: A2 185-231...\n")
f_report.write("\nCheck open area: A2 185-231...\n")
A2RawDataBuff = ctypes.c_ubyte*47
A2RawReadByte = A2RawDataBuff()
Res = 0xFF
result_sum = 0
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 185, 47, A2RawReadByte)
if 0 == Res:
    for item in range(len(A2RawReadByte)):
        if 0 != A2RawReadByte[item]:
            print('A2[{}]=0x{:0>2X},{}'.format(185 + item, A2RawReadByte[item], 'OK'))
            f.write('A2[{}]=0x{:0>2X},{}\n'.format(185 + item, A2RawReadByte[item], 'OK'))
            result_sum += 1
        else:
            print('A2[{}]=0x{:0>2X},{}'.format(185 + item, A2RawReadByte[item], 'Fail'))
            f.write('A2[{}]=0x{:0>2X},{}\n'.format(185 + item, A2RawReadByte[item], 'Fail'))
if result_sum == 47:
    f_report.write("\nopen area: A2 185-231 OK")
else:
    f_report.write("\nopen area: A2 185-231 FAIL")
print("\nRead password area and Encryption  area A2 128-184...")
f.write("\nRead password area and Encryption  area A2 128-184...\n")
f_report.write("\nRead password area and Encryption  area A2 128-184...\n")
A2RawDataBuff = ctypes.c_ubyte*57
A2RawReadByte = A2RawDataBuff()
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 128, 57, A2RawReadByte)
if 0 == Res:
    for item in range(len(A2RawReadByte)):
       print('A2[{}]=0x{:0>2X}'.format(128 + item, A2RawReadByte[item]))
       f.write('A2[{}]=0x{:0>2X}\n'.format(128 + item, A2RawReadByte[item]))
       f_report.write('A2[{}]=0x{:0>2X}\n'.format(128 + item, A2RawReadByte[item]))

print("\nRead Encryption  area: A2 232-247...")
f.write("\nRead Encryption  area: A2 232-247...\n")
f_report.write("\nRead Encryption  area: A2 232-247...\n")
A2RawDataBuff = ctypes.c_ubyte*16
A2RawReadByte = A2RawDataBuff()
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 232, 16, A2RawReadByte)
if 0 == Res:
    for item in range(len(A2RawReadByte)):
        if 0 == A2RawReadByte[item]:
            print('A2[{}]=0x{:0>2X}'.format(232 + item, A2RawReadByte[item]))
            f.write('A2[{}]=0x{:0>2X}\n'.format(232 + item, A2RawReadByte[item]))
            f_report.write('A2[{}]=0x{:0>2X}\n'.format(232 + item, A2RawReadByte[item]))

del A2RawReadByte, A2RawDataBuff

#########################################################
#       Write data with user write password
#########################################################
print("\nA2 140-143 wirte new data ")
f.write("\nA2 140-143 wirte new data \n")
f_report.write("\nA2 140-143 wirte new data \n")
A2WriteDataBuff = ctypes.c_ubyte*4
A2WriteByte = A2WriteDataBuff(140,141,142,143)
testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 140, 4, A2WriteByte)
time.sleep(1)

print("\nPown Off ")
f.write("\nPown Off \n")
testEvb.AteAllPowerOff()
time.sleep(1)
print("\nPown On ")
f.write("\nPown On \n")
testEvb.AteAllPowerOn()
time.sleep(1)
print("\nWrite user writing password... ")
f.write("\nWrite user writing password... \n")
f_report.write("\nWrite user writing password... \n")
Sfp_User_Write_099Pwd_Entry()

Res = 0xFF
result_sum = 0
A2ReadDataBuff = ctypes.c_ubyte*4
A2ReadByte = A2ReadDataBuff()
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 140, 4, A2ReadByte)
if 0 == Res:
    for item in range(len(A2ReadByte)):
        if A2WriteByte[item] == A2ReadByte[item]:
            print('write A2[{}]=0x{:0>2X},{}'.format(140+item, A2WriteByte[item], 'OK'))
            f.write('write A2[{}]=0x{:0>2X},{}\n'.format(140+item, A2WriteByte[item], 'OK'))
            print('read A2[{}]=0x{:0>2X},{}'.format(140+item, A2ReadByte[item], 'OK'))
            f.write('read A2[{}]=0x{:0>2X},{}\n'.format(140+item, A2ReadByte[item], 'OK'))
            result_sum += 1
if result_sum == 4:
    f_report.write("\nWrite A2 140-143 OK")
else:
    f_report.write("\nWrite A2 140-143 FAIL")
#restore A2 140-143
print("\nA2 140-143 restore to default data ")
f.write("\nA2 140-143 restore default data \n")
f_report.write("\nA2 140-143 restore default data \n")
A2WriteDataBuff = ctypes.c_ubyte*4
A2WriteByte = A2WriteDataBuff(0,0,0,0)
testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 140, 4, A2WriteByte)
time.sleep(1)
Res = 0xFF
result_sum = 0
A2ReadDataBuff = ctypes.c_ubyte*4
A2ReadByte = A2ReadDataBuff()
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 140, 4, A2ReadByte)
if 0 == Res:
    for item in range(len(A2ReadByte)):
        if A2WriteByte[item] == A2ReadByte[item]:
            print('read A2[{}]=0x{:0>2X},{}'.format(140+item, A2ReadByte[item], 'OK'))
            f.write('read A2[{}]=0x{:0>2X},{}\n'.format(140+item, A2ReadByte[item], 'OK'))
            result_sum += 1
if result_sum == 4:
    f_report.write("\nA2 140-143 restore OK")
else:
    f_report.write("\nA2 140-143 restore FAIL")

print("\nA2 244-247 wirte new data...")
f.write("\nA2 244-247 wirte new data...\n")
f_report.write("\nA2 244-247 wirte new data...\n")
A2WriteDataBuff = ctypes.c_ubyte*4
A2WriteByte = A2WriteDataBuff(244,245,246,247)
testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 244, 4, A2WriteByte)
time.sleep(1)

print("\nPown Off ")
f.write("\nPown Off \n")
testEvb.AteAllPowerOff()
time.sleep(1)
print("\nPown On ")
f.write("\nPown On \n")
testEvb.AteAllPowerOn()
time.sleep(1)
print("\nWrite user writing password... ")
f.write("\nWrite user writing password... \n")
f_report.write("\nWrite user writing password... \n")
Sfp_User_Write_099Pwd_Entry()

Res = 0xFF
result_sum = 0
A2ReadDataBuff = ctypes.c_ubyte*4
A2Readbyte = A2ReadDataBuff()
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 244, 4, A2ReadByte)
if 0 == Res:
    for item in range(len(A2ReadByte)):
        if A2WriteByte[item] == A2ReadByte[item]:
            print('write A2[{}]=0x{:0>2X},{}'.format(item, A2WriteByte[item], 'OK'))
            f.write('write A2[{}]=0x{:0>2X},{}\n'.format(item, A2WriteByte[item], 'OK'))
            print('read A2[{}]=0x{:0>2X},{}'.format(item, A2ReadByte[item], 'OK'))
            f.write('read A2[{}]=0x{:0>2X},{}\n'.format(item, A2ReadByte[item], 'OK'))
            result_sum += 1
if result_sum == 4:
    f_report.write("\nA2 244-247 wirte OK")
else:
    f_report.write("\nA2 244-247 wirte FAIL")

print("\nA2 244-247 restore to default data ")
f.write("\nA2 244-247 restore to default data \n")
f_report.write("\nA2 244-247 restore to default data \n")

A2WriteDataBuff = ctypes.c_ubyte*4
A2WriteByte = A2WriteDataBuff(0,0,0,0)
testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 244, 4, A2WriteByte)
time.sleep(1)
Res = 0xFF
result_sum = 0
A2ReadDataBuff = ctypes.c_ubyte*4
A2ReadByte = A2ReadDataBuff()
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 244, 4, A2ReadByte)
if 0 == Res:
    for item in range(len(A2ReadByte)):
        if A2WriteByte[item] == A2ReadByte[item]:
            print('read A2[{}]=0x{:0>2X},{}'.format(item, A2ReadByte[item], 'OK'))
            f.write('read A2[{}]=0x{:0>2X},{}\n'.format(item, A2ReadByte[item], 'OK'))
            result_sum += 1
if result_sum == 4:
    f_report.write("\nA2 244-247 restore OK")
else:
    f_report.write("\nA2 244-247 restore FAIL")

del A2WriteDataBuff, A2WriteByte, A2ReadDataBuff, A2ReadByte
#########################################################
#       Change to user new read password
#########################################################
print("\nPown Off ")
f.write("\nPown Off \n")
testEvb.AteAllPowerOff()
time.sleep(1)
print("\nPown On ")
f.write("\nPown On \n")
testEvb.AteAllPowerOn()
time.sleep(1)
print("\nWrite user writing password... ")
f.write("\nWrite user writing password... \n")
f_report.write("\nWrite user writing password... \n")
Sfp_User_Write_099Pwd_Entry()
A2WriteDataBuff = ctypes.c_ubyte*4
A2WriteByte = A2WriteDataBuff(1, 2, 3, 4)
print("\nWrite the user's new password for the first time... ")
f.write("\nWrite the user's new password for the first time... \n")
f_report.write("\nWrite the user's new password for the first time... \n")
testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 132, 4, A2WriteByte)
time.sleep(1)
print("\nWrite the user's new password for the second time... ")
f.write("\nWrite the user's new password for the second time... \n")
f_report.write("\nWrite the user's new password for the second time... \n")
testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 132, 4, A2WriteByte)
print("\nPown Off ")
f.write("\nPown Off \n")
testEvb.AteAllPowerOff()
time.sleep(1)
print("\nPown On ")
f.write("\nPown On \n")
testEvb.AteAllPowerOn()
time.sleep(1)
print("\nWrite user new reading password, check... ")
f.write("\nWrite user new reading password, check... \n")
f_report.write("\nWrite user new reading password, check... \n")

A2WriteDataBuff = ctypes.c_ubyte*4
A2WriteByte = A2WriteDataBuff(1, 2, 3, 4)
testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 128, 4, A2WriteByte)
Res = 0xFF
A2ReadDataBuff = ctypes.c_ubyte*8
A2ReadByte = A2ReadDataBuff()
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 128, 8, A2ReadByte)
result_sum = 0
if 0 == Res:
    for item in range(4):
        if A2ReadByte[item] == A2ReadByte[item+4]:
            print('A2[{}]=0x{:0>2X},A2[{}]=0x{:0>2X},{}'.format(128+item, A2ReadByte[item], 132+item, A2ReadByte[item+4], 'OK'))
            f.write('A2[{}]=0x{:0>2X},A2[{}]=0x{:0>2X},{}\n'.format(128+item, A2ReadByte[item], 132+item, A2ReadByte[item+4], 'OK'))
            result_sum += 1
        else:
            break

if 4 == result_sum:
    print("\nNew reading password change OK! ")
    f.write("\nNew reading password change OK! \n")
    f_report.write("\nNew reading password change OK! \n")
else:
    print("\nNew reading password change FAIL! ")
    f.write("\nNew reading password change FAIL! \n")
    f_report("\nNew reading password change FAIL! \n")
#########################################################
#           Change to user new write password
#########################################################
print("\nPown Off ")
f.write("\nPown Off \n")
testEvb.AteAllPowerOff()
time.sleep(1)
print("\nPown On ")
f.write("\nPown On \n")
testEvb.AteAllPowerOn()
time.sleep(1)
print("\nWrite user writing password... ")
f.write("\nWrite user writing password... \n")
f_report.write("\nWrite user writing password... \n")

Sfp_User_Write_099Pwd_Entry()
A2WriteDataBuff = ctypes.c_ubyte*4
A2WriteByte = A2WriteDataBuff(5, 6, 7, 8)
print("\nWrite the user's new password for the first time... ")
f.write("\nWrite the user's new password for the first time... \n")
f_report.write("\nWrite the user's new password for the first time... \n")
testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 136, 4, A2WriteByte)
time.sleep(1)
print("\nWrite the user's new password for the second time... ")
f.write("\nWrite the user's new password for the second time... \n")
f_report.write("\nWrite the user's new password for the second time... \n")
testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 136, 4, A2WriteByte)
print("\nPown Off ")
f.write("\nPown Off \n")
testEvb.AteAllPowerOff()
time.sleep(1)
print("\nPown On ")
f.write("\nPown On \n")
testEvb.AteAllPowerOn()
time.sleep(1)
print("\nWrite user new writing password, check... ")
f.write("\nWrite user new writing password, check... \n")
f_report.write("\nWrite user new writing password, check... \n")
A2WriteDataBuff = ctypes.c_ubyte*4
A2WriteByte = A2WriteDataBuff(5, 6, 7, 8)
testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 128, 4, A2WriteByte)
Res = 0xFF

A2ReadDataExtBuff = ctypes.c_ubyte*4
A2ReadExtByte = A2ReadDataExtBuff()
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 136, 4, A2ReadExtByte)
result_sum = 0
if 0 == Res:
    for item in range(4):
        if A2WriteByte[item] == A2ReadExtByte[item]:
            print('A2[{}]=0x{:0>2X},A2[{}]=0x{:0>2X},{}'.format(128+item, A2WriteByte[item], 136+item, A2ReadExtByte[item], 'OK'))
            f.write('A2[{}]=0x{:0>2X},A2[{}]=0x{:0>2X},{}\n'.format(128+item, A2WriteByte[item], 136+item, A2ReadExtByte[item], 'OK'))
            result_sum += 1
if 4 == result_sum:
    print("\nNew writing password change OK! ")
    f.write("\nNew writing password change OK! \n")
    f_report.write("\nNew writing password change OK! \n")
else:
    print("\nNew writing password change FAIL! ")
    f.write("\nNew writing password change FAIL! \n")
    f_report.write("\nNew writing password change FAIL! \n")
#########################################################
#           Restore to user default password
#########################################################
print("\nRestore user default password... ")
f.write("\nRestore user default password... \n")
f_report.write("\nRestore user default password... \n")
userDefaultPassword = {132:0x0B, 133:0x0C, 134:0x0D, 135:0x0E, 136:0x0A, 137:0x0B, 138:0x0C, 139:0x0D}
passwordArray = list(userDefaultPassword.values())
addrArray = list(userDefaultPassword.keys())

Sfp_Factory_Pwd_Entry(is_other_Module)
time.sleep(1)

userReadPassword = ctypes.c_ubyte*4
A2WriteByte = userReadPassword(passwordArray[0],passwordArray[1],passwordArray[2],passwordArray[3])
testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], addrArray[0], 4, A2WriteByte)
time.sleep(1)

userWritePassword = ctypes.c_ubyte*4
A2WriteByte = userWritePassword(userDefaultPassword[136],userDefaultPassword[137],userDefaultPassword[138],userDefaultPassword[139])
testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], addrArray[4], 4, A2WriteByte)
time.sleep(1)

testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)

Sfp_User_Read_099Pwd_Entry()


A2ReadDataBuff = ctypes.c_ubyte*8
A2ReadByte = A2ReadDataBuff()
Res = 0xFF

Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 132, 8, A2ReadByte)
if 0 == Res:
    for item in range(len(A2ReadByte)):
        if A2ReadByte[item] == passwordArray[item]:
            print('A2[{}]=0x{:0>2X},{}'.format(132+item, A2ReadByte[item], 'OK'))
            f.write('A2[{}]=0x{:0>2X},{}\n'.format(132+item, A2ReadByte[item], 'OK'))

    if list(A2ReadByte) == passwordArray:
        print("\nRestore user default reading password OK! ")
        f.write("\nRestore user default reading password OK! \n")
        f_report.write("\nRestore user default reading password Ok! \n")
    else:
        print("\nRestore user default reading password FAIL! ")
        f.write("\nRestore user default reading password FAIL! \n")
        f_report.write("\nRestore user default reading password FAIL! \n")

del userReadPassword
dateTime = time.strptime(time.asctime())
dateTime = "{:4}-{:02}-{:02} {:02}:{:02}:{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
print("\n****************************************************************************")
print("099 user encryption rule test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\n099 user encryption rule test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
f.write("\n****************************************************************************")
f_report.write("\n****************************************************************************")
f_report.write("\n099 user encryption rule test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
f_report.write("\n****************************************************************************")
testEvb.AteAllPowerOff()
f.close()
f_report.close()
