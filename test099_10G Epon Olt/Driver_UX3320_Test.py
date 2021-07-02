import ctypes
from ctypes import *
import time
<<<<<<< HEAD
import sys
from sys import path
from cmdServ import cmdservdll, Sfp_Factory_Pwd_Entry, getAdc0, adc02TempIndex
from classTestEvb import *
=======
from cmdServ import cmdservdll, devUsbIndex
from cmdServ import Sfp_Factory_Pwd_Entry, AteAllPowerOn, AteAllPowerOff, openUsbDevice
>>>>>>> 2da87054d45d32a3addd32c95e9cb15ab0fa91ac


#Test times
wr_and_rd_times  = 2
# user type for password
is_088_Module = 0
is_other_Module = 1
user_password_type = is_other_Module


#Product list
ComboSfpI2cAddr = [0xA0,0xA2,0xB0,0xB2,0xA4]
SfpI2cAddr = [0xA0,0xA2,0xA4]
XfpI2dAddr = [0xA0,0xA4]

<<<<<<< HEAD
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
class Driver_UX3320(Driver):
    def __int__(self, name):
        self._driver_name = name
    # property adjust reg : 0x8C-0x8D, 'APC'
    def getAPCReg(self):
        return self._apc_reg_1, self._apc_reg_2, self._apc_reg_name, self._apc_reg_len
    def setAPCReg(self, apc_reg):
        self._apc_reg_1, self._apc_reg_2, self._apc_reg_name, self._apc_reg_len = apc_reg
    apc_reg = property(getAPCReg, setAPCReg)

    def getModReg(self):
        return self._mod_reg_1, self._mod_reg_2, self._mod_reg_name, self._mod_reg_len
    def setModReg(self, mod_reg):
        self._mod_reg_1, self._mod_reg_2, self._mod_reg_name, self._mod_reg_len = mod_reg
    aer_reg = property(getModReg, setModReg)

   

    # property apc table
    def getAPCTable(self):
        return self._apc_table_index, self._apc_table_dat, self._apc_slop, self._apc_offset
    def setAPCTable(self, apc_table):
        self._apc_table_index, self._apc_table_dat, self._apc_slop, self._apc_offset = apc_table
    apc_table = property(getAPCTable, setAPCTable)

    # property mod table
    def getMODTable(self):
        return self._mod_table_index, self._mod_table_dat, self._mod_slop, self._mod_offset
    def setMODTable(self, mod_table):
        self._mod_table_index, self._mod_table_dat, self._mod_slop, self._mod_offset = mod_table
    aer_table = property(getMODTable, setMODTable)


    # property mcu apc adjust index
    def getMcuAPCIndex(self):
        return self._mcu_apc_adjust
    def setMcuAPCIndex(self, index):
        self._mcu_apc_adjust = index
    mcu_apc_adjust = property(getMcuAPCIndex, setMcuAPCIndex)

    # property mcu mod index
    def getMcuMODIndex(self):
        return self._mcu_mod_adjust
    def setMcuMODIndex(self, index):
        self._mcu_mod_adjust = index
    mcu_mod_adjust = property(getMcuMODIndex, setMcuMODIndex)

    # property mcu maxmod index

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
=======
#########################################################
#               Subroutines
#########################################################

>>>>>>> 2da87054d45d32a3addd32c95e9cb15ab0fa91ac

#########################################################
#               Open USB Device
#########################################################
<<<<<<< HEAD
testEvb.openUsbDevice()
=======
openUsbDevice(devUsbIndex)
>>>>>>> 2da87054d45d32a3addd32c95e9cb15ab0fa91ac

#########################################################
#               Slot Power On
#########################################################
<<<<<<< HEAD
testEvb.AteAllPowerOn()
=======
AteAllPowerOn(devUsbIndex)
>>>>>>> 2da87054d45d32a3addd32c95e9cb15ab0fa91ac
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
<<<<<<< HEAD
    strFwVer = [chr(strCmdOut[item]) for item in range(len(strCmdOut)) if 0 != strCmdOut[item]]
else:
    print("Can't get firmware version, stop test ! ")
    sys.exit()
