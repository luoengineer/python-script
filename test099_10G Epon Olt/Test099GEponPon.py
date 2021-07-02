import ctypes
from ctypes import *
import time
from cmdServ import devUsbIndex, devSffChannel, objdll, cmdservdll
from cmdServ import Sfp_Factory_Pwd_Entry, AteAllPowerOn, AteAllPowerOff, openUsbDevice

#########################################################
#               Test Configuration
#########################################################
#True or False
A0_WRITE_READ_REPEATED_TEST = False
A2_WRITE_READ_REPEATED_TEST = False
B0_WRITE_READ_REPEATED_TEST = False
B2_WRITE_READ_REPEATED_TEST = False
ENCRYPTION_RULE_TEST        = True


#########################################################
#               I2C address Configuration
#########################################################
# Product list
ComboSfpI2cAddr = [0xA0,0xA2,0xB0,0xB2,0xA4]
SfpI2cAddr = [0xA0,0xA2,0xA4]
XfpI2dAddr = [0xA0,0xA4]

#########################################################
#               Load DLL
#########################################################
objdll = ctypes.cdll.LoadLibrary(".\AteApi.dll")
cmdservdll = ctypes.windll.LoadLibrary(".\SuperCommand.dll")

#########################################################
#               Subroutines
#########################################################
def Sfp_Factory_Pwd_Entry():
    i2cWriteBuf = c_ubyte * 4
    factoryPwd = i2cWriteBuf(0x58, 0x47, 0x54, 0x45)
    objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 123, 4, byref(factoryPwd))

def AteAllPowerOn(dev_Usb_Index):
    objdll.AteSffPowerOn(dev_Usb_Index)
    objdll.AteSfpPowerOn(dev_Usb_Index)

def AteAllPowerOff(dev_Usb_Index):
    objdll.AteSffPowerOff(dev_Usb_Index)
    objdll.AteSfpPowerOff(dev_Usb_Index)
   
def I2C_Read(nDev, nReg, nLen, pbyBuf):
    pbyValBuff = ctypes.c_ubyte * 256
    pbyVal = pbyValBuff()
    #print("{},{},{}".format(nDev, nReg, nLen))
    wRes = objdll.AteIicRandomRead(devUsbIndex, devSffChannel, nDev, nReg, nLen, pbyVal)
    if 0 == wRes:
        for i in range(nLen):
            pbyBuf[i] = pbyVal[i]
            #print("{}".format(pbyBuf[i]), end=' ')
    return wRes
    
def I2C_Write(nDev, nReg, nLen, pbyDat):
    pbyValBuff = ctypes.c_ubyte * 256
    pbyVal = pbyValBuff()
    for i in range(nLen):
        #print("{}".format((i)%256), end=' ')
        #print("{}".format(pbyDat[i]), end=' ')
        pbyVal[i % 256] = pbyDat[i]
        #print("{}".format(pbyVal[i]))
    byRes = objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, nDev, nReg, nLen, byref(pbyVal))
    return byRes
    


#########################################################
#               Open USB Device
#########################################################
usbHandle = 0
usbHandle = objdll.AteOpenDevice(devUsbIndex)
if usbHandle != 0:
    print("Open USB device {}".format("device_0"))
    objdll.AteCloseDevice(usbHandle)

#########################################################
#               Slot Power On
#########################################################
AteAllPowerOn(devUsbIndex)
time.sleep(2)

#########################################################
#               Entry Password
#########################################################
Sfp_Factory_Pwd_Entry()
time.sleep(1)

#########################################################
#               Regsite Sevices
#########################################################
cmdType = b"I2C_WRITE"
I2C_Write_FUNC = WINFUNCTYPE(c_int, c_int, c_int, c_int, POINTER(c_ubyte))
_i2c_write_func = I2C_Write_FUNC(I2C_Write)
cmdservdll.RegistCallBackFunciton(string_at(cmdType), _i2c_write_func)

cmdType = b'I2C_READ'
I2C_Read_FUNC = WINFUNCTYPE(c_int, c_int, c_int, c_int, POINTER(c_ubyte))
_i2c_read_func = I2C_Read_FUNC(I2C_Read)
cmdservdll.RegistCallBackFunciton(string_at(cmdType), _i2c_read_func)

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
    for item in range(len(strCmdOut)):
        if 0x00 != strCmdOut[item]:
            print("{}".format(chr(strCmdOut[item])), end='')
            strFwVer.append(chr(strCmdOut[item]))
            #f.write(chr(strCmdOut[item]))
    else:
        print("{0:d}".format(retStauts))
        #f.write(str(retStauts))
strFwVer = ''.join(strFwVer)


#########################################################
#                 Open File
#########################################################
dateTime = time.strptime(time.asctime())
dateTime = "{:4}{:02}{:02}{:02}{:02}{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
testTitle = strFwVer+'@'+dateTime
fileName = strFwVer+'.txt'
f = open(fileName, 'a+')
time.sleep(1)
f.write(testTitle)

print("\n")
f.write('\n\n')
# Read B0
B0RawDataBuff = ctypes.c_ubyte*256
B0RawReadByte = B0RawDataBuff()
f.write("B0 raw data: \n")
Res = 0xFF
Res = objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[2], 0, 256, B0RawReadByte)
if 0 == Res:
    for item in range(len(B0RawReadByte)):
        print("{}{:0>2X}{}".format("0x", B0RawReadByte[item], ","), end='')
        f.write("{}{:0>2X}{}".format("0x", B0RawReadByte[item], ","))
else:
    f.write('B0 read raw data fail.'+'\n')
del B0RawDataBuff
del B0RawReadByte

