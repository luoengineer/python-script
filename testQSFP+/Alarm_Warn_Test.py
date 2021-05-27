import ctypes
from ctypes import *
import time
import random
import operator
from cmdServ import cmdservdll,Sfp_Factory_Pwd_Entry
from classTestEvb import *
import sys
import math
import os

#Test times
#wr_and_rd_times  = 5
run_time_second = 30 * 1  # unit : s
# user type for password
is_088_Module = 0
is_other_Module = 1
user_password_type = is_other_Module

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
Alarm_and_Warning_threshold_Byte = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, \
                                    20, 22, 24, 26, 28, 30, 32, 34, 36, 38]
Alarm_and_Warning_Flag_Bits_Byte = [112, 113, 114, 115, 116, 117]

def read_rxpower():
    A2RawDataBuff = ctypes.c_ubyte * 2
    A2RawReadByte = A2RawDataBuff()
    print("Read A2 104-105(Rxpower), 099 must be 0x0000  ")
    f.write("Read A2 104-105(Rxpower), 099 must be 0x0000 \n")
    Res = 0xFF
    Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 104, 2, A2RawReadByte)
    if 0 == Res:
        if (0 == A2RawReadByte[0]) and (0 == A2RawReadByte[1]):
            print(
                'A2[{}-{}](Rxpower)=0x{:0>2X},0x{:0>2X}, {}'.format(104, 105, A2RawReadByte[0], A2RawReadByte[1], 'OK'))
            f.write(
                'A2[{}-{}](Rxpower)=0x{:0>2X},0x{:0>2X}, {}'.format(104, 105, A2RawReadByte[0], A2RawReadByte[1], 'OK'))
        else:
            print('A2[{}-{}](Rxpower)=0x{:0>2X},0x{:0>2X}, {}'.format(104, 105, A2RawReadByte[0], A2RawReadByte[1],
                                                                      'Error'))
            f.write('A2[{}-{}](Rxpower)=0x{:0>2X},0x{:0>2X}, {}'.format(104, 105, A2RawReadByte[0], A2RawReadByte[1],
                                                                        'Error'))
    else:
        print('Read A2 104-105 fail.')
        f.write('Read A2 104-105 fail.')
        return 'fail'
        #f.close()
        #sys.exit()

def sff8472ToTemperature(temp_msb, temp_lsb):
    if temp_msb & 0x80 == 0x80:
        temp_msb = 127 - (temp_msb & 0x7F) + 1
        temp_msb = -temp_msb
        case_temp = temp_msb + temp_lsb/256
    else:
        case_temp = temp_msb + temp_lsb/256
    return case_temp

def temperatureToSff8472(temperature):
    temp = math.modf(temperature)
    #print(temp[0], temp[1])
    if temperature < 0:
        temp_msb = int(-temp[1]) + 0x80 - 127
        temp_lsb = 256 - round(256 * (-temp[0]))
    else:
        temp_msb = int(temp[1])
        temp_lsb = round(256 * temp[0])
    return temp_msb, temp_lsb

def sff8472ToVoltage(volt_msb, volt_lsb):
    voltage = (volt_msb * 256 + volt_lsb) * 100 / 1000000
    return voltage

def voltageToSff8472(voltage):
    #print(voltage)
    assert voltage > 0, "voltage not less than 0V"
    voltage = voltage * 1000000 / 100
    volt_msb = int(voltage) >> 8
    volt_lsb = int(voltage) & 0xFF
    return volt_msb, volt_lsb

def sff8472ToTxbias(txbias_msb, txbias_lsb, tx_unit):
    assert tx_unit == 2 or tx_unit == 4, "txbias unit error!"
    txbias = (txbias_msb * 256 + txbias_lsb) * tx_unit / 1000
    return txbias

def txbiasToSff8472(txbias, tx_unit):
    assert txbias > 0 , "txbias not less than 0 mA"
    assert tx_unit == 2 or tx_unit == 4, "txbias unit error!"
    txbias = txbias * 1000 / tx_unit
    txbias_msb = int(txbias) >> 8
    txbias_lsb = int(txbias) & 0xFF
    return txbias_msb, txbias_lsb

def sff8472ToTxpower(txpower_msb, txpower_lsb, tx_unit):
    assert tx_unit == 0.1 or tx_unit == 0.2, "txpower unit error!"
    txpower = math.log10((txpower_msb * 256 + txpower_lsb) / 10000) * 10
    return txpower

def txpowerToSff8472(txpower, tx_unit):
    assert tx_unit == 0.1 or tx_unit == 0.2, "txpower unit error!"
    txpower = math.pow(10, txpower / 10) * 10000
    txpower_msb = int(txpower) >> 8
    txpower_lsb = int(txpower) & 0xFF
    return txpower_msb, txpower_lsb



def read_ddmi_case_temperature():
    A2RawDataBuff = ctypes.c_ubyte * 2
    A2RawReadByte = A2RawDataBuff()
    Res = 0xFF
    Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 96, 2, A2RawReadByte)
    if 0 == Res:
        print("Read A2 96-97(case temperature) = 0x{:0>2X},0x{:0>2X} ".format(A2RawReadByte[0], A2RawReadByte[1]))
        f.write("\nRead A2 96-97(case temperature) = 0x{:0>2X},0x{:0>2X} ".format(A2RawReadByte[0], A2RawReadByte[1]))
        caseTemp = sff8472ToTemperature(A2RawReadByte[0], A2RawReadByte[1])
        print("case temperature : {} °C".format(caseTemp))
        f.write("\ncase temperature : {} °C".format(caseTemp))
        return 'ok', caseTemp
    else:
        print("Read DDMI case temperature fail. ")
        f.write("\nRead DDMI case temperature fail. ")
        return 'fail'

def read_ddmi_voltage():
    A2RawDataBuff = ctypes.c_ubyte * 2
    A2RawReadByte = A2RawDataBuff()
    Res = 0xFF
    Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 98, 2, A2RawReadByte)
    if 0 == Res:
        print("Read A2 98-99(supply voltage) = 0x{:0>2X},0x{:0>2X} ".format(A2RawReadByte[0], A2RawReadByte[1]))
        f.write("\nRead A2 98-99(supply voltage) = 0x{:0>2X},0x{:0>2X} ".format(A2RawReadByte[0], A2RawReadByte[1]))
        voltage = (A2RawReadByte[0] * 256 + A2RawReadByte[1]) / 10000
        print("Module DDMI supply voltage : {} V".format(voltage))
        f.write("\nModule DDMI supply voltage : {} V".format(voltage))
        return 'ok', voltage
    else:
        print("Read DDMI supply voltage fail. ")
        f.write("\nRead DDMI supply voltage fail. ")
        return 'fail'


