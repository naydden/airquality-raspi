FROM ubuntu:16.04

MAINTAINER Boyan Naydenov "boyan.naydenov@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python3 python3-dev python3-pip unzip curl

COPY ./web/requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY ./web/ /app

WORKDIR /app/static/static

RUN curl -S -ko ./d3/d3.v5.min.js https://d3js.org/d3.v5.min.js
RUN curl -SL -ko zipped.zip https://github.com/twbs/bootstrap/releases/download/v4.3.1/bootstrap-4.3.1-dist.zip && \
    unzip zipped.zip -d ./bootstrap && \
    rm -f zipped.zip
RUN curl -S -ko ./jquery/jquery-3.5.0.min.js https://code.jquery.com/jquery-3.5.0.min.js

WORKDIR /app

ENTRYPOINT [ "python3" ]

CMD [ "-u", "main.py" ]
