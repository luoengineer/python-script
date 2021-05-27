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
    for item in range(len(strCmdOut)):
        if 0x00 != strCmdOut[item]:
            #print("{}".format(chr(strCmdOut[item])), end='')
            strFwVer.append(chr(strCmdOut[item]))
    else:
        print("{0:d}".format(retStauts))
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
print("driver UX3320 test, start time : {}".format(dateTime))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\ndriver UX3320 test, start time : {}".format(dateTime))
f.write("\n****************************************************************************")
print("{}".format(testTitle))
f.write('\n'+testTitle)

print("\nGet Driver register initial Value:\n")
f.write('\n\nGet Driver register initial Value:\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0x80,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_I2C_READ 0xA2 0x80 8 :')
    f.write('MCU_I2C_READ 0xA2 0x80 8 :')
    for item in range(46):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0x88,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_I2C_READ 0xA2 0x88 8 :')
    f.write('MCU_I2C_READ 0xA2 0x88 8 :')
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
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0xD1,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_I2C_READ 0xA2 0xD1 8 :')
    f.write('MCU_I2C_READ 0xA2 0xD1 8 :')
    for item in range(46):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0xDC,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_I2C_READ 0xA2 0xDC 8 :')
    f.write('MCU_I2C_READ 0xA2 0xDC 8 :')
    for item in range(46):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))


#########################################################
#               Verify UX3320 APC
#########################################################
print("\nUX3320 APC auto mode, UX3320 8C-8Dh adjust to '0x58'")
f.write("\n\nUX3320 APC auto mode, UX3320 8C-8Dh adjust to '0x58'\n")
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
        strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0x8C,2)')
        print(repr(strCmdIn.value)+'\n')
        f.write(repr(strCmdIn.value)+'\n')
        strCmdOutBuff = ctypes.c_ubyte * 10
        strCmdOut = strCmdOutBuff()
        cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
        print("\n[8C-8D]=0x{:2X}".format((int(chr(list(strCmdOut)[2]), 16)*16+int(chr(list(strCmdOut)[3]), 16))*4 + (int(chr(list(strCmdOut)[7]), 16)*16+int(chr(list(strCmdOut)[8]), 16))))
        f.write("\n[8C-8D]=0x{:2X}".format((int(chr(list(strCmdOut)[2]), 16)*16+int(chr(list(strCmdOut)[3]), 16))*4 + (int(chr(list(strCmdOut)[7]), 16)*16+int(chr(list(strCmdOut)[8]), 16))))

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

if tempIndex < 0x60:
    print("\nUX3320 APC auto mode,now tempIndex is {}, UX3320 8C-8Dh should adjust to '0x{:2X}'".format(tempIndex,int(
        tempIndex*int('0x151',16)/1000+int('0x5F',16))))
    f.write("\nUX3320 APC auto mode,now tempIndex is {}, UX3320 8C-8Dh should adjust to '0x{:2X}'".format(tempIndex,int(
        tempIndex*int('0x151',16)/1000+int('0x5F',16))))
else:
    print("\nUX3320 Mod auto mode,now tempIndex is {}, UX3320 87-88h should adjust to '0x{:2X}'".format(tempIndex, int(
        tempIndex * int('0x2C4', 16) / 1000 + int('0x6C', 16))))
    f.write("\nUX3320 Mod Max auto mode,now tempIndex is {}, UX3320 87-88h should adjust to '0x{:2X}'".format(tempIndex, int(
        tempIndex * int('0x2C4', 16) / 1000 + int('0x6C', 16))))
f.write("\n")
strCmdIn = create_string_buffer(b'MCU_SET_TABLE(LUT,2,0,0x60,0x01,0x51,0x00,0x5F,0xFF,0x02,0xC4,0x00,0x6C)')
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
        strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0x8C,2)')
        f.write(repr(strCmdIn.value)+'\n')
        strCmdOutBuff = ctypes.c_ubyte * 10
        strCmdOut = strCmdOutBuff()
        cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
        print("\n[8C-8D]=0x{:2X}".format(
            (int(chr(list(strCmdOut)[2]), 16) * 16 + int(chr(list(strCmdOut)[3]), 16)) * 4 + (
                        int(chr(list(strCmdOut)[7]), 16) * 16 + int(chr(list(strCmdOut)[8]), 16))))
        f.write("\n[8C-8D]=0x{:2X}".format(
            (int(chr(list(strCmdOut)[2]), 16) * 16 + int(chr(list(strCmdOut)[3]), 16)) * 4 + (
                        int(chr(list(strCmdOut)[7]), 16) * 16 + int(chr(list(strCmdOut)[8]), 16))))
