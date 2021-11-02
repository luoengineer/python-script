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


#Test times
wr_and_rd_times  = 2
# user type for password
is_088_Module = 0
is_other_Module = 1
user_password_type = is_other_Module

userCode = 351
#Product list
ComboSfpI2cAddr = [0xA0,0xA2,0xB0,0xB2,0xA4]
SfpI2cAddr = [0xA0,0xA2,0xA4]
XfpI2cAddr = [0xA0,0xA4]

devUsbIndex = 0
devSffChannel = 1
devSfpChannel = 2

# Driver Base Class
class Driver(object):
    def __int__(self, name):
        self._driver_name = name

    #property driver name
    def getDriverName(self):
        return  self._driver_name
    def setDriverName(self, name):
        self._driver_name = name
    driver_name = property(getDriverName, setDriverName)

    #property driver i2c address
    def getDriverAddr(self):
        return  self._driver_addr
    def setDriverAddr(self, address):
        self._driver_addr = address
    driver_addr = property(getDriverAddr, setDriverAddr)

    # property driver registers
    def getDriverRegMap(self):
        return self._driver_reg_map
    def setDriverRegMap(self, regmap):
        self._driver_reg_map = regmap
    driver_reg_map = property(getDriverRegMap, setDriverRegMap)

# Driver : GN25L96, ONET1131, GN7153B ...
class Driver_GN25L96(Driver):
    def __int__(self, name):
        self._driver_name = name

    # property adjust reg : 0xA4, 'APC'
    def getAPCReg(self):
        return self._apc_reg, self._apc_reg_name, self._apc_reg_len
    def setAPCReg(self, apc_reg):
        self._apc_reg, self._apc_reg_name, self._apc_reg_len = apc_reg
    apc_reg = property(getAPCReg, setAPCReg)

    def getAERReg(self):
        return self._aer_reg, self._aer_reg_name, self._aer_reg_len
    def setAERReg(self, aer_reg):
        self._aer_reg, self._aer_reg_name, self._aer_reg_len = aer_reg
    aer_reg = property(getAERReg, setAERReg)

    def getMaxMODReg(self):
        return self._maxmod_reg, self._maxmod_reg_name, self._maxmod_reg_len
    def setMaxMODReg(self, maxmod_reg):
        self._maxmod_reg, self._maxmod_reg_name, self._maxmod_reg_len = maxmod_reg
    maxmod_reg = property(getMaxMODReg, setMaxMODReg)

    # property apc table
    def getAPCTable(self):
        return self._apc_table_index, self._apc_table_dat, self._apc_slop, self._apc_offset
    def setAPCTable(self, apc_table):
        self._apc_table_index, self._apc_table_dat, self._apc_slop, self._apc_offset = apc_table
    apc_table = property(getAPCTable, setAPCTable)

    # property aer table
    def getAERTable(self):
        return self._aer_table_index, self._aer_table_dat, self._aer_slop, self._aer_offset
    def setAERTable(self, aer_table):
        self._aer_table_index, self._aer_table_dat, self._aer_slop, self._aer_offset = aer_table
    aer_table = property(getAERTable, setAERTable)

    # property maxmod table
    def getMaxMODTable(self):
        return self._maxmod_table_index, self._maxmod_table_dat, self._maxmod_slop, self._maxmod_offset
    def setMaxMODTable(self, maxmod_table):
        self._maxmod_table_index, self._maxmod_table_dat, self._maxmod_slop, self._maxmod_offset = maxmod_table
    maxmod_table = property(getMaxMODTable, setMaxMODTable)

    # property mcu apc adjust index
    def getMcuAPCIndex(self):
        return self._mcu_apc_adjust
    def setMcuAPCIndex(self, index):
        self._mcu_apc_adjust = index
    mcu_apc_adjust = property(getMcuAPCIndex, setMcuAPCIndex)

    # property mcu aer index
    def getMcuAERIndex(self):
        return self._mcu_aer_adjust
    def setMcuAERIndex(self, index):
        self._mcu_aer_adjust = index
    mcu_aer_adjust = property(getMcuAERIndex, setMcuAERIndex)

    # property mcu maxmod index
    def getMcuMaxMODIndex(self):
        return self._mcu_maxmod_adjust
    def setMcuMaxMODIndex(self, index):
        self._mcu_maxmod_adjust = index
    mcu_maxmod_adjust = property(getMcuMaxMODIndex, setMcuMaxMODIndex)

    #function
    def cmd_write_lut(self, lookupTable):
        command_str = 'MCU_SET_TABLE(LUT' + ',' + str(lookupTable[0]) + ',0,' \
                      + str(lookupTable[1]) + ')'
        command_str = bytes(command_str, encoding="utf8")
        strCmdIn = create_string_buffer(command_str)
        strCmdOutBuff = ctypes.c_ubyte * 8
        strCmdOut = strCmdOutBuff()
        cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
        ret = chr(strCmdOut[0]) + chr(strCmdOut[1])
        return  ret

    def cmd_mcu_set_adjust(self, adjust_index, adjust_mode):
        command_str = 'MCU_SET_ADJUST(' + str(adjust_index) + ',' \
                      + adjust_mode + ', 0, 0, 0, 0)'
        command_str = bytes(command_str, encoding="utf8")
        strCmdIn = create_string_buffer(command_str)
        strCmdOutBuff = ctypes.c_ubyte * 8
        strCmdOut = strCmdOutBuff()
        cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
        ret = chr(strCmdOut[0]) + chr(strCmdOut[1])
        return ret

    def cmd_mcu_i2c_read(self, drv_addr, reg_addr, reg_len):
        command_str = 'MCU_I2C_READ(' + str(drv_addr) + ',' \
                      + str(reg_addr) + ',' \
                      + str(reg_len) + ')'
        command_str = bytes(command_str, encoding="utf8")
        strCmdIn = create_string_buffer(command_str)
        strCmdOutBuff = ctypes.c_ubyte * 8
        strCmdOut = strCmdOutBuff()
        cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
        return strCmdOut

