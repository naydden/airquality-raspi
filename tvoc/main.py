import datetime, time, bme680, json
from pi_bme680 import Sensor

### Initialise the sensor
sensor = Sensor(bme680)
sensor.initialise(bme680)

while True:
	time.sleep(1)
	data_dict = sensor.getData();
	print(data_dict['str']);