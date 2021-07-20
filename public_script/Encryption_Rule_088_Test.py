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
user_password_type = is_088_Module

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
def Sfp_User_088Pwd_Entry():
    i2cWriteBuf = c_ubyte * 4
    user088Pwd = i2cWriteBuf(0x00, 0x00, 0x10, 0x11)
    testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 123, 4, byref(user088Pwd))

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
print("088 user encryption rule test, start time : {}".format(dateTime))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\n088 user encryption rule test, start time : {}".format(dateTime))
f.write("\n****************************************************************************")
f_report.write("\n****************************************************************************")
f_report.write("\n088 user encryption rule test, start time : {}".format(dateTime))
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
#先读用户EEPROM(128-247),作为恢复数据，检查除BOM(144-159)外是否全为0
#########################################################
print("\nNot write password to check user Encryption area")
f.write("\n Not write password to check user Encryption  area\n")
print("\nCheck A2 128-247...")
f.write("\nCheck A2 128-247...\n")
A2RawDataBuff = ctypes.c_ubyte*120
A2RawReadByte = A2RawDataBuff()
Res = 0xFF
result_sum = 0
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 128, 120, A2RawReadByte)
if 0 == Res:
    for item in range(len(A2RawReadByte)):
        if item < 144-128 or item > 159-128:
            print('A2[{}]=0x{:0>2X},{}'.format(128 + item, A2RawReadByte[item], 'OK'))
            f.write('A2[{}]=0x{:0>2X},{}\n'.format(128 + item, A2RawReadByte[item], 'OK'))
        elif 0 == A2RawReadByte[item]:
            print('A2[{}]=0x{:0>2X},{}'.format(128 + item, A2RawReadByte[item], 'OK'))
            f.write('A2[{}]=0x{:0>2X},{}\n'.format(128 + item, A2RawReadByte[item], 'OK'))
            result_sum += 1
        else:
            print('A2[{}]=0x{:0>2X},{}'.format(128 + item, A2RawReadByte[item], 'Fail'))
            f.write('A2[{}]=0x{:0>2X},{}\n'.format(128 + item, A2RawReadByte[item], 'Fail'))
if result_sum == 120-(159-144)+1:
    f_report.write("\nA2 128-247 OK")

#########################################################
#写入使用用户密码,写用户指定写区域，
#然后回读检查是否写入，最后恢复。
#########################################################
print("\n输入用户密码")
f.write("\n输入用户密码\n")
f_report.write("\n输入用户密码")
Sfp_User_088Pwd_Entry()
time.sleep(1)
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
time.sleep(1)
A2_226_241_buf = ctypes.create_string_buffer(b'N&GPON-C+0000000', 16)
Res = 0xFF
Res = testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 226, 16, byref(A2_226_241_buf))
if 0 == Res:
    print("Model存储区A2[226-241]写入OK!")
    f.write("Model存储区A2[226-241]写入OK!\n")
else:
    print("Model存储区A2[226-241]写入FAIL!")
    f.write("Model存储区A2[226-241]写入FAIL!\n")
time.sleep(1)
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
time.sleep(1)
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
time.sleep(1)
testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)
print("重上电")
f.write("重上电")

print("\nModel存储区检查")
f.write("\nModel存储区检查\n")

A2_140_143_Read = create_string_buffer(4)
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 140, 4, byref(A2_140_143_Read))
if 0 == Res:
    if list(A2_140_143_buf) == list(A2_140_143_Read):
        print('Model存储区A2[140-143] Reading Data equal Writing data, OK!')
        f.write('Model存储区A2[140-143] Reading Data equal Writing data, OK!\n')
        f_report.write('\nModel存储区A2[140-143] Reading Data equal Writing data, OK!\n')
    else:
        for item in range(len(A2_140_143_Read)):
            print(A2_140_143_Read[item])
        for item in range(len(A2_140_143_buf)):
            print(A2_140_143_buf[item])
        print('Model存储区A2[140-143] Reading Data not equal Writing data, Fail!')
        f.write('Model存储区A2[140-143] Reading Data not equal Writing data, Fail!\n')
        f_report.write('Model存储区A2[140-143] Reading Data not equal Writing data, Fail!\n')

A2_226_242_Read = create_string_buffer(16)
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 226, 16, byref(A2_226_242_Read))
if 0 == Res:
    if list(A2_226_241_buf) == list(A2_226_242_Read):
        print('Model存储区A2[226-242] Reading Data equal Writing data, OK!')
        f.write('Model存储区A2[226-242] Reading Data equal Writing data, OK!\n')
        f_report.write('Model存储区A2[226-242] Reading Data equal Writing data, OK!\n')
    else:
        print('Model存储区A2[226-242] Reading Data not equal Writing data, Fail!')
        f.write('Model存储区A2[226-242] Reading Data not equal Writing data, Fail!\n')
        f_report.write('Model存储区A2[226-242] Reading Data not equal Writing data, Fail!\n')

