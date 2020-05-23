FROM ubuntu:16.04

MAINTAINER Boyan Naydenov "boyan.naydenov@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python3 python3-dev python3-pip

WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install pymongo

COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "-u", "main.py" ]
