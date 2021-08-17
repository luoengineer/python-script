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
cmdservdll = ctypes.windll.LoadLibrary(os.path.dirname(os.path.dirname(__file__)) + "\\pyscriptlib\\SuperCommand.dll")


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
        #print("0x{:2X}".format(pbyVal[i]))
    byRes = testEvb.objdll.AteIicRandomWrite(devusbindex, devSffChannel, nDev, nReg, nLen, byref(pbyVal))
    #if byRes != 0:
    #    print("0x{:2X}".format(byRes))
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

def Xfp_Factory_Pwd_Entry(_userType):
    i2cWriteBuf = c_ubyte * 4
    if 0 == _userType:
        factoryPwd = i2cWriteBuf(0xD8, 0x47, 0x54, 0x45)
    elif 1 == _userType:
        factoryPwd = i2cWriteBuf(0x58, 0x47, 0x54, 0x45)
    testEvb.objdll.AteIicRandomWrite(devusbindex, devSffChannel, 0xA0, 123, 4, byref(factoryPwd))

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

def to_ascii(h):
    list_s = []
    for i in range(0,len(h),2):
        list_s.append(chr(int(h[i:i+2].upper(),16)))
    return ''.join(list_s)

def ascii_to_hex(c):
    if c >= 0x30 and c <= 0x39:
        c -= 0x30
    elif c >= 65 and c <= 70:
        c = c - 65 + 10
    elif c >= 97 and c <= 102:
        c = c - 97 + 10
    return c

'''
parameter example :
table_type: BASE/LUT/DRIVER
lut_index : 1
lut_wirte_offset : 0
lut_test_data : "1,2,3,4,5,6,7,8,9,10"
return:
'OK' or 'FAIL'
'''
def cmd_write_table(table_type, table_index, table_wirte_offset, table_data):
    table_data = ','.join([str(x) for x in table_data])
    command_str = 'MCU_SET_TABLE(' + table_type + ',' + str(table_index) + ',' + str(table_wirte_offset) \
            + ',' + table_data + ')'
    command_str = bytes(command_str, encoding="utf8")
    strCmdIn = create_string_buffer(command_str)
    strCmdOutBuff = ctypes.c_ubyte * 8
    strCmdOut = strCmdOutBuff()
    cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
    ret = chr(strCmdOut[0]) + chr(strCmdOut[1])
    return ret

def cmd_read_table(table_type, table_index, table_read_offset, table_read_len):
    command_str = 'MCU_GET_TABLE(' + table_type + ',' + str(table_index) + ',' + str(table_read_offset) \
            + ',' + str(table_read_len) + ')'
    command_str = bytes(command_str, encoding="utf8")
    strCmdIn = create_string_buffer(command_str)
    strCmdOutBuff = ctypes.c_ubyte * 1024
    strCmdOut = strCmdOutBuff()
    #lut_data = ctypes.c_ubyte * 128
    table_data = []
    if 0 == cmdservdll.SuperCmdSer(strCmdIn, strCmdOut):
        for item in range(table_read_len):
            ch0 = ascii_to_hex(strCmdOut[2 + item * 5])
            ch1 = ascii_to_hex(strCmdOut[3 + item * 5])
            #print("{}, {}".format(ch0, ch1))
            table_data.append(ch0*16+ch1)
        return 'OK', table_data
    else:
        return 'FAIL', None

#read max 8 regs
def cmd_read_drv_reg(drv_addr, reg_offset, reg_read_len):
    command_str = 'MCU_I2C_READ(' + str(drv_addr) + ',' \
                  + str(reg_offset) + ',' \
                  + str(reg_read_len) + ')'
    command_str = bytes(command_str, encoding="utf8")
    strCmdIn = create_string_buffer(command_str)
    strCmdOutBuff = ctypes.c_ubyte * 64
    strCmdOut = strCmdOutBuff()
    regs_data = []
    if 0 == cmdservdll.SuperCmdSer(strCmdIn, strCmdOut):
        for item in range(reg_read_len):
            ch0 = ascii_to_hex(strCmdOut[2 + item * 5])
            ch1 = ascii_to_hex(strCmdOut[3 + item * 5])
            # print("{}, {}".format(ch0, ch1))
            regs_data.append(ch0 * 16 + ch1)
        return 'OK', regs_data
    else:
        return 'FAIL', None