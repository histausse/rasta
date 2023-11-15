FROM python:3.11-slim
RUN apt-get update && apt-get -y install time
COPY run.sh /

RUN python3 -m pip install androguard
