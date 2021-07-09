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

pub_path = os.path.dirname(os.path.dirname(__file__))
pub_path = os.path.join(pub_path, 'public_script')
sys.path.append(pub_path)
from Driver_GN25L96_Class import *

#==============================================================================
#Test times
#==============================================================================
wr_and_rd_times  = 2
# user type for password
is_088_Module = 0
is_other_Module = 1
user_password_type = is_other_Module


#Product list
ComboSfpI2cAddr = [0xA0,0xA2,0xB0,0xB2,0xA4]
SfpI2cAddr = [0xA0,0xA2,0xA4]
XfpI2cAddr = [0xA0,0xA4]

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

# Creating a Class Instance
driveInstance = Driver_GN25L96()
driveInstance.driver_name = 'GN25L96'
driveInstance.driver_addr = 0xA2
driveInstance.driver_reg_map = [0x90, 0x91, 0x92, 0x93, 0x94, 0x96, 0x97, 0x98, 0x99, 0x9A, \
                                0x9B, 0x9C, 0x9D, 0x9E, 0x9F, 0xA0, 0xA1, 0xA2, 0xA3, 0xA4, \
                                0xA5, 0xA6, 0xA7, 0xA8, 0xA9, 0xAA, 0xAB, 0xAC, 0xAD, 0xAE, \
                                0xAF, 0xB0, 0xB1, 0xB3, 0xB4, 0xB5, 0xB6, 0xB7, 0xB8, 0xB9, \
                                0xBB, 0xBC, 0xBD, 0xBE, 0xBF, 0xC0, 0xC1, 0xC2, 0xC3, 0xC4, \
                                0xC5, 0xC6, 0xC7, 0xD6, 0xD7, 0xD8, 0xD9, 0xDA, 0xDB, 0xDC, \
                                0xDD, 0xDE, 0xDF, 0xE0, 0xE1]

driveInstance.apc_reg = 0xA4, 'APC', 1
driveInstance.apc_table = 2, [0x4B,0x02,0x51,0x00,0x5F,0xFF,0x01,0xC4,0x00,0x6C], 1000, 1
driveInstance.mcu_apc_adjust = 6

#需要确认AER是否使能，如果enable就读0xA8，否则读0xA2-0xA3
#driveInstance.aer_reg = 0xA8, 'AER', 1 #AER Enable
driveInstance.aer_reg = 0xA2, 'AER', 2 #AER Disable, use Lut
driveInstance.aer_table = 3, [0x4B,0x00,0x32,0x00,0x0E,0xFF,0x00,0x56,0x00,0x0C], 1000, 1
driveInstance.mcu_aer_adjust = 7

driveInstance.maxmod_reg = 0xA7, 'Max MOD', 1
driveInstance.maxmod_table = 11, [0x60,0x02,0x51,0x00,0x5F,0xFF,0x01,0xC4,0x00,0x6C], 1000, 1
driveInstance.mcu_maxmod_adjust = 10


print("\n****************************************************************************")
print("Driver {} test, start time : {}".format(driveInstance._driver_name, dateTime))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nDriver {} test, start time : {}".format(driveInstance._driver_name, dateTime))
f.write("\n****************************************************************************")
print("{}".format(testTitle))
f.write('\n'+testTitle)

print("\nAt first, reading LUT...")
f.write("\nAt first, reading LUT...")
lut_apc = []
ret, lut_apc = cmd_read_table('lut', driveInstance.apc_table[0], 0, 128)
if 'OK' != ret:
    print("\nCan't read APC LUT")
    f.write("\nCan't read APC LUT")
    sys.exit()
else:
    print("\nFinish reading APC LUT")
    f.write("\nFinish reading APC LUT")

lut_aer = []
ret, lut_aer = cmd_read_table('lut', driveInstance.aer_table[0], 0, 128)
if 'OK' != ret:
    print("\nCan't read AER LUT")
    f.write("\nCan't read AER LUT")
    sys.exit()
else:
    print("\nFinish reading AER LUT")
    f.write("\nFinish reading AER LUT")

lut_max_mod = []
ret, lut_max_mod = cmd_read_table('lut', driveInstance.maxmod_table[0], 0, 96)
if 'OK' != ret:
    print("\nCan't read MAX MOD LUT")
    f.write("\nCan't read MAX MOD LUT")
    sys.exit()
else:
    print("\nFinish reading MAX MOD LUT")
    f.write("\nFinish reading MAX MOD LUT")

