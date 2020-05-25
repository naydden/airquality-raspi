FROM raspbian/stretch

MAINTAINER Boyan Naydenov "boyan.naydenov@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python3 python3-dev python3-pip && \
    apt-get install -y python3-smbus

RUN apt-get install -y git


WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install pymongo

# BME680 related libraries. This will only work on a Raspberry PI since it needs GPIO access.

RUN git clone https://github.com/pimoroni/bme680

WORKDIR ./bme680/library
RUN python3 setup.py install

WORKDIR ../../
RUN pip3 install bme680

COPY ./tvoc/ /app
COPY env.env /app

ENTRYPOINT [ "python3" ]

CMD [ "-u", "main.py" ]
