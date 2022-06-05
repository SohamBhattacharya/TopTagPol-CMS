#!/usr/bin/env python

import os


# NOTE: If you want to send {x} as an argument, use {{x}}
# Otherwise, {x} will have to be formatted here

jetLabel = "AK8Puppi"
jetName = "jet_selectedPatJetsAK8PFPuppi_boost_2_1_sd_z0p1_b0_R1"

#jetLabel = "AK15"
#jetName = "jet_selectedPatJetsAK15PFPuppi_boost_2_1_sd_0p1_0_1"

nJetMax = 100000

l_pdgid = [0, 11, 13, 22, 211, 130]
l_pdgidName = ["all", "e", "#mu", "#gamma", "CH", "NH"]

#l_pdgid = [211]
#l_pdgidName = ["CH"]

xMin = -1.0
xMax = +1.0
nBinX = 50

yMin = -1.0
yMax = +1.0
nBinY = 50

xBinWidth = (xMax - xMin) / nBinX
yBinWidth = (yMax - yMin) / nBinY


xMin_EtaPhiRot = -0.8
xMax_EtaPhiRot = +0.8
nBinX_EtaPhiRot = 50

yMin_EtaPhiRot = -0.8
yMax_EtaPhiRot = +0.8
nBinY_EtaPhiRot = 50

xBinWidth_EtaPhiRot = (xMax_EtaPhiRot - xMin_EtaPhiRot) / nBinX_EtaPhiRot
yBinWidth_EtaPhiRot = (yMax_EtaPhiRot - yMin_EtaPhiRot) / nBinY_EtaPhiRot


outDir = f"plots/jetImages/{jetName}"


