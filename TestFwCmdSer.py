import ctypes
from ctypes import *
import time


#########################################################
#               EVBoard Configuration
#########################################################
# Config EVBoard usb
devUsbIndex = 0

# Config EVBoard slot
devSffChannel = 1
devSfpChannel = 2

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
fileName = strFwVer+'@'+dateTime+'.txt'
f = open(fileName, 'w+')
time.sleep(1)
f.write(strFwVer)

print("\n")
f.write('\n\n')
# Read A0
A0RawDataBuff = ctypes.c_ubyte*256
A0RawReadByte = A0RawDataBuff()
f.write("A0 raw data: \n")
Res = 0xFF
Res = objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[0], 0, 256, A0RawReadByte)
if 0 == Res:
    for item in range(len(A0RawReadByte)):
        f.write("{}{:0>2X}{}".format("0x", A0RawReadByte[item], ","))
else:
    f.write('read raw data fail.'+'\n')

print("\n")
f.write('\n\n')
# Read A2
A2RawDataBuff = ctypes.c_ubyte*256
A2RawReadByte = A2RawDataBuff()
f.write("A2 raw data: \n")
Res = 0xFF
Res = objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 0, 256, A2RawReadByte)
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

print("\nGet Driver register initial Value:\n")
f.write('\n\nGet Driver register initial Value:\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0x90,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    f.write('MCU_I2C_READ 0xA2 0x90 8 :')
    for item in range(46):
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
    for item in range(46):
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
    for item in range(46):
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
    for item in range(46):
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
    for item in range(46):
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
    for item in range(46):
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
    for item in range(46):
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
    for item in range(46):
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
    for item in range(46):
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
    for item in range(46):
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

#########################################################
#               Verify GN25L96 APC
#########################################################
print("\n  APC auto mode, 25L96 A4 adjust to '0x58' \n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_SET_TABLE(LUT,2,0,0x4B,0x00,0x00,0x00,0x58,0xFF,0x00,0x00,0x00,0x58)')
f.write(repr(strCmdIn.value)+'\n')
strCmdOutBuff = ctypes.c_ubyte*8
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0])+chr(strCmdOut[1]):
    # TODO: first read back,then hold target,max,miin
    strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(4, A, 0, 0, 0, 0)')
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

print("\n  APC auto mode, 25L96 A4 adjust to '0x88' \n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_SET_TABLE(LUT,2,0,0x4B,0x00,0x00,0x00,0x88,0xFF,0x00,0x00,0x00,0x88)')
f.write(repr(strCmdIn.value)+'\n')
strCmdOutBuff = ctypes.c_ubyte*8
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0])+chr(strCmdOut[1]):
    # TODO: first read back,then hold target,max,miin
    strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(4, A, 0, 0, 0, 0)')
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

print("\n  Mod Max auto mode, 25L96 A7 adjust to '0x38' \n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_SET_TABLE(LUT,7,0,0x4B,0x00,0x00,0x00,0x38,0xFF,0x00,0x00,0x00,0x38)')
f.write(repr(strCmdIn.value)+'\n')
strCmdOutBuff = ctypes.c_ubyte*8
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0])+chr(strCmdOut[1]):
    # TODO: first read back,then hold target,max,miin
    strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(2, A, 0, 0, 0, 0)')
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

print("\n  Mod Max auto mode, 25L96 A7 adjust to '0x98' \n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_SET_TABLE(LUT,7,0,0x4B,0x00,0x00,0x00,0x98,0xFF,0x00,0x00,0x00,0x98)')
f.write(repr(strCmdIn.value)+'\n')
strCmdOutBuff = ctypes.c_ubyte*8
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0])+chr(strCmdOut[1]):
    # TODO: first read back,then hold target,max,miin
    strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(2, A, 0, 0, 0, 0)')
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

f.close()
AteAllPowerOff(devUsbIndex)