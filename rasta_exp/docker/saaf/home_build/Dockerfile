FROM ubuntu:14.04

# RUN sed -i -e "s/archive.ubuntu.com/old-releases.ubuntu.com/g" /etc/apt/sources.list

RUN apt-get update && apt-get install -y git time

RUN mkdir /workspace
RUN git init /workspace/saaf && \
    cd /workspace/saaf && \
    git remote add origin https://github.com/SAAF-Developers/saaf && \
    git fetch --depth=1 origin fc8dd8c86da2fa3c98ae9902e00c95ae248ecadb && \
    git reset --hard FETCH_HEAD

RUN apt-get update && apt-get install -y ant openjdk-6-jdk mysql-server

# This allows to pass the db tests, the db is not needed for running the tool
RUN mysqld & sleep 10 && \
    mysql -e 'CREATE DATABASE saaftest;' && \
    mysql -e "CREATE USER 'saafuser' IDENTIFIED BY 'saafpass';" && \
    mysql -e "GRANT ALL PRIVILEGES ON saaftest.* TO 'saafuser';"
    

RUN mysqld & sleep 10 && \
    update-java-alternatives -s /usr/lib/jvm/java-1.6.0-openjdk-amd64 &&  \
    export JAVA_TOOL_OPTIONS=-Dfile.encoding=UTF8 && \
    cd /workspace/saaf && ant clean && ant fat-jar

COPY run.sh /