A2_242_243_ReadBuf = ctypes.c_ubyte*2
A2_242_243_Read = A2_242_243_ReadBuf()
# Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 242, 2, A2_242_243_Read)
if 0 == Res:
    if list(A2_242_243_byte) == list(A2_242_243_Read):
        print('Model存储区A2[242-243] Reading Data equal Writing data, OK!')
        f.write('Model存储区A2[242-243] Reading Data equal Writing data, OK!\n')
        f_report.write('Model存储区A2[242-243] Reading Data equal Writing data, OK!\n')
    else:
        for item in range(len(A2_242_243_byte)):
            print(A2_242_243_byte[item])
        for item in range(len(A2_242_243_Read)):
            print(A2_242_243_Read[item])
        print('Model存储区A2[242-243] Reading Data not equal Writing data, Fail!')
        f.write('Model存储区A2[242-243] Reading Data not equal Writing data, Fail!\n')
        f_report.write('Model存储区A2[242-243] Reading Data not equal Writing data, Fail!\n')

print("\nItem存储区(BOM编码)检查")
f.write("\nItem存储区(BOM编码)检查\n")
A2_144_159_ReadBuf = ctypes.c_ubyte*16
A2_144_159_Read = A2_144_159_ReadBuf()
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 144, 16, A2_144_159_Read)
if 0 == Res:
    if list(A2_144_159_byte) == list(A2_144_159_Read):
        print('Model存储区A2[144-159] Reading Data equal Writing data, OK!')
        f.write('Model存储区A2[144-159] Reading Data equal Writing data, OK!\n')
        f_report.write('Model存储区A2[144-159] Reading Data equal Writing data, OK!\n')
    else:
        print('Model存储区A2[144-159] Reading Data not equal Writing data, Fail!')
        f.write('Model存储区A2[144-159] Reading Data not equal Writing data, Fail!\n')
        f_report.write('Model存储区A2[144-159] Reading Data not equal Writing data, Fail!\n')

print("\nA2 Restore...")
f.write("\nA2 Restore...\n")
Sfp_User_088Pwd_Entry()
time.sleep(1)

testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 128, 120,
                                           A2RawReadByte)
time.sleep(2)
testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)
Res = 0xFF
A2_128_247_Read = create_string_buffer(120)
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 128, 120,
                                           byref(A2_128_247_Read))
if 0 == Res and list(A2_128_247_Read) == list(A2_128_247_Read):
    print('A2[128-247] restore to 0, OK!')
    f.write('\nA2[128-247] restore to 0, OK!\n')
    f_report.write('A2[128-247] restore OK!\n')
else:
    print('A2[128-247] restore to 0,  Fail!')
    f.write('\nA2[128-247] restore to 0,  Fail!\n')
    f_report.write('A2[128-247] restore Fail!\n')
time.sleep(1)

#########################################################
#先读用户EEPROM检查是否全为0，然后写用户指定写区域，
#然后回读检查是否写入，最后恢复为全0。写入使用工厂密码
#########################################################
testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)
print("重上电")
f.write("重上电")

print("\n不写密码检查用户EEPROM")
f.write("\n不写密码检查用户EEPROM\n")

A2RawDataBuff = ctypes.c_ubyte*120
A2RawReadByte = A2RawDataBuff()
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 128, 120, A2RawReadByte)
if 0 == Res:
    for item in range(len(A2RawReadByte)):
        if item < 144 or item > 159:
            print('A2[{}]=0x{:0>2X},{}'.format(128 + item, A2RawReadByte[item], 'OK'))
            f.write('A2[{}]=0x{:0>2X},{}\n'.format(128 + item, A2RawReadByte[item], 'OK'))
        elif 0 == A2RawReadByte[item]:
            print('A2[{}]=0x{:0>2X},{}'.format(128 + item, A2RawReadByte[item], 'OK'))
            f.write('A2[{}]=0x{:0>2X},{}\n'.format(128 + item, A2RawReadByte[item], 'OK'))
        else:
            print('A2[{}]=0x{:0>2X},{}'.format(128 + item, A2RawReadByte[item], 'Fail'))
            f.write('A2[{}]=0x{:0>2X},{}\n'.format(128 + item, A2RawReadByte[item], 'Fail'))
print("\n输入工厂密码")
f.write("\n输入工厂密码\n")
f_report.write("\n输入工厂密码")
Sfp_Factory_Pwd_Entry(0)
time.sleep(1)
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
time.sleep(1)
A2_226_241_buf = ctypes.create_string_buffer(b'N&GPON-C+0000000', 16)
Res = 0xFF
Res = testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 226, 16, byref(A2_226_241_buf))
if 0 == Res:
    print("Model存储区A2[226-241]写入OK!")
    f.write("Model存储区A2[226-241]写入OK!\n")
