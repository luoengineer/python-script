import ctypes as ct
from ctypes import *

__version__ = "0.0.1"
__date__ = "6 May 2021"
__all__ = ['cTestEvb', 'devusbindex', 'devSffChannel', '_cmdservdll', '_ateapidll']

devusbindex = 0
devSffChannel = 1

_ateapidll = ct.windll.LoadLibrary(".\ATEAPI.dll")
_cmdservdll = ct.windll.LoadLibrary(".\SuperCommand.dll")

def I2C_Read(nDev, nReg, nLen, pbyBuf):
    pbyValBuff = ct.c_ubyte * 256
    pbyVal = pbyValBuff()
    # print("{},{},{}".format(nDev, nReg, nLen))
    wRes = _ateapidll.AteIicRandomRead(devusbindex, devSffChannel, nDev, nReg, nLen, pbyVal)
    if 0 == wRes:
        for i in range(nLen):
            pbyBuf[i] = pbyVal[i]
            # print("{}".format(pbyBuf[i]), end=' ')
    return wRes

def I2C_Write(nDev, nReg, nLen, pbyDat):
    pbyValBuff = ct.c_ubyte * 256
    pbyVal = pbyValBuff()
    for i in range(nLen):
        # print("{}".format((i)%256s), end=' ')
        # print("{}".format(pbyDat[i]), end=' ')
        pbyVal[i % 256] = pbyDat[i]
        # print("{}".format(pbyVal[i]))
    byRes = _ateapidll.AteIicRandomWrite(devusbindex, devSffChannel, nDev, nReg, nLen, byref(pbyVal))
    return byRes

#==============================================================================
#               Regsite Sevices
#==============================================================================
cmdType = b"I2C_WRITE"
I2C_Write_FUNC = WINFUNCTYPE(c_int, c_int, c_int, c_int, POINTER(c_ubyte))
_i2c_write_func = I2C_Write_FUNC(I2C_Write)
_cmdservdll.RegistCallBackFunciton(string_at(cmdType), _i2c_write_func)

cmdType = b'I2C_READ'
I2C_Read_FUNC = WINFUNCTYPE(c_int, c_int, c_int, c_int, POINTER(c_ubyte))
_i2c_read_func = I2C_Read_FUNC(I2C_Read)
_cmdservdll.RegistCallBackFunciton(string_at(cmdType), _i2c_read_func)

class cTestEvb:

    def __init__(self, devusbindex=0):
        self.devUsbIndex = devusbindex
        # load dll
        #self._DLL = ct.windll.LoadLibrary(".\ATEAPI.dll")

    # use property
    def setUsbDevice(self, devusbindex):
        self.devUsbIndex = devusbindex
    def getUsbDevice(self):
        return self.devUsbIndex
    devusbindex = property(setUsbDevice, getUsbDevice)

    # Open USB Device
    def openUsbDevice(self):
        usbHandle = 0
        usbHandle = _ateapidll.AteOpenDevice(self.devUsbIndex)
        if usbHandle != 0:
            print("Open USB device {}".format(self.devUsbIndex))
            _ateapidll.AteCloseDevice(usbHandle)

    # Slot Power On
    def AteAllPowerOn(self):
        _ateapidll.AteSffPowerOn(self.devUsbIndex)
        _ateapidll.AteSfpPowerOn(self.devUsbIndex)


    def AteAllPowerOff(self):
        _ateapidll.AteSffPowerOff(self.devUsbIndex)
        _ateapidll.AteSfpPowerOff(self.devUsbIndex)


    #_userType : 0: is_088_Module, 1: is_other_Module
    def Sfp_Factory_Pwd_Entry(self, _userType):
        i2cWriteBuf = c_ubyte * 4
        if 0 == _userType:
            factoryPwd = i2cWriteBuf(0xD8, 0x47, 0x54, 0x45)
        elif 1 == _userType:
            factoryPwd = i2cWriteBuf(0x58, 0x47, 0x54, 0x45)
        _ateapidll.AteIicRandomWrite(devusbindex, devSffChannel, 0xA2, 123, 4, byref(factoryPwd))

    def Xfp_Factory_Pwd_Entry(self, _userType):
        i2cWriteBuf = c_ubyte * 4
        if 0 == _userType:
            factoryPwd = i2cWriteBuf(0xD8, 0x47, 0x54, 0x45)
        elif 1 == _userType:
            factoryPwd = i2cWriteBuf(0x58, 0x47, 0x54, 0x45)
        _ateapidll.AteIicRandomWrite(devusbindex, devSffChannel, 0xA0, 123, 4, byref(factoryPwd))

    def getAdc0(self):
        strCmdIn = create_string_buffer(b'MCU_GET_ADC(0)')
        strCmdOutBuff = ct.c_ubyte * 32
        strCmdOut = strCmdOutBuff()
        retStauts = _cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
        if 0 == retStauts:
            tempCmdOut = strCmdOut[2:4]
            strCmdOut[2:4] = strCmdOut[4:6]
            strCmdOut[4:6] = tempCmdOut
        return strCmdOut

    def adc02TempIndex(self, _ascTouple):
        ascii_list = list(_ascTouple)
        tempIndex = int(chr(ascii_list[4]), 16) * 16 + int(chr(ascii_list[5]), 16)
        return tempIndex

    def Sfp_User_Read_088Pwd_Entry(self):
        i2cWriteBuf = c_ubyte * 4
        userPwd = i2cWriteBuf(0x00, 0x00, 0x10, 0x11)
        _ateapidll.AteIicRandomWrite(devusbindex, devSffChannel, 0xA2, 123, 4, byref(userPwd))

    def PRINTV(*arg):
        #    print(arg)
        pass



