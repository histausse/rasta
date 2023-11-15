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

#RUN wget https://github.com/siis/ic3/releases/download/v0.2.0/ic3-0.2.0-bin.tgz && \
#    tar -xzf ic3-0.2.0-bin.tgz -C /workspace/ic3_bin --strip-components=1 && rm ic3-0.2.0-bin.tgz

# Install recent maven (for https)
RUN wget https://archive.apache.org/dist/maven/maven-3/3.8.7/binaries/apache-maven-3.8.7-bin.tar.gz --no-check-certificate && \
    echo '21c2be0a180a326353e8f6d12289f74bc7cd53080305f05358936f3a1b6dd4d91203f4cc799e81761cf5c53c5bbe9dcc13bdb27ec8f57ecf21b2f9ceec3c8d27  apache-maven-3.8.7-bin.tar.gz' | sha512sum --check &&\
    tar -xzf apache-maven-3.8.7-bin.tar.gz -C /workspace/maven --strip-components=1 && rm apache-maven-3.8.7-bin.tar.gz

ENV PATH="${PATH}://workspace/maven/bin"

RUN wget https://github.com/siis/ic3/archive/refs/tags/v0.2.0.tar.gz && \
    tar -xzf v0.2.0.tar.gz -C /workspace/ic3 --strip-components=1 && rm v0.2.0.tar.gz && \
    cd /workspace/ic3 && \
    mvn -Dhttps.protocols=TLSv1.2 clean compile package -P standalone

COPY run.sh /
