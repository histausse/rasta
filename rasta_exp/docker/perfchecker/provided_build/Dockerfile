FROM ubuntu:14.04

RUN apt-get update && apt-get install -y time wget unzip openjdk-7-jdk

RUN mkdir /workspace

COPY perfchecker.jar /workspace/
COPY soot-2.5.0.jar /workspace/
COPY checksums.sha256 /workspace/

# Check that the provided perfchecker.jar and soot-2.5.0.jar are the same as the one
# we got
RUN cd /workspace && sha256sum -c checksums.sha256

# Get android.jar s. Note: we don't download android.jar s for version >= 24 because it uses version 52.0 of java bytecode, not supported by java 7
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
    mkdir -p /opt/android-sdk/platforms/android-20 && \
    wget -O /opt/android-sdk/platforms/android-20/zip.zip https://dl.google.com/android/repository/android-20_r02.zip && \
    /usr/bin/find /opt/android-sdk/platforms/ -name '*.zip' -execdir bsdtar -x --strip-components=1 -f {} \;

RUN cd /workspace/ && \
    wget http://downloads.sourceforge.net/project/dex2jar/dex2jar-2.0-20140818.061505-10.zip && \
    unzip dex2jar-2.0-20140818.061505-10.zip && rm dex2jar-2.0-20140818.061505-10.zip && \
    mv dex2jar-2.0-SNAPSHOT dex2jar && \
    chmod +x /workspace/dex2jar/*

ENV PATH="/workspace/dex2jar:$PATH"

COPY run.sh /
COPY subrun.sh /
