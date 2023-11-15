#!/usr/bin/env bash

DATA_DIR=$1
if [[ -z "${DATA_DIR}" ]]; then
    echo 'MISSING DATA_DIR parameter'
    echo 'usage:  ./extract_result.sh DATA_DIR'
    exit 1
fi
DATA_DIR="$(readlink -f "$DATA_DIR")"

DB="${DATA_DIR}/results/rasta.db"
DB_DREBIN="${DATA_DIR}/results/drebin.db"
FOLDER="figs"

rasta-status -d ${DB} -f ${FOLDER} --title "Exit status for the Rasta dataset"
rasta-status -d ${DB_DREBIN} -f ${FOLDER} --title "Exit status for the Drebin dataset"
rasta-success-year -d ${DB} -f "${FOLDER}/by_year"

rasta-common-errors -d ${DB} -f "${FOLDER}/common_err" -s FAILED
rasta-avg-nb-errors -d ${DB} -f "${FOLDER}/common_err"
rasta-error-repartition -d ${DB} -f "${FOLDER}"
rasta-avg-ressource -d ${DB} -f "${FOLDER}"

rasta-decorelate-factor -d ${DB} -f "${FOLDER}/decorelation" --decile 8
rasta-decorelate-factor -d ${DB} -f "${FOLDER}/decorelation" --decile 6
