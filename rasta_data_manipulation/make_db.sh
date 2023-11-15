#!/usr/bin/env bash

DATA_DIR=$1
if [[ -z "${DATA_DIR}" ]]; then
    echo 'MISSING DATA_DIR parameter'
    echo 'usage:  ./make_db.sh DATA_DIR'
    exit 1
fi
DATA_DIR="$(readlink -f "$DATA_DIR")"


all_rasta_apk=$(mktemp)
cat ${DATA_DIR}/dataset/set* > ${all_rasta_apk}
rasta-populate-db-apk -a ${all_rasta_apk} \
    -d "${DATA_DIR}/results/rasta.db" \
    --year-and-sdk "${DATA_DIR}/androzoo/year_and_sdk.csv.gz" \
    --latest-with-added-date "${DATA_DIR}/androzoo/latest_with-added-date.csv.gz" \
    --fix-dex-file
rasta-populate-db-tool -d "${DATA_DIR}/results/rasta.db"
report_folders="status_set0 status_set1 status_set2 status_set3 status_set4 status_set5 status_set6 status_set7 status_set8 status_set9"
for folder in ${report_folders}; do
    rasta-populate-db-report -d "${DATA_DIR}/results/rasta.db" -r "${DATA_DIR}/results/reports/rasta/${folder}"
done
rasta-populate-db-report -d "${DATA_DIR}/results/rasta.db" --estimate-cause

rasta-populate-db-apk -a "${DATA_DIR}/dataset/drebin" \
    -d "${DATA_DIR}/results/drebin.db" \
    --year-and-sdk "${DATA_DIR}/androzoo/year_and_sdk.csv.gz" \
    --latest-with-added-date "${DATA_DIR}/androzoo/latest_with-added-date.csv.gz" \
    --fix-dex-file
rasta-populate-db-tool -d "${DATA_DIR}/results/drebin.db"
rasta-populate-db-report -d "${DATA_DIR}/results/drebin.db" -r "${DATA_DIR}/results/reports/drebin/status_drebin"
rasta-populate-db-report -d "${DATA_DIR}/results/drebin.db" --estimate-cause

rm ${all_rasta_apk}
