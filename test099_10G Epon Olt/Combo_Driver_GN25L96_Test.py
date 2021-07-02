import ctypes
from ctypes import *
import time
from cmdServ import cmdservdll, devUsbIndex
from cmdServ import Sfp_Factory_Pwd_Entry, AteAllPowerOn, AteAllPowerOff, openUsbDevice
from cmdServ import getAdc0, adc02TempIndex


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

#########################################################
#               Subroutines
#########################################################


#########################################################
#               Open USB Device
#########################################################
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
    for item in range(len(strCmdOut)):
        if 0x00 != strCmdOut[item]:
            #print("{}".format(chr(strCmdOut[item])), end='')
            strFwVer.append(chr(strCmdOut[item]))
    else:
        print("{0:d}".format(retStauts))

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
print("{}".format(testTitle))
f.write('\n\n'+testTitle)

print("\nGet Driver register initial Value:\n")
f.write('\n\nGet Driver register initial Value:\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0x90,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_I2C_READ 0xA2 0x90 8 :')
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
    print('MCU_I2C_READ 0xA2 0x98 8 :')
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
    print('MCU_I2C_READ 0xA2 0xA0 8 :')
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
    print('MCU_I2C_READ 0xA2 0xA8 8 :')
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
    print('MCU_I2C_READ 0xA2 0xB0 8 :')
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
    print('MCU_I2C_READ 0xA2 0xB8 8 :')
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
    print('MCU_I2C_READ 0xA2 0xC0 8 :')
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
    print('MCU_I2C_READ 0xA2 0xD6 8 :')
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
    print('MCU_I2C_READ 0xA2 0xDE 8 :')
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
    print('MCU_I2C_READ 0xA2 0xE0 8 :')
    f.write('MCU_I2C_READ 0xA2 0xE0 8 :')
    for item in range(46):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

#########################################################
#               Verify GN25L96 APC
#########################################################
print("\nGN25L96 APC auto mode, 25L96 A4 adjust to '0x58'")
f.write("\n\nGN25L96 APC auto mode, 25L96 A4 adjust to '0x58'\n")
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
        print(repr(strCmdIn.value)+'\n')
        f.write(repr(strCmdIn.value)+'\n')
        strCmdOutBuff = ctypes.c_ubyte * 8
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
    print("\nGN25L96 APC auto mode,now tempIndex is {}, 25L96 A4 should adjust to '0x{:2X}'".format(tempIndex,int(
        tempIndex*int('0x251',16)/1000+int('0x5F',16))))
    f.write("\nGN25L96 APC auto mode,now tempIndex is {}, 25L96 A4 should adjust to '0x{:2X}'".format(tempIndex,int(
        tempIndex*int('0x251',16)/1000+int('0x5F',16))))
else:
    print("\nGN25L96 APC auto mode,now tempIndex is {}, 25L96 A4 should adjust to '0x{:2X}'".format(tempIndex, int(
        tempIndex * int('0x1C4', 16) / 1000 + int('0x6C', 16))))
    f.write("\nGN25L96 APC auto mode,now tempIndex is {}, 25L96 A4 should adjust to '0x{:2X}'".format(tempIndex, int(
        tempIndex * int('0x1C4', 16) / 1000 + int('0x6C', 16))))
f.write('\n')
strCmdIn = create_string_buffer(b'MCU_SET_TABLE(LUT,2,0,0x4B,0x02,0x51,0x00,0x5F,0xFF,0x01,0xC4,0x00,0x6C)')
f.write(repr(strCmdIn.value)+'\n')
strCmdOutBuff = ctypes.c_ubyte*8
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0])+chr(strCmdOut[1]):
    # TODO: first read back,then hold target,max,miin
    strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(4, A, 0, 0, 0, 0)')
    print(repr(strCmdIn.value)+'\n')
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
f.write("\n\nGN25L96 Mod Max auto mode, 25L96 A7 adjust to '0x38'\n")
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
        #print("{}".format(ascii2hex(strCmdOut[item])))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

