FROM ubuntu:18.04

RUN apt-get update && apt-get install -y git wget time openjdk-8-jdk ant mysql-server unzip

RUN mkdir /workspace && \
    git init /workspace/dialdroid && \
    cd /workspace/dialdroid && \
    git remote add origin https://github.com/dialdroid-android/DIALDroid.git && \
    git fetch --depth=1 origin 968577d43de9c2377a024593e2b2fcecb4b3e875 && \
    git reset --hard FETCH_HEAD

RUN git clone https://github.com/dialdroid-android/android-platforms.git /workspace/platforms && \
    git clone https://github.com/Sable/android-platforms.git /workspace/sable-platforms && \
    cp -R -n /workspace/sable-platforms/* /workspace/platforms/ && \
    rm -rf /workspace/sable-platforms

RUN git init /workspace/dialdroid_db && \
    cd /workspace/dialdroid_db && \
    git remote add origin https://github.com/dialdroid-android/dialdroid-db.git && \
    git fetch --depth=1 origin c8d364c11eaced258057d2b214547ccbd32edfc5 && \
    git reset --hard FETCH_HEAD

# RUN sed -i 's/mysql-connector-java-5.1.31.jar/mysql-connector-java-8.0.18.jar/g' /workspace/dialdroid/build.xml
RUN cd /workspace/dialdroid && \
    mkdir bin && \
    cp build/*.txt . && \
    cp build/cc.properties . && \
    rm -rf build/* && rm -rf target/* && \
    update-java-alternatives -s java-1.8.0-openjdk-amd64 && \
    ant create_run_jar

# jar in jar + singularity = problems... so:
RUN mkdir /workspace/dialdroid_bin && \
    mv /workspace/dialdroid/build/dialdroid.jar /workspace/dialdroid_bin && \
    cd /workspace/dialdroid_bin && \
    unzip dialdroid.jar
COPY run.sh /
