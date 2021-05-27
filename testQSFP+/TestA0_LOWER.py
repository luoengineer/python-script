import ctypes
from ctypes import *
import time
import math
import operator
from cmdServ import cmdservdll, Sfp_Factory_Pwd_Entry
from classTestEvb import *
import sys


# user type for password
is_088_Module = 0
is_other_Module = 1
user_password_type = is_other_Module

# Product list
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
def sffToTemperature(temp_msb, temp_lsb):
    if temp_msb & 0x80 == 0x80:
        temp_msb = 127 - (temp_msb & 0x7F) + 1
        temp_msb = -temp_msb
        case_temp = temp_msb + temp_lsb/256
    else:
        case_temp = temp_msb + temp_lsb/256
    return case_temp

def temperatureToSff(temperature):
    temp = math.modf(temperature)
    #print(temp[0], temp[1])
    if temperature < 0:
        temp_msb = int(-temp[1]) + 0x80 - 127
        temp_lsb = 256 - round(256 * (-temp[0]))
    else:
        temp_msb = int(temp[1])
        temp_lsb = round(256 * temp[0])
    return temp_msb, temp_lsb

def sffToVoltage(volt_msb, volt_lsb):
    voltage = (volt_msb * 256 + volt_lsb) * 100 / 1000000
    return voltage

def voltageToSff(voltage):
    #print(voltage)
    assert voltage > 0, "voltage not less than 0V"
    voltage = voltage * 1000000 / 100
    volt_msb = int(voltage) >> 8
    volt_lsb = int(voltage) & 0xFF
    return volt_msb, volt_lsb

def sffToTxbias(txbias_msb, txbias_lsb, tx_unit):
    assert tx_unit == 2 or tx_unit == 4, "txbias unit error!"
    txbias = (txbias_msb * 256 + txbias_lsb) * tx_unit / 1000
    return txbias

def txbiasToSff(txbias, tx_unit):
    assert txbias > 0 , "txbias not less than 0 mA"
    assert tx_unit == 2 or tx_unit == 4, "txbias unit error!"
    txbias = txbias * 1000 / tx_unit
    txbias_msb = int(txbias) >> 8
    txbias_lsb = int(txbias) & 0xFF
    return txbias_msb, txbias_lsb

def sffToTxpower(txpower_msb, txpower_lsb, tx_unit):
    assert tx_unit == 0.1 or tx_unit == 0.2, "txpower unit error!"
    txpower = math.log10((txpower_msb * 256 + txpower_lsb) / 10000) * 10
    return txpower

def txpowerToSff(txpower, tx_unit):
    assert tx_unit == 0.1 or tx_unit == 0.2, "txpower unit error!"
    txpower = math.pow(10, txpower / 10) * 10000
    txpower_msb = int(txpower) >> 8
    txpower_lsb = int(txpower) & 0xFF
    return txpower_msb, txpower_lsb

def sffToRxpower(rxpower_msb, rxpower_lsb):
    rxpower = math.log10((rxpower_msb * 256 + rxpower_lsb) / 10000) * 10
    return rxpower

def rxpowerToSff(rxpower):
    rxpower = math.pow(10, rxpower / 10) * 10000
    rxpower_msb = int(rxpower) >> 8
    rxpower_lsb = int(rxpower) & 0xFF
    return rxpower_msb, rxpower_lsb

#########################################################
#              Open USB Device
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
print("QSFP28 A0 Lower Memory read and write test, start time : {}".format(dateTime))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nQSFP28 A0 Lower Memory read and write test, start time : {}".format(dateTime))
f.write("\n****************************************************************************")
print("{}".format(testTitle))
f.write('\n'+testTitle)

#backup A0 lower memory
A0RawDataBuff = ctypes.c_ubyte*128
A0RawReadByte = A0RawDataBuff()
print("\nA0 Lower raw data:")
f.write("\nA0 Lower raw data: \n")
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[0], 0, 128, A0RawReadByte)
if 0 == Res:
    for item in range(128):
        print("0x{0:X}".format(A0RawReadByte[item]), end=' ')
        f.write(str(hex(A0RawReadByte[item]))+',')
else:
    f.write('read A0 Lower raw data fail.'+'\n')
    print('read A0 Lower raw data fail.' + '\n')
    f.close()
    sys.exit()

#A0[0]
print("\nA0[0] is {0x:02X}, Identifier".format(A0RawReadByte[0]))
f.write("\nA0[0] is {0x:02X}, Identifier ".format(A0RawReadByte[0]))

#A0[1]
if A0RawReadByte[1] == 0:
    print("\nA[1] is {0x:02X}, OK".format(A0RawReadByte[1]))
    f.write("\nA[1] is {0x:02X}, OK".format(A0RawReadByte[1]))
else:
    print("\nA[1] is {0x:02X}, ERROR£¡Reserved byte must be 0".format(A0RawReadByte[1]))
    f.write("\nA[1] is {0x:02X}, ERROR£¡Reserved byte must be 0".format(A0RawReadByte[1]))

#A0[2]
if (A0RawReadByte[2] & 0x01) == 0x00:
    print("\nA0[2] bit 0 is 0, data is ready.")
    f.write("\nA0[2] bit 0 is 0, data is ready.")
else:
    print("\nA0[2] bit 0 is 1, data is not ready.")
    f.write("\nA0[2] bit 0 is 1, data is not ready.")

if (A0RawReadByte[2] & 0x02) == 0x02:
    print("\nA0[2] bit 1 is 1, Digital state of the IntL Interrupt output pin is high level")
    f.write("\nA0[2] bit 1 is 1, Digital state of the IntL Interrupt output pin is high level")
else:
    print("\nA0[2] bit 1 is 0, Digital state of the IntL Interrupt output pin is low level")
    f.write("\nA0[2] bit 1 is 0, Digital state of the IntL Interrupt output pin is low level")

if (A0RawReadByte[2] & 0x04) == 0x04:
    print("\nA0[2] bit 2 is 1,  Flat memory: page 0 only.")
    f.write("\nA0[2] bit 2 is 1,  Flat memory:  page 0 only.")
else:
    print("\nA0[2] bit 2 is 0, Flat memory: paging.")
    f.write("\nA0[2] bit 2 is 0,  Flat memory: paging.")

#A0[3] : LOS
if (A0RawReadByte[3] & 0x80) == 0x80:
    print("\nA0[3] bit 7 is 1,  Tx channel 4 LOS is Latched.")
    f.write("\nA0[3] bit 7 is 1,  Tx channel 4 LOS is Latched.")
else:
    print("\nA0[3] bit 7 is 0,  Tx channel 4 LOS is not Latched.")
    f.write("\nA0[3] bit 7 is 0,  Tx channel 4 LOS is not Latched.")
