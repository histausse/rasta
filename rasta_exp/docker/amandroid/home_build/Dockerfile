FROM ubuntu:22.04

# RUN sed -i -e "s/archive.ubuntu.com/old-releases.ubuntu.com/g" /etc/apt/sources.list

RUN apt-get update && apt-get install -y git time unzip wget

RUN mkdir /workspace
RUN git init /workspace/amandroid && \
    cd /workspace/amandroid && \
    git remote add origin https://github.com/arguslab/Argus-SAF.git && \
    git fetch --depth=1 origin v3.2.0 && \
    git reset --hard FETCH_HEAD

# Avoid downloading this each time we launch a new docker
RUN mkdir -p /workspace/.amandroid_stash && \
    cd /workspace/.amandroid_stash && \
    wget https://www.fengguow.dev/resources/amandroid.zip && \
    wget https://www.fengguow.dev/resources/amandroid.checksum && \
    unzip amandroid.zip

RUN apt-get update && apt-get install -y openjdk-8-jdk

RUN cd /workspace/amandroid && \
    sed -i 's/val remotec = getRemoteChecksum("amandroid.checksum")/\/\/val remotec = getRemoteChecksum("amandroid.checksum")/' /workspace/amandroid/amandroid/src/main/scala/org/argus/amandroid/core/AndroidGlobalConfig.scala && \
    sed -i '46i\\    val remotec = localc' /workspace/amandroid/amandroid/src/main/scala/org/argus/amandroid/core/AndroidGlobalConfig.scala && \ 
    sed -i '164i javacOptions in jawa ++= Seq("-encoding", "UTF-8")' /workspace/amandroid/build.sbt

RUN cd /workspace/amandroid && \
    ./tools/bin/sbt -Duser.home=/workspace clean compile assembly test 

RUN ln -s /workspace/amandroid/target/scala-2.12/argus-saf-3.2.0-assembly.jar /workspace/amandroid/argus-saf.jar

COPY run.sh /
