FROM python:3-alpine

ENV port 8070
ENV name display


RUN cd /etc
RUN mkdir app
WORKDIR /etc/app
ADD *.py /etc/app/
ADD requirements.txt /etc/app/.
RUN pip install -r requirements.txt

CMD python /etc/app/display_webthing.py --port $port --i2c_expander $i2c_expander --i2c_address $i2c_address


