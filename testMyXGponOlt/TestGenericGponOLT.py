import ctypes
from ctypes import *
import time
import sys
import os

path = os.path.dirname(os.path.dirname(__file__))
path = os.path.join(path, 'pyscriptlib')
sys.path.append(path)
from cmdServ import *
from classTestEvb import *

pub_path = os.path.dirname(os.path.dirname(__file__))
pub_path = os.path.join(pub_path, 'public_script')
sys.path.append(pub_path)


userCode = 351
# Product list
ComboSfpI2cAddr = [0xA0,0xA2,0xB0,0xB2,0xA4]
SfpI2cAddr = [0xA0,0xA2,0xA4]
XfpI2cAddr = [0xA0,0xA4]

devUsbIndex = 0
devSffChannel = 1
devSfpChannel = 2
#########################################################
#               Inner Funtion
#########################################################
def Sfp_User_Pwd_Entry(userCode):
    i2cWriteBuf = c_ubyte * 4
    if 351 == userCode:
        factoryPwd = i2cWriteBuf(0xC0, 0x72, 0x61, 0x79)
    elif 1 == userCode:
        factoryPwd = i2cWriteBuf(0x58, 0x47, 0x54, 0x45)
    testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, 0xA2, 123, 4, byref(factoryPwd))

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
Sfp_User_Pwd_Entry(userCode)
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
print("Generic GPON OLT test, start time : {}".format(dateTime))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nGeneric GPON OLT test, start time : {}".format(dateTime))
f.write("\n****************************************************************************")
print("{}".format(testTitle))
f.write('\n'+testTitle)
f.close()


#########################################################
#               Test Configuration
#########################################################
#True or False
FW_Basic_Config_Check_TEST = True
A0_WRITE_READ_REPEATED_TEST = True
A0_Direct_High_WRITE_READ_REPEATED_TEST = True
A2_WRITE_READ_REPEATED_TEST = True
A2_Direct_High_WRITE_READ_REPEATED_TEST = True
A2_Page02_WRITE_READ_REPEATED_TEST = False
Driver_GN25L99_TEST = False
Driver_GN25L96_TEST = False
Driver_UX3320_TEST = False
Tx_Soft_Dis_En_STRESS_TEST = False
Inner_I2C_STRESS_TEST = False
Password_READ_BACK_TEST = True
Module_Init_Check_TEST = False


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

# A0 write and read repeated
if True == A0_WRITE_READ_REPEATED_TEST:
    os.system('.\A0_Direct_Write_Read_Repeated_Test.py')

if True == A0_Direct_High_WRITE_READ_REPEATED_TEST:
    os.system('.\A0_Direct_High_Write_Read_Repeated_Test.py')

# A2 write and read repeated
if True == A2_WRITE_READ_REPEATED_TEST:
    os.system('.\A2_Direct_Write_Read_Repeated_Test.py')

if True == A2_Direct_High_WRITE_READ_REPEATED_TEST:
    os.system('.\A2_Direct_High_Write_Read_Repeated_Test.py')

if True == A2_Page02_WRITE_READ_REPEATED_TEST:
    os.system('.\A2_Page02_Direct_Write_Read_Repeated_Test.py')

f = open(fileName, 'a+')
dateTime = time.strptime(time.asctime())
dateTime = "{:4}-{:02}-{:02} {:02}:{:02}:{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
print("\n****************************************************************************")
print("Generic GPON OLT test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nGeneric GPON OLT test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
f.write("\n****************************************************************************")
testEvb.AteAllPowerOff()
f.close()

