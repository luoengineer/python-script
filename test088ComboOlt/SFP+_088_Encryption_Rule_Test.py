import ctypes
from ctypes import *
import time
import random
import operator
import sys
from sys import path
path.append('./python_lib')
from cmdServ import cmdservdll, Sfp_Factory_Pwd_Entry
from classTestEvb import *

#Test times
wr_and_rd_times  = 2
# user type for password
is_088_Module = 0
is_other_Module = 1
user_password_type = is_088_Module

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
def Sfp_User_088Pwd_Entry():
    i2cWriteBuf = c_ubyte * 4
    user088Pwd = i2cWriteBuf(0x00, 0x00, 0x10, 0x11)
    testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 123, 4, byref(user088Pwd))



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
#dateTime = time.strptime(time.asctime())
dateTime = time.strptime(time.asctime( time.localtime(startTick)))
dateTime = "{:4}-{:02}-{:02} {:02}:{:02}:{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
testTitle = strFwVer
fileName = strFwVer+'.txt'
f = open(fileName, 'a+')
time.sleep(1)
print("\n****************************************************************************")
print("088 user encryption rule test, start time : {}".format(dateTime))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\n088 user encryption rule test, start time : {}".format(dateTime))
f.write("\n****************************************************************************")
print("{}".format(testTitle))
f.write('\n'+testTitle)

testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)

#########################################################
#               Read with no any password(default)
#########################################################
print("\n不写密码检查用户EEPROM")
f.write("\n不写密码检查用户EEPROM\n")

A2RawDataBuff = ctypes.c_ubyte*120
A2RawReadByte = A2RawDataBuff()
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 128, 120, A2RawReadByte)
if 0 == Res:
    for item in range(len(A2RawReadByte)):
        if 0 == A2RawReadByte[item]:
            print('A2[{}]=0x{:0>2X},{}'.format(128 + item, A2RawReadByte[item], 'OK'))
            f.write('A2[{}]=0x{:0>2X},{}\n'.format(128 + item, A2RawReadByte[item], 'OK'))
        else:
            print('A2[{}]=0x{:0>2X},{}'.format(128 + item, A2RawReadByte[item], 'Fail'))
            f.write('A2[{}]=0x{:0>2X},{}\n'.format(128 + item, A2RawReadByte[item], 'Fail'))
print("\n输入用户密码")
f.write("\n输入用户密码\n")
Sfp_User_088Pwd_Entry()

print("\nModel存储区写入")
f.write("\nModel存储区写入\n")
A2_140_143_buf = ctypes.create_string_buffer(b'XGPO', 4)
Res = 0xFF
Res = testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 140, 4, byref(A2_140_143_buf))
if 0 == Res:
    print("Model存储区A2[140-143]写入OK!")
    f.write("Model存储区A2[140-143]写入OK!\n")
else:
    print("Model存储区A2[140-143]写入FAIL!")
    f.write("Model存储区A2[140-143]写入FAIL!\n")
time.sleep(2)
A2_226_241_buf = ctypes.create_string_buffer(b'N&GPON-C+0000000', 16)
Res = 0xFF
Res = testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 226, 16, byref(A2_226_241_buf))
if 0 == Res:
    print("Model存储区A2[226-241]写入OK!")
    f.write("Model存储区A2[226-241]写入OK!\n")
else:
    print("Model存储区A2[226-241]写入FAIL!")
    f.write("Model存储区A2[226-241]写入FAIL!\n")
time.sleep(2)
A2_242_243_buf = ctypes.c_ubyte*2 #Model checkusm
A2_242_243_byte = A2_242_243_buf(0xFB, 0xAC)
Res = 0xFF
Res = testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 242, 2, A2_242_243_byte)
if 0 == Res:
    print("Model存储区A2[242-243]写入OK!")
    f.write("Model存储区A2[242-243]写入OK!\n")
else:
    print("Model存储区A2[242-243]写入FAIL!")
    f.write("Model存储区A2[242-243]写入FAIL!\n")
