import ctypes
from ctypes import *
import time
import sys
from sys import path
from cmdServ import cmdservdll, Sfp_Factory_Pwd_Entry, getAdc0, adc02TempIndex
from classTestEvb import *


#Test times
wr_and_rd_times  = 2
run_time_second = 3600 * 8  # unit : s
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

    def cmd_read_lut(self, lutable_index):
        command_str = 'MCU_GET_TABLE(lut,' + str(lutable_index) + ',0,128)'
        command_str = bytes(command_str, encoding="utf8")
        strCmdIn = create_string_buffer(command_str)
        strCmdOutBuff = ctypes.c_ubyte * 639
        strCmdOut = strCmdOutBuff()
        retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
        if 0 == retStauts:
            return "OK", strCmdOut
        else:
            return "FAIL"

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
        ret = 0xFF
        ret = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
        return ret, strCmdOut

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
endTick = startTick + run_time_second
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
driveInstance.apc_table = 2, "0x4B,0x00,0x00,0x00,0xB9,0xFF,0x00,0x00,0x00,0xB9", 512, 1
driveInstance.mcu_apc_adjust = 4
driveInstance.mod_reg = 0x87, 0x88, 'MOD', 2
driveInstance.mod_table = 3, "0x60,0x02,0x51,0x00,0x5F,0xFF,0x01,0xC4,0x00,0x6C", 512, 1
driveInstance.mcu_mod_adjust = 5
print("\n****************************************************************************")
print("Inner I2C Access {} Stress test, start time : {}".format(driveInstance._driver_name, dateTime))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nInner I2C Access {} Stress test, start time : {}".format(driveInstance._driver_name, dateTime))
f.write("\n****************************************************************************")
print("{}".format(testTitle))
f.write('\n'+testTitle)

read_drv_init_val = False
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
#               Verify UX3320 APC
#########################################################

#Backup lut
print("\n\nBackup {} LUT".format(driveInstance.apc_reg[2]))
f.write("\n\nBackup {} LUT".format(driveInstance.apc_reg[2]))
Res = 0xFF
Res, RawReadByte = driveInstance.cmd_read_lut(driveInstance.apc_table[0])
if "OK" == Res:
    print('\n{} LUT :'.format(driveInstance.apc_reg[2]))
    f.write('\n{} LUT :'.format(driveInstance.apc_reg[2]))
    for item in range(len(RawReadByte)):
        print("{}".format(chr(RawReadByte[item])), end='')
        f.write(chr(RawReadByte[item]))
else:
    f.write('read {} LUT fail.'.format(driveInstance.apc_reg[2]))
    print('read {} LUT fail.'.format(driveInstance.apc_reg[2]))
    f.close()
    sys.exit()
ApcRawLut = str(RawReadByte, 'utf-8')
#print("\n")
#print(ApcRawLut)


print("\n\nNow start realtime adjust {} with mcu temperature".format(driveInstance.apc_reg[2]))
f.write("\n\nNow start realtime adjust {} with mcu temperature".format(driveInstance.apc_reg[2]))

print("Write {} Lut ".format(driveInstance.apc_reg[2]), end='')
f.write("\nWrite {} Lut ".format(driveInstance.apc_reg[2]))
if 'OK' == driveInstance.cmd_write_lut(driveInstance.apc_table):
    total_times_count = 0
    error_times_count = 0
    error_times_statistics = []
    while time.time() < endTick:
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
            ret, strCmdOut = driveInstance.cmd_mcu_i2c_read(driveInstance.driver_addr, driveInstance.apc_reg[0],
                                                       driveInstance.apc_reg[3])
            if ret != 0:
                error_times_count += 1
                error_times_statistics.append(str(total_times_count))
            else:
                for item in range(len(strCmdOut)):
                    print("{}".format(chr(strCmdOut[item])), end='')
                    f.write(chr(strCmdOut[item]))
            total_times_count += 1
else:
    print("\nWrite {} Lut Fail.".format(driveInstance.apc_reg[2]), end='')
    f.write("\nWrite {} Lut Fail.".format(driveInstance.apc_reg[2]))

#Restore lut
print("\nRestore {} Lut".format(driveInstance.apc_reg[2]), end='')
f.write("\nRestore {} Lut".format(driveInstance.apc_reg[2]))
driveInstance.apc_table = 2, ApcRawLut, 512, 1
if 'OK' == driveInstance.cmd_write_lut(driveInstance.apc_table):
    print("\n{} LUT restore success.".format(driveInstance.apc_reg[2]))
    f.write("\n{} LUT restore success.".format(driveInstance.apc_reg[2]))
else:
    print("\n{} LUT restore fail.".format(driveInstance.apc_reg[2]))
    f.write("\n{} LUT restore fail.".format(driveInstance.apc_reg[2]))

if len(error_times_statistics) > 0:
    #print("\n{}".format(error_times_statistics))
    for item in range(len(error_times_statistics)):
        print("\nError happen in Round {} ".format(error_times_statistics[item]))
        f.write("\n\nError happen in Round {} ".format(error_times_statistics[item]))
else:
    print("\nNo error, total execute Round {} OK . ".format(total_times_count))
    f.write("\n\nNo error, total execute Round {} OK . ".format(total_times_count))

dateTime = time.strptime(time.asctime())
dateTime = "{:4}-{:02}-{:02} {:02}:{:02}:{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
print("\n****************************************************************************")
print("Inner I2C Access {} Stress test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(driveInstance._driver_name, dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nInner I2C Access {} Stress test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(driveInstance._driver_name, dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
f.write("\n****************************************************************************")
testEvb.AteAllPowerOff()
f.close()

