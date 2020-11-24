FROM Debian:10-slim

RUN mkdir /usr/src/app
WORKDIR /usr/src/app
ADD . /usr/src/app

RUN  apt install --no-install-recommends -y python3-distutils
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN cd /usr/src/app && python3 main.py --config json --build webhook --storage redis

RUN echo "service is run"