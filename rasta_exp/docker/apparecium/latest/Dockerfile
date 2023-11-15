FROM ubuntu:22.04

# RUN sed -i -e "s/archive.ubuntu.com/old-releases.ubuntu.com/g" /etc/apt/sources.list

RUN apt-get update && apt-get install -y git time

RUN mkdir /workspace
RUN git init /workspace/apparecium && \
    cd /workspace/apparecium && \
    git remote add origin https://github.com/askk/apparecium.git && \
    git fetch --depth=1 origin e27e108950e56b69f34fa97262c07d154b9163e8 && \
    git reset --hard FETCH_HEAD

RUN apt-get update && apt-get install -y python2.7 wget && \
    ln -s /usr/bin/python2.7 /usr/bin/python

RUN wget https://bootstrap.pypa.io/pip/2.7/get-pip.py && \
    python2.7 get-pip.py && \
    rm get-pip.py && \
    python2.7 -m pip install pydot 
RUN sed -i 's#d3-visualization#/mnt#' /workspace/apparecium/dftest.py

COPY run.sh /