def read_ddmi_txbias():
    A2RawDataBuff = ctypes.c_ubyte * 2
    A2RawReadByte = A2RawDataBuff()
    Res = 0xFF
    Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 100, 2, A2RawReadByte)
    if 0 == Res:
        print("Read A2 100-101(TxBias) = 0x{:0>2X},0x{:0>2X} ".format(A2RawReadByte[0], A2RawReadByte[1]))
        f.write("\nRead A2 A2 100-101(TxBias) = 0x{:0>2X},0x{:0>2X} ".format(A2RawReadByte[0], A2RawReadByte[1]))
        bias = (A2RawReadByte[0] * 256 + A2RawReadByte[1]) * 2 / 1000
        print("Module DDMI TX bias : {} mA".format(bias))
        f.write("\nModule DDMI TX bias : {} mA".format(bias))
        return 'ok', bias
    else:
        print("Read DDMI TX bias fail. ")
        f.write("\nRead DDMI TX bias fail. ")
        return 'fail'


def read_ddmi_txpower():
    A2RawDataBuff = ctypes.c_ubyte * 2
    A2RawReadByte = A2RawDataBuff()
    Res = 0xFF
    Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 102, 2, A2RawReadByte)
    if 0 == Res:
        print("Read A2 102-103(TxPower) = 0x{:0>2X},0x{:0>2X} ".format(A2RawReadByte[0], A2RawReadByte[1]))
        f.write("\nRead A2 102-103(TxPower) = 0x{:0>2X},0x{:0>2X} ".format(A2RawReadByte[0], A2RawReadByte[1]))
        #txpower = math.log10((A2RawReadByte[0] * 256 + A2RawReadByte[1]) / 10000) * 10
        txpower = sff8472ToTxpower(A2RawReadByte[0], A2RawReadByte[1], 0.1)
        print("Module DDMI TX Power : {} dBm".format(txpower))
        f.write("\nModule DDMI TX Power : {} dBm".format(txpower))
        return 'ok', txpower
    else:
        print("Read DDMI TX Power fail. ")
        f.write("\nRead DDMI TX Power fail. ")
        return 'fail'

def read_A2_Status():
    A2RawDataBuff = ctypes.c_ubyte * 1
    A2RawReadByte = A2RawDataBuff()
    print("Read A2 110: ")
    f.write("\nRead A2 110: \n")
    Res = 0xFF
    Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 110, 1, A2RawReadByte)
    if 0 == Res:
        print('A2[{}]=0x{:0>2X}'.format(110, A2RawReadByte[0]))
        f.write('A2[{}]=0x{:0>2X}\n'.format(110, A2RawReadByte[0]))
    else:
        print('Read A2 110 fail.')
        f.write('Read A2 110 fail.')
        return 'fail'

def get_temperature_alarm_warn_threshold():
    temp_alarm_warn_Buff = ctypes.c_ubyte * 8
    temp_alarm_warn = temp_alarm_warn_Buff()
    Res = 0xFF
    Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 0, 8, temp_alarm_warn)
    if 0 == Res:
        temp_high_alarm = sff8472ToTemperature(temp_alarm_warn[0], temp_alarm_warn[1])
        temp_low_alarm = sff8472ToTemperature(temp_alarm_warn[2], temp_alarm_warn[3])
        temp_high_warning = sff8472ToTemperature(temp_alarm_warn[4], temp_alarm_warn[5])
        temp_low_warning = sff8472ToTemperature(temp_alarm_warn[6], temp_alarm_warn[7])
        return temp_high_alarm, temp_low_alarm, temp_high_warning, temp_low_warning
    else:
        print("Read temperature Alarm and Warning thresold fail")
        f.write("Read temperature Alarm and Warning thresold fail")

def set_temperature_alarm_warn_threshold(threshold_name, threshold_value):
    assert threshold_name != 'TEMP HIGH ALARM'  \
           or threshold_name != 'TEMP LOW ALARM' \
           or threshold_name != 'TEMP HIGH WARINING' \
           or threshold_name != 'TEMP LOW WARNING'\
           ,"Parameter Error !"
    temp_alarm_warn_Buff = ctypes.c_ubyte * 2
    temp_alarm_warn = temp_alarm_warn_Buff()
    temp_alarm_warn[0], temp_alarm_warn[1] = temperatureToSff8472(threshold_value)

    Res = 0xFF
    if threshold_name == 'TEMP HIGH ALARM':
        Res = testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], \
            Alarm_and_Warning_threshold_Byte[0], 2, byref(temp_alarm_warn))
    if threshold_name == 'TEMP LOW ALARM':
        Res = testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], \
            Alarm_and_Warning_threshold_Byte[1], 2, byref(temp_alarm_warn))
    if threshold_name == 'TEMP HIGH WARNING':
        Res = testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], \
            Alarm_and_Warning_threshold_Byte[2], 2, byref(temp_alarm_warn))
    if threshold_name == 'TEMP LOW WARNING':
        Res = testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], \
            Alarm_and_Warning_threshold_Byte[3], 2, byref(temp_alarm_warn))
    if 0 == Res:
        print("\nSet temperature {} thresold ok".format(threshold_name))
        f.write("\nSet temperature {} thresold ok".format(threshold_name))
    else:
        print("\nSet temperature {} thresold fail".format(threshold_name))
        f.write("\nSet temperature {} thresold fail".format(threshold_name))

def get_temp_alarm_Flag(alarm_flag):
    temp_alarm_flag_Buff = ctypes.c_ubyte * 2
    temp_alarm_flag = temp_alarm_flag_Buff()
    Res = 0xFF
    Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], \
                                          Alarm_and_Warning_Flag_Bits_Byte[0], 1, temp_alarm_flag)
    if 0 == Res:
        if alarm_flag == 'TEMP HIGH ALARM':
            temp_high_alarm_flag = True if temp_alarm_flag[0] & 0x80 == 0x80 else False
            return temp_high_alarm_flag
        if alarm_flag == 'TEMP LOW ALARM':
            temp_low_alarm_flag = True if temp_alarm_flag[0] & 0x40 == 0x40 else False
            return temp_low_alarm_flag
        return 'Parameter Error'
    else:
        print("Read temperature Alarm flag fail :{}".format(Res))
        f.write("Read temperature Alarm flag fail :{}".format(Res))

