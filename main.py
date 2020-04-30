from flask import Flask, request, render_template
from flask import Response
import time
import bme680


# https://medium.com/@rchang/learning-how-to-build-a-web-application-c5499bd15c8f#.bdph6phki

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Air

app = Flask(__name__)
sensor = bme680.BME680()

#Connect to Database and create database session
engine = create_engine('sqlite:///air-data.db')
Base.metadata.bind = engine

## Start raspi server here and poll it later

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


# #This will let us Create a new book and save it in our database
# @app.route('/books/new/',methods=['GET','POST'])
# def newBook():
#    if request.method == 'POST':
#        newBook = Book(title = request.form['name'], author = request.form['author'], genre = request.form['genre'])
#        session.add(newBook)
#        session.commit()
#        return redirect(url_for('showBooks'))
#    else:
#        return render_template('newBook.html')


# #This will let us Update our books and save it in our database
# @app.route("/books/<int:book_id>/edit/", methods = ['GET', 'POST'])
# def editBook(book_id):
#    editedBook = session.query(Book).filter_by(id=book_id).one()
#    if request.method == 'POST':
#        if request.form['name']:
#            editedBook.title = request.form['name']
#            return redirect(url_for('showBooks'))
#    else:
#        return render_template('editBook.html', book = editedBook)

# #This will let us Delete our book
# @app.route('/books/<int:book_id>/delete/', methods = ['GET','POST'])
# def deleteBook(book_id):
#    bookToDelete = session.query(Book).filter_by(id=book_id).one()
#    if request.method == 'POST':
#        session.delete(bookToDelete)
#        session.commit()
#        return redirect(url_for('showBooks', book_id=book_id))
#    else:
#        return render_template('deleteBook.html',book = bookToDelete)


# try:
# 	while True:
# 		if sensor.get_sensor_data():
# 			output = "{0:.2f} C,{1:.2f} hPa,{2:.2f} %RH".format(sensor.data.temperature, sensor.data.pressure, sensor.data.humidity)

# 			if sensor.data.heat_stable:
# 				print("{0},{1} Ohms".format(output, sensor.data.gas_resistance))

# 			else:
# 				print(output)

# 		time.sleep(1)

# except KeyboardInterrupt:
# 	pass

# def get_message():
# 	'''this could be any function that blocks until data is ready'''
# 	# poll raspi server here, save to database and return database last entry
# 	time.sleep(1.0)
# 	s = time.ctime(time.time())
# 	return s

@app.route('/stream')
def stream():
	def eventStream():
		while True:
			if sensor.get_sensor_data():
				output = "{0:.2f} C,{1:.2f} hPa,{2:.2f} %RH".format(sensor.data.temperature, sensor.data.pressure, sensor.data.humidity)

				if sensor.data.heat_stable:
					output = "{0},{1} Ohms".format(output, sensor.data.gas_resistance)
			time.sleep(1)
			yield 'data: {}\n\n'.format(output)
	return Response(eventStream(), mimetype="text/event-stream")


def initiate_sensor():
	# These calibration data can safely be commented
	# out, if desired.

	print("Calibration data:")
	for name in dir(sensor.calibration_data):

		if not name.startswith('_'):
			value = getattr(sensor.calibration_data, name)

			if isinstance(value, int):
				print("{}: {}".format(name, value))

		# These oversampling settings can be tweaked to 
		# change the balance between accuracy and noise in
		# the data.

		sensor.set_humidity_oversample(bme680.OS_2X)
		sensor.set_pressure_oversample(bme680.OS_4X)
		sensor.set_temperature_oversample(bme680.OS_8X)
		sensor.set_filter(bme680.FILTER_SIZE_3)
		sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

		print("\n\nInitial reading:")
		for name in dir(sensor.data):
			value = getattr(sensor.data, name)

		if not name.startswith('_'):
			print("{}: {}".format(name, value))

		sensor.set_gas_heater_temperature(320)
		sensor.set_gas_heater_duration(150)
		sensor.select_gas_heater_profile(0)

		# Up to 10 heater profiles can be configured, each
		# with their own temperature and duration.
		# sensor.set_gas_heater_profile(200, 150, nb_profile=1)
		# sensor.select_gas_heater_profile(1)


if __name__ == '__main__':
	initiate_sensor();
	app.run(debug=True, host='0.0.0.0', threaded=True)