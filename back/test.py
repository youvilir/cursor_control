import device

def GetDeviceList():
    devices = device.getDeviceList()
    return devices

def EnumerateDevices():
    devices = device.EnumerateDevices()
    return devices

print(EnumerateDevices())