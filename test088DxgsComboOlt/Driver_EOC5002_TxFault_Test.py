import ctypes
from ctypes import *
import time
import sys
from sys import path
#path.append('./python_lib')
from cmdServ import cmdservdll, Sfp_Factory_Pwd_Entry
from classTestEvb import *
import math

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

# test configure
driver_name = 'EOC5002'
i2c_addr = 0xA8 # driver I2C address
reg_addr_array = [26, 27, 28] # driver txfault register
reg_name_array = ['TX_FAULT_LDBIAS_FTH', 'TX_FAULT_MPD_TH', 'TXFAULT_VF_TH']
reg_length = 1 # threshold register numbers
reg_max_th = [255,255,255]
reg_min_th = [0,0,0,0]
ddmi_i2c_addr = 'B2' # A2 or B2
ddmi_txfault_reg = '110'
#########################################################
#               create object
#########################################################
testEvb = cTestEvb(devUsbIndex)
#########################################################
#               Inner Funtion
#########################################################
def read_A2_TxFault(txfault_reg):
    i2cReadBuf = ctypes.c_ubyte*1
    i2cReadByte = i2cReadBuf()
    res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[1], 110, 1, i2cReadByte)
    if 0 == res:
        TxFaultFlag = 1 if 0x04 == (i2cReadByte[0] & 0x04) else 0
        return TxFaultFlag
    else:
        print("Read A2[{}] fail ".format(txfault_reg))
        f.write("Read A2[{}] fail ".format(txfault_reg))

def read_B2_TxFault(txfault_reg):
    i2cReadBuf = ctypes.c_ubyte*1
    i2cReadByte = i2cReadBuf()
    res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, ComboSfpI2cAddr[3], 110, 1, i2cReadByte)
    if 0 == res:
        TxFaultFlag = 1 if 0x04 == (i2cReadByte[0] & 0x04) else 0
        return TxFaultFlag
    else:
        print("Read B2[{}] fail ".format(txfault_reg))
        f.write("Read B2[{}] fail ".format(txfault_reg))

def binary_SetRegTh(left, right):
    if right >= left:
        mid = int(left + (right - left)/2)
    return mid

def step_SetRegTh(dir, Th, extremum ,step = 10):
    if dir:
        if Th-step >= extremum:
            Th -= step
        else:
            Th = extremum
    else:
        if Th+step <= extremum:
            Th += step
        else:
            Th = extremum
    return Th

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
print("Driver {} TxFault test, start time : {}".format(driver_name, dateTime))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nDriver {} TxFault test, start time : {}".format(driver_name, dateTime))
f.write("\n****************************************************************************")
print("{}".format(testTitle))
f.write('\n'+testTitle)



for item in range(len(reg_addr_array)):
    #read Fault status
    print("\nPOR...")
    f.write("\nPOR...")
    testEvb.AteAllPowerOff()
    time.sleep(1)
    testEvb.AteAllPowerOn()
    time.sleep(1)
    Sfp_Factory_Pwd_Entry(user_password_type)
    time.sleep(1)

    print("\nRead {}[{}] TxFault flag :".format(ddmi_i2c_addr, ddmi_txfault_reg), end = '')
    f.write("\nRead {}[{}] TxFault flag :".format(ddmi_i2c_addr, ddmi_txfault_reg))
    if 'A2' == ddmi_i2c_addr:
        txfaultFlag = read_A2_TxFault(ddmi_txfault_reg)
    else:
        txfaultFlag = read_B2_TxFault(ddmi_txfault_reg)
    print("{}".format(txfaultFlag))
    f.write("{}".format(txfaultFlag))

    command_str = 'MCU_I2C_READ(' + str(i2c_addr) + ',' \
                  + str(reg_addr_array[item]) + ',' \
                  + str(reg_length) + ')'
    command_str = bytes(command_str, encoding="utf8")

    print("\nRead {} Register {} ({}) :".format(driver_name, reg_addr_array[item], reg_name_array[item]), end='')
    f.write("\nRead {} Register {} ({}) :".format(driver_name, reg_addr_array[item], reg_name_array[item]))
    strCmdIn = create_string_buffer(command_str)
    retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 0 == retStauts:
       for getdat in range(4):
            print("{}".format(chr(strCmdOut[getdat])), end='')
            f.write(chr(strCmdOut[getdat]))
    else:
        print("Fail : {0:d}".format(retStauts))
        f.write("Fail : {0:d}".format(retStauts))
    reg_th = strCmdOut[2:4]
    ascii_list = list(reg_th)
    reg_th = int(chr(ascii_list[0]), 16) * 16 + int(chr(ascii_list[1]), 16)
    #print("\n{:2d}".format(reg_th))
    cal_dir = True if reg_th > 0 else False

    while 1 != txfaultFlag:
        #reg_th = reg_th - 1 if cal_dir else reg_th + 1
        #reg_th = binary_SetRegTh(0, reg_th) if cal_dir else binary_SetRegTh(reg_th, 256)
        reg_th = step_SetRegTh(cal_dir, reg_th, reg_min_th[item]) if cal_dir else step_SetRegTh(cal_dir, reg_th, reg_max_th[item])

        print("\nWrite {} Register {} ({}) :0x{:02X}".format(driver_name, reg_addr_array[item], reg_name_array[item], reg_th), end='')
        f.write("\nWrite {} Register {} ({}) :0x{:02X}".format(driver_name, reg_addr_array[item], reg_name_array[item], reg_th))
        command_str = 'MCU_I2C_WRITE(' + str(i2c_addr) + ',' \
                        + str(reg_addr_array[item]) + ',' \
                        + str(reg_th) + ')'
        command_str = bytes(command_str, encoding="utf8")
        strCmdIn = create_string_buffer(command_str)
        retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
        if 0 != retStauts:
            print("{0:d}".format(retStauts))
            f.write(str(retStauts))

        print("\nRead {}[{}] TxFault flag :".format(ddmi_i2c_addr, ddmi_txfault_reg), end='')
        f.write("\nRead {}[{}] TxFault flag :".format(ddmi_i2c_addr, ddmi_txfault_reg))
        if 'A2' == ddmi_i2c_addr:
            txfaultFlag = read_A2_TxFault(ddmi_txfault_reg)
        else:
            txfaultFlag = read_B2_TxFault(ddmi_txfault_reg)
        print("{}".format(txfaultFlag))
        f.write("{}".format(txfaultFlag))
        if reg_th <= reg_min_th[item] or reg_th >= reg_max_th[item]:
            break

    if 1 == txfaultFlag:
        print("{} {} Verity Ok".format(driver_name, reg_name_array[item]))
        f.write("\n{} {} Verity Ok".format(driver_name, reg_name_array[item]))
    else:
        print("{} {} Verity Fail".format(driver_name, reg_name_array[item]))
        f.write("\n{} {} Verity Fail".format(driver_name, reg_name_array[item]))

dateTime = time.strptime(time.asctime())
dateTime = "{:4}-{:02}-{:02} {:02}:{:02}:{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
print("\n****************************************************************************")
print("Driver {} TxFault test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(driver_name, dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nDriver {} TxFault test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(driver_name, dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
f.write("\n****************************************************************************")
testEvb.AteAllPowerOff()
f.close()

