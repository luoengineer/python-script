import ctypes
from ctypes import *

import time

# cdecl
objdll = ctypes.cdll.LoadLibrary(".\ATEAPI.dll")
cvidll = ctypes.cdll.LoadLibrary(".\cvidll.dll")

devnum = objdll.AteGetDeviceNums()
print(devnum)

#open usb
devIndex = 0
devChannel = 1
objdll.AteOpenDevice.restype = c_void_p
objdll.AteCloseDevice.argtypes = [c_void_p]

handle = 0
handle = objdll.AteOpenDevice(devIndex)
if handle != 0:
    print("Open USB device {}".format("device_0"))
    objdll.AteCloseDevice(handle)

objdll.AteSffPowerOn(devIndex)
time.sleep(2)

#TODO：i2c reset not complete
#reset usb
#objdll.AteIicReset.argtypes = [c_ulong,c_ubyte,c_ulong]
#I2cRate = 20
#if 0 == objdll.AteIicReset(devIndex,devChannel,I2cRate):
#    print("Reset USB device success")

arrayI2cAddr = [0xA0,0xA2,0xB0,0xB2,0xA4]
print("Find I2C address :",end=' ')
for i2cFind in range(len(arrayI2cAddr)):
    if 0 == objdll.AteIicFind(devIndex, devChannel, arrayI2cAddr[i2cFind]):
        print("0x{0:X}".format(arrayI2cAddr[i2cFind]), end=' ')
print("\n")


currentReadNum = 16
currentReadBuff = ctypes.c_ubyte*currentReadNum
currentReadByte = currentReadBuff()
Res = 0xFF
Res = objdll.AteIicCurrentRead(devIndex, devChannel, arrayI2cAddr[0], currentReadNum, currentReadByte)
if 0 == Res:
if 0 == Res:
    print("current read :",end=' ')
    for i1 in range(currentReadNum):
        print("0x{0:X}".format(currentReadByte[i1]), end=' ')
else:
    print("{0:d}".format(Res))
print("\n")


print("After entry factory password ... ")
factoryPassword = c_ubyte*4
arrAddr = factoryPassword(0xD8, 0x47, 0x54, 0x45)
objdll.AteIicRandomWrite(devIndex, devChannel, arrayI2cAddr[1], 0x7B, 4, byref(arrAddr))

arrayI2cAddr = [0xA0,0xA2,0xB0,0xB2,0xA4]
print("Find I2C address :",end=' ')
for i2cFind in range(len(arrayI2cAddr)):
    if 0 == objdll.AteIicFind(devIndex, devChannel, arrayI2cAddr[i2cFind]):
        print("0x{0:X}".format(arrayI2cAddr[i2cFind]),end=' ')
print("\n")

vi2cAddr_Array = ctypes.c_ubyte*128
serchI2cAddr = vi2cAddr_Array()
if 0 == objdll.AteIicSearch(devIndex, devChannel, serchI2cAddr):
    print("Serched : ",end=' ')
    for i1 in range(128):
        if serchI2cAddr[i1] != 0:
            print("0x{0:X}".format(serchI2cAddr[i1]), end=' ')
    print("\n")
time.sleep(2)

#INT AteIicRandomRead(ULONG iIndex, BYTE channel, BYTE slave, BYTE offset, ULONG readLen, BYTE * readBuf);
randomReadBuff = ctypes.c_ubyte*128
randomReadByte = randomReadBuff()
Res = 0xFF
raddomReadNum = 32
Res = objdll.AteIicRandomRead(devIndex, devChannel, arrayI2cAddr[0], 0, raddomReadNum, randomReadByte)
if 0 == Res:
    print("random read：")
    for i1 in range(raddomReadNum):
        print("0x{0:X}".format(randomReadByte[i1]), end=' ')
else:
    print("{0:d}".format(Res))

print("\n")
boardDllVerNum = 8
boardDllVerBuff = ctypes.c_ubyte*boardDllVerNum
boardVer = boardDllVerBuff()
Res = 0xFF
if 0 == objdll.AteBoardGetDllVer(devIndex, boardVer):
    for i2 in range(boardDllVerNum):
        print(boardVer[i2], end=' ')

print("\n")
boardC51VerNum = 8
boardC51VerBuff = ctypes.c_ubyte*boardC51VerNum
boardC51Ver = boardC51VerBuff()
Res = 0xFF
if 0 == objdll.AteBoardGetC51Ver(devIndex, boardC51Ver):
    for i2 in range(boardC51VerNum):
        print(boardC51Ver[i2], end=' ')

print("\n")
boardC51SnNum = 16
boardC51SnBuff = ctypes.c_ubyte*boardC51SnNum
boardC51Sn = boardC51SnBuff()
Res = 0xFF
if 0 == objdll.AteBoardGetC51Sn(devIndex, boardC51Sn):
    print("board c51 sn:")
    for i2 in range(boardC51VerNum):
        print("{0:d}".format(boardC51Sn[i2]), end=' ')


time.sleep(2)
objdll.AteSffPowerOff(devIndex)


