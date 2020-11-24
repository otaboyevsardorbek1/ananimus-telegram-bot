FROM Debian:latest
FROM python:3.7.4

RUN mkdir /usr/src/app
WORKDIR /usr/src/app
ADD docker /usr/src/app

RUN  apt install --no-install-recommends -y python3-distutils
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY docker .

RUN cd /usr/src/app/src && python3 main.py --config json --build webhook --storage redis

RUN echo "service is run"