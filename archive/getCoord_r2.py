import time
import struct

###################################
#open  logfiles
###################################

fCoord = open('/home/user-1/Projects/PROJ0001/coordinates.txt', 'wr+') 
fMar = open('/home/user-1/Projects/PROJ0001/printerMessage.txt', 'wr+') 
fArd = open('/home/user-1/Projects/PROJ0001/arduinoMessage.txt', 'wr+')
fCoord.write('position,value\r\n')

###################################
# Home Printer
###################################

writeCommand('G28 X0 Y0\n', 1)
writeCommand('G90\n', 1)
writeCommand(struct.pack('<B', 1),2)


###################################
#collect data
###################################

i =0 
for i in range(10):
	writeCommand('G1 X%d\n' %i, 1)
	writeCommand(struct.pack('<B', 2),2)

fCoord.close()
fMar.close()
fArd.close()
print('message file closed')
###################################
#functions
###################################

def writeCommand(command, device):	
	selectSerial(device).write('%s\n' %command)
	time.sleep(1)
	selectLogfile(device).write(selectSerial(device).read(1000))
	selectLogfile(device).flush()
	selectLogfile(device).seek(0)
	while 1:
		line = selectLogfile(device).readline()
		time.sleep(.1)
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

