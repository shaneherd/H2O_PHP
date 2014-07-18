import os
from serial import Serial

ser = Serial('/dev/ttyUSB0', 9600)

#get all of the freakduinos in the database that are active
freakduinosList = os.popen('mysql -B --disable-column-names --user=shane --password=password h2o -e "select HEX(address) as address FROM nodes WHERE type = 2 AND active = 1";').read().strip()  
#the above statement returns an extra newline at the end. the .strip() at the end of the line removes the extra newline
#the above statement possibly returns multiple rows
#split the returned statement at each new record
freakduinosList = freakduinosList.split()

#create empty lists for all of the nodes and all of the valves
allNodesList = list()
allValvesList = list()
amountsToSend = list()
dataToSend = list()
activeFreakduinos = list()

#create commands
startCommand = "ff00"
stopCommand = "ffff"
almostDoneCommand = "ffcc"
errorCommand = "ffdd"

#go through each freakduino and find all of the children nodes for that freakduino
for freakduino in freakduinosList:
    #get all of the nodes for the current freakduino
    nodesList = os.popen('mysql -B --disable-column-names --user=shane --password=password h2o -e "select HEX(address) as address FROM nodes WHERE parent=x\'' + str(freakduino) + '\'  AND active = 1";').read().strip()
    #split the returned statement at each new record
    nodesList = nodesList.split()
    #add the nodesList to the list which holds all of the nodes (not just the nodes for the current freakduino)
    allNodesList.append(nodesList)
    activeFreakduinos.append(0)
    
    #go through each node for the current freakduino and find all of the children valves for that node
    for node in nodesList:
        #get all of the valves for the current node
        valvesList = os.popen('mysql -B --disable-column-names --user=shane --password=password h2o -e "select HEX(address) as address FROM nodes WHERE parent=x\'' + str(node) + '\'  AND active = 1";').read().strip()
        #split the returned statement at each new record
        valvesList = valvesList.split()
        
        #add the valvesList to the list which holds all of the valves (not just the valves for the current node)
        allValvesList.append(valvesList)

print "freakduinos: " , freakduinosList
print "nodes: " , allNodesList
print "valves: " , allValvesList

i = 0
j = 0
print "\ntreeview of nodes"
#get the amounts of water to send and combine that with the address
for freakduino in freakduinosList:
    print freakduino
    for node in allNodesList[i]:
        print "\t" , node
        data = list()
        send = list()
        for valve in allValvesList[j]:
            print "\t\t" , valve
            #get the valve id of the current valve
            valveID = os.popen('mysql -B --disable-column-names --user=shane --password=password h2o -e "select id from nodes where address=x\'' + str(valve) + '\'";').read().strip()
            
            #get the amout to send for the current valve
            amountToSend = os.popen('mysql -B --disable-column-names --user=shane --password=password h2o -e "select litersPerDay from customers where valveID = ' + str(valveID) +  '";').read().strip()
            send.append(amountToSend)
            
            #combine address with amounts to send
            currentData = str(valve) + str(amountToSend)
            data.append(currentData)
        j = j + 1
        amountsToSend.append(send)
        dataToSend.append(data)
    i = i + 1
    
print "\nverifying that correct amounts were retrieved and combined with address correctly"
print "amountsToSend: " , amountsToSend
print "dataToSend: " , dataToSend

#send data to freakduinos without starting
i = 0
j = 0
print "\ninitializing data on all freakduinos"
for freakduino in freakduinosList:
    for node in allNodesList[i]:
        for data in dataToSend[j]:
            ser.write(data)
            print "data being sent: " , data
        j = j + 1
    i = i + 1
    
#At this point, all data has been sent
#Set initialize pin in database low
os.popen('mysql -B --disable-column-names --user=shane --password=password h2o -e "UPDATE status SET status=0  where id != 2";').read()
#Set ready pin in database high so that the user can press the start button in the app
os.popen('mysql -B --disable-column-names --user=shane --password=password h2o -e "UPDATE status SET status=1  where id = 2";').read()    
    
start = 0
stop = 0

print ""
#continually check the start pin in the database
#once it is high, continue with the program
while start == 0:
    print "checking start pin in database"
    startReturned = os.popen('mysql -B --disable-column-names --user=shane --password=password h2o -e "select status from status where id = 3";').read().strip()
    start = int(startReturned)

#Set start pin in database low
os.popen('mysql -B --disable-column-names --user=shane --password=password h2o -e "UPDATE status SET status=0  where id = 3";').read()
    
#initialize variables
numToRunAtSameTime = 2
i = 0
numFreakduinos = len(freakduinosList)
numDone = 0

#start the first # of freakduios
print "\nstarting initial freakduinos"
while i < numToRunAtSameTime:
    #start freakduino #i
    freakduino = freakduinosList[i]
    freakduino = freakduino[0:2]
    print "starting freakduino " , freakduino
    startFreakduino = freakduino + startCommand + "00"
    activeFreakduinos[i] = 1
    ser.write(startFreakduino)
    i = i + 1
    print "activeFreakduinos:" , activeFreakduinos

