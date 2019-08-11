import time
import struct

###################################
#open message files
###################################

fCoord = open('/home/user-1/Projects/PROJ0001/coordinates.txt', 'wr+') 
fMar = open('/home/user-1/Projects/PROJ0001/printerMessage.txt', 'wr+') 
fArd = open('/home/user-1/Projects/PROJ0001/arduinoMessage.txt', 'wr+')
fCoord.write('position,value\r\n')

###################################
#write to serial devices
###################################

#marSer.write('G28 X0 Y0\n') #home the printer
ardSer.write(struct.pack('<B', 1)) #read light val, need struct to send value as binary. otherwise Arduino will interperate as ASCII character

###################################
#read from serial devices
###################################

### marlin
#time.sleep(1)
#fMar.write(marSer.read(1000))
#fMar.flush()
#fMar.seek(0) # for some reason the file needs to be closed and reopened to be read.

### arduino
fArd.write(ardSer.read(1000))
fArd.flush()
fArd.seek(0)

#fMar = open('/home/user-1/Projects/PROJ0001/printerMessage.txt', 'r+') 
#fArd = open('/home/user-1/Projects/PROJ0001/arduinoMessage.txt', 'r+') 

###################################
#parse messages, check for OK status
###################################

writeCommand('G28 X0 Y0\n', 1)
writeCommand(struct.pack('<B', 1),2)
#while 1:
#	marLine = fMar.readline()
#	time.sleep(.1)
#	print('%s line'%marLine)
#	if marLine == 'ok\n':
#		print('Marlin ok received')
#		break
#	if not marLine:
#		print('EOF Marlin reached')
#		break			
#while 1:	
#	ardLine = fArd.readline()
#	time.sleep(.1)
#	print('%s line'%ardLine)
#	if ardLine == 'ok\r\n':
#		print('arduino ok received')
#		break
#	if not ardLine:
#		print('EOF arduino reached')
#		break

print('message file closed')


###################################
#collect data
###################################
#p = 1
#for p to 100:
#	marSer.write('G28 X0 Y0\n') # move to position
#	ardSer.write(struct.pack('<B', 1))

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

fCoord.close()
fMar.close()
fArd.close()
