#!/usr/bin/env bash


APK_FILENAME=$1
ANDROID_JARS='/opt/android-sdk/platforms/android-10/android.jar:/opt/android-sdk/platforms/android-11/android.jar:/opt/android-sdk/platforms/android-12/android.jar:/opt/android-sdk/platforms/android-13/android.jar:/opt/android-sdk/platforms/android-14/android.jar:/opt/android-sdk/platforms/android-15/android.jar:/opt/android-sdk/platforms/android-3/android.jar:/opt/android-sdk/platforms/android-16/android.jar:/opt/android-sdk/platforms/android-17/android.jar:/opt/android-sdk/platforms/android-18/android.jar:/opt/android-sdk/platforms/android-19/android.jar:/opt/android-sdk/platforms/android-20/android.jar:/opt/android-sdk/platforms/android-4/android.jar:/opt/android-sdk/platforms/android-21/android.jar:/opt/android-sdk/platforms/android-5/android.jar:/opt/android-sdk/platforms/android-22/android.jar:/opt/android-sdk/platforms/android-6/android.jar:/opt/android-sdk/platforms/android-23/android.jar:/opt/android-sdk/platforms/android-7/android.jar:/opt/android-sdk/platforms/android-8/android.jar'

cd /mnt
d2j-dex2jar.sh ${APK_FILENAME}

JAR_FILENAME=$(echo ${APK_FILENAME} | sed 's/.apk/-dex2jar.jar/')
mkdir /mnt/classes
mv "/mnt/$JAR_FILENAME" /mnt/classes
cd /mnt/classes
unzip ${JAR_FILENAME}
rm ${JAR_FILENAME}

echo -e '1\ny\n/mnt/classes/' | java ${JAVA_PARAM} -cp "/workspace/perfchecker.jar:/workspace/soot-2.5.0.jar:${ANDROID_JARS}:/mnt/classes" androidPerf.CheckerMain