read_drv_init_val = True
if True == read_drv_init_val:
    print("\nGet Driver register initial Value:\n")
    f.write('\n\nGet Driver register initial Value:\n')

    for item in range(len(driveInstance.driver_reg_map)):
        command_str = 'MCU_I2C_READ(' + str(driveInstance.driver_addr) + ',' \
                      + str(driveInstance.driver_reg_map[item]) + ',' \
                      + '1)'
        command_str = bytes(command_str, encoding="utf8")
        strCmdIn = create_string_buffer(command_str)
        strCmdOutBuff = ctypes.c_ubyte*4
        strCmdOut = strCmdOutBuff()
        retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
        if 0 == retStauts:
            #print("\n")
            #f.write("\ns")
            print('\n{}[0x{:2X}] = '.format(driveInstance.driver_name, driveInstance.driver_reg_map[item]), end='')
            f.write('\n{}[0x{:2X}] = '.format(driveInstance.driver_name, driveInstance.driver_reg_map[item]))
            for item in range(len(strCmdOut)):
                print("{}".format(chr(strCmdOut[item])), end='')
                f.write(chr(strCmdOut[item]))
        else:
            print("{0:d}".format(retStauts))
            f.write(str(retStauts))

#########################################################
#               Verify GN25L96 APC
#########################################################
print("\n\nNow start realtime adjust {} with mcu temperature".format(driveInstance.apc_reg[1]))
f.write("\n\nNow start realtime adjust {} with mcu temperature".format(driveInstance.apc_reg[1]))

print("Write {} Lut : {}".format(driveInstance.apc_reg[1], driveInstance.apc_table[1]), end='')
f.write("\nWrite {} Lut : {}".format(driveInstance.apc_reg[1], driveInstance.apc_table[1]))
if 'OK' == cmd_write_table('lut', driveInstance.apc_table[0], 0, driveInstance.apc_table[1]):
    strCmdOutBuff = ctypes.c_ubyte * 32
    strCmdOut = strCmdOutBuff()
    strCmdOut = getAdc0()
    if 0 != strCmdOut:
        print("\nADC 0(Hex):", end='')
        f.write("\nADC 0(Hex):")
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
    else:
        print("Can't get ADC 0 ")
        f.write("Can't get ADC 0 ")

    tempIndex = adc02TempIndex(strCmdOut)
    print("\ntempIndex : {}".format(tempIndex))
    f.write("\ntempIndex : {}".format(tempIndex))

    lutable_lis = []
    lutable_list = driveInstance.apc_table[1]
    #print("\n{}".format(apc_table_list))
    adjust_val = 0xFF
    if tempIndex < lutable_list[0]:
        adjust_val = round(tempIndex * (lutable_list[1] * 256 + lutable_list[2]) / \
                     driveInstance.apc_table[2] \
                     + (lutable_list[3]* 256 + lutable_list[4]) / driveInstance.apc_table[3])
    else:
        adjust_val = round(tempIndex * (lutable_list[6] * 256 + lutable_list[7]) / \
                     driveInstance.apc_table[2] \
                     + (lutable_list[8] * 256 + lutable_list[9]) / driveInstance.apc_table[3])
    print("Set {} {} mode,now tempIndex is {}, 0x{:2X} should adjust to '0x{:2X}'".format(driveInstance._driver_name, \
                                                                                            driveInstance.apc_reg[1],
                                                                                            tempIndex,
                                                                                            driveInstance.apc_reg[0],
                                                                                            int(adjust_val)))
    f.write("\nSet {} {} mode,now tempIndex is {}, 0x{:2X} should adjust to '0x{:2X}'".format(driveInstance._driver_name, \
                                                                                            driveInstance.apc_reg[1],
                                                                                            tempIndex,
                                                                                            driveInstance.apc_reg[0],
                                                                                            int(adjust_val)))
    if 'OK' == (driveInstance.cmd_mcu_set_adjust(driveInstance.mcu_apc_adjust, 'A')):
        print("Read {} 0x{:2X} = ".format(driveInstance._driver_name, driveInstance.apc_reg[0]), end='')
        f.write("\nRead {} 0x{:2X} = ".format(driveInstance._driver_name, driveInstance.apc_reg[0]))
        reg_val = []
        ret, reg_val = cmd_read_drv_reg(driveInstance.driver_addr, driveInstance.apc_reg[0], driveInstance.apc_reg[2])
        if 'OK' == ret and (reg_val[0] == int(adjust_val) or reg_val[0] == int(adjust_val)-1 or reg_val == int(adjust_val)+1):
            print("0x{:02X}, OK".format(reg_val[0]), end='')
            f.write("0x{:02X}, OK".format(reg_val[0]))
        else:
            print("0x{:02X}, FAIL".format(reg_val[0]), end='')
            f.write("0x{:02X}, FAIL".format(reg_val[0]))
else:
    print("\nWrite {} Lut Fail.".format(driveInstance.apc_reg[1]), end='')
    f.write("\nWrite {} Lut Fail.".format(driveInstance.apc_reg[1]))
