import ctypes
from ctypes import *
import time
import random
import operator
import sys
import os

path = os.path.dirname(os.path.dirname(__file__))
path = os.path.join(path, 'pyscriptlib')
sys.path.append(path)
from cmdServ import *
from classTestEvb import *

#==============================================================================
# Test times
#==============================================================================
wr_and_rd_times  = 5
# user type for password
is_088_Module = 0
is_other_Module = 1
user_password_type = is_other_Module

# Product list
ComboSfpI2cAddr = [0xA0,0xA2,0xB0,0xB2,0xA4]
SfpI2cAddr = [0xA0,0xA2,0xA4]
XfpI2cAddr = [0xA0,0xA4]

devUsbIndex = 0
devSffChannel = 1
devSfpChannel = 2

SFF_A0_DIRECT = True
SFF_A0_DIRECT_HIGH = True
SFF_A2_DIRECT = True
SFF_A2_DIRECT_HIGH = True
SFF_B0_DIRECT = False
SFF_B0_DIRECT_HIGH = False
SFF_B2_DIRECT = False
SFF_B2_DIRECT_HIGH = False

module_base_talbe_nums = 4+1
module_drv_table_nums = 0+1
module_lutable_nums = 7+1

#########################################################
#               create object
#########################################################
testEvb = cTestEvb(devUsbIndex)

#########################################################
#               Inner Funtion
#########################################################
def i2c_read_sff_table(dev_usb_index, dev_sff_channel, i2c_addr, reg_offset, reg_len):
    i2cReadDataBuff = ctypes.c_ubyte * 128
    i2cRead = i2cReadDataBuff()
    testEvb.objdll.AteIicRandomRead(dev_usb_index, dev_sff_channel, i2c_addr, reg_offset, reg_len, byref(i2cRead))
    for item in range(128):
        print('0x{:02X}'.format(i2cRead[item]), end=',')
        f.write(str(hex(i2cRead[item])) + ',')
    f.write('\n')

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
print("Backup Module Data, start time : {}".format(dateTime))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nBackup Module Data, start time : {}".format(dateTime))
f.write("\n****************************************************************************")
print("{}".format(testTitle))
f.write('\n'+testTitle)

#########################################################
#               Backup A0,A2...
#########################################################
if True == SFF_A0_DIRECT:
    print('\nBackup A0 Direct :')
    f.write('\nBackup A0 Direct :\n')
    i2c_read_sff_table(devUsbIndex, devSffChannel, ComboSfpI2cAddr[0], 0, 128)

if True == SFF_A0_DIRECT_HIGH:
    print('\nBackup A0 Direct High:')
    f.write('\nBackup A0 Direct High:\n')
    i2c_read_sff_table(devUsbIndex, devSffChannel, ComboSfpI2cAddr[0], 128, 128)

if True == SFF_A2_DIRECT:
    print('\nBackup A2 Direct :')
    f.write('\nBackup A2 Direct :\n')
    i2c_read_sff_table(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 0, 96)

if True == SFF_A2_DIRECT_HIGH:
    print('\nBackup A2 Direct High:')
    f.write('\nBackup A2 Direct High:\n')
    i2c_read_sff_table(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 128, 128)

if True == SFF_B0_DIRECT:
    print('\nBackup B0 Direct :')
    f.write('\nBackup B0 Direct :\n')
    i2c_read_sff_table(devUsbIndex, devSffChannel, ComboSfpI2cAddr[2], 0, 128)

if True == SFF_B0_DIRECT_HIGH:
    print('\nBackup B0 Direct High:')
    f.write('\nBackup B0 Direct High:\n')
    i2c_read_sff_table(devUsbIndex, devSffChannel, ComboSfpI2cAddr[2], 128, 128)

if True == SFF_B2_DIRECT:
    print('\nBackup B2 Direct :')
    f.write('\nBackup B2 Direct :\n')
    i2c_read_sff_table(devUsbIndex, devSffChannel, ComboSfpI2cAddr[3], 0, 96)

if True == SFF_B2_DIRECT_HIGH:
    print('\nBackup B2 Direct High:')
    f.write('\nBackup B2 Direct High:\n')
    i2c_read_sff_table(devUsbIndex, devSffChannel, ComboSfpI2cAddr[3], 128, 128)