print("\n")
f.write('\n\n')
# Read B2
B2RawDataBuff = ctypes.c_ubyte*256
B2RawReadByte = B2RawDataBuff()
f.write("B2 raw data: \n")
Res = 0xFF
Res = objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[3], 0, 256, B2RawReadByte)
if 0 == Res:
    for item in range(len(B2RawReadByte)):
        f.write("{}{:0>2X}{}".format("0x", B2RawReadByte[item], ","))
else:
    f.write('read raw data fail.'+'\n')
del B2RawDataBuff
del B2RawReadByte

print("\n")
f.write('\n\n')
# Read A0
A0RawDataBuff = ctypes.c_ubyte*256
A0RawReadByte = A0RawDataBuff()
f.write("A0 raw data: \n")
Res = 0xFF
Res = objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[0], 0, 256, A0RawReadByte)
if 0 == Res:
    for item in range(len(A0RawReadByte)):
        f.write("{}{:0>2X}{}".format("0x", A0RawReadByte[item], ","))
else:
    f.write('read raw data fail.'+'\n')
del A0RawDataBuff
del A0RawReadByte

print("\n")
f.write('\n\n')
# Read A2
A2RawDataBuff = ctypes.c_ubyte*256
A2RawReadByte = A2RawDataBuff()
f.write("A2 raw data: \n")
Res = 0xFF
Res = objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 0, 256, A2RawReadByte)
if 0 == Res:
    for item in range(len(A2RawReadByte)):
        f.write("{}{:0>2X}{}".format("0x", A2RawReadByte[item], ","))
else:
    f.write('read raw data fail.'+'\n')

