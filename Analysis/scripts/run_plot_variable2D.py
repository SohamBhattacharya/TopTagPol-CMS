#!/usr/bin/env python

import os
import subprocess


username = subprocess.check_output(["whoami"]).strip().decode("UTF-8")


ymlConfig_str =  """
samples:
    
    TTJets:
        names:
            - "TTJets_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM:latest"
            - "TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM:latest"
            - "TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM:latest"
            - "TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM:latest"
        weights:
            - 1.821
            - 0.7532
            - 0.1316
            - 0.001407
    
    TTJets_HT-800to1200:
        names:
            - "TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM:latest"
        weights:
            - 1.0
    
    TTJets_HT-1200to2500:
        names:
            - "TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM:latest"
        weights:
            - 1.0
    
    ZprimeToTT_M1000_W10:
        names:
            - "ZprimeToTT_M1000_W10_TuneCP2_PSweights_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM:latest"
        weights:
            - 1.0
    
    ZprimeToTT_M2000_W20:
        names:
            - "ZprimeToTT_M2000_W20_TuneCP2_PSweights_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM:latest"
        weights:
            - 1.0
    
    ZprimeToTT_M3000_W30:
        names:
            - "ZprimeToTT_M3000_W30_TuneCP2_PSweights_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM:latest"
        weights:
            - 1.0
    
    ZprimeToTT_M4000_W40:
        names:
            - "ZprimeToTT_M4000_W40_TuneCP2_PSweights_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM:latest"
        weights:
            - 1.0
    
    Wprimetotb_M3000W30:
        names:
            - "Wprimetotb_M3000W30_LH_TuneCP5_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2_MINIAODSIM:latest"
            - "Wprimetotb_M3000W30_RH_TuneCP5_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM:latest"
        weights:
            - 1.0
            - 1.0
    
    Wprimetotb_M4000W40:
        names:
            - "Wprimetotb_M4000W40_LH_TuneCP5_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM:latest"
            - "Wprimetotb_M4000W40_RH_TuneCP5_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM:latest"
        weights:
            - 1.0
            - 1.0
    
    Wprimetotb_M6000W60:
        names:
            - "Wprimetotb_M6000W60_LH_TuneCP5_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM:latest"
            - "Wprimetotb_M6000W60_RH_TuneCP5_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM:latest"
        weights:
            - 1.0
            - 1.0
    
    QCD:
        names:
            - "QCD_Pt_300to470_TuneCP5_13TeV_pythia8_RunIIAutumn18MiniAOD-PREMIX_RECODEBUG_102X_upgrade2018_realistic_v15-v1_MINIAODSIM:latest"
            - "QCD_Pt_470to600_TuneCP5_13TeV_pythia8_RunIIAutumn18MiniAOD-PREMIX_RECODEBUG_102X_upgrade2018_realistic_v15_ext1-v1_MINIAODSIM:latest"
            - "QCD_Pt_600to800_TuneCP5_13TeV_pythia8_RunIIAutumn18MiniAOD-PREMIX_RECODEBUG_102X_upgrade2018_realistic_v15-v1_MINIAODSIM:latest"
            - "QCD_Pt_800to1000_TuneCP5_13TeV_pythia8_RunIIAutumn18MiniAOD-PREMIX_RECODEBUG_102X_upgrade2018_realistic_v15_ext1-v1_MINIAODSIM:latest"
            - "QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8_RunIIAutumn18MiniAOD-PREMIX_RECODEBUG_102X_upgrade2018_realistic_v15-v1_MINIAODSIM:latest"
            - "QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8_RunIIAutumn18MiniAOD-PREMIX_RECODEBUG_102X_upgrade2018_realistic_v15_ext1-v1_MINIAODSIM:latest"
            - "QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8_RunIIAutumn18MiniAOD-PREMIX_RECODEBUG_102X_upgrade2018_realistic_v15_ext1-v1_MINIAODSIM:latest"
            - "QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8_RunIIAutumn18MiniAOD-PREMIX_RECODEBUG_102X_upgrade2018_realistic_v15_ext1-v1_MINIAODSIM:latest"
        weights:
            - 6826.0
            - 552.6
            - 156.6
            - 26.32
            - 7.5
            - 0.6479
            - 0.08715
            - 0.005242
    

#friendlist:
#    
#    pnet:
#        - 


sample:         "Wprimetotb_M6000W60"
tree:           "treeMaker/tree"
source:         "ntupleLists/{sample}_{tag}.txt"
friends: []

plotX:           "genTop_pT"
plotY:           "ROOT::VecOps::DeltaR(genTop_Wlep_eta, genTop_b_eta, genTop_Wlep_phi, genTop_b_phi)"
wVar:            "abs(genTop_isLeptonic) > 0.5"

vardict:
    jet:            "jet_selectedPatJetsAK8PFPuppi_boost_2_1_sd_z0p1_b0_R1"

maxEntries: -1
binsX: "numpy.arange(0.0, 5000.0, 100)"
binsY: "numpy.arange(0.0, 5.0, 0.05)"
xRange:
    - 0.0
    - 3500.0
yRange:
    - 0.0
    - 3.0
zRange:
    - 1.0e-6
    - 1.0
nDivX: null
nDivY: null
logZ: true
xTitle: "t^{lep}_{gen} p_{T} [GeV]"
yTitle: "#DeltaR(lep_{gen}, b_{gen})"
zTitle: "a.u."
title: "W'_{6 TeV}"
titlePos:
    - 2000
    - 2.75
outFileName: plots/variables/others/deltaR-genTopB-genTopLep_vs_genTop-pT_WprimetotbM6000W60.pdf
cpufrac: 0.5

"""


timestamp = subprocess.check_output(["date", "+%Y-%m-%d_%H-%M-%N"]).strip().decode("UTF-8")

os.system(f"mkdir -p /tmp/{username}")
tmpCfgName = f"/tmp/{username}/config_plot_variable2D_{timestamp}.yml"

with open(tmpCfgName, "w") as fOut :
    
    fOut.write(ymlConfig_str)

cmd = f"python -u python/plot_variable2D.py --config {tmpCfgName}"
os.system(cmd)
