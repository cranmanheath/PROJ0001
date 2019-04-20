import serial
import time
import struct
import csv
import numpy as np


###################################
#initialize ports
###################################
marSer = ""
ardSer = ""
port1 = "USB0"
port2 = "ACM0"
s = ""
while 1:
	try:
		marSer = serial.Serial('/dev/tty%s' %port1, 115200, timeout=0)#, parity=serial.PARITY_NONE, rtscts=1
	except:
		print("unable to connect to %s" %port1)
		s = raw_input("try another port?: ")
		if s == "quit":
			break
		else:
			port1 = s
	else:
		print("connected to %s" %marSer.name)
		break

while 1:
	try:
		ardSer = serial.Serial('/dev/tty%s' %port2, 9600, timeout=0)
	except:
		print("unable to connect to %s" %port2)
		s = raw_input("try another port?: ")
		if s == "quit":
			break
		else:
			port2 = s
	else:
		print("connected to %s" %ardSer.name)
		break
#time.sleep(0.1)

###################################
#functions
###################################
def readoutSerial(device):
	""" Clear the serial input buffer """
	selectSerial(device).flushInput()


def writeCommand(command, device, timeout=20):
	"""
	This function writes a Marlin or Arduino command to the
	serial port named device.  
	"""	
	ser = selectSerial(device)
	ser.write('%s' %command)
	start_time = time.time()
	if device == 2:
		time.sleep(.1)
	incoming_data = []

	while time.time() - start_time < timeout:
		while ser.inWaiting():
			line = ser.readline()
			#print(line)
			incoming_data.append(line)
			
			if 'ok' in line:
				print('Device', device, 'ok recieved')
				return incoming_data
	raise SystemError('Device timed out')			
	return

def selectSerial(devID):
	switcher = {
	1: marSer, #marlin
	2: ardSer  #arduino
	}
	return switcher.get(devID, "no device selected");

def selectLogfile(devID):
	switcher = {
	1: fMar, #marlin
	2: fArd  #arduino
	}
	return switcher.get(devID, "no device selected");

def calibrate(fGcode):	
	selectSerial(1).write(fGcode)			
	return;


###################################
#open  logfiles
###################################

#fCoord = open('/home/user-1/Projects/PROJ0001/coordinates.txt', 'ar+') 
#fMar = open('/home/user-1/Projects/PROJ0001/printerMessage.txt', 'ar+') 
#fArd = open('/home/user-1/Projects/PROJ0001/arduinoMessage.txt', 'ar+')
#fCoord.write('position,value\r\n')
#fpos = open('/home/user-1/Projects/PROJ0001/newPosition.txt', 'wr')

###################################
# Home Printer
###################################

readoutSerial(1)

#while 1:
#	a = raw_input("give command or quit: ")
#	if a == "quit":
#		break
#	else:
#		marlin_data = writeCommand('%s\n' %a , 1)
#		arduino_data = writeCommand(2, 2)
#		print('marlin_data:' + ''.join(marlin_data))
#		print('arduino_data:' + ''.join(arduino_data))

time.sleep(0.1)

# Create meshgrid to scan
x_array = np.arange(0, 100, 33)
y_array = np.arange(0, 100, 33)
XX, YY = np.meshgrid(x_array, y_array)

# Create empty arrays to fill as the printer moves to each grid point.
true_x = np.nan*np.zeros_like(XX)
true_y = np.nan*np.zeros_like(YY)
led_values = np.nan*np.zeros_like(XX)

# Park printer (Good place to start)
writeCommand('G28\n', 1)
print('Printer parked')

for i_x in np.arange(XX.shape[0]):
	for i_y in np.arange(YY.shape[1]):
		# Move to positon X_i, Y_i.
		writeCommand('G1 X%d Y%d\n' % (XX[i_x, i_y], YY[i_x, i_y]) , 1)
		# Give the printer some time to move back in y.
		if (i_y == 0) and (i_y > 0):
			time.sleep(5) 
		marlin_loc = writeCommand('M114\n', 1)
		print(marlin_loc)
		true_x[i_x, i_y] = marlin_loc[0].split(':')[1].split(' ')[0]
		true_y[i_x, i_y] = marlin_loc[0].split(':')[2].split(' ')[0]
		led_values[i_x, i_y] = int(writeCommand(2, 2)[0].rstrip())
		

#for i, x_i in enumerate(x_array):
#	writeCommand('G1 X%d\n' % x_i , 1)
#	marlin_loc = writeCommand('M114\n', 1)
#	#print(x_i, marlin_loc)
#	led_vals[i] = writeCommand(2, 2)[0].rstrip()
#	true_x_array[i] = marlin_loc[0].split(':')[1].split(' ')[0]

for i_x in np.arange(XX.shape[0]):
	for i_y in np.arange(YY.shape[1]):
		print(true_x[i_x, i_y], true_y[i_x, i_y], led_values[i_x, i_y])

#for x_i, led_i in zip(true_x_array, led_vals):
#	print(x_i, led_i)



####################################
##collect data
####################################
marSer.close()
ardSer.close()
print('Ports Closed')