mcuCoreTemperature = A2RawReadByte[96]+(A2RawReadByte[97]/256)
print("\nMCU Croe temperature : {:>10f} °C".format(mcuCoreTemperature))
f.write("\n\nMCU Croe temperature : {:>10f} °C".format(mcuCoreTemperature))
f.write("\n\nMCU temperature Index :{}{:>2x}".format("0x", (round(mcuCoreTemperature)+40)))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_ADC(0)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print("ADC 0(Hex):")
    f.write('MCU_GET_ADC 0 :')
    tempCmdOut = strCmdOut[2:4]
    strCmdOut[2:4] = strCmdOut[4:6]
    strCmdOut[4:6] = tempCmdOut
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))
#print("\n{},{},{},{}".format(strCmdOut[2], strCmdOut[3], strCmdOut[4], strCmdOut[5]))
#print("\nADC 0(Dec) : {:>4d}".format((strCmdOut[2]-48)*1000+(strCmdOut[3]-48)*100+(strCmdOut[4]-48)*10+(strCmdOut[5]-65)))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_ADC(1)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print("ADC 1(Hex):")
    f.write('MCU_GET_ADC 1 :')
    tempCmdOut = strCmdOut[2:4]
    strCmdOut[2:4] = strCmdOut[4:6]
    strCmdOut[4:6] = tempCmdOut
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_ADC(2)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print("ADC 2(Hex):")
    f.write('MCU_GET_ADC 2 :')
    tempCmdOut = strCmdOut[2:4]
    strCmdOut[2:4] = strCmdOut[4:6]
    strCmdOut[4:6] = tempCmdOut
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_ADC(3)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print("ADC 3(Hex):")
    f.write('MCU_GET_ADC 3 :')
    tempCmdOut = strCmdOut[2:4]
    strCmdOut[2:4] = strCmdOut[4:6]
    strCmdOut[4:6] = tempCmdOut
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_ADC(4)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print("ADC 4(Hex):")
    f.write('MCU_GET_ADC 4 :')
    tempCmdOut = strCmdOut[2:4]
    strCmdOut[2:4] = strCmdOut[4:6]
    strCmdOut[4:6] = tempCmdOut
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_ADC(5)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print("ADC 5(Hex):")
    f.write('MCU_GET_ADC 5 :')
    tempCmdOut = strCmdOut[2:4]
    strCmdOut[2:4] = strCmdOut[4:6]
    strCmdOut[4:6] = tempCmdOut
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_ADC(6)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print("ADC 6(Hex):")
    f.write('MCU_GET_ADC 6 :')
    tempCmdOut = strCmdOut[2:4]
    strCmdOut[2:4] = strCmdOut[4:6]
    strCmdOut[4:6] = tempCmdOut
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_ADC(7)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print("ADC 7(Hex):")
    f.write('MCU_GET_ADC 7 :')
    tempCmdOut = strCmdOut[2:4]
    strCmdOut[2:4] = strCmdOut[4:6]
    strCmdOut[4:6] = tempCmdOut
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_ADC(8)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print("ADC 8(Hex):")
    f.write('MCU_GET_ADC 8 :')
    tempCmdOut = strCmdOut[2:4]
    strCmdOut[2:4] = strCmdOut[4:6]
    strCmdOut[4:6] = tempCmdOut
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_ADC(9)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print("ADC 9(Hex):")
    f.write('MCU_GET_ADC 9 :')
    tempCmdOut = strCmdOut[2:4]
    strCmdOut[2:4] = strCmdOut[4:6]
    strCmdOut[4:6] = tempCmdOut
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_ADC(10)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print("ADC 10(Hex):")
    f.write('MCU_GET_ADC 10 :')
    tempCmdOut = strCmdOut[2:4]
    strCmdOut[2:4] = strCmdOut[4:6]
    strCmdOut[4:6] = tempCmdOut
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_ADC(11)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print("ADC 11(Hex):")
    f.write('MCU_GET_ADC 11 :')
    tempCmdOut = strCmdOut[2:4]
    strCmdOut[2:4] = strCmdOut[4:6]
    strCmdOut[4:6] = tempCmdOut
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_ADC(12)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print("ADC 12(Hex):")
    f.write('MCU_GET_ADC 12 :')
    tempCmdOut = strCmdOut[2:4]
    strCmdOut[2:4] = strCmdOut[4:6]
    strCmdOut[4:6] = tempCmdOut
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_ADC(13)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print("ADC 13(Hex):")
    f.write('MCU_GET_ADC 13 :')
    tempCmdOut = strCmdOut[2:4]
    strCmdOut[2:4] = strCmdOut[4:6]
    strCmdOut[4:6] = tempCmdOut
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_ADC(14)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print("ADC 14(Hex):")
    f.write('MCU_GET_ADC 14 :')
    tempCmdOut = strCmdOut[2:4]
    strCmdOut[2:4] = strCmdOut[4:6]
    strCmdOut[4:6] = tempCmdOut
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_PWM(0)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print("PWM 0(Hex):")
    f.write('MCU_GET_PWM 0 :')
    tempCmdOut = strCmdOut[2:4]
    strCmdOut[2:4] = strCmdOut[4:6]
    strCmdOut[4:6] = tempCmdOut
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("MCU_GET_PWM(0) fail: {0:d}".format(retStauts))
    f.write("MCU_GET_PWM(0) fail: {}".format(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_PWM(1)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print("PWM 1(Hex):")
    f.write('MCU_GET_PWM 1 :')
    tempCmdOut = strCmdOut[2:4]
    strCmdOut[2:4] = strCmdOut[4:6]
    strCmdOut[4:6] = tempCmdOut
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("MCU_GET_PWM(1) fail: {0:d}".format(retStauts))
    #f.write(str(retStauts))
    f.write("MCU_GET_PWM(0) fail: {}".format(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_ADJUST(0)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_GET_ADJUST 0 :')
    tempCmdOut = strCmdOut[9:11]
    strCmdOut[9:11] = strCmdOut[11:13]
    strCmdOut[11:13] = tempCmdOut
    tempCmdOut = strCmdOut[16:18]
    strCmdOut[16:18] = strCmdOut[18:20]
    strCmdOut[18:20] = tempCmdOut
    tempCmdOut = strCmdOut[23:25]
    strCmdOut[23:25] = strCmdOut[25:27]
    strCmdOut[25:27] = tempCmdOut
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_ADJUST(1)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_GET_ADJUST 1 :')
    tempCmdOut = strCmdOut[9:11]
    strCmdOut[9:11] = strCmdOut[11:13]
    strCmdOut[11:13] = tempCmdOut
    tempCmdOut = strCmdOut[16:18]
    strCmdOut[16:18] = strCmdOut[18:20]
    strCmdOut[18:20] = tempCmdOut
    tempCmdOut = strCmdOut[23:25]
    strCmdOut[23:25] = strCmdOut[25:27]
    strCmdOut[25:27] = tempCmdOut
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_ADJUST(2)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_GET_ADJUST 2 :')
    tempCmdOut = strCmdOut[9:11]
    strCmdOut[9:11] = strCmdOut[11:13]
    strCmdOut[11:13] = tempCmdOut
    tempCmdOut = strCmdOut[16:18]
    strCmdOut[16:18] = strCmdOut[18:20]
    strCmdOut[18:20] = tempCmdOut
    tempCmdOut = strCmdOut[23:25]
    strCmdOut[23:25] = strCmdOut[25:27]
    strCmdOut[25:27] = tempCmdOut
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_ADJUST(3)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_GET_ADJUST 3 :')
    tempCmdOut = strCmdOut[9:11]
    strCmdOut[9:11] = strCmdOut[11:13]
    strCmdOut[11:13] = tempCmdOut
    tempCmdOut = strCmdOut[16:18]
    strCmdOut[16:18] = strCmdOut[18:20]
    strCmdOut[18:20] = tempCmdOut
    tempCmdOut = strCmdOut[23:25]
    strCmdOut[23:25] = strCmdOut[25:27]
    strCmdOut[25:27] = tempCmdOut
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_ADJUST(4)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_GET_ADJUST 4 :')
    tempCmdOut = strCmdOut[9:11]
    strCmdOut[9:11] = strCmdOut[11:13]
    strCmdOut[11:13] = tempCmdOut
    tempCmdOut = strCmdOut[16:18]
    strCmdOut[16:18] = strCmdOut[18:20]
    strCmdOut[18:20] = tempCmdOut
    tempCmdOut = strCmdOut[23:25]
    strCmdOut[23:25] = strCmdOut[25:27]
    strCmdOut[25:27] = tempCmdOut
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_ADJUST(5)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_GET_ADJUST 5 :')
    tempCmdOut = strCmdOut[9:11]
    strCmdOut[9:11] = strCmdOut[11:13]
    strCmdOut[11:13] = tempCmdOut
    tempCmdOut = strCmdOut[16:18]
    strCmdOut[16:18] = strCmdOut[18:20]
    strCmdOut[18:20] = tempCmdOut
    tempCmdOut = strCmdOut[23:25]
    strCmdOut[23:25] = strCmdOut[25:27]
    strCmdOut[25:27] = tempCmdOut
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_ADJUST(6)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_GET_ADJUST 6 :')
    tempCmdOut = strCmdOut[9:11]
    strCmdOut[9:11] = strCmdOut[11:13]
    strCmdOut[11:13] = tempCmdOut
    tempCmdOut = strCmdOut[16:18]
    strCmdOut[16:18] = strCmdOut[18:20]
    strCmdOut[18:20] = tempCmdOut
    tempCmdOut = strCmdOut[23:25]
    strCmdOut[23:25] = strCmdOut[25:27]
    strCmdOut[25:27] = tempCmdOut
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_ADJUST(7)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_GET_ADJUST 7 :')
    tempCmdOut = strCmdOut[9:11]
    strCmdOut[9:11] = strCmdOut[11:13]
    strCmdOut[11:13] = tempCmdOut
    tempCmdOut = strCmdOut[16:18]
    strCmdOut[16:18] = strCmdOut[18:20]
    strCmdOut[18:20] = tempCmdOut
    tempCmdOut = strCmdOut[23:25]
    strCmdOut[23:25] = strCmdOut[25:27]
    strCmdOut[25:27] = tempCmdOut
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_ADJUST(8)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_GET_ADJUST 8 :')
    tempCmdOut = strCmdOut[9:11]
    strCmdOut[9:11] = strCmdOut[11:13]
    strCmdOut[11:13] = tempCmdOut
    tempCmdOut = strCmdOut[16:18]
    strCmdOut[16:18] = strCmdOut[18:20]
    strCmdOut[18:20] = tempCmdOut
    tempCmdOut = strCmdOut[23:25]
    strCmdOut[23:25] = strCmdOut[25:27]
    strCmdOut[25:27] = tempCmdOut
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_ADJUST(9)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_GET_ADJUST 9 :')
    tempCmdOut = strCmdOut[9:11]
    strCmdOut[9:11] = strCmdOut[11:13]
    strCmdOut[11:13] = tempCmdOut
    tempCmdOut = strCmdOut[16:18]
    strCmdOut[16:18] = strCmdOut[18:20]
    strCmdOut[18:20] = tempCmdOut
    tempCmdOut = strCmdOut[23:25]
    strCmdOut[23:25] = strCmdOut[25:27]
    strCmdOut[25:27] = tempCmdOut
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_ADJUST(10)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_GET_ADJUST 10 :')
    tempCmdOut = strCmdOut[9:11]
    strCmdOut[9:11] = strCmdOut[11:13]
    strCmdOut[11:13] = tempCmdOut
    tempCmdOut = strCmdOut[16:18]
    strCmdOut[16:18] = strCmdOut[18:20]
    strCmdOut[18:20] = tempCmdOut
    tempCmdOut = strCmdOut[23:25]
    strCmdOut[23:25] = strCmdOut[25:27]
    strCmdOut[25:27] = tempCmdOut
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_DAC(0)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_GET_DAC 0 :')
    tempCmdOut = strCmdOut[2:4]
    strCmdOut[2:4] = strCmdOut[4:6]
    strCmdOut[4:6] = tempCmdOut
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_DAC(1)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_GET_DAC 1 :')
    tempCmdOut = strCmdOut[2:4]
    strCmdOut[2:4] = strCmdOut[4:6]
    strCmdOut[4:6] = tempCmdOut
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_DAC(2)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_GET_DAC 2 :')
    tempCmdOut = strCmdOut[2:4]
    strCmdOut[2:4] = strCmdOut[4:6]
    strCmdOut[4:6] = tempCmdOut
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_DAC(3)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_GET_DAC 3 :')
    tempCmdOut = strCmdOut[2:4]
    strCmdOut[2:4] = strCmdOut[4:6]
    strCmdOut[4:6] = tempCmdOut
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

#########################################################
#               ADJUST SET DAC0 (EA)
#########################################################
print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(0,M,0,0x0005,0,0)') #little endian
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
    f.write('MCU_SET_ADJUST(0,M,0,0x0500,0,0) ,')
    strCmdIn = create_string_buffer(b'MCU_GET_DAC(0)')
    retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 0 == retStauts:
        f.write('MCU_GET_DAC 0 :')
        tempCmdOut = strCmdOut[2:4]
        strCmdOut[2:4] = strCmdOut[4:6]
        strCmdOut[4:6] = tempCmdOut
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
    else:
        print("\nMCU_GET_DAC 0 fail : {0:d}".format(retStauts))
        f.write("\nMCU_GET_DAC 0 fail : {0:d}".format(str(retStauts)))
else:
    print("MCU_SET_ADJUST(0,M,0,0x0005,0,0) fail :{0:d}".format(retStauts))
    f.write("MCU_SET_ADJUST(0,M,0,0x0005,0,0) fail ：{0:d}".format(retStauts))
#########################################################
#               COMMAND SET DAC0 (EA)
#########################################################
print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(0,I,0,0x0005,0,0)') #little endian
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
strCmdIn = create_string_buffer(b'MCU_SET_DAC(0, 0x000A)') #little endian
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
    f.write('MCU_SET_DAC(0, 0xA00) ,')
    strCmdIn = create_string_buffer(b'MCU_GET_DAC(0)')
    retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 0 == retStauts:
        f.write('MCU_GET_DAC 0 :')
        tempCmdOut = strCmdOut[2:4]
        strCmdOut[2:4] = strCmdOut[4:6]
        strCmdOut[4:6] = tempCmdOut
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
    else:
        print("\nMCU_GET_DAC 0 fail : {0:d}".format(retStauts))
        f.write("\nMCU_GET_DAC 0 fail : {0:d}".format(str(retStauts)))
else:
    print("\nMCU_SET_DAC(0, 0xA00) fail :{0:d}".format(retStauts))
    f.write("\nMCU_SET_DAC(0, 0xA00) fail :{0:d}".format(retStauts))
########################################################
#               ADJUST SET DAC1 (TEC)
#########################################################
print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(1,M,0,0x3408,0xAC0D,0x4006)') #little endian
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
    f.write('MCU_SET_ADJUST(1,M,0,0x834,0xDAC,0x640) ,')
    strCmdIn = create_string_buffer(b'MCU_GET_DAC(1)')
    retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 0 == retStauts:
        f.write('MCU_GET_DAC 1 :')
        tempCmdOut = strCmdOut[2:4]
        strCmdOut[2:4] = strCmdOut[4:6]
        strCmdOut[4:6] = tempCmdOut
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
    else:
        print("\nMCU_GET_DAC 1 fail : {0:d}".format(retStauts))
        f.write("\nMCU_GET_DAC 1 fail : {0:d}".format(str(retStauts)))
else:
    print("MCU_SET_ADJUST(1,M,0,0x3408,0xAC0D,0x4006) fail :{0:d}".format(retStauts))
    f.write("MCU_SET_ADJUST(1,M,0,0x3408,0xAC0D,0x4006) fail ：{0:d}".format(retStauts))

#########################################################
#               COMMAND SET DAC1 (TEC)
#########################################################
print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(1,I,0,0xD217,0xAC0D,0x4006)') #little endian
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
strCmdIn = create_string_buffer(b'MCU_SET_DAC(1,0x000A)') #little endian
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
    f.write('MCU_SET_DAC(1, 0xA00) ,')
    strCmdIn = create_string_buffer(b'MCU_GET_DAC(1)')
    retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 0 == retStauts:
        f.write('MCU_GET_DAC 1 :')
        tempCmdOut = strCmdOut[2:4]
        strCmdOut[2:4] = strCmdOut[4:6]
        strCmdOut[4:6] = tempCmdOut
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
    else:
        print("\nMCU_GET_DAC 1 fail : {0:d}".format(retStauts))
        f.write("\nMCU_GET_DAC 1 fail : {0:d}".format(retStauts))
else:
    print("\nMCU_SET_DAC(1, 0xA00) fail :{0:d}".format(retStauts))
    f.write("\nMCU_SET_DAC(1, 0xA00) fail :{0:d}".format(retStauts))
#########################################################
#               ADJUST SET DAC2 (XGPON APD)
#########################################################
print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(2,M,0,0x000E,0xFF0F,0x0005)') #little endian
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
    f.write('MCU_SET_ADJUST(2,M,0,0x000E,0xFF0F,0x0005) ,')
    strCmdIn = create_string_buffer(b'MCU_GET_DAC(2)')
    retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 0 == retStauts:
        f.write('MCU_GET_DAC 2 :')
        tempCmdOut = strCmdOut[2:4]
        strCmdOut[2:4] = strCmdOut[4:6]
        strCmdOut[4:6] = tempCmdOut
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
    else:
        print("\nMCU_GET_DAC 2 fail : {0:d}".format(retStauts))
        f.write("\nMCU_GET_DAC 2 fail : {0:d}".format(retStauts))
else:
    print("MCU_SET_ADJUST(2,M,0,0x000E,0xFF0F,0x0000) fail :{0:d}".format(retStauts))
    f.write("MCU_SET_ADJUST(2,M,0,0x000E,0xFF0F,0x0000) fail ：{0:d}".format(retStauts))

#########################################################
#               COMMAND SET DAC2 (XGPON APD)
#########################################################
print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(2,I,0,0xFF0F,0xFF0F,0x0005)') #little endian
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
strCmdIn = create_string_buffer(b'MCU_SET_DAC(2, 0x000E)') #little endian
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
    f.write('MCU_SET_DAC(2, 0xE00) ,')
    strCmdIn = create_string_buffer(b'MCU_GET_DAC(2)')
    retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 0 == retStauts:
        f.write('MCU_GET_DAC 2 :')
        tempCmdOut = strCmdOut[2:4]
        strCmdOut[2:4] = strCmdOut[4:6]
        strCmdOut[4:6] = tempCmdOut
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
    else:
        print("\nMCU_GET_DAC 2 fail : {0:d}".format(retStauts))
        f.write("\nMCU_GET_DAC 2 fail : {0:d}".format(retStauts))
else:
    print("\nMCU_SET_DAC(2, 0xE00) fail :{0:d}".format(retStauts))
    f.write("\nMCU_SET_DAC(2, 0xE00) fail :{0:d}".format(retStauts))
#########################################################
#               ADJUST SET DAC3 (GPON APD)
#########################################################
print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(3,M,0,0x000E,0xFF0F,0x0005)') #little endian
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
    f.write('MCU_SET_ADJUST(3,M,0,0x834,0xDAC,0x640) ,')
    strCmdIn = create_string_buffer(b'MCU_GET_DAC(3)')
    retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 0 == retStauts:
        f.write('MCU_GET_DAC 3 :')
        tempCmdOut = strCmdOut[2:4]
        strCmdOut[2:4] = strCmdOut[4:6]
        strCmdOut[4:6] = tempCmdOut
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
    else:
        print("\nMCU_GET_DAC 3 fail : {0:d}".format(retStauts))
        f.write("\nMCU_GET_DAC 3 fail : {0:d}".format(retStauts))
else:
    print("MCU_SET_ADJUST(3,M,0,0x000E,0xFF0F,0x0000) fail :{0:d}".format(retStauts))
    f.write("MCU_SET_ADJUST(3,M,0,0x000E,0xFF0F,0x0000) fail ：{0:d}".format(retStauts))

#########################################################
#               COMMAND SET DAC3 (GPON APD)
#########################################################
print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(3,I,0,0xFF0F,0xFF0F,0x0005)') #little endian
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
strCmdIn = create_string_buffer(b'MCU_SET_DAC(3, 0x000E)') #little endian
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
    f.write('MCU_SET_DAC(3, 0xE00) ,')
    strCmdIn = create_string_buffer(b'MCU_GET_DAC(3)')
    retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 0 == retStauts:
        f.write('MCU_GET_DAC 3 :')
        tempCmdOut = strCmdOut[2:4]
        strCmdOut[2:4] = strCmdOut[4:6]
        strCmdOut[4:6] = tempCmdOut
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
    else:
        print("\nMCU_GET_DAC 3 fail : {0:d}".format(retStauts))
        f.write("\nMCU_GET_DAC 3 fail : {0:d}".format(retStauts))
else:
    print("\nMCU_SET_DAC(3, 0xE00) fail :{0:d}".format(retStauts))
    f.write("\nMCU_SET_DAC(3, 0xE00) fail :{0:d}".format(retStauts))
#########################################################
#               ADJUST SET PWM0
#########################################################
print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(4,M,0,0xAB06,0,0)') #little endian
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
    f.write('MCU_SET_ADJUST(4,M,0,0x06AB,0,0) ,')
    strCmdIn = create_string_buffer(b'MCU_GET_PWM(0)')
    retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 0 == retStauts:
        f.write('MCU_GET_PWM 0 :')
        tempCmdOut = strCmdOut[2:4]
        strCmdOut[2:4] = strCmdOut[4:6]
        strCmdOut[4:6] = tempCmdOut
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
    else:
        print("\nMCU_GET_PWM 0 fail : {0:d}".format(retStauts))
        f.write("\nMCU_GET_PWM 0 fail : {0:d}".format(retStauts))
else:
    print("MCU_SET_ADJUST(4,M,0,0xAB06,0,0) fail :{0:d}".format(retStauts))
    f.write("MCU_SET_ADJUST(4,M,0,0xAB06,0,0) fail ：{0:d}".format(retStauts))
#########################################################
#               COMMAND SET PWM0
#########################################################
print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(4,I,0,0x0004,0,0)') #little endian
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
strCmdIn = create_string_buffer(b'MCU_SET_PWM(0,0x8802)') #little endian
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
    f.write('MCU_SET_PWM(0, 0x288) ,')
    strCmdIn = create_string_buffer(b'MCU_GET_PWM(0)')
    retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 0 == retStauts:
        f.write('MCU_GET_PWM 0 :')
        tempCmdOut = strCmdOut[2:4]
        strCmdOut[2:4] = strCmdOut[4:6]
        strCmdOut[4:6] = tempCmdOut
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
    else:
        print("\nMCU_GET_PWM 0 fail : {0:d}".format(retStauts))
        f.write("\nMCU_GET_PWM 0 fail : {0:d}".format(retStauts))
else:
    print("\nMCU_SET_PWM(0, 0x288) fail :{}".format(chr(strCmdOut[0]) + chr(strCmdOut[1])))
    f.write("\nMCU_SET_PWM(0, 0x288) fail :{}".format(chr(strCmdOut[0]) + chr(strCmdOut[1])))

#########################################################
#               ADJUST SET PWM1
#########################################################
print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(5,M,0,0xAB05,0,0)') #little endian
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
    f.write('MCU_SET_ADJUST(5,M,0,0x05AB,0,0) ,')
    strCmdIn = create_string_buffer(b'MCU_GET_PWM(1)')
    retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 0 == retStauts:
        f.write('MCU_GET_PWM 1 :')
        tempCmdOut = strCmdOut[2:4]
        strCmdOut[2:4] = strCmdOut[4:6]
        strCmdOut[4:6] = tempCmdOut
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
    else:
        print("\nMCU_GET_PWM 1 fail : {0:d}".format(retStauts))
        f.write("\nMCU_GET_PWM 1 fail : {0:d}".format(retStauts))
else:
    print("MCU_SET_ADJUST(5,M,0,0xAB05,0,0) fail :{0:d}".format(retStauts))
    f.write("MCU_SET_ADJUST(5,M,0,0xAB05,0,0) fail ：{0:d}".format(retStauts))
#########################################################
#               COMMAND SET PWM1
#########################################################
print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(5,I,0,0x0004,0,0)') #little endian
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
strCmdIn = create_string_buffer(b'MCU_SET_PWM(1,0x8801)') #little endian
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
    f.write('MCU_SET_PWM(0, 0x188) ,')
    strCmdIn = create_string_buffer(b'MCU_GET_PWM(1)')
    retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 0 == retStauts:
        f.write('MCU_GET_PWM 1 :')
        tempCmdOut = strCmdOut[2:4]
        strCmdOut[2:4] = strCmdOut[4:6]
        strCmdOut[4:6] = tempCmdOut
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
    else:
        print("\nMCU_GET_PWM 1 fail : {0:d}".format(retStauts))
        f.write("\nMCU_GET_PWM 1 fail : {0:d}".format(retStauts))
else:
    print("\nMCU_SET_PWM(1, 0x188) fail :{}".format(chr(strCmdOut[0]) + chr(strCmdOut[1])))
    f.write("\nMCU_SET_PWM(1, 0x188) fail :{}".format(chr(strCmdOut[0]) + chr(strCmdOut[1])))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_TABLE(base,0,0,128)')
strCmdOutBuff = ctypes.c_ubyte*640
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_GET_TABLE base 0 :')
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_TABLE(base,1,0,128)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_GET_TABLE base 1 :')
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_TABLE(base,2,0,128)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_GET_TABLE base 2 :')
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))


print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_TABLE(base,3,0,128)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_GET_TABLE base 3 :')
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_TABLE(driver,1,0,128)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_GET_TABLE driver 1 :')
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\nGet Driver 1 register initial Value:\n")
f.write('\n\nGet Driver register initial Value:\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0x90,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_I2C_READ 0xA2 0x90 8 :')
    for item in range(40):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0x98,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_I2C_READ 0xA2 0x98 8 :')
    for item in range(40):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0xA0,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_I2C_READ 0xA2 0xA0 8 :')
    for item in range(40):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0xA8,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_I2C_READ 0xA2 0xA8 8 :')
    for item in range(40):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0xB0,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_I2C_READ 0xA2 0xB0 8 :')
    for item in range(40):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0xB8,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_I2C_READ 0xA2 0xB8 8 :')
    for item in range(40):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0xC0,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_I2C_READ 0xA2 0xC0 8 :')
    for item in range(40):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0xD6,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_I2C_READ 0xA2 0xD6 8 :')
    for item in range(40):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0xDE,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_I2C_READ 0xA2 0xDE 8 :')
    for item in range(40):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0xE0,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_I2C_READ 0xA2 0xE0 8 :')
    for item in range(40):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_TABLE(driver,0,0,128)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_GET_TABLE driver 0 :')
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
print("\nGet Driver 0 register initial Value:\n")
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0x10,0x00,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_I2C_READ 0x10 0x00 8 :')
    for item in range(40):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
print("\nGet Driver 0 register initial Value:\n")
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0x10,0x0A,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_I2C_READ 0x10 0x0A 8 :')
    for item in range(40):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
print("\nGet Driver 0 register initial Value:\n")
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0x10,0x12,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_I2C_READ 0x10 0x12 8 :')
    for item in range(40):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
print("\nGet Driver 0 register initial Value:\n")
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0x10,0x33,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_I2C_READ 0x10 0x33 1 :')
    for item in range(40):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_TABLE(lut,0,0,128)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_GET_TABLE lut 0 :')
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_TABLE(lut,1,0,128)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_GET_TABLE lut 1 :')
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_TABLE(lut,2,0,128)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_GET_TABLE lut 2 :')
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_TABLE(lut,3,0,128)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_GET_TABLE lut 3 :')
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_TABLE(lut,4,0,128)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_GET_TABLE lut 4 :')
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_TABLE(lut,6,0,128)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_GET_TABLE lut 6 :')
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_TABLE(lut,7,0,128)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_GET_TABLE lut 7 :')
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_TABLE(lut,8,0,128)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_GET_TABLE lut 8 :')
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_TABLE(lut,9,0,128)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_GET_TABLE lut 9 :')
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_TABLE(lut,10,0,128)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_GET_TABLE lut 10 :')
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_TABLE(lut,11,0,96)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_GET_TABLE lut 11 :')
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))
#########################################################
#               Verify GN25L96 APC
#########################################################
print("\nGN25L96 APC auto mode, 25L96 A4 adjust to '0x58'")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_SET_TABLE(LUT,2,0,0x4B,0x00,0x00,0x00,0x58,0xFF,0x00,0x00,0x00,0x58)')
f.write(repr(strCmdIn.value)+'\n')
strCmdOutBuff = ctypes.c_ubyte*8
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0])+chr(strCmdOut[1]):
    # TODO: first read back,then hold target,max,miin
    strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(6, A, 0, 0, 0, 0)')
    f.write(repr(strCmdIn.value)+'\n')
    time.sleep(1)
    strCmdOutBuff = ctypes.c_ubyte * 8
    strCmdOut = strCmdOutBuff()
    cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
        strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0xA4,1)')
        f.write(repr(strCmdIn.value)+'\n')
        strCmdOutBuff = ctypes.c_ubyte * 8
        strCmdOut = strCmdOutBuff()
        cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))

