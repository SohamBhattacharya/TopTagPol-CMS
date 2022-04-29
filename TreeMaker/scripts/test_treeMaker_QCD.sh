#!/bin/bash

nohup cmsRun MyTools/EDAnalyzers/python/ConfFile_cfg.py \
outFileBaseName=ntupleTree_QCD \
sourceFile=sourceFiles/QCD_Pt_470to600_TuneCP5_13TeV_pythia8_RunIIAutumn18MiniAOD-PREMIX_RECODEBUG_102X_upgrade2018_realistic_v15_ext1-v1_MINIAODSIM/QCD_Pt_470to600_TuneCP5_13TeV_pythia8_RunIIAutumn18MiniAOD-PREMIX_RECODEBUG_102X_upgrade2018_realistic_v15_ext1-v1_MINIAODSIM.txt \
debug=1 \
maxEvents=10 \
> logs/ConfFile_cfg_QCD.log &
