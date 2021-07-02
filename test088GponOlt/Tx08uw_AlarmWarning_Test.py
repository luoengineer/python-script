import ctypes
from ctypes import *
import time
from cmdServ import *
from cmdServ import cmdservdll,Sfp_Factory_Pwd_Entry
from classTestEvb import *
import sys

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

devUsbIndex = 0
devSffChannel = 1
devSfpChannel = 2

#########################################################
#               create object
#########################################################
testEvb = cTestEvb(devUsbIndex)


txPower08uWAll = {48:0x00, 49:0x00, 50:0x00, 51:0x00, 52:0x00, 53:0x00, 54:0x00, 55:0x00, 108:0x00, 109:0x00}
txPower08uWThreshold = list(txPower08uWAll.values())[0:8]
addrArray = list(txPower08uWAll.keys())
#########################################################
#               Inner Funtion
#########################################################
def txpower08uwFlagAssert(devUsbIndex, devSffChannel, SfpI2cAddr):
#def txpower08uwFlagAssert(*devParams)
    A2ReadDatBuf = ctypes.c_ubyte*1
    A2Read = A2ReadDatBuf()
    Ret = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr, 113, 1, A2Read)
    if 0 == Ret:
        print('A2[{}]=0x{:0>2X}'.format(113, A2Read[0]))
        print('TX Power High Alarm（0.8uW）flag: {}'.format((A2Read[0]&0x02)>>1))
        print('TX Power Low Alarm（0.8uW）flag: {}'.format((A2Read[0] & 0x01)))
        f.write('\nA2[{}]=0x{:0>2X}'.format(113, A2Read[0]))
        f.write('\nTX Power High Alarm（0.8uW）flag: {}'.format((A2Read[0] & 0x02) >> 1))
        f.write('\nTX Power Low Alarm（0.8uW）flag: {}'.format((A2Read[0] & 0x01)))
    else:
        print("{}".format(Ret))
    Ret = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr, 117, 1, A2Read)
    if 0 == Ret:
        print('A2[{}]=0x{:0>2X}'.format(117, A2Read[0]))
        print('TX Power High Warning（0.8uW）flag: {}'.format((A2Read[0] & 0x02) >> 1))
        print('TX Power Low Warning（0.8uW）flag: {}'.format((A2Read[0] & 0x01)))
        f.write('\nA2[{}]=0x{:0>2X}'.format(117, A2Read[0]))
        f.write('\nTX Power High Waring（0.8uW）flag: {}'.format((A2Read[0] & 0x02) >> 1))
        f.write('\nTX Power Low Warning（0.8uW）flag: {}'.format((A2Read[0] & 0x01)))
    else:
        print("{}".format(Ret))




#########################################################
#               Open USB Device
#########################################################
#TODO: How to config several usb device
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
print("tx(0.8uW) alarm and warning test, start time : {}".format(dateTime))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\ntx(0.8uW) alarm and warning test, start time : {}".format(dateTime))
f.write("\n****************************************************************************")
print("{}".format(testTitle))
f.write('\n'+testTitle)




#1, read 0.8uw txpower
print("\nRead 0.8uW Txpowr from A2 108-109")
f.write('\n\nRead 0.8uW Txpowr from A2 108-109')
A2ReadTxDataBuff = ctypes.c_ubyte*2
A2ReadTxByte = A2ReadTxDataBuff()
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 108, 2, A2ReadTxByte)
if 0 == Res:
    print('A2[{}]=0x{:0>2X}, A2[{}]=0x{:0>2X}'.format(108, A2ReadTxByte[0], 109, A2ReadTxByte[1]))
    f.write('\nA2[{}]=0x{:0>2X}, A2[{}]=0x{:0>2X}'.format(108, A2ReadTxByte[0], 109, A2ReadTxByte[1]))
if 0 == A2ReadTxByte[0] and 0 == A2ReadTxByte[1]:
    txPower = '-40'
    print("txpower is {} uW".format(txPower))
    f.write("\ntxpower is {} uW".format(txPower))
else:
    txPower = math.log10((A2ReadTxByte[0]*256 + A2ReadTxByte[1])/1250) * 10
    print("txpower is {:0>4f} uW".format(txPower))
    f.write("\ntxpower is {:0>4f} uW".format(txPower))