print("\nGN25L96 APC auto mode, 25L96 A4 adjust to '0x88'")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_SET_TABLE(LUT,2,0,0x4B,0x00,0x00,0x00,0x88,0xFF,0x00,0x00,0x00,0x88)')
f.write(repr(strCmdIn.value)+'\n')
strCmdOutBuff = ctypes.c_ubyte*8
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0])+chr(strCmdOut[1]):
    # TODO: first read back,then hold target,max,miin
    strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(6, A, 0, 0, 0, 0)')
    f.write(repr(strCmdIn.value)+'\n')
    time.sleep(1)
    strCmdOutBuff = ctypes.c_ubyte * 8
    strCmdOut = strCmdOutBuff()
    cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
        strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0xA4,1)')
        f.write(repr(strCmdIn.value)+'\n')
        strCmdOutBuff = ctypes.c_ubyte * 8
        strCmdOut = strCmdOutBuff()
        cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
#########################################################
#               Verify GN25L96 Mod Max
#########################################################
print("\nGN25L96 Mod Max auto mode, 25L96 A7 adjust to '0x38'")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_SET_TABLE(LUT,11,0,0x4B,0x00,0x00,0x00,0x38,0xFF,0x00,0x00,0x00,0x38)')
f.write(repr(strCmdIn.value)+'\n')
strCmdOutBuff = ctypes.c_ubyte*8
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0])+chr(strCmdOut[1]):
    # TODO: first read back,then hold target,max,miin
    strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(10, A, 0, 0, 0, 0)')
    f.write(repr(strCmdIn.value)+'\n')
    time.sleep(1)
    strCmdOutBuff = ctypes.c_ubyte * 8
    strCmdOut = strCmdOutBuff()
    cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
        strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0xA7,1)')
        f.write(repr(strCmdIn.value)+'\n')
        strCmdOutBuff = ctypes.c_ubyte * 8
        strCmdOut = strCmdOutBuff()
        cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))