for pdgid, pdgidName in zip(l_pdgid, l_pdgidName) :
    
    constiCut = f"(abs({jetName}_consti_id_reco) == {pdgid})"
    
    if (pdgid == 0) :
        
        constiCut = f"(abs({jetName}_consti_id_reco) > 0)"
    
    command = """
        python -u python/plot_jetImage.py \
        --fileAndTreeNames \
            "ntupleLists/ZprimeToTT_M1000_W10_TuneCP2_PSweights_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM_latest.txt:treeMaker/tree" \
        --cut \
            "({jetName}_pT_reco > 400) & (fabs({jetName}_eta_reco) < 2.5) & ({jetName}_nConsti_reco >= 1) & ({jetName}_nearestGenTopDR_reco < 0.6) & ({jetName}_nearestGenTopIsLeptonic_reco > 0.5) & ({jetName}_nearestGenTopbDR_reco < 0.6) & ({jetName}_nearestGenTopWlepDR_reco < 0.6)" \
        --constiCut \
            "{constiCut}" \
        --nJetMax {nJetMax} \
        --xVar "({jetName}_consti_LBGS_x_reco - {xMin}) / {xBinWidth}" \
        --yVar "({jetName}_consti_LBGS_y_reco - {yMin}) / {yBinWidth}" \
        --wVar "{jetName}_consti_enFrac_reco" \
        --resolverOperation "{{new}}+{{old}}" \
        --xRange 0 50 \
        --yRange 0 70 \
        --zRange 1e-6 1 \
        --nDivX 5 5 0 \
        --nDivY 7 5 0 \
        --logZ \
        --xTitle "x-axis pixel no." \
        --yTitle "y-axis pixel no." \
        --zTitle "Fraction of jet energy" \
        --title "#splitline{{t^{{lep}} jet ({jetLabel}) image ({pdgidName} component)}}{{#splitline{{Z'#rightarrowt#bar{{t}}, m_{{Z'}} = 1 TeV}}{{p_{{T, jet}} > 400 GeV, |#eta_{{jet}}| < 2.5}}}}" \
        --titlePos 2 68 \
        --outFileName "{outDir}/jetImage_lepTop_energyFrac_constiPdgid{pdgid}_LBGS_ZprimeToTT_M1000_W10.pdf" \
    """.format(
        jetLabel = jetLabel,
        jetName = jetName,
        nJetMax = nJetMax,
        constiCut = constiCut,
        pdgid = pdgid,
        pdgidName = pdgidName,
        xMin = xMin,
        xMax = xMax,
        xBinWidth = xBinWidth,
        yMin = yMin,
        yMax = yMax,
        yBinWidth = yBinWidth,
        outDir = outDir,
    )
    
    os.system(command)
    #print("\n")
    
    
    command = """
        python -u python/plot_jetImage.py \
        --fileAndTreeNames \
            "ntupleLists/ZprimeToTT_M3000_W30_TuneCP2_PSweights_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM_latest.txt:treeMaker/tree" \
        --cut \
            "({jetName}_pT_reco > 400) & (abs({jetName}_eta_reco) < 2.5) & ({jetName}_nConsti_reco >= 1) & ({jetName}_nearestGenTopDR_reco < 0.6) & ({jetName}_nearestGenTopIsLeptonic_reco > 0.5) & ({jetName}_nearestGenTopbDR_reco < 0.6) & ({jetName}_nearestGenTopWlepDR_reco < 0.6)" \
        --constiCut \
            "{constiCut}" \
        --nJetMax {nJetMax} \
        --xVar "({jetName}_consti_LBGS_x_reco - {xMin}) / {xBinWidth}" \
        --yVar "({jetName}_consti_LBGS_y_reco - {yMin}) / {yBinWidth}" \
        --wVar "{jetName}_consti_enFrac_reco" \
        --resolverOperation "{{new}}+{{old}}" \
        --xRange 0 50 \
        --yRange 0 70 \
        --zRange 1e-6 1 \
        --nDivX 5 5 0 \
        --nDivY 7 5 0 \
        --logZ \
        --xTitle "x-axis pixel no." \
        --yTitle "y-axis pixel no." \
        --zTitle "Fraction of jet energy" \
        --title "#splitline{{t^{{lep}} jet ({jetLabel}) image ({pdgidName} component)}}{{#splitline{{Z'#rightarrowt#bar{{t}}, m_{{Z'}} = 3 TeV}}{{p_{{T, jet}} > 400 GeV, |#eta_{{jet}}| < 2.5}}}}" \
        --titlePos 2 68 \
        --outFileName "{outDir}/jetImage_lepTop_energyFrac_constiPdgid{pdgid}_LBGS_ZprimeToTT_M3000_W30.pdf" \
    """.format(
        jetLabel = jetLabel,
        jetName = jetName,
        nJetMax = nJetMax,
        constiCut = constiCut,
        pdgid = pdgid,
        pdgidName = pdgidName,
        xMin = xMin,
        xMax = xMax,
        xBinWidth = xBinWidth,
        yMin = yMin,
        yMax = yMax,
        yBinWidth = yBinWidth,
        outDir = outDir,
    )
    
    os.system(command)
    #print("\n")
    
    
    #command = """
    #    python -u python/plot_jetImage.py \
    #    --fileAndTreeNames \
    #        "ntupleLists/ZprimeToTT_M1000_W10_TuneCP2_PSweights_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM_latest.txt:treeMaker/tree" \
    #    --cut \
    #        "({jetName}_pT_reco > 400) & (fabs({jetName}_eta_reco) < 2.5) & ({jetName}_nConsti_reco >= 1) & ({jetName}_nearestGenTopDR_reco < 0.6) & ({jetName}_nearestGenTopIsLeptonic_reco > 0.5) & ({jetName}_nearestGenTopbDR_reco < 0.6) & ({jetName}_nearestGenTopWlepDR_reco < 0.6)" \
    #    --constiCut \
    #        "{constiCut}" \
    #    --nJetMax {nJetMax} \
    #    --xVar "({jetName}_consti_EtaPhiRot_dEta_reco - {xMin}) / {xBinWidth}" \
    #    --yVar "({jetName}_consti_EtaPhiRot_dPhi_reco - {yMin}) / {yBinWidth}" \
    #    --wVar "{jetName}_consti_enFrac_reco" \
    #    --resolverOperation "{{new}}+{{old}}" \
    #    --xRange 0 50 \
    #    --yRange 0 70 \
    #    --zRange 1e-6 1 \
    #    --nDivX 5 5 0 \
    #    --nDivY 7 5 0 \
    #    --logZ \
    #    --xTitle "x-axis pixel no." \
    #    --yTitle "y-axis pixel no." \
    #    --zTitle "Fraction of jet energy" \
    #    --title "#splitline{{t^{{lep}} jet ({jetLabel}) image ({pdgidName} component)}}{{#splitline{{Z'#rightarrowt#bar{{t}}, m_{{Z'}} = 1 TeV}}{{p_{{T, jet}} > 400 GeV, |#eta_{{jet}}| < 2.5}}}}" \
    #    --titlePos 2 68 \
    #    --outFileName "{outDir}/jetImage_lepTop_energyFrac_constiPdgid{pdgid}_EtaPhiRot_ZprimeToTT_M1000_W10.pdf" \
    #""".format(
    #    jetLabel = jetLabel,
    #    jetName = jetName,
    #    nJetMax = nJetMax,
    #    constiCut = constiCut,
    #    pdgid = pdgid,
    #    pdgidName = pdgidName,
    #    xMin = xMin_EtaPhiRot,
    #    xMax = xMax_EtaPhiRot,
    #    xBinWidth = xBinWidth_EtaPhiRot,
    #    yMin = yMin_EtaPhiRot,
    #    yMax = yMax_EtaPhiRot,
    #    yBinWidth = yBinWidth_EtaPhiRot,
    #    outDir = outDir,
    #)
    #
    #os.system(command)
    #print("\n")
    #
    #
    #command = """
    #    python -u python/plot_jetImage.py \
    #    --fileAndTreeNames \
    #        "ntupleLists/ZprimeToTT_M3000_W30_TuneCP2_PSweights_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM_latest.txt:treeMaker/tree" \
    #    --cut \
    #        "({jetName}_pT_reco > 400) & (fabs({jetName}_eta_reco) < 2.5) & ({jetName}_nConsti_reco >= 1) & ({jetName}_nearestGenTopDR_reco < 0.6) & ({jetName}_nearestGenTopIsLeptonic_reco > 0.5) & ({jetName}_nearestGenTopbDR_reco < 0.6) & ({jetName}_nearestGenTopWlepDR_reco < 0.6)" \
    #    --constiCut \
    #        "{constiCut}" \
    #    --nJetMax {nJetMax} \
    #    --xVar "({jetName}_consti_EtaPhiRot_dEta_reco - {xMin}) / {xBinWidth}" \
    #    --yVar "({jetName}_consti_EtaPhiRot_dPhi_reco - {yMin}) / {yBinWidth}" \
    #    --wVar "{jetName}_consti_enFrac_reco" \
    #    --resolverOperation "{{new}}+{{old}}" \
    #    --xRange 0 50 \
    #    --yRange 0 70 \
    #    --zRange 1e-6 1 \
    #    --nDivX 5 5 0 \
    #    --nDivY 7 5 0 \
    #    --logZ \
    #    --xTitle "x-axis pixel no." \
    #    --yTitle "y-axis pixel no." \
    #    --zTitle "Fraction of jet energy" \
    #    --title "#splitline{{t^{{lep}} jet ({jetLabel}) image ({pdgidName} component)}}{{#splitline{{Z'#rightarrowt#bar{{t}}, m_{{Z'}} = 3 TeV}}{{p_{{T, jet}} > 400 GeV, |#eta_{{jet}}| < 2.5}}}}" \
    #    --titlePos 2 68 \
    #    --outFileName "{outDir}/jetImage_lepTop_energyFrac_constiPdgid{pdgid}_EtaPhiRot_ZprimeToTT_M3000_W30.pdf" \
    #""".format(
    #    jetLabel = jetLabel,
    #    jetName = jetName,
    #    nJetMax = nJetMax,
    #    constiCut = constiCut,
    #    pdgid = pdgid,
    #    pdgidName = pdgidName,
    #    xMin = xMin_EtaPhiRot,
    #    xMax = xMax_EtaPhiRot,
    #    xBinWidth = xBinWidth_EtaPhiRot,
    #    yMin = yMin_EtaPhiRot,
    #    yMax = yMax_EtaPhiRot,
    #    yBinWidth = yBinWidth_EtaPhiRot,
    #    outDir = outDir,
    #)
    #
    #os.system(command)
    #print("\n")
    #
    #
    #command = """
    #    python -u python/plot_jetImage.py \
    #    --fileAndTreeNames \
    #        "ntupleLists/ZprimeToTT_M3000_W30_TuneCP2_PSweights_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM_latest.txt:treeMaker/tree" \
    #    --cut \
    #        "({jetName}_pT_reco > 400) & (fabs({jetName}_eta_reco) < 2.5) & ({jetName}_nConsti_reco >= 1) & ({jetName}_nearestGenTopDR_reco < 0.6) & ({jetName}_nearestGenTopIsLeptonic_reco > 0.5) & ({jetName}_nearestGenTopbDR_reco < 0.6) & ({jetName}_nearestGenTopWlepDR_reco < 0.6)" \
    #    --constiCut \
    #        "{constiCut}" \
    #    --nJetMax {nJetMax} \
    #    --xVar "({jetName}_consti_dEta_reco - {xMin}) / {xBinWidth}" \
    #    --yVar "({jetName}_consti_dPhi_reco - {yMin}) / {yBinWidth}" \
    #    --wVar "{jetName}_consti_enFrac_reco" \
    #    --resolverOperation "{{new}}+{{old}}" \
    #    --xRange 0 50 \
    #    --yRange 0 70 \
    #    --zRange 1e-6 1 \
    #    --nDivX 5 5 0 \
    #    --nDivY 7 5 0 \
    #    --logZ \
    #    --xTitle "x-axis pixel no." \
    #    --yTitle "y-axis pixel no." \
    #    --zTitle "Fraction of jet energy" \
    #    --title "#splitline{{t^{{lep}} jet ({jetLabel}) image ({pdgidName} component)}}{{#splitline{{Z'#rightarrowt#bar{{t}}, m_{{Z'}} = 3 TeV}}{{p_{{T, jet}} > 400 GeV, |#eta_{{jet}}| < 2.5}}}}" \
    #    --titlePos 2 68 \
    #    --outFileName "{outDir}/jetImage_lepTop_energyFrac_constiPdgid{pdgid}_DetaDphi_ZprimeToTT_M3000_W30.pdf" \
    #""".format(
    #    jetLabel = jetLabel,
    #    jetName = jetName,
    #    nJetMax = nJetMax,
    #    constiCut = constiCut,
    #    pdgid = pdgid,
    #    pdgidName = pdgidName,
    #    xMin = xMin_EtaPhiRot,
    #    xMax = xMax_EtaPhiRot,
    #    xBinWidth = xBinWidth_EtaPhiRot,
    #    yMin = yMin_EtaPhiRot,
    #    yMax = yMax_EtaPhiRot,
    #    yBinWidth = yBinWidth_EtaPhiRot,
    #    outDir = outDir,
    #)
    #
    #os.system(command)
    #print("\n")
    
    
    #command = """
    #    python -u python/plot_jetImage.py \
    #    --fileAndTreeNames \
    #        "ntupleLists/ZprimeToTT_M1000_W10_TuneCP2_PSweights_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM_latest.txt:treeMaker/tree" \
    #    --cut \
    #        "({jetName}_pT_reco > 400) & (fabs({jetName}_eta_reco) < 2.5) & ({jetName}_nConsti_reco >= 1) & ({jetName}_nearestGenTopDR_reco < 0.6) & ({jetName}_nearestGenTopIsLeptonic_reco > 0.5) & ({jetName}_nearestGenTopbDR_reco < 0.6) & ({jetName}_nearestGenTopWlepDR_reco < 0.6)" \
    #    --constiCut \
    #        "{constiCut}" \
    #    --nJetMax {nJetMax} \
    #    --xVar "({jetName}_consti_LBGS_x_reco - {xMin}) / {xBinWidth}" \
    #    --yVar "({jetName}_consti_LBGS_y_reco - {yMin}) / {yBinWidth}" \
    #    --wVar "{jetName}_consti_enFrac_reco" \
    #    --resolverOperation "{{new}}+{{old}}" \
    #    --xRange 0 50 \
    #    --yRange 0 70 \
    #    --zRange 1e-6 1 \
    #    --nDivX 5 5 0 \
    #    --nDivY 7 5 0 \
    #    --logZ \
    #    --xTitle "x-axis pixel no." \
    #    --yTitle "y-axis pixel no." \
    #    --zTitle "Fraction of jet energy" \
    #    --title "#splitline{{t^{{had}} jet ({jetLabel}) image ({pdgidName} component)}}{{#splitline{{Z'#rightarrowt#bar{{t}}, m_{{Z'}} = 1 TeV}}{{p_{{T, jet}} > 400 GeV, |#eta_{{jet}}| < 2.5}}}}" \
    #    --titlePos 2 68 \
    #    --outFileName "{outDir}/jetImage_hadTop_energyFrac_constiPdgid{pdgid}_LBGS_ZprimeToTT_M1000_W10.pdf" \
    #""".format(
    #    jetLabel = jetLabel,
    #    jetName = jetName,
    #    nJetMax = nJetMax,
    #    constiCut = constiCut,
    #    pdgid = pdgid,
    #    pdgidName = pdgidName,
    #    xMin = xMin,
    #    xMax = xMax,
    #    xBinWidth = xBinWidth,
    #    yMin = yMin,
    #    yMax = yMax,
    #    yBinWidth = yBinWidth,
    #    outDir = outDir,
    #)
    #
    #os.system(command)
    #print("\n")
    
    
    
    command = """
        python -u python/plot_jetImage.py \
        --fileAndTreeNames \
            "ntupleLists/QCD_Pt_470to600_TuneCP5_13TeV_pythia8_RunIIAutumn18MiniAOD-PREMIX_RECODEBUG_102X_upgrade2018_realistic_v15_ext1-v1_MINIAODSIM_latest.txt:treeMaker/tree" \
        --cut \
            "({jetName}_pT_reco > 400) & (abs({jetName}_eta_reco) < 2.5) & ({jetName}_nConsti_reco >= 1) & ({jetName}_nearestGenTopDR_reco > 1)" \
        --constiCut \
            "{constiCut}" \
        --nJetMax {nJetMax} \
        --xVar "({jetName}_consti_LBGS_x_reco - {xMin}) / {xBinWidth}" \
        --yVar "({jetName}_consti_LBGS_y_reco - {yMin}) / {yBinWidth}" \
        --wVar "{jetName}_consti_enFrac_reco" \
        --resolverOperation "{{new}}+{{old}}" \
        --xRange 0 50 \
        --yRange 0 70 \
        --zRange 1e-6 1 \
        --nDivX 5 5 0 \
        --nDivY 7 5 0 \
        --logZ \
        --xTitle "x-axis pixel no." \
        --yTitle "y-axis pixel no." \
        --zTitle "Fraction of jet energy" \
        --title "#splitline{{QCD jet ({jetLabel}) image ({pdgidName} component)}}{{p_{{T, jet}} > 400 GeV, |#eta_{{jet}}| < 2.5}}" \
        --titlePos 2 68 \
        --outFileName "{outDir}/jetImage_qcd_energyFrac_constiPdgid{pdgid}_LBGS_QCD_Pt_470to600.pdf" \
    """.format(
        jetName = jetName,
        jetLabel = jetLabel,
        nJetMax = nJetMax,
        constiCut = constiCut,
        pdgid = pdgid,
        pdgidName = pdgidName,
        xMin = xMin,
        xMax = xMax,
        xBinWidth = xBinWidth,
        yMin = yMin,
        yMax = yMax,
        yBinWidth = yBinWidth,
        outDir = outDir,
    )
    
    os.system(command)
    #print("\n")
    
    
    
    command = """
        python -u python/plot_jetImage.py \
        --fileAndTreeNames \
            "ntupleLists/WJetsToLNu_Pt-400To600_TuneCP5_13TeV-amcatnloFXFX-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM_latest.txt:treeMaker/tree" \
        --cut \
            "({jetName}_pT_reco > 400) & (abs({jetName}_eta_reco) < 2.5) & ({jetName}_nConsti_reco >= 1) & ({jetName}_nearestGenWDR_reco < 0.6) & ({jetName}_nearestGenWIsLeptonic_reco > 0.5)" \
        --constiCut \
            "{constiCut}" \
        --nJetMax {nJetMax} \
        --xVar "({jetName}_consti_LBGS_x_reco - {xMin}) / {xBinWidth}" \
        --yVar "({jetName}_consti_LBGS_y_reco - {yMin}) / {yBinWidth}" \
        --wVar "{jetName}_consti_enFrac_reco" \
        --resolverOperation "{{new}}+{{old}}" \
        --xRange 0 50 \
        --yRange 0 70 \
        --zRange 1e-6 1 \
        --nDivX 5 5 0 \
        --nDivY 7 5 0 \
        --logZ \
        --xTitle "x-axis pixel no." \
        --yTitle "y-axis pixel no." \
        --zTitle "Fraction of jet energy" \
        --title "#splitline{{W^{{lep}} jet ({jetLabel}) image ({pdgidName} component)}}{{#splitline{{W+jets, 400 < p_{{T}} < 600 GeV}}{{p_{{T, jet}} > 400 GeV, |#eta_{{jet}}| < 2.5}}}}" \
        --titlePos 2 68 \
        --outFileName "{outDir}/jetImage_lepW_energyFrac_constiPdgid{pdgid}_LBGS_WJetsToLNu_Pt-400To600.pdf" \
    """.format(
        jetName = jetName,
        jetLabel = jetLabel,
        nJetMax = nJetMax,
        constiCut = constiCut,
        pdgid = pdgid,
        pdgidName = pdgidName,
        xMin = xMin,
        xMax = xMax,
        xBinWidth = xBinWidth,
        yMin = yMin,
        yMax = yMax,
        yBinWidth = yBinWidth,
        outDir = outDir,
    )
    
    os.system(command)
    #print("\n")
    
    
    command = """
        python -u python/plot_jetImage.py \
        --fileAndTreeNames \
            "ntupleLists/DYJetsToLL_Pt-400To650_TuneCP5_13TeV-amcatnloFXFX-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM_latest.txt:treeMaker/tree" \
        --cut \
            "({jetName}_pT_reco > 400) & (abs({jetName}_eta_reco) < 2.5) & ({jetName}_nConsti_reco >= 1) & ({jetName}_nearestGenZDR_reco < 0.6) & ({jetName}_nearestGenZIsLeptonic_reco > 0.5) & ({jetName}_nearestGenZlep1DR_reco < 0.6) & ({jetName}_nearestGenZlep2DR_reco < 0.6)" \
        --constiCut \
            "{constiCut}" \
        --nJetMax {nJetMax} \
        --xVar "({jetName}_consti_LBGS_x_reco - {xMin}) / {xBinWidth}" \
        --yVar "({jetName}_consti_LBGS_y_reco - {yMin}) / {yBinWidth}" \
        --wVar "{jetName}_consti_enFrac_reco" \
        --resolverOperation "{{new}}+{{old}}" \
        --xRange 0 50 \
        --yRange 0 70 \
        --zRange 1e-6 1 \
        --nDivX 5 5 0 \
        --nDivY 7 5 0 \
        --logZ \
        --xTitle "x-axis pixel no." \
        --yTitle "y-axis pixel no." \
        --zTitle "Fraction of jet energy" \
        --title "#splitline{{Z^{{lep}} jet ({jetLabel}) image ({pdgidName} component)}}{{#splitline{{Z+jets, 400 < p_{{T}} < 650 GeV}}{{p_{{T, jet}} > 400 GeV, |#eta_{{jet}}| < 2.5}}}}" \
        --titlePos 2 68 \
        --outFileName "{outDir}/jetImage_lepZ_energyFrac_constiPdgid{pdgid}_LBGS_DYJetsToLL_Pt-400To650.pdf" \
    """.format(
        jetName = jetName,
        jetLabel = jetLabel,
        nJetMax = nJetMax,
        constiCut = constiCut,
        pdgid = pdgid,
        pdgidName = pdgidName,
        xMin = xMin,
        xMax = xMax,
        xBinWidth = xBinWidth,
        yMin = yMin,
        yMax = yMax,
        yBinWidth = yBinWidth,
        outDir = outDir,
    )
    
    os.system(command)
    #print("\n")
    
    
    
    #command = """
    #    python -u python/plot_jetImage.py \
    #    --fileAndTreeNames \
    #        "ntupleLists/ZprimeToTT_M1000_W10_TuneCP2_PSweights_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM_latest.txt:treeMaker/tree" \
    #    --cut \
    #        "({jetName}_pT_reco > 400) & (fabs({jetName}_eta_reco) < 2.5) & ({jetName}_nConsti_reco >= 1) & ({jetName}_nearestGenTopDR_reco < 0.6) & ({jetName}_nearestGenTopIsLeptonic_reco > 0.5)" \
    #    --constiCut \
    #        "(abs({jetName}_consti_id_reco) == {pdgid}) * ({jetName}_consti_pT_reco > 20)" \
    #    --nJetMax {nJetMax} \
    #    --xVar "({jetName}_consti_LBGS_x_reco - {xMin}) / {xBinWidth}" \
    #    --yVar "({jetName}_consti_LBGS_y_reco - {yMin}) / {yBinWidth}" \
    #    --wVar "where({jetName}_consti_svdxy_reco < 0, 0, 1-min({jetName}_consti_svdxy_reco, 3)/3.0)" \
    #    --resolverOperation "{{new}} if ({{newResolver}} > {{oldResolver}}) else {{old}}" \
    #    --resolverUpdate "max({{newResolver}}, {{oldResolver}})" \
    #    --resolverVar "{jetName}_consti_pT_reco" \
    #    --xRange 0 50 \
    #    --yRange 0 70 \
    #    --zRange 1e-6 1 \
    #    --nDivX 5 5 0 \
    #    --nDivY 7 5 0 \
    #    --logZ \
    #    --xTitle "x-axis pixel no." \
    #    --yTitle "y-axis pixel no." \
    #    --zTitle "Transformed |d_{{xy}}({pdgidName}, SV)|" \
    #    --title "#splitline{{t^{{lep}} jet ({jetLabel}) image ({pdgidName} component)}}{{#splitline{{Z'#rightarrowt#bar{{t}}, m_{{Z'}} = 1 TeV}}{{p_{{T, jet}} > 400 GeV, |#eta_{{jet}}| < 2.5}}}}" \
    #    --titlePos 2 68 \
    #    --outFileName "{outDir}/jetImage_lepTop_dxyWrtSV_constiPdgid{pdgid}_LBGS_ZprimeToTT_M1000_W10.pdf" \
    #""".format(
    #    jetName = jetName,
    #    nJetMax = nJetMax,
    #    constiCut = constiCut,
    #    pdgid = pdgid,
    #    pdgidName = pdgidName,
    #    xMin = xMin,
    #    xMax = xMax,
    #    xBinWidth = xBinWidth,
    #    yMin = yMin,
    #    yMax = yMax,
    #    yBinWidth = yBinWidth,
    #    outDir = outDir,
    #)
    #
    #os.system(command)
    #print("\n")
    #
    #
    #command = """
    #    python -u python/plot_jetImage.py \
    #    --fileAndTreeNames \
    #        "ntupleLists/ZprimeToTT_M1000_W10_TuneCP2_PSweights_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM_latest.txt:treeMaker/tree" \
    #    --cut \
    #        "({jetName}_pT_reco > 400) & (fabs({jetName}_eta_reco) < 2.5) & ({jetName}_nConsti_reco >= 1) & ({jetName}_nearestGenTopDR_reco < 0.6) & ({jetName}_nearestGenTopIsLeptonic_reco < 0.5)" \
    #    --constiCut \
    #        "(abs({jetName}_consti_id_reco) == {pdgid}) * ({jetName}_consti_pT_reco > 20)" \
    #    --nJetMax {nJetMax} \
    #    --xVar "({jetName}_consti_LBGS_x_reco - {xMin}) / {xBinWidth}" \
    #    --yVar "({jetName}_consti_LBGS_y_reco - {yMin}) / {yBinWidth}" \
    #    --wVar "where({jetName}_consti_svdxy_reco < 0, 0, 1-min({jetName}_consti_svdxy_reco, 3)/3.0)" \
    #    --resolverOperation "{{new}} if ({{newResolver}} > {{oldResolver}}) else {{old}}" \
    #    --resolverUpdate "max({{newResolver}}, {{oldResolver}})" \
    #    --resolverVar "{jetName}_consti_pT_reco" \
    #    --xRange 0 50 \
    #    --yRange 0 70 \
    #    --zRange 1e-6 1 \
    #    --nDivX 5 5 0 \
    #    --nDivY 7 5 0 \
    #    --logZ \
    #    --xTitle "x-axis pixel no." \
    #    --yTitle "y-axis pixel no." \
    #    --zTitle "Transformed |d_{{xy}}({pdgidName}, SV)|" \
    #    --title "#splitline{{t^{{had}} jet ({jetLabel}) image ({pdgidName} component)}}{{#splitline{{Z'#rightarrowt#bar{{t}}, m_{{Z'}} = 1 TeV}}{{p_{{T, jet}} > 400 GeV, |#eta_{{jet}}| < 2.5}}}}" \
    #    --titlePos 2 68 \
    #    --outFileName "{outDir}/jetImage_hadTop_dxyWrtSV_constiPdgid{pdgid}_LBGS_ZprimeToTT_M1000_W10.pdf" \
    #""".format(
    #    jetName = jetName,
    #    nJetMax = nJetMax,
    #    constiCut = constiCut,
    #    pdgid = pdgid,
    #    pdgidName = pdgidName,
    #    xMin = xMin,
    #    xMax = xMax,
    #    xBinWidth = xBinWidth,
    #    yMin = yMin,
    #    yMax = yMax,
    #    yBinWidth = yBinWidth,
    #    outDir = outDir,
    #)
    #
    #os.system(command)
    #print("\n")
    #
    #
    #command = """
    #    python -u python/plot_jetImage.py \
    #    --fileAndTreeNames \
    #        "ntupleLists/QCD_Pt_470to600_TuneCP5_13TeV_pythia8_RunIIAutumn18MiniAOD-PREMIX_RECODEBUG_102X_upgrade2018_realistic_v15_ext1-v1_MINIAODSIM_latest.txt:treeMaker/tree" \
    #    --cut \
    #        "({jetName}_pT_reco > 400) & (fabs({jetName}_eta_reco) < 2.5) & ({jetName}_nConsti_reco >= 1) & ({jetName}_nearestGenTopDR_reco > 1)" \
    #    --constiCut \
    #        "abs({jetName}_consti_id_reco) == {pdgid} * ({jetName}_consti_pT_reco > 20)" \
    #    --nJetMax {nJetMax} \
    #    --xVar "({jetName}_consti_LBGS_x_reco - {xMin}) / {xBinWidth}" \
    #    --yVar "({jetName}_consti_LBGS_y_reco - {yMin}) / {yBinWidth}" \
    #    --wVar "where({jetName}_consti_svdxy_reco < 0, 0, 1-min({jetName}_consti_svdxy_reco, 3)/3.0)" \
    #    --resolverOperation "{{new}} if ({{newResolver}} > {{oldResolver}}) else {{old}}" \
    #    --resolverUpdate "max({{newResolver}}, {{oldResolver}})" \
    #    --resolverVar "{jetName}_consti_pT_reco" \
    #    --xRange 0 50 \
    #    --yRange 0 70 \
    #    --zRange 1e-6 1 \
    #    --nDivX 5 5 0 \
    #    --nDivY 7 5 0 \
    #    --logZ \
    #    --xTitle "x-axis pixel no." \
    #    --yTitle "y-axis pixel no." \
    #    --zTitle "Transformed |d_{{xy}}({pdgidName}, SV)|" \
    #    --title "#splitline{{QCD jet ({jetLabel}) image ({pdgidName} component)}}{{p_{{T, jet}} > 400 GeV, |#eta_{{jet}}| < 2.5}}" \
    #    --titlePos 2 68 \
    #    --outFileName "{outDir}/jetImage_qcd_dxyWrtSV_constiPdgid{pdgid}_LBGS_QCD_Pt_470to600.pdf" \
    #""".format(
    #    jetName = jetName,
    #    nJetMax = nJetMax,
    #    constiCut = constiCut,
    #    pdgid = pdgid,
    #    pdgidName = pdgidName,
    #    xMin = xMin,
    #    xMax = xMax,
    #    xBinWidth = xBinWidth,
    #    yMin = yMin,
    #    yMax = yMax,
    #    yBinWidth = yBinWidth,
    #    outDir = outDir,
    #)
    #
    #os.system(command)
    #print("\n")
    
    
    
    
