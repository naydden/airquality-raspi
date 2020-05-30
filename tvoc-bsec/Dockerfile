FROM raspbian/stretch

MAINTAINER Boyan Naydenov "boyan.naydenov@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python3 python3-dev python3-pip && \
    apt-get install -y python3-smbus

RUN apt-get install -y git

WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install pymongo

COPY ./tvoc-bsec/ /app

RUN git clone https://github.com/alexh-name/bsec_bme680_linux.git

RUN mv ./BSEC_1.4.7.4_Generic_Release/ ./bsec_bme680_linux/src/
WORKDIR ./bsec_bme680_linux/
RUN rm -rf make.config
RUN mv ../make.config .
RUN ./make.sh

WORKDIR ../

ENTRYPOINT [ "python3" ]

CMD [ "-u", "main.py" ]
