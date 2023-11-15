FROM ubuntu:14.04

# RUN sed -i -e "s/archive.ubuntu.com/old-releases.ubuntu.com/g" /etc/apt/sources.list
RUN apt-get update && apt-get install -y git time

RUN mkdir /workspace
RUN git clone https://github.com/ub-rms/blueseal.git /workspace/blueseal && \
    cd /workspace/blueseal && git checkout 95e820049f9ded681019724d0b4a86dc028bd78b

RUN rm -rf /workspace/blueseal/BlueSeal/android-jars && \
    git clone https://github.com/Sable/android-platforms.git /workspace/blueseal/BlueSeal/android-jars && \
    cd /workspace/blueseal/BlueSeal/android-jars && git checkout 74c993c02160cdeb1d52e46017a2ecd536ea1d5d


RUN apt-get update && apt-get install -y openjdk-7-jdk ant

RUN cd /workspace/blueseal/BlueSeal && mkdir /workspace/blueseal/BlueSeal/bin && \
    ant build

RUN sed -i 's#^exec java# exec java -Duser.home=/tmp/user/#' /workspace/blueseal/BlueSeal/tools/apktool
COPY run.sh /
