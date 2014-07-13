import os

#get all of the freakduinos in the database that are active
freakduinosList = os.popen('mysql -B --disable-column-names --user=shane --password=password h2o -e "select HEX(address) as address FROM nodes WHERE type = 2 AND active = 1";').read().strip()  
#the above statement returns an extra newline at the end. the .strip() at the end of the line removes the extra newline
#the above statement possibly returns multiple rows
#split the returned statement at each new record
freakduinosList = freakduinosList.split()

#create empty lists for all of the nodes and all of the valves
allNodesList = list()
allValvesList = list()

#go through each freakduino and find all of the children nodes for that freakduino
for freakduino in freakduinosList:
    #get all of the nodes for the current freakduino
    nodesList = os.popen('mysql -B --disable-column-names --user=shane --password=password h2o -e "select HEX(address) as address FROM nodes WHERE parent=x\'' + str(freakduino) + '\'  AND active = 1";').read().strip()
    #split the returned statement at each new record
    nodesList = nodesList.split()
    #add the nodesList to the list which holds all of the nodes (not just the nodes for the current freakduino)
    allNodesList.append(nodesList)
    
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
for freakduino in freakduinosList:
    print freakduino
    for node in allNodesList[i]:
        print "\t" , node
        for valve in allValvesList[j]:
            print "\t\t" , valve
        j = j + 1
    i = i + 1
    
'''
This script is started by the h2o.sh script when the initialize pin has been set high
Get all of the active valves
Get amounts to sned to each of the valves
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
Set stop pin in database low
'''