#########################################################
#               create object
#########################################################
testEvb = cTestEvb(devUsbIndex)


#########################################################
#               Inner Funtion
#########################################################
def Sfp_User_Pwd_Entry(userCode):
    i2cWriteBuf = c_ubyte * 4
    if 351 == userCode:
        factoryPwd = i2cWriteBuf(0x20, 0x14, 0x05, 0x29)
    elif 1 == userCode:
        factoryPwd = i2cWriteBuf(0x58, 0x47, 0x54, 0x45)
    testEvb.objdll.AteIicRandomWrite(devUsbIndex, devSffChannel, 0xA2, 123, 4, byref(factoryPwd))
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
driveInstance.apc_table = 2, "0x4B,0x02,0x51,0x00,0x5F,0xFF,0x01,0xC4,0x00,0x6C", 1000, 1
driveInstance.mcu_apc_adjust = 4

driveInstance.aer_reg = 0xA8, 'AER', 1
driveInstance.aer_table = 6, "0x4B,0x00,0x00,0xFF,0xE8,0xFF,0x00,0x00,0xFF,0xE8", 1000, 1
driveInstance.mcu_aer_adjust = 7

driveInstance.maxmod_reg = 0xA7, 'Max MOD', 1
driveInstance.maxmod_table = 7, "0x60,0x02,0x51,0x00,0x5F,0xFF,0x01,0xC4,0x00,0x6C", 1000, 1
driveInstance.mcu_maxmod_adjust = 2


