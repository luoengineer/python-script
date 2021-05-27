import ctypes
from ctypes import *
from classTestEvb import *

#########################################################
#               EVBoard Configuration
#########################################################
devusbindex = 0
devSffChannel = 1
testEvb = cTestEvb(devusbindex)

#########################################################
#               Load DLL
#########################################################
#objdll = ctypes.cdll.LoadLibrary(".\AteApi.dll")
cmdservdll = ctypes.windll.LoadLibrary(".\SuperCommand.dll")


def I2C_Read(nDev, nReg, nLen, pbyBuf):
    pbyValBuff = ctypes.c_ubyte * 256
    pbyVal = pbyValBuff()
    # print("{},{},{}".format(nDev, nReg, nLen))
    wRes = testEvb.objdll.AteIicRandomRead(devusbindex, devSffChannel, nDev, nReg, nLen, pbyVal)
    if 0 == wRes:
        for i in range(nLen):
            pbyBuf[i] = pbyVal[i]
            # print("{}".format(pbyBuf[i]), end=' ')
    return wRes

def I2C_Write(nDev, nReg, nLen, pbyDat):
    pbyValBuff = ctypes.c_ubyte * 256
    pbyVal = pbyValBuff()
    for i in range(nLen):
        # print("{}".format((i)%256s), end=' ')
        # print("{}".format(pbyDat[i]), end=' ')
        pbyVal[i % 256] = pbyDat[i]
        # print("{}".format(pbyVal[i]))
    byRes = testEvb.objdll.AteIicRandomWrite(devusbindex, devSffChannel, nDev, nReg, nLen, byref(pbyVal))
    return byRes


#########################################################
#               Regsite Sevices
#########################################################
cmdType = b"I2C_WRITE"
I2C_Write_FUNC = WINFUNCTYPE(c_int, c_int, c_int, c_int, POINTER(c_ubyte))
_i2c_write_func = I2C_Write_FUNC(I2C_Write)
cmdservdll.RegistCallBackFunciton(string_at(cmdType), _i2c_write_func)

cmdType = b'I2C_READ'
I2C_Read_FUNC = WINFUNCTYPE(c_int, c_int, c_int, c_int, POINTER(c_ubyte))
_i2c_read_func = I2C_Read_FUNC(I2C_Read)
cmdservdll.RegistCallBackFunciton(string_at(cmdType), _i2c_read_func)

#########################################################
#               Subroutines
#########################################################
#_userType : 0: is_088_Module, 1: is_other_Module
def Sfp_Factory_Pwd_Entry(_userType):
    i2cWriteBuf = c_ubyte * 4
    if 0 == _userType:
        factoryPwd = i2cWriteBuf(0xD8, 0x47, 0x54, 0x45)
    elif 1 == _userType:
        factoryPwd = i2cWriteBuf(0x58, 0x47, 0x54, 0x45)
    testEvb.objdll.AteIicRandomWrite(devusbindex, devSffChannel, 0xA2, 123, 4, byref(factoryPwd))


def getAdc0():
    strCmdIn = create_string_buffer(b'MCU_GET_ADC(0)')
    strCmdOutBuff = ctypes.c_ubyte * 32
    strCmdOut = strCmdOutBuff()
    retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    if 0 == retStauts:
        tempCmdOut = strCmdOut[2:4]
        strCmdOut[2:4] = strCmdOut[4:6]
        strCmdOut[4:6] = tempCmdOut
    return strCmdOut

def adc02TempIndex(_ascTouple):
    ascii_list = list(_ascTouple)
    tempIndex = int(chr(ascii_list[4]), 16) * 16 + int(chr(ascii_list[5]), 16)
    return tempIndex

def Sfp_User_Read_088Pwd_Entry():
    i2cWriteBuf = c_ubyte * 4
    userPwd = i2cWriteBuf(0x00, 0x00, 0x10, 0x11)
    testEvb.objdll.AteIicRandomWrite(devusbindex, devSffChannel, 0xA2, 123, 4, byref(userPwd))