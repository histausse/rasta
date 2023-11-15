#!/bin/bash

set_name=$1

parallel echo {1}_-_{2} :::: dataset/${set_name} tools  > ${set_name}_all
