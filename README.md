# realtime-webraspi

## For generating backup file
docker-compose exec -T mydb mongodump -u $USR -p $PASS --authenticationDatabase admin --archive --gzip --db air_data > dump.gz

## For recovring backup file
docker-compose exec -T db mongorestore --archive --gzip < dump.gz


Microservice application that measures air quality together with temperature, pressure and humidity. Composed of three main services:

- tvoc: uses bme680 sensor to extract data.
- mydb: saves data into a persisten database with a volume.
- web: shows data from mydb into the browser.

Technology:

- BME680 sensor
- Raspberry Pi
- Flask

It is intended to function as a home monitoring system, pushing data in real time to any client that may be listening on a specific port.

Requirements:
