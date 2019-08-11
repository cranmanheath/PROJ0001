###################################
#initialize Serial connection and move printer
###################################


import serial


port1 = "USB0" #Linux USB ports are /dev/ttyUSBx (x=0,1,2,3...)


while 1:
    try:
        ser = serial.Serial('/dev/tty%s' %port1, 115200, timeout=0)
    except:
        print("unable to connect to %s" %port1)
    else:
        print("connected to %s" %ser.name)
        break
        

ser.write('G28\n')      #G28 = home the printer
time.sleep(5)           #wait 5 seconds for printer to home.
ser.write('G1 X50 Y25') #Move printer 50mm in x-dir and 25mm in y-dir
