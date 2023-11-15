FROM ubuntu:22.04

# RUN sed -i -e "s/archive.ubuntu.com/old-releases.ubuntu.com/g" /etc/apt/sources.list

RUN apt-get update && apt-get install -y git time unzip wget

RUN mkdir /workspace
RUN git init /workspace/iccta && \
    cd /workspace/iccta && \
    git remote add origin https://github.com/lilicoding/soot-infoflow-android-iccta.git && \
    git fetch --depth=1 origin 831afaaf7b4320a11f9453afb3d02cf41cfa6b69 && \
    git reset --hard FETCH_HEAD

RUN apt-get update && apt-get install -y openjdk-8-jdk mysql-server sdkmanager

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


#RUN mysqld & sleep 3 && \
RUN sed -i '211s/);/)ENGINE=InnoDB  CHARACTER SET utf8;/' /workspace/iccta/res/schema
#    mysql -e 'CREATE DATABASE cc' && \
#    mysql cc < /workspace/iccta/res/schema && \
#    mysql -e "CREATE USER 'icc_ta_user' IDENTIFIED BY 'P@ssw0rd';" && \
#    mysql -e "GRANT ALL PRIVILEGES ON cc.* TO 'icc_ta_user';"

RUN sed -i 's/<name>.*<\/name>/<name>cc<\/name>/' /workspace/iccta/res/jdbc.xml && \
    sed -i 's/<username>.*<\/username>/<username>icc_ta_user<\/username>/' /workspace/iccta/res/jdbc.xml && \
    sed -i 's/<password>.*<\/password>/<password>P@ssw0rd<\/password>/' /workspace/iccta/res/jdbc.xml && \
    sed -i 's/<name>.*<\/name>/<name>cc<\/name>/' /workspace/iccta/release/res/jdbc.xml && \
    sed -i 's/<username>.*<\/username>/<username>icc_ta_user<\/username>/' /workspace/iccta/release/res/jdbc.xml && \
    sed -i 's/<password>.*<\/password>/<password>P@ssw0rd<\/password>/' /workspace/iccta/release/res/jdbc.xml && \
    sed -i 's/android_jars=.*/android_jars=\/opt\/android-sdk\/platforms/' /workspace/iccta/release/res/iccta.properties

RUN cd /workspace && \
    echo 'user=icc_ta_user' > cc.properties && \
    echo 'password=P@ssw0rd' >> cc.properties && \
    echo 'characterEncoding=ISO-8859-1' >> cc.properties && \
    echo 'useUnicode=true' >> cc.properties && \
    wget https://github.com/JordanSamhi/Tools/raw/master/ic3.jar

RUN cd /workspace/iccta && \
    wget https://github.com/JordanSamhi/Tools/raw/master/iccta.jar

# JarRsrcLoader is broken in singularity for some reason, so let's get rid of the jar stuff
RUN mkdir /workspace/iccta/unzipped && \
    unzip /workspace/iccta/iccta.jar -d /workspace/iccta/unzipped


COPY run.sh /