#########################################################
#               Verify UX3320 Mod
#########################################################
print("\nUX3320 Mod auto mode, UX3320 87-88h adjust to '0x38'")
f.write("\n\nUX3320 Mod auto mode, UX3320 87-88h adjust to '0x38'\n")
strCmdIn = create_string_buffer(b'MCU_SET_TABLE(LUT,3,0,0x4B,0x00,0x00,0x00,0x38,0xFF,0x00,0x00,0x00,0x38)')
f.write(repr(strCmdIn.value)+'\n')
strCmdOutBuff = ctypes.c_ubyte*8
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0])+chr(strCmdOut[1]):
    # TODO: first read back,then hold target,max,miin
    strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(5, A, 0, 0, 0, 0)')
    f.write(repr(strCmdIn.value)+'\n')
    time.sleep(1)
    strCmdOutBuff = ctypes.c_ubyte * 8
    strCmdOut = strCmdOutBuff()
    cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
        strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0x87,2)')
        print(repr(strCmdIn.value)+'\n')
        f.write(repr(strCmdIn.value)+'\n')
        strCmdOutBuff = ctypes.c_ubyte * 10
        strCmdOut = strCmdOutBuff()
        cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
    print("\n[87-88]=0x{:2X}".format(
        (int(chr(list(strCmdOut)[2]), 16) * 16 + int(chr(list(strCmdOut)[3]), 16)) * 4 + (
                int(chr(list(strCmdOut)[7]), 16) * 16 + int(chr(list(strCmdOut)[8]), 16))))
    f.write("\n[87-88]=0x{:2X}".format(
        (int(chr(list(strCmdOut)[2]), 16) * 16 + int(chr(list(strCmdOut)[3]), 16)) * 4 + (
                int(chr(list(strCmdOut)[7]), 16) * 16 + int(chr(list(strCmdOut)[8]), 16))))
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


if tempIndex < 0x60:
    print("\nUX3320 Mod auto mode,now tempIndex is {}, UX3320 87-88h should adjust to '0x{:2X}'".format(tempIndex,int(
        tempIndex*int('0x251',16)/1000+int('0x5F',16))))
    f.write("\nUX3320 Mod auto mode,now tempIndex is {}, UX3320 87-88h should adjust to '0x{:2X}'".format(tempIndex,int(
        tempIndex*int('0x251',16)/1000+int('0x5F',16))))
else:
    print("\nUX3320 Mod auto mode,now tempIndex is {}, UX3320 87-88h should adjust to '0x{:2X}'".format(tempIndex, int(
        tempIndex * int('0x1C4', 16) / 1000 + int('0x6C', 16))))
    f.write("\nUX3320 Mod Max auto mode,now tempIndex is {}, UX3320 87-88h should adjust to '0x{:2X}'".format(tempIndex, int(
        tempIndex * int('0x1C4', 16) / 1000 + int('0x6C', 16))))
f.write('\n')
strCmdIn = create_string_buffer(b'MCU_SET_TABLE(LUT,3,0,0x60,0x02,0x51,0x00,0x5F,0xFF,0x01,0xC4,0x00,0x6C)')
f.write(repr(strCmdIn.value)+'\n')
strCmdOutBuff = ctypes.c_ubyte*8
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0])+chr(strCmdOut[1]):
    # TODO: first read back,then hold target,max,miin
    strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(5, A, 0, 0, 0, 0)')
    print(repr(strCmdIn.value)+'\n')
    f.write(repr(strCmdIn.value)+'\n')
    time.sleep(1)
    strCmdOutBuff = ctypes.c_ubyte * 10
    strCmdOut = strCmdOutBuff()
    cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
        strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0x87,2)')
        f.write(repr(strCmdIn.value)+'\n')
        strCmdOutBuff = ctypes.c_ubyte * 10
        strCmdOut = strCmdOutBuff()
        cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
    print("\n[87-88]=0x{:2X}".format(
        (int(chr(list(strCmdOut)[2]), 16) * 16 + int(chr(list(strCmdOut)[3]), 16)) * 4 + (
                int(chr(list(strCmdOut)[7]), 16) * 16 + int(chr(list(strCmdOut)[8]), 16))))
    f.write("\n[87-88]=0x{:2X}".format(
        (int(chr(list(strCmdOut)[2]), 16) * 16 + int(chr(list(strCmdOut)[3]), 16)) * 4 + (
                int(chr(list(strCmdOut)[7]), 16) * 16 + int(chr(list(strCmdOut)[8]), 16))))

dateTime = time.strptime(time.asctime())
dateTime = "{:4}-{:02}-{:02} {:02}:{:02}:{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
print("\n****************************************************************************")
print("driver UX3320 test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\ndriver UX3320 test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
f.write("\n****************************************************************************")
AteAllPowerOff(devUsbIndex)
f.close()

