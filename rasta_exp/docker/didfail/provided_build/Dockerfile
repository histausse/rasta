FROM ubuntu:12.04

RUN sed -i -e "s/archive.ubuntu.com/old-releases.ubuntu.com/g" /etc/apt/sources.list

RUN apt-get update && apt-get install -y git time

RUN mkdir -p /workspace/didfail

RUN apt-get update && \
    apt-get install -y wget unzip bzip2 && \
    apt-get install -y openjdk-7-jdk openjdk-7-jre-headless && \
    apt-get remove -y openjdk-6-jre openjdk-6-jre-headless && \
    apt-get install -y gcc-4.6-multilib && \
    apt-get install -y lib32stdc++6 && \
    apt-get install -y zlib1g-dev:i386

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

RUN cd /workspace/didfail && \
    wget -nc http://www.cs.cmu.edu/~wklieber/didfail/epicc-0.1.tgz && \
    wget -nc https://github.com/dare-android/platform_dalvik/releases/download/dare-1.1.0/dare-1.1.0-linux.tgz && \
    wget -nc http://www.cs.cmu.edu/~wklieber/didfail/platform-16.zip && \
    wget -nc http://www.cs.cmu.edu/~wklieber/didfail/platform-19.zip && \
    wget -nc http://www.cs.cmu.edu/~wklieber/didfail/toyapps-2014-04-28.zip && \
    mkdir epicc && \
    tar xzf epicc-0.1.tgz -C epicc && \
    tar xzf dare-1.1.0-linux.tgz && \
    unzip platform-16.zip && \
    unzip platform-19.zip && \
    unzip -q toyapps-2014-04-28.zip && \
    wget -nc http://www.cs.cmu.edu/~wklieber/didfail/didfail.zip && \
    unzip -q -d /workspace/didfail/cert didfail.zip && \
    cp cert/paths.distrib.sh cert/paths.local.sh && \
    sed -i 's/export didfail=.*/export didfail=\/workspace\/didfail/' /workspace/didfail/cert/paths.local.sh && \
    sed -i 's/export sdk_platforms=.*/export sdk_platforms=\/opt\/android-sdk\/platforms/' /workspace/didfail/cert/paths.local.sh && \
    sed -i 's/export wkspc=.*/export wkspc=\/workspace/' /workspace/didfail/cert/paths.local.sh && \
    sed -i 's/export soot_base=.*/export soot_base=\/workspace/' /workspace/didfail/cert/paths.local.sh && \
    sed -i 's/export jvm_flags=.*/# export jvm_flags="-Xmx16g -Xss16g"/' /workspace/didfail/cert/paths.local.sh && \
    sed -i 's/export max_mem=.*/# export max_mem=17179869184/' /workspace/didfail/cert/paths.local.sh && \
    sed -i 's/export max_time=.*/# export max_time=4200/' /workspace/didfail/cert/paths.local.sh && \
    wget -nc http://www.cs.cmu.edu/~wklieber/didfail/workspace.tar.bz2 && \
    tar xjf workspace.tar.bz2 -C /workspace

#    sed -i 's/export jvm_flags=.*/export jvm_flags="-Xmx16g -Xss16g"/' /workspace/didfail/cert/paths.local.sh && \
#    sed -i 's/export max_mem=.*/export max_mem=17179869184/' /workspace/didfail/cert/paths.local.sh && \
#    sed -i 's/export max_time=.*/export max_time=4200/' /workspace/didfail/cert/paths.local.sh && \

COPY run.sh /workspace/run.sh
