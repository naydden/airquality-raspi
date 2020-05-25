from flask import Flask, request, render_template, Response, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime, time, bme680, json

from pi_bme680 import Sensor
from database_setup import Base, Air

app = Flask(__name__)
sensor = Sensor(bme680)

### Initialise the sensor
sensor.initialise(bme680)

### Connect to Database and create database session
engine = create_engine('sqlite:///air-data.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine

### Define routes

@app.route('/index')
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/bme680')
def bme680():
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	air_data = session.query(Air).all()
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