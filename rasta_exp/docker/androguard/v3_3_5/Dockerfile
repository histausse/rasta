FROM python:3.11-slim
RUN apt-get update && apt-get -y install time python3-pip git
COPY run.sh /


RUN mkdir /workspace

RUN git clone --depth 1 --branch v3.3.5 https://github.com/androguard/androguard.git /workspace/androguard
RUN python3 -m pip install -e /workspace/androguard
COPY main.py /workspace/
