#!/usr/bin/env bash

APK_FILENAME=$1

export TIME="time: %e
kernel-cpu-time: %S
user-cpu-time: %U
max-rss-mem: %M
avg-rss-mem: %t
avg-total-mem: %K
page-size: %Z
nb-major-page-fault: %F
nb-minor-page-fault: %R
nb-fs-input: %I
nb-fs-output: %O
nb-socket-msg-received: %r
nb-socket-msg-sent: %s
nb-signal-delivered: %k
exit-status: %x"


#cd /mnt/
#cp /workspace/droidsafe/android-apps/Makefile_apk /mnt/Makefile
#basename=$(basename -s .apk ${APK_FILENAME})
#sed -i "s#^NAME := APPNAME#NAME := ${basename}#" /mnt/Makefile
#/usr/bin/time -o /mnt/report -q /usr/bin/timeout --kill-after=20s ${TIMEOUT} make -f /mnt/Makefile specdump-apk > /mnt/stdout 2> /mnt/stderr

export ANDROID_SDK_HOME=/opt/android-sdk/
export DROIDSAFE_SRC_HOME=/workspace/droidsafe/
# export DROIDSAFE_MEMORY=16


cd /mnt
/usr/bin/time -o /mnt/report -q /usr/bin/timeout --kill-after=20s ${TIMEOUT} sh -c "/workspace/droidsafe/bin/unpack-apk -f ${1} && /workspace/droidsafe/bin/droidsafe -approot /mnt -apkfile ${1} -t specdump" >> /mnt/stdout 2>> /mnt/stderr