def get_temp_warning_Flag(warning_flag):
    temp_warning_flag_Buff = ctypes.c_ubyte * 2
    temp_warning_flag = temp_warning_flag_Buff()
    Res = 0xFF
    Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], \
                                          Alarm_and_Warning_Flag_Bits_Byte[4], 1, temp_warning_flag)
    if 0 == Res:
        if warning_flag == 'TEMP HIGH WARNING':
            temp_high_warning_flag = True if temp_warning_flag[0] & 0x80 == 0x80 else False
            return temp_high_warning_flag
        if warning_flag == 'TEMP LOW WARNING':
            temp_low_warning_flag = True if temp_warning_flag[0] & 0x40 == 0x40 else False
            return temp_low_warning_flag
        return 'Parameter Error'
    else:
        print("Read temperature Warning flag fail")
        f.write("Read temperature Warning flag fail")

def get_voltage_alarm_warn_threshold():
    volt_alarm_warn_Buff = ctypes.c_ubyte * 8
    volt_alarm_warn = volt_alarm_warn_Buff()
    Res = 0xFF
    Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 8, 8, volt_alarm_warn)
    if 0 == Res:
        volt_high_alarm = sff8472ToVoltage(volt_alarm_warn[0], volt_alarm_warn[1])
        volt_low_alarm = sff8472ToVoltage(volt_alarm_warn[2], volt_alarm_warn[3])
        volt_high_warning = sff8472ToVoltage(volt_alarm_warn[4], volt_alarm_warn[5])
        volt_low_warning = sff8472ToVoltage(volt_alarm_warn[6], volt_alarm_warn[7])
        return volt_high_alarm, volt_low_alarm, volt_high_warning, volt_low_warning
    else:
        print("Read voltage Alarm and Warning thresold fail")
        f.write("Read voltage Alarm and Warning thresold fail")

def set_voltage_alarm_warn_threshold(threshold_name, threshold_value):
    assert threshold_name != 'VOLT HIGH ALARM'  \
           or threshold_name != 'VOLT LOW ALARM' \
           or threshold_name != 'VOLT HIGH WARINING' \
           or threshold_name != 'VOLT LOW WARNING'\
           ,"Parameter Error !"
    volt_alarm_warn_Buff = ctypes.c_ubyte * 2
    volt_alarm_warn = volt_alarm_warn_Buff()
    volt_alarm_warn[0], volt_alarm_warn[1] = voltageToSff8472(threshold_value)
    Res = 0xFF
    if threshold_name == 'VOLT HIGH ALARM':
        Res = testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], \
            Alarm_and_Warning_threshold_Byte[4], 2, byref(volt_alarm_warn))
    if threshold_name == 'VOLT LOW ALARM':
        Res = testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], \
            Alarm_and_Warning_threshold_Byte[5], 2, byref(volt_alarm_warn))
    if threshold_name == 'VOLT HIGH WARNING':
        Res = testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], \
            Alarm_and_Warning_threshold_Byte[6], 2, byref(volt_alarm_warn))
    if threshold_name == 'VOLT LOW WARNING':
        Res = testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], \
            Alarm_and_Warning_threshold_Byte[7], 2, byref(volt_alarm_warn))
    if 0 == Res:
        print("\nSet voltage {} threshold {} ok".format(threshold_name, threshold_value))
        f.write("\nSet voltage {} threshold {} ok".format(threshold_name,threshold_value))
    else:
        print("\nSet voltage {} threshold {} fail".format(threshold_name, threshold_value))
        f.write("\nSet voltage {} threshold {} fail".format(threshold_name, threshold_value))

def get_volt_alarm_Flag(alarm_flag):
    volt_alarm_flag_Buff = ctypes.c_ubyte * 2
    volt_alarm_flag = volt_alarm_flag_Buff()
    Res = 0xFF
    Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], \
                                          Alarm_and_Warning_Flag_Bits_Byte[0], 1, volt_alarm_flag)
    if 0 == Res:
        if alarm_flag == 'VOLT HIGH ALARM':
            volt_high_alarm_flag = True if volt_alarm_flag[0] & 0x20 == 0x20 else False
            return volt_high_alarm_flag
        if alarm_flag == 'VOLT LOW ALARM':
            volt_low_alarm_flag = True if volt_alarm_flag[0] & 0x10 == 0x10 else False
            return volt_low_alarm_flag
        return 'Parameter Error'
    else:
        print("Read voltage Alarm flag fail :{}".format(Res))
        f.write("Read voltage Alarm flag fail :{}".format(Res))

def get_volt_warning_Flag(warning_flag):
    volt_warning_flag_Buff = ctypes.c_ubyte * 2
    volt_warning_flag = volt_warning_flag_Buff()
    Res = 0xFF
    Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], \
                                          Alarm_and_Warning_Flag_Bits_Byte[4], 1, volt_warning_flag)
    if 0 == Res:
        if warning_flag == 'VOLT HIGH WARNING':
            volt_high_warning_flag = True if volt_warning_flag[0] & 0x20 == 0x20 else False
            return volt_high_warning_flag
        if warning_flag == 'VOLT LOW WARNING':
            volt_low_warning_flag = True if volt_warning_flag[0] & 0x10 == 0x10 else False
            return volt_low_warning_flag
        return 'Parameter Error'
    else:
        print("Read voltage Warning flag fail")
        f.write("Read voltage Warning flag fail")


def get_txbias_alarm_warn_threshold():
    txbias_alarm_warn_Buff = ctypes.c_ubyte * 8
    txbias_alarm_warn = txbias_alarm_warn_Buff()
    Res = 0xFF
    Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 16, 8, txbias_alarm_warn)
    if 0 == Res:
        txbias_high_alarm = sff8472ToTxbias(txbias_alarm_warn[0], txbias_alarm_warn[1], 2)
        txbias_low_alarm = sff8472ToTxbias(txbias_alarm_warn[2], txbias_alarm_warn[3], 2)
        txbias_high_warning = sff8472ToTxbias(txbias_alarm_warn[4], txbias_alarm_warn[5], 2)
        txbias_low_warning = sff8472ToTxbias(txbias_alarm_warn[6], txbias_alarm_warn[7], 2)
        return txbias_high_alarm, txbias_low_alarm, txbias_high_warning, txbias_low_warning
    else:
        print("Read txbias Alarm and Warning thresold fail")
        f.write("Read txbias Alarm and Warning thresold fail")

