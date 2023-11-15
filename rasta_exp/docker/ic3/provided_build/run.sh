#!/bin/bash

cd /workspace/dare
mkdir -p /mnt/dare_out
mkdir -p /mnt/ic3_out

./dare -d /mnt/dare_out $@ /mnt/app.apk && echo 'DARE FINISHED' || echo 'DARE FAILED'

echo 'DARE FINISHED' 1>&2

newargs=( "$@" )
# Filter out '-x' from args
for index in "${!newargs[@]}" ; do
    [[ ${newargs[$index]} = '-x' ]] && unset -v 'newargs[$index]' ;
done

java "${newargs[@]}" -jar /workspace/ic3_bin/ic3-0.2.0-full.jar -protobuf /mnt/ic3_out -apkormanifest /mnt/app.apk -input /mnt/dare_out/retargeted/app/ -cp /workspace/ic3/src/main/resources/android.jar -out /mnt/ic3_out