#########################################################
#               Verify GN25L96 Max MOD
#########################################################
print("\n\nNow start realtime adjust {} with mcu temperature".format(driveInstance.maxmod_reg[1]))
f.write("\n\nNow start realtime adjust {} with mcu temperature".format(driveInstance.maxmod_reg[1]))

print("Write {} Lut : {}".format(driveInstance.maxmod_reg[1], driveInstance.maxmod_table[1]), end='')
f.write("\nWrite {} Lut : {}".format(driveInstance.maxmod_reg[1], driveInstance.maxmod_table[1]))
if 'OK' == cmd_write_table('lut', driveInstance.maxmod_table[0], 0, driveInstance.maxmod_table[1]):
    strCmdOutBuff = ctypes.c_ubyte * 32
    strCmdOut = strCmdOutBuff()
    strCmdOut = getAdc0()
    if 0 != strCmdOut:
        print("\nADC 0(Hex):", end='')
        f.write("\nADC 0(Hex):")
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
    else:
        print("Can't get ADC 0 ")
        f.write("Can't get ADC 0 ")

    tempIndex = adc02TempIndex(strCmdOut)
    print("\ntempIndex : {}".format(tempIndex))
    f.write("\ntempIndex : {}".format(tempIndex))
    lutable_list = []
    lutable_list = driveInstance.maxmod_table[1]
    adjust_val = 0xFF
    if tempIndex < lutable_list[0]:
        adjust_val = round(tempIndex * (lutable_list[1] * 256 + lutable_list[2]) / \
                     driveInstance.maxmod_table[2] \
                     + (lutable_list[3] * 256 + lutable_list[4]) / driveInstance.maxmod_table[3])
    else:
        adjust_val = round(tempIndex * (lutable_list[6] * 256 + lutable_list[7]) / \
                     driveInstance.maxmod_table[2] \
                     + (lutable_list[8] * 256 + lutable_list[9]) / driveInstance.maxmod_table[3])
    print("Set {} {} mode,now tempIndex is {}, 0x{:2X} should adjust to '0x{:2X}'".format(driveInstance._driver_name, \
                                                                                            driveInstance.maxmod_reg[1],
                                                                                            tempIndex,
                                                                                            driveInstance.maxmod_reg[0],
                                                                                            int(adjust_val)))
    f.write("\nSet {} {} mode,now tempIndex is {}, 0x{:2X} should adjust to '0x{:2X}'".format(driveInstance._driver_name, \
                                                                                            driveInstance.maxmod_reg[1],
                                                                                            tempIndex,
                                                                                            driveInstance.maxmod_reg[0],
                                                                                            int(adjust_val)))
    if 'OK' == (driveInstance.cmd_mcu_set_adjust(driveInstance.mcu_maxmod_adjust, 'A')):
        print("Read {} 0x{:2X} = ".format(driveInstance._driver_name, driveInstance.maxmod_reg[0]), end='')
        f.write("\nRead {} 0x{:2X} = ".format(driveInstance._driver_name, driveInstance.maxmod_reg[0]))
        reg_val = []
        ret, reg_val = cmd_read_drv_reg(driveInstance.driver_addr, driveInstance.maxmod_reg[0], driveInstance.maxmod_reg[2])
        if 'OK' == ret and (reg_val[0] == int(adjust_val) or reg_val[0] == int(adjust_val)-1 or reg_val == int(adjust_val)+1):
            print("0x{:02X}, OK".format(reg_val[0]), end='')
            f.write("0x{:02X}, OK".format(reg_val[0]))
        else:
            print("0x{:02X}, FAIL".format(reg_val[0]), end='')
            f.write("0x{:02X}, FAIL".format(reg_val[0]))
else:
    print("\nWrite {} Lut Fail. ".format(driveInstance.maxmod_reg[1]), end='')
    f.write("\nWrite {} Lut Fail. ".format(driveInstance.maxmod_reg[1]))

#########################################################
#               Verify GN25L96 AER
#########################################################
print("\n\nNow start realtime adjust {} with mcu temperature".format(driveInstance.aer_reg[1]))
f.write("\n\nNow start realtime adjust {} with mcu temperature".format(driveInstance.aer_reg[1]))

reg_data = []
isAerFlag = 0
ret, reg_data = cmd_read_drv_reg(driveInstance.driver_addr, 0X9D, 1)
if 'OK' == ret:
    isAerFlag = reg_data[0]&0x01
    print("\nRead GN25L96 0x9D, AUTO_ER_EN is {}".format(isAerFlag))
    f.write("\nRead GN25L96 0x9D, AUTO_ER_EN is {}".format(isAerFlag))
else:
    print("\nRead GN25L96 0x9D fail")
    f.write("\nRead GN25L96 0x9D fail")


