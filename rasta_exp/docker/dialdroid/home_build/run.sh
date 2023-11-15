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

export CLASS_PATH='/workspace/dialdroid_bin::/workspace/dialdroid_bin/infoflow-android-dialdroid.jar:/workspace/dialdroid_bin/infoflow-dialdroid.jar:/workspace/dialdroid_bin/soot-dialdroid.jar:/workspace/dialdroid_bin/ic3-dialdroid-classes.jar:/workspace/dialdroid_bin/axml-2.0.0.jar:/workspace/dialdroid_bin/coal-0.1.7.jar:/workspace/dialdroid_bin/coal-strings-0.1.2.jar:/workspace/dialdroid_bin/commons-cli-1.3.1.jar:/workspace/dialdroid_bin/jsch-0.1.51.jar:/workspace/dialdroid_bin/log4j-1.2.17.jar:/workspace/dialdroid_bin/mysql-connector-java-5.1.31.jar:/workspace/dialdroid_bin/protobuf-java-2.5.0.jar:/workspace/dialdroid_bin/slf4j-api-1.7.7.jar:/workspace/dialdroid_bin/slf4j-log4j12-1.7.13.jar:/workspace/dialdroid_bin/herosclasses-trunk.jar:/workspace/dialdroid_bin/soot-dialdroid.jar:/workspace/dialdroid_bin/infoflow-android-dialdroid.jar:/workspace/dialdroid_bin/infoflow-dialdroid.jar'


# Create and run database as current user on specific file
#SQL_DATA=`mktemp -d`
#
SQL_DATA=/mnt/mysql
LOG_FILE="$SQL_DATA/log"
mkdir $SQL_DATA
chmod 777 $SQL_DATA
chmod +x $SQL_DATA/..
mysqld --datadir=$SQL_DATA --log-error=$LOG_FILE --default-time-zone='+00:00' --initialize-insecure
#mysqld --datadir=$SQL_DATA --skip-name-resolve --log-error=$LOG_FILE --default-time-zone='+00:00' --bind-address=127.0.0.1 --mysqlx=OFF --socket=$SQL_DATA/mysqld.sock &
mysqld --datadir=$SQL_DATA --skip-name-resolve --log-error=$LOG_FILE --default-time-zone='+00:00' --bind-address=127.0.0.1 --pid-file=/mnt/mysql/pid.pid --socket=$SQL_DATA/mysqld.sock &
DB_PID="$!"

# Wait for connection
until mysql -u root --socket="$SQL_DATA/mysqld.sock" -e 'CREATE DATABASE dialdroid_test'
do 
    echo 'Waiting for DB, error 2002 ^ is normal'
    sleep 1
done
mysql -u root --socket="$SQL_DATA/mysqld.sock" dialdroid_test < /workspace/dialdroid_db/DIALDroid.sql
mysql -u root --socket="$SQL_DATA/mysqld.sock" -e "CREATE USER 'root' IDENTIFIED BY 'Nice2Hear';"
mysql -u root --socket="$SQL_DATA/mysqld.sock" -e "GRANT ALL PRIVILEGES ON dialdroid_test.* TO 'root';"

cd /mnt

ln -s /workspace/dialdroid/build/cc.properties .
ln -s /workspace/dialdroid/build/AndroidCallbacks.txt .
ln -s /workspace/dialdroid/build/EasyTaintWrapperSource.txt .
ln -s /workspace/dialdroid/build/ic3-android.jar .

#/usr/bin/time -o /mnt/report -q /usr/bin/timeout --kill-after=20s ${TIMEOUT} java ${JAVA_PARAM} -jar /workspace/dialdroid/build/dialdroid.jar appanalysis /workspace/platforms/ dialdroid_test 127.0.0.1 /mnt/${APK_FILENAME} SOCIAL > /mnt/stdout 2> /mnt/stderr

/usr/bin/time -o /mnt/report -q /usr/bin/timeout --kill-after=20s ${TIMEOUT} java ${JAVA_PARAM} -cp ${CLASS_PATH} com.yaogroup.collusion.AppAnalysis appanalysis /workspace/platforms/ dialdroid_test 127.0.0.1 /mnt/${APK_FILENAME} SOCIAL > /mnt/stdout 2> /mnt/stderr


kill -9 ${DB_PID}
