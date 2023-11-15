#!/bin/bash

set_name=$1


for set_num in `seq 0 9`; do
	set_name=set${set_num}
	utils/gen_tasks.sh ${set_name}
done
utils/gen_tasks.sh drebin
