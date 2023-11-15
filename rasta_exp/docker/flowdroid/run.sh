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


/usr/bin/time -o /mnt/report -q /usr/bin/timeout --kill-after=20s ${TIMEOUT} java ${JAVA_PARAM} -jar ${JAR_FILE} -a /mnt/${APK_FILENAME} -p /opt/android-sdk/platforms/ -s soot-infoflow-android/SourcesAndSinks.txt --mergedexfiles > /mnt/stdout 2> /mnt/stderr
