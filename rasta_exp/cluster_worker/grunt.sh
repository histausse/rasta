#!/bin/bash


while /bin/true
do
    python3 grunt-worker.py --no-mark-done --overwrite --singularity --image-basedir ~/sif
    if [[ z"$?" == z111 ]]
    then
	    break
    fi
    sleep 10
done