if (A0RawReadByte[3] & 0x40) == 0x40:
    print("\nA0[3] bit 6 is 1,  Tx channel 3 LOS is Latched.")
    f.write("\nA0[3] bit 6 is 1,  Tx channel 3 LOS is Latched.")
else:
    print("\nA0[3] bit 6 is 0,  Tx channel 3 LOS is not Latched.")
    f.write("\nA0[3] bit 6 is 0,  Tx channel 3 LOS is not Latched.")
if (A0RawReadByte[3] & 0x20) == 0x20:
    print("\nA0[3] bit 5 is 1,  Tx channel 2 LOS is Latched.")
    f.write("\nA0[3] bit 5 is 1,  Tx channel 2 LOS is Latched.")
else:
    print("\nA0[3] bit 5 is 0,  Tx channel 2 LOS is not Latched.")
    f.write("\nA0[3] bit 5 is 0,  Tx channel 2 LOS is not Latched.")
if (A0RawReadByte[3] & 0x10) == 0x10:
    print("\nA0[3] bit 4 is 1,  Tx channel 1 LOS is Latched.")
    f.write("\nA0[3] bit 4 is 1,  Tx channel 1 LOS is Latched.")
else:
    print("\nA0[3] bit 4 is 0,  Tx channel 1 LOS is not Latched.")
    f.write("\nA0[3] bit 4 is 0,  Tx channel 1 LOS is not Latched.")
if (A0RawReadByte[3] & 0x08) == 0x08:
    print("\nA0[3] bit 3 is 1,  Rx channel 4 LOS is Latched.")
    f.write("\nA0[3] bit 3 is 1,  Rx channel 4 LOS is Latched.")
else:
    print("\nA0[3] bit 3 is 0,  Rx channel 4 LOS is not Latched.")
    f.write("\nA0[3] bit 3 is 0,  Rx channel 4 LOS is not Latched.")
if (A0RawReadByte[3] & 0x04) == 0x04:
    print("\nA0[3] bit 2 is 1,  Rx channel 3 LOS is Latched.")
    f.write("\nA0[3] bit 2 is 1,  Rx channel 3 LOS is Latched.")
else:
    print("\nA0[3] bit 2 is 0,  Rx channel 3 LOS is not Latched.")
    f.write("\nA0[3] bit 2 is 0,  Rx channel 3 LOS is not Latched.")
if (A0RawReadByte[3] & 0x02) == 0x02:
    print("\nA0[3] bit 1 is 1,  Rx channel 2 LOS is Latched.")
    f.write("\nA0[3] bit 1 is 1,  Rx channel 2 LOS is Latched.")
else:
    print("\nA0[3] bit 1 is 0,  Rx channel 2 LOS is not Latched.")
    f.write("\nA0[3] bit 1 is 0,  Rx channel 2 LOS is not Latched.")
if (A0RawReadByte[3] & 0x01) == 0x01:
    print("\nA0[3] bit 0 is 1,  Rx channel 1 LOS is Latched.")
    f.write("\nA0[3] bit 0 is 1,  Rx channel 1 LOS is Latched.")
else:
    print("\nA0[3] bit 0 is 0,  Rx channel 1 LOS is not Latched.")
    f.write("\nA0[3] bit 0 is 0,  Rx channel 1 LOS is not Latched.")

#A0[4]: tx fault
if (A0RawReadByte[4] & 0x08) == 0x08:
    print("\nA0[4] bit 3 is 1, TX channel 4 fault.")
    f.write("\nA0[4] bit 3 is 1, TX channel 4 fault.")
if (A0RawReadByte[4] & 0x04) == 0x04:
    print("\nA0[4] bit 2 is 1, TX channel 3 fault.")
    f.write("\nA0[4] bit 2 is 1, TX channel 3 fault.")
if (A0RawReadByte[4] & 0x02) == 0x02:
    print("\nA0[4] bit 1 is 1, TX channel 2 fault.")
    f.write("\nA0[4] bit 1 is 1, TX channel 2 fault.")
if (A0RawReadByte[4] & 0x01) == 0x01:
    print("\nA0[4] bit 0 is 1, TX channel 1 fault.")
    f.write("\nA0[4] bit 0 is 1, TX channel 1 fault.")

#A0[5]
if A0RawReadByte[5] == 0:
    print("\nA[5] is {0x:02X}, OK".format(A0RawReadByte[5]))
    f.write("\nA[5] is {0x:02X}, OK".format(A0RawReadByte[5]))
else:
    print("\nA[5] is {0x:02X}, ERROR£¡Reserved byte must be 0".format(A0RawReadByte[5]))
    f.write("\nA[5] is {0x:02X}, ERROR£¡Reserved byte must be 0".format(A0RawReadByte[5]))

#A0[6]
if (A0RawReadByte[6] & 0x80) == 0x80:
    print("\nA0[6] bit 7 is 1,  high temperature alarm is Latched.")
    f.write("\nA0[6] bit 7 is 1,  high temperature alarm is Latched.")
else:
    print("\nA0[6] bit 7 is 0,  high temperature alarm is not Latched.")
    f.write("\nA0[6] bit 7 is 0,  high temperature alarm is not Latched.")
if (A0RawReadByte[6] & 0x40) == 0x40:
    print("\nA0[6] bit 6 is 1,  low temperature alarm is Latched.")
    f.write("\nA0[6] bit 6 is 1,  low temperature alarm is Latched.")
else:
    print("\nA0[6] bit 6 is 0,  low temperature alarm is not Latched.")
    f.write("\nA0[6] bit 6 is 0,  low temperature alarm is not Latched.")
if (A0RawReadByte[6] & 0x20) == 0x20:
    print("\nA0[6] bit 5 is 1,  high temperature warning is Latched.")
    f.write("\nA0[6] bit 5 is 1,  high temperature warning is Latched.")
else:
    print("\nA0[6] bit 5 is 0,  high temperature warning is not Latched.")
    f.write("\nA0[6] bit 5 is 0,  high temperature warning is not Latched.")
if (A0RawReadByte[6] & 0x10) == 0x10:
    print("\nA0[6] bit 4 is 1,  low temperature warning is Latched.")
    f.write("\nA0[6] bit 4 is 1,  low temperature warning is Latched.")
else:
    print("\nA0[6] bit 4 is 0,  low temperature warning is not Latched.")
    f.write("\nA0[6] bit 4 is 0,  low temperature warning is not Latched.")

#A0[7]
if (A0RawReadByte[7] & 0x80) == 0x80:
    print("\nA0[7] bit 7 is 1,  high vcc alarm is Latched.")
    f.write("\nA0[7] bit 7 is 1,  high vcc alarm is Latched.")