print("Write {} Lut : {}".format(driveInstance.aer_reg[1], driveInstance.aer_table[1]), end='')
f.write("\nWrite {} Lut : {}".format(driveInstance.apc_reg[1], driveInstance.aer_table[1]))
if 'OK' == cmd_write_table('lut', driveInstance.aer_table[0], 0, driveInstance.aer_table[1]):
    strCmdOutBuff = ctypes.c_ubyte * 32
    strCmdOut = strCmdOutBuff()
    strCmdOut = getAdc0()
    if 0 != strCmdOut:
        print("\nADC 0(Hex):", end='')
        f.write("\nADC 0(Hex):")
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
    else:
        print("Can't get ADC 0 ")
        f.write("Can't get ADC 0 ")

    tempIndex = adc02TempIndex(strCmdOut)
    print("\ntempIndex : {}".format(tempIndex))
    f.write("\ntempIndex : {}".format(tempIndex))
    lutable_list = []
    lutable_list = driveInstance.aer_table[1]

    adjust_val = 0xFF
    if tempIndex < lutable_list[0]:
        adjust_val = round(tempIndex * (lutable_list[1] * 256 + lutable_list[2]) / \
                     driveInstance.aer_table[2] \
                     + (lutable_list[3] * 256 + lutable_list[4]) / driveInstance.aer_table[3])
    else:
        adjust_val = round(tempIndex * (lutable_list[6] * 256 + lutable_list[7]) / \
                     driveInstance.aer_table[2] \
                     + (lutable_list[8] * 256 + lutable_list[9]) / driveInstance.aer_table[3])
    if 1 == isAerFlag:
        adjust_val = int(adjust_val) & 0x3F
    print("Set {} {} mode,now tempIndex is {}, 0x{:2X} should adjust to '0x{:2X}'".format(driveInstance._driver_name, \
                                                                                        driveInstance.aer_reg[1],
                                                                                        tempIndex,
                                                                                        driveInstance.aer_reg[0],
                                                                                        int(adjust_val)))
    f.write("\nSet {} {} mode,now tempIndex is {}, 0x{:2X} should adjust to '0x{:2X}'".format(driveInstance._driver_name, \
                                                                                        driveInstance.aer_reg[1],
                                                                                        tempIndex,
                                                                                        driveInstance.aer_reg[0],
                                                                                        int(adjust_val)))
    if 'OK' == (driveInstance.cmd_mcu_set_adjust(driveInstance.mcu_aer_adjust, 'A')):
        print("Read {} 0x{:2X} = ".format(driveInstance._driver_name, driveInstance.aer_reg[0]), end='')
        f.write("\nRead {} 0x{:2X} = ".format(driveInstance._driver_name, driveInstance.aer_reg[0]))
        reg_val = []
        ret, reg_val = cmd_read_drv_reg(driveInstance.driver_addr, driveInstance.aer_reg[0],
                                        driveInstance.aer_reg[2])
        if 0 == isAerFlag:
            read_reg_val = int((reg_val[0]*256+reg_val[1])/64)
        else:
            read_reg_val = reg_val[0]&0x3F
        if 'OK' == ret and (read_reg_val == int(adjust_val) or read_reg_val == int(adjust_val)-1 or read_reg_val == int(adjust_val)+1):
            print("0x{:02X}, OK".format(read_reg_val), end='')
            f.write("0x{:02X}, OK".format(read_reg_val))
        else:
            print("0x{:02X}, FAIL".format(read_reg_val), end='')
            f.write("0x{:02X} != 0x{:02X}, FAIL".format(read_reg_val))
else:
    print("\nWrite {} Lut Fail.".format(driveInstance.aer_reg[1]), end='')
    f.write("\nWrite {} Lut Fail.".format(driveInstance.aer_reg[1]))

print("\nRestore LUT...")
f.write("\nRestore LUT...")
if 'OK' == cmd_write_table('lut', driveInstance.apc_table[0], 0, lut_apc):
    print("\nFinish restore APC LUT")
    f.write("\nFinish restore APC LUT")
if 'OK' == cmd_write_table('lut', driveInstance.aer_table[0], 0, lut_aer):
    print("\nFinish restore AER LUT")
    f.write("\nFinish restore AER LUT")
if 'OK' == cmd_write_table('lut', driveInstance.maxmod_table[0], 0, lut_max_mod):
    print("\nFinish restore MAX MOD LUT")
    f.write("\nFinish restore MAX MOD LUT")

dateTime = time.strptime(time.asctime())
dateTime = "{:4}-{:02}-{:02} {:02}:{:02}:{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
print("\n****************************************************************************")
print("Driver {} test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(driveInstance._driver_name, dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nDriver {} test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(driveInstance._driver_name, dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
f.write("\n****************************************************************************")
testEvb.AteAllPowerOff()
f.close()