#while not all are started
while i < numFreakduinos and stop == 0:
    almostDone = False
    
    #check if the stop pin in the database is high
    stopReturned = os.popen('mysql -B --disable-column-names --user=shane --password=password h2o -e "select status from status where id = 4";').read().strip()
    stop = int(stopReturned)
    if stop == 1: 
        print "\nsending stop signal to all active freakduinos"
        activesPlace = 0
        for activeFreakduino in activeFreakduinos:
            if activeFreakduino == 1:
                freakduino = freakduinosList[activesPlace]
                activeFreakduinos[activesPlace] = 0
                activeFreakduino = freakduino[0:2]
                stopFreakduino = activeFreakduino + stopCommand + "00"
                ser.write(stopFreakduino)
                print "activesPlace: " , activesPlace
            activesPlace = activesPlace + 1   
    else:
        print "\nlistening for almost done"
        dataRead = ser.readline()
        if dataRead: #if it isn't empty
            dataRead = str(dataRead) #insure that the dataRead is a string so that we can use substring
            if dataRead[2:6] == "ffcc": #almost done command
                freakduinoToStop = dataRead[0:2]
                print "freakduinoToStop from command: " , freakduinoToStop
                activesPlace = 0
                for freakduino in freakduinosList:
                    if freakduino[0:2] == freakduinoToStop: #if the current freakduino is equal to the freakduino to stop from the command read in
                        if activeFreakduinos[activesPlace] == 1: #make sure that that freakduino was active
                            print "stopping freakduino " , freakduino
                            activeFreakduinos[activesPlace] = 0
                            almostDone = True
                            print "activeFreakduinos:" , activeFreakduinos
                    activesPlace = activesPlace + 1
        print "almostDoneSignal: " , almostDone
        
    
    if almostDone:
        print "\nsending start to next freakduino "
        #start freakduino #i
        freakduino = freakduinosList[i]
        freakduino = freakduino[0:2]
        print "starting freakduino " , freakduino
        startFreakduino = freakduino + startCommand + "00"
        activeFreakduinos[i] = 1
        i = i + 1
        numDone = numDone + 1
        print "activeFreakduinos:" , activeFreakduinos

#if previous loop finished because all freakduinos have been started        
if stop == 0:
    #while not all are done and stop hasn't been pressed
    while numDone < numFreakduinos and stop == 0: 
        #finish remaining freakduinoss
        almostDone = False
        
        #check if the stop pin in the database is high
        stopReturned = os.popen('mysql -B --disable-column-names --user=shane --password=password h2o -e "select status from status where id = 4";').read().strip()
        stop = int(stopReturned)
        
        if stop == 1:
            print "\nsending stop signal to all active freakduinos"
            activesPlace = 0
            for activeFreakduino in activeFreakduinos:
                if activeFreakduino == 1:
                    freakduino = freakduinosList[activesPlace]
                    activeFreakduinos[activesPlace] = 0
                    activeFreakduino = freakduino[0:2]
                    stopFreakduino = activeFreakduino + stopCommand + "00"
                    ser.write(stopFreakduino)
                activesPlace = activesPlace + 1
        else:
            print "\nlistening for almost done"
            dataRead = ser.readline()
            if dataRead: #if it isn't empty
                dataRead = str(dataRead) #convert input to string
                if dataRead[2:6] == "ffcc": #almost done command
                    freakduinoToStop = dataRead[0:2]
                    print "freakduinoToStop: " , freakduinoToStop
                    activesPlace = 0
                    for freakduino in freakduinosList:
                        if freakduino[0:2] == freakduinoToStop: #if the current freakduino equals the freakduino to stop from the command
                            if activeFreakduinos[activesPlace] == 1: #if the current freakduino is active
                                print "stopping freakduino " , freakduino
                                activeFreakduinos[activesPlace] = 0
                                almostDone = True
                                print "activeFreakduinos:" , activeFreakduinos
                        activesPlace = activesPlace + 1
            print "almostDoneSignal: " , almostDone
            
        if almostDone:
            numDone = numDone + 1
    
#all valves are done or system has been manually stopped
#set stop pin in database low (if it was already low, it won't affect anything)
os.popen('mysql -B --disable-column-names --user=shane --password=password h2o -e "UPDATE status SET status=0  where id != 5";').read()
#set done pin in database high
os.popen('mysql -B --disable-column-names --user=shane --password=password h2o -e "UPDATE status SET status=1  where id = 5";').read()

'''
This script is started by the h2o.sh script when the initialize pin has been set high
Get all of the active valves
Get amounts to send to each of the valves
Combine address with the amount

Send data to freakduinos without starting
    i = 0
    j = 0
    for freakduino in freakduinosList:
        for node in allNodesList[i]:
            for valve in allValvesList[j]:
                noResponse = true
                while noResponse:
                    send combined address and amount to freakduino
                    look for response from freakduino
                    if response found
                        noResponse = false
                j = j + 1
            i = i + 1
    At this point, all data has been sent
    Set initialize pin in database low
    Set ready pin in database high so that the user can press the start button in the app


start = 0
stop = 0
while start == 0:
    start = start pin valve from database

Set start pin in databse low    
numToRunAtSameTime = 3
i = 0
numFreakduinos = freakduinosList.len()
numDone = 0

start the first # of freakduinos
while i < numToRunAtSameTime:
    send start to freakduinosList[i]
    i = i + 1
    
while not all are done
while numDone < numFreakduinos and stop == 0:
    while not all are started
    while i < numFreakduinos and stop == 0:
        almostDone = false
        stop = stop pin value from database
        if stop == 1:
            send stop signal to all active freakduinos
        else:
            listen for almost done signal from active freakduinos
            if almostDone:
                send confirmation of almostDone receieved to sending freakduino so that it will stop sending
                send start to freakduinosList[i]
                numDone = numDone + 1
                i = i + 1
    
    finish remaining freakduinos
    stop = stop pin value from database
    if stop == 1:
        send stop signal to all active freakduinos
    else:
        listen for almost done signal from active freakduinos
        if almostDone:
            send confirmation of almostDone receieved to sending freakduino so that it will stop sending
            numDone = numDone + 1    


All valves are done or have been manually stopped
Set done pin in database high
'''