else:
    print("\nA0[7] bit 7 is 0,  high vcc alarm is not Latched.")
    f.write("\nA0[7] bit 7 is 0,  high vcc alarm is not Latched.")
if (A0RawReadByte[7] & 0x40) == 0x40:
    print("\nA0[7] bit 6 is 1,  low vcc alarm is Latched.")
    f.write("\nA0[7] bit 6 is 1,  low vcc alarm is Latched.")
else:
    print("\nA0[7] bit 6 is 0,  low vcc alarm is not Latched.")
    f.write("\nA0[7] bit 6 is 0,  low vcc alarm is not Latched.")
if (A0RawReadByte[7] & 0x20) == 0x20:
    print("\nA0[7] bit 5 is 1,  high vcc warning is Latched.")
    f.write("\nA0[7] bit 5 is 1,  high vcc warning is Latched.")
else:
    print("\nA0[7] bit 5 is 0,  high vcc warning is not Latched.")
    f.write("\nA0[7] bit 5 is 0,  high vcc warning is not Latched.")
if (A0RawReadByte[7] & 0x10) == 0x10:
    print("\nA0[7] bit 4 is 1,  low vcc warning is Latched.")
    f.write("\nA0[7] bit 4 is 1,  low vcc warning is Latched.")
else:
    print("\nA0[7] bit 4 is 0,  low vcc warning is not Latched.")
    f.write("\nA0[7] bit 4 is 0,  low vcc warning is not Latched.")

#A0[8]
print("\nA0[8] is {0x:02X}, Vendor Specific".format(A0RawReadByte[8]))
f.write("\nA0[8] is {0x:02X}, Vendor Specific".format(A0RawReadByte[8]))

#temperature and vcc
case_temp = temperatureToSff(A0RawReadByte[22], A0RawReadByte[23])
print("\ncase temperature £º {:2f} ¡ãC".format(case_temp))
f.write("\ncase temperature £º {:2f} ¡ãC".format(case_temp))

vcc = voltageToSff(A0RawReadByte[26], A0RawReadByte[27])
print("\nvoltage £º {:2f} V".format(vcc))
f.write("\nvoltage £º {:2f} V".format(vcc))

#A0[9]
if (A0RawReadByte[9] & 0x80) == 0x80:
    print("\nA0[9] bit 7 is 1,  RX channel 1 high alarm is Latched.")
    f.write("\nA0[9] bit 7 is 1,  RX channel 1 high alarm is Latched.")
else:
    print("\nA0[9] bit 7 is 0,  RX channel 1 high alarm is not Latched.")
    f.write("\nA0[9] bit 7 is 0,  RX channel 1 high alarm is not Latched.")
if (A0RawReadByte[9] & 0x40) == 0x40:
    print("\nA0[9] bit 6 is 1,  RX channel 1 low alarm is Latched.")
    f.write("\nA0[9] bit 6 is 1,  RX channel 1 low alarm is Latched.")
else:
    print("\nA0[9] bit 6 is 0,  RX channel 1 low alarm is not Latched.")
    f.write("\nA0[9] bit 6 is 0,  RX channel 1 low alarm is not Latched.")
if (A0RawReadByte[9] & 0x20) == 0x20:
    print("\nA0[9] bit 5 is 1,  RX channel 1 high warning is Latched.")
    f.write("\nA0[9] bit 5 is 1,  RX channel 1 high warning is Latched.")
else:
    print("\nA0[9] bit 5 is 0,  RX channel 1 high warning is not Latched.")
    f.write("\nA0[9] bit 5 is 0,  RX channel 1 high warning is not Latched.")
if (A0RawReadByte[9] & 0x10) == 0x10:
    print("\nA0[9] bit 4 is 1,  RX channel 1 low warning is Latched.")
    f.write("\nA0[9] bit 4 is 1,  RX channel 1 low warning is Latched.")
else:
    print("\nA0[9] bit 4 is 0,  RX channel 1 low warning is not Latched.")
    f.write("\nA0[9] bit 4 is 0,  RX channel 1 low warning is not Latched.")
if (A0RawReadByte[9] & 0x08) == 0x08:
    print("\nA0[9] bit 3 is 1,  RX channel 2 high alarm is Latched.")
    f.write("\nA0[9] bit 3 is 1,  RX channel 2 high alarm is Latched.")
else:
    print("\nA0[9] bit 3 is 0,  RX channel 2 high alarm is not Latched.")
    f.write("\nA0[9] bit 3 is 0,  RX channel 2 high alarm is not Latched.")
if (A0RawReadByte[9] & 0x04) == 0x04:
    print("\nA0[9] bit 2 is 1,  RX channel 2 low alarm is Latched.")
    f.write("\nA0[9] bit 2 is 1,  RX channel 2 low alarm is Latched.")
else:
    print("\nA0[9] bit 2 is 0,  RX channel 2 low alarm is not Latched.")
    f.write("\nA0[9] bit 2 is 0,  RX channel 2 low alarm is not Latched.")
if (A0RawReadByte[9] & 0x02) == 0x02:
    print("\nA0[9] bit 1 is 1,  RX channel 2 high warning is Latched.")
    f.write("\nA0[9] bit 1 is 1,  RX channel 2 high warning is Latched.")
else:
    print("\nA0[9] bit 1 is 0,  RX channel 2 high warning is not Latched.")
    f.write("\nA0[9] bit 1 is 0,  RX channel 2 high warning is not Latched.")
if (A0RawReadByte[9] & 0x01) == 0x01:
    print("\nA0[9] bit 0 is 1,  RX channel 2 low warning is Latched.")
    f.write("\nA0[9] bit 0 is 1,  RX channel 2 low warning is Latched.")
else:
    print("\nA0[9] bit 0 is 0,  RX channel 2 low warning is not Latched.")
    f.write("\nA0[9] bit 0 is 0,  RX channel 2 low warning is not Latched.")

#A0[10]
if (A0RawReadByte[10] & 0x80) == 0x80:
    print("\nA0[10] bit 7 is 1,  RX channel 3 high alarm is Latched.")
    f.write("\nA0[10] bit 7 is 1,  RX channel 3 high alarm is Latched.")
else:
    print("\nA0[10] bit 7 is 0,  RX channel 3 high alarm is not Latched.")
    f.write("\nA0[10] bit 7 is 0,  RX channel 3 high alarm is not Latched.")
if (A0RawReadByte[10] & 0x40) == 0x40:
    print("\nA0[10] bit 6 is 1,  RX channel 3 low alarm is Latched.")
    f.write("\nA0[10] bit 6 is 1,  RX channel 3 low alarm is Latched.")
