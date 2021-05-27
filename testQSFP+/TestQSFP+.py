import ctypes
from ctypes import *
import time
import random
import operator
from cmdServ import cmdservdll,Sfp_Factory_Pwd_Entry
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

#########################################################
#               create object
#########################################################
testEvb = cTestEvb(devUsbIndex)
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
print("QSFP28 test, start time : {}".format(dateTime))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nQSFP28 test, start time : {}".format(dateTime))
f.write("\n****************************************************************************")
print("{}".format(testTitle))
f.write('\n'+testTitle)
f.close()


#########################################################
#               Test Configuration
#########################################################
#True or False
FW_Basic_Config_Check_TEST = True
Driver_GN25L99_TEST = False
Driver_GN25L96_TEST = False
Driver_UX3320_TEST = True
Password_READ_BACK_TEST = True
A0_WRITE_READ_REPEATED_TEST = True
A0_Page_0_WRITE_READ_REPEATED_TEST = True
TxPower08uW_Alarm_Warning_TEST = False
Tx_Soft_Dis_En_STRESS_TEST = False
Inner_I2C_STRESS_TEST = True
Module_Init_Check_TEST = True
A0_WRITE_READ_STRESS_USERPASSWORD_TEST = False


if True == FW_Basic_Config_Check_TEST:
    os.system('.\TestFWBasicInfo.py')

if True == Driver_GN25L96_TEST:
    os.system('.\Driver_GN25L96_Test.py')

if True == Driver_GN25L99_TEST:
    os.system('.\Driver_GN25L99_Test.py')

if True == Driver_UX3320_TEST:
    os.system('.\Driver_UX3320_Test.py')

if True == Password_READ_BACK_TEST:
    os.system('.\Password_ReadBack_Test.py')

if True == Tx_Soft_Dis_En_STRESS_TEST:
    os.system('.\Tx_Soft_Dis_En_Stress_Test.py')

if True == Inner_I2C_STRESS_TEST:
    os.system('.\InnerI2C_UX3320_Stress_Test.py')

if True == Module_Init_Check_TEST:
    os.system('.\Module_Init_Check_Test.py')

if True == A0_WRITE_READ_STRESS_USERPASSWORD_TEST:
    os.system('.\A0_Direct_Write_Read_Repeated_ByUserpassword_Test.py')

if True == A0_Page_0_WRITE_READ_REPEATED_TEST:
    os.system('.\A0_Direct_High_Write_Read_Repeated_Test.py')

if True == TxPower08uW_Alarm_Warning_TEST:
    os.system('.\Tx08uw_AlarmWarning_Test.py')

# A0 write and read repeated
if True == A0_WRITE_READ_REPEATED_TEST:
    os.system('.\A0_Direct_Write_Read_Repeated_Test.py')

f = open(fileName, 'a+')
dateTime = time.strptime(time.asctime())
dateTime = "{:4}-{:02}-{:02} {:02}:{:02}:{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
print("\n****************************************************************************")
print("QSFP28 test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nQSFP28 test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
f.write("\n****************************************************************************")
testEvb.AteAllPowerOff()
f.close()

