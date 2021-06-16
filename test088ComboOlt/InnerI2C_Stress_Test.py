import ctypes
from ctypes import *
import time
from cmdServ import cmdservdll,Sfp_Factory_Pwd_Entry
from cmdServ import getAdc0, adc02TempIndex
from classTestEvb import *
import sys

#Test times
#wr_and_rd_times  = 5
run_time_second = 3600*4  # unit : s
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
endTick = startTick + run_time_second
dateTime = time.strptime(time.asctime( time.localtime(startTick)))
dateTime = "{:4}-{:02}-{:02} {:02}:{:02}:{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
testTitle = strFwVer
fileName = strFwVer+'.txt'
f = open(fileName, 'a+')
time.sleep(1)
print("\n****************************************************************************")
print("Inner I2c stress test, start time : {}".format(dateTime))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nInner I2c stress test, start time : {}".format(dateTime))
f.write("\n****************************************************************************")
print("{}".format(testTitle))
f.write('\n'+testTitle)

#########################################################
#           Write APC Lut and set auto mode
#########################################################
f.write('\n')
strCmdIn = create_string_buffer(b'MCU_SET_TABLE(LUT,2,0,0x4B,0x03,0x51,0x00,0x5F,0xFF,0x03,0xC4,0x00,0x6C)')
f.write(repr(strCmdIn.value)+'\n')
strCmdOutBuff = ctypes.c_ubyte*8
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0])+chr(strCmdOut[1]):
    # TODO: first read back,then hold target,max,miin
    print("Write 25L96 APC lut, ok")
    f.write("Write 25L96 APC lut, ok")
    strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(6, A, 0, 0, 0, 0)')
    #print(repr(strCmdIn.value)+'\n')
    f.write(repr(strCmdIn.value)+'\n')
    time.sleep(1)
    strCmdOutBuff = ctypes.c_ubyte * 8
    strCmdOut = strCmdOutBuff()
    cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
        print("Set 25L96 APC auto mode, ok")
        f.write("Set 25L96 APC auto mode, ok")
    else:
        print("Set 25L96 APC auto mode, fail ")
        f.write("Set 25L96 APC auto mode, fail ")
else:
    print("Write 25L96 APC lut, fail")
    f.write("Write 25L96 APC lut, fail")
#########################################################
#           Write MOD Max Lut and set auto mode
#########################################################
f.write('\n')
strCmdIn = create_string_buffer(b'MCU_SET_TABLE(LUT,11,0,0x60,0x02,0x51,0x00,0x5F,0xFF,0x01,0xC4,0x00,0x6C)')
f.write(repr(strCmdIn.value)+'\n')
strCmdOutBuff = ctypes.c_ubyte*8
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0])+chr(strCmdOut[1]):
    # TODO: first read back,then hold target,max,miin
    print("Write 25L96 MOD Max lut, ok")
    f.write("Write 25L96 MOD Max lut, ok")
    strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(10, A, 0, 0, 0, 0)')
    f.write(repr(strCmdIn.value)+'\n')
    time.sleep(1)
    strCmdOutBuff = ctypes.c_ubyte * 8
    strCmdOut = strCmdOutBuff()
    cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
        print("Set 25L96 MOD Max auto mode, ok")
        f.write("Set 25L96 MOD Max auto mode, ok")
    else:
        print("Set 25L96 MOD Max auto mode, fail ")
        f.write("Set 25L96 MOD Max auto mode, fail ")
else:
    print("Write 25L96 MOD Max lut, fail")
    f.write("Write 25L96 MOD Max lut, fail")
#########################################################
#           Write AER Lut and set auto mode
#########################################################
f.write('\n')
strCmdIn = create_string_buffer(b'MCU_SET_TABLE(LUT,3,0,0x5A,0xFE,0xA8,0x00,0x1E,0xFF,0xFE,0x70,0x00,0x52)')
f.write(repr(strCmdIn.value)+'\n')
strCmdOutBuff = ctypes.c_ubyte*8
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0])+chr(strCmdOut[1]):
    # TODO: first read back,then hold target,max,miin
    print("Write 25L96 AER lut, ok")
    f.write("Write 25L96 AER lut, ok")
    strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(7, A, 0, 0, 0, 0)')
    f.write(repr(strCmdIn.value)+'\n')
    time.sleep(1)
    strCmdOutBuff = ctypes.c_ubyte * 8
    strCmdOut = strCmdOutBuff()
    cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
        print("Set 25L96 AER auto mode, ok")
        f.write("Set 25L96 AER auto mode, ok")
    else:
        print("Set 25L96 AER auto mode, fail ")
        f.write("Set 25L96 AER auto mode, fail ")
