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

