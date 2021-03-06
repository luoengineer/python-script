import ctypes
from ctypes import *
import time
import random
import operator
from cmdServ import cmdservdll, Sfp_Factory_Pwd_Entry
from classTestEvb import *
import sys
import os



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

module_adc_chn_nums = 7
module_adjust_chn_nums = 8
module_dac_chn_nums = 2
module_base_talbe_nums = 4
module_drv_table_nums = 1
module_lutable_nums = 4

#########################################################
#               create object
#########################################################
testEvb = cTestEvb(devUsbIndex)

#########################################################
#               Inner Funtion
#########################################################
def mcu_get_adc(adc_chn):
    command_str = 'MCU_GET_ADC(' + str(adc_chn) + ')'
    command_str = bytes(command_str, encoding="utf8")
    strCmdIn = create_string_buffer(command_str)
    strCmdOutBuff = ctypes.c_ubyte * 32
    strCmdOut = strCmdOutBuff()
    retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 0 == retStauts:
        print("\nADC {:d} : ".format(adc_chn), end='')
        f.write("\nADC {:d} : ".format(adc_chn))
        tempCmdOut = strCmdOut[2:4]
        strCmdOut[2:4] = strCmdOut[4:6]
        strCmdOut[4:6] = tempCmdOut
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
    else:
        print("{0:d}".format(retStauts))
        f.write(str(retStauts))
    
def mcu_get_adjust(adjust_chn):
    command_str = 'MCU_GET_ADJUST(' + str(adjust_chn) + ')'
    command_str = bytes(command_str, encoding="utf8")
    strCmdIn = create_string_buffer(command_str)
    strCmdOutBuff = ctypes.c_ubyte * 32
    strCmdOut = strCmdOutBuff()
    retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 0 == retStauts:
        print('\nMCU_GET_ADJUST {:d} :'.format(adjust_chn),end='')
        f.write('\nMCU_GET_ADJUST {:d} :'.format(adjust_chn))
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

def mcu_get_dac(dac_chn):
    command_str = 'MCU_GET_DAC(' + str(dac_chn) + ')'
    command_str = bytes(command_str, encoding="utf8")
    strCmdIn = create_string_buffer(command_str)
    strCmdOutBuff = ctypes.c_ubyte * 32
    strCmdOut = strCmdOutBuff()
    retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 0 == retStauts:
        print('\nMCU_GET_DAC {:d} :'.format(dac_chn), end='')
        f.write('\nMCU_GET_DAC {:d} :'.format(dac_chn))
        tempCmdOut = strCmdOut[2:4]
        strCmdOut[2:4] = strCmdOut[4:6]
        strCmdOut[4:6] = tempCmdOut
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
    else:
        print("{0:d}".format(retStauts))
        f.write(str(retStauts))

def mcu_get_base_table(base_table_index):
    command_str = 'MCU_GET_TABLE(base,' + str(base_table_index) + ',0,128)'
    command_str = bytes(command_str, encoding="utf8")
    strCmdIn = create_string_buffer(command_str)
    strCmdOutBuff = ctypes.c_ubyte * 1024
    strCmdOut = strCmdOutBuff()
    retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 0 == retStauts:
        print('\nMCU_GET_TABLE base {:d} :'.format(base_table_index))
        f.write('\nMCU_GET_TABLE base {:d} :'.format(base_table_index))
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
    else:
        print("\nGet base {} table fail, error code :{:d}".format(base_table_index, retStauts))
        f.write("\nGet base {} table fail, error code :{:d}".format(base_table_index, retStauts))

def mcu_get_lut(lutable_index):
    command_str = 'MCU_GET_TABLE(lut,' + str(lutable_index) + ',0,128)'
    command_str = bytes(command_str, encoding="utf8")
    strCmdIn = create_string_buffer(command_str)
    strCmdOutBuff = ctypes.c_ubyte * 1024
    strCmdOut = strCmdOutBuff()
    retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 0 == retStauts:
        print('\nMCU_GET_TABLE lut {:d} :'.format(lutable_index))
        f.write('\nMCU_GET_TABLE lut {:d} :'.format(lutable_index))
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
    else:
        print("Get lut {} table fail, error code :{:d}".format(lutable_index, retStauts))

def mcu_get_driver_table(drv_table_index):
    command_str = 'MCU_GET_TABLE(driver,' + str(drv_table_index) + ',0,128)'
    command_str = bytes(command_str, encoding="utf8")
    strCmdIn = create_string_buffer(command_str)
    strCmdOutBuff = ctypes.c_ubyte * 1024
    strCmdOut = strCmdOutBuff()
    retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 0 == retStauts:
        print('\nMCU_GET_TABLE driver {:d} :'.format(drv_table_index))
        f.write('\nMCU_GET_TABLE driver {:d} :'.format(drv_table_index))
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
    else:
        print("Get driver {} table fail, error code :{:d}".format(drv_table_index, retStauts))
        f.write("Get driver {} table fail, error code :{:d}".format(drv_table_index, retStauts))

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
print("GPON OLT Basic configuration test, start time : {}".format(dateTime))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nGPON OLT Basic configuration test, start time : {}".format(dateTime))
f.write("\n****************************************************************************")
print("{}".format(testTitle))
f.write('\n'+testTitle)

#########################################################
#                 MCU Get ADC
#########################################################
print("\n")
f.write('\n\n')
for item in range(module_adc_chn_nums):
    mcu_get_adc(item)


#########################################################
#               Adjust  check
#########################################################
print("\n")
f.write('\n\n')
for item in range(module_adjust_chn_nums):
    mcu_get_adjust(item)

#########################################################
#               DAC  check
#########################################################
print("\n")
f.write('\n\n')
for item in range(module_dac_chn_nums):
    mcu_get_dac(item)

#########################################################
#               Lut  check
#########################################################
print("\n")
f.write('\n\n')
for item in range(module_base_talbe_nums):
    mcu_get_base_table(item)

print("\n")
f.write('\n\n')
for item in range(module_drv_table_nums):
    mcu_get_driver_table(item)

print("\n")
f.write('\n\n')
for item in range(module_lutable_nums):
    mcu_get_lut(item)

dateTime = time.strptime(time.asctime())
dateTime = "{:4}-{:02}-{:02} {:02}:{:02}:{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
print("\n****************************************************************************")
print("GPON OLT basic configuration test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nGPON OLT basic configuration test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
f.write("\n****************************************************************************")
#testEvb.AteAllPowerOff()
f.close()

