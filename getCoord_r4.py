import serial
import time
import struct


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
	selectSerial(device).flushInput()


def writeCommand(command, device):	
	selectSerial(device).write('%s\n' %command)
	time.sleep(.1)
	selectSerial(device).flushOutput()
	time.sleep(.1)
	while 1:
		line = selectSerial(device).readline()
		time.sleep(.1)
		print(line)

		if device == 1:
			if line == 'ok\n':
				print('Marlin ok received')
				break
			if not line:
				print('EOF Marlin reached')
				break
		if device == 2:
			if line == 'ok\r\n':
				print('arduino ok received')
				break
			if not line:
				print('EOF arduino reached')
				break				
	return;

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

while 1:
	a = input("give command or quit: ")
	if a == "quit":
		break
	else:
		writeCommand('%s\n' %a , 1)
###################################
#collect data
###################################
marSer.close()
ardSer.close()
print('Ports Closed')
