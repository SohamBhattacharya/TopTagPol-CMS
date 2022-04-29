#!/usr/bin/env python

from __future__ import print_function

import os


l_sampleName = [
"TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM",
"TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM",
"TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM",
"TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM",
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

