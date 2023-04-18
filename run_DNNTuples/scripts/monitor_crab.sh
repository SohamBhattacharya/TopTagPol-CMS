#!/bin/bash

DIR=$1

eval `scramv1 runtime -sh`

while true
do 
    python ./DeepNTuples/Ntupler/run/crab.py --work-area $DIR --status
    sleep 1800
done
