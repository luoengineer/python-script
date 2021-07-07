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
#B2 default data
B2_Def_Data = {128:0x00, 129:0x00, 130:0x00, 131:0x00, \
               132:0x0B, 133:0x0C, 134:0x0D, 135:0x0E, \
               136:0x0A, 137:0x0B, 138:0x0C, 139:0x0D}


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

def i2c_write_verify():
    i2cWriteBuf = ctypes.c_ubyte * 4
    B2_Test_Data = i2cWriteBuf(1, 2, 3, 4)
    testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, ComboSfpI2cAddr[3], 140, 4, byref(B2_Test_Data))
    time.sleep(1)
    B2ReadbackDataBuff = ctypes.c_ubyte*4
    B2ReadbackByte = B2ReadbackDataBuff()
    Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[3], 140, 4, B2ReadbackByte)
    cnt = 0
    if 0 == Res:
        #return operator.eq(i2cWriteBuf, B2ReadbackDataBuff)
        for item in range(len(B2ReadbackByte)):
            if B2_Test_Data[item] == B2ReadbackByte[item]:
                cnt += 1
        if cnt == 4:
            return True
        else:
            return False
    else:
        return "fail"

def restore_default_data():
    i2cWriteBuf = ctypes.c_ubyte * 4
    B2_Default_Data = i2cWriteBuf(0, 0, 0, 0)
    Sfp_Factory_Pwd_Entry(user_password_type)
    testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, ComboSfpI2cAddr[3], 140, 4, byref(B2_Default_Data))
    time.sleep(2)
    B2ReadbackDataBuff = ctypes.c_ubyte * 4
    B2ReadbackByte = B2ReadbackDataBuff()
    cnt = 0
    Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[3], 140, 4, B2ReadbackByte)
    if 0 == Res:
        for item in range(len(B2ReadbackByte)):
            if B2_Default_Data[item] == B2ReadbackByte[item]:
                cnt += 1
        if cnt == 4:
            return True
        else:
            return False
    else:
        return "fail"
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
print("099 B2 encryption test, start time : {}".format(dateTime))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\n099 B2 encryption test, start time : {}".format(dateTime))
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
#         Read with no any password(default)
#########################################################
print("\nNot write any password, read B2 Direct High")
f.write("\nNot write any password, read B2 Direct High\n")

B2RawDataBuff = ctypes.c_ubyte*128
B2RawReadByte = B2RawDataBuff()
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[3], 128, 128, B2RawReadByte)
if 0 == Res:
    for item in range(len(B2RawReadByte)):
        if 0 == B2RawReadByte[item]:
            print('B2[{}]=0x{:0>2X},{}'.format(128 + item, B2RawReadByte[item], 'OK'))
            f.write('B2[{}]=0x{:0>2X},{}\n'.format(128 + item, B2RawReadByte[item], 'OK'))
        else:
            print('B2[{}]=0x{:0>2X},{}'.format(128 + item, B2RawReadByte[item], 'Fail'))
            f.write('B2[{}]=0x{:0>2X},{}\n'.format(128 + item, B2RawReadByte[item], 'Fail'))

print("\nWrite to B2 Direct High")
f.write("\nWrite to B2 Direct High\n")
ret = i2c_write_verify()
if "fail" == ret:
    print("I2C read fail, stop test ! ")
    sys.exit()
if True == ret:
    print("\nError: B2 Direct High has been writen with no any password")
    f.write("\nError: B2 Direct High has been writen with no any password\n")
else:
    print("\nOK: B2 Direct High has not been writen with no any password")
    f.write("\nOK: B2 Direct High has not been writen with no any password\n")

ret = restore_default_data()
if "fail" == ret:
    print("I2C read fail, stop test ! ")
    sys.exit()
if True == ret:
    print("\nOK: restore default data")
    f.write("\nOK: restore default data\n")
else:
    print("\nFail: not restore default data")
    f.write("\nFail: not restore default data\n")
#clear any password
testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)


#########################################################
#            Read with user read password
#########################################################
print("\nInput user reading password, read B2 Direct High")
f.write("\nInput user reading password, read B2 Direct High\n")
Sfp_User_Read_099Pwd_Entry()
time.sleep(1)