print("\nGN25L96 Mod Max auto mode, 25L96 A7 adjust to '0x98'")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_SET_TABLE(LUT,11,0,0x4B,0x00,0x00,0x00,0x98,0xFF,0x00,0x00,0x00,0x98)')
f.write(repr(strCmdIn.value)+'\n')
strCmdOutBuff = ctypes.c_ubyte*8
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0])+chr(strCmdOut[1]):
    # TODO: first read back,then hold target,max,miin
    strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(10, A, 0, 0, 0, 0)')
    f.write(repr(strCmdIn.value)+'\n')
    time.sleep(1)
    strCmdOutBuff = ctypes.c_ubyte * 8
    strCmdOut = strCmdOutBuff()
    cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
        strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0xA7,1)')
        f.write(repr(strCmdIn.value)+'\n')
        strCmdOutBuff = ctypes.c_ubyte * 8
        strCmdOut = strCmdOutBuff()
        cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))

#########################################################
#               Verify ONET1131 BIAS
#########################################################
print("\n1131 BIAS Lut mode, 1131[15~16] adjust to '0x150'")
f.write("\n\n1131 BIAS Lut mode, 1131[15~16] adjust to '0x150' \n")
strCmdIn = create_string_buffer(b'MCU_SET_TABLE(LUT,4,0,0x4B,0x00,0x00,0x01,0x50,0xFF,0x00,0x00,0x01,0x50)')
f.write(str(strCmdIn.value)+'\n')
strCmdOutBuff = ctypes.c_ubyte*8
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0])+chr(strCmdOut[1]):
    # TODO: first read back,then hold target,max,miin
    strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(8, A, 0, 0, 0, 0)')
    f.write(str(strCmdIn.value)+'\n')
    time.sleep(1)
    strCmdOutBuff = ctypes.c_ubyte * 8
    strCmdOut = strCmdOutBuff()
    cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
        strCmdIn = create_string_buffer(b'MCU_I2C_READ(0x10,0x0F,2)')
        f.write(str(strCmdIn.value)+'\n')
        strCmdOutBuff = ctypes.c_ubyte * 8
        strCmdOut = strCmdOutBuff()
        cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))

