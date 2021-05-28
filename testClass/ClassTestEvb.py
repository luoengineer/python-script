import ctypes


Class cTestEvb:
    #------------------ Attribute ------------------#
    # Config EVBoard usb
    devUsbIndex = 0

    # Config EVBoard slot
    devSffChannel = 1
    devSfpChannel = 2

    #load dll
    objdll = ctypes.cdll.LoadLibrary(".\ATEAPI.dll")


    #------------------ Method ------------------#
    def setUsbDevice(self, usbDeviceNum):
        self.devUsbIndex = usbDeviceNum

    def getUsbDevice(self):
        return self.devUsbIndex

    # Open USB Device
    def openUsbDevice(devUsbIndex):
        usbHandle = 0
        usbHandle = objdll.AteOpenDevice(devUsbIndex)
        if usbHandle != 0:
            print("Open USB device {}".format(devUsbIndex))
            objdll.AteCloseDevice(usbHandle)

    # Slot Power On
    def AteAllPowerOn(dev_Usb_Index):
        objdll.AteSffPowerOn(dev_Usb_Index)
        objdll.AteSfpPowerOn(dev_Usb_Index)


    def AteAllPowerOff(dev_Usb_Index):
        objdll.AteSffPowerOff(dev_Usb_Index)
        objdll.AteSfpPowerOff(dev_Usb_Index)










