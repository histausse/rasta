FROM ubuntu:22.04

RUN apt-get update && apt-get install -y time wget

ENV GatorRoot /workspace/gator
RUN mkdir /workspace && cd /workspace && \
    wget http://web.cse.ohio-state.edu/presto/software/gator/downloads/gator-3.8.tar.gz && \
    tar xzf gator-3.8.tar.gz && rm gator-3.8.tar.gz && \
    mv gator-3.8 gator 

RUN apt-get update && apt-get install -y openjdk-8-jdk python3 openjdk-19-jdk unzip

# We need to download some API that are not available from the linux sdkmanager
# like 'addon-google_apis-google-23', funny thing: the sdkmanager from google is not
# java-8 compatible, but there is no garenty that gator is compatible with java > 8
RUN mkdir -p /opt/android-sdk && \
    cd /opt/android-sdk && \
    wget https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip && \
    unzip commandlinetools-linux-9477386_latest.zip && rm commandlinetools-linux-9477386_latest.zip

ENV PATH="/opt/android-sdk/cmdline-tools/bin:$PATH"

RUN yes | sdkmanager --sdk_root=/opt/android-sdk --licenses &&\
    sdkmanager --sdk_root=/opt/android-sdk "platforms;android-10" &&\
    sdkmanager --sdk_root=/opt/android-sdk "platforms;android-11" &&\
    sdkmanager --sdk_root=/opt/android-sdk "platforms;android-12" &&\
    sdkmanager --sdk_root=/opt/android-sdk "platforms;android-13" &&\
    sdkmanager --sdk_root=/opt/android-sdk "platforms;android-14" &&\
    sdkmanager --sdk_root=/opt/android-sdk "platforms;android-15" &&\
    sdkmanager --sdk_root=/opt/android-sdk "platforms;android-16" &&\
    sdkmanager --sdk_root=/opt/android-sdk "platforms;android-17" &&\
    sdkmanager --sdk_root=/opt/android-sdk "platforms;android-18" &&\
    sdkmanager --sdk_root=/opt/android-sdk "platforms;android-19" &&\
    sdkmanager --sdk_root=/opt/android-sdk "platforms;android-20" &&\
    sdkmanager --sdk_root=/opt/android-sdk "platforms;android-21" &&\
    sdkmanager --sdk_root=/opt/android-sdk "platforms;android-22" &&\
    sdkmanager --sdk_root=/opt/android-sdk "platforms;android-23" &&\
    sdkmanager --sdk_root=/opt/android-sdk "platforms;android-24" &&\
    sdkmanager --sdk_root=/opt/android-sdk "platforms;android-25" &&\
    sdkmanager --sdk_root=/opt/android-sdk "platforms;android-26" &&\
    sdkmanager --sdk_root=/opt/android-sdk "platforms;android-27" &&\
    sdkmanager --sdk_root=/opt/android-sdk "platforms;android-28" &&\
    sdkmanager --sdk_root=/opt/android-sdk "platforms;android-29" &&\
    sdkmanager --sdk_root=/opt/android-sdk "platforms;android-3"  &&\
    sdkmanager --sdk_root=/opt/android-sdk "platforms;android-30" &&\
    sdkmanager --sdk_root=/opt/android-sdk "platforms;android-31" &&\
    sdkmanager --sdk_root=/opt/android-sdk "platforms;android-32" &&\
    sdkmanager --sdk_root=/opt/android-sdk "platforms;android-33" &&\
    sdkmanager --sdk_root=/opt/android-sdk "platforms;android-4"  &&\
    sdkmanager --sdk_root=/opt/android-sdk "platforms;android-5"  &&\
    sdkmanager --sdk_root=/opt/android-sdk "platforms;android-6"  &&\
    sdkmanager --sdk_root=/opt/android-sdk "platforms;android-7"  &&\
    sdkmanager --sdk_root=/opt/android-sdk "platforms;android-8"
