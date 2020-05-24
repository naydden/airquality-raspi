from pymongo import MongoClient,errors

# global variables for MongoDB host (default port is 27017)
DOMAIN = 'mydb'
PORT = 27017

def getEnv():
	env = {}
	with open("env.env") as f:
		for line in f.readlines():
			key, value = line.rstrip("\n").split("=")
			env[key] = value
	return env;


# use a try-except indentation to catch MongoClient() errors
try:
	# try to instantiate a client instance
	client = MongoClient(
		host = [ str(DOMAIN) + ":" + str(PORT) ],
		serverSelectionTimeoutMS = 3000, # 3 second timeout
		username = getEnv()['MONGODB_USER'],
		password = getEnv()['MONGODB_PASS'],
	)

	# print the version of MongoDB server if connection successful
	print ("server version:", client.server_info()["version"])

	# creates my db
	mydb = client["air_data"]

	# get the database_names from the MongoClient()
	database_names = client.list_database_names()
	print ("\ndatabases:", database_names)

	# creates a collection
	mycol = mydb["bme680"]
	# checks if collection exists
	print(mydb.list_collection_names())

	mydoc = { "timestamp": 3, "temperature": 0, "pressure": 0, "humidity": 0, "airq": 0 }
	mycol.insert_one(mydoc)
	mydoc = { "timestamp": 4, "temperature": 1, "pressure": 2, "humidity": 3, "airq": 4 }
	mycol.insert_one(mydoc)

	for x in mycol.find():
		print(x)

except errors.ServerSelectionTimeoutError as err:
	# set the client and DB name list to 'None' and `[]` if exception
	client = None
	database_names = []

	# catch pymongo.errors.ServerSelectionTimeoutError
	print ("pymongo ERROR:", err)

print ("\ndatabases:", database_names)




# client = MongoClient(<<MONGODB URL>>)
# db=client.admin
# # Issue the serverStatus command and print the results
# serverStatusResult=db.command("serverStatus")
# pprint(serverStatusResult)