FROM ubuntu:22.04

#RUN sed -i -e "s/archive.ubuntu.com/old-releases.ubuntu.com/g" /etc/apt/sources.list

RUN apt-get update && apt-get install -y wget time git

RUN mkdir /workspace

RUN git init /workspace/ic3 && \
    cd /workspace/ic3 && \
    git remote add origin https://github.com/JordanSamhi/ic3.git && \
    git fetch --depth=1 origin 6a7828a5b7c7fb8d21f19086e27e0acb937769ba && \
    git reset --hard FETCH_HEAD

RUN apt-get update && apt-get install -y maven openjdk-8-jdk sdkmanager
RUN update-java-alternatives -s /usr/lib/jvm/java-1.8.0-openjdk-amd64

RUN sdkmanager "platforms;android-10" &&\
    sdkmanager "platforms;android-11" &&\
    sdkmanager "platforms;android-12" &&\
    sdkmanager "platforms;android-13" &&\
    sdkmanager "platforms;android-14" &&\
    sdkmanager "platforms;android-15" &&\
    sdkmanager "platforms;android-16" &&\
    sdkmanager "platforms;android-17" &&\
    sdkmanager "platforms;android-18" &&\
    sdkmanager "platforms;android-19" &&\
    sdkmanager "platforms;android-20" &&\
    sdkmanager "platforms;android-21" &&\
    sdkmanager "platforms;android-22" &&\
    sdkmanager "platforms;android-23" &&\
    sdkmanager "platforms;android-24" &&\
    sdkmanager "platforms;android-25" &&\
    sdkmanager "platforms;android-26" &&\
    sdkmanager "platforms;android-27" &&\
    sdkmanager "platforms;android-28" &&\
    sdkmanager "platforms;android-29" &&\
    sdkmanager "platforms;android-3"  &&\
    sdkmanager "platforms;android-30" &&\
    sdkmanager "platforms;android-31" &&\
    sdkmanager "platforms;android-32" &&\
    sdkmanager "platforms;android-33" &&\
    sdkmanager "platforms;android-4"  &&\
    sdkmanager "platforms;android-5"  &&\
    sdkmanager "platforms;android-6"  &&\
    sdkmanager "platforms;android-7"  &&\
    sdkmanager "platforms;android-8"
    #sdkmanager "platforms;android-9" for some reason this one 404

RUN cd /workspace/ic3 && \
    mvn clean install:install-file -Dfile=libs/coal-all-0.1.7.jar -DgroupId=edu.psu.cse.siis -DartifactId=coal -Dversion=0.1.7 -Dpackaging=jar && \
    mvn clean package -P standalone

COPY run.sh /
