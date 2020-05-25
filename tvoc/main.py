import time, bme680, json
from pi_bme680 import Sensor
from pymongo import MongoClient,errors


# global variables for MongoDB host (default port is 27017)
DB_DOMAIN = 'mydb'
DB_PORT = 27017


def getEnv():
	env = {}
	with open("../env.env") as f:
		for line in f.readlines():
			key, value = line.rstrip("\n").split("=")
			env[key] = value
	return env;

def connectToDB():
	client = MongoClient(
		host = [ str(DB_DOMAIN) + ":" + str(DB_PORT) ],
		serverSelectionTimeoutMS = 3000, # 3 second timeout
	)

	# creates/selects db
	mydb = client["air_data"]
	return mydb;

### Initialise the sensor
sensor = Sensor(bme680)
sensor.initialise(bme680)
gas_baseline =  sensor.getGasSensorBaseline();
print("Gas baseline obtained");

try:
	mydb = connectToDB();
	mycol = mydb["bme680"];
	while True:
		time.sleep(60)
		data_dict = sensor.getData(gas_baseline);

#		mydoc = {
#					"timestamp": datetime.datetime.now().replace(microsecond=0).isoformat(),
#					"temperature": data_dict['temperature'],
#					"pressure": data_dict['pressure'],
#					"humidity": data_dict['humidity'],
#					"airq": data_dict['airq']
##				}

		mycol.insert_one(data_dict)

except errors.ServerSelectionTimeoutError as err:
		# catch pymongo.errors.ServerSelectionTimeoutError
		print ("pymongo ERROR:", err)
		exit();