=======
    for item in range(len(strCmdOut)):
        if 0x00 != strCmdOut[item]:
            #print("{}".format(chr(strCmdOut[item])), end='')
            strFwVer.append(chr(strCmdOut[item]))
    else:
        print("{0:d}".format(retStauts))

>>>>>>> 2da87054d45d32a3addd32c95e9cb15ab0fa91ac
strFwVer = ''.join(strFwVer)


#########################################################
#                 Open File
#########################################################
<<<<<<< HEAD
startTick = time.time()
dateTime = time.strptime(time.asctime( time.localtime(startTick)))
dateTime = "{:4}-{:02}-{:02} {:02}:{:02}:{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
testTitle = strFwVer
fileName = strFwVer+'.txt'
f = open(fileName, 'a+')
time.sleep(1)

# Creating a Class Instance
driveInstance = Driver_UX3320()
driveInstance.driver_name = 'UX3320'
driveInstance.driver_addr = 0xA2
driveInstance.driver_reg_map = [0x80, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x8A, 0x8C, \
                                0x8D, 0xDC, 0xB8, 0xB9, 0xBA, 0xBB, 0xBC, 0xBD, 0xBE, 0xBF, \
                                0xA8, 0xA9, 0xAA, 0xAB, 0xAC, 0xAD, 0xAE, 0xAF, 0xB0, 0xB1, \
                                0xB2, 0xB3, 0xD1, 0xB4, 0xB5, 0xB6, 0xB7]
driveInstance.apc_reg = 0x8C, 0x8D, 'APC', 2
driveInstance.apc_table = 2, "0x4B,0x00,0x00,0x00,0x58,0xFF,0x00,0x00,0x00,0x58", 1000, 1
driveInstance.mcu_apc_adjust = 4
driveInstance.mod_reg = 0x87, 0x88, 'MOD', 2
driveInstance.mod_table = 3, "0x60,0x02,0x51,0x00,0x5F,0xFF,0x01,0xC4,0x00,0x6C", 1000, 1
driveInstance.mcu_mod_adjust = 5
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
=======
dateTime = time.strptime(time.asctime())
dateTime = "{:4}{:02}{:02}{:02}{:02}{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
testTitle = strFwVer+'@'+dateTime
fileName = strFwVer+'.txt'
f = open(fileName, 'a+')
time.sleep(1)
print("{}".format(testTitle))
f.write('\n\n'+testTitle)

print("\nGet Driver register initial Value:\n")
f.write('\n\nGet Driver register initial Value:\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0x80,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_I2C_READ 0xA2 0x80 8 :')
    f.write('MCU_I2C_READ 0xA2 0x80 8 :')
    for item in range(46):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0x88,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_I2C_READ 0xA2 0x88 8 :')
    f.write('MCU_I2C_READ 0xA2 0x88 8 :')
    for item in range(46):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0xA8,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_I2C_READ 0xA2 0xA8 8 :')
    f.write('MCU_I2C_READ 0xA2 0xA8 8 :')
    for item in range(46):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0xB0,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_I2C_READ 0xA2 0xB0 8 :')
    f.write('MCU_I2C_READ 0xA2 0xB0 8 :')
    for item in range(46):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0xB8,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_I2C_READ 0xA2 0xB8 8 :')
    f.write('MCU_I2C_READ 0xA2 0xB8 8 :')
    for item in range(46):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0xD1,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_I2C_READ 0xA2 0xD1 8 :')
    f.write('MCU_I2C_READ 0xA2 0xD1 8 :')
    for item in range(46):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0xDC,8)')
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print('MCU_I2C_READ 0xA2 0xDC 8 :')
    f.write('MCU_I2C_READ 0xA2 0xDC 8 :')
    for item in range(46):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

>>>>>>> 2da87054d45d32a3addd32c95e9cb15ab0fa91ac

#########################################################
#               Verify UX3320 APC
#########################################################
<<<<<<< HEAD
print("\n\nNow start realtime adjust {} with mcu temperature".format(driveInstance.apc_reg[2]))
f.write("\n\nNow start realtime adjust {} with mcu temperature".format(driveInstance.apc_reg[2]))

