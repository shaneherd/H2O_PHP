#Every specified amount of time to wait, check the database initialize pin.
#When the pin is high, start the h2o.py script. Do not run it as a seperate thread.
#Running it as a seperate thread would cause the h2o.sh script to continue running in the background
#which would use a lot of resources. Running it as the same thread allows the script to resume once the h2o.py 
#script has finished. This way we don't have to restart this thread manually.

mysqlusername="shane"
mysqlpassword="password"

#Set wait time between database reads
waitTime="5" #seconds

#Start Loop
while :
do
	#Read MySQL Database and get the pin status
	initialize=$(mysql -B --disable-column-names --user=$mysqlusername --password=$mysqlpassword h2o -e "SELECT status FROM status WHERE id='1'";)
	
	#if initialize is high, run the h2o.py script
	if [ "$initialize" == "1" ]; then
		echo "GPIO 1 Turned On  (Initialize)"
		python /home/pi/h2o.py
	else #else don't run the script
		echo "GPIO 1 Turned Off (Initialize)"
	fi
	
	#Complete Loop
	sleep $waitTime
done