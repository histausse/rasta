#!/usr/bin/env bash

# params: TIMEOUT APK_FILENAME

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


/usr/bin/time -o /mnt/report -q /usr/bin/timeout --kill-after=20s ${TIMEOUT} ruby /workspace/redexer/scripts/cmd.rb /mnt/${APK_FILENAME} --cmd logging --outputdir /mnt/ --to /mnt/new.apk > /mnt/stdout 2> /mnt/stderr
