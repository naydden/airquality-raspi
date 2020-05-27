from flask import Flask, request, render_template, Response, jsonify
from pymongo import MongoClient,errors
import datetime, time, json

app = Flask(__name__)


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


### Define routes

@app.route('/index')
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/bme680')
def bme680():
	air_data = [];
	try:
		print("ENTRANDO")
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
		print(air_data);
	except errors.ServerSelectionTimeoutError as err:
			# catch pymongo.errors.ServerSelectionTimeoutError
			print ("pymongo ERROR:", err)
			exit();
	return render_template('bme680.html', air_data=air_data)


@app.route('/bme680/<variable>')
def bme680_temp(variable):
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
	return render_template('bme680_singleView.html', air_data=air_data, variable=variable)

# @app.route('/stream')
# def stream():
# 	def eventStream():
# 		while True:
# 			time.sleep(1)
# 			st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
# 			data_dict = sensor.getData();

# 			# yield jsonify(data_dict)
# 			yield 'data: {}\n\n'.format(json.dumps(data_dict))

# 	return Response(eventStream(), mimetype="text/event-stream")


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', threaded=True)







