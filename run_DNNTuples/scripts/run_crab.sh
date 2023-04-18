#!/bin/bash

# File with sample list
INPUT=$1

# v<N>
VERSION=$2

if [ -z "$INPUT" ]; then
    echo "Missing input argument."
    exit 1
fi

if [ -z "$VERSION" ]; then
    echo "Missing version argument."
    exit 1
fi


source /cvmfs/cms.cern.ch/common/crab-setup.sh

python DeepNTuples/Ntupler/run/crab.py \
-p DeepNTuples/Ntupler/test/DeepNtuplizerAK8.py \
--site T2_DE_DESY \
-o /store/user/$USER/TopTagPol/DeepNtuples/$VERSION \
-t DeepNtuplesAK8-$VERSION \
-i $INPUT \
--set-input-dataset \
-s FileBased \
-n 5 \
--max-memory 2500 \
--max-runtime-min 2750 \
--work-area crab_projects_$VERSION \
#--send-external \
#--dryrun