def set_txbias_alarm_warn_threshold(threshold_name, threshold_value):
    assert threshold_name != 'TXBIAS HIGH ALARM'  \
           or threshold_name != 'TXBIAS LOW ALARM' \
           or threshold_name != 'TXBIAS HIGH WARINING' \
           or threshold_name != 'TXBIAS LOW WARNING'\
           ,"Parameter Error !"
    txbias_alarm_warn_Buff = ctypes.c_ubyte * 2
    txbias_alarm_warn = txbias_alarm_warn_Buff()
    txbias_alarm_warn[0], txbias_alarm_warn[1] = txbiasToSff8472(threshold_value, 2)
    Res = 0xFF
    if threshold_name == 'TXBIAS HIGH ALARM':
        Res = testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], \
            Alarm_and_Warning_threshold_Byte[8], 2, byref(txbias_alarm_warn))
    if threshold_name == 'TXBIAS LOW ALARM':
        Res = testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], \
            Alarm_and_Warning_threshold_Byte[9], 2, byref(txbias_alarm_warn))
    if threshold_name == 'TXBIAS HIGH WARNING':
        Res = testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], \
            Alarm_and_Warning_threshold_Byte[10], 2, byref(txbias_alarm_warn))
    if threshold_name == 'TXBIAS LOW WARNING':
        Res = testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], \
            Alarm_and_Warning_threshold_Byte[11], 2, byref(txbias_alarm_warn))
    if 0 == Res:
        print("\nSet txbias {} threshold {} ok".format(threshold_name, threshold_value))
        f.write("\nSet txbias {} threshold {} ok".format(threshold_name,threshold_value))
    else:
        print("\nSet txbias {} threshold {} fail".format(threshold_name, threshold_value))
        f.write("\nSet txbias {} threshold {} fail".format(threshold_name, threshold_value))

def get_txbias_alarm_Flag(alarm_flag):
    txbias_alarm_flag_Buff = ctypes.c_ubyte * 2
    txbias_alarm_flag = txbias_alarm_flag_Buff()
    Res = 0xFF
    Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], \
                                          Alarm_and_Warning_Flag_Bits_Byte[0], 1, txbias_alarm_flag)
    if 0 == Res:
        if alarm_flag == 'TXBIAS HIGH ALARM':
            txbias_high_alarm_flag = True if txbias_alarm_flag[0] & 0x08 == 0x08 else False
            return txbias_high_alarm_flag
        if alarm_flag == 'TXBIAS LOW ALARM':
            txbias_low_alarm_flag = True if txbias_alarm_flag[0] & 0x04 == 0x04 else False
            return txbias_low_alarm_flag
        return 'Parameter Error'
    else:
        print("Read txbias Alarm flag fail :{}".format(Res))
        f.write("Read txbias Alarm flag fail :{}".format(Res))

def get_txbias_warning_Flag(warning_flag):
    txbias_warning_flag_Buff = ctypes.c_ubyte * 2
    txbias_warning_flag = txbias_warning_flag_Buff()
    Res = 0xFF
    Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], \
                                          Alarm_and_Warning_Flag_Bits_Byte[4], 1, txbias_warning_flag)
    if 0 == Res:
        if warning_flag == 'TXBIAS HIGH WARNING':
            txbias_high_warning_flag = True if txbias_warning_flag[0] & 0x08 == 0x08 else False
            return txbias_high_warning_flag
        if warning_flag == 'TXBIAS LOW WARNING':
            txbias_low_warning_flag = True if txbias_warning_flag[0] & 0x04 == 0x04 else False
            return txbias_low_warning_flag
        return 'Parameter Error'
    else:
        print("Read txbias Warning flag fail")
        f.write("Read txbias Warning flag fail")

def get_txpower_alarm_warn_threshold():
    txpower_alarm_warn_Buff = ctypes.c_ubyte * 8
    txpower_alarm_warn = txpower_alarm_warn_Buff()
    Res = 0xFF
    Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 24, 8, txpower_alarm_warn)
    if 0 == Res:
        txpower_high_alarm = sff8472ToTxpower(txpower_alarm_warn[0], txpower_alarm_warn[1], 0.1)
        txpower_low_alarm = sff8472ToTxpower(txpower_alarm_warn[2], txpower_alarm_warn[3], 0.1)
        txpower_high_warning = sff8472ToTxpower(txpower_alarm_warn[4], txpower_alarm_warn[5], 0.1)
        txpower_low_warning = sff8472ToTxpower(txpower_alarm_warn[6], txpower_alarm_warn[7], 0.1)
        return txpower_high_alarm, txpower_low_alarm, txpower_high_warning, txpower_low_warning
    else:
        print("Read txpower Alarm and Warning thresold fail")
        f.write("Read txpower Alarm and Warning thresold fail")

def set_txpower_alarm_warn_threshold(threshold_name, threshold_value):
    assert threshold_name != 'TXPOWER HIGH ALARM'  \
           or threshold_name != 'TXPOWER LOW ALARM' \
           or threshold_name != 'TXPOWER HIGH WARNING' \
           or threshold_name != 'TXPOWER LOW WARNING'\
           ,"Parameter Error !"
    txpower_alarm_warn_Buff = ctypes.c_ubyte * 2
    txpower_alarm_warn = txpower_alarm_warn_Buff()
    txpower_alarm_warn[0], txpower_alarm_warn[1] = txpowerToSff8472(threshold_value, 0.1)
    Res = 0xFF
    if threshold_name == 'TXPOWER HIGH ALARM':
        Res = testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], \
            Alarm_and_Warning_threshold_Byte[12], 2, byref(txpower_alarm_warn))
    if threshold_name == 'TXPOWER LOW ALARM':
        Res = testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], \
            Alarm_and_Warning_threshold_Byte[13], 2, byref(txpower_alarm_warn))
    if threshold_name == 'TXPOWER HIGH WARNING':
        Res = testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], \
            Alarm_and_Warning_threshold_Byte[14], 2, byref(txpower_alarm_warn))
    if threshold_name == 'TXPOWER LOW WARNING':
        Res = testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], \
            Alarm_and_Warning_threshold_Byte[15], 2, byref(txpower_alarm_warn))
    if 0 == Res:
        print("\nSet txpower {} threshold {} ok".format(threshold_name, threshold_value))
        f.write("\nSet txpower {} threshold {} ok".format(threshold_name,threshold_value))
    else:
        print("\nSet txpower {} threshold {} fail".format(threshold_name, threshold_value))
        f.write("\nSet txpower {} threshold {} fail".format(threshold_name, threshold_value))

def get_txpower_alarm_Flag(alarm_flag):
    txpower_alarm_flag_Buff = ctypes.c_ubyte * 2
    txpower_alarm_flag = txpower_alarm_flag_Buff()
    Res = 0xFF
    Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], \
                                          Alarm_and_Warning_Flag_Bits_Byte[0], 1, txpower_alarm_flag)
    if 0 == Res:
        if alarm_flag == 'TXPOWER HIGH ALARM':
            txpower_high_alarm_flag = True if txpower_alarm_flag[0] & 0x02 == 0x02 else False
            return txpower_high_alarm_flag
        if alarm_flag == 'TXPOWER LOW ALARM':
            txpower_low_alarm_flag = True if txpower_alarm_flag[0] & 0x01 == 0x01 else False
            return txpower_low_alarm_flag
        return 'Parameter Error'
    else:
        print("Read txpower Alarm flag fail :{}".format(Res))
        f.write("Read txpower Alarm flag fail :{}".format(Res))

