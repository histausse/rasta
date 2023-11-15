FROM ubuntu:14.04

# RUN sed -i -e "s/archive.ubuntu.com/old-releases.ubuntu.com/g" /etc/apt/sources.list

RUN apt-get update && apt-get install -y git time

RUN mkdir /workspace
RUN git init /workspace/droidsafe && \
    cd /workspace/droidsafe && \
    git remote add origin https://github.com/MIT-PAC/droidsafe-src.git && \
    git fetch --depth=1 origin 1eab2fc473f3d32ba352280a6c520b216bd1b5df && \
    git reset --hard FETCH_HEAD

RUN apt-get update && apt-get install -y ant openjdk-7-jdk wget unzip make python

# Download the android-sdk (no sdk-manager on 12.04)
RUN apt-get update && apt-get install -y bsdtar && \
    mkdir -p /opt/android-sdk/platforms/android-3 && \
    wget -O /opt/android-sdk/platforms/android-3/zip.zip https://dl.google.com/android/repository/android-1.5_r04-linux.zip && \
    mkdir -p /opt/android-sdk/platforms/android-4 && \
    wget -O /opt/android-sdk/platforms/android-4/zip.zip https://dl.google.com/android/repository/android-1.6_r03-linux.zip && \
    mkdir -p /opt/android-sdk/platforms/android-5 && \
    wget -O /opt/android-sdk/platforms/android-5/zip.zip https://dl.google.com/android/repository/android-2.0_r01-linux.zip && \
    mkdir -p /opt/android-sdk/platforms/android-6 && \
    wget -O /opt/android-sdk/platforms/android-6/zip.zip https://dl.google.com/android/repository/android-2.0.1_r01-linux.zip && \
    mkdir -p /opt/android-sdk/platforms/android-7 && \
    wget -O /opt/android-sdk/platforms/android-7/zip.zip https://dl.google.com/android/repository/android-2.1_r03.zip && \
    mkdir -p /opt/android-sdk/platforms/android-8 && \
    wget -O /opt/android-sdk/platforms/android-8/zip.zip https://dl.google.com/android/repository/android-2.2_r03.zip && \
    mkdir -p /opt/android-sdk/platforms/android-10 && \
    wget -O /opt/android-sdk/platforms/android-10/zip.zip https://dl.google.com/android/repository/android-2.3.3_r02.zip && \
    mkdir -p /opt/android-sdk/platforms/android-11 && \
    wget -O /opt/android-sdk/platforms/android-11/zip.zip https://dl.google.com/android/repository/android-3.0_r02.zip && \
    mkdir -p /opt/android-sdk/platforms/android-12 && \
    wget -O /opt/android-sdk/platforms/android-12/zip.zip https://dl.google.com/android/repository/android-3.1_r03.zip && \
    mkdir -p /opt/android-sdk/platforms/android-13 && \
    wget -O /opt/android-sdk/platforms/android-13/zip.zip https://dl.google.com/android/repository/android-3.2_r01.zip && \
    mkdir -p /opt/android-sdk/platforms/android-14 && \
    wget -O /opt/android-sdk/platforms/android-14/zip.zip https://dl.google.com/android/repository/android-14_r04.zip && \
    mkdir -p /opt/android-sdk/platforms/android-15 && \
    wget -O /opt/android-sdk/platforms/android-15/zip.zip https://dl.google.com/android/repository/android-15_r05.zip && \
    mkdir -p /opt/android-sdk/platforms/android-16 && \
    wget -O /opt/android-sdk/platforms/android-16/zip.zip https://dl.google.com/android/repository/android-16_r05.zip && \
    mkdir -p /opt/android-sdk/platforms/android-17 && \
    wget -O /opt/android-sdk/platforms/android-17/zip.zip https://dl.google.com/android/repository/android-17_r03.zip && \
    mkdir -p /opt/android-sdk/platforms/android-18 && \
    wget -O /opt/android-sdk/platforms/android-18/zip.zip https://dl.google.com/android/repository/android-18_r03.zip && \
    mkdir -p /opt/android-sdk/platforms/android-19 && \
    wget -O /opt/android-sdk/platforms/android-19/zip.zip https://dl.google.com/android/repository/android-19_r04.zip && \
    mkdir -p /opt/android-sdk/platforms/android-21 && \
    wget -O /opt/android-sdk/platforms/android-21/zip.zip https://dl.google.com/android/repository/android-21_r02.zip && \
    mkdir -p /opt/android-sdk/platforms/android-22 && \
    wget -O /opt/android-sdk/platforms/android-22/zip.zip https://dl.google.com/android/repository/android-22_r02.zip && \
    mkdir -p /opt/android-sdk/platforms/android-23 && \
    wget -O /opt/android-sdk/platforms/android-23/zip.zip https://dl.google.com/android/repository/platform-23_r03.zip && \
    mkdir -p /opt/android-sdk/platforms/android-24 && \
    wget -O /opt/android-sdk/platforms/android-24/zip.zip https://dl.google.com/android/repository/platform-24_r02.zip && \
    mkdir -p /opt/android-sdk/platforms/android-25 && \
    wget -O /opt/android-sdk/platforms/android-25/zip.zip https://dl.google.com/android/repository/platform-25_r03.zip && \
    mkdir -p /opt/android-sdk/platforms/android-26 && \
    wget -O /opt/android-sdk/platforms/android-26/zip.zip https://dl.google.com/android/repository/platform-26_r02.zip && \
    mkdir -p /opt/android-sdk/platforms/android-27 && \
    wget -O /opt/android-sdk/platforms/android-27/zip.zip https://dl.google.com/android/repository/platform-27_r03.zip && \
    mkdir -p /opt/android-sdk/platforms/android-28 && \
    wget -O /opt/android-sdk/platforms/android-28/zip.zip https://dl.google.com/android/repository/platform-28_r06.zip && \
    mkdir -p /opt/android-sdk/platforms/android-29 && \
    wget -O /opt/android-sdk/platforms/android-29/zip.zip https://dl.google.com/android/repository/platform-29_r05.zip && \
    mkdir -p /opt/android-sdk/platforms/android-20 && \
    wget -O /opt/android-sdk/platforms/android-20/zip.zip https://dl.google.com/android/repository/android-20_r02.zip && \
    mkdir -p /opt/android-sdk/platforms/android-30 && \
    wget -O /opt/android-sdk/platforms/android-30/zip.zip https://dl.google.com/android/repository/platform-30_r03.zip && \
    mkdir -p /opt/android-sdk/platforms/android-31 && \
    wget -O /opt/android-sdk/platforms/android-31/zip.zip https://dl.google.com/android/repository/platform-Sv2_r01.zip && \
    mkdir -p /opt/android-sdk/platforms/android-32 && \
    wget -O /opt/android-sdk/platforms/android-32/zip.zip https://dl.google.com/android/repository/platform-32_r01.zip && \
    mkdir -p /opt/android-sdk/platforms/android-33 && \
    wget -O /opt/android-sdk/platforms/android-33/zip.zip https://dl.google.com/android/repository/platform-TiramisuPrivacySandbox_r08.zip && \
    /usr/bin/find /opt/android-sdk/platforms/ -name '*.zip' -execdir bsdtar -x --strip-components=1 -f {} \;

ENV ANDROID_SDK_HOME=/opt/android-sdk
ENV DROIDSAFE_SRC_HOME=/workspace/droidsafe/
ENV CLASSPATH=".:/workspace/droidsafe/classes/main:/workspace/droidsafe/bin/*:/workspace/droidsafe/lib/asmutil.jar:/workspace/droidsafe/lib/slf4j-api-1.7.2.jar:/workspace/droidsafe/lib/logback-classic-1.0.7.jar:/workspace/droidsafe/lib/logback-core-1.0.7.jar:/workspace/droidsafe/lib/soot-2.5.0.jar"

RUN cd /workspace/droidsafe && sed -i '213i\\             encoding="UTF-8"' /workspace/droidsafe/build.xml && \
    ant -Dfile.encoding=UTF-8 compile

COPY run.sh /