else:
    print("\nA0[10] bit 6 is 0,  RX channel 3 low alarm is not Latched.")
    f.write("\nA0[10] bit 6 is 0,  RX channel 3 low alarm is not Latched.")
if (A0RawReadByte[10] & 0x20) == 0x20:
    print("\nA0[10] bit 5 is 1,  RX channel 3 high warning is Latched.")
    f.write("\nA0[10] bit 5 is 1,  RX channel 3 high warning is Latched.")
else:
    print("\nA0[10] bit 5 is 0,  RX channel 3 high warning is not Latched.")
    f.write("\nA0[10] bit 5 is 0,  RX channel 3 high warning is not Latched.")
if (A0RawReadByte[10] & 0x10) == 0x10:
    print("\nA0[10] bit 4 is 1,  RX channel 3 low warning is Latched.")
    f.write("\nA0[10] bit 4 is 1,  RX channel 3 low warning is Latched.")
else:
    print("\nA0[10] bit 4 is 0,  RX channel 3 low warning is not Latched.")
    f.write("\nA0[10] bit 4 is 0,  RX channel 3 low warning is not Latched.")
if (A0RawReadByte[10] & 0x08) == 0x08:
    print("\nA0[10] bit 3 is 1,  RX channel 4 high alarm is Latched.")
    f.write("\nA0[10] bit 3 is 1,  RX channel 4 high alarm is Latched.")
else:
    print("\nA0[10] bit 3 is 0,  RX channel 4 high alarm is not Latched.")
    f.write("\nA0[10] bit 3 is 0,  RX channel 4 high alarm is not Latched.")
if (A0RawReadByte[10] & 0x04) == 0x04:
    print("\nA0[10] bit 2 is 1,  RX channel 4 low alarm is Latched.")
    f.write("\nA0[10] bit 2 is 1,  RX channel 4 low alarm is Latched.")
else:
    print("\nA0[10] bit 2 is 0,  RX channel 4 low alarm is not Latched.")
    f.write("\nA0[10] bit 2 is 0,  RX channel 4 low alarm is not Latched.")
if (A0RawReadByte[10] & 0x02) == 0x02:
    print("\nA0[10] bit 1 is 1,  RX channel 4 high warning is Latched.")
    f.write("\nA0[10] bit 1 is 1,  RX channel 4 high warning is Latched.")
else:
    print("\nA0[10] bit 1 is 0,  RX channel 4 high warning is not Latched.")
    f.write("\nA0[10] bit 1 is 0,  RX channel 4 high warning is not Latched.")
if (A0RawReadByte[10] & 0x01) == 0x01:
    print("\nA0[10] bit 0 is 1,  RX channel 4 low warning is Latched.")
    f.write("\nA0[10] bit 0 is 1,  RX channel 4 low warning is Latched.")
else:
    print("\nA0[10] bit 0 is 0,  RX channel 4 low warning is not Latched.")
    f.write("\nA0[10] bit 0 is 0,  RX channel 4 low warning is not Latched.")

#A0[11]
if (A0RawReadByte[11] & 0x80) == 0x80:
    print("\nA0[11] bit 7 is 1,  TX bias channel 1 high alarm is Latched.")
    f.write("\nA0[11] bit 7 is 1,  TX bias channel 1 high alarm is Latched.")
else:
    print("\nA0[11] bit 7 is 0,  TX bias channel 1 high alarm is not Latched.")
    f.write("\nA0[11] bit 7 is 0,  TX bias channel 1 high alarm is not Latched.")
if (A0RawReadByte[11] & 0x40) == 0x40:
    print("\nA0[11] bit 6 is 1,  TX bias channel 1 low alarm is Latched.")
    f.write("\nA0[11] bit 6 is 1,  TX bias channel 1 low alarm is Latched.")
else:
    print("\nA0[11] bit 6 is 0,  TX bias channel 1 low alarm is not Latched.")
    f.write("\nA0[11] bit 6 is 0,  TX bias channel 1 low alarm is not Latched.")
if (A0RawReadByte[11] & 0x20) == 0x20:
    print("\nA0[11] bit 5 is 1,  TX bias channel 1 high warning is Latched.")
    f.write("\nA0[11] bit 5 is 1,  TX bias channel 1 high warning is Latched.")
else:
    print("\nA0[11] bit 5 is 0,  TX bias channel 1 high warning is not Latched.")
    f.write("\nA0[11] bit 5 is 0,  TX bias channel 1 high warning is not Latched.")
if (A0RawReadByte[11] & 0x10) == 0x10:
    print("\nA0[11] bit 4 is 1,  TX bias channel 1 low warning is Latched.")
    f.write("\nA0[11] bit 4 is 1,  TX bias channel 1 low warning is Latched.")
else:
    print("\nA0[11] bit 4 is 0,  TX bias channel 1 low warning is not Latched.")
    f.write("\nA0[11] bit 4 is 0,  TX bias channel 1 low warning is not Latched.")
if (A0RawReadByte[11] & 0x08) == 0x08:
    print("\nA0[11] bit 3 is 1,  TX bias channel 2 high alarm is Latched.")
    f.write("\nA0[11] bit 3 is 1,  TX bias channel 2 high alarm is Latched.")
else:
    print("\nA0[11] bit 3 is 0,  TX bias channel 2 high alarm is not Latched.")
    f.write("\nA0[11] bit 3 is 0,  TX bias channel 2 high alarm is not Latched.")
if (A0RawReadByte[11] & 0x04) == 0x04:
    print("\nA0[11] bit 2 is 1,  TX bias channel 2 low alarm is Latched.")
    f.write("\nA0[11] bit 2 is 1,  TX bias channel 2 low alarm is Latched.")
else:
    print("\nA0[11] bit 2 is 0,  TX bias channel 2 low alarm is not Latched.")
    f.write("\nA0[11] bit 2 is 0,  TX bias channel 2 low alarm is not Latched.")
if (A0RawReadByte[11] & 0x02) == 0x02:
    print("\nA0[11] bit 1 is 1,  TX bias channel 2 high warning is Latched.")
    f.write("\nA0[11] bit 1 is 1,  TX bias channel 2 high warning is Latched.")
else:
    print("\nA0[11] bit 1 is 0,  TX bias channel 2 high warning is not Latched.")
    f.write("\nA0[11] bit 1 is 0,  TX bias channel 2 high warning is not Latched.")
if (A0RawReadByte[11] & 0x01) == 0x01:
    print("\nA0[11] bit 0 is 1,  TX bias channel 2 low warning is Latched.")
    f.write("\nA0[11] bit 0 is 1,  TX bias channel 2 low warning is Latched.")
