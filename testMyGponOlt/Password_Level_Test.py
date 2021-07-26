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
#Test times
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
def Sfp_User_Pwd_Entry():
    i2cWriteBuf = c_ubyte * 4
    userPwd = i2cWriteBuf(0x00, 0x00, 0x10, 0x11)
    testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 123, 4, byref(userPwd))
    del i2cWriteBuf, userPwd

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
print("Password level test, start time : {}".format(dateTime))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nPassword level test, start time : {}".format(dateTime))
f.write("\n****************************************************************************")
print("{}".format(testTitle))
f.write('\n'+testTitle)

#########################################################
#   test step 1 : Backup A0 0-255 and A2 0-95 and A2 128-255
#########################################################
#read raw A0 direct data
A0RawDataBuff = ctypes.c_ubyte*128
A0RawReadByte = A0RawDataBuff()
f.write("\nA0 0-127 raw data: \n")
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[0], 0, 128, A0RawReadByte)
if 0 == Res:
    for item in range(len(A0RawReadByte)):
        f.write(str(hex(A0RawReadByte[item]))+',')
else:
    f.write('read A0 direct raw data fail.'+'\n')
    print('read A0 direct raw data fail.' + '\n')
    f.close()
    sys.exit()
#read raw A0 direct high data
A0_direct_high_RawDataBuff = ctypes.c_ubyte*128
A0_direct_high_RawReadByte = A0_direct_high_RawDataBuff()
f.write("\nA0 direct high raw data: \n")
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[0], 128, 128, A0_direct_high_RawReadByte)
if 0 == Res:
    for item in range(len(A0_direct_high_RawReadByte)):
        f.write(str(hex(A0_direct_high_RawReadByte[item]))+',')
else:
    f.write('read A0 direct high raw data fail.'+'\n')
    print('read A0 direct high raw data fail.' + '\n')
    f.close()
    sys.exit()

#read raw A2 data
A2_Direct_RawDataBuff = ctypes.c_ubyte*96
A2_Direct_RawReadByte = A2_Direct_RawDataBuff()
f.write("\nA2 0-95 raw data: \n")
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 0, 96, A2_Direct_RawReadByte)
if 0 == Res:
    for item in range(len(A2_Direct_RawReadByte)):
        f.write(str(hex(A2_Direct_RawReadByte[item]))+',')
else:
    f.write('read A2 0-95 raw data fail.'+'\n')
    print('read A2 0-95 raw data fail.' + '\n')
    f.close()
    sys.exit()

A2_Direct_High_RawDataBuff = ctypes.c_ubyte*128
A2_Direct_High_RawReadByte = A2_Direct_High_RawDataBuff()
f.write("\nA2 128-255 raw data: \n")
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 128, 128, A2_Direct_High_RawReadByte)
if 0 == Res:
    for item in range(len(A2_Direct_High_RawReadByte)):
        f.write(str(hex(A2_Direct_High_RawReadByte[item]))+',')
else:
    f.write('read A2 128-255 raw data fail.'+'\n')
    print('read A2 128-255 raw data fail.' + '\n')
    f.close()
    sys.exit()

#Run test
print("\nPOR...")
f.write("\nPOR...")
#clear any password
testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)

#########################################################
#   test step 2 : no any password write A0 0-127
#########################################################
print("\nno any passsword, write A0 direct ...")
f.write("\nno any passsword, write A0 direct ...")

A0WriteDataBuff = [0x00] * 128
A0WriteDataBuff = random_int_list(0, 256, 128)
A0WriteByte = (c_ubyte * 128)(*A0WriteDataBuff)

print('\nwrite :\n')
f.write('\nwrite :\n')
for item in range(len(A0WriteByte)):
    print("{},".format(str(hex(A0WriteByte[item]))), end='')
    f.write(str(hex(A0WriteByte[item])) + ',')
f.write('\n')
print("\n")
testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[0], 0, 128, byref(A0WriteByte))
time.sleep(1)

testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)

A0ReadDataBuff = ctypes.c_ubyte * 256
randomReadByte = A0ReadDataBuff()
testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[0], 0, 128, randomReadByte)

print('read :\n')
f.write('read :\n')
for item in range(len(randomReadByte)):
    print("{},".format(str(hex(randomReadByte[item]))), end='')
    f.write(str(hex(randomReadByte[item])) + ',')
print('\n')
f.write('\n')

wr_and_rd_success = 0
for item in range(128):
    if randomReadByte[item] == A0WriteByte[item]:
        wr_and_rd_success += 1

