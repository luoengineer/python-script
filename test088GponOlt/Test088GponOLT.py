import ctypes
from ctypes import *
import time
from cmdServ import cmdservdll, devUsbIndex, devSffChannel
from cmdServ import Sfp_Factory_Pwd_Entry, AteAllPowerOn, AteAllPowerOff, openUsbDevice
import sys

#########################################################
#               Test Configuration
#########################################################
#True or False
A0_WRITE_READ_STRESS_TEST = True
A2_WRITE_READ_STRESS_TEST = True
Driver_GN25L96_TEST = True
Driver_UX3320_TEST = False
TxPower08uW_Alarm_Warning_TEST = False
TxPower_Dis_En_STRESS_TEST = True
Inner_I2C_STRESS_TEST = True

# user type for password
is_088_Module = 0
is_other_Module = 1
user_password_type = is_088_Module

# Product list
SfpI2cAddr = [0xA0,0xA2,0xA4]

#load dll
objdll = ctypes.cdll.LoadLibrary(".\ATEAPI.dll")

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
print("Generic GPON OLT test, start time : {}".format(dateTime))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nGeneric GPON OLT test, start time : {}".format(dateTime))
f.write("\n****************************************************************************")
print("{}".format(testTitle))
f.write('\n'+testTitle)


#########################################################
#               Read  A0
#########################################################
A0RawDataBuff = ctypes.c_ubyte*256
A0RawReadByte = A0RawDataBuff()
f.write("\nA0 raw data: \n")
Res = 0xFF
Res = objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[0], 0, 256, A0RawReadByte)
if 0 == Res:
    for item in range(len(A0RawReadByte)):
        print("{}{:0>2X}".format("0x", A0RawReadByte[item]), end=',')
        f.write("{}{:0>2X}{}".format("0x", A0RawReadByte[item], ","))
else:
    print('read raw data fail.'+'\n')
    f.write('read raw data fail.'+'\n')

print("\n")
f.write('\n\n')
#########################################################
#               Read  A2
#########################################################
A2RawDataBuff = ctypes.c_ubyte*256
A2RawReadByte = A2RawDataBuff()
f.write("A2 raw data: \n")
Res = 0xFF
Res = objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 0, 256, A2RawReadByte)
if 0 == Res:
    for item in range(len(A2RawReadByte)):
        print("{}{:0>2X}".format("0x", A2RawReadByte[item]), end=",")
        f.write("{}{:0>2X}{}".format("0x", A2RawReadByte[item], ","))
else:
    print('read raw data fail.' + '\n')
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

#########################################################
#               Adjust  check
#########################################################
print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_ADJUST(0)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_GET_ADJUST 0 :')
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
    print('MCU_GET_ADJUST 1 :')
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
    print('MCU_GET_ADJUST 2 :')
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
    print('MCU_GET_ADJUST 3 :')
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
    print('MCU_GET_ADJUST 4 :')
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
    print('MCU_GET_ADJUST 5 :')
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
    print('MCU_GET_ADJUST 6 :')
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
    print('MCU_GET_ADJUST 7 :')
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
#########################################################
#               DAC  check
#########################################################
print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_DAC(0)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_GET_DAC 0 :')
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
    print('MCU_GET_DAC 1 :')
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

#########################################################
#               ADJUST SET DAC0 (LOS)
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
        print('MCU_GET_DAC 0 :')
        f.write('MCU_GET_DAC 0 :')
        tempCmdOut = strCmdOut[2:4]
        strCmdOut[2:4] = strCmdOut[4:6]
        strCmdOut[4:6] = tempCmdOut
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
    else:
        print("\nMCU_GET_DAC 0 fail : {0:d}".format(retStauts))
        f.write("\nMCU_GET_DAC 0 fail : {0:d}".format(retStauts))
else:
    print("MCU_SET_ADJUST(0,M,0,0x0005,0,0) fail :{0:d}".format(retStauts))
    f.write("MCU_SET_ADJUST(0,M,0,0x0005,0,0) fail ：{0:d}".format(retStauts))
#########################################################
#               COMMAND SET DAC0 (LOS)
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
        print('MCU_GET_DAC 0 :')
        f.write('MCU_GET_DAC 0 :')
        tempCmdOut = strCmdOut[2:4]
        strCmdOut[2:4] = strCmdOut[4:6]
        strCmdOut[4:6] = tempCmdOut
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
    else:
        print("\nMCU_GET_DAC 0 fail : {0:d}".format(retStauts))
        f.write("\nMCU_GET_DAC 0 fail : {0:d}".format(retStauts))
else:
    print("\nMCU_SET_DAC(0, 0xA00) fail :{0:d}".format(retStauts))
    f.write("\nMCU_SET_DAC(0, 0xA00) fail :{0:d}".format(retStauts))
#########################################################
#               ADJUST SET DAC1 (GPON APD)
#########################################################
print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(1,M,0,0x000E,0xFF0F,0x0005)') #little endian
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
    f.write('MCU_SET_ADJUST(1,M,0,0x834,0xDAC,0x640) ,')
    strCmdIn = create_string_buffer(b'MCU_GET_DAC(1)')
    retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 0 == retStauts:
        print('MCU_GET_DAC 1 :')
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
    print("MCU_SET_ADJUST(1,M,0,0x000E,0xFF0F,0x0000) fail :{0:d}".format(retStauts))
    f.write("MCU_SET_ADJUST(1,M,0,0x000E,0xFF0F,0x0000) fail ：{0:d}".format(retStauts))

