FROM ubuntu:12.04

RUN sed -i -e "s/archive.ubuntu.com/old-releases.ubuntu.com/g" /etc/apt/sources.list

RUN apt-get update && apt-get install -y git python2.7 time

RUN mkdir /workspace
RUN git clone https://github.com/maggieddie/pushdownoo.git /workspace/pushdownoo

RUN cd /workspace/pushdownoo && git checkout c06e03f6501d1441389d17271e44b9f345f637ff

RUN apt-get update && apt-get install -y ant openjdk-6-jdk make graphviz && \
    ln -s /usr/bin/dot /usr/local/bin/dot

RUN cd /workspace/pushdownoo/jdex2sex && make clean && make
RUN mkdir /workspace/pushdownoo/pdafordalvik/test && \
    cd /workspace/pushdownoo/pdafordalvik && \
    sed -i '266d' /workspace/pushdownoo/pdafordalvik/build.xml && \
    sed -i '262,264d' /workspace/pushdownoo/pdafordalvik/build.xml && \
    sed -i '163,164d' /workspace/pushdownoo/pdafordalvik/android-knowledge/sinks.txt && \
    sed -i '158d' /workspace/pushdownoo/pdafordalvik/android-knowledge/sinks.txt && \
    sed -i '80,83d' /workspace/pushdownoo/pdafordalvik/android-knowledge/classes.txt && \
    sed -i '410,412d' /workspace/pushdownoo/pdafordalvik/android-knowledge/callbacks.txt && \
    sed -i '407,408d' /workspace/pushdownoo/pdafordalvik/android-knowledge/callbacks.txt && \
    sed -i '263i\\      println("ee3d6c7015b83b3dc84b21a2e79506175f07c00ecf03e7b3b8edea4e445618bd: END OF ANALYSIS.")' /workspace/pushdownoo/pdafordalvik/src/org/ucombinator/playhelpers/PlayHelper.scala && \
    sed -i '116i\\    println("ee3d6c7015b83b3dc84b21a2e79506175f07c00ecf03e7b3b8edea4e445618bd: START OF ANALYSIS.")' /workspace/pushdownoo/pdafordalvik/src/org/ucombinator/playhelpers/PlayHelper.scala && \
    sed -i 's#^exec java# exec java -Duser.home=/tmp/user/#' ../apktool/apktool && \
    export ANT_OPTS="-Xmx2048M -Xms2048M -Xss512M -XX:MaxPermSize=512m" && \
    make
COPY run.sh /
