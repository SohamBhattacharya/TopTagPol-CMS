#!/bin/bash

CMSSWREL=CMSSW_10_6_30

mkdir -p envs
cd envs

if [ -d "$CMSSWREL" ]; then
    echo "$CMSSWREL already exists."
    exit 1
fi

cmsrel $CMSSWREL
cd $CMSSWREL/src
cmsenv

#ln -s ../../../BTagHelpers     .
#ln -s ../../../FatJetHelpers   .
#ln -s ../../../NtupleCommons   .
#ln -s ../../../Ntupler         .

ln -s ../../../DNNTuples DeepNTuples

scram b -j8
