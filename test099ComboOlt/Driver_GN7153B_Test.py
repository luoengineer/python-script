import ctypes
from ctypes import *
import time
from cmdServ import cmdservdll, devUsbIndex
from cmdServ import Sfp_Factory_Pwd_Entry, AteAllPowerOn, AteAllPowerOff, openUsbDevice
from cmdServ import getAdc0, adc02TempIndex
import sys

#Test times
wr_and_rd_times  = 2
# user type for password
is_088_Module = 0
is_other_Module = 1
user_password_type = is_other_Module

#Product list
ComboSfpI2cAddr = [0xA0,0xA2,0xB0,0xB2,0xA4]
SfpI2cAddr = [0xA0,0xA2,0xA4]
XfpI2dAddr = [0xA0,0xA4]

#driver I2C address
DrvI2cAddr = 0x48

#########################################################
#               Inner Funtion
#########################################################


#########################################################
#               Open USB Device
#########################################################
#TODO: How to config several usb device
openUsbDevice(devUsbIndex)

#########################################################
#               Slot Power On
#########################################################
AteAllPowerOn(devUsbIndex)
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
#dateTime = time.strptime(time.asctime())
dateTime = time.strptime(time.asctime( time.localtime(startTick)))
dateTime = "{:4}-{:02}-{:02} {:02}:{:02}:{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
testTitle = strFwVer
fileName = strFwVer+'.txt'
f = open(fileName, 'a+')
time.sleep(1)
print("\n****************************************************************************")
print("driver GN7153B test, start time : {}".format(dateTime))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\ndriver GN7153B test, start time : {}".format(dateTime))
f.write("\n****************************************************************************")
print("{}".format(testTitle))
f.write('\n'+testTitle)

print("\nGet Driver register initial Value:\n")
f.write('\n\nGet Driver register initial Value:\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0x48,0x02,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_I2C_READ 0x48 0x02 8 :')
    f.write('MCU_I2C_READ 0x48 0x02 8 :')
    for item in range(46):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0x48,0x0B,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_I2C_READ 0x48 0x0B 8 :')
    f.write('MCU_I2C_READ 0x48 0x0B 8 :')
    for item in range(46):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0x48,0x14,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_I2C_READ 0x48 0x14 8 :')
    f.write('MCU_I2C_READ 0x48 0x14 8 :')
    for item in range(46):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0x48,0x33,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_I2C_READ 0x48 0x33 8 :')
    f.write('MCU_I2C_READ 0x48 0x33 8 :')
    for item in range(46):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0x48,0x3E,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_I2C_READ 0x48 0x3E 8 :')
    f.write('MCU_I2C_READ 0x48 0x3E 8 :')
    for item in range(46):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0x48,0x48,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_I2C_READ 0x48 0x48 8 :')
    f.write('MCU_I2C_READ 0x48 0x48 8 :')
    for item in range(46):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0x48,0x50,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_I2C_READ 0x48 0x50 8 :')
    f.write('MCU_I2C_READ 0x48 0x50 8 :')
    for item in range(46):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0x48,0x58,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_I2C_READ 0x48 0x58 8 :')
    f.write('MCU_I2C_READ 0x48 0x58 8 :')
    for item in range(46):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0x48,0x60,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_I2C_READ 0x48 0x60 8 :')
    f.write('MCU_I2C_READ 0x48 0x60 8 :')
    for item in range(46):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0x48,0x6A,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_I2C_READ 0x48 0x6A 8 :')
    f.write('MCU_I2C_READ 0x48 0x6A 8 :')
    for item in range(46):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0x48,0x73,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_I2C_READ 0x48 0x73 8 :')
    f.write('MCU_I2C_READ 0x48 0x73 8 :')
    for item in range(46):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0x48,0x7B,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_I2C_READ 0x48 0x7B 8 :')
    f.write('MCU_I2C_READ 0x48 0x7B 8 :')
    for item in range(46):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0x48,0x84,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_I2C_READ 0x48 0x84 8 :')
    f.write('MCU_I2C_READ 0x48 0x84 8 :')
    for item in range(46):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0x48,0x8C,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_I2C_READ 0x48 0x8C 8 :')
    f.write('MCU_I2C_READ 0x48 0x8C 8 :')
    for item in range(46):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))
#########################################################
#               Verify GN7153B APC
#########################################################
print("\nGN7153B APC auto mode, GN7153B 0x0D-0x0E adjust to '0x58,0x04'")
f.write("\n\nGN7153B APC auto mode, GN7153B 0x0D-0x0E adjust to '0x58,0x04'\n")
strCmdIn = create_string_buffer(b'MCU_SET_TABLE(LUT,4,0,0x4B,0x00,0x00,0x00,0x58,0xFF,0x00,0x00,0x00,0x58)')
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
        strCmdIn = create_string_buffer(b'MCU_I2C_READ(0x48,0x0D,2)')
        print(repr(strCmdIn.value)+'\n')
        f.write(repr(strCmdIn.value)+'\n')
        strCmdOutBuff = ctypes.c_ubyte * 16
        strCmdOut = strCmdOutBuff()
        cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
