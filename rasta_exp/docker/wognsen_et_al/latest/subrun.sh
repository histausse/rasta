#!/usr/bin/env bash

APK_FILENAME=$1

cd /mnt

# Patch for defining user.home for java commands (apktool uses the home dir)
# https://stackoverflow.com/questions/1501235/change-user-home-system-property
export _JAVA_OPTIONS=-Duser.home=/mnt

apktool d ${APK_FILENAME} > /mnt/stdout 2> /mnt/stderr

HASH=`echo ${APK_FILENAME} | cut -d '.' -f '1'`

# Fix misshandling of escaped quote in generator.py
find ${HASH} -name '*.smali' -exec sed -i "s#\\\'#BACKSLASH-SINGLEQ#g" {} \;

python2.7 /workspace/dalvik-bytecode-analysis-tool/prolog/generator.py ./${HASH}/

xsb -S --noprompt -e "['out.pl'], printMethodCalls, printStats, halt."