time.sleep(2)
A2_144_159_buf = ctypes.c_ubyte*16
A2_144_159_byte = A2_144_159_buf(0x33,0x34,0x30,0x36,0x31,0x37,0x31,0x39,0,0,0,0,0,0,0xFE,0x60)
Res = 0xFF
Res = testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 144, 16, A2_144_159_byte)
if 0 == Res:
    print("Item存储区(BOM编码)A2[144-159]写入OK!")
    f.write("Item存储区(BOM编码)A2[144-159]写入OK!\n")
else:
    print("Item存储区(BOM编码)A2[144-159]写入FAIL!")
    f.write("Item存储区(BOM编码)A2[144-159]写入FAIl!\n")
testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)
print("重上电")
f.write("重上电")
time.sleep(1)
print("\nModel存储区检查")
f.write("\nModel存储区检查\n")
A2RawDataBuff = create_string_buffer(4)
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 140, 4, byref(A2RawDataBuff))
if 0 == Res:
    if list(A2_140_143_buf) == list(A2RawDataBuff):
        print('Model存储区A2[140-143] Reading Data equal Writing data, OK!')
        f.write('Model存储区A2[140-143] Reading Data equal Writing data, OK!')
    else:
        for item in range(len(A2RawDataBuff)):
            print(A2RawDataBuff[item])
        for item in range(len(A2_140_143_buf)):
            print(A2_140_143_buf[item])
        print('Model存储区A2[140-143] Reading Data not equal Writing data, Fail!')
        f.write('Model存储区A2[140-143] Reading Data not equal Writing data, Fail!')

A2RawDataBuff = create_string_buffer(16)
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 226, 16, byref(A2RawDataBuff))
if 0 == Res:
    if list(A2_226_241_buf) == list(A2RawDataBuff):
        print('Model存储区A2[226-242] Reading Data equal Writing data, OK!')
        f.write('Model存储区A2[226-242] Reading Data equal Writing data, OK!')
    else:
        print('Model存储区A2[226-242] Reading Data not equal Writing data, Fail!')
        f.write('Model存储区A2[226-242] Reading Data not equal Writing data, Fail!')

A2RawDataBuff = ctypes.c_ubyte*2
A2RawReadByte = A2RawDataBuff()
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 242, 2, A2RawReadByte)
if 0 == Res:
    if list(A2_242_243_byte) == list(A2RawReadByte):
        print('Model存储区A2[242-243] Reading Data equal Writing data, OK!')
        f.write('Model存储区A2[242-243] Reading Data equal Writing data, OK!')
    else:
        for item in range(len(A2_242_243_byte)):
            print(A2_242_243_byte[item])
        for item in range(len(A2RawReadByte)):
            print(A2RawReadByte[item])
        print('Model存储区A2[242-243] Reading Data not equal Writing data, Fail!')
        f.write('Model存储区A2[242-243] Reading Data not equal Writing data, Fail!')

print("\nItem存储区(BOM编码)检查")
f.write("\nItem存储区(BOM编码)检查\n")
A2RawDataBuff = ctypes.c_ubyte*16
A2RawReadByte = A2RawDataBuff()
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 144, 16, A2RawReadByte)
if 0 == Res:
    if list(A2_144_159_byte) == list(A2RawReadByte):
        print('Model存储区A2[144-159] Reading Data equal Writing data, OK!')
        f.write('Model存储区A2[144-159] Reading Data equal Writing data, OK!')
    else:
        print('Model存储区A2[144-159] Reading Data not equal Writing data, Fail!')
        f.write('Model存储区A2[144-159] Reading Data not equal Writing data, Fail!')

print("\nA2 Restore to All '0'")
f.write("\nA2 Restore to All '0'\n")
Sfp_User_088Pwd_Entry()
time.sleep(1)
A2_128_255_buf = create_string_buffer(128)
Res = 0xFF
Res = testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 128, 128, byref(A2_128_255_buf))
if 0 == Res:
    print('A2[128-255] restore to 0, OK!')
    f.write('\nA2[128-255] restore to 0, OK!\n')