print("Write {} Lut : {}".format(driveInstance.apc_reg[2], driveInstance.apc_table[1]), end='')
f.write("\nWrite {} Lut : {}".format(driveInstance.apc_reg[2], driveInstance.apc_table[1]))
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
    adjust_val_1  =  int(adjust_val)>>2
    adjust_val_2 =   int(adjust_val) & 0x03
    #print("adjust val = 0x{:2X}".format(int(adjust_val)))
    print("Set {} {} mode,now tempIndex is {}, 0x{:2X}-0x{:2X} should adjust to '0x{:0>2X}', '0x{:0>2X}'".format(driveInstance._driver_name, \
                                                                                            driveInstance.apc_reg[2],
                                                                                            tempIndex,
                                                                                            driveInstance.apc_reg[0],
                                                                                            driveInstance.apc_reg[1],
                                                                                            adjust_val_1, adjust_val_2))
    f.write("\nSet {} {} mode,now tempIndex is {}, 0x{:2X}-0x{:2X} should adjust to '0x{:0>2X}', '0x{:0>2X}'".format(driveInstance._driver_name, \
                                                                                            driveInstance.apc_reg[2],
                                                                                            tempIndex,
                                                                                            driveInstance.apc_reg[0],
                                                                                            driveInstance.apc_reg[1],
                                                                                            adjust_val_1, adjust_val_2))
    if 'OK' == (driveInstance.cmd_mcu_set_adjust(driveInstance.mcu_apc_adjust, 'A')):
        print("Read {} 0x{:2X},0x{:2X} = ".format(driveInstance._driver_name, driveInstance.apc_reg[0], driveInstance.apc_reg[1]), end='')
        f.write("\nRead {} 0x{:2X},0x{:2X} = ".format(driveInstance._driver_name, driveInstance.apc_reg[0], driveInstance.apc_reg[1]))
        strCmdOut = driveInstance.cmd_mcu_i2c_read(driveInstance.driver_addr, driveInstance.apc_reg[0],
                                                   driveInstance.apc_reg[3])
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
else:
    print("\nWrite {} Lut Fail.".format(driveInstance.apc_reg[2]), end='')
    f.write("\nWrite {} Lut Fail.".format(driveInstance.apc_reg[2]))


########################################################
#               Verify UX3320 MOD
#########################################################
print("\n\nNow start realtime adjust {} with mcu temperature".format(driveInstance.mod_reg[2]))
f.write("\n\nNow start realtime adjust {} with mcu temperature".format(driveInstance.mod_reg[2]))

print("Write {} Lut : {}".format(driveInstance.mod_reg[2], driveInstance.mod_table[1]), end='')
f.write("\nWrite {} Lut : {}".format(driveInstance.mod_reg[2], driveInstance.mod_table[1]))
if 'OK' == driveInstance.cmd_write_lut(driveInstance.mod_table):
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

    lutable_list = driveInstance.mod_table[1].split(",")
    #print("\n{}".format(apc_table_list))

    if tempIndex < int(lutable_list[0], 16):
        adjust_val = tempIndex * (int(lutable_list[1], 16) * 256 + int(lutable_list[2], 16)) / \
                     driveInstance.mod_table[2] \
                     + (int(lutable_list[3],16) * 256 + int(lutable_list[4],16)) / driveInstance.mod_table[3]
    else:
        adjust_val = tempIndex * (int(lutable_list[6], 16) * 256 + int(lutable_list[7], 16)) / \
                     driveInstance.mod_table[2] \
                     + (int(lutable_list[8], 16) * 256 + int(lutable_list[9], 16)) / driveInstance.mod_table[3]
    adjust_val_1  =  int(adjust_val)>>2
    adjust_val_2 =   int(adjust_val) & 0x03
    #print("adjust val = 0x{:2X}".format(int(adjust_val)))
    print("Set {} {} mode,now tempIndex is {}, 0x{:2X}-0x{:2X} should adjust to '0x{:0>2X}', '0x{:0>2X}'".format(driveInstance._driver_name, \
                                                                                            driveInstance.mod_reg[2],
                                                                                            tempIndex,
                                                                                            driveInstance.mod_reg[0],
                                                                                            driveInstance.mod_reg[1],
                                                                                            adjust_val_1, adjust_val_2))
    f.write("\nSet {} {} mode,now tempIndex is {}, 0x{:2X}-0x{:2X} should adjust to '0x{:0>2X}', '0x{:0>2X}'".format(driveInstance._driver_name, \
                                                                                            driveInstance.mod_reg[2],
                                                                                            tempIndex,
                                                                                            driveInstance.mod_reg[0],
                                                                                            driveInstance.mod_reg[1],
                                                                                            adjust_val_1, adjust_val_2))
    if 'OK' == (driveInstance.cmd_mcu_set_adjust(driveInstance.mcu_mod_adjust, 'A')):
        print("Read {} 0x{:2X},0x{:2X} = ".format(driveInstance._driver_name, driveInstance.mod_reg[0], driveInstance.mod_reg[1]), end='')
        f.write("\nRead {} 0x{:2X},0x{:2X} = ".format(driveInstance._driver_name, driveInstance.mod_reg[0], driveInstance.mod_reg[1]))
        strCmdOut = driveInstance.cmd_mcu_i2c_read(driveInstance.driver_addr, driveInstance.mod_reg[0],
                                                   driveInstance.mod_reg[3])
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
else:
    print("\nWrite {} Lut Fail.".format(driveInstance.mod_reg[2]), end='')
    f.write("\nWrite {} Lut Fail.".format(driveInstance.mod_reg[2]))