def get_txpower_warning_Flag(warning_flag):
    txpower_warning_flag_Buff = ctypes.c_ubyte * 2
    txpower_warning_flag = txpower_warning_flag_Buff()
    Res = 0xFF
    Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], \
                                          Alarm_and_Warning_Flag_Bits_Byte[4], 1, txpower_warning_flag)
    if 0 == Res:
        if warning_flag == 'TXPOWER HIGH WARNING':
            txpower_high_warning_flag = True if txpower_warning_flag[0] & 0x02 == 0x02 else False
            return txpower_high_warning_flag
        if warning_flag == 'TXPOWER LOW WARNING':
            txpower_low_warning_flag = True if txpower_warning_flag[0] & 0x01 == 0x01 else False
            return txpower_low_warning_flag
        return 'Parameter Error'
    else:
        print("Read txpower Warning flag fail")
        f.write("Read txpower Warning flag fail")
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
print("SFF-8472 DDMI Alarm and Warning test, start time : {}".format(dateTime))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nSFF-8472 DDMI Alarm and Warning test, start time : {}".format(dateTime))
f.write("\n****************************************************************************")
print("Firmware Version : {}".format(testTitle))
f.write('\nFirmware Version : '+testTitle)

strCmdIn = create_string_buffer(b'MCU_GET_TABLE(base,3,4,16)')
strCmdOutBuff = ctypes.c_ubyte * 64
strCmdOut = strCmdOutBuff()
strModuleId = []
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    strModuleId = [chr(strCmdOut[item]) for item in range(len(strCmdOut)) if 0 != strCmdOut[item]]
    strModuleId = ''.join(strModuleId).split(',')
    print("Module ID : ", end='')
    f.write("\nModule ID : ")
    for item in range(len(strModuleId)):
        if '0xFF' == strModuleId[item]:
            print("{}".format(strModuleId[item]), end='')
            f.write("{}".format(strModuleId[item]))
        else:
            print("{}".format(chr(int(strModuleId[item], 16))), end='')
            f.write("{}".format(chr(int(strModuleId[item], 16))))
else:
    print("Can't get module ID! ")

#########################################################
#    test step 1 :  Backup alarm and warning threshold
#########################################################
A2RawDataBuff = ctypes.c_ubyte*96
A2RawReadByte = A2RawDataBuff()
f.write("\nA2 Direct raw data: \n")
Res = 0xFF
Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 0, 96, A2RawReadByte)
if 0 == Res:
    for item in range(96):
        f.write(str(hex(A2RawReadByte[item]))+',')
else:
    f.write('read A2 0-96 raw data fail.'+'\n')
    print('read A2 0-96 raw data fail.' + '\n')
    f.close()
    sys.exit()

#########################################################
#    test step 2 :  case temperature alarm and warning
#########################################################
#read current case temperature
print("\nRead Temperature...")
f.write("\nRead Temperature...")
status, case_temperature = read_ddmi_case_temperature()
if status == 'fail':
    print("\nDon't get DDMI case temperature")
    f.write("\nDon't get DDMI case temperature")
    sys.exit()
#print("\ntest 1 = {}".format(sff8472ToTemperature(128, 1)))
#print("\ntest 2 = {}".format(sff8472ToTemperature(127, 255)))
#print("\ntest 3= {}".format(temperatureToSff8472(127.996)))
#print("\ntest 4= {}".format(temperatureToSff8472(-127.996)))
#read current case temperature alarm and warning threshold
temp_high_alarm_threshold, temp_low_alarm_threshold,\
    temp_high_warning_threshold, temp_low_warning_threshold = get_temperature_alarm_warn_threshold()
print("Case Temperature High Alarm Threshold : {} ".format(temp_high_alarm_threshold))
print("Case Temperature Low Alarm Threshold : {} ".format(temp_low_alarm_threshold))
print("Case Temperature High Warning Threshold : {}".format(temp_high_warning_threshold))
print("Case Temperature Low Warning Threshold : {}".format(temp_low_warning_threshold))
f.write("\nCase Temperature High Alarm Threshold : {}".format(temp_high_alarm_threshold))
f.write("\nCase Temperature Low Alarm Threshold : {}".format(temp_low_alarm_threshold))
f.write("\nCase Temperature High Warning Threshold : {}".format(temp_high_warning_threshold))
f.write("\nCase Temperature Low Warning Threshold : {}".format(temp_low_warning_threshold))

#read current case temperature flag bits
print("\nNow case temperature alarm and warning :")
f.write("\nNow case temperature alarm and warning :")
HighAlarmFlag = get_temp_alarm_Flag('TEMP HIGH ALARM')
LowAlarmFlag = get_temp_alarm_Flag('TEMP LOW ALARM')
if True == HighAlarmFlag:
    print("Case Temperature High Alarm. ")
    f.write("\nCase Temperature High Alarm. ")
else:
    print("Case Temperature not High Alarm. ")
    f.write("\nCase Temperature not High Alarm. ")
if True == LowAlarmFlag:
    print("Case Temperature Low Alarm" )
    f.write("\nCase Temperature Low Alarm")
else:
    print("Case Temperature not Low Alarm")
    f.write("\nCase Temperature not Low Alarm")
HighWarningFlag = get_temp_warning_Flag('TEMP HIGH WARNING')
LowWarningFlag = get_temp_warning_Flag('TEMP LOW WARNING')
if True == HighWarningFlag:
    print("Case Temperature High Warning. ")
    f.write("\nCase Temperature High Warning. ")
else:
    print("Case Temperature not High Warning. ")
    f.write("\nCase Temperature not High Warning. ")
if True == LowWarningFlag:
    print("Case Temperature Low Warning" )
    f.write("\nCase Temperature Low Warning")
else:
    print("Case Temperature not Low Warning")
    f.write("\nCase Temperature not Low Warning")

# set threshold , enable alarm or warning
print("\nSet case temperature high alarm threshold ...")
f.write("\nSet case temperature high alarm threshold ...")
#high alarm threshold = case_temperature - 10
set_temperature_alarm_warn_threshold('TEMP HIGH ALARM', case_temperature-10)
time.sleep(2)
HighAlarmFlag = get_temp_alarm_Flag('TEMP HIGH ALARM')
if True == HighAlarmFlag:
    print("Case temperature high alarm, test temp high alarm flag ok ！")
    f.write("\nCase temperature high alarm, test temp high alarm flag ok ！")
