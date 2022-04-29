nohup cmsRun MyTools/EDAnalyzers/python/ConfFile_cfg.py \
outFileBaseName=ntupleTree_Wprimetotb_M3000W30_LH \
outputDir=output \
sourceFile=sourceFiles/Wprimetotb_M3000W30_LH_TuneCP5_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2_MINIAODSIM/Wprimetotb_M3000W30_LH_TuneCP5_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2_MINIAODSIM.txt \
maxEvents=10000 \
debug=0 \
> logs/ConfFile_cfg_Wprimetotb_M3000W30_LH.log &


nohup cmsRun MyTools/EDAnalyzers/python/ConfFile_cfg.py \
outFileBaseName=ntupleTree_Wprimetotb_M3000W30_RH \
outputDir=output \
sourceFile=sourceFiles/Wprimetotb_M3000W30_RH_TuneCP5_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM/Wprimetotb_M3000W30_RH_TuneCP5_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM.txt \
maxEvents=10000 \
debug=0 \
> logs/ConfFile_cfg_Wprimetotb_M3000W30_RH.log &