else:
    print("Model存储区A2[226-241]写入FAIL!")
    f.write("Model存储区A2[226-241]写入FAIL!\n")
time.sleep(1)
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
time.sleep(1)
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
time.sleep(1)
testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)
print("重上电")
f.write("重上电")
time.sleep(1)
print("\nModel存储区检查")
f.write("\nModel存储区检查\n")
A2_140_143_Read = ctypes.create_string_buffer(4)
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 140, 4, byref(A2_140_143_Read))
if 0 == Res:
    if list(A2_140_143_buf) == list(A2_140_143_Read):
        print('Model存储区A2[140-143] Reading Data equal Writing data, OK!')
        f.write('Model存储区A2[140-143] Reading Data equal Writing data, OK!\n')
        f_report.write('\nModel存储区A2[140-143] Reading Data equal Writing data, OK!\n')
    else:
        for item in range(len(A2_140_143_Read)):
            print(A2RawDataBuff[item])
        for item in range(len(A2_140_143_buf)):
            print(A2_140_143_buf[item])
        print('Model存储区A2[140-143] Reading Data not equal Writing data, Fail!')
        f.write('Model存储区A2[140-143] Reading Data not equal Writing data, Fail!\n')
        f_report.write('\nModel存储区A2[140-143] Reading Data not equal Writing data, Fail!\n')

A2_226_242_Read = create_string_buffer(16)
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 226, 16, byref(A2_226_242_Read))
if 0 == Res:
    if list(A2_226_241_buf) == list(A2_226_242_Read):
        print('Model存储区A2[226-242] Reading Data equal Writing data, OK!')
        f.write('Model存储区A2[226-242] Reading Data equal Writing data, OK!\n')
        f_report.write('Model存储区A2[226-242] Reading Data equal Writing data, OK!\n')
    else:
        print('Model存储区A2[226-242] Reading Data not equal Writing data, Fail!')
        f.write('Model存储区A2[226-242] Reading Data not equal Writing data, Fail!\n')
        f_report.write('Model存储区A2[226-242] Reading Data not equal Writing data, Fail!\n')

A2_242_243_ReadBuf = ctypes.c_ubyte*2
A2_242_243_Read = A2_242_243_ReadBuf()
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 242, 2, A2_242_243_Read)
if 0 == Res:
    if list(A2_242_243_byte) == list(A2_242_243_Read):
        print('Model存储区A2[242-243] Reading Data equal Writing data, OK!')
        f.write('Model存储区A2[242-243] Reading Data equal Writing data, OK!\n')
        f_report.write('Model存储区A2[242-243] Reading Data equal Writing data, OK!\n')
    else:
        for item in range(len(A2_242_243_byte)):
            print(A2_242_243_byte[item])
        for item in range(len(A2_242_243_Read)):
            print(A2_242_243_Read[item])
        print('Model存储区A2[242-243] Reading Data not equal Writing data, Fail!')
        f.write('Model存储区A2[242-243] Reading Data not equal Writing data, Fail!\n')
        f_report('Model存储区A2[242-243] Reading Data not equal Writing data, Fail!\n')

print("\nItem存储区(BOM编码)检查")
f.write("\nItem存储区(BOM编码)检查\n")
A2_144_159_ReadBuf = ctypes.c_ubyte*16
A2_144_159_Read = A2_144_159_ReadBuf()
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 144, 16, A2_144_159_Read)
if 0 == Res:
    if list(A2_144_159_byte) == list(A2_144_159_Read):
        print('Model存储区A2[144-159] Reading Data equal Writing data, OK!')
        f.write('Model存储区A2[144-159] Reading Data equal Writing data, OK!\n')
        f_report.write('Model存储区A2[144-159] Reading Data equal Writing data, OK!\n')
    else:
        print('Model存储区A2[144-159] Reading Data not equal Writing data, Fail!')
        f.write('Model存储区A2[144-159] Reading Data not equal Writing data, Fail!\n')
        f_report.write('Model存储区A2[144-159] Reading Data not equal Writing data, Fail!\n')

print("\nA2 Restore...")
f.write("\nA2 Restore...\n")
Sfp_User_088Pwd_Entry()
time.sleep(1)

testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 128, 120,
                                           A2RawReadByte)
time.sleep(2)
testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)
Res = 0xFF
A2_128_247_Read = create_string_buffer(120)
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 128, 120,
                                           byref(A2_128_247_Read))
