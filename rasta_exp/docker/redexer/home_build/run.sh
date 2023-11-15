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

# Going into the mount point
cd /mnt

# Patch for defining user.home for java commands (apktool uses the home dir)
# https://stackoverflow.com/questions/1501235/change-user-home-system-property
export _JAVA_OPTIONS=-Duser.home=/mnt

ln -s /workspace/redexer/data .
/usr/bin/time -o /mnt/report -q /usr/bin/timeout --kill-after=20s ${TIMEOUT} ruby /workspace/redexer/scripts/cmd.rb /mnt/${APK_FILENAME} --cmd logging --outputdir /mnt/ --to /mnt/new.apk > /mnt/stdout 2> /mnt/stderr