print("\n1131 BIAS Lut mode, 1131[15~16] adjust to '0x300'")
f.write("\n\n1131 BIAS Lut mode, 1131[15~16] adjust to '0x300' \n")
strCmdIn = create_string_buffer(b'MCU_SET_TABLE(LUT,4,0,0x4B,0x00,0x00,0x03,0x00,0xFF,0x00,0x00,0x03,0x00)')
f.write(repr(strCmdIn.value)+'\n')
strCmdOutBuff = ctypes.c_ubyte*8
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0])+chr(strCmdOut[1]):
    # TODO: first read back,then hold target,max,miin
    strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(8, A, 0, 0, 0, 0)')
    f.write(repr(strCmdIn.value)+'\n')
    time.sleep(1)
    strCmdOutBuff = ctypes.c_ubyte * 8
    strCmdOut = strCmdOutBuff()
    cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
        strCmdIn = create_string_buffer(b'MCU_I2C_READ(0x10,0x0F,2)')
        f.write(repr(strCmdIn.value)+'\n')
        strCmdOutBuff = ctypes.c_ubyte * 8
        strCmdOut = strCmdOutBuff()
        cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
#########################################################
#               Verify ONET1131 MOD
#########################################################
print("\n1131 MOD Lut mode, 1131[12] adjust to '0x30'")
f.write("\n\n1131 MOD Lut mode, 1131[12] adjust to '0x30' \n")
strCmdIn = create_string_buffer(b'MCU_SET_TABLE(LUT,10,0,0x4B,0x00,0x00,0x00,0x30,0xFF,0x00,0x00,0x00,0x30)')
f.write(str(strCmdIn.value)+'\n')
strCmdOutBuff = ctypes.c_ubyte*8
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0])+chr(strCmdOut[1]):
    # TODO: first read back,then hold target,max,miin
    strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(9, A, 0, 0, 0, 0)')
    f.write(str(strCmdIn.value)+'\n')
    time.sleep(1)
    strCmdOutBuff = ctypes.c_ubyte * 8
    strCmdOut = strCmdOutBuff()
    cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
        strCmdIn = create_string_buffer(b'MCU_I2C_READ(0x10,0x0C,1)')
        f.write(str(strCmdIn.value)+'\n')
        strCmdOutBuff = ctypes.c_ubyte * 8
        strCmdOut = strCmdOutBuff()
        cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))