else:
    print("\nA0[11] bit 0 is 0,  TX bias channel 2 low warning is not Latched.")
    f.write("\nA0[11] bit 0 is 0,  TX bias channel 2 low warning is not Latched.")

#A0[12]
if (A0RawReadByte[12] & 0x80) == 0x80:
    print("\nA0[12] bit 7 is 1,  TX bias channel 3 high alarm is Latched.")
    f.write("\nA0[12] bit 7 is 1,  TX bias channel 3 high alarm is Latched.")
else:
    print("\nA0[12] bit 7 is 0,  TX bias channel 3 high alarm is not Latched.")
    f.write("\nA0[12] bit 7 is 0,  TX bias channel 3 high alarm is not Latched.")
if (A0RawReadByte[12] & 0x40) == 0x40:
    print("\nA0[12] bit 6 is 1,  TX bias channel 3 low alarm is Latched.")
    f.write("\nA0[12] bit 6 is 1,  TX bias channel 3 low alarm is Latched.")
else:
    print("\nA0[12] bit 6 is 0,  TX bias channel 3 low alarm is not Latched.")
    f.write("\nA0[12] bit 6 is 0,  TX bias channel 3 low alarm is not Latched.")
if (A0RawReadByte[12] & 0x20) == 0x20:
    print("\nA0[12] bit 5 is 1,  TX bias channel 3 high warning is Latched.")
    f.write("\nA0[12] bit 5 is 1,  TX bias channel 3 high warning is Latched.")
else:
    print("\nA0[12] bit 5 is 0,  TX bias channel 3 high warning is not Latched.")
    f.write("\nA0[12] bit 5 is 0,  TX bias channel 3 high warning is not Latched.")
if (A0RawReadByte[12] & 0x10) == 0x10:
    print("\nA0[12] bit 4 is 1,  TX bias channel 3 low warning is Latched.")
    f.write("\nA0[12] bit 4 is 1,  TX bias channel 3 low warning is Latched.")
else:
    print("\nA0[12] bit 4 is 0,  TX bias channel 3 low warning is not Latched.")
    f.write("\nA0[12] bit 4 is 0,  TX bias channel 3 low warning is not Latched.")
if (A0RawReadByte[12] & 0x08) == 0x08:
    print("\nA0[12] bit 3 is 1,  TX bias channel 4 high alarm is Latched.")
    f.write("\nA0[12] bit 3 is 1,  TX bias channel 4 high alarm is Latched.")
else:
    print("\nA0[12] bit 3 is 0,  TX bias channel 4 high alarm is not Latched.")
    f.write("\nA0[12] bit 3 is 0,  TX bias channel 4 high alarm is not Latched.")
if (A0RawReadByte[12] & 0x04) == 0x04:
    print("\nA0[12] bit 2 is 1,  TX bias channel 4 low alarm is Latched.")
    f.write("\nA0[12] bit 2 is 1,  TX bias channel 4 low alarm is Latched.")
else:
    print("\nA0[12] bit 2 is 0,  TX bias channel 4 low alarm is not Latched.")
    f.write("\nA0[12] bit 2 is 0,  TX bias channel 4 low alarm is not Latched.")
if (A0RawReadByte[12] & 0x02) == 0x02:
    print("\nA0[12] bit 1 is 1,  TX bias channel 4 high warning is Latched.")
    f.write("\nA0[12] bit 1 is 1,  TX bias channel 4 high warning is Latched.")
else:
    print("\nA0[12] bit 1 is 0,  TX bias channel 4 high warning is not Latched.")
    f.write("\nA0[12] bit 1 is 0,  TX bias channel 4 high warning is not Latched.")
if (A0RawReadByte[12] & 0x01) == 0x01:
    print("\nA0[12] bit 0 is 1,  TX bias channel 4 low warning is Latched.")
    f.write("\nA0[12] bit 0 is 1,  TX bias channel 4 low warning is Latched.")
else:
    print("\nA0[12] bit 0 is 0,  TX bias channel 4 low warning is not Latched.")
    f.write("\nA0[12] bit 0 is 0,  TX bias channel 4 low warning is not Latched.")

#A0[13-18]
for item in range(len(18-13)):
    offset = item + 13
    if A0RawReadByte[offset] == 0:
        print("\nA0[{:d}] is {0x:02X}, OK".format(offset, A0RawReadByte[offset]))
        f.write("\nA0[;d] is {0x:02X}, OK".format(offset, A0RawReadByte[offset]))
    else:
        print("\nA0[{:d}] is {0x:02X}, ERROR£¡Reserved byte must be 0".format(offset, A0RawReadByte[offset]))
        f.write("\nA0[{:d}] is {0x:02X}, ERROR£¡Reserved byte must be 0".format(offset, A0RawReadByte[offset]))

#A0[19-21]
for item in range(len(21-19)):
    offset = item + 19
    print("\nA0[{:d}] is {0x:02X}, Vendor Specific".format(offset, A0RawReadByte[offset]))
    f.write("\nA0[{:d}] is {0x:02X}, Vendor Specific".format(offset, A0RawReadByte[offset]))

#A0[22-23]
temperature = sffToTemperature(A0RawReadByte[22], A0RawReadByte[23])
print("\nModule temperature : {:2f} ¡ãC".format(temperature))
f.write("\nModule temperature : {:2f} ¡ãC".format(temperature))

voltage = sffToVoltage(A0RawReadByte[26], A0RawReadByte[27])
print("\nMoudle voltage : {:2f}".format(voltage))
f.write("\nMoudle voltage : {:2f}".format(voltage))

#A0[24-25]
for item in range(len(25-24)):
    offset = item + 24
    if A0RawReadByte[offset] == 0:
        print("\nA0[{:d}] is {0x:02X}, OK".format(offset, A0RawReadByte[offset]))
        f.write("\nA0[;d] is {0x:02X}, OK".format(offset, A0RawReadByte[offset]))
    else:
        print("\nA0[{:d}] is {0x:02X}, ERROR£¡Reserved byte must be 0".format(offset, A0RawReadByte[offset]))
        f.write("\nA0[{:d}] is {0x:02X}, ERROR£¡Reserved byte must be 0".format(offset, A0RawReadByte[offset]))

#A0[28-29]
for item in range(len(29-28)):
    offset = item + 28
    if A0RawReadByte[offset] == 0:
        print("\nA0[{:d}] is {0x:02X}, OK".format(offset, A0RawReadByte[offset]))
        f.write("\nA0[;d] is {0x:02X}, OK".format(offset, A0RawReadByte[offset]))
    else:
        print("\nA0[{:d}] is {0x:02X}, ERROR£¡Reserved byte must be 0".format(offset, A0RawReadByte[offset]))
        f.write("\nA0[{:d}] is {0x:02X}, ERROR£¡Reserved byte must be 0".format(offset, A0RawReadByte[offset]))

