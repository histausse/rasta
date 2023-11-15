#!/usr/bin/env bash

# DOCKER OR SINGULARITY ?
MODE=$1
TOOL_NAME=$2
CONTAINER_IMG=$3
WORKDIR=$4
TMP_DIR=$5
APK_FILENAME=$6

[[ -z "$MODE" ]] || [[ -z "$TOOL_NAME" ]] || [[ -z "$CONTAINER_IMG" ]] || [[ -z "$WORKDIR" ]] || [[ -z "$TMP_DIR" ]] || [[ -z "$APK_FILENAME" ]] && (echo MISSING parameters; exit 1)

ENV_FILE="./envs/${TOOL_NAME}.env"
if [[ -e "./envs/${TOOL_NAME}_medium.env"  ]]
then
	ENV_FILE=./envs/${TOOL_NAME}_medium.env
	echo USING medium ENV : $ENV_FILE
fi

#TODO Handle env files for docker/singularity: param   --env-file=
if [[ "DOCKER" == "$MODE" ]]; then
    # DOCKER
    docker run --read-only -it --env-file=${ENV_FILE} --tmpfs /run --tmpfs /tmp --mount type=bind,source=${WORKDIR},destination=/mnt --user=$(id -u):$(id -g) -t ${CONTAINER_IMG} /run.sh ${TIMEOUT} ${APK_FILENAME}
fi
if [[ "SINGULARITY" == "$MODE" ]]; then
    # SINGULARITY
    echo ${TMP_WORKDIR}
    singularity exec --net --network=none --no-home --cleanenv --env-file=${ENV_FILE} --bind ${WORKDIR}:/mnt --bind ${TMP_DIR}:/tmp -c ${CONTAINER_IMG}.sif /run.sh ${TIMEOUT} ${APK_FILENAME}
fi