dateTime = time.strptime(time.asctime())
dateTime = "{:4}-{:02}-{:02} {:02}:{:02}:{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
print("\n****************************************************************************")
print("driver {} test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(driveInstance._driver_name, dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\ndriver {} test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(driveInstance._driver_name, dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
f.write("\n****************************************************************************")
testEvb.AteAllPowerOff()
=======
print("\nUX3320 APC auto mode, UX3320 8C-8Dh adjust to '0x58'")
f.write("\n\nUX3320 APC auto mode, UX3320 8C-8Dh adjust to '0x58'\n")
strCmdIn = create_string_buffer(b'MCU_SET_TABLE(LUT,2,0,0x4B,0x00,0x00,0x00,0x58,0xFF,0x00,0x00,0x00,0x58)')
f.write(repr(strCmdIn.value)+'\n')
strCmdOutBuff = ctypes.c_ubyte*8
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0])+chr(strCmdOut[1]):
    # TODO: first read back,then hold target,max,miin
    strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(4, A, 0, 0, 0, 0)')
    f.write(repr(strCmdIn.value)+'\n')
    time.sleep(1)
    strCmdOutBuff = ctypes.c_ubyte * 8
    strCmdOut = strCmdOutBuff()
    cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
        strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0x8C,2)')
        print(repr(strCmdIn.value)+'\n')
        f.write(repr(strCmdIn.value)+'\n')
        strCmdOutBuff = ctypes.c_ubyte * 10
        strCmdOut = strCmdOutBuff()
        cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
        print("\n[8C-8D]=0x{:2X}".format((int(chr(list(strCmdOut)[2]), 16)*16+int(chr(list(strCmdOut)[3]), 16))*4 + (int(chr(list(strCmdOut)[7]), 16)*16+int(chr(list(strCmdOut)[8]), 16))))
        f.write("\n[8C-8D]=0x{:2X}".format((int(chr(list(strCmdOut)[2]), 16)*16+int(chr(list(strCmdOut)[3]), 16))*4 + (int(chr(list(strCmdOut)[7]), 16)*16+int(chr(list(strCmdOut)[8]), 16))))

print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_ADC(0)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print("ADC 0(Hex):")
    f.write('MCU_GET_ADC 0 :')
    tempCmdOut = strCmdOut[2:4]
    strCmdOut[2:4] = strCmdOut[4:6]
    strCmdOut[4:6] = tempCmdOut
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

ascii_list = list(strCmdOut)
tempIndex = int(chr(ascii_list[4]), 16)*16+int(chr(ascii_list[5]), 16)
print("\ntempIndex : {}".format(tempIndex))

if tempIndex < 0x60:
    print("\nUX3320 APC auto mode,now tempIndex is {}, UX3320 8C-8Dh should adjust to '0x{:2X}'".format(tempIndex,int(
        tempIndex*int('0x151',16)/1000+int('0x5F',16))))
    f.write("\nUX3320 APC auto mode,now tempIndex is {}, UX3320 8C-8Dh should adjust to '0x{:2X}'".format(tempIndex,int(
        tempIndex*int('0x151',16)/1000+int('0x5F',16))))