#A0[30-33]
for item in range(len(33-30)):
    offset = item + 30
    print("\nA0[{:d}] is {0x:02X}, Vendor Specific".format(offset, A0RawReadByte[offset]))
    f.write("\nA0[{:d}] is {0x:02X}, Vendor Specific".format(offset, A0RawReadByte[offset]))

#A0 page0[220]
print("\nA0[220]:")
f.write("\nA0[220]: \n")
rxpow_type = ctypes.c_ubyte
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[0], 220, 1, byref(rxpow_type))
if 0 == Res:
    print("0x{0:X}".format(rxpow_type))
    f.write(str(hex(rxpow_type)))
else:
    f.write('read A0[220] fail.'+'\n')
    print('read A0[220] fail.' + '\n')
    f.close()
    sys.exit()
if rxpow_type & 0x08 == 0x08:
    print("\nReceived power measurements type is Average Power.")
    f.write("\nReceived power measurements type is Average Power.")
else:
    print("\nReceived power measurements type is OMA.")
    f.write("\nReceived power measurements type is OMA.")

#A0[34-41]rxpow
rx1_power = rxpowerToSff(A0RawReadByte[34], A0RawReadByte[35])
print("\nRX channel 1 £º {:2f} dBm".format(rx1_power))
f.write("\nRX channel 1 £º {:2f} dBm".format(rx1_power))
rx2_power = rxpowerToSff(A0RawReadByte[36], A0RawReadByte[37])
print("\nRX channel 2 £º {:2f} dBm".format(rx2_power))
f.write("\nRX channel 2 £º {:2f} dBm".format(rx2_power))
rx3_power = rxpowerToSff(A0RawReadByte[38], A0RawReadByte[39])
print("\nRX channel 3 £º {:2f} dBm".format(rx3_power))
f.write("\nRX channel 3 £º {:2f} dBm".format(rx3_power))
rx4_power = rxpowerToSff(A0RawReadByte[40], A0RawReadByte[41])
print("\nRX channel 4 £º {:2f} dBm".format(rx4_power))
f.write("\nRX channel 4 £º {:2f} dBm".format(rx4_power))
#A0[42-49] txbias
tx1_bias = txbiasToSff(A0RawReadByte[42], A0RawReadByte[43], 2)
print("\nTX bias channel 1 £º {:2f} mA".format(tx1_bias))
f.write("\nTX bias channel 1 £º {:2f} mA".format(tx1_bias))
tx2_bias = txbiasToSff(A0RawReadByte[44], A0RawReadByte[45], 2)
print("\nTX bias channel 2 £º {:2f} mA".format(tx2_bias))
f.write("\nTX bias channel 2 £º {:2f} mA".format(tx2_bias))
tx3_bias = txbiasToSff(A0RawReadByte[46], A0RawReadByte[47], 2)
print("\nTX bias channel 3 £º {:2f} mA".format(tx3_bias))
f.write("\nTX bias channel 3 £º {:2f} mA".format(tx3_bias))
tx4_bias = txbiasToSff(A0RawReadByte[48], A0RawReadByte[49], 2)
print("\nTX bias channel 4 £º {:2f} mA".format(tx4_bias))
f.write("\nTX bias channel 4 £º {:2f} mA".format(tx4_bias))

#A0[50-57]Reserved channel monitor set 3
for item in range(len(57-50)):
    offset = item + 50
    if A0RawReadByte[offset] == 0:
        print("\nA0[{:d}] is {0x:02X}, OK".format(offset, A0RawReadByte[offset]))
        f.write("\nA0[;d] is {0x:02X}, OK".format(offset, A0RawReadByte[offset]))
    else:
        print("\nA0[{:d}] is {0x:02X}, ERROR£¡Reserved byte must be 0".format(offset, A0RawReadByte[offset]))
        f.write("\nA0[{:d}] is {0x:02X}, ERROR£¡Reserved byte must be 0".format(offset, A0RawReadByte[offset]))

#A0[58-65]Reserved channel monitor set 4
for item in range(len(58-65)):
    offset = item + 58
    if A0RawReadByte[offset] == 0:
        print("\nA0[{:d}] is {0x:02X}, OK".format(offset, A0RawReadByte[offset]))
        f.write("\nA0[;d] is {0x:02X}, OK".format(offset, A0RawReadByte[offset]))
    else:
        print("\nA0[{:d}] is {0x:02X}, ERROR£¡Reserved byte must be 0".format(offset, A0RawReadByte[offset]))
        f.write("\nA0[{:d}] is {0x:02X}, ERROR£¡Reserved byte must be 0".format(offset, A0RawReadByte[offset]))

#A0[66-81]
for item in range(len(68-61)):
    offset = item + 61
    print("\nA0[{:d}] is {0x:02X}, Vendor Specific".format(offset, A0RawReadByte[offset]))
    f.write("\nA0[{:d}] is {0x:02X}, Vendor Specific".format(offset, A0RawReadByte[offset]))

#A0[82-85]Reserved channel monitor set 4
for item in range(len(85-82)):
    offset = item + 82
    if A0RawReadByte[offset] == 0:
        print("\nA0[{:d}] is {0x:02X}, OK".format(offset, A0RawReadByte[offset]))
        f.write("\nA0[;d] is {0x:02X}, OK".format(offset, A0RawReadByte[offset]))
    else:
        print("\nA0[{:d}] is {0x:02X}, ERROR£¡Reserved byte must be 0".format(offset, A0RawReadByte[offset]))
        f.write("\nA0[{:d}] is {0x:02X}, ERROR£¡Reserved byte must be 0".format(offset, A0RawReadByte[offset]))

#A0[86]software disable
if A0RawReadByte[86] & 0x01 == 0x01:
    print("\nA0[86] bit 0 is 1, TX channel 1 software disable.")
    f.write("\nA0[4] bit 0 is 1, TX channel 1 software disable.")
if A0RawReadByte[86] & 0x02 == 0x02:
    print("\nA0[86] bit 1 is 1, TX channel 2 software disable.")
    f.write("\nA0[4] bit 1 is 1, TX channel 2 software disable.")
if A0RawReadByte[86] & 0x04 == 0x04:
    print("\nA0[86] bit 2 is 1, TX channel 3 software disable.")
    f.write("\nA0[4] bit 2 is 1, TX channel 3 software disable.")
