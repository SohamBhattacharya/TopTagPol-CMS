#!/usr/bin/env python

from __future__ import print_function

import os


l_sampleName = [
    "QCD_Pt_170to300_TuneCP5_13TeV_pythia8_RunIIAutumn18MiniAOD-PREMIX_RECODEBUG_102X_upgrade2018_realistic_v15-v1_MINIAODSIM",
    "QCD_Pt_300to470_TuneCP5_13TeV_pythia8_RunIIAutumn18MiniAOD-PREMIX_RECODEBUG_102X_upgrade2018_realistic_v15-v1_MINIAODSIM",
    "QCD_Pt_470to600_TuneCP5_13TeV_pythia8_RunIIAutumn18MiniAOD-PREMIX_RECODEBUG_102X_upgrade2018_realistic_v15_ext1-v1_MINIAODSIM",
    "QCD_Pt_600to800_TuneCP5_13TeV_pythia8_RunIIAutumn18MiniAOD-PREMIX_RECODEBUG_102X_upgrade2018_realistic_v15-v1_MINIAODSIM",
    "QCD_Pt_800to1000_TuneCP5_13TeV_pythia8_RunIIAutumn18MiniAOD-PREMIX_RECODEBUG_102X_upgrade2018_realistic_v15_ext1-v1_MINIAODSIM",
    "QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8_RunIIAutumn18MiniAOD-PREMIX_RECODEBUG_102X_upgrade2018_realistic_v15-v1_MINIAODSIM",
    "QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8_RunIIAutumn18MiniAOD-PREMIX_RECODEBUG_102X_upgrade2018_realistic_v15_ext1-v1_MINIAODSIM",
    "QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8_RunIIAutumn18MiniAOD-PREMIX_RECODEBUG_102X_upgrade2018_realistic_v15_ext1-v1_MINIAODSIM",
    "QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8_RunIIAutumn18MiniAOD-PREMIX_RECODEBUG_102X_upgrade2018_realistic_v15_ext1-v1_MINIAODSIM",
]


l_sourceFile = ["sourceFiles/{sampleName}/{sampleName}.txt".format(sampleName = sampleName) for sampleName in l_sampleName]


cmd = ("python scripts/run_condor.py "
    "--processNames {processNames} "
    "--inputFileLists {inputFileList} "
    "--cmsRunFile MyTools/EDAnalyzers/python/ConfFile_cfg.py "
    "--outputDir condorJobs "
    "--nUnitPerJob 1 "
    #"--nInputFileMax 2 "
    "--movetoT2 "
    #"--test "
).format(
    processNames = " ".join(l_sampleName),
    inputFileList = " ".join(l_sourceFile),
)

print(cmd)


os.system(cmd)
