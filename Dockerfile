FROM python:2.7-slim

WORKDIR /app
ADD config/ /app/config
ADD grabber.py /app/grabber.py
ADD intelfeed.py /app/intelfeed.py
ADD scripts /app/scripts

RUN apt-get update -y
RUN apt install python-pip default-jre -y
RUN pip install wget

EXPOSE 1337

CMD ["python", "intelfeed.py", "1337"]
