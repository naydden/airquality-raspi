from subprocess import Popen, PIPE, STDOUT
from pymongo import MongoClient,errors

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
	while True:

		line = p.stdout.readline().decode('UTF-8');
		counter += 1;
		line = line.split(',');

		data_dict['timestamp'] = "T".join(line[0].split(" "));
		data_dict['airq'] = float(line[1].split(':')[1]);
		data_dict['temperature'] = float(line[2].split(':')[1]);
		data_dict['humidity'] = float(line[3].split(':')[1]);
		data_dict['pressure'] = float(line[4].split(':')[1]);

		# save to the db every minute
		if counter == 20: # equals to 60 seconds since each line is being read every 3 seconds
			mycol.insert_one(data_dict)
			counter = 0;

		if not line: break

except errors.ServerSelectionTimeoutError as err:
		# catch pymongo.errors.ServerSelectionTimeoutError
		print ("pymongo ERROR:", err)
		exit();