else:
    print("Case temperature not high alarm, test temp high alarm flag fail ！")
    f.write("\nCase temperature not high alarm, test temp high alarm flag fail ！")

print("\nSet case temperature low alarm threshold ...")
f.write("\nSet case temperature low alarm threshold ...")
# low alarm threshold = case_temperature + 10
set_temperature_alarm_warn_threshold('TEMP LOW ALARM', case_temperature+10)
time.sleep(2)
LowAlarmFlag = get_temp_alarm_Flag('TEMP LOW ALARM')
if True == LowAlarmFlag:
    print("Case temperature low alarm, test temp low alarm flag ok ！")
    f.write("\nCase temperature low alarm, test temp low alarm flag ok ！")
else:
    print("Case temperature not low alarm, test temp low alarm flag fail ！")
    f.write("\nCase temperature not low alarm, test temp low alarm flag fail ！")

print("\nSet case temperature high warning threshold ...")
f.write("\nSet case temperature high warning threshold ...")
#high warning threshold = case_temperature + 10
set_temperature_alarm_warn_threshold('TEMP HIGH WARNING', case_temperature-10)
time.sleep(2)
HighWarningFlag = get_temp_warning_Flag('TEMP HIGH WARNING')
if True == HighWarningFlag:
    print("Case temperature high warning, test temp warning alarm flag ok ！")
    f.write("\nCase temperature high warning, test temp high warning flag ok ！")
else:
    print("Case temperature not high warning, test temp high warning flag fail ！")
    f.write("\nCase temperature not high warning, test temp high warning flag fail ！")

print("\nSet case temperature low warning threshold ...")
f.write("\nSet case temperature low warning threshold ...")
# low alarm threshold = case_temperature - 10
set_temperature_alarm_warn_threshold('TEMP LOW WARNING', case_temperature+10)
time.sleep(2)
LowWarningFlag = get_temp_warning_Flag('TEMP LOW WARNING')
if True == LowWarningFlag:
    print("Case temperature low warning, test temp low warning flag ok ！")
    f.write("\nCase temperature low warning, test temp low warning flag ok ！")
else:
    print("Case temperature not low warning, test temp low warning flag fail ！")
    f.write("\nCase temperature not low warning, test temp low warning flag fail ！")

#########################################################
#    test step 3 :  voltage alarm and warning
#########################################################
#read current voltage
print("\nRead Voltage...")
f.write("\nRead Voltages...")
status, voltage = read_ddmi_voltage()
if status == 'fail':
    print("\nDon't get DDMI voltage !")
    f.write("\nDon't get DDMI voltage !")
    sys.exit()

volt_high_alarm_threshold, volt_low_alarm_threshold,\
    volt_high_warning_threshold, volt_low_warning_threshold = get_voltage_alarm_warn_threshold()
print("Voltage High Alarm Threshold : {} ".format(volt_high_alarm_threshold))
print("Voltage Low Alarm Threshold : {} ".format(volt_low_alarm_threshold))
print("Voltage High Warning Threshold : {}".format(volt_high_warning_threshold))
print("Voltage Low Warning Threshold : {}".format(volt_low_warning_threshold))
f.write("\nVoltage High Alarm Threshold : {}".format(volt_high_alarm_threshold))
f.write("\nVoltage Low Alarm Threshold : {}".format(volt_low_alarm_threshold))
f.write("\nVoltage High Warning Threshold : {}".format(volt_high_warning_threshold))
f.write("\nVoltage Low Warning Threshold : {}".format(volt_low_warning_threshold))

#read current voltage flag bits
print("\nNow voltage alarm and warning :")
f.write("\nNow voltage alarm and warning :")
HighAlarmFlag = get_volt_alarm_Flag('VOLT HIGH ALARM')
LowAlarmFlag = get_volt_alarm_Flag('VOLT LOW ALARM')
if True == HighAlarmFlag:
    print("Voltage High Alarm. ")
    f.write("\nVoltage High Alarm. ")
else:
    print("Voltage not High Alarm. ")
    f.write("\nVoltage not High Alarm. ")
if True == LowAlarmFlag:
    print("Voltage Low Alarm" )
    f.write("\nVoltage Low Alarm")
else:
    print("Voltage not Low Alarm")
    f.write("\nVoltage not Low Alarm")
HighWarningFlag = get_volt_warning_Flag('VOLT HIGH WARNING')
LowWarningFlag = get_volt_warning_Flag('VOLT LOW WARNING')
if True == HighWarningFlag:
    print("Voltage High Warning. ")
    f.write("\nVoltage High Warning. ")
else:
    print("Voltage not High Warning. ")
    f.write("\nVoltage not High Warning. ")
if True == LowWarningFlag:
    print("Voltage Low Warning" )
    f.write("\nVoltage Low Warning")
else:
    print("Voltage not Low Warning")
    f.write("\nVoltage not Low Warning")

# set threshold , enable alarm or warning
print("\nSet Voltage high alarm threshold ...")
f.write("\nSet Voltage high alarm threshold ...")
#high alarm threshold = voltage - 0.5
#print(voltage)
#print(voltage-0.5)
set_voltage_alarm_warn_threshold('VOLT HIGH ALARM', voltage-0.5)
time.sleep(2)
HighAlarmFlag = get_volt_alarm_Flag('VOLT HIGH ALARM')
if True == HighAlarmFlag:
    print("Voltage high alarm, test voltage high alarm flag ok ！")
    f.write("\nVoltage high alarm, test voltage high alarm flag ok ！")
else:
    print("Voltage not high alarm, test voltage high alarm flag fail ！")
    f.write("\nVoltage not high alarm, test voltage high alarm flag fail ！")

print("\nSet voltage low alarm threshold ...")
f.write("\nSet voltage low alarm threshold ...")
# low alarm threshold = voltage + 0.5
set_voltage_alarm_warn_threshold('VOLT LOW ALARM', voltage+0.5)
time.sleep(2)
LowAlarmFlag = get_volt_alarm_Flag('VOLT LOW ALARM')
if True == LowAlarmFlag:
    print("Voltage low alarm, test volt low alarm flag ok ！")
    f.write("\nVoltage low alarm, test volt low alarm flag ok ！")
else:
    print("Voltage not low alarm, test volt low alarm flag fail ！")
    f.write("\nVoltage not low alarm, test volt low alarm flag fail ！")

print("\nSet Voltage high warning threshold ...")
f.write("\nSet Voltage high warning threshold ...")
#high warning threshold = Voltage + 10
set_voltage_alarm_warn_threshold('VOLT HIGH WARNING', voltage-0.5)
time.sleep(2)
HighWarningFlag = get_volt_warning_Flag('VOLT HIGH WARNING')
if True == HighWarningFlag:
    print("Voltage high warning, test volt warning alarm flag ok ！")
    f.write("\nVoltage high warning, test volt high warning flag ok ！")