else:
    print('A2[128-255] restore to 0,  Fail!')
    f.write('\nA2[128-255] restore to 0,  Fail!\n')
'''
#########################################################
#               Read with user read password
#########################################################
print("\n输入用户读密码")
f.write("\n输入用户读密码\n")
Sfp_User_088Pwd_Entry()
time.sleep(1)

print("\n明文区185-231检查")
f.write("\n明文区185-231检查\n")
A2RawDataBuff = ctypes.c_ubyte*47
A2RawReadByte = A2RawDataBuff()
Res = 0xFF
Res = objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 185, 47, A2RawReadByte)
if 0 == Res:
    for item in range(len(A2RawReadByte)):
        if 0 != A2RawReadByte[item]:
            print('A2[{}]=0x{:0>2X},{}'.format(185 + item, A2RawReadByte[item], 'OK'))
            f.write('A2[{}]=0x{:0>2X},{}\n'.format(185 + item, A2RawReadByte[item], 'OK'))
        else:
            print('A2[{}]=0x{:0>2X},{}'.format(185 + item, A2RawReadByte[item], 'Fail'))
            f.write('A2[{}]=0x{:0>2X},{}\n'.format(185 + item, A2RawReadByte[item], 'Fail'))

print("\n密码区，加密区128-184读")
f.write("\n密码区，加密区128-184读\n")
A2RawDataBuff = ctypes.c_ubyte*57
A2RawReadByte = A2RawDataBuff()
Res = 0xFF
Res = objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 128, 57, A2RawReadByte)
if 0 == Res:
    for item in range(len(A2RawReadByte)):
       print('A2[{}]=0x{:0>2X}'.format(128 + item, A2RawReadByte[item]))
       f.write('A2[{}]=0x{:0>2X}\n'.format(128 + item, A2RawReadByte[item]))

print("\n加密区232-247读")
f.write("\n加密区232-247读\n")
A2RawDataBuff = ctypes.c_ubyte*16
A2RawReadByte = A2RawDataBuff()
Res = 0xFF
Res = objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 232, 16, A2RawReadByte)
if 0 == Res:
    for item in range(len(A2RawReadByte)):
        if 0 == A2RawReadByte[item]:
            print('A2[{}]=0x{:0>2X}'.format(232 + item, A2RawReadByte[item]))
            f.write('A2[{}]=0x{:0>2X}\n'.format(232 + item, A2RawReadByte[item]))

#########################################################
#               Read with user write password
#########################################################
print("\n输入用户写密码")
f.write("\n输入用户写密码\n")
Sfp_User_Write_099Pwd_Entry()
time.sleep(1)

print("\n明文区185-231检查")
f.write("\n明文区185-231检查\n")
A2RawDataBuff = ctypes.c_ubyte*47
A2RawReadByte = A2RawDataBuff()
Res = 0xFF
Res = objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 185, 47, A2RawReadByte)
if 0 == Res:
    for item in range(len(A2RawReadByte)):
        if 0 != A2RawReadByte[item]:
            print('A2[{}]=0x{:0>2X},{}'.format(185 + item, A2RawReadByte[item], 'OK'))
            f.write('A2[{}]=0x{:0>2X},{}\n'.format(185 + item, A2RawReadByte[item], 'OK'))
        else:
            print('A2[{}]=0x{:0>2X},{}'.format(185 + item, A2RawReadByte[item], 'Fail'))
            f.write('A2[{}]=0x{:0>2X},{}\n'.format(185 + item, A2RawReadByte[item], 'Fail'))

print("\n密码区，加密区128-184读")
f.write("\n密码区，加密区128-184读\n")
A2RawDataBuff = ctypes.c_ubyte*57
A2RawReadByte = A2RawDataBuff()
Res = 0xFF
Res = objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 128, 57, A2RawReadByte)
if 0 == Res:
    for item in range(len(A2RawReadByte)):
       print('A2[{}]=0x{:0>2X}'.format(128 + item, A2RawReadByte[item]))
       f.write('A2[{}]=0x{:0>2X}\n'.format(128 + item, A2RawReadByte[item]))

print("\n加密区232-247读")
f.write("\n加密区232-247读\n")
A2RawDataBuff = ctypes.c_ubyte*16
A2RawReadByte = A2RawDataBuff()
Res = 0xFF
Res = objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 232, 16, A2RawReadByte)
if 0 == Res:
    for item in range(len(A2RawReadByte)):
        if 0 == A2RawReadByte[item]:
            print('A2[{}]=0x{:0>2X}'.format(232 + item, A2RawReadByte[item]))
            f.write('A2[{}]=0x{:0>2X}\n'.format(232 + item, A2RawReadByte[item]))

del A2RawReadByte, A2RawDataBuff

#########################################################
#       Write data with user write password
#########################################################
print("\nA2 140-143 wirte new data ")
f.write("\nA2 140-143 wirte new data \n")
A2WriteDataBuff = ctypes.c_ubyte*4
A2WriteByte = A2WriteDataBuff(140,141,142,143)
objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 140, 4, A2WriteByte)
time.sleep(1)

print("\nPown Off ")
f.write("\nPown Off \n")
AteAllPowerOff(devUsbIndex)
time.sleep(1)
print("\nPown On ")
f.write("\nPown On \n")
AteAllPowerOn(devUsbIndex)
time.sleep(1)
print("\nWrite user writing password... ")
f.write("\nWrite user writing password... \n")
Sfp_User_Write_099Pwd_Entry()

Res = 0xFF
A2ReadDataBuff = ctypes.c_ubyte*4
A2ReadByte = A2ReadDataBuff()
Res = objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 140, 4, A2ReadByte)
if 0 == Res:
    for item in range(len(A2ReadByte)):
        if A2WriteByte[item] == A2ReadByte[item]:
            print('write A2[{}]=0x{:0>2X},{}'.format(140+item, A2WriteByte[item], 'OK'))
            f.write('write A2[{}]=0x{:0>2X},{}\n'.format(140+item, A2WriteByte[item], 'OK'))
            print('read A2[{}]=0x{:0>2X},{}'.format(140+item, A2ReadByte[item], 'OK'))
            f.write('read A2[{}]=0x{:0>2X},{}\n'.format(140+item, A2ReadByte[item], 'OK'))
#restore A2 140-143
print("\nA2 140-143 restore to default data ")
f.write("\nA2 140-143 restore default data \n")
A2WriteDataBuff = ctypes.c_ubyte*4
A2WriteByte = A2WriteDataBuff(0,0,0,0)
objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 140, 4, A2WriteByte)
time.sleep(1)
Res = 0xFF
A2ReadDataBuff = ctypes.c_ubyte*4
A2ReadByte = A2ReadDataBuff()
Res = objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 140, 4, A2ReadByte)
if 0 == Res:
    for item in range(len(A2ReadByte)):
        if A2WriteByte[item] == A2ReadByte[item]:
            print('read A2[{}]=0x{:0>2X},{}'.format(140+item, A2ReadByte[item], 'OK'))
            f.write('read A2[{}]=0x{:0>2X},{}\n'.format(140+item, A2ReadByte[item], 'OK'))

print("\nA2 244-247 wirte new data ")
f.write("\nA2 244-247 wirte new data \n")
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
Sfp_User_088Pwd_Entry()

Res = 0xFF
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

print("\nA2 244-247 restore to default data ")
f.write("\nA2 244-247 restore to default data \n")
A2WriteDataBuff = ctypes.c_ubyte*4
A2WriteByte = A2WriteDataBuff(0,0,0,0)
objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 244, 4, A2WriteByte)
time.sleep(1)
Res = 0xFF
A2ReadDataBuff = ctypes.c_ubyte*4
A2ReadByte = A2ReadDataBuff()
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 244, 4, A2ReadByte)
if 0 == Res:
    for item in range(len(A2ReadByte)):
        if A2WriteByte[item] == A2ReadByte[item]:
            print('read A2[{}]=0x{:0>2X},{}'.format(item, A2ReadByte[item], 'OK'))
            f.write('read A2[{}]=0x{:0>2X},{}\n'.format(item, A2ReadByte[item], 'OK'))

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
Sfp_User_088Pwd_Entry()
A2WriteDataBuff = ctypes.c_ubyte*4
A2WriteByte = A2WriteDataBuff(1, 2, 3, 4)
print("\nWrite the first time new user writing password... ")
f.write("\nWrite the first time new user writing password... \n")
testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 132, 4, A2WriteByte)
time.sleep(1)
print("\nWrite the second time new user writing password... ")
f.write("\nWrite the second time new user writing password... \n")
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
A2WriteDataBuff = ctypes.c_ubyte*4
A2WriteByte = A2WriteDataBuff(1, 2, 3, 4)
testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 128, 4, A2WriteByte)
Res = 0xFF
A2ReadDataBuff = ctypes.c_ubyte*8
A2ReadByte = A2ReadDataBuff()
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 128, 8, A2ReadByte)
count = 0
if 0 == Res:
    for item in range(4):
        if A2ReadByte[item] == A2ReadByte[item+4]:
            print('A2[{}]=0x{:0>2X},A2[{}]=0x{:0>2X},{}'.format(128+item, A2ReadByte[item], 132+item, A2ReadByte[item+4], 'OK'))
            f.write('A2[{}]=0x{:0>2X},A2[{}]=0x{:0>2X},{}\n'.format(128+item, A2ReadByte[item], 132+item, A2ReadByte[item+4], 'OK'))
            count += 1
        else:
            break

if 4 == count:
    print("\nNew reading password change success! ")
    f.write("\nNew reading password change success! \n")
else:
    print("\nNew reading password change fail! ")
    f.write("\nNew reading password change fail! \n")
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
Sfp_User_088Pwd_Entry()
A2WriteDataBuff = ctypes.c_ubyte*4
A2WriteByte = A2WriteDataBuff(5, 6, 7, 8)
print("\nWrite the first time new user writing password... ")
f.write("\nWrite the first time new user writing password... \n")
testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 136, 4, A2WriteByte)
time.sleep(1)
print("\nWrite the second time new user writing password... ")
f.write("\nWrite the second time new user writing password... \n")
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
A2WriteDataBuff = ctypes.c_ubyte*4
A2WriteByte = A2WriteDataBuff(5, 6, 7, 8)
testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 128, 4, A2WriteByte)
Res = 0xFF

A2ReadDataExtBuff = ctypes.c_ubyte*4
A2ReadExtByte = A2ReadDataExtBuff()
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 136, 4, A2ReadExtByte)
count = 0
if 0 == Res:
    for item in range(4):
        if A2WriteByte[item] == A2ReadExtByte[item]:
            print('A2[{}]=0x{:0>2X},A2[{}]=0x{:0>2X},{}'.format(128+item, A2WriteByte[item], 136+item, A2ReadExtByte[item], 'OK'))
            f.write('A2[{}]=0x{:0>2X},A2[{}]=0x{:0>2X},{}\n'.format(128+item, A2WriteByte[item], 136+item, A2ReadExtByte[item], 'OK'))
            count += 1
if 4 == count:
    print("\nNew writing password change success! ")
    f.write("\nNew writing password change success! \n")
else:
    print("\nNew writing password change fail! ")
    f.write("\nNew writing password change fail! \n")
#########################################################
#           Restore to user default password
#########################################################
print("\nRestore user default password... ")
f.write("\nRestore user default password... \n")

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

Sfp_User_088Pwd_Entry()


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
        print("\nRestore user default reading password success! ")
        f.write("\nRestore user default reading password success! \n")
    else:
        print("\nRestore user default reading password fail! ")
        f.write("\nRestore user default reading password fail! \n")
'''

dateTime = time.strptime(time.asctime())
dateTime = "{:4}-{:02}-{:02} {:02}:{:02}:{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
print("\n****************************************************************************")
print("088 user encryption rule test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\n088 user encryption rule test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
f.write("\n****************************************************************************")

testEvb.AteAllPowerOff()
f.close()