#2, read alarm and warn threshold
A2Tx08uWHighAlarm = A2Tx08uWLowAlarm = A2Tx08uWHighWarning = A2Tx08uWLowWarning = 0
print("Read  A2 48-55")
f.write('\n\nRead A2 48-55')
A2ReadDataBuff = ctypes.c_ubyte*8
A2ReadByte = A2ReadDataBuff()
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 48, 8, A2ReadByte)
if 0 == Res:
    #hold raw data
    A2Tx08uWThresholdArray = list(A2ReadByte)
    A2Tx08uWHighAlarm = A2Tx08uWThresholdArray[0:2]
    A2Tx08uWLowAlarm  = A2Tx08uWThresholdArray[2:4]
    A2Tx08uWHighWarning = A2Tx08uWThresholdArray[4:6]
    A2Tx08uWLowWarning = A2Tx08uWThresholdArray[6:]
    #print("{}".format(A2Tx08uWThreshold))
    print('A2[{}]=0x{:0>2X}, A2[{}]=0x{:0>2X}'.format(48, A2ReadByte[0], 49, A2ReadByte[1]))
    f.write('\nA2[{}]=0x{:0>2X}, A2[{}]=0x{:0>2X}'.format(48, A2ReadByte[0], 49, A2ReadByte[1]))
    if 0 == (A2ReadByte[0] * 256 + A2ReadByte[1]):
        print("High Alarm is {} uW".format('-Inf'))
        f.write("\nHigh Alarm is {} uW".format('-Inf'))
    else:
        txPower = math.log10((A2ReadByte[0] * 256 + A2ReadByte[1]) / 1250) * 10
        print("High Alarm is {:0>4f} uW".format(txPower))
        f.write("\nHigh Alarm is {:0>4f} uW".format(txPower))

    print('A2[{}]=0x{:0>2X}, A2[{}]=0x{:0>2X}'.format(50, A2ReadByte[2], 51, A2ReadByte[3]))
    f.write('\n\nA2[{}]=0x{:0>2X}, A2[{}]=0x{:0>2X}'.format(50, A2ReadByte[2], 51, A2ReadByte[3]))
    if 0 == (A2ReadByte[2] * 256 + A2ReadByte[3]):
        print("Low Alarm is {} uW".format('-Inf'))
        f.write("\nLow Alarm is {} uW".format('-Inf'))
    else:
        txPower = math.log10((A2ReadByte[2] * 256 + A2ReadByte[3]) / 1250) * 10
        print("Low Alarm is {:0>4f} uW".format(txPower))
        f.write("\nLow Alarm is {:0>4f} uW".format(txPower))

    print('A2[{}]=0x{:0>2X}, A2[{}]=0x{:0>2X}'.format(52, A2ReadByte[4], 53, A2ReadByte[5]))
    f.write('\n\nA2[{}]=0x{:0>2X}, A2[{}]=0x{:0>2X}'.format(52, A2ReadByte[4], 53, A2ReadByte[5]))
    if 0 == (A2ReadByte[4] * 256 + A2ReadByte[5]):
        print("High Warning is {} uW".format('-Inf'))
        f.write("\nHigh Warning is {} uW".format('-Inf'))
    else:
        txPower = math.log10((A2ReadByte[4] * 256 + A2ReadByte[5]) / 1250) * 10
        print("High Warning is {:0>4f} uW".format(txPower))
        f.write("\nHigh Warning is {:0>4f} uW".format(txPower))

    print('A2[{}]=0x{:0>2X}, A2[{}]=0x{:0>2X}'.format(54, A2ReadByte[6], 55, A2ReadByte[7]))
    f.write('\n\nA2[{}]=0x{:0>2X}, A2[{}]=0x{:0>2X}'.format(54, A2ReadByte[6], 55, A2ReadByte[7]))
    if 0 == (A2ReadByte[6] * 256 + A2ReadByte[7]):
        print("Low Warning is {} uW".format('-Inf'))
        f.write("\nLow Warning is {} uW".format('-Inf'))
    else:
        txPower = math.log10((A2ReadByte[6] * 256 + A2ReadByte[7]) / 1250) * 10
        print("Low Warning is {:0>4f} uW".format(txPower))
        f.write("\nLow Warning is {:0>4f} uW".format(txPower))

