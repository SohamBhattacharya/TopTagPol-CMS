#!/bin/bash

ARG1=$1

if [[ "$ARG1" != "9000" ]]; then
    echo "Exiting."
    exit
fi

GFAL_PATH="gsiftp://dcache-cms-gridftp.desy.de:2811/pnfs/desy.de/cms/tier2/store/user/sobhatta/TopTagPol/ntuples"
GREP_STR="TTJets_HT"

for d in $(gfal-ls $GFAL_PATH | grep $GREP_STR | sort -V); do
    path="$GFAL_PATH/$d"
    echo "Deleting: "$path
    gfal-rm -r $path
done
