#!/usr/bin/env bash

SIF_DIR=$1
if [[ -z "${SIF_DIR}" ]]; then
    echo MISSING SIF_DIR parameter
    exit 1
fi

[[ -d "${SIF_DIR}" ]] || mkdir "${SIF_DIR}"

tools="androguard androguard_dad didfail adagio anadroid blueseal didfail flowdroid mallodroid redexer saaf wognsen_et_al iccta ic3 ic3_fork gator droidsafe apparecium amandroid dialdroid"

for tool in ${tools}; do
    curl -L -o "${SIF_DIR}/rasta-${tool}.sif" "https://zenodo.org/records/10980349/files/rasta-${tool}.sif?download=1"
done;