RUN sdkmanager --sdk_root=/opt/android-sdk "add-ons;addon-google_apis-google-3"  &&\
    sdkmanager --sdk_root=/opt/android-sdk "add-ons;addon-google_apis-google-4"  &&\
    sdkmanager --sdk_root=/opt/android-sdk "add-ons;addon-google_apis-google-5"  &&\
    sdkmanager --sdk_root=/opt/android-sdk "add-ons;addon-google_apis-google-6"  &&\
    sdkmanager --sdk_root=/opt/android-sdk "add-ons;addon-google_apis-google-7"  &&\
    sdkmanager --sdk_root=/opt/android-sdk "add-ons;addon-google_apis-google-8"  &&\
    sdkmanager --sdk_root=/opt/android-sdk "add-ons;addon-google_apis-google-9"  &&\
    sdkmanager --sdk_root=/opt/android-sdk "add-ons;addon-google_apis-google-10"  &&\
    sdkmanager --sdk_root=/opt/android-sdk "add-ons;addon-google_apis-google-11"  &&\
    sdkmanager --sdk_root=/opt/android-sdk "add-ons;addon-google_apis-google-12"  &&\
    sdkmanager --sdk_root=/opt/android-sdk "add-ons;addon-google_apis-google-13"  &&\
    sdkmanager --sdk_root=/opt/android-sdk "add-ons;addon-google_apis-google-14"  &&\
    sdkmanager --sdk_root=/opt/android-sdk "add-ons;addon-google_apis-google-15"  &&\
    sdkmanager --sdk_root=/opt/android-sdk "add-ons;addon-google_apis-google-16"  &&\
    sdkmanager --sdk_root=/opt/android-sdk "add-ons;addon-google_apis-google-17"  &&\
    sdkmanager --sdk_root=/opt/android-sdk "add-ons;addon-google_apis-google-18"  &&\
    sdkmanager --sdk_root=/opt/android-sdk "add-ons;addon-google_apis-google-19"  &&\
    sdkmanager --sdk_root=/opt/android-sdk "add-ons;addon-google_apis-google-21"  &&\
    sdkmanager --sdk_root=/opt/android-sdk "add-ons;addon-google_apis-google-22"  &&\
    sdkmanager --sdk_root=/opt/android-sdk "add-ons;addon-google_apis-google-23"  &&\
    sdkmanager --sdk_root=/opt/android-sdk "add-ons;addon-google_apis-google-24" 
#RUN sdkmanager --sdk_root=/opt/android-sdk "add-ons;addon-google_apis-google-20" 
#RUN sdkmanager --sdk_root=/opt/android-sdk "add-ons;addon-google_apis-google-25" 
#RUN sdkmanager --sdk_root=/opt/android-sdk "add-ons;addon-google_apis-google-26" 
#RUN sdkmanager --sdk_root=/opt/android-sdk "add-ons;addon-google_apis-google-27" 
#RUN sdkmanager --sdk_root=/opt/android-sdk "add-ons;addon-google_apis-google-28" 
#RUN sdkmanager --sdk_root=/opt/android-sdk "add-ons;addon-google_apis-google-29" 
#RUN sdkmanager --sdk_root=/opt/android-sdk "add-ons;addon-google_apis-google-30" 
#RUN sdkmanager --sdk_root=/opt/android-sdk "add-ons;addon-google_apis-google-31" 
#RUN sdkmanager --sdk_root=/opt/android-sdk "add-ons;addon-google_apis-google-32" 
#RUN sdkmanager --sdk_root=/opt/android-sdk "add-ons;addon-google_apis-google-33" 
#RUN sdkmanager --sdk_root=/opt/android-sdk "add-ons;addon-google_apis-google-34"

ENV GatorRoot=/workspace/gator
ENV ANDROID_SDK=/opt/android-sdk
RUN mkdir -p /opt/android-sdk/tools/bin/ && \
    ln -s /opt/android-sdk/cmdline-tools/bin/sdkmanager /opt/android-sdk/tools/bin/sdkmanager && \
    update-java-alternatives -s /usr/lib/jvm/java-1.8.0-openjdk-amd64

RUN cd /workspace/gator/gator && ./gator b
RUN sed -i "s/cmd = \['java', '-Xmx12G',/cmd = ['java', *os.environ.get('JAVA_PARAM', '-Xmx12G').split(),/" /workspace/gator/gator/gator

COPY ./run.sh /