print("\n")
f.write("\n")

if wr_and_rd_success == 128:
    #totalSuccess += 1
    f.write('ERROR : no any password, write A0 direct data equal read data.' + '\n\n')
    print("ERROR: No any password, write A0 direct data equal read data.")
else:
    f.write('PASS : no any password, write A0 direct data not equal read data.' + '\n\n')
    print("PASS: No any password, write A0 direct data not equal read data.")

print("\nPOR...")
f.write("\nPOR...")
#clear any password
testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)


#########################################################
#   test step 3 : no any password write A0 128-255
#########################################################
print("\nno any passsword, write A0 direct high ...")
f.write("\nno any passsword, write A0 direct high ...")

A0WriteDataBuff = [0x00] * 128
A0WriteDataBuff = random_int_list(0, 256, 128)
A0WriteByte = (c_ubyte * 128)(*A0WriteDataBuff)

print('\nwrite :\n')
f.write('\nwrite :\n')
for item in range(len(A0WriteByte)):
    print("{},".format(str(hex(A0WriteByte[item]))), end='')
    f.write(str(hex(A0WriteByte[item])) + ',')
f.write('\n')
print("\n")
testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[0], 128, 128, byref(A0WriteByte))
time.sleep(1)

testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)

A0ReadDataBuff = ctypes.c_ubyte * 256
randomReadByte = A0ReadDataBuff()
testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[0], 128, 128, randomReadByte)

print('read :\n')
f.write('read :\n')
for item in range(len(randomReadByte)):
    print("{},".format(str(hex(randomReadByte[item]))), end='')
    f.write(str(hex(randomReadByte[item])) + ',')
print('\n')
f.write('\n')

wr_and_rd_success = 0
for item in range(128):
    if randomReadByte[item] == A0WriteByte[item]:
        wr_and_rd_success += 1

print("\n")
f.write("\n")

if wr_and_rd_success == 128:
    #totalSuccess += 1
    f.write('ERROR : no any password, write A0 direct high data equal read data.' + '\n\n')
    print("ERROR: No any password, write A0 direct high data equal read data.")
else:
    f.write('PASS : no any password, write A0 direct high data not equal read data.' + '\n\n')
    print("PASS: No any password, write A0 direct high data not equal read data.")

print("\nPOR...")
f.write("\nPOR...")
#clear any password
testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)

#########################################################
#   test step 4 : factory password write A0 0-127
#########################################################
print("\nwrite factory passsword, write A0 direct  ...")
f.write("\nwrite factory passsword, write A0 direct ...")

Sfp_Factory_Pwd_Entry(user_password_type)
time.sleep(1)

A0WriteDataBuff = [0x00] * 128
A0WriteDataBuff = random_int_list(0, 256, 128)
A0WriteByte = (c_ubyte * 128)(*A0WriteDataBuff)

print('write :\n')
f.write('write :\n')
for item in range(len(A0WriteByte)):
    print("{},".format(str(hex(A0WriteByte[item]))), end='')
    f.write(str(hex(A0WriteByte[item])) + ',')
f.write('\n')
print("\n")
testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[0], 0, 128, byref(A0WriteByte))
time.sleep(2)

testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)

A0ReadDataBuff = ctypes.c_ubyte * 128
randomReadByte = A0ReadDataBuff()
testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[0], 0, 128, randomReadByte)

print('read :\n')
f.write('read :\n')
for item in range(len(randomReadByte)):
    print("{},".format(str(hex(randomReadByte[item]))), end='')
    f.write(str(hex(randomReadByte[item])) + ',')
print('\n')
f.write('\n')

wr_and_rd_success = 0
for item in range(len(randomReadByte)):
    if randomReadByte[item] == A0WriteByte[item]:
        wr_and_rd_success += 1
print("\n")
f.write("\n")
if wr_and_rd_success == 128:
    f.write('PASS : factory password, write A0 direct data equal read data.' + '\n\n')
    print("PASS: factory password, write A0 direct data equal read data.")
else:
    f.write('ERROR : factory password, write A0 direct data not equal read data.' + '\n\n')
    print("ERROR: factory password, write A0 direct data not equal read data.")

print("\nPOR...")
f.write("\nPOR...")
#clear any password
testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)

#########################################################
#   test step 5 : factory password write A0 128-255
#########################################################
print("\nwrite factory passsword ...")
f.write("\nwrite factory passsword ...")

