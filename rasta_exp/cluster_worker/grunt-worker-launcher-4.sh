#!/bin/bash -l


module load tools/Singularity
module load lang/Python/3.8.6-GCCcore-10.2.0

source ../venvrasta/bin/activate

seq 4 | parallel --jobs 4 ./grunt.sh

#while /bin/true
#do
#    python3 grunt-worker.py --no-mark-done --overwrite --singularity --image-basedir ~/sif
#    if [[ z"$?" == z111 ]]
#    then
#	    break
#    fi
#    sleep 10
#done
