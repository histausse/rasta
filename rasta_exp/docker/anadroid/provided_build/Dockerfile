FROM ubuntu:12.04

RUN sed -i -e "s/archive.ubuntu.com/old-releases.ubuntu.com/g" /etc/apt/sources.list

RUN apt-get update && apt-get install -y git python2.7 time

RUN mkdir /workspace
RUN git clone https://github.com/maggieddie/pushdownoo.git /workspace/pushdownoo

RUN cd /workspace/pushdownoo && git checkout c06e03f6501d1441389d17271e44b9f345f637ff

RUN apt-get update && apt-get install -y openjdk-6-jdk make graphviz && \
    ln -s /usr/bin/dot /usr/local/bin/dot

RUN sed -i '266d' /workspace/pushdownoo/pdafordalvik/build.xml && \
    sed -i '262,264d' /workspace/pushdownoo/pdafordalvik/build.xml && \
    sed -i '163,164d' /workspace/pushdownoo/pdafordalvik/android-knowledge/sinks.txt && \
    sed -i '158d' /workspace/pushdownoo/pdafordalvik/android-knowledge/sinks.txt && \
    sed -i '80,83d' /workspace/pushdownoo/pdafordalvik/android-knowledge/classes.txt && \
    sed -i '410,412d' /workspace/pushdownoo/pdafordalvik/android-knowledge/callbacks.txt && \
    sed -i '407,408d' /workspace/pushdownoo/pdafordalvik/android-knowledge/callbacks.txt && \
    cd /workspace/pushdownoo/jdex2sex && make clean && make
COPY run.sh /
