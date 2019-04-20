import serial

marSer = serial.Serial('/dev/ttyUSB1', 115200, timeout=0, parity=serial.PARITY_EVEN, rtscts=1)

ardSer = serial.Serial('/dev/ttyACM1', 9600, timeout=0, parity=serial.PARITY_EVEN, rtscts=1)

print("connected to %s" %marSer.name)
print("connected to %s" %ardSer.name)

