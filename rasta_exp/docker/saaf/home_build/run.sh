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

export _JAVA_OPTIONS=-Duser.home=/mnt

cd /mnt
# copying saaf software in /mnt (30 MB) as it needs to run and write in its own directory
cp -Rf /workspace/saaf ./
cd saaf 
/usr/bin/time -o /mnt/report -q /usr/bin/timeout --kill-after=20s ${TIMEOUT} java ${JAVA_PARAM} -jar /mnt/saaf/dist/SAAF.jar -hl -log /mnt/log.txt -nodb -rprt /mnt/rprt /mnt/${APK_FILENAME} > /mnt/stdout 2> /mnt/stderr