else:
    print("\nUX3320 Mod auto mode,now tempIndex is {}, UX3320 87-88h should adjust to '0x{:2X}'".format(tempIndex, int(
        tempIndex * int('0x2C4', 16) / 1000 + int('0x6C', 16))))
    f.write("\nUX3320 Mod Max auto mode,now tempIndex is {}, UX3320 87-88h should adjust to '0x{:2X}'".format(tempIndex, int(
        tempIndex * int('0x2C4', 16) / 1000 + int('0x6C', 16))))
f.write("\n")
strCmdIn = create_string_buffer(b'MCU_SET_TABLE(LUT,2,0,0x60,0x01,0x51,0x00,0x5F,0xFF,0x02,0xC4,0x00,0x6C)')
f.write(repr(strCmdIn.value)+'\n')
strCmdOutBuff = ctypes.c_ubyte*8
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0])+chr(strCmdOut[1]):
    # TODO: first read back,then hold target,max,miin
    strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(4, A, 0, 0, 0, 0)')
    print(repr(strCmdIn.value)+'\n')
    f.write(repr(strCmdIn.value)+'\n')
    time.sleep(1)
    strCmdOutBuff = ctypes.c_ubyte * 8
    strCmdOut = strCmdOutBuff()
    cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
        strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0x8C,2)')
        f.write(repr(strCmdIn.value)+'\n')
        strCmdOutBuff = ctypes.c_ubyte * 10
        strCmdOut = strCmdOutBuff()
        cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
        print("\n[8C-8D]=0x{:2X}".format(
            (int(chr(list(strCmdOut)[2]), 16) * 16 + int(chr(list(strCmdOut)[3]), 16)) * 4 + (
                        int(chr(list(strCmdOut)[7]), 16) * 16 + int(chr(list(strCmdOut)[8]), 16))))
        f.write("\n[8C-8D]=0x{:2X}".format(
            (int(chr(list(strCmdOut)[2]), 16) * 16 + int(chr(list(strCmdOut)[3]), 16)) * 4 + (
                        int(chr(list(strCmdOut)[7]), 16) * 16 + int(chr(list(strCmdOut)[8]), 16))))
#########################################################
#               Verify UX3320 Mod
#########################################################
print("\nUX3320 Mod auto mode, UX3320 87-88h adjust to '0x38'")
f.write("\n\nUX3320 Mod auto mode, UX3320 87-88h adjust to '0x38'\n")
strCmdIn = create_string_buffer(b'MCU_SET_TABLE(LUT,3,0,0x4B,0x00,0x00,0x00,0x38,0xFF,0x00,0x00,0x00,0x38)')
f.write(repr(strCmdIn.value)+'\n')
strCmdOutBuff = ctypes.c_ubyte*8
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0])+chr(strCmdOut[1]):
    # TODO: first read back,then hold target,max,miin
    strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(5, A, 0, 0, 0, 0)')
    f.write(repr(strCmdIn.value)+'\n')
    time.sleep(1)
    strCmdOutBuff = ctypes.c_ubyte * 8
    strCmdOut = strCmdOutBuff()
    cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
        strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0x87,2)')
        print(repr(strCmdIn.value)+'\n')
        f.write(repr(strCmdIn.value)+'\n')
        strCmdOutBuff = ctypes.c_ubyte * 10
        strCmdOut = strCmdOutBuff()
        cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
    print("\n[87-88]=0x{:2X}".format(
        (int(chr(list(strCmdOut)[2]), 16) * 16 + int(chr(list(strCmdOut)[3]), 16)) * 4 + (
                int(chr(list(strCmdOut)[7]), 16) * 16 + int(chr(list(strCmdOut)[8]), 16))))
    f.write("\n[87-88]=0x{:2X}".format(
        (int(chr(list(strCmdOut)[2]), 16) * 16 + int(chr(list(strCmdOut)[3]), 16)) * 4 + (
                int(chr(list(strCmdOut)[7]), 16) * 16 + int(chr(list(strCmdOut)[8]), 16))))
