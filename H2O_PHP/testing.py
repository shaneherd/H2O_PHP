import os
from serial import Serial
 
ser = Serial('/dev/ttyUSB0', 9600)

while True:
    print "listening for almost done"
    dataRead = ser.readline()
    if dataRead: #if it isn't empty
        print "checking dataRead"
        dataRead = str(dataRead)
        print "dataRead: " , dataRead
        print "command: " , dataRead[2:6]
        if dataRead[2:4] == "ffcc":
            almostDone = True
