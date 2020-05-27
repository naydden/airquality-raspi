# airquality-raspi

Micro-service application that measures air quality together with temperature, pressure and humidity. Composed of three main services:

- **tvoc**: uses bme680 sensor to extract air parameters data.
- **mydb**: saves data into a persistent database (MongoDB).
- **web**: shows data from mydb into the browser (flask + bootstrap + d3 v5).

The **test** service is used within the x86 branch for testing purposes. It substitutes the job of *tvoc* during development for faster iteration. It basically fills the database with fresh values when running the application on a x86 machine.


## Required technology:

- BME680 sensor
- Raspberry Pi
- Docker, Docker-compose, Flask, D3, MongoDB, Bootstrap

In order to run the project one needs to:

1. Install docker and docker-compose
2. Download jquery and put it under /web/static/jquery/.
3. Download bootstrap and put it under /web/static/bootstrap/.
4. Download d3 and put it under /web/static/d3/.

## Thoughts

This was my first project with a micro-services architecture and I am quite happy with the results. It allowed me to separate the different problems and tackle them in an easier and more organised way. The flexibility it offers is great too. I was able to easily switch between *tvoc* and *test* when changing the environment from the raspberry pi to my computer. On the other hand, docker containerisation is great for portability and dependencies management. Needless to say, docker-compose does a great job managing the different services making the overall work-flow much easier.

Some challenges I ran into:

- Exposing the i2c device to docker-composer network. This device is used by the sensor and needs to be accessible from the docker container.
- The armvl7 architecture and the Raspbian OS made it difficult to use MongoDB on the raspberry pi. Luckily, I [found](https://hub.docker.com/r/andresvidal/rpi3-mongodb3/) a mongodb image that uses pre-compiled 32bit ARM binaries. That is why I am not using the latest version.


## Some useful commands

-- To create a backup file of the stored data:

> docker-compose exec -T mydb mongodump -u $USR -p $PASS --authenticationDatabase admin --archive --gzip --db air_data > dump.gz

-- To recover a backup file into a db:

> docker-compose exec -T db mongorestore --archive --gzip < dump.gz

-- To expose a device to a docker container:

> docker run -d --rm --device /dev/i2c-1 --name tvoc tvoc

---

## About the BME680 sensor

To interact with the sensor, there is an open-source library from Pimoroni and a proprietary one, from Bosch, which is only available in C.

- [Pimoroni](https://pypi.org/project/bme680/)
- [Bosch](https://github.com/BoschSensortec/BME680_driver)

The air quality score calculation can be tricky.
