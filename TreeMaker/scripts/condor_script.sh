#!/bin/sh

DIR=@dir@
PROXY=@proxy@

echo "Working directory: "$DIR
cd $DIR
echo "Moved to working directory."

#export SCRAM_ARCH=slc7_amd64_gcc820
export CPATH=$CPATH:$DIR
export ROOT_INCLUDE_PATH=$ROOT_INCLUDE_PATH:$DIR

source /cvmfs/grid.desy.de/etc/profile.d/grid-ui-env.sh
#source /cvmfs/cms.cern.ch/crab3/crab.sh

# Proxy path must be common to all nodes
# Default path is /tmp/, but thatis not common for all nodes
export X509_USER_PROXY=$PROXY

source /cvmfs/cms.cern.ch/cmsset_default.sh

#eval cmsenv
eval `scramv1 runtime -sh`

echo -n "HOSTNAME: "
hostname
echo -n "CMSOS: "
cmsos
echo -n "CMSARCH: "
cmsarch
echo -n "SCRAM_ARCH: "
echo $SCRAM_ARCH
echo -n "LD_LIBRARY_PATH: "
echo $LD_LIBRARY_PATH

#echo "Creating voms-proxy..."
#eval vpxy
echo "Proxy info:"
voms-proxy-info -all
echo ""

@cmd@
