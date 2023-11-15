FROM ubuntu:22.04

# RUN sed -i -e "s/archive.ubuntu.com/old-releases.ubuntu.com/g" /etc/apt/sources.list

RUN apt-get update && apt-get install -y wget time

RUN mkdir -p /workspace/flowdroid/soot-infoflow-cmd/target &&\
    mkdir -p /workspace/flowdroid/soot-infoflow-android &&\
    wget -O /workspace/flowdroid/soot-infoflow-cmd/target/soot-infoflow-cmd-jar-with-dependencies.jar https://github.com/secure-software-engineering/FlowDroid/releases/download/v2.10/soot-infoflow-cmd-jar-with-dependencies.jar &&\
    wget -O /workspace/flowdroid/soot-infoflow-android/SourcesAndSinks.txt https://raw.githubusercontent.com/secure-software-engineering/FlowDroid/v2.10/soot-infoflow-android/SourcesAndSinks.txt

RUN apt-get update && apt-get install -y openjdk-8-jdk sdkmanager

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

RUN update-java-alternatives -s /usr/lib/jvm/java-1.8.0-openjdk-amd64

# Run for one app:
# cd /workspace/flowdroid && java -jar soot-infoflow-cmd/target/soot-infoflow-cmd-jar-with-dependencies.jar -a DroidBench/apk/Lifecycle/ActivityLifecycle1.apk -p /opt/android-sdk/platforms/ -s soot-infoflow-android/SourcesAndSinks.txt

COPY run.sh /