else:
    print("Voltage not high warning, test volt high warning flag fail ！")
    f.write("\nVoltage not high warning, test volt high warning flag fail ！")

print("\nSet voltage low warning threshold ...")
f.write("\nSet voltage low warning threshold ...")
# low alarm threshold = voltage - 10
set_voltage_alarm_warn_threshold('VOLT LOW WARNING', voltage+0.5)
time.sleep(2)
LowWarningFlag = get_volt_warning_Flag('VOLT LOW WARNING')
if True == LowWarningFlag:
    print("Voltage low warning, test volt low warning flag ok ！")
    f.write("\nVoltage low warning, test volt low warning flag ok ！")
else:
    print("Voltage not low warning, test volt low warning flag fail ！")
    f.write("\nVoltage not low warning, test volt low warning flag fail ！")

########################################################
#    test step 4 :  txbias alarm and warning
#########################################################
#read curren txbias
print("\nRead txbias...")
f.write("\nRead txbias...")
status, txbias = read_ddmi_txbias()
if status == 'fail':
    print("\nDon't get DDMI txbias !")
    f.write("\nDon't get DDMI txbias !")
    sys.exit()

txbias_high_alarm_threshold, txbias_low_alarm_threshold,\
    txbias_high_warning_threshold, txbias_low_warning_threshold = get_txbias_alarm_warn_threshold()
print("Txbias High Alarm Threshold : {} ".format(txbias_high_alarm_threshold))
print("Txbias Low Alarm Threshold : {} ".format(txbias_low_alarm_threshold))
print("Txbias High Warning Threshold : {}".format(txbias_high_warning_threshold))
print("Txbias Low Warning Threshold : {}".format(txbias_low_warning_threshold))
f.write("\nTxbias High Alarm Threshold : {}".format(txbias_high_alarm_threshold))
f.write("\nTxbias Low Alarm Threshold : {}".format(txbias_low_alarm_threshold))
f.write("\nTxbias High Warning Threshold : {}".format(txbias_high_warning_threshold))
f.write("\nTxbias Low Warning Threshold : {}".format(txbias_low_warning_threshold))

#read current txbias flag bits
print("\nNow txbias alarm and warning :")
f.write("\nNow txbias alarm and warning :")
HighAlarmFlag = get_txbias_alarm_Flag('TXBIAS HIGH ALARM')
LowAlarmFlag = get_txbias_alarm_Flag('TXBIAS LOW ALARM')
if True == HighAlarmFlag:
    print("Txbias High Alarm. ")
    f.write("\nTxbias High Alarm. ")
else:
    print("Txbias not High Alarm. ")
    f.write("\nTxbias not High Alarm. ")
if True == LowAlarmFlag:
    print("Txbias Low Alarm" )
    f.write("\nTxbias Low Alarm")
else:
    print("Txbias not Low Alarm")
    f.write("\nTxbias not Low Alarm")
HighWarningFlag = get_txbias_warning_Flag('TXBIAS HIGH WARNING')
LowWarningFlag = get_txbias_warning_Flag('TXBIAS LOW WARNING')
if True == HighWarningFlag:
    print("Txbias High Warning. ")
    f.write("\nTxbias High Warning. ")
else:
    print("Txbias not High Warning. ")
    f.write("\nTxbias not High Warning. ")
if True == LowWarningFlag:
    print("Txbias Low Warning" )
    f.write("\nTxbias Low Warning")
else:
    print("Txbias not Low Warning")
    f.write("\nTxbias not Low Warning")

# set threshold , enable alarm or warning
print("\nSet Txbias high alarm threshold ...")
f.write("\nSet Txbias high alarm threshold ...")
#high alarm threshold = txbias - 5
set_txbias_alarm_warn_threshold('TXBIAS HIGH ALARM', txbias-5)
time.sleep(2)
HighAlarmFlag = get_txbias_alarm_Flag('TXBIAS HIGH ALARM')
if True == HighAlarmFlag:
    print("Txbias high alarm, test txbias high alarm flag ok ！")
    f.write("\nTxbias high alarm, test txbias high alarm flag ok ！")
else:
    print("Txbias not high alarm, test txbias high alarm flag fail ！")
    f.write("\nTxbias not high alarm, test txbias high alarm flag fail ！")

print("\nSet txbias low alarm threshold ...")
f.write("\nSet txbias low alarm threshold ...")
# low alarm threshold = txbias + 5
set_txbias_alarm_warn_threshold('TXBIAS LOW ALARM', txbias+5)
time.sleep(2)
LowAlarmFlag = get_txbias_alarm_Flag('TXBIAS LOW ALARM')
if True == LowAlarmFlag:
    print("Txbias low alarm, test txbias low alarm flag ok ！")
    f.write("\nTxbias low alarm, test txbias low alarm flag ok ！")
else:
    print("Txbias not low alarm, test txbias low alarm flag fail ！")
    f.write("\nTxbias not low alarm, test txbias low alarm flag fail ！")

print("\nSet Txbias high warning threshold ...")
f.write("\nSet Txbias high warning threshold ...")
#high warning threshold = txbias + 10
set_txbias_alarm_warn_threshold('TXBIAS HIGH WARNING', txbias-5)
time.sleep(2)
HighWarningFlag = get_txbias_warning_Flag('TXBIAS HIGH WARNING')
if True == HighWarningFlag:
    print("Txbias high warning, test txbias warning alarm flag ok ！")
    f.write("\nTxbias high warning, test txbias high warning flag ok ！")
else:
    print("Txbias not high warning, test txbias high warning flag fail ！")
    f.write("\nTxbias not high warning, test txbias high warning flag fail ！")

print("\nSet txbias low warning threshold ...")
f.write("\nSet txbias low warning threshold ...")
# low alarm threshold = txbias - 10
set_txbias_alarm_warn_threshold('TXBIAS LOW WARNING', txbias+5)
time.sleep(2)
LowWarningFlag = get_txbias_warning_Flag('TXBIAS LOW WARNING')
if True == LowWarningFlag:
    print("Txbias low warning, test txbias low warning flag ok ！")
    f.write("\nTxbias low warning, test txbias low warning flag ok ！")
else:
    print("Txbias not low warning, test txbias low warning flag fail ！")
    f.write("\nTxbias not low warning, test txbias low warning flag fail ！")


