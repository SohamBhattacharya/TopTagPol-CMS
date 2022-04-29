#!/usr/bin/env python

import os
import dataclasses

from typing import List, Set, Dict, Tuple, Optional


jetName = "jet_selectedPatJetsAK15PFPuppi_boost_2_1_sd_z0p1_b0_R1"
nJetMax = 10000


l_pdgid = [11, 13, 211]#, 13, 22, 211, 130]
l_pdgidName = ["e", "#mu", "CH"]#, "#mu", "#gamma", "CH", "NH"]

outDir = "plots/variables/%s" %(jetName)


commonCut = (
    "({jetName}_pT_reco > 200) & (fabs({jetName}_eta_reco) < 2.5) & "
    "({jetName}_nConsti_reco >= 3) "
)


@dataclasses.dataclass
class VariableInfo :
    
    varName : str
    plotBin : str
    xRange : str
    yRange : str
    xTitle : str
    yTitle : str
    outFileName : str
    
    logY : str = ""
    centerLabelX : str = ""


l_varInfo = []



l_varInfo.append(VariableInfo(
    varName = "mu_segCompat",
    plotBin = "100 0 5",
    xRange = "0 1",
    yRange = "1e-4 1e2",
    logY = "--logY",
    xTitle = "segment compatibility",
    yTitle = "arbitrary unit",
    outFileName = "mu_segCompat",
))

l_varInfo.append(VariableInfo(
    varName = "mu_nValidMuonHits",
    plotBin = "200 0 200",
    xRange = "0 60",
    yRange = "1e-4 1e2",
    logY = "--logY",
    #centerLabelX = "--centerLabelX",
    xTitle = "N_{valid #mu hit}",
    yTitle = "arbitrary unit",
    outFileName = "mu_nValidMuonHits",
))

l_varInfo.append(VariableInfo(
    varName = "mu_nMatchedStations",
    plotBin = "10 0 10",
    xRange = "0 10",
    yRange = "1e-4 1e2",
    logY = "--logY",
    #centerLabelX = "--centerLabelX",
    xTitle = "N_{#mu stations}",
    yTitle = "arbitrary unit",
    outFileName = "mu_nMatchedStations",
))

l_varInfo.append(VariableInfo(
    varName = "mu_nValidPixelHits",
    plotBin = "50 0 50",
    xRange = "0 20",
    yRange = "1e-4 1e2",
    logY = "--logY",
    #centerLabelX = "--centerLabelX",
    xTitle = "N_{valid pixel hit}",
    yTitle = "arbitrary unit",
    outFileName = "mu_nValidPixelHits",
))

l_varInfo.append(VariableInfo(
    varName = "mu_nTrackerLayers",
    plotBin = "50 0 50",
    xRange = "0 30",
    yRange = "1e-4 1e2",
    logY = "--logY",
    #centerLabelX = "--centerLabelX",
    xTitle = "N_{tracker layers}",
    yTitle = "arbitrary unit",
    outFileName = "mu_nTrackerLayers",
))

l_varInfo.append(VariableInfo(
    varName = "mu_miniPfIsoCH",
    plotBin = "1000 0 1000",
    xRange = "0 50",
    yRange = "1e-4 1e2",
    logY = "--logY",
    xTitle = "mini PF-iso (CH)",
    yTitle = "arbitrary unit",
    outFileName = "mu_miniPfIsoCH",
))

l_varInfo.append(VariableInfo(
    varName = "mu_miniPfIsoNH",
    plotBin = "1000 0 1000",
    xRange = "0 50",
    yRange = "1e-4 1e2",
    logY = "--logY",
    xTitle = "mini PF-iso (NH)",
    yTitle = "arbitrary unit",
    outFileName = "mu_miniPfIsoNH",
))

l_varInfo.append(VariableInfo(
    varName = "mu_miniPfIsoPh",
    plotBin = "1000 0 1000",
    xRange = "0 50",
    yRange = "1e-4 1e2",
    logY = "--logY",
    xTitle = "mini PF-iso (#gamma)",
    yTitle = "arbitrary unit",
    outFileName = "mu_miniPfIsoPh",
))


for iVar, varInfo in enumerate(l_varInfo) :
    
    d_format = {}
    #d_format["pdgid"]           = pdgid
    #d_format["pdgidName"]       = pdgidName
    d_format["outDir"]          = outDir
    d_format["jetName"]         = jetName
    d_format["nJetMax"]         = nJetMax
    
    d_format["commonCut"]       = commonCut.format(**d_format)
    
    d_format.update(varInfo.__dict__)
    
    
    
    command = """
        python -u python/plot_variable.py \
        --fileAndTreeNames \
            "sourceFiles/ZprimeToTT_M2000_W20_TuneCP2_PSweights_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM_2022-01-29_18-12-26.txt:treeMaker/tree" \
            "sourceFiles/QCD_Pt_470to600_TuneCP5_13TeV_pythia8_RunIIAutumn18MiniAOD-PREMIX_RECODEBUG_102X_upgrade2018_realistic_v15_ext1-v1_MINIAODSIM_2022-01-29_18-13-16.txt:treeMaker/tree" \
        --plotVars \
            "{jetName}_consti_{varName}_reco" \
            "{jetName}_consti_{varName}_reco" \
        --cuts \
            "({commonCut}) & ({jetName}_nearestGenTopDR_reco < 1) & (abs({jetName}_nearestGenTopIsLeptonic_reco) == 13) & ({jetName}_consti_pT_reco > 5) & (abs({jetName}_consti_id_reco) == 13) " \
            "({commonCut}) & ({jetName}_consti_pT_reco > 5) & (abs({jetName}_consti_id_reco) == 13) " \
        --labels \
            "PF-#mu in t^{{#mu}} jet" \
            "PF-#mu in QCD jet" \
        --lineColors \
            2 \
            4 \
        --lineStyles \
            1 \
            1 \
        --plotBin {plotBin} \
        --xRange {xRange} \
        --yRange {yRange} \
        --nJetMax {nJetMax} \
        --xTitle "{xTitle}" \
        --yTitle "{yTitle}" \
        --title "title" \
        --titlePos 0 0 \
        --outFileName "{outDir}/consti_{outFileName}.pdf" \
        {logY} \
        {centerLabelX} \
    """.format(
        **d_format
    )
    
    os.system(command)
    print("\n")
