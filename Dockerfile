FROM ubuntu:16.04

MAINTAINER Boyan Naydenov "boyan.naydenov@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python3 python3-dev python3-pip

RUN apt-get install -y git

COPY ./requirements.txt /app/requirements.txt


WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# BME680 related libraries. This will only work on a Raspberry PI since it needs GPIO access.

RUN git clone https://github.com/pimoroni/bme680

WORKDIR ./bme680/library
RUN python3 setup.py install

WORKDIR ../../
RUN pip3 install bme680

COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "main.py" ]