print("\n1131 MOD Lut mode, 1131[12] adjust to '0xA0'")
f.write("\n\n1131 MOD Lut mode, 1131[12] adjust to '0xA0' \n")
strCmdIn = create_string_buffer(b'MCU_SET_TABLE(LUT,10,0,0x4B,0x00,0x00,0x00,0xA0,0xFF,0x00,0x00,0x00,0xA0)')
f.write(repr(strCmdIn.value)+'\n')
strCmdOutBuff = ctypes.c_ubyte*8
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0])+chr(strCmdOut[1]):
    # TODO: first read back,then hold target,max,miin
    strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(9, A, 0, 0, 0, 0)')
    f.write(repr(strCmdIn.value)+'\n')
    time.sleep(1)
    strCmdOutBuff = ctypes.c_ubyte * 8
    strCmdOut = strCmdOutBuff()
    cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
        strCmdIn = create_string_buffer(b'MCU_I2C_READ(0x10,0x0C,1)')
        f.write(repr(strCmdIn.value)+'\n')
        strCmdOutBuff = ctypes.c_ubyte * 8
        strCmdOut = strCmdOutBuff()
        cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
del strCmdIn
del strCmdOutBuff, strCmdOut

f.close()
AteAllPowerOff(devUsbIndex)

#A0 write and read repeated
if True == A0_WRITE_READ_REPEATED_TEST:
    with open('.\A0_Direct_Write_Read_Repeated_Test.py', 'r') as fi:
        exec(fi.read())

#A2 write and read repeated
if True == A2_WRITE_READ_REPEATED_TEST:
    with open('.\A2_Direct_Write_Read_Repeated_Test.py', 'r') as fi:
        exec(fi.read())

#B0 write and read repeated
if True == B0_WRITE_READ_REPEATED_TEST:
    with open('.\B0_Direct_Write_Read_Repeated_Test.py', 'r') as fi:
        exec(fi.read())

#B2 write and read repeated
if True == B2_WRITE_READ_REPEATED_TEST:
    with open('.\B2_Direct_Write_Read_Repeated_Test.py', 'r') as fi:
        exec(fi.read())

#099 encryption rule test
if True == ENCRYPTION_RULE_TEST:
    with open('.\SFP+_099_Encryption_Rule_Test.py', 'r') as fi:
        exec(fi.read())