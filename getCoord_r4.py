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
        time.sleep(.1)  #sleep for arduino to not lose packet.
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
#       a = raw_input("give command or quit: ")
#       if a == "quit":
#               break
#       else:
#               marlin_data = writeCommand('%s\n' %a , 1)
#               arduino_data = writeCommand(2, 2)
#               print('marlin_data:' + ''.join(marlin_data))
#               print('arduino_data:' + ''.join(arduino_data))

def get_location(timeout=60):
    """
    Gets the location of the printer and waits if the printer is still
    moving.
    """
    start_time = time.time()
    marlin_loc = writeCommand('M114\n', 1)
    # Give the printer up to timeout to move to the next position.
    while time.time() - start_time < timeout:
        if 'busy' in marlin_loc[0]:
            marlin_loc = writeCommand('M114\n', 1)
        else:
            break
    return marlin_loc

time.sleep(0.1)

############################################
#### SCAN THE GRID #########################
############################################

# Create meshgrid to scan
x_array = np.arange(0, 100, 50)
y_array = np.arange(0, 100, 50)
XX, YY = np.meshgrid(x_array, y_array)

# Create empty arrays to fill as the printer moves to each grid point.
true_x = np.nan*np.zeros_like(XX)
true_y = np.nan*np.zeros_like(YY)
led_values = np.nan*np.zeros_like(XX)

# Park printer (Good place to start)
writeCommand('G28\n', 1)
print('Printer parked')
writeCommand('G1 Z20\n', 1)
get_location()

for i_x in np.arange(XX.shape[0]):
    for i_y in np.arange(YY.shape[1]):
        # Move to positon X_i, Y_i.
        writeCommand('G1 X%d Y%d\n' % (XX[i_x, i_y], YY[i_x, i_y]) , 1)
        marlin_loc = get_location()
        true_x[i_x, i_y] = marlin_loc[0].split(':')[1].split(' ')[0]
        true_y[i_x, i_y] = marlin_loc[0].split(':')[2].split(' ')[0]
        led_values[i_x, i_y] = int(writeCommand(2, 2)[0].rstrip())

writeCommand('G28\n', 1)
print('Printer parked')

###################################################
################# SAVE TO FILE ####################
###################################################
with open('led_values.csv', 'w') as f:
    """Save the data run to a csv file. """
    w = csv.writer(f)
    # Print header.
    w.writerow(['x', 'y', 'led_value'])

    for i_x in np.arange(XX.shape[0]):
        for i_y in np.arange(YY.shape[1]):
            w.writerow([true_x[i_x, i_y], true_y[i_x, i_y],
                     led_values[i_x, i_y]])

##################################################
########### FIND X & Y AT MAX LED_VALUE ##########
##################################################
i_max = np.argmax(led_values) # Max on flattened array.
print('Max value:', led_values.flatten()[i_max],
        'at X = ', true_x.flatten()[i_max],
        'Y = ', true_y.flatten()[i_max])

####################################
##collect data
####################################
marSer.close()
ardSer.close()
print('Ports Closed')
