FROM ubuntu:16.04

# RUN sed -i -e "s/archive.ubuntu.com/old-releases.ubuntu.com/g" /etc/apt/sources.list

RUN apt-get update && apt-get install -y git time

RUN mkdir /workspace

RUN apt-get update && apt-get install -y python-pip

RUN git clone https://github.com/sfahl/mallodroid.git /workspace/mallodroid &&\
    cd /workspace/mallodroid && git checkout 78f4e524be143c7776a7d4f9c62b035fa2bdd84a &&\
    sed -i '428i\\	print "ee3d6c7015b83b3dc84b21a2e79506175f07c00ecf03e7b3b8edea4e445618bd: END OF ANALYSIS."' /workspace/mallodroid/mallodroid.py

RUN pip install androguard==3.0 # Python2 compatible

COPY run.sh /