Sfp_Factory_Pwd_Entry(user_password_type)
time.sleep(1)

A0WriteDataBuff = [0x00] * 128
A0WriteDataBuff = random_int_list(0, 256, 128)
A0WriteByte = (c_ubyte * 128)(*A0WriteDataBuff)

print('\nwrite :\n')
f.write('\nwrite :\n')
for item in range(len(A0WriteByte)):
    print("{},".format(str(hex(A0WriteByte[item]))), end='')
    f.write(str(hex(A0WriteByte[item])) + ',')
f.write('\n')
print("\n")
testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[0], 128, 128, byref(A0WriteByte))
time.sleep(2)

testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)

A0ReadDataBuff = ctypes.c_ubyte * 128
randomReadByte = A0ReadDataBuff()
testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[0], 128, 128, randomReadByte)

print('read :\n')
f.write('read :\n')
for item in range(len(randomReadByte)):
    print("{},".format(str(hex(randomReadByte[item]))), end='')
    f.write(str(hex(randomReadByte[item])) + ',')
print('\n')
f.write('\n')

wr_and_rd_success = 0
for item in range(len(randomReadByte)):
    if randomReadByte[item] == A0WriteByte[item]:
        wr_and_rd_success += 1
print("\n")
f.write("\n")
if wr_and_rd_success == 128:
    f.write('PASS : factory password, write A0 direct high data equal read data.' + '\n\n')
    print("PASS: factory password, write A0 direct high data equal read data.")
else:
    f.write('ERROR : factory password, write A0 direct high data not equal read data.' + '\n\n')
    print("ERROR: factory password, write A0 direct high data not equal read data.")

print("\nPOR...")
f.write("\nPOR...")
#clear any password
testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)

#########################################################
#    test step 6 :  no any password write A2 0-95
#########################################################
print("\nNo any passsword, write A2 direct ...")
f.write("\nNo any passsword, wirte A2 direct ...")

A2_Direct_WriteDataBuff = [0x00] * 96
A2_Direct_WriteDataBuff = random_int_list(0, 256, 96)
A2_Direct_WriteByte = (c_ubyte * 96)(*A2_Direct_WriteDataBuff)

print('\nwrite :\n')
f.write('\nwrite :\n')
for item in range(len(A2_Direct_WriteByte)):
    print("{},".format(str(hex(A2_Direct_WriteByte[item]))), end='')
    f.write(str(hex(A2_Direct_WriteByte[item])) + ',')
f.write('\n')
print("\n")
testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 0, 96, byref(A2_Direct_WriteByte))
time.sleep(1)

testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)

A2_Direct_ReadDataBuff = ctypes.c_ubyte * 96
A2_Direct_ReadByte = A2_Direct_ReadDataBuff()
testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 0, 96, A2_Direct_ReadByte)

print('read :\n')
f.write('read :\n')
for item in range(len(A2_Direct_ReadByte)):
    print("{},".format(str(hex(A2_Direct_ReadByte[item]))), end='')
    f.write(str(hex(A2_Direct_ReadByte[item])) + ',')
print('\n')
f.write('\n')

wr_and_rd_success = 0
for item in range(96):
    if A2_Direct_ReadByte[item] == A2_Direct_WriteByte[item]:
        wr_and_rd_success += 1
print("\n")
f.write("\n")
if wr_and_rd_success == 96:
    f.write('ERROR : no any password, write A2 direct data equal read data.' + '\n\n')
    print("ERROR: no any password, write A2 direct data equal read data.")
else:
    f.write('PASS: no any password, write A2 direct data not equal read data.' + '\n\n')
    print("PASS: no any password, write A2 direct data not equal read data.")

print("POR...")
f.write("POR...")
#clear any password
testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)

#########################################################
#    test step 7 :  no any password write A2 128-255
#########################################################
print("\nNo any passsword, write A2 direct high ...")
f.write("\nNo any passsword, write A2 direct high ...")

A2_Direct_High_WriteDataBuff = [0x00] * 128
A2_Direct_High_WriteDataBuff = random_int_list(0, 256, 128)
A2_Direct_High_WriteByte = (c_ubyte * 128)(*A2_Direct_High_WriteDataBuff)

print('\nwrite :\n')
f.write('\nwrite :\n')
for item in range(len(A2_Direct_High_WriteByte)):
    print("{},".format(str(hex(A2_Direct_High_WriteByte[item]))), end='')
    f.write(str(hex(A2_Direct_High_WriteByte[item])) + ',')