#########################################################
#    test step 5 :  txpower alarm and warning
#########################################################
#read curren txpower
print("\nRead txpower...")
f.write("\nRead txpower...")
status, txpower = read_ddmi_txpower()
if status == 'fail':
    print("\nDon't get DDMI txpower !")
    f.write("\nDon't get DDMI txpower !")
    sys.exit()

txpower_high_alarm_threshold, txpower_low_alarm_threshold,\
    txpower_high_warning_threshold, txpower_low_warning_threshold = get_txpower_alarm_warn_threshold()
print("Txpower High Alarm Threshold : {} ".format(txpower_high_alarm_threshold))
print("Txpower Low Alarm Threshold : {} ".format(txpower_low_alarm_threshold))
print("Txpower High Warning Threshold : {}".format(txpower_high_warning_threshold))
print("Txpower Low Warning Threshold : {}".format(txpower_low_warning_threshold))
f.write("\nTxpower High Alarm Threshold : {}".format(txpower_high_alarm_threshold))
f.write("\nTxpower Low Alarm Threshold : {}".format(txpower_low_alarm_threshold))
f.write("\nTxpower High Warning Threshold : {}".format(txpower_high_warning_threshold))
f.write("\nTxpower Low Warning Threshold : {}".format(txpower_low_warning_threshold))

#read current txpower flag bits
print("\nNow txpower alarm and warning :")
f.write("\nNow txpower alarm and warning :")
HighAlarmFlag = get_txpower_alarm_Flag('TXPOWER HIGH ALARM')
LowAlarmFlag = get_txpower_alarm_Flag('TXPOWER LOW ALARM')
if True == HighAlarmFlag:
    print("Txpower High Alarm. ")
    f.write("\nTxpower High Alarm. ")
else:
    print("Txpower not High Alarm. ")
    f.write("\nTxpower not High Alarm. ")
if True == LowAlarmFlag:
    print("Txpower Low Alarm" )
    f.write("\nTxpower Low Alarm")
else:
    print("Txpower not Low Alarm")
    f.write("\nTxpower not Low Alarm")
HighWarningFlag = get_txpower_warning_Flag('TXPOWER HIGH WARNING')
LowWarningFlag = get_txpower_warning_Flag('TXPOWER LOW WARNING')
if True == HighWarningFlag:
    print("Txpower High Warning. ")
    f.write("\nTxpowers High Warning. ")
else:
    print("Txpower not High Warning. ")
    f.write("\nTxpower not High Warning. ")
if True == LowWarningFlag:
    print("Txpower Low Warning" )
    f.write("\nTxpower Low Warning")
else:
    print("Txpower not Low Warning")
    f.write("\nTxpower not Low Warning")

# set threshold , enable alarm or warning
print("\nSet Txpower high alarm threshold ...")
f.write("\nSet Txpower high alarm threshold ...")
#high alarm threshold = txpower - 1
set_txpower_alarm_warn_threshold('TXPOWER HIGH ALARM', txpower-1)
time.sleep(2)
HighAlarmFlag = get_txpower_alarm_Flag('TXPOWER HIGH ALARM')
if True == HighAlarmFlag:
    print("Txpower high alarm, test txpower high alarm flag ok ！")
    f.write("\nTxpower high alarm, test txpower high alarm flag ok ！")
else:
    print("Txpower not high alarm, test txpower high alarm flag fail ！")
    f.write("\nTxpower not high alarm, test txpower high alarm flag fail ！")

print("\nSet txpower low alarm threshold ...")
f.write("\nSet txpower low alarm threshold ...")
# low alarm threshold = txpower + 1
set_txpower_alarm_warn_threshold('TXPOWER LOW ALARM', txpower+1)
time.sleep(2)
LowAlarmFlag = get_txpower_alarm_Flag('TXPOWER LOW ALARM')
if True == LowAlarmFlag:
    print("Txpower low alarm, test txpower low alarm flag ok ！")
    f.write("\nTxpower low alarm, test txpower low alarm flag ok ！")
else:
    print("Txpower not low alarm, test txpower low alarm flag fail ！")
    f.write("\nTxpower not low alarm, test txpower low alarm flag fail ！")

print("\nSet Txpower high warning threshold ...")
f.write("\nSet Txpower high warning threshold ...")
#high warning threshold = txpower - 1
set_txpower_alarm_warn_threshold('TXPOWER HIGH WARNING', txpower-1)
time.sleep(2)
HighWarningFlag = get_txpower_warning_Flag('TXPOWER HIGH WARNING')
if True == HighWarningFlag:
    print("Txpower high warning, test txpower warning alarm flag ok ！")
    f.write("\nTxpower high warning, test txpower high warning flag ok ！")
else:
    print("Txpower not high warning, test txpower high warning flag fail ！")
    f.write("\nTxpower not high warning, test txpower high warning flag fail ！")

print("\nSet txpower low warning threshold ...")
f.write("\nSet txpower low warning threshold ...")
# low alarm threshold = txpower - 1
set_txpower_alarm_warn_threshold('TXPOWER LOW WARNING', txpower+1)
time.sleep(2)
LowWarningFlag = get_txpower_warning_Flag('TXPOWER LOW WARNING')
if True == LowWarningFlag:
    print("Txpower low warning, test txpower low warning flag ok ！")
    f.write("\nTxpower low warning, test txpower low warning flag ok ！")
else:
    print("Txpower not low warning, test txpower low warning flag fail ！")
    f.write("\nTxpower not low warning, test txpower low warning flag fail ！")


#########################################################
#    test step 6 :  rxpower alarm and warning
#########################################################


#########################################################
#    test step 7 :  Restore A2 0-95
#########################################################
Sfp_Factory_Pwd_Entry(user_password_type)
time.sleep(1)
testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, SfpI2cAddr[1], 0, 96, byref(A2RawReadByte))
time.sleep(2)
testEvb.AteAllPowerOff()
time.sleep(1)
testEvb.AteAllPowerOn()
time.sleep(1)
A2ReadDataBuff = ctypes.c_ubyte * 96
randomReadByte = A2ReadDataBuff()
testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 0, 96, randomReadByte)
if True == operator.eq(A2RawDataBuff, A2ReadDataBuff):
    f.write('\nA2 Direct restore success.' + '\n')
    print("A2 Direct restore success.")
else:
    f.write('\nA2 Direct restore fail.' + '\n')
    print("A2 Direct restore fail.")

dateTime = time.strptime(time.asctime())
dateTime = "{:4}-{:02}-{:02} {:02}:{:02}:{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
print("\n****************************************************************************")
print("SFF-8472 DDMI Alarm and Warning test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nSFF-8472 DDMI Alarm and Warning test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
f.write("\n****************************************************************************")
testEvb.AteAllPowerOff()
f.close()

