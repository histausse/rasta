FROM ubuntu:12.04

RUN sed -i -e "s/archive.ubuntu.com/old-releases.ubuntu.com/g" /etc/apt/sources.list

RUN apt-get update && apt-get install -y wget time

RUN mkdir -p /workspace/dare && mkdir /workspace/ic3_bin /workspace/ic3 /workspace/maven

RUN apt-get update && apt-get install -y openjdk-7-jdk

# Install dare
RUN apt-get update && apt-get install -y ia32-libs
RUN wget https://github.com/dare-android/platform_dalvik/releases/download/dare-1.1.0/dare-1.1.0-linux.tgz && \
    tar -xzf dare-1.1.0-linux.tgz -C /workspace/dare --strip-components=1 && rm dare-1.1.0-linux.tgz && \
    cd /workspace/dare && ./dex-preopt --bootstrap

RUN wget https://github.com/siis/ic3/releases/download/v0.2.0/ic3-0.2.0-bin.tgz && \
    tar -xzf ic3-0.2.0-bin.tgz -C /workspace/ic3_bin --strip-components=1 && rm ic3-0.2.0-bin.tgz

COPY run.sh /workspace/run.sh
