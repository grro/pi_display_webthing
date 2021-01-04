FROM python:3.9.1-alpine

ENV port 8070
ENV name display

ADD . /tmp/
WORKDIR /tmp/
RUN  python /tmp/setup.py install
WORKDIR /
RUN rm -r /tmp/

CMD display --command listen --name $name --port $port --i2c_expander $i2c_expander --i2c_address $i2c_address