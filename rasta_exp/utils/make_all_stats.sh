#!/bin/bash

utils/get_status_stats.py drebin > drebin_stats
seq 0 9 | parallel -j10 'utils/get_status_stats.py set{} > set{}_stats'
