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
get a list of all of the freakduinos
get a list of all of the nodes for the specific freakduinos
get a list of all of the valves for the specific nodes
'''