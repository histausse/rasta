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


cd /workspace/dare
mkdir -p /mnt/dare_out
mkdir -p /mnt/ic3_out

# Expand Java Params: -Xmx16g -Xss16g ===> -x -Xmx16g -x -Xss16g
DARE_JAVA_PARAM=`echo "${JAVA_PARAM}" | sed "s/-X/-x -X/g"`

#./dare -d /mnt/dare_out $@ /mnt/app.apk && echo 'DARE FINISHED' || echo 'DARE FAILED'
echo "Doing: ./dare -d /mnt/dare_out ${DARE_JAVA_PARAM} /mnt/${APK_FILENAME}"

# Monitoring time of DARE (but time measurement will be lost)
/usr/bin/time -o /mnt/report -q /usr/bin/timeout --kill-after=20s ${TIMEOUT} ./dare -d /mnt/dare_out ${DARE_JAVA_PARAM} /mnt/${APK_FILENAME} > /mnt/stdout 2> /mnt/stderr

echo 'DARE FINISHED'

#java "${newargs[@]}" -jar /workspace/ic3/target/ic3-0.2.0-full.jar -protobuf /mnt/ic3_out -apkormanifest /mnt/app.apk -input /mnt/dare_out/retargeted/app/ -cp /workspace/ic3/src/main/resources/android.jar -out /mnt/ic3_out

HASH=`echo ${APK_FILENAME} | cut -d '.' -f '1'`

echo "Doing: java ${JAVA_PARAM} -jar /workspace/ic3/target/ic3-0.2.0-full.jar -protobuf /mnt/ic3_out -apkormanifest /mnt/${APK_FILENAME} -input /mnt/dare_out/retargeted/${HASH}/ -cp /workspace/ic3/src/main/resources/android.jar -out /mnt/ic3_out"

# Monitoring time of IC3
/usr/bin/time -o /mnt/report -q /usr/bin/timeout --kill-after=20s ${TIMEOUT}  java ${JAVA_PARAM} -jar /workspace/ic3/target/ic3-0.2.0-full.jar -protobuf /mnt/ic3_out -apkormanifest /mnt/${APK_FILENAME} -input /mnt/dare_out/retargeted/${HASH}/ -cp /workspace/ic3/src/main/resources/android.jar -out /mnt/ic3_out >> /mnt/stdout 2>> /mnt/stderr

echo "IC3 finished"