if 0 == Res and list(A2_128_247_Read) == list(A2_128_247_Read):
    print('A2[128-247] restore to 0, OK!')
    f.write('\nA2[128-247] restore to 0, OK!\n')
    f_report.write('A2[128-247] restore OK!\n')
else:
    print('A2[128-247] restore to 0,  Fail!')
    f.write('\nA2[128-247] restore to 0,  Fail!\n')
    f_report.write('A2[128-247] restore Fail!\n')
time.sleep(1)

#########################################################
#       Change to user new password
#########################################################
print("\nPown Off ")
f.write("\nPown Off \n")
testEvb.AteAllPowerOff()
time.sleep(1)
print("\nPown On ")
f.write("\nPown On \n")
testEvb.AteAllPowerOn()
time.sleep(1)
print("\nWrite user default password... ")
f.write("\nWrite user default password... \n")
Sfp_User_088Pwd_Entry()
time.sleep(1)
print("\nWrite user eeprom ")
f.write("\nWrite user eeprom \n")
A2_128_132_buf = ctypes.create_string_buffer(b'XGPON', 5)
testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 128, 5, byref(A2_128_132_buf))
time.sleep(1)

A2WriteDataBuff = ctypes.c_ubyte*4
A2WriteByte = A2WriteDataBuff(0, 2, 3, 4)
print("\nWrite the new user password... ")
f.write("\nWrite the new user password... \n")
testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 119, 4, A2WriteByte)
time.sleep(1)

print("\nPown Off ")
f.write("\nPown Off \n")
testEvb.AteAllPowerOff()
time.sleep(1)
print("\nPown On ")
f.write("\nPown On \n")
testEvb.AteAllPowerOn()
time.sleep(1)
print("\nWrite user new password, check... ")
f.write("\nWrite user new password, check... \n")
A2WriteDataBuff = ctypes.c_ubyte*4
A2WriteByte = A2WriteDataBuff(0, 2, 3, 4)
testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 123, 4, A2WriteByte)

A2ReadDataBuff = create_string_buffer(5)
testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 128, 5, byref(A2ReadDataBuff))
if list(A2ReadDataBuff) == list(A2_128_132_buf):
    print("\nNew user password change success! ")
    f.write("\nNew user password change success! \n")
    f_report.write("\nNew user password change success! \n")
else:
    for i in range(len(A2ReadDataBuff)):
        print(A2ReadDataBuff[i])
    for i in range(len(A2_128_132_buf)):
        print(A2_128_132_buf[i])
    print("\nNew user password change fail! ")
    f.write("\nNew user password change fail! \n")
    f_report.write("\nNew user password change fail! \n")
#########################################################
#           Restore to user default password
#########################################################
print("\nRestore user default password... ")
f.write("\nRestore user default password... \n")

userDefaultPassword = {119:0, 120:0, 121:0x10, 122:0x11}
passwordArray = list(userDefaultPassword.values())
addrArray = list(userDefaultPassword.keys())

#Sfp_Factory_Pwd_Entry(0)
time.sleep(1)

userReadPassword = ctypes.c_ubyte*4
A2WriteByte = userReadPassword(passwordArray[0],passwordArray[1],passwordArray[2],passwordArray[3])
testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], addrArray[0], 4, A2WriteByte)
time.sleep(1)

testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)

Sfp_User_088Pwd_Entry()

A2ReadDataBuff = create_string_buffer(5)
testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 128, 5, byref(A2ReadDataBuff))
if list(A2ReadDataBuff) == list(A2_128_132_buf):
    print("\nRestore user default password success! ")
    f.write("\nRestore user default password success! \n")
    f_report.write("Restore user default password success! \n")
else:
    for i in range(len(A2ReadDataBuff)):
        print(A2ReadDataBuff[i])
    for i in range(len(A2_128_132_buf)):
        print(A2_128_132_buf[i])
    print("\nRestore user default password fail! ")
    f.write("\nRestore user default password fail! \n")
    f_report.write("\nRestore user default password fail! \n")

print("\nA2 Restore...")
f.write("\nA2 Restore...\n")
Sfp_User_088Pwd_Entry()
time.sleep(1)

testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 128, 120,
                                           A2RawReadByte)
time.sleep(2)
testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)
Res = 0xFF
A2_128_247_Read = create_string_buffer(120)
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 128, 120,
                                           byref(A2_128_247_Read))
if 0 == Res and list(A2_128_247_Read) == list(A2_128_247_Read):
    print('A2[128-247] restore to 0, OK!')
    f.write('\nA2[128-247] restore to 0, OK!\n')
    f_report.write('A2[128-247] restore OK!\n')
else:
    print('A2[128-247] restore to 0,  Fail!')
    f.write('\nA2[128-247] restore to 0,  Fail!\n')
    f_report.write('A2[128-247] restore Fail!\n')
time.sleep(1)
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