if A0RawReadByte[86] & 0x08 == 0x08:
    print("\nA0[86] bit 3 is 1, TX channel 4 software disable.")
    f.write("\nA0[4] bit 3 is 1, TX channel 4 software disable.")

#A0 page0[195]
print("\nA0[195]:")
f.write("\nA0[195]: \n")
A0_195 = ctypes.c_ubyte
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[0], 195, 1, byref(A0_195))
if 0 == Res:
    print("0x{0:02X}".format(A0_195))
    f.write("0x{0:02X}".format(A0_195))
else:
    f.write('read A0[195] fail.'+'\n')
    print('read A0[195] fail.' + '\n')
    f.close()
    sys.exit()
A0_195_bit5 = True, A0_195 & 0x20 == 0x20, False

#A0 page0[221]
print("\nA0[221]:")
f.write("\nA0[221]: \n")
Enhanced_Options = ctypes.c_ubyte
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[0], 221, 1, byref(Enhanced_Options))
if 0 == Res:
    print("0x{0:X}".format(Enhanced_Options))
    f.write(str(hex(Enhanced_Options)))
else:
    f.write('read A0[221] fail.'+'\n')
    print('read A0[221] fail.' + '\n')
    f.close()
    sys.exit()
Rate_Selection = True, Enhanced_Options & 0x08 == 0x08, False
Application_select_table = True, Enhanced_Options & 0x04, False

if A0RawReadByte == False and Rate_Selection == False and Application_select_table == False
    print("\n Provide no support for rate selection.")
    f.write("\n Provide no support for rate selection.")

#A0 page0[141]
print("\nA0[141]:")
f.write("\nA0[141]: \n")
Extended_RateSelect = ctypes.c_ubyte
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[0], 141, 1, byref(Extended_RateSelect))
if 0 == Res:
    print("0x{0:X}".format(Extended_RateSelect))
    f.write(str(hex(Extended_RateSelect)))
else:
    f.write('read A0[141] fail.'+'\n')
    print('read A0[141] fail.' + '\n')
    f.close()
    sys.exit()
if Extended_RateSelect & 0x01 == 0x01 and Rate_Selection == True:
    print("\nRate selection using extended rate select.")
    f.write("\nRate selection using extended rate select.")

#A0[87-88]
def Ext_Rate_Select(rate_sel = 3):
    rate_sel &= 0x03
    if rate_sel == 0:
        return "Optimized for data rates less than 2.2Gb/s"
    elif rate_sel  == 1:
        return "Optimized for data rates from 2.2 up to 6.6 Gb/s"
    elif rate_sel == 2:
        return "Optimized for 6.6 Gb/s data rates and above"
    else:
        return "Reserved"
print("\nRx4_Rate_select is {:s}".format(Ext_Rate_Select((A0RawReadByte[87]&0xC0)>>6)))
print("\nRx3_Rate_select is {:s}".format(Ext_Rate_Select((A0RawReadByte[87]&0x30)>>4)))
print("\nRx2_Rate_select is {:s}".format(Ext_Rate_Select((A0RawReadByte[87]&0x0C)>>2)))
print("\nRx1_Rate_select is {:s}".format(Ext_Rate_Select((A0RawReadByte[87]&0x03)>>0)))
print("\nTx4_Rate_select is {:s}".format(Ext_Rate_Select((A0RawReadByte[88]&0xC0)>>6)))
print("\nTx3_Rate_select is {:s}".format(Ext_Rate_Select((A0RawReadByte[88]&0x30)>>4)))
print("\nTx2_Rate_select is {:s}".format(Ext_Rate_Select((A0RawReadByte[88]&0x0C)>>2)))
print("\nTx1_Rate_select is {:s}".format(Ext_Rate_Select((A0RawReadByte[88]&0x03)>>0)))
f.write("\nRx4_Rate_select is {:s}".format(Ext_Rate_Select((A0RawReadByte[87]&0xC0)>>6)))
f.write("\nRx3_Rate_select is {:s}".format(Ext_Rate_Select((A0RawReadByte[87]&0x30)>>4)))
f.write("\nRx2_Rate_select is {:s}".format(Ext_Rate_Select((A0RawReadByte[87]&0x0C)>>2)))
f.write("\nRx1_Rate_select is {:s}".format(Ext_Rate_Select((A0RawReadByte[87]&0x03)>>0)))
f.write("\nTx4_Rate_select is {:s}".format(Ext_Rate_Select((A0RawReadByte[88]&0xC0)>>6)))
f.write("\nTx3_Rate_select is {:s}".format(Ext_Rate_Select((A0RawReadByte[88]&0x30)>>4)))
f.write("\nTx2_Rate_select is {:s}".format(Ext_Rate_Select((A0RawReadByte[88]&0x0C)>>2)))
f.write("\nTx1_Rate_select is {:s}".format(Ext_Rate_Select((A0RawReadByte[88]&0x03)>>0)))

if Application_select_table == True:
    print("\nRate selection with application select tables.")
    f.write("\nRate selection with application select tables.")

#A0[89-92]
def Application_select(app_sel = 0):
    control_mode = (app_sel & 0x80)>>7
    module_behavior = (app_sel & 0x3F)
    if module_behavior == 0x3F:
        print("\nTable Select TS = 111111b, is invalid.")
        f.write("\nTable Select TS = 111111b, is invalid.")
    application_select = ""
    if control_mode == 1:
        application_select = "Application select is " + str(hex(module_behavior))
    elif control_mode == 0:
        application_select = "Extended rate selection"
    return application_select
print("\nRx4_Application_Select is {:s}".format(Application_select(A0RawReadByte[89])))
print("\nRx3_Application_Select is {:s}".format(Application_select(A0RawReadByte[90])))
print("\nRx2_Application_Select is {:s}".format(Application_select(A0RawReadByte[91])))
print("\nRx1_Application_Select is {:s}".format(Application_select(A0RawReadByte[92])))
f.write("\nRx4_Application_Select is {:s}".format(Application_select(A0RawReadByte[89])))
f.write("\nRx3_Application_Select is {:s}".format(Application_select(A0RawReadByte[90])))
f.write("\nRx2_Application_Select is {:s}".format(Application_select(A0RawReadByte[91])))
f.write("\nRx1_Application_Select is {:s}".format(Application_select(A0RawReadByte[92])))
#A0[94-97]
print("\nTx4_Application_Select is {:s}".format(Application_select(A0RawReadByte[94])))
print("\nTx3_Application_Select is {:s}".format(Application_select(A0RawReadByte[95])))
print("\nTx2_Application_Select is {:s}".format(Application_select(A0RawReadByte[96])))
print("\nTx1_Application_Select is {:s}".format(Application_select(A0RawReadByte[97])))
f.write("\nTx4_Application_Select is {:s}".format(Application_select(A0RawReadByte[94])))
f.write("\nTx3_Application_Select is {:s}".format(Application_select(A0RawReadByte[95])))
f.write("\nTx2_Application_Select is {:s}".format(Application_select(A0RawReadByte[96])))
f.write("\nTx1_Application_Select is {:s}".format(Application_select(A0RawReadByte[97])))