#3,read alarm and warning flag
txpower08uwFlagAssert(devUsbIndex, devSffChannel, SfpI2cAddr[1])

#4, modify alarm or warning threshold
print("\nModify Txpower (0.8uW ) High alarm threshold. High alarm flag will be '1' ")
f.write("\n\nModify Txpower (0.8uW ) High alarm threshold'. High alarm flag will be '1'")
i2cWriteBuf = c_ubyte * 2
i2dWriteByte = i2cWriteBuf(A2Tx08uWLowAlarm[0], A2Tx08uWLowAlarm[1])
Res = testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, 0xA2, 48, 2, byref(i2dWriteByte))
if 0 == Res:
    time.sleep(1)
    txpower08uwFlagAssert(devUsbIndex, devSffChannel, SfpI2cAddr[1])
else:
    print("Write A2[48-49] fail. ")

print("\nModify Txpower (0.8uW ) Low alarm threshold. Low alarm flag will be '1'")
f.write("\n\nModify Txpower (0.8uW ) Low alarm threshold. Low alarm flag will be '1'")
i2dWriteByte = i2cWriteBuf(A2Tx08uWHighAlarm[0], A2Tx08uWHighAlarm[1])
Res = testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, 0xA2, 50, 2, byref(i2dWriteByte))
if 0 == Res:
    time.sleep(1)
    txpower08uwFlagAssert(devUsbIndex, devSffChannel, SfpI2cAddr[1])
else:
    print("Write A2[50-51] fail. ")

print("\nModify Txpower (0.8uW ) High warning threshold. High warning will be '1'")
f.write("\n\nModify Txpower (0.8uW ) High warning threshold. High warning will be '1'")
i2cWriteBuf = c_ubyte * 2
i2dWriteByte = i2cWriteBuf(A2Tx08uWLowWarning[0], A2Tx08uWLowWarning[1])
Res = testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, 0xA2, 52, 2, byref(i2dWriteByte))
if 0 == Res:
    time.sleep(1)
    txpower08uwFlagAssert(devUsbIndex, devSffChannel, SfpI2cAddr[1])
else:
    print("Write A2[52-53] fail. ")

print("\nModify Txpower (0.8uW ) Low warning threshold. Low warning flag will be '1'")
f.write("\n\nModify Txpower (0.8uW ) Low warning threshold. Low warning flag will be '1'")
i2dWriteByte = i2cWriteBuf(A2Tx08uWHighWarning[0], A2Tx08uWHighWarning[1])
Res = testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, 0xA2, 54, 2, byref(i2dWriteByte))
if 0 == Res:
    time.sleep(1)
    txpower08uwFlagAssert(devUsbIndex, devSffChannel, SfpI2cAddr[1])
else:
    print("Write A2[54-55] fail. ")

#restore raw threshold
i2cWriteBuf = ctypes.c_ubyte*8
A2WriteByte = i2cWriteBuf(A2Tx08uWHighAlarm[0],A2Tx08uWHighAlarm[1],A2Tx08uWLowAlarm[0],A2Tx08uWLowAlarm[1],
                          A2Tx08uWHighWarning[0],A2Tx08uWHighWarning[1],A2Tx08uWLowWarning[0],A2Tx08uWLowWarning[1])
testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 48, 8, A2WriteByte)
time.sleep(1)
print("\nRestore A2 txpower(0.8uW) threshold ")
f.write("\n\nRestore A2 txpower(0.8uW) threshold ")
txpower08uwFlagAssert(devUsbIndex, devSffChannel, SfpI2cAddr[1])
dateTime = time.strptime(time.asctime())
dateTime = "{:4}-{:02}-{:02} {:02}:{:02}:{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
print("\n****************************************************************************")
print("tx(0.8uW) alarm and warning test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\ntx(0.8uW) alarm and warning test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
f.write("\n****************************************************************************")
testEvb.AteAllPowerOff()

f.close()

