FROM ubuntu:16.04

MAINTAINER Boyan Naydenov "boyan.naydenov@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python3 python3-dev python3-pip

COPY ./web/requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY ./web/ /app

ENTRYPOINT [ "python3" ]

CMD [ "-u", "main.py" ]