f.write('\n')
print("\n")
testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 128, 128, byref(A2_Direct_High_WriteByte))
time.sleep(1)

testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)

A2_Direct_High_ReadDataBuff = ctypes.c_ubyte * 128
A2_Direct_High_ReadByte = A2_Direct_High_ReadDataBuff()
testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 128, 128, A2_Direct_High_ReadByte)

print('read :\n')
f.write('read :\n')
for item in range(len(A2_Direct_High_ReadByte)):
    print("{},".format(str(hex(A2_Direct_High_ReadByte[item]))), end='')
    f.write(str(hex(A2_Direct_High_ReadByte[item])) + ',')
print('\n')
f.write('\n')

wr_and_rd_success = 0
for item in range(128):
    if A2_Direct_High_ReadByte[item] == A2_Direct_High_WriteByte[item]:
        wr_and_rd_success += 1
print("\n")
f.write("\n")
if wr_and_rd_success == 128:
    f.write('ERROR : no any password, write A2 direct high data equal read data.' + '\n\n')
    print("ERROR: no any password, write A2 direct high data equal read data.")
else:
    f.write('PASS : no any password, write A2 direct high data not equal read data.' + '\n\n')
    print("PASS: no any password, write A2 direct high data not equal read data.")



#########################################################
#    test step 8 :  factory password write A2 0-95
#########################################################
print("\nwrite factory passsword, write A2 direct ...")
f.write("\nwrite factory passsword, wirte A2 direct ...")
Sfp_Factory_Pwd_Entry(user_password_type)

A2_Direct_WriteDataBuff = [0x00] * 96
A2_Direct_WriteDataBuff = random_int_list(0, 256, 96)
A2_Direct_WriteByte = (c_ubyte * 96)(*A2_Direct_WriteDataBuff)

print('\nwrite :\n')
f.write('\nwrite :\n')
for item in range(len(A2_Direct_WriteByte)):
    print("{},".format(str(hex(A2_Direct_WriteByte[item]))), end='')
    f.write(str(hex(A2_Direct_WriteByte[item])) + ',')
f.write('\n')
print("\n")
testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 0, 96, byref(A2_Direct_WriteByte))
time.sleep(1)

testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)

A2_Direct_ReadDataBuff = ctypes.c_ubyte * 96
A2_Direct_ReadByte = A2_Direct_ReadDataBuff()
testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 0, 96, A2_Direct_ReadByte)

print('read :\n')
f.write('read :\n')
for item in range(len(A2_Direct_ReadByte)):
    print("{},".format(str(hex(A2_Direct_ReadByte[item]))), end='')
    f.write(str(hex(A2_Direct_ReadByte[item])) + ',')
print('\n')
f.write('\n')

wr_and_rd_success = 0
for item in range(96):
    if A2_Direct_ReadByte[item] == A2_Direct_WriteByte[item]:
        wr_and_rd_success += 1
print("\n")
f.write("\n")
if wr_and_rd_success == 96:
    #totalSuccess += 1
    f.write('PASS : factory password, write A2 direct data equal read data.' + '\n\n')
    print("PASS: factory password, write A2 direct data equal read data.")
else:
    f.write('ERROR : factory password, write A2 direct data not equal read data.' + '\n\n')
    print("ERROR: factory password, write A2 direct data not equal read data.")

print("POR...")
f.write("POR...")
#clear any password
testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)

#########################################################
#    test step 9 :  factory password write A2 128-255
#########################################################
print("\nwrite factory passsword, write A2 direct high ...")
f.write("\nwrite factory passsword, write A2 direct high ...")
Sfp_Factory_Pwd_Entry(user_password_type)

A2_Direct_High_WriteDataBuff = [0x00] * 128
A2_Direct_High_WriteDataBuff = random_int_list(0, 256, 128)
A2_Direct_High_WriteByte = (c_ubyte * 128)(*A2_Direct_High_WriteDataBuff)

print('\nwrite :\n')
f.write('\nwrite :\n')
for item in range(len(A2_Direct_High_WriteByte)):
    print("{},".format(str(hex(A2_Direct_High_WriteByte[item]))), end='')
    f.write(str(hex(A2_Direct_High_WriteByte[item])) + ',')
f.write('\n')
print("\n")
testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 128, 128, byref(A2_Direct_High_WriteByte))
time.sleep(1)

testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)

A2_Direct_High_ReadDataBuff = ctypes.c_ubyte * 128
A2_Direct_High_ReadByte = A2_Direct_High_ReadDataBuff()
testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 128, 128, A2_Direct_High_ReadByte)

