#!/bin/bash

exit

#DCACHEDIR="/pnfs/desy.de/cms/tier2/store/user/sobhatta/TopTagPol/ntuples"
#GFALPATH="gsiftp://dcache-cms-gridftp.desy.de:2811/pnfs/desy.de/cms/tier2/store/user/sobhatta/TopTagPol/ntuples"
#
#for dir in $(ls $DCACHEDIR | |grep "MINIAOSIM_" | sort -V); do
#    
#    printf "\n********************\n"
#    
#    SAMPLENAME=$(echo $dir | awk -F '_2021' '{print $1}')
#    SAMPLEDATE=$(echo $dir | awk -F 'MINIAODSIM_' '{print $2}')
#    SRC="$GFALPATH/$dir"
#    DST="$GFALPATH/$SAMPLENAME/$SAMPLEDATE"
#    #DST_OLDNAME="$DST/$dir"
#    #DST_NEWNAME="$DST/$SAMPLENAME/$SAMPLEDATE"
#    echo $dir
#    echo $SRC
#    echo $DST
#    echo $DST_OLDNAME
#    echo $DST_NEWNAME
#    echo ""
#    
#    (gfal-mkdir -p $DST) && \
#    (gfal-copy -r -f $SRC "$DST/") && \
#    (gfal-rm -r $SRC)
#    
#    printf "********************\n"
#    
#done
