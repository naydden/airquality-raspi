import time

class Sensor():

	def __init__(self, bme680):
		self.sensor = bme680.BME680();

	def initialise(self,bme680):
		self.sensor.set_humidity_oversample(bme680.OS_2X)
		self.sensor.set_pressure_oversample(bme680.OS_4X)
		self.sensor.set_temperature_oversample(bme680.OS_8X)
		self.sensor.set_filter(bme680.FILTER_SIZE_3)
		self.sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
		self.sensor.set_gas_heater_temperature(320)
		self.sensor.set_gas_heater_duration(150)
		self.sensor.select_gas_heater_profile(0)

	def getGasSensorBaseline(self):
		start_time = time.time(self)
		curr_time = time.time()
		# takes 5 minutes to complete
		burn_in_time = 300

		burn_in_data = []

	    print("Collecting gas resistance burn-in data for 5 mins\n")
	    while curr_time - start_time < burn_in_time:
	        curr_time = time.time()
	        if self.sensor.get_sensor_data() and self.sensor.data.heat_stable:
	            gas = self.sensor.data.gas_resistance
	            burn_in_data.append(gas)
	            print("Gas: {0} Ohms".format(gas))
	            time.sleep(1)

	    gas_baseline = sum(burn_in_data[-50:]) / 50.0

	    print("Gas baseline: {0} Ohms, humidity baseline: {1:.2f} %RH\n".format(gas_baseline, hum_baseline))
	    return gas_baseline;

	def getAirQualityScore(self, gas_baseline):
        gas =  self.sensor.data.gas_resistance
        gas_offset = gas_baseline - gas

		# Set the humidity baseline to 40%, an optimal indoor humidity.
		hum_baseline = 40.0

		# This sets the balance between humidity and gas reading in the
		# calculation of air_quality_score (25:75, humidity:gas)
		hum_weighting = 0.25

        hum = self.sensor.data.humidity
        hum_offset = hum - hum_baseline

        # Calculate hum_score as the distance from the hum_baseline.
        if hum_offset > 0:
            hum_score = (100 - hum_baseline - hum_offset) / (100 - hum_baseline) * (hum_weighting * 100)

        else:
            hum_score = (hum_baseline + hum_offset) / hum_baseline * (hum_weighting * 100)

        # Calculate gas_score as the distance from the gas_baseline.
        if gas_offset > 0:
            gas_score = (gas / gas_baseline) * (100 - (hum_weighting * 100))

        else:
            gas_score = 100 - (hum_weighting * 100)

        # Calculate air_quality_score
        air_quality_score = hum_score + gas_score

        return air_quality_score;

	def getData(self):
		data_dict = {};
		output = '';

		gas_baseline = getGasSensorBaseline();

		if self.sensor.get_sensor_data() and self.sensor.data.heat_stable:
			data_dict['timestamp'] = datetime.datetime.now().replace(microsecond=0).isoformat();
			data_dict['temperature'] = self.sensor.data.temperature;
			data_dict['pressure'] = self.sensor.data.pressure;
			data_dict['humidity'] = self.sensor.data.humidity;
			data_dict['airq'] = getAirQualityScore(gas_baseline);
		else:
			data_dict['timestamp'] = datetime.datetime.now().replace(microsecond=0).isoformat();
			data_dict['temperature'] = 0;
			data_dict['pressure'] = 0;
			data_dict['humidity'] = 0;
			data_dict['airq'] = 0;

		return data_dict;