ascii_list = list(strCmdOut)
#print("\ntempIndex : {}".format(ascii_list))
#print("\n{}".format(chr(ascii_list[4])))
#print("\n{}".format(chr(ascii_list[5])))
tempIndex = int(chr(ascii_list[4]), 16)*16+int(chr(ascii_list[5]), 16)
print("\ntempIndex : {}".format(tempIndex))

if tempIndex < 0x60:
    print("\nGN25L96 Mod Max auto mode,now tempIndex is {}, 25L96 A7 should adjust to '0x{:2X}'".format(tempIndex,int(
        tempIndex*int('0x251',16)/1000+int('0x5F',16))))
    f.write("\nGN25L96 Mod Max auto mode,now tempIndex is {}, 25L96 A7 should adjust to '0x{:2X}'".format(tempIndex,int(
        tempIndex*int('0x251',16)/1000+int('0x5F',16))))
else:
    print("\nGN25L96 Mod Max auto mode,now tempIndex is {}, 25L96 A7 should adjust to '0x{:2X}'".format(tempIndex, int(
        tempIndex * int('0x1C4', 16) / 1000 + int('0x6C', 16))))
    f.write("\nGN25L96 Mod Max auto mode,now tempIndex is {}, 25L96 A7 should adjust to '0x{:2X}'".format(tempIndex, int(
        tempIndex * int('0x1C4', 16) / 1000 + int('0x6C', 16))))
f.write('\n')
strCmdIn = create_string_buffer(b'MCU_SET_TABLE(LUT,7,0,0x60,0x02,0x51,0x00,0x5F,0xFF,0x01,0xC4,0x00,0x6C)')
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
########################################################
#               Verify GN25L96 AER
#########################################################
print("\nGN25L96 AER auto mode, 25L96 A8 adjust to '0x1F'")
f.write("\n\nGN25L96 AER auto mode, 25L96 A8 adjust to '0x1F'\n")
strCmdIn = create_string_buffer(b'MCU_SET_TABLE(LUT,6,0,0x4B,0x00,0x00,0x00,0x1F,0xFF,0x00,0x00,0x00,0x1F)')
f.write(repr(strCmdIn.value)+'\n')
strCmdOutBuff = ctypes.c_ubyte*8
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0])+chr(strCmdOut[1]):
    # TODO: first read back,then hold target,max,miin
    strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(7, A, 0, 0, 0, 0)')
    f.write(repr(strCmdIn.value)+'\n')
    time.sleep(1)
    strCmdOutBuff = ctypes.c_ubyte * 8
    strCmdOut = strCmdOutBuff()
    cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
        strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0xA8,1)')
        f.write(repr(strCmdIn.value)+'\n')
        strCmdOutBuff = ctypes.c_ubyte * 8
        strCmdOut = strCmdOutBuff()
        cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))

print("\nGN25L96 AER auto mode, 25L96 A8 adjust to '0x28'")
f.write("\n\nGN25L96 AER auto mode, 25L96 A8 adjust to '0x28'\n")
strCmdIn = create_string_buffer(b'MCU_SET_TABLE(LUT,6,0,0x4B,0x00,0x00,0xFF,0xE8,0xFF,0x00,0x00,0xFF,0xE8)')
f.write(repr(strCmdIn.value)+'\n')
strCmdOutBuff = ctypes.c_ubyte*8
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0])+chr(strCmdOut[1]):
    # TODO: first read back,then hold target,max,miin
    strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(7, A, 0, 0, 0, 0)')
    f.write(repr(strCmdIn.value)+'\n')
    time.sleep(1)
    strCmdOutBuff = ctypes.c_ubyte * 8
    strCmdOut = strCmdOutBuff()
    cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
        strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0xA8,1)')
        f.write(repr(strCmdIn.value)+'\n')
        strCmdOutBuff = ctypes.c_ubyte * 8
        strCmdOut = strCmdOutBuff()
        cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))

AteAllPowerOff(devUsbIndex)
f.close()