B2RawDataBuff = ctypes.c_ubyte*128
B2RawReadByte = B2RawDataBuff()
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[3], 128, 128, B2RawReadByte)
if 0 == Res:
    #B2_Read_128to139 = [B2RawReadByte[item] for item in range(12) if B2RawReadByte[item] == B2_Def_Data[128+item]]
    for item in range(12):
        if B2RawReadByte[item] == B2_Def_Data[item+128]:
            print('B2[{}]=0x{:0>2X},{}'.format(128+item, B2RawReadByte[item], 'OK'))
            f.write('B2[{}]=0x{:0>2X},{}\n'.format(128+item, B2RawReadByte[item], 'OK'))
        else:
            print('B2[{}]=0x{:0>2X},{}'.format(128 + item, B2RawReadByte[item], 'Fail'))
            f.write('B2[{}]=0x{:0>2X},{}\n'.format(128 + item, B2RawReadByte[item], 'Fail'))
    for item in range(128-12):
        if 0 == B2RawReadByte[item+12]:
            print('B2[{}]=0x{:0>2X},{}'.format(140 + item, B2RawReadByte[item+12], 'OK'))
            f.write('B2[{}]=0x{:0>2X},{}\n'.format(140 + item, B2RawReadByte[item+12], 'OK'))
        else:
            print('B2[{}]=0x{:0>2X},{}'.format(140 + item, B2RawReadByte[item+12], 'Fail'))
            f.write('B2[{}]=0x{:0>2X},{}\n'.format(140 + item, B2RawReadByte[item + 12], 'Fail'))

print("\nWrite to B2 Direct High")
f.write("\nWrite to B2 Direct High\n")
ret = i2c_write_verify()
if "fail" == ret:
    print("I2C read fail, stop test ! ")
    sys.exit()
if True == ret:
    print("\nError: B2 Direct High has been writen with user reading password")
    f.write("\nError: B2 Direct High has been writen with user reading password\n")
else:
    print("\nOK: B2 Direct High has not been writen with user reading password")
    f.write("\nOK: B2 Direct High has not been writen with user reading password\n")

ret = restore_default_data()
if "fail" == ret:
    print("I2C read fail, stop test ! ")
    sys.exit()
if True == ret:
    print("\nOK: restore default data")
    f.write("\nOK: restore default data\n")
else:
    print("\nFail: not restore default data")
    f.write("\nFail: not restore default data\n")
#clear any password
testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)

#########################################################
#               Read with user write password
#########################################################
print("\nInput user writing password, read B2 Direct High")
f.write("\nInput user writing password, read B2 Direct High\n")
Sfp_User_Write_099Pwd_Entry()
time.sleep(1)
B2RawDataBuff = ctypes.c_ubyte*128
B2RawReadByte = B2RawDataBuff()
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[3], 128, 128, B2RawReadByte)
if 0 == Res:
    #B2_Read_128to139 = [B2RawReadByte[item] for item in range(12) if B2RawReadByte[item] == B2_Def_Data[128+item]]
    for item in range(12):
        if B2RawReadByte[item] == B2_Def_Data[item+128]:
            print('B2[{}]=0x{:0>2X},{}'.format(128+item, B2RawReadByte[item], 'OK'))
            f.write('B2[{}]=0x{:0>2X},{}\n'.format(128 + item, B2RawReadByte[item], 'OK'))
        else:
            print('B2[{}]=0x{:0>2X},{}'.format(128 + item, B2RawReadByte[item], 'Fail'))
            f.write('B2[{}]=0x{:0>2X},{}\n'.format(128 + item, B2RawReadByte[item], 'Fail'))
    for item in range(128-12):
        if 0 == B2RawReadByte[item+12]:
            print('B2[{}]=0x{:0>2X},{}'.format(140 + item, B2RawReadByte[item+12], 'OK'))
            f.write('B2[{}]=0x{:0>2X},{}\n'.format(140 + item, B2RawReadByte[item + 12], 'OK'))
        else:
            print('B2[{}]=0x{:0>2X},{}'.format(140 + item, B2RawReadByte[item+12], 'Fail'))
            f.write('B2[{}]=0x{:0>2X},{}\n'.format(140 + item, B2RawReadByte[item + 12], 'Fail'))

