FROM ubuntu:14.04

# RUN sed -i -e "s/archive.ubuntu.com/old-releases.ubuntu.com/g" /etc/apt/sources.list

RUN apt-get update && apt-get install -y git time

RUN mkdir /workspace
RUN git init /workspace/hopper && \
    cd /workspace/hopper && \
    git remote add origin https://github.com/cuplv/hopper.git && \
    git fetch --depth=1 origin 9f0e99360468f74762cacc81dcba933ac255bc87 && \
    git reset --hard FETCH_HEAD

RUN git init /workspace/droidel && \
    cd /workspace/droidel && \
    git remote add origin https://github.com/cuplv/droidel.git && \
    git fetch --depth=1 origin 04dd9858a20d166571b56af164059aad5ebe60d2 && \
    git reset --hard FETCH_HEAD

RUN apt-get update && apt-get install -y openjdk-7-jdk ant wget unzip maven maven2 binutils g++ \
        make scala python

RUN cd /workspace/ && \
    wget http://downloads.sourceforge.net/project/dex2jar/dex2jar-2.0-20140818.061505-10.zip && \
    unzip dex2jar-2.0-20140818.061505-10.zip && rm dex2jar-2.0-20140818.061505-10.zip && \
    mv dex2jar-2.0-SNAPSHOT dex2jar && \
    chmod +x /workspace/dex2jar/*

RUN cd /workspace/ && \
    wget -O - https://github.com/sbt/sbt/releases/download/v0.13.18/sbt-0.13.18.tgz | tar xzv && \
    cd sbt && \
    mkdir -p /root/.ivy2/local && \
    cp -r lib/local-preloaded/* /root/.ivy2/local/

ENV PATH="/workspace/sbt/bin:/workspace/dex2jar:$PATH"

RUN mkdir /workspace/hopper/lib &&  git init /workspace/hopper/lib/z3 && \
    cd /workspace/hopper/lib/z3 && \
    git remote add origin https://github.com/Z3Prover/z3.git && \
    git fetch --depth=1 origin  7f6ef0b6c0813f2e9e8f993d45722c0e5b99e152 && \
    git reset --hard FETCH_HEAD && \
    python scripts/mk_make.py --java && cd build && make && \
    cp *.jar ../.. && cp *.so ../..

RUN sed -i 's#cd walautil#cd walautil \&\& git checkout 6aad86d730da36f6b21363a14612eb7fa45535ac#' /workspace/droidel/lib/install_deps.sh && \
    sed -i 's#cd jphantom#cd jphantom \&\& git checkout 097a8f82bd09cf32b7826fa3876be4018c3eb562#' /workspace/droidel/lib/install_deps.sh  && \
    sed -i 's#javac#javac -encoding ISO-8859-1#g' /workspace/droidel/stubs/compile_stubs.sh && \
    cd /workspace/droidel/lib/ && ./install_deps.sh && \
    cd /workspace/droidel && sbt compile && sbt publishLocal

COPY android-4.4.2.jar /workspace/droidel/stubs/

RUN cd /workspace/droidel/stubs/ && \
    ./compile_stubs.sh android-4.4.2.jar && \
    cp /workspace/droidel/stubs/out/droidel_android-4.4.2.jar /workspace/hopper/lib/

RUN cd /workspace/hopper && \
    sed -i 's#target/scala-2.10/hopper_2.10-0.1-one-jar.jar#/workspace/hopper/target/scala-2.10/hopper_2.10-0.1-one-jar.jar#' /workspace/hopper/hopper.sh && \
    sed -i 's#pwd#dirname -- "$(readlink -f "${BASH_SOURCE}")"#' /workspace/hopper/hopper.sh && \
    sbt one-jar

COPY run.sh /