#########################################################
#               COMMAND SET DAC1 (GPON APD)
#########################################################
print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(1,I,0,0xFF0F,0xFF0F,0x0005)') #little endian
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
strCmdIn = create_string_buffer(b'MCU_SET_DAC(1, 0x000E)') #little endian
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
    print('MCU_SET_DAC(1, 0xE00) ,')
    f.write('MCU_SET_DAC(1, 0xE00) ,')
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
    print("\nMCU_SET_DAC(1, 0xE00) fail :{0:d}".format(retStauts))
    f.write("\nMCU_SET_DAC(1, 0xE00) fail :{0:d}".format(retStauts))
#########################################################
#               Lut  check
#########################################################
print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_TABLE(base,0,0,128)')
strCmdOutBuff = ctypes.c_ubyte*640
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_GET_TABLE base 0 :')
    f.write('MCU_GET_TABLE base 0 :')
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("Get base 0 table fail, error code :{0:d}".format(retStauts))
    f.write("Get base 0 table fail, error code :{0:d}".format(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_TABLE(base,1,0,128)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_GET_TABLE base 1 :')
    f.write('MCU_GET_TABLE base 1 :')
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("Get base 1 table fail, error code :{0:d}".format(retStauts))
    f.write("Get base 1 table fail, error code :{0:d}".format(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_TABLE(base,3,0,128)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_GET_TABLE base 3 :')
    f.write('MCU_GET_TABLE base 3 :')
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("Get base 3 table fail, error code :{0:d}".format(retStauts))
    f.write("Get base 3 table fail, error code :{0:d}".format(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_TABLE(driver,0,0,128)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_GET_TABLE driver 0 :')
    f.write('MCU_GET_TABLE driver 0 :')
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("Get driver 0 table fail, error code :{0:d}".format(retStauts))
    f.write("Get driver 0 table fail, error code :{0:d}".format(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_TABLE(lut,0,0,128)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_GET_TABLE lut 0 :')
    f.write('MCU_GET_TABLE lut 0 :')
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("Get lut 0 table fail, error code :{0:d}".format(retStauts))
    f.write("Get lut 0 table fail, error code :{0:d}".format(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_TABLE(lut,1,0,128)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_GET_TABLE lut 1 :')
    f.write('MCU_GET_TABLE lut 1 :')
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("Get lut 1 table fail, error code :{0:d}".format(retStauts))
    f.write("Get lut 1 table fail, error code :{0:d}".format(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_TABLE(lut,2,0,128)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_GET_TABLE lut 2 :')
    f.write('MCU_GET_TABLE lut 2 :')
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("Get lut 2 table fail, error code :{0:d}".format(retStauts))
    f.write("Get lut 2 table fail, error code :{0:d}".format(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_TABLE(lut,3,0,128)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_GET_TABLE lut 3 :')
    f.write('MCU_GET_TABLE lut 3 :')
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("Get lut 3 table fail, error code :{0:d}".format(retStauts))
    f.write("Get lut 3 table fail, error code :{0:d}".format(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_TABLE(lut,4,0,128)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_GET_TABLE lut 4 :')
    f.write('MCU_GET_TABLE lut 4 :')
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("Get lut 4 table fail, error code :{0:d}".format(retStauts))
    f.write("Get lut 4 table fail, error code :{0:d}".format(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_TABLE(lut,6,0,128)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_GET_TABLE lut 6 :')
    f.write('MCU_GET_TABLE lut 6 :')
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("Get lut 6 table fail, error code :{0:d}".format(retStauts))
    f.write("Get lut 6 table fail, error code :{0:d}".format(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_TABLE(lut,7,0,128)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_GET_TABLE lut 7 :')
    f.write('MCU_GET_TABLE lut 7 :')
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("Get lut 7 table fail, error code :{0:d}".format(retStauts))
    f.write("Get lut 7 table fail, error code :{0:d}".format(retStauts))

del strCmdIn
del strCmdOutBuff, strCmdOut

dateTime = time.strptime(time.asctime())
dateTime = "{:4}-{:02}-{:02} {:02}:{:02}:{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
print("\n****************************************************************************")
print("Generic GPON OLT basic test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nGeneric GPON OLT basic test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
f.write("\n****************************************************************************")
AteAllPowerOff(devUsbIndex)
f.close()

if True == TxPower08uW_Alarm_Warning_TEST:
    with open('.\Tx08uw_AlarmWarning_Test.py', 'rb') as fi:
        exec(fi.read())

if True == Driver_GN25L96_TEST:
    with open('.\Driver_GN25L96_Test.py', 'r') as fi:
        exec(fi.read())


if True == Driver_UX3320_TEST:
    with open('.\Driver_UX3320_Test.py', 'rb') as fi:
        exec(fi.read())

#A0 write and read repeated
if True == A0_WRITE_READ_STRESS_TEST:
    with open('.\A0_Direct_Write_Read_Repeated_Test.py', 'r') as fi:
        exec(fi.read())

#A2 write and read repeated
if True == A2_WRITE_READ_STRESS_TEST:
    with open('.\A2_Direct_Write_Read_Repeated_Test.py', 'r') as fi:
        exec(fi.read())

if True == TxPower_Dis_En_STRESS_TEST:
    with open('.\Tx_Soft_Dis_En_Repeated_Test.py', 'rb') as fi:
        exec(fi.read())

if True == Inner_I2C_STRESS_TEST:
    with open('.\InnerI2C_Stress_Test.py', 'rb') as fi:
        exec(fi.read())