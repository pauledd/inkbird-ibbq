#!/usr/bin/env python3

'''
reads Inbird iBBQ Thermometer temperature values on sensor 1 and outputs it.

'''




from bluepy.btle import *
import datetime

class MyDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
#        print(cHandle,data)
#        if cHandle == 25:
#            print(data,int.from_bytes(data[2:4],"big"))
        if cHandle == 48:
            
            temp0 = int(int.from_bytes(data[:2],"little") / 10)
            temp1 = int(int.from_bytes(data[-2:],"little") / 10)
            print(datetime.datetime.now().strftime("%H:%M:%S"),",",temp0,",",temp1,sep="")

# Set thermometer mac adress here
dev = Peripheral("0c:ae:7d:e7:9e:3d")


dev.setDelegate(MyDelegate())
# authenticate
z = dev.getCharacteristics(0x0028,0x0029)
dev.writeCharacteristic(0x0029,bytearray.fromhex("2107060504030201b8220000000000",),1)

# get battery level
#dev.writeCharacteristic(0x0034,bytearray.fromhex("082400000000"),1)


# Enable realtime data collection
s = dev.getCharacteristics(0x0033,0x0034)
dev.writeCharacteristic(0x0034,bytearray.fromhex("0B0100000000"),1)


# Subscribe to realtime data collectionx
service = dev.getServiceByUUID(UUID("0000fff0-0000-1000-8000-00805f9b34fb"))
service.getCharacteristics(UUID("0000fff4-0000-1000-8000-00805f9b34fb"))
i=0
while True:
	if dev.waitForNotifications(2.0):
		continue
