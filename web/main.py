from flask import Flask, request, render_template, Response, jsonify
from pymongo import MongoClient,errors
import datetime, time, json

app = Flask(__name__)


# global variables for MongoDB host (default port is 27017)
DB_DOMAIN = 'mydb'
DB_PORT = 27017

def getEnv():
	env = {}
	with open("env.env") as f:
		for line in f.readlines():
			key, value = line.rstrip("\n").split("=")
			env[key] = value
	return env;

def connectToDB():
	client = MongoClient(
		host = [ str(DB_DOMAIN) + ":" + str(DB_PORT) ],
		serverSelectionTimeoutMS = 3000, # 3 second timeout
		username = getEnv()['MONGODB_USER'],
		password = getEnv()['MONGODB_PASS'],
	)

	# creates/selects db
	mydb = client["air_data_prod"]
	return mydb;


### Define routes

@app.route('/index')
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/bme680')
def bme680():
	air_data = [];
	try:
		mydb = connectToDB();
		mycol = mydb["bme680"]
		for x in mycol.find():
			data = {
				'timestamp' : x['timestamp'],
				'temperature' : x['temperature'],
				'pressure' : x['pressure'],
				'humidity' : x['humidity'],
				'airq' : x['airq']
			}
			air_data.append(data);
	except errors.ServerSelectionTimeoutError as err:
			# catch pymongo.errors.ServerSelectionTimeoutError
			print ("pymongo ERROR:", err)
			exit();
	return render_template('bme680.html', air_data=air_data)

@app.route('/stream')
def stream():
	def eventStream():
		while True:
			time.sleep(1)
			st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
			data_dict = sensor.getData();

			# DBSession = sessionmaker(bind=engine)
			# session = DBSession()
			# session.add(Air(timestamp=st, airquality=data_dict['airq'], temperature=data_dict['temperature']
			# 	, pressure=data_dict['pressure'], humidity=data_dict['humidity']))
			# session.commit()

			# yield jsonify(data_dict)
			yield 'data: {}\n\n'.format(json.dumps(data_dict))

	return Response(eventStream(), mimetype="text/event-stream")


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', threaded=True)







