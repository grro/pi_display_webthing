FROM python:3.9.1-alpine

ADD . /tmp/
WORKDIR /tmp/
RUN  python /tmp/setup.py install
WORKDIR /
RUN rm -r /tmp/

CMD display --command listen --port $port --i2c_expander $i2c_expander --i2c_address $i2c_address