#########################################################
#               Backup Data Table
#########################################################
print("\n")
f.write('\n\n')
base_tmp_data = []
base_raw_data = []
#base raw base data
print("\nBackup base-table raw data ...")
f.write("\nBackup base-table raw data ...")
for base_index in range(module_base_talbe_nums):
    base_raw_data.append([])
    ret, base_tmp_data = cmd_read_table('base', base_index, 0, 128)
    if 'OK' == ret:
        print('\nMCU_GET_TABLE base {:d} :'.format(base_index))
        f.write('\nMCU_GET_TABLE base {:d} :'.format(base_index))
        #print("data size : {}".format(len(lut_tmp_data)))
        for item in range(len(base_tmp_data)):
            print("0x{:02X}".format(base_tmp_data[item]), end=',')
            f.write("0x{:02X},".format(base_tmp_data[item]))
            base_raw_data[base_index].append(base_tmp_data[item])
    else:
        print("\nBackup base {} table fail".format(base_index))
        f.write("\nBackup base {} table fail".format(base_index))

print("\n")
f.write('\n\n')
drv_tmp_data = []
drv_raw_data = []
#get raw drv data
print("\nBackup driver-table raw data ...")
f.write("\nBackup driver-table raw data ...")
for drv_index in range(module_drv_table_nums):
    drv_raw_data.append([])
    ret, drv_tmp_data = cmd_read_table('driver', drv_index, 0, 128)
    if 'OK' == ret:
        print('\nMCU_GET_TABLE driver {:d} :'.format(drv_index))
        f.write('\nMCU_GET_TABLE driver {:d} :'.format(drv_index))
        #print("data size : {}".format(len(lut_tmp_data)))
        for item in range(len(drv_tmp_data)):
            print("0x{:02X}".format(drv_tmp_data[item]), end=',')
            f.write("0x{:02X},".format(drv_tmp_data[item]))
            drv_raw_data[drv_index].append(drv_tmp_data[item])
    else:
        print("\nBackup driver {} table fail".format(drv_index))
        f.write("\nBackup driver {} table fail".format(drv_index))

print("\n")
f.write('\n\n')
lut_tmp_data = []
lut_raw_data = []
#get raw lut data
print("\nRead lut raw data ...")
f.write("\nRead lut raw data ...")
for lut_index in range(module_lutable_nums):
    lut_raw_data.append([])
    ret, lut_tmp_data = cmd_read_table('lut', lut_index, 0, 128)
    if 'OK' == ret:
        print('\nMCU_GET_TABLE lut {:d} :'.format(lut_index))
        f.write('\nMCU_GET_TABLE lut {:d} :'.format(lut_index))
        #print("data size : {}".format(len(lut_tmp_data)))
        for item in range(len(lut_tmp_data)):
            print("0x{:02X}".format(lut_tmp_data[item]), end=',')
            f.write("0x{:02X},".format(lut_tmp_data[item]))
            lut_raw_data[lut_index].append(lut_tmp_data[item])
    else:
        print("\nread lut {} table fail".format(lut_index))
        f.write("\nread lut {} table fail".format(lut_index))

'''
#restore lut raw data
print("\nRestore lut raw data ...")
f.write("\n\nRestore lut raw data ...")
for lut_index in range(len(lut_raw_data)):
#for lut_index in lut_raw_data:
    #lut_tmp_data = lut_raw_data[lut_index].copy()
    for lut_value in range(len(lut_raw_data[lut_index])):
        lut_tmp_data[lut_value] = lut_raw_data[lut_index][lut_value]
    if 'OK' == cmd_write_lut(lut_index, 0, lut_tmp_data):
        print("lut {} wirting ok!".format(lut_index))
        f.write("\nlut {} wirting ok!".format(lut_index))
    else:
        print("lut {} writing fail!".format(lut_index))
        f.write("\nlut {} writing fail!".format(lut_index))
'''
dateTime = time.strptime(time.asctime())
dateTime = "{:4}-{:02}-{:02} {:02}:{:02}:{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
print("\n****************************************************************************")
print("Backup Module Data, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nBackup Module Data, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
f.write("\n****************************************************************************")
testEvb.AteAllPowerOff()
f.close()

