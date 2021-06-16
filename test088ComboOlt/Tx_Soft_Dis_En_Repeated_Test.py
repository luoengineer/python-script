import ctypes
from ctypes import *
import time
import random
import operator
import math
from cmdServ import cmdservdll,Sfp_Factory_Pwd_Entry

from classTestEvb import *
import sys

#Test times
wr_and_rd_times  = 2000
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

tx_soft_dis = 0x40
tx_soft_en  = 0x00

#########################################################
#               Inner Funtion
#########################################################
def txSoftDis():
    i2cWriteBuf = ctypes.c_ubyte*1

    #  write A2[110], disable XG
    i2cWriteByte = i2cWriteBuf(tx_soft_dis)
    testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 110, 1, i2cWriteByte)
    # now write B2[110], disable GPON
    i2cWriteByte = i2cWriteBuf(tx_soft_dis)
    testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, ComboSfpI2cAddr[3], 110, 1, i2cWriteByte)

def txSoftEn():
    i2cWriteBuf = ctypes.c_ubyte * 1
    #  write A2[110], disable XG
    i2cWriteByte = i2cWriteBuf(tx_soft_en)
    testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 110, 1, i2cWriteByte)
    # now write B2[110], disable GPON
    i2cWriteByte = i2cWriteBuf(tx_soft_en)
    testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, ComboSfpI2cAddr[3], 110, 1, i2cWriteByte)

def getXGTxpower():
    i2cReadBuf = ctypes.c_ubyte*2
    i2cReadByte = i2cReadBuf()
    testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 0x66, 2, i2cReadByte)
    return i2cReadByte

def getGPONTxpower():
    i2cReadBuf = ctypes.c_ubyte*2
    i2cReadByte = i2cReadBuf()
    testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[3], 0x66, 2, i2cReadByte)
    return i2cReadByte
def calcTxpower01uW(_byte_dat):
    if 0 == (_byte_dat[0] * 256 + _byte_dat[1]):
        return '-Inf'
    else:
        txPower = math.log10((_byte_dat[0] * 256 + _byte_dat[1]) / 10000) * 10
        return txPower
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
print("Tx Soft Dis-En stress test, start time : {}".format(dateTime))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nTx Soft Dis-En stress test, start time : {}".format(dateTime))
f.write("\n****************************************************************************")
print("{}".format(testTitle))
f.write('\n'+testTitle)

# clear factory password
testEvb.AteAllPowerOff()
time.sleep(2)
testEvb.AteAllPowerOn()
time.sleep(2)

#########################################################
#                 Run test
#########################################################
xgtxSoftDis_ok = xgtxSoftDis_fail = xgtxSoftEn_ok = xgtxSoftEn_fail = 0
gpontxSoftDis_ok = gpontxSoftDis_fail = gpontxSoftEn_ok = gpontxSoftEn_fail = 0
for cnt in range(wr_and_rd_times):
    txSoftDis()
    time.sleep(1)
    i2cReadTx = getXGTxpower()
    txpower = calcTxpower01uW(i2cReadTx)
    if ('-Inf' == txpower) or (-40 == txpower):
        xgtxSoftDis_ok += 1
        print("Round {} XG TX: {} dBm, tx soft disable ok ! ".format(cnt, txpower))
        f.write("\nRound {} XG TX: {} dBm,  tx soft disable ok ! ".format(cnt, txpower))
    else:
        xgtxSoftDis_fail += 1
        print("Round {} XG TX: {} dBm, tx soft disable fail ! ".format(cnt, txpower))
        f.write("\nRound {} XG TX: {} dBm, tx soft disable fail ! ".format(cnt, txpower))
    i2cReadTx = getGPONTxpower()
    txpower = calcTxpower01uW(i2cReadTx)
    if ('-Inf' == txpower) or (-40 == txpower):
        gpontxSoftDis_ok += 1
        print("Round {} GPON TX: {} dBm, tx soft disable ok ! ".format(cnt, txpower))
        f.write("\nRound {} GPON TX: {} dBm, tx soft disable ok ! ".format(cnt, txpower))
    else:
        gpontxSoftDis_fail += 1
        print("Round {} GPON TX: {} dBm, tx soft disable fail ! ".format(cnt, txpower))
        f.write("\nRound {} GPON TX: {} dBm, tx soft disable fail ! ".format(cnt, txpower))

    txSoftEn()
    time.sleep(1)
    i2cReadTx = getXGTxpower()
    txpower = calcTxpower01uW(i2cReadTx)
    if ('-Inf' != txpower) and (-40 < txpower):
        xgtxSoftEn_ok += 1
        print("Round {} XG TX: {} dBm, tx soft enable ok ! ".format(cnt, txpower))
        f.write("\nRound {} XG TX: {} dBm, tx soft enable ok ! ".format(cnt, txpower))
    else:
        xgtxSoftEn_fail += 1
        print("Round {} XG TX: {} dBm, tx soft enable fail ! ".format(cnt, txpower))
        f.write("\nRound {} XG TX: {} dBm, tx soft enable fail ! ".format(cnt, txpower))
    i2cReadTx = getGPONTxpower()
    txpower = calcTxpower01uW(i2cReadTx)
    if ('-Inf' != txpower) and (-40 < txpower):
        gpontxSoftEn_ok += 1
        print("Round {} GPON  TX: {} dBm, tx soft enable ok ! ".format(cnt, txpower))
        f.write("\nRound {} GPON TX: {} dBm, tx soft enable ok ! ".format(cnt, txpower))
    else:
        gpontxSoftEn_fail += 1
        print("Round {} GPON TX: {} dBm, tx soft enable fail ! ".format(cnt, txpower))
        f.write("\nRound {} GPON TX: {} dBm, tx soft enable fail ! ".format(cnt, txpower))

print("XG tx soft disable is ok total {} times".format(xgtxSoftDis_ok))
f.write("\nXG tx soft disable is ok total {} times".format(xgtxSoftDis_ok))
print("XG tx soft disable is fail total {} times".format(xgtxSoftDis_fail))
f.write("\nXG tx soft disable is fail total {} times".format(xgtxSoftDis_fail))
print("XG tx soft enable is ok total {} times".format(xgtxSoftEn_ok))
f.write("\nXG tx soft enable is ok total {} times".format(xgtxSoftEn_ok))
print("XG tx soft enable is fail total {} times".format(xgtxSoftEn_fail))
f.write("\nXG tx soft enable is fail total {} times".format(xgtxSoftEn_fail))

print("GPON tx soft disable is ok total {} times".format(gpontxSoftDis_ok))
f.write("\nGPON tx soft disable is ok total {} times".format(gpontxSoftDis_ok))
print("GPON tx soft disable is fail total {} times".format(gpontxSoftDis_fail))
f.write("\nGPON tx soft disable is fail total {} times".format(gpontxSoftDis_fail))
print("GPON tx soft enable is ok total {} times".format(gpontxSoftEn_ok))
f.write("\nGPON tx soft enable is ok total {} times".format(gpontxSoftEn_ok))
print("GPON tx soft enable is fail total {} times".format(gpontxSoftEn_fail))
f.write("\nGPON tx soft enable is fail total {} times".format(gpontxSoftEn_fail))
dateTime = time.strptime(time.asctime())
dateTime = "{:4}-{:02}-{:02} {:02}:{:02}:{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
print("\n****************************************************************************")
print("Tx Soft Dis-En stress test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nTx Soft Dis-En stress test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
f.write("\n****************************************************************************")
testEvb.AteAllPowerOff()
f.close()