print("\nWrite to B2 Direct High")
f.write("\nWrite to B2 Direct High\n")
ret = i2c_write_verify()
if "fail" == ret:
    print("I2C read fail, stop test ! ")
    sys.exit()
if True == ret:
    print("\nOK: B2 Direct High has been writen with user wrting password")
    f.write("\nOK: B2 Direct High has been writen with user writing password\n")
else:
    print("\nError: B2 Direct High has not been writen with user writing password")
    f.write("\nError: B2 Direct High has not been writen with user writing password\n")

ret = restore_default_data()
if "fail" == ret:
    print("I2C read fail, stop test ! ")
    sys.exit()
if True == ret:
    print("\nOK: restore default data")
    f.write("\nOK: restore default data\n")
else:
    print("\nFail: not restore default data")
    f.write("\nFail: not restore default data\n")
#clear any password
testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)

#########################################################
#               Read with factory password
#########################################################
print("\nInput factory password, read B2 Direct High")
f.write("\nInput factory password, read B2 Direct High\n")
Sfp_Factory_Pwd_Entry(user_password_type)
time.sleep(1)
B2RawDataBuff = ctypes.c_ubyte*128
B2RawReadByte = B2RawDataBuff()
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[3], 128, 128, B2RawReadByte)
if 0 == Res:
    #B2_Read_128to139 = [B2RawReadByte[item] for item in range(12) if B2RawReadByte[item] == B2_Def_Data[128+item]]
    for item in range(12):
        if B2RawReadByte[item] == B2_Def_Data[item+128]:
            print('B2[{}]=0x{:0>2X},{}'.format(128+item, B2RawReadByte[item], 'OK'))
            f.write('B2[{}]=0x{:0>2X},{}\n'.format(128 + item, B2RawReadByte[item], 'OK'))
        else:
            print('B2[{}]=0x{:0>2X},{}'.format(128 + item, B2RawReadByte[item], 'Fail'))
            f.write('B2[{}]=0x{:0>2X},{}\n'.format(128 + item, B2RawReadByte[item], 'Fail'))

    for item in range(128-12):
        if 0 == B2RawReadByte[item+12]:
            print('B2[{}]=0x{:0>2X},{}'.format(140 + item, B2RawReadByte[item+12], 'OK'))
            f.write('B2[{}]=0x{:0>2X},{}\n'.format(140 + item, B2RawReadByte[item + 12], 'OK'))
        else:
            print('B2[{}]=0x{:0>2X},{}'.format(140 + item, B2RawReadByte[item+12], 'Fail'))
            f.write('B2[{}]=0x{:0>2X},{}\n'.format(140 + item, B2RawReadByte[item + 12], 'Fail'))

print("\nWrite to B2 Direct High")
f.write("\nWrite to B2 Direct High\n")
ret = i2c_write_verify()
if "fail" == ret:
    print("I2C read fail, stop test ! ")
    sys.exit()
if True == ret:
    print("\nOK: B2 Direct High has been writen with factory password")
    f.write("\nOK: B2 Direct High has been writen with factory password\n")
else:
    print("\nError: B2 Direct High has not been writen with factory password")
    f.write("\nError: B2 Direct High has not been writen with factory password\n")

ret = restore_default_data()
if "fail" == ret:
    print("I2C read fail, stop test ! ")
    sys.exit()
if True == ret:
    print("\nOK: restore default data")
    f.write("\nOK: restore default data\n")
else:
    print("\nFail: not restore default data")
    f.write("\nFail: not restore default data\n")

dateTime = time.strptime(time.asctime())
dateTime = "{:4}-{:02}-{:02} {:02}:{:02}:{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
print("\n****************************************************************************")
print("099 B2 encryption test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\n099 B2 encryption test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
f.write("\n****************************************************************************")

testEvb.AteAllPowerOff()
f.close()