print("\n")
f.write('\n\n')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
strCmdOut = getAdc0()
if 0 != strCmdOut:
    print("ADC 0(Hex):")
    f.write('MCU_GET_ADC 0 :')
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("Can't get ADC 0 ")
    f.write("Can't get ADC 0 ")

tempIndex = adc02TempIndex(strCmdOut)
print("\ntempIndex : {}".format(tempIndex))

if tempIndex < 0x4B:
    APCSet = int(tempIndex*int('0x251',16)/128+int('0x5F',16)) + 0x400 # Reg14 bit2 is APC_OVR
else:
    APCSet = int(tempIndex * int('0x1C4', 16) / 128 + int('0x6C', 16)) + 0x400 # Reg14 bit2 is APC_OVR
print("\nGN7153B APC auto mode,now tempIndex is {}, GN7153B 0x0D-0x0E should adjust to '0x{:02X},0x{:02X}'".format( \
    tempIndex, APCSet & 0xFF, (APCSet) >> 8))
f.write("\nGN7153B APC auto mode,now tempIndex is {}, GN7153B 0x0D-0x0E should adjust to '0x{:02X},0x{:02X}'".format( \
    tempIndex, APCSet & 0xFF, (APCSet) >> 8))

print("\n")
f.write('\n')
strCmdIn = create_string_buffer(b'MCU_SET_TABLE(LUT,4,0,0x4B,0x02,0x51,0x00,0x5F,0xFF,0x01,0xC4,0x00,0x6C)')
f.write(repr(strCmdIn.value)+'\n')
strCmdOutBuff = ctypes.c_ubyte*8
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0])+chr(strCmdOut[1]):
    # TODO: first read back,then hold target,max,miin
    strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(8, A, 0, 0, 0, 0)')
    print(repr(strCmdIn.value)+'\n')
    f.write(repr(strCmdIn.value)+'\n')
    time.sleep(1)
    strCmdOutBuff = ctypes.c_ubyte * 8
    strCmdOut = strCmdOutBuff()
    cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
        strCmdIn = create_string_buffer(b'MCU_I2C_READ(0x48,0x0D,2)')
        f.write(repr(strCmdIn.value)+'\n')
        strCmdOutBuff = ctypes.c_ubyte * 16
        strCmdOut = strCmdOutBuff()
        cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
########################################################
#               Verify GN7153B MOD
#########################################################
print("\nGN7153B MOD auto mode, GN7153B 0x59-0x5A adjust to '0x1F'")
f.write("\n\nGN7153B MOD auto mode, GN7153B 0x59-0x5A adjust to '0x1F'\n")
strCmdIn = create_string_buffer(b'MCU_SET_TABLE(LUT,10,0,0x4B,0x00,0x00,0x00,0x1F,0xFF,0x00,0x00,0x00,0x1F)')
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
        strCmdIn = create_string_buffer(b'MCU_I2C_READ(0x48,0x59,2)')
        f.write(repr(strCmdIn.value)+'\n')
        strCmdOutBuff = ctypes.c_ubyte * 16
        strCmdOut = strCmdOutBuff()
        cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))

print("\n")
f.write('\n\n')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
strCmdOut = getAdc0()
if 0 != strCmdOut:
    print("ADC 0(Hex):")
    f.write('MCU_GET_ADC 0 :')
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("Can't get ADC 0 ")
    f.write("Can't get ADC 0 ")

tempIndex = adc02TempIndex(strCmdOut)
print("\ntempIndex : {}".format(tempIndex))

if tempIndex < 0x4B:
    ModSet = int(tempIndex*int('0x350',16)/128+int('0x12',16))
    #print("{}".format(ModSet))
else:
    ModSet = int(tempIndex * int('0x400', 16) / 128 + int('0x15', 16))
print("\nGN7153B MOD auto mode,now tempIndex is {}, GN7153B 0x59-0x5A should adjust to '0x{:02X},0x{:02X}'".format( \
    tempIndex, ModSet & 0xFF, (ModSet & 0x300) >> 8))
f.write("\nGN7153B MOD auto mode,now tempIndex is {}, GN7153B 0x59-0x5A should adjust to '0x{:02X},0x{:02X}'".format( \
            tempIndex, ModSet & 0xFF, (ModSet & 0x300) >> 8))
strCmdIn = create_string_buffer(b'MCU_SET_TABLE(LUT,10,0,0x4B,0x03,0x50,0x00,0x12,0xFF,0x04,0x00,0x00,0x15)')
f.write('\n'+repr(strCmdIn.value)+'\n')
strCmdOutBuff = ctypes.c_ubyte*8
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0])+chr(strCmdOut[1]):
    # TODO: first read back,then hold target,max,miin
    strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(9, A, 0, 0, 0, 0)')
    f.write(repr(strCmdIn.value)+'\n')
    time.sleep(1)
    strCmdOutBuff = ctypes.c_ubyte * 16
    strCmdOut = strCmdOutBuff()
    cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
        strCmdIn = create_string_buffer(b'MCU_I2C_READ(0x48,0x59,2)')
        f.write(repr(strCmdIn.value)+'\n')
        strCmdOutBuff = ctypes.c_ubyte * 16
        strCmdOut = strCmdOutBuff()
        cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))

