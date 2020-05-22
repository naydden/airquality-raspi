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

	def getData(self):
		data_dict = {};
		output = '';
		if self.sensor.get_sensor_data():
			output = "{0:.2f} C,{1:.2f} hPa,{2:.2f} %RH".format(self.sensor.data.temperature, self.sensor.data.pressure, self.sensor.data.humidity)

		if self.sensor.data.heat_stable:
			output = "{0},{1} Ohms".format(output, self.sensor.data.gas_resistance)
		data_dict['str'] = output;
		data_dict['temperature'] = self.sensor.data.temperature;
		data_dict['pressure'] = self.sensor.data.pressure;
		data_dict['humidity'] = self.sensor.data.humidity;
		data_dict['airq'] = self.sensor.data.gas_resistance;
		return data_dict;