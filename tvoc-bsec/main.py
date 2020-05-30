from subprocess import Popen, PIPE, STDOUT
from pymongo import MongoClient,errors
import re

# global variables for MongoDB host (default port is 27017)
DB_DOMAIN = 'mydb'
DB_PORT = 27017

def connectToDB():
	client = MongoClient(
		host = [ str(DB_DOMAIN) + ":" + str(DB_PORT) ],
		serverSelectionTimeoutMS = 3000, # 3 second timeout
	)

	# creates/selects db
	mydb = client["air_data"]
	return mydb;

try:
	mydb = connectToDB();
	mycol = mydb["bme680"];
	p = Popen('./bsec_bme680', stdout = PIPE, stderr = STDOUT, shell = True)

	counter = 0;
	counterAccuracy = 0;
	while True:

		data_dict = {};
		line = p.stdout.readline().decode('UTF-8');

		if not re.match(r'^[0-9]',line) and counter == 0:
			line = p.stdout.readline().decode('UTF-8');

		counter += 1;
		print(line)
		line = line.split(',');

		data_dict['timestamp'] = "T".join(line[0].split(" "));
		data_dict['airq'] = float(line[1].split(':')[1]);
		data_dict['temperature'] = float(line[2].split(':')[1]);
		data_dict['humidity'] = float(line[3].split(':')[1]);
		data_dict['pressure'] = float(line[4].split(':')[1]);

		iaq_accuracy = int(list(line[1].split(':')[0].split("(")[1])[0]);

		print("IAQ", data_dict['airq'])
		print("IAQ accuracy: ", iaq_accuracy)

		if iaq_accuracy < 2:
			counterAccuracy += 1;
			# if sensor accuracy does not calibrate in 30min, then exit.
			if counterAccuracy > 600:
				print ("SENSOR CALIBRATION NEEDED!");
				exit();
		else:
			counterAccuracy = 0;

		# save to the db every minute
		if counter == 20: # equals to 60 seconds since each line is being read every 3 seconds
			mycol.insert_one(data_dict)
			counter = 0;

		if not line: break

except errors.ServerSelectionTimeoutError as err:
		# catch pymongo.errors.ServerSelectionTimeoutError
		print ("pymongo ERROR:", err)
		exit();