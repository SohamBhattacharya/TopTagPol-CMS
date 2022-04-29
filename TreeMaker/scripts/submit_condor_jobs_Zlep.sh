#!/usr/bin/env python

from __future__ import print_function

import os


l_sampleName = [
"ZprimeToZHToZlepHinc_narrow_M-600_TuneCP5_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2_MINIAODSIM",
"ZprimeToZHToZlepHinc_narrow_M-800_TuneCP5_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2_MINIAODSIM",
"ZprimeToZHToZlepHinc_narrow_M-1000_TuneCP5_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM",
"ZprimeToZHToZlepHinc_narrow_M-1200_TuneCP5_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM",
"ZprimeToZHToZlepHinc_narrow_M-1400_TuneCP5_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM",
"ZprimeToZHToZlepHinc_narrow_M-1600_TuneCP5_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM",
"ZprimeToZHToZlepHinc_narrow_M-1800_TuneCP5_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM",
"ZprimeToZHToZlepHinc_narrow_M-2000_TuneCP5_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM",
"ZprimeToZHToZlepHinc_narrow_M-2500_TuneCP5_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM",
"ZprimeToZHToZlepHinc_narrow_M-3000_TuneCP5_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM",
"ZprimeToZHToZlepHinc_narrow_M-3500_TuneCP5_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM",
"ZprimeToZHToZlepHinc_narrow_M-4000_TuneCP5_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM",
"Zprime_VBF_Zh_Zlephinc_narrow_M-600_TuneCP5_PSweights_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2_MINIAODSIM",
"Zprime_VBF_Zh_Zlephinc_narrow_M-800_TuneCP5_PSweights_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2_MINIAODSIM",
"Zprime_VBF_Zh_Zlephinc_narrow_M-1000_TuneCP5_PSweights_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2_MINIAODSIM",
"Zprime_VBF_Zh_Zlephinc_narrow_M-1200_TuneCP5_PSweights_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2_MINIAODSIM",
"Zprime_VBF_Zh_Zlephinc_narrow_M-1400_TuneCP5_PSweights_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2_MINIAODSIM",
"Zprime_VBF_Zh_Zlephinc_narrow_M-1600_TuneCP5_PSweights_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2_MINIAODSIM",
"Zprime_VBF_Zh_Zlephinc_narrow_M-1800_TuneCP5_PSweights_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2_MINIAODSIM",
"Zprime_VBF_Zh_Zlephinc_narrow_M-2000_TuneCP5_PSweights_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2_MINIAODSIM",
"Zprime_VBF_Zh_Zlephinc_narrow_M-2500_TuneCP5_PSweights_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2_MINIAODSIM",
"Zprime_VBF_Zh_Zlephinc_narrow_M-3000_TuneCP5_PSweights_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2_MINIAODSIM",
"Zprime_VBF_Zh_Zlephinc_narrow_M-3500_TuneCP5_PSweights_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2_MINIAODSIM",
"Zprime_VBF_Zh_Zlephinc_narrow_M-4000_TuneCP5_PSweights_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2_MINIAODSIM",
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
