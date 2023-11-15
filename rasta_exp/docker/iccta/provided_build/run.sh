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

export CLASS_PATH='/workspace/iccta/unzipped:/workspace/iccta/unzipped/c3p0-0.9.1.2.jar:/workspace/iccta/unzipped/jdom-2.0.5.jar:/workspace/iccta/unzipped/AXMLPrinter2.jar:/workspace/iccta/unzipped/android.jar:/workspace/iccta/unzipped/junit.jar:/workspace/iccta/unzipped/commons-cli-1.2.jar:/workspace/iccta/unzipped/axml-2.0.jar:/workspace/iccta/unzipped/slf4j-api-1.7.5.jar:/workspace/iccta/unzipped/slf4j-simple-1.7.5.jar:/workspace/iccta/unzipped/guava-18.0.jar:/workspace/iccta/unzipped/dexlib2-2.1.0-dev.jar:/workspace/iccta/unzipped/asm-debug-all-5.0.3.jar:/workspace/iccta/unzipped/cglib-nodep-2.2.2.jar:/workspace/iccta/unzipped/cos.jar:/workspace/iccta/unzipped/hamcrest-all-1.3.jar:/workspace/iccta/unzipped/j2ee.jar:/workspace/iccta/unzipped/java_cup.jar:/workspace/iccta/unzipped/javassist-3.18.2-GA.jar:/workspace/iccta/unzipped/jboss-common-core-2.5.0.Final.jar:/workspace/iccta/unzipped/junit-4.11.jar:/workspace/iccta/unzipped/mockito-all-1.10.8.jar:/workspace/iccta/unzipped/mockito-all-1.9.5.jar:/workspace/iccta/unzipped/org.hamcrest.core_1.3.0.jar:/workspace/iccta/unzipped/polyglot.jar:/workspace/iccta/unzipped/powermock-mockito-1.6.1-full.jar:/workspace/iccta/unzipped/util-2.1.0-dev.jar:/workspace/iccta/unzipped/FlowDroid.jar:/workspace/iccta/unzipped/mysql-connector-java-8.0.18.jar'

# Create and run database as current user on specific file
#SQL_DATA=`mktemp -d`
#
SQL_DATA=/mnt/mysql
LOG_FILE="$SQL_DATA/log"
mkdir $SQL_DATA
chmod 777 $SQL_DATA
chmod +x $SQL_DATA/..
mysqld --datadir=$SQL_DATA --log-error=$LOG_FILE --default-time-zone='+00:00' --initialize-insecure
mysqld --datadir=$SQL_DATA --skip-name-resolve --log-error=$LOG_FILE --default-time-zone='+00:00' --bind-address=127.0.0.1 --mysqlx=OFF --socket=$SQL_DATA/mysqld.sock &
DB_PID="$!"

# Wait for db connection
until mysql -u root --socket="$SQL_DATA/mysqld.sock" -e 'CREATE DATABASE cc'
do
    echo 'Waiting for DB, error 2002 ^ is normal'
    sleep 1
done
mysql -u root --socket="$SQL_DATA/mysqld.sock" cc < /workspace/iccta/res/schema
mysql -u root --socket="$SQL_DATA/mysqld.sock" -e "CREATE USER 'icc_ta_user' IDENTIFIED BY 'P@ssw0rd';"
mysql -u root --socket="$SQL_DATA/mysqld.sock" -e "GRANT ALL PRIVILEGES ON cc.* TO 'icc_ta_user';"

cd /mnt
ln -s /workspace/iccta/res /mnt/
ln -s /workspace/iccta/libs /mnt/
ln -s /workspace/iccta/iccProvider /mnt/
ln -s /workspace/iccta/release /mnt/
ln -s /workspace/iccta/AndroidCallbacks.txt /mnt/

#java ${JAVA_PARAM} -jar /workspace/ic3.jar -a /mnt/${APK_FILENAME} -cp /opt/android-sdk/platforms -db /workspace/cc.properties
# Normal command
#echo "java ${JAVA_PARAM} -jar /workspace/iccta/iccta.jar /mnt/${APK_FILENAME} /opt/android-sdk/platforms"
# Singularity because broken classloader for some reason
#echo "java -cp \$CLASS_PATH soot.jimple.infoflow.android.iccta.TestApps.Test /mnt/${APK_FILENAME} /opt/android-sdk/platforms"

/usr/bin/time -o /mnt/report -q /usr/bin/timeout --kill-after=20s ${TIMEOUT} sh -c "java ${JAVA_PARAM} -jar /workspace/ic3.jar -a /mnt/${APK_FILENAME} -cp /opt/android-sdk/platforms -db /workspace/cc.properties && java ${JAVA_PARAM} -cp ${CLASS_PATH} soot.jimple.infoflow.android.iccta.TestApps.Test /mnt/${APK_FILENAME} /opt/android-sdk/platforms" > /mnt/stdout 2> /mnt/stderr

kill -9 ${DB_PID}
