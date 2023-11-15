FROM ubuntu:22.04

# RUN sed -i -e "s/archive.ubuntu.com/old-releases.ubuntu.com/g" /etc/apt/sources.list

RUN apt-get update && apt-get install -y git time wget

RUN mkdir /workspace
RUN git init /workspace/dalvik-bytecode-analysis-tool && \
    cd /workspace/dalvik-bytecode-analysis-tool && \
    git remote add origin https://bitbucket.org/erw/dalvik-bytecode-analysis-tool.git && \
    git fetch --depth=1 origin 33f952eaf9048d8a040de369c8dd6c4a21477b07 && \
    git reset --hard FETCH_HEAD

RUN apt-get update && apt-get install -y python2.7 wget && \
    ln -s /usr/bin/python2.7 /usr/bin/python

RUN wget https://bootstrap.pypa.io/pip/2.7/get-pip.py && \
    python2.7 get-pip.py && \
    rm get-pip.py && \
    python2.7 -m pip install pydot


# Install a compatible version of apktool
RUN apt-get update && apt-get install -y  bzip2 openjdk-8-jdk && \
    cd /workspace && \
    wget https://connortumbleson.com/apktool/googlecode/apktool1.5.2.tar.bz2 && \
    tar -xjf apktool1.5.2.tar.bz2 && rm apktool1.5.2.tar.bz2 && \
    mkdir bin && \
    echo '#!/bin/sh' > bin/apktool && \
    echo 'java -jar /workspace/apktool1.5.2/apktool.jar $@' >> bin/apktool && \
    chmod +x bin/apktool

# Install XDB
RUN apt-get update && apt-get install -y gcc make && \
    cd /workspace && \
    wget https://xsb.sourceforge.net/downloads/XSB.tar.gz && \
    tar -xzf XSB.tar.gz && rm XSB.tar.gz && \
    cd /workspace/XSB/build && \
    ./configure && ./makexsb
# according to the doc xdb is a little picky about its invocation, this way we always use
# the absolute path
RUN echo '#!/bin/sh' > /workspace/bin/xsb && \
    echo '/workspace/XSB/bin/xsb "$@"' >> /workspace/bin/xsb && \
    chmod +x /workspace/bin/xsb

ENV PATH="${PATH}:/workspace/bin"

COPY run.sh /
COPY subrun.sh /
