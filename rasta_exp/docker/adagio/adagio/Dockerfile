FROM ubuntu:20.04

# RUN sed -i -e "s/archive.ubuntu.com/old-releases.ubuntu.com/g" /etc/apt/sources.list

RUN apt-get update && apt-get install -y git time

RUN mkdir /workspace

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python3.8 python3-pip python3-scipy python3-matplotlib python3-sklearn-lib

RUN git clone https://github.com/hgascon/adagio.git /workspace/adagio &&\
    cd /workspace/adagio && git checkout 8a2c1445df638d9c2fd2b1008a079cb092a63f0b &&\
    sed -i 's/matplotlib==3.1.1/#matplotlib==3.1.1/' /workspace/adagio/requirements.txt &&\
    sed -i 's/scikit-learn==0.21.2/#scikit-learn==0.21.2/' /workspace/adagio/requirements.txt &&\
    sed -i 's/scipy==1.3.0/#scipy==1.3.0/' /workspace/adagio/requirements.txt &&\
    pip3 install -r /workspace/adagio/requirements.txt

COPY run.sh /
