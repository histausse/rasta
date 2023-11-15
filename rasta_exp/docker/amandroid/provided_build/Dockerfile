FROM ubuntu:18.04

# RUN sed -i -e "s/archive.ubuntu.com/old-releases.ubuntu.com/g" /etc/apt/sources.list

RUN apt-get update && apt-get install -y git time unzip wget

RUN mkdir /workspace
RUN git init /workspace/amandroid && \
    cd /workspace/amandroid && \
    git remote add origin https://github.com/arguslab/Argus-SAF.git && \
    git fetch --depth=1 origin 06596c6bb03fe2560030b52bf2b47d17d1bd3068 && \
    git reset --hard FETCH_HEAD

# Avoid downloading this each time we launch a new docker
RUN mkdir -p /root/.amandroid_stash && \
    cd /root/.amandroid_stash && \
    wget https://www.fengguow.dev/resources/amandroid.zip && \
    wget https://www.fengguow.dev/resources/amandroid.checksum && \
    unzip amandroid.zip

RUN apt-get update && apt-get install -y openjdk-8-jdk

RUN ln -s /workspace/amandroid/binaries/argus-saf-3.2.1-SNAPSHOT-assembly.jar /workspace/amandroid/argus-saf.jar
