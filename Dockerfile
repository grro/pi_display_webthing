FROM python:3-alpine

ENV port 8070
ENV name Display
ENV i2c_expander PCF8574
ENV i2c_address 0x27


RUN cd /etc
RUN mkdir app
WORKDIR /etc/app
ADD *.py /etc/app/
ADD requirements.txt /etc/app/.
RUN pip install -r requirements.txt

CMD python /etc/app/display_webthing.py $port $name $i2c_expander $i2c_address


