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

JAR_FILENAME=$(echo ${APK_FILENAME} | sed 's/.apk/-dex2jar.jar/')

cd /mnt
#/usr/bin/time -o /mnt/report -q /usr/bin/timeout --kill-after=20s ${TIMEOUT} 
sh -c "d2j-dex2jar.sh ${APK_FILENAME} && /workspace/hopper/hopper.sh -app ${JAR_FILENAME} -droidel_home /workspace/droidel -android_jar /workspace/hopper/lib/droidel_android-4.4.2.jar -check_android_leaks"
#> /mnt/stdout 2> /mnt/stderr