print("\n")
f.write('\n\n')
strCmdIn = create_string_buffer(b'MCU_GET_ADC(0)')
strCmdOutBuff = ctypes.c_ubyte*32
strCmdOut = strCmdOutBuff()
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    print("ADC 0(Hex):")
    f.write('MCU_GET_ADC 0 :')
    tempCmdOut = strCmdOut[2:4]
    strCmdOut[2:4] = strCmdOut[4:6]
    strCmdOut[4:6] = tempCmdOut
    for item in range(len(strCmdOut)):
        print("{}".format(chr(strCmdOut[item])), end='')
        f.write(chr(strCmdOut[item]))
        #print("{}".format(ascii2hex(strCmdOut[item])))
else:
    print("{0:d}".format(retStauts))
    f.write(str(retStauts))

ascii_list = list(strCmdOut)
tempIndex = int(chr(ascii_list[4]), 16)*16+int(chr(ascii_list[5]), 16)
print("\ntempIndex : {}".format(tempIndex))

if tempIndex < 0x60:
    print("\nUX3320 Mod auto mode,now tempIndex is {}, UX3320 87-88h should adjust to '0x{:2X}'".format(tempIndex,int(
        tempIndex*int('0x251',16)/1000+int('0x5F',16))))
    f.write("\nUX3320 Mod auto mode,now tempIndex is {}, UX3320 87-88h should adjust to '0x{:2X}'".format(tempIndex,int(
        tempIndex*int('0x251',16)/1000+int('0x5F',16))))
else:
    print("\nUX3320 Mod auto mode,now tempIndex is {}, UX3320 87-88h should adjust to '0x{:2X}'".format(tempIndex, int(
        tempIndex * int('0x1C4', 16) / 1000 + int('0x6C', 16))))
    f.write("\nUX3320 Mod Max auto mode,now tempIndex is {}, UX3320 87-88h should adjust to '0x{:2X}'".format(tempIndex, int(
        tempIndex * int('0x1C4', 16) / 1000 + int('0x6C', 16))))
f.write('\n')
strCmdIn = create_string_buffer(b'MCU_SET_TABLE(LUT,3,0,0x60,0x02,0x51,0x00,0x5F,0xFF,0x01,0xC4,0x00,0x6C)')
f.write(repr(strCmdIn.value)+'\n')
strCmdOutBuff = ctypes.c_ubyte*8
strCmdOut = strCmdOutBuff()
cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 'OK' == chr(strCmdOut[0])+chr(strCmdOut[1]):
    # TODO: first read back,then hold target,max,miin
    strCmdIn = create_string_buffer(b'MCU_SET_ADJUST(5, A, 0, 0, 0, 0)')
    print(repr(strCmdIn.value)+'\n')
    f.write(repr(strCmdIn.value)+'\n')
    time.sleep(1)
    strCmdOutBuff = ctypes.c_ubyte * 10
    strCmdOut = strCmdOutBuff()
    cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 'OK' == chr(strCmdOut[0]) + chr(strCmdOut[1]):
        strCmdIn = create_string_buffer(b'MCU_I2C_READ(0xA2,0x87,2)')
        f.write(repr(strCmdIn.value)+'\n')
        strCmdOutBuff = ctypes.c_ubyte * 10
        strCmdOut = strCmdOutBuff()
        cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
        for item in range(len(strCmdOut)):
            print("{}".format(chr(strCmdOut[item])), end='')
            f.write(chr(strCmdOut[item]))
    print("\n[87-88]=0x{:2X}".format(
        (int(chr(list(strCmdOut)[2]), 16) * 16 + int(chr(list(strCmdOut)[3]), 16)) * 4 + (
                int(chr(list(strCmdOut)[7]), 16) * 16 + int(chr(list(strCmdOut)[8]), 16))))
    f.write("\n[87-88]=0x{:2X}".format(
        (int(chr(list(strCmdOut)[2]), 16) * 16 + int(chr(list(strCmdOut)[3]), 16)) * 4 + (
                int(chr(list(strCmdOut)[7]), 16) * 16 + int(chr(list(strCmdOut)[8]), 16))))

AteAllPowerOff(devUsbIndex)
>>>>>>> 2da87054d45d32a3addd32c95e9cb15ab0fa91ac
f.close()

