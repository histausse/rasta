FROM ubuntu:12.04

RUN sed -i -e "s/archive.ubuntu.com/old-releases.ubuntu.com/g" /etc/apt/sources.list

RUN apt-get update && apt-get install -y git time

RUN mkdir -p /workspace/didfail

RUN apt-get update && \
    apt-get install -y wget unzip make ant && \
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

# Build jasmin
RUN cd /workspace && \
    wget https://github.com/Sable/jasmin/archive/79c79f314297e28037cfa91fa9316325e3a515bb.zip && \
    unzip 79c79f314297e28037cfa91fa9316325e3a515bb.zip && \
    rm 79c79f314297e28037cfa91fa9316325e3a515bb.zip && \
    mv jasmin-79c79f314297e28037cfa91fa9316325e3a515bb/ jasmin && \
    cd jasmin && cp ant.settings.template ant.settings && \
    sed -i 's/java_cup.jar=.*/java_cup.jar=libs\/java_cup.jar/' ant.settings && \
    ant jasmin-jar

# Build hero
RUN cd /workspace && \
    wget https://github.com/Sable/heros/archive/5b8180ebf9ba0eb869579425a7adb3d967da8c61.zip && \
    unzip 5b8180ebf9ba0eb869579425a7adb3d967da8c61.zip && \
    rm 5b8180ebf9ba0eb869579425a7adb3d967da8c61.zip && \
    mv heros-5b8180ebf9ba0eb869579425a7adb3d967da8c61/ heros && \
    cd heros && cp ant.settings.template ant.settings && \
    echo '' >> ant.settings && echo 'slf4j-api.jar=slf4j-api-1.7.5.jar' >> ant.settings && \
    echo 'slf4j-simple.jar=slf4j-simple-1.7.5.jar' >> ant.settings && \
    ant jar && \
    cp -r build/classes bin

# Build soot
RUN cd /workspace && \
    wget https://github.com/soot-oss/soot/archive/b4e51615db0effbb2ddc847035664b45756f4f82.zip && \
    unzip b4e51615db0effbb2ddc847035664b45756f4f82.zip && \
    rm b4e51615db0effbb2ddc847035664b45756f4f82.zip && \
    mv soot-b4e51615db0effbb2ddc847035664b45756f4f82/ soot && \
    cd soot && cp ant.settings.template ant.settings && mkdir -p ../JastAddExtensions/SootJastAddJ && \
    sed -i 's/jasmin.jar=..\/libs\/jasminclasses-custom.jar/jasmin.jar=..\/jasmin\/lib\/jasminclasses-2.2.1.jar/' ant.settings && \
    sed -i 's/javacup.jar=..\/libs\/java_cup.jar/javacup.jar=libs\/java_cup.jar/' ant.settings && \
    ant fulljar

# Commit specific for nov 2014
RUN cd /workspace && \
    wget https://bitbucket.org/wsnavely/soot-infoflow-latest/get/3ff51b5fb9f551aef0b3598585f83fe334c0b99b.tar.gz && \
    tar -xvzf 3ff51b5fb9f551aef0b3598585f83fe334c0b99b.tar.gz && \
    mv wsnavely-soot-infoflow-latest-3ff51b5fb9f5 soot-infoflow && \
    cd soot-infoflow && mv ant.settings.jenkins ant.settings && \
    sed -i 's/soot.jar=.*/soot.jar=..\/soot\/lib\/soot-trunk.jar/' ant.settings && \
    ant jar && \
    cp -r build/classes bin

# Commit specific for nov 2014
RUN cd /workspace && \
    wget https://bitbucket.org/wsnavely/soot-infoflow-android-latest/get/31620d664220dfa86de4b5fcc876e866eb41979f.tar.gz && \
    tar -xvzf 31620d664220dfa86de4b5fcc876e866eb41979f.tar.gz && rm 31620d664220dfa86de4b5fcc876e866eb41979f.tar.gz && \
    mv wsnavely-soot-infoflow-android-latest-31620d664220 soot-infoflow-android && \
    cd soot-infoflow-android && mv ant.settings.jenkins ant.settings && \
    sed -i 's/soot.jar=.*/soot.jar=..\/soot\/lib\/soot-trunk.jar/' ant.settings && \
    sed -i 's/infoflow.jar=.*/infoflow.jar=..\/soot-infoflow\/build\/jar\/soot-infoflow.jar/' ant.settings && \
    ant jar && \
    cp -r build/classes bin

SHELL ["/bin/bash", "-c"]
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
    wget -O didfail.zip https://bitbucket.org/wklieber/didfail/get/99bc1187c822b216fca81237c16225d7540d80dd.zip && \
    unzip didfail.zip -d cert && \
    mv cert/*/* cert/ && \
    cp cert/paths.distrib.sh cert/paths.local.sh && \
    sed -i 's/export didfail=.*/export didfail=\/workspace\/didfail/' /workspace/didfail/cert/paths.local.sh && \
    sed -i 's/export sdk_platforms=.*/export sdk_platforms=\/opt\/android-sdk\/platforms/' /workspace/didfail/cert/paths.local.sh && \
    sed -i 's/export wkspc=.*/export wkspc=\/workspace/' /workspace/didfail/cert/paths.local.sh && \
    sed -i 's/export soot_base=.*/export soot_base=\/workspace/' /workspace/didfail/cert/paths.local.sh && \
    sed -i 's/export jvm_flags=.*/# export jvm_flags="-Xmx16g -Xss16g"/' /workspace/didfail/cert/paths.local.sh && \
    sed -i 's/export max_mem=.*/# export max_mem=17179869184/' /workspace/didfail/cert/paths.local.sh && \
    sed -i 's/export max_time=.*/# export max_time=4200/' /workspace/didfail/cert/paths.local.sh && \
    source /workspace/didfail/cert/paths.local.sh; \
    cd /workspace/didfail/cert/transformApk && make 


#    sed -i 's/export jvm_flags=.*/export jvm_flags="-Xmx16g -Xss16g"/' /workspace/didfail/cert/paths.local.sh && \
#    sed -i 's/export max_mem=.*/export max_mem=17179869184/' /workspace/didfail/cert/paths.local.sh && \
#    sed -i 's/export max_time=.*/export max_time=4200/' /workspace/didfail/cert/paths.local.sh && \

COPY run.sh /
