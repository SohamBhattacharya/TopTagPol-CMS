#!/bin/bash

ARG1=$1

if [[ "$ARG1" != "9000" ]]; then
    echo "Exiting."
    exit
fi

for d in $(find /pnfs/desy.de/cms/tier2/store/user/sobhatta/TopTagPol/ntuples/ -mindepth 2 -maxdepth 2 | grep ZprimeToTT_M | grep 2022 | sort -V); do
echo gsiftp://dcache-cms-gridftp.desy.de:2811$d
gfal-rm -r gsiftp://dcache-cms-gridftp.desy.de:2811$d
done