########################################################
#         Verify GN7153B Register writing
#########################################################
print("\nRead GN7153B regsiter 98")
f.write("\nRead GN7153B regsiter 98")
#read register raw value
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0x48,98,1)')
strCmdOutBuff = ctypes.c_ubyte*8
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
rawRegVal = [chr(strCmdOut[item]) for item in range(len(strCmdOut)) if 0 != strCmdOut[item]]
rawRegVal = ''.join(rawRegVal)
print(rawRegVal)
#modify register value
print("\nModify GN7153B register 98 to 0x0B")
f.write("\nModify GN7153B register 98 to 0x0B")
strCmdIn = create_string_buffer(b'MCU_I2C_WRITE(0x48,98,0x0B)')
strCmdOutBuff = ctypes.c_ubyte*8
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
#save
    print("\nWrite GN7153B register 98 ok, now save GN7153B register 98 to flash...")
    f.write("\nWrite GN7153B register 98 ok , now save GN7153B register 98 to flash...")
    strCmdIn = create_string_buffer(b'DRV_SAVE_REG(0)')
    strCmdOutBuff = ctypes.c_ubyte*8
    strCmdOut = strCmdOutBuff()
    cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
        print("\nSave GN7153B register ok, now power to reboot")
        f.write("\nSave GN7153B register ok, now power to reboot")
        # power off
        time.sleep(2)
        AteAllPowerOff(devUsbIndex)
else:
    print("\nWrite GN7153B register fail...")
    f.write("\nWrite GN7153B register fail...")
    sys.exit()

# power on
AteAllPowerOn(devUsbIndex)
time.sleep(1)
Sfp_Factory_Pwd_Entry(user_password_type)
time.sleep(2)

#read register value is modified
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0x48,98,1)')
strCmdOutBuff = ctypes.c_ubyte*8
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
readRegVal = [chr(strCmdOut[item]) for item in range(len(strCmdOut)) if 0 != strCmdOut[item]]
readRegVal = ''.join(readRegVal)
if '0x0B' == readRegVal:
    print("\nModify GN7153B register 98 ok, now register 98 = {}".format(readRegVal))
    f.write("\nModify GN7153B register 98 ok, now register 98 = {}".format(readRegVal))
else:
    print("\nModify GN7153B register 98 fail")
    f.write("\nModify GN7153B register 98 fail")

#restore raw value
print("\nRestore GN7153B register 98...")
f.write("\nRestore GN7153B register 98...")
rawRegWriteVal = rawRegVal[rawRegVal.index('x')+1:len(rawRegVal)]
strCmdIn = create_string_buffer(b'MCU_I2C_WRITE(0x48,98,0x1F)')
strCmdOutBuff = ctypes.c_ubyte*8
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
#save
    print("\nRestore GN7153B register 98 ok, now save GN7153B register 98 to flash...")
    f.write("\nRestore GN7153B register 98 ok , now save GN7153B register 98 to flash...")
    strCmdIn = create_string_buffer(b'DRV_SAVE_REG(0)')
    strCmdOutBuff = ctypes.c_ubyte*8
    strCmdOut = strCmdOutBuff()
    cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
        print("\nSave GN7153B register ok, now power to reboot")
        f.write("\nSave GN7153B register ok, now power to reboot")
        # power off
        AteAllPowerOff(devUsbIndex)
else:
    print("\nRestore GN7153B register fail...")
    f.write("\nRestore GN7153B register fail...")
    sys.exit()

# power on
AteAllPowerOn(devUsbIndex)
time.sleep(1)
Sfp_Factory_Pwd_Entry(user_password_type)
time.sleep(1)

#read register value is raw
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0x48,98,1)')
strCmdOutBuff = ctypes.c_ubyte*8
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
readRegVal = [chr(strCmdOut[item]) for item in range(len(strCmdOut)) if 0 != strCmdOut[item]]
readRegVal = ''.join(readRegVal)
if rawRegVal == readRegVal:
    print("\nRestore GN7153B register 98 ok")
    f.write("\nRestore GN7153B register 98 ok")
else:
    print(readRegVal)
    print(rawRegVal)
    print("\nRestore GN7153B register 98 fail")
    f.write("\nRestore GN7153B register 98 fail")


dateTime = time.strptime(time.asctime())
dateTime = "{:4}-{:02}-{:02} {:02}:{:02}:{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
print("\n****************************************************************************")
print("driver GN7153B test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\ndriver GN7153B test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
f.write("\n****************************************************************************")
AteAllPowerOff(devUsbIndex)
f.close()