else:
     print("Write 25L96 AER lut, fail")
     f.write("Write 25L96 AER lut, fail")
#########################################################
#               Get temperature index
#########################################################
#for cnt in range(wr_and_rd_times):
while time.time() < endTick:
    strCmdOutBuff = ctypes.c_ubyte*32
    strCmdOut = strCmdOutBuff()
    strCmdOut = getAdc0()
    if 0 != strCmdOut:
        print("\n\nADC 0(Hex):")
        f.write('\n\nMCU_GET_ADC 0 :')
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
    else:
        print("Can't get ADC 0 ")
        f.write("Can't get ADC 0 ")

    tempIndex = adc02TempIndex(strCmdOut)
    print("\ntempIndex : {}".format(tempIndex))
    f.write("\ntempIndex : {}".format(tempIndex))
    #########################################################
    #               Verify GN25L96 APC
    #########################################################
    if tempIndex < 0x4B:
        print("GN25L96 APC auto mode,now tempIndex is {}, 25L96 A4 should adjust to '0x{:02X}'".format(tempIndex,int(
            tempIndex*int('0x351',16)/1000+int('0x5F',16))))
        f.write("\nGN25L96 APC auto mode,now tempIndex is {}, 25L96 A4 should adjust to '0x{:02X}'".format(tempIndex,int(
            tempIndex*int('0x351',16)/1000+int('0x5F',16))))
    else:
        print("\nGN25L96 APC auto mode,now tempIndex is {}, 25L96 A4 should adjust to '0x{:02X}'".format(tempIndex, int(
            tempIndex * int('0x3C4', 16) / 1000 + int('0x6C', 16))))
        f.write("\nGN25L96 APC auto mode,now tempIndex is {}, 25L96 A4 should adjust to '0x{:02X}'".format(tempIndex, int(
            tempIndex * int('0x3C4', 16) / 1000 + int('0x6C', 16))))
    f.write("\n")
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
    if tempIndex < 0x60:
        print("\nGN25L96 Mod Max auto mode,now tempIndex is {}, 25L96 A7 should adjust to '0x{:02X}'".format(tempIndex,int(
            tempIndex*int('0x251',16)/1000+int('0x5F',16))))
        f.write("\nGN25L96 Mod Max auto mode,now tempIndex is {}, 25L96 A7 should adjust to '0x{:02X}'".format(tempIndex,int(
            tempIndex*int('0x251',16)/1000+int('0x5F',16))))
    else:
        print("\nGN25L96 Mod Max auto mode,now tempIndex is {}, 25L96 A7 should adjust to '0x{:02X}'".format(tempIndex, int(
            tempIndex * int('0x1C4', 16) / 1000 + int('0x6C', 16))))
        f.write("\nGN25L96 Mod Max auto mode,now tempIndex is {}, 25L96 A7 should adjust to '0x{:02X}'".format(tempIndex, int(
            tempIndex * int('0x1C4', 16) / 1000 + int('0x6C', 16))))
    f.write("\n")
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
    if tempIndex < 0x5A:
        print("\nGN25L96 AER auto mode,now tempIndex is {}, 25L96 A8 should adjust to '0x{:02X}'".format(tempIndex,int(
            tempIndex*(int('0xFEA8',16)-65535)/1000+int('0x1E',16))))
        f.write("\nGN25L96 AER auto mode,now tempIndex is {}, 25L96 A8 should adjust to '0x{:02X}'".format(tempIndex,int(
            tempIndex*(int('0xFEA8',16)-65535)/1000+int('0x1E',16))))
    else:
        print("\nGN25L96 AER auto mode,now tempIndex is {}, 25L96 A8 should adjust to '0x{:02X}'".format(tempIndex, int(
            tempIndex * (int('0xFE70', 16)-65535) / 1000 + int('0x52', 16))))
        f.write("\nGN25L96 AER auto mode,now tempIndex is {}, 25L96 A8 should adjust to '0x{:02X}'".format(tempIndex, int(
            tempIndex * (int('0xFE70', 16)-65535) / 1000 + int('0x52', 16))))
    f.write("\n")
    strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0xA8,1)')
    f.write(repr(strCmdIn.value)+'\n')
    strCmdOutBuff = ctypes.c_ubyte * 8
    strCmdOut = strCmdOutBuff()
    cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))

dateTime = time.strptime(time.asctime())
dateTime = "{:4}-{:02}-{:02} {:02}:{:02}:{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
print("\n****************************************************************************")
print("Inner I2c stress test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nInner I2c stress test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
f.write("\n****************************************************************************")
testEvb.AteAllPowerOff()
f.close()