#A0[93]
print("\nPower set is {:d}".format((A0RawReadByte[93]&0x02)>>1))
f.write("\nPower set is {:d}".format((A0RawReadByte[93]&0x02)>>1))
print("\nPower override is {:d}".format(A0RawReadByte[93]&0x01))
f.write("\nPower override is {:d}".format(A0RawReadByte[93]&0x01))

#A0[98-99]
for item in range(len(99-98)):
    offset = item + 98
    if A0RawReadByte[offset] == 0:
        print("\nA0[{:d}] is {0x:02X}, OK".format(offset, A0RawReadByte[offset]))
        f.write("\nA0[;d] is {0x:02X}, OK".format(offset, A0RawReadByte[offset]))
    else:
        print("\nA0[{:d}] is {0x:02X}, ERROR£¡Reserved byte must be 0".format(offset, A0RawReadByte[offset]))
        f.write("\nA0[{:d}] is {0x:02X}, ERROR£¡Reserved byte must be 0".format(offset, A0RawReadByte[offset]))
#A0[100]
print("\nMask Tx LOS is {:d}".format((A0RawReadByte[100]&0xF0)>>4))
f.write("\nMask Tx LOS is {:d}".format((A0RawReadByte[100]&0xF0)>>4))
print("\nMask Rx LOS is {:d}".format((A0RawReadByte[100]&0x0F)>>0))
f.write()"\nMask Rx LOS is {:d}".format((A0RawReadByte[100]&0x0F)>>0)

#A0[101]
print("\nMask Tx Fault is {:d}".format((A0RawReadByte[101]&0x0F)>>0))
f.write()"\nMask Tx Fault is {:d}".format((A0RawReadByte[101]&0x0F)>>0)

#A0[102]
offset = 102
if A0RawReadByte[offset] == 0:
    print("\nA0[{:d}] is {0x:02X}, OK".format(offset, A0RawReadByte[offset]))
    f.write("\nA0[;d] is {0x:02X}, OK".format(offset, A0RawReadByte[offset]))
else:
    print("\nA0[{:d}] is {0x:02X}, ERROR£¡Reserved byte must be 0".format(offset, A0RawReadByte[offset]))
    f.write("\nA0[{:d}] is {0x:02X}, ERROR£¡Reserved byte must be 0".format(offset, A0RawReadByte[offset]))

#A0[103]
print("\nMask temperature alarm and warning is {:d}".format((A0RawReadByte[103]&0xF0)>>4))
f.write("\nMask temperature alarm and warning is {:d}".format((A0RawReadByte[103]&0xF0)>>4))
print("\nMask MInitialization complete flag is {:d}".format((A0RawReadByte[103]&0x01)>>0))
f.write("\nMask MInitialization complete flag is {:d}".format((A0RawReadByte[103]&0x01)>>0))

#A0[104]
print("\nMask VCC alarm and warning is {:d}".format((A0RawReadByte[104]&0xF0)>>4))
f.write("\nMask VCC alarm and warning is {:d}".format((A0RawReadByte[104]&0xF0)>>4))

#A0[105-106]
for item in range(len(106-105)):
    offset = item + 105
    print("\nA0[{:d}] is {0x:02X}, Vendor Specific".format(offset, A0RawReadByte[offset]))
    f.write("\nA0[{:d}] is {0x:02X}, Vendor Specific".format(offset, A0RawReadByte[offset]))

#A0[107-118]
for item in range(len(118-107)):
    offset = item + 107
    if A0RawReadByte[offset] == 0:
        print("\nA0[{:d}] is {0x:02X}, OK".format(offset, A0RawReadByte[offset]))
        f.write("\nA0[;d] is {0x:02X}, OK".format(offset, A0RawReadByte[offset]))
    else:
        print("\nA0[{:d}] is {0x:02X}, ERROR£¡Reserved byte must be 0".format(offset, A0RawReadByte[offset]))
        f.write("\nA0[{:d}] is {0x:02X}, ERROR£¡Reserved byte must be 0".format(offset, A0RawReadByte[offset]))
#A0[119-122]
print("\nPassword Change Entry Area is 0x{:02X},0x{:02X},0x{:02X},0x{:02X}".format(A0RawReadByte[119],A0RawReadByte[120],A0RawReadByte[121],A0RawReadByte[122]))
f.write("\nPassword Change Entry Area is 0x{:02X},0x{:02X},0x{:02X},0x{:02X}".format(A0RawReadByte[119],A0RawReadByte[120],A0RawReadByte[121],A0RawReadByte[122]))
#A0[123-126]
print("\nPassword Entry Area is 0x{:02X},0x{:02X},0x{:02X},0x{:02X}".format(A0RawReadByte[123],A0RawReadByte[124],A0RawReadByte[125],A0RawReadByte[126]))
f.write("\nPassword Entry Area is 0x{:02X},0x{:02X},0x{:02X},0x{:02X}".format(A0RawReadByte[123],A0RawReadByte[124],A0RawReadByte[125],A0RawReadByte[126]))
#A0[127]
print("\nPage Select is 0x{:02X}".format(A0RawReadByte[127]))
f.write("\nPage Select is 0x{:02X}".format(A0RawReadByte[127]))

#restore A0 Lower memory
testEvb.AteAllPowerOn()
time.sleep(2)
Sfp_Factory_Pwd_Entry(user_password_type)
time.sleep(1)
testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[0], 0, 128, byref(A0RawReadByte))
time.sleep(1)
A0ReadDataBuff = ctypes.c_ubyte * 128
randomReadByte = A0ReadDataBuff()
testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[0], 0, 128, randomReadByte)
if True == operator.eq(A0RawDataBuff, A0ReadDataBuff):
    f.write('A0 Lower memory restore success.' + '\n')
    print("A0 Lower memory restore success.")
else:
    f.write('A0 Lower memory restore fail.' + '\n')
    print("A0 Lower memory restore fail.")

dateTime = time.strptime(time.asctime())
dateTime = "{:4}-{:02}-{:02} {:02}:{:02}:{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
print("\n****************************************************************************")
print("QSFP28 A0 Lower Memory read and write test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nQSFP28 A0 Lower Memory read and write test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
f.write("\n****************************************************************************")
#testEvb.AteAllPowerOff()
f.close()