print("\n****************************************************************************")
print("driver {} test, start time : {}".format(driveInstance._driver_name, dateTime))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\ndriver {} test, start time : {}".format(driveInstance._driver_name, dateTime))
f.write("\n****************************************************************************")
print("{}".format(testTitle))
f.write('\n'+testTitle)

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
if 'OK' == driveInstance.cmd_write_lut(driveInstance.apc_table):
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

    lutable_list = driveInstance.apc_table[1].split(",")
    #print("\n{}".format(apc_table_list))

    if tempIndex < int(lutable_list[0], 16):
        adjust_val = tempIndex * (int(lutable_list[1], 16) * 256 + int(lutable_list[2], 16)) / \
                     driveInstance.apc_table[2] \
                     + (int(lutable_list[3],16) * 256 + int(lutable_list[4],16)) / driveInstance.apc_table[3]
    else:
        adjust_val = tempIndex * (int(lutable_list[6], 16) * 256 + int(lutable_list[7], 16)) / \
                     driveInstance.apc_table[2] \
                     + (int(lutable_list[8], 16) * 256 + int(lutable_list[9], 16)) / driveInstance.apc_table[3]
    #print("adjust val = 0x{:2X}".format(int(adjust_val)))
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
        strCmdOut = driveInstance.cmd_mcu_i2c_read(driveInstance.driver_addr, driveInstance.apc_reg[0],
                                                   driveInstance.apc_reg[2])
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
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
if 'OK' == (driveInstance.cmd_write_lut(driveInstance.maxmod_table)):
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

    lutable_list = driveInstance.maxmod_table[1].split(",")

    if tempIndex < int(lutable_list[0], 16):
        adjust_val = tempIndex * (int(lutable_list[1], 16) * 256 + int(lutable_list[2], 16)) / \
                     driveInstance.maxmod_table[2] \
                     + (int(lutable_list[3],16) * 256 + int(lutable_list[4],16)) / driveInstance.maxmod_table[3]
    else:
        adjust_val = tempIndex * (int(lutable_list[6], 16) * 256 + int(lutable_list[7], 16)) / \
                     driveInstance.maxmod_table[2] \
                     + (int(lutable_list[8], 16) * 256 + int(lutable_list[9], 16)) / driveInstance.maxmod_table[3]
    #print("adjust val = 0x{:2X}".format(int(adjust_val)))
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
        strCmdOut = driveInstance.cmd_mcu_i2c_read(driveInstance.driver_addr, driveInstance.maxmod_reg[0],
                                                   driveInstance.maxmod_reg[2])
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
else:
    print("\nWrite {} Lut Fail. ".format(driveInstance.maxmod_reg[1]), end='')
    f.write("\nWrite {} Lut Fail. ".format(driveInstance.maxmod_reg[1]))

#########################################################
#               Verify GN25L96 AER
#########################################################
print("\n\nNow start realtime adjust {} with mcu temperature".format(driveInstance.aer_reg[1]))
f.write("\n\nNow start realtime adjust {} with mcu temperature".format(driveInstance.aer_reg[1]))

print("Write {} Lut : {}".format(driveInstance.aer_reg[1], driveInstance.aer_table[1]), end='')
f.write("\nWrite {} Lut : {}".format(driveInstance.apc_reg[1], driveInstance.aer_table[1]))
if 'OK' == driveInstance.cmd_write_lut(driveInstance.aer_table):
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

    lutable_list = driveInstance.aer_table[1].split(",")
    #print("\n{}".format(apc_table_list))

    if tempIndex < int(lutable_list[0], 16):
        adjust_val = tempIndex * (int(lutable_list[1], 16) * 256 + int(lutable_list[2], 16)) / \
                     driveInstance.aer_table[2] \
                     + (int(lutable_list[3],16) * 256 + int(lutable_list[4], 16)) / driveInstance.aer_table[3]
    else:
        adjust_val = tempIndex * (int(lutable_list[6], 16) * 256 + int(lutable_list[7], 16)) / \
                     driveInstance.aer_table[2] \
                     + (int(lutable_list[8], 16) * 256 + int(lutable_list[9], 16)) / driveInstance.aer_table[3]
    adjust_val = int(adjust_val) & 0x3F
    #print("adjust val = 0x{:2X}".format(int(adjust_val)))
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
        strCmdOut = driveInstance.cmd_mcu_i2c_read(driveInstance.driver_addr, driveInstance.aer_reg[0],
                                                   driveInstance.aer_reg[2])
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
else:
    print("\nWrite {} Lut Fail.".format(driveInstance.aer_reg[1]), end='')
    f.write("\nWrite {} Lut Fail.".format(driveInstance.aer_reg[1]))



dateTime = time.strptime(time.asctime())
dateTime = "{:4}-{:02}-{:02} {:02}:{:02}:{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
print("\n****************************************************************************")
print("driver {} test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(driveInstance._driver_name, dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\ndriver {} test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(driveInstance._driver_name, dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
f.write("\n****************************************************************************")
testEvb.AteAllPowerOff()
f.close()

