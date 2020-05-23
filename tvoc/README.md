To run it in a Raspberry Pi we need to expose the sensor pin:

docker run -d --rm --device /dev/i2c-1 --name tvoc tvoc