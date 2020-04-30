FROM ubuntu:16.04

MAINTAINER Boyan Naydenov "boyan.naydenov@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python3 python3-dev python3-pip

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# BME680 related libraries. This will only work on a Raspberry PI since it needs GPIO access.

RUN curl https://get.pimoroni.com/i2c | bash
RUN git clone https://github.com/pimoroni/bme680
RUN sudo python3 ./bme680/library/setup.py install
RUN sudo pip3 install bme680

COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "main.py" ]