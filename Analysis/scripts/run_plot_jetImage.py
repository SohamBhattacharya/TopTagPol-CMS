#!/usr/bin/env python

import os


# NOTE: If you want to send {x} as an argument, use {{x}}
# Otherwise, {x} will have to be formatted here


jetName = "jet_selectedPatJetsAK15PFPuppi_boost_2_1_sd_0p1_0_1"

nJetMax = 10000

l_pdgid = [11, 13, 22, 211, 130]
l_pdgidName = ["e", "#mu", "#gamma", "CH", "NH"]

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


xMin_PtEtaRot = -1.5
xMax_PtEtaRot = +1.5
nBinX_PtEtaRot = 50

yMin_PtEtaRot = -1.5
yMax_PtEtaRot = +1.5
nBinY_PtEtaRot = 50

xBinWidth_PtEtaRot = (xMax_PtEtaRot - xMin_PtEtaRot) / nBinX_PtEtaRot
yBinWidth_PtEtaRot = (yMax_PtEtaRot - yMin_PtEtaRot) / nBinY_PtEtaRot


outDir = "plots/jetImages"


for pdgid, pdgidName in zip(l_pdgid, l_pdgidName) :
    
    #command = """
    #    python -u python/plot_jetImage.py \
    #    --fileAndTreeNames \
    #        "sourceFiles/ZprimeToTT_M1000_W10_TuneCP2_PSweights_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM_2021-07-22_15-56-01.txt:treeMaker/tree" \
    #    --cut \
    #        "({jetName}_pT_reco > 200) & (fabs({jetName}_eta_reco) < 2.4) & ({jetName}_nConsti_reco >= 3) & ({jetName}_nearestGenTopDR_reco < 1) & ({jetName}_nearestGenTopIsLeptonic_reco > 0.5)" \
    #    --constiCut \
    #        "abs({jetName}_consti_id_reco) == {pdgid}" \
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
    #    --title "#splitline{{t^{{lep}} jet (AK15) image ({pdgidName} component)}}{{#splitline{{Z'#rightarrowt#bar{{t}}, m_{{Z'}} = 1 TeV}}{{p_{{T, jet}} #geq 200 GeV, |#eta_{{jet}}| < 2.4}}}}" \
    #    --titlePos 2 68 \
    #    --outFileName "{outDir}/jetImage_lepTop_energyFrac_constiPdgid{pdgid}_LBGS_ZprimeToTT_M1000_W10.pdf" \
    #""".format(
    #    jetName = jetName,
    #    nJetMax = nJetMax,
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
    
    
    #command = """
    #    python -u python/plot_jetImage.py \
    #    --fileAndTreeNames \
    #        "/nfs/dust/cms/user/sobhatta/work/TopTagPol/TreeMaker/CMSSW_10_5_0/src/ntupleTree_ZprimeToTT_M3000_W30.root:treeMaker/tree" \
    #    --cut \
    #        "({jetName}_pT_reco > 200) & (fabs({jetName}_eta_reco) < 2.4) & ({jetName}_nConsti_reco >= 3) & ({jetName}_nearestGenTopDR_reco < 1) & ({jetName}_nearestGenTopIsLeptonic_reco > 0.5)" \
    #    --constiCut \
    #        "abs({jetName}_consti_id_reco) == {pdgid}" \
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
    #    --title "#splitline{{t^{{lep}} jet (AK15) image ({pdgidName} component)}}{{#splitline{{Z'#rightarrowt#bar{{t}}, m_{{Z'}} = 3 TeV}}{{p_{{T, jet}} #geq 200 GeV, |#eta_{{jet}}| < 2.4}}}}" \
    #    --titlePos 2 68 \
    #    --outFileName "{outDir}/jetImage_lepTop_energyFrac_constiPdgid{pdgid}_LBGS_ZprimeToTT_M3000_W30.pdf" \
    #""".format(
    #    jetName = jetName,
    #    nJetMax = nJetMax,
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
    
    
    #command = """
    #    python -u python/plot_jetImage.py \
    #    --fileAndTreeNames \
    #        "sourceFiles/ZprimeToTT_M1000_W10_TuneCP2_PSweights_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM_2021-07-22_15-56-01.txt:treeMaker/tree" \
    #    --cut \
    #        "({jetName}_pT_reco > 200) & (fabs({jetName}_eta_reco) < 2.4) & ({jetName}_nConsti_reco >= 3) & ({jetName}_nearestGenTopDR_reco < 1) & ({jetName}_nearestGenTopIsLeptonic_reco > 0.5)" \
    #    --constiCut \
    #        "abs({jetName}_consti_id_reco) == {pdgid}" \
    #    --nJetMax {nJetMax} \
    #    --xVar "({jetName}_consti_PtEtaRot_dEta_reco - {xMin}) / {xBinWidth}" \
    #    --yVar "({jetName}_consti_PtEtaRot_dPhi_reco - {yMin}) / {yBinWidth}" \
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
    #    --title "#splitline{{t^{{lep}} jet (AK15) image ({pdgidName} component)}}{{#splitline{{Z'#rightarrowt#bar{{t}}, m_{{Z'}} = 1 TeV}}{{p_{{T, jet}} #geq 200 GeV, |#eta_{{jet}}| < 2.4}}}}" \
    #    --titlePos 2 68 \
    #    --outFileName "{outDir}/jetImage_lepTop_energyFrac_constiPdgid{pdgid}_PtEtaRot_ZprimeToTT_M1000_W10.pdf" \
    #""".format(
    #    jetName = jetName,
    #    nJetMax = nJetMax,
    #    pdgid = pdgid,
    #    pdgidName = pdgidName,
    #    xMin = xMin_PtEtaRot,
    #    xMax = xMax_PtEtaRot,
    #    xBinWidth = xBinWidth_PtEtaRot,
    #    yMin = yMin_PtEtaRot,
    #    yMax = yMax_PtEtaRot,
    #    yBinWidth = yBinWidth_PtEtaRot,
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
    #        "/nfs/dust/cms/user/sobhatta/work/TopTagPol/TreeMaker/CMSSW_10_5_0/src/ntupleTree_ZprimeToTT_M3000_W30.root:treeMaker/tree" \
    #    --cut \
    #        "({jetName}_pT_reco > 200) & (fabs({jetName}_eta_reco) < 2.4) & ({jetName}_nConsti_reco >= 3) & ({jetName}_nearestGenTopDR_reco < 1) & ({jetName}_nearestGenTopIsLeptonic_reco > 0.5)" \
    #    --constiCut \
    #        "abs({jetName}_consti_id_reco) == {pdgid}" \
    #    --nJetMax {nJetMax} \
    #    --xVar "({jetName}_consti_PtEtaRot_dEta_reco - {xMin}) / {xBinWidth}" \
    #    --yVar "({jetName}_consti_PtEtaRot_dPhi_reco - {yMin}) / {yBinWidth}" \
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
    #    --title "#splitline{{t^{{lep}} jet (AK15) image ({pdgidName} component)}}{{#splitline{{Z'#rightarrowt#bar{{t}}, m_{{Z'}} = 3 TeV}}{{p_{{T, jet}} #geq 200 GeV, |#eta_{{jet}}| < 2.4}}}}" \
    #    --titlePos 2 68 \
    #    --outFileName "{outDir}/jetImage_lepTop_energyFrac_constiPdgid{pdgid}_PtEtaRot_ZprimeToTT_M3000_W30.pdf" \
    #""".format(
    #    jetName = jetName,
    #    nJetMax = nJetMax,
    #    pdgid = pdgid,
    #    pdgidName = pdgidName,
    #    xMin = xMin_PtEtaRot,
    #    xMax = xMax_PtEtaRot,
    #    xBinWidth = xBinWidth_PtEtaRot,
    #    yMin = yMin_PtEtaRot,
    #    yMax = yMax_PtEtaRot,
    #    yBinWidth = yBinWidth_PtEtaRot,
    #    outDir = outDir,
    #)
    #
    #os.system(command)
    #print("\n")
    
    
    #command = """
    #    python -u python/plot_jetImage.py \
    #    --fileAndTreeNames \
    #        "sourceFiles/ZprimeToTT_M1000_W10_TuneCP2_PSweights_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM_2021-07-22_15-56-01.txt:treeMaker/tree" \
    #    --cut \
    #        "({jetName}_pT_reco > 200) & (fabs({jetName}_eta_reco) < 2.4) & ({jetName}_nConsti_reco >= 3) & ({jetName}_nearestGenTopDR_reco < 1) & ({jetName}_nearestGenTopIsLeptonic_reco < 0.5)" \
    #    --constiCut \
    #        "(abs({jetName}_consti_id_reco) == {pdgid})" \
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
    #    --title "#splitline{{t^{{had}} jet (AK15) image ({pdgidName} component)}}{{#splitline{{Z'#rightarrowt#bar{{t}}, m_{{Z'}} = 1 TeV}}{{p_{{T, jet}} #geq 200 GeV, |#eta_{{jet}}| < 2.4}}}}" \
    #    --titlePos 2 68 \
    #    --outFileName "{outDir}/jetImage_hadTop_energyFrac_constiPdgid{pdgid}_LBGS_ZprimeToTT_M1000_W10.pdf" \
    #""".format(
    #    jetName = jetName,
    #    nJetMax = nJetMax,
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
    #
    #command = """
    #    python -u python/plot_jetImage.py \
    #    --fileAndTreeNames \
    #        "sourceFiles/QCD_Pt_470to600_TuneCP5_13TeV_pythia8_RunIIAutumn18MiniAOD-PREMIX_RECODEBUG_102X_upgrade2018_realistic_v15_ext1-v1_MINIAODSIM_2021-07-22_15-54-16.txt:treeMaker/tree" \
    #    --cut \
    #        "({jetName}_pT_reco > 200) & (fabs({jetName}_eta_reco) < 2.4) & ({jetName}_nConsti_reco >= 3) & ({jetName}_nearestGenTopDR_reco > 1)" \
    #    --constiCut \
    #        "abs({jetName}_consti_id_reco) == {pdgid}" \
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
    #    --title "#splitline{{QCD jet (AK15) image ({pdgidName} component)}}{{p_{{T, jet}} #geq 200 GeV, |#eta_{{jet}}| < 2.4}}" \
    #    --titlePos 2 68 \
    #    --outFileName "{outDir}/jetImage_qcd_energyFrac_constiPdgid{pdgid}_LBGS_QCD_Pt_470to600.pdf" \
    #""".format(
    #    jetName = jetName,
    #    nJetMax = nJetMax,
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
            "sourceFiles/ZprimeToZHToZlepHinc_narrow_M-1000_TuneCP5_13TeV-madgraph-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM_2021-08-26_12-53-37.txt:treeMaker/tree" \
        --cut \
            "({jetName}_pT_reco > 200) & (fabs({jetName}_eta_reco) < 2.4) & ({jetName}_nConsti_reco >= 3) & ({jetName}_nearestGenZDR_reco < 1) & ({jetName}_nearestGenZIsLeptonic_reco > 0.5)" \
        --constiCut \
            "(abs({jetName}_consti_id_reco) == {pdgid})" \
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
        --title "#splitline{{Z^{{lep}} jet (AK15) image ({pdgidName} component)}}{{#splitline{{Z'#rightarrowZh, m_{{Z'}} = 1 TeV}}{{p_{{T, jet}} #geq 200 GeV, |#eta_{{jet}}| < 2.4}}}}" \
        --titlePos 2 68 \
        --outFileName "{outDir}/jetImage_lepZ_energyFrac_constiPdgid{pdgid}_LBGS_ZprimeToZH_M1000.pdf" \
    """.format(
        jetName = jetName,
        nJetMax = nJetMax,
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
    print("\n")
    
    
    
    #command = """
    #    python -u python/plot_jetImage.py \
    #    --fileAndTreeNames \
    #        "sourceFiles/ZprimeToTT_M1000_W10_TuneCP2_PSweights_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM_2021-07-22_15-56-01.txt:treeMaker/tree" \
    #    --cut \
    #        "({jetName}_pT_reco > 200) & (fabs({jetName}_eta_reco) < 2.4) & ({jetName}_nConsti_reco >= 3) & ({jetName}_nearestGenTopDR_reco < 1) & ({jetName}_nearestGenTopIsLeptonic_reco > 0.5)" \
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
    #    --title "#splitline{{t^{{lep}} jet (AK15) image ({pdgidName} component)}}{{#splitline{{Z'#rightarrowt#bar{{t}}, m_{{Z'}} = 1 TeV}}{{p_{{T, jet}} #geq 200 GeV, |#eta_{{jet}}| < 2.4}}}}" \
    #    --titlePos 2 68 \
    #    --outFileName "{outDir}/jetImage_lepTop_dxyWrtSV_constiPdgid{pdgid}_LBGS_ZprimeToTT_M1000_W10.pdf" \
    #""".format(
    #    jetName = jetName,
    #    nJetMax = nJetMax,
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
    #        "sourceFiles/ZprimeToTT_M1000_W10_TuneCP2_PSweights_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM_2021-07-22_15-56-01.txt:treeMaker/tree" \
    #    --cut \
    #        "({jetName}_pT_reco > 200) & (fabs({jetName}_eta_reco) < 2.4) & ({jetName}_nConsti_reco >= 3) & ({jetName}_nearestGenTopDR_reco < 1) & ({jetName}_nearestGenTopIsLeptonic_reco < 0.5)" \
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
    #    --title "#splitline{{t^{{had}} jet (AK15) image ({pdgidName} component)}}{{#splitline{{Z'#rightarrowt#bar{{t}}, m_{{Z'}} = 1 TeV}}{{p_{{T, jet}} #geq 200 GeV, |#eta_{{jet}}| < 2.4}}}}" \
    #    --titlePos 2 68 \
    #    --outFileName "{outDir}/jetImage_hadTop_dxyWrtSV_constiPdgid{pdgid}_LBGS_ZprimeToTT_M1000_W10.pdf" \
    #""".format(
    #    jetName = jetName,
    #    nJetMax = nJetMax,
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
    #        "sourceFiles/QCD_Pt_470to600_TuneCP5_13TeV_pythia8_RunIIAutumn18MiniAOD-PREMIX_RECODEBUG_102X_upgrade2018_realistic_v15_ext1-v1_MINIAODSIM_2021-07-22_15-54-16.txt:treeMaker/tree" \
    #    --cut \
    #        "({jetName}_pT_reco > 200) & (fabs({jetName}_eta_reco) < 2.4) & ({jetName}_nConsti_reco >= 3) & ({jetName}_nearestGenTopDR_reco > 1)" \
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
    #    --title "#splitline{{QCD jet (AK15) image ({pdgidName} component)}}{{p_{{T, jet}} #geq 200 GeV, |#eta_{{jet}}| < 2.4}}" \
    #    --titlePos 2 68 \
    #    --outFileName "{outDir}/jetImage_qcd_dxyWrtSV_constiPdgid{pdgid}_LBGS_QCD_Pt_470to600.pdf" \
    #""".format(
    #    jetName = jetName,
    #    nJetMax = nJetMax,
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
    
    
    
    