print('read :\n')
f.write('read :\n')
for item in range(len(A2_Direct_High_ReadByte)):
    print("{},".format(str(hex(A2_Direct_High_ReadByte[item]))), end='')
    f.write(str(hex(A2_Direct_High_ReadByte[item])) + ',')
print('\n')
f.write('\n')

wr_and_rd_success = 0
for item in range(128):
    if A2_Direct_High_ReadByte[item] == A2_Direct_High_WriteByte[item]:
        wr_and_rd_success += 1
print("\n")
f.write("\n")
if wr_and_rd_success == 128:
    #totalSuccess += 1
    f.write('PASS : factory password, write A2 direct high data equal read data.' + '\n\n')
    print("PASS: factory password, write A2 direct high data equal read data.")
else:
    f.write('ERROR : factory password, write A2 direct high data not equal read data.' + '\n\n')
    print("ERROR: factory password, write A2 direct high data not equal read data.")


#########################################################
#    test step 10 :  restore all
#########################################################
#restore A0 0-127
print("POR...")
f.write("POR...")
#clear any password
testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)

Sfp_Factory_Pwd_Entry(user_password_type)
time.sleep(1)

testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[0], 0, 128, byref(A0RawReadByte))
time.sleep(1)

testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)
Sfp_Factory_Pwd_Entry(user_password_type)
time.sleep(1)

A0ReadDataBuff = ctypes.c_ubyte * 128
randomReadByte = A0ReadDataBuff()
testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[0], 0, 128, randomReadByte)
if True == operator.eq(A0RawDataBuff, A0ReadDataBuff):
    f.write('A0 direct restore success.' + '\n')
    print("A0 direct restore success.")
else:
    f.write('A0 direct restore fail.' + '\n')
    print("A0 direct restore fail.")
#restore A0 128-255
print("POR...")
f.write("POR...")
#clear any password
testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)

Sfp_Factory_Pwd_Entry(user_password_type)
time.sleep(1)

testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[0], 128, 128, byref(A0_direct_high_RawReadByte))
time.sleep(1)

testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)
Sfp_Factory_Pwd_Entry(user_password_type)
time.sleep(1)

A0ReadDataBuff = ctypes.c_ubyte * 128
randomReadByte = A0ReadDataBuff()
testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[0], 128, 128, randomReadByte)
if True == operator.eq(A0_direct_high_RawDataBuff, A0ReadDataBuff):
    f.write('A0 direct high restore success.' + '\n')
    print("A0 direct high restore success.")
else:
    f.write('A0 direct high restore fail.' + '\n')
    print("A0 direct high restore fail.")

#restore A2 direct
print("POR...")
f.write("POR...")
#clear any password
testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)

Sfp_Factory_Pwd_Entry(user_password_type)
time.sleep(1)

testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 0, 96, byref(A2_Direct_RawReadByte))
time.sleep(1)

testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)
Sfp_Factory_Pwd_Entry(user_password_type)
time.sleep(1)

A2_Direct_ReadDataBuff = ctypes.c_ubyte * 96
A2_Direct_ReadByte = A2_Direct_ReadDataBuff()
testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 0, 96, A2_Direct_ReadByte)
if True == operator.eq(A2_Direct_RawDataBuff, A2_Direct_ReadDataBuff):
    f.write('A2 direct restore success.' + '\n')
    print("A2 direct restore success.")
else:
    f.write('A2 direct restore fail.' + '\n')
    print("A2 direct restore fail.")

#restore A2 direct high
print("POR...")
f.write("POR...")
#clear any password
testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)

Sfp_Factory_Pwd_Entry(user_password_type)
time.sleep(1)

testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 128, 128, byref(A2_Direct_High_RawReadByte))
time.sleep(1)

testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)
Sfp_Factory_Pwd_Entry(user_password_type)
time.sleep(1)

A2_Direct_High_ReadDataBuff = ctypes.c_ubyte * 128
A2_Direct_High_ReadByte = A2_Direct_High_ReadDataBuff()
testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 128, 128, A2_Direct_High_ReadByte)
if True == operator.eq(A2_Direct_High_RawDataBuff, A2_Direct_High_ReadDataBuff):
    f.write('A2 direct high restore success.' + '\n')
    print("A2 direct high restore success.")
else:
    f.write('A2 direct high restore fail.' + '\n')
    print("A2 direct high restore fail.")


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

