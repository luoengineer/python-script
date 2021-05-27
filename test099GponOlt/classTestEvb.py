import ctypes

__version__ = "0.0.1"
__date__ = "6 May 2021"

__all__ = ['cTestEvb']

class cTestEvb:

    def __init__(self, devusbindex=0):
        self.devUsbIndex = devusbindex
        # load dll
        self.objdll = ctypes.cdll.LoadLibrary(".\ATEAPI.dll")

    # use property
    def setUsbDevice(self, devusbindex):
        self.devUsbIndex = devusbindex
    def getUsbDevice(self):
        return self.devUsbIndex
    devusbindex = property(setUsbDevice, getUsbDevice)

    # Open USB Device
    def openUsbDevice(self):
        usbHandle = 0
        usbHandle = self.objdll.AteOpenDevice(self.devUsbIndex)
        if usbHandle != 0:
            print("Open USB device {}".format(self.devUsbIndex))
            self.objdll.AteCloseDevice(usbHandle)

    # Slot Power On
    def AteAllPowerOn(self):
        self.objdll.AteSffPowerOn(self.devUsbIndex)
        self.objdll.AteSfpPowerOn(self.devUsbIndex)


    def AteAllPowerOff(self):
        self.objdll.AteSffPowerOff(self.devUsbIndex)
        self.objdll.AteSfpPowerOff(self.devUsbIndex)

    





