#!/usr/bin/env python


import os


# NOTE: If you want to send {x} as an argument, use {{x}}
# Otherwise, {x} will have to be formatted here


l_pdgid = [11, 13, 22, 211, 130]
l_pdgidName = ["\$\\mathrm{{e}}\$", "\$\\mathrm{{\\mu}}\$", "\$\\mathrm{{\\gamma}}\$", "CH", "NH"]

for pdgid, pdgidName in zip(l_pdgid, l_pdgidName) :
    
    #command = """
    #    python -u plot_jetImage.py \
    #    --fileAndTreeNames \
    #        "/home/soham/naf_dust/work/TopTagPol/TreeMaker/CMSSW_10_5_0/src/ntupleTree_ZprimeToTT_M1000_W10_new.root:treeMaker/tree" \
    #    --cut \
    #        "(jet_selectedPatJetsAK15PFPuppi_pT_reco > 200) & (fabs(jet_selectedPatJetsAK15PFPuppi_eta_reco) < 2.4) & (jet_selectedPatJetsAK15PFPuppi_nConsti_reco >= 3) & (jet_selectedPatJetsAK15PFPuppi_nearestGenTopDR_reco < 1) & (jet_selectedPatJetsAK15PFPuppi_nearestGenTopIsLeptonic_reco > 0.5)" \
    #    --constiCut \
    #        "abs({{jet_selectedPatJetsAK15PFPuppi_consti_id_reco}}) == {pdgid}" \
    #    --nJetMax -1 \
    #    --xVar "jet_selectedPatJetsAK15PFPuppi_constiTrans_x_reco" \
    #    --yVar "jet_selectedPatJetsAK15PFPuppi_constiTrans_y_reco" \
    #    --wVar "jet_selectedPatJetsAK15PFPuppi_constiTrans_w_reco" \
    #    --resolverOperation "{{new}}+{{old}}" \
    #    --xMin -1 \
    #    --xMax +1 \
    #    --nBinX 50 \
    #    --yMin -1 \
    #    --yMax +1 \
    #    --nBinY 50 \
    #    --zMin 1e-6 \
    #    --zMax 1 \
    #    --xRange 0 50 \
    #    --yRange 0 65 \
    #    --logZ \
    #    --xTitle "x-axis pixel \#" \
    #    --yTitle "y-axis pixel \#" \
    #    --zTitle "Fraction of jet energy" \
    #    --title "\$\\mathrm{{t^\\text{{lep}}}}\$ jet (AK15) image ({pdgidName} component)\n\$\\mathrm{{Z^\\prime\\to t\\bar{{t}}}}\$ (\$\\mathrm{{m_{{Z^\\prime}}=1}}\$ TeV)\n\$\\mathrm{{p_{{T, \\text{{jet}}}} > 200~\\text{{GeV}},\\ |\\eta_\\text{{jet}}| < 2.4}}\$" \
    #    --titlePos 2 63 \
    #    --outFileName "jetImage_lepTop_energyFrac_constiPdgid{pdgid}_ZprimeToTT_M1000_W10.pdf" \
    #""".format(
    #    pdgid = pdgid,
    #    pdgidName = pdgidName,
    #)
    #
    #os.system(command)
    #print("\n")
    #
    #
    #
    #command = """
    #    python -u plot_jetImage.py \
    #    --fileAndTreeNames \
    #        "/home/soham/naf_dust/work/TopTagPol/TreeMaker/CMSSW_10_5_0/src/ntupleTree_QCD_Pt_470to600_PREMIX_RECODEBUG_new.root:treeMaker/tree" \
    #    --cut \
    #        "(jet_selectedPatJetsAK15PFPuppi_pT_reco > 200) & (fabs(jet_selectedPatJetsAK15PFPuppi_eta_reco) < 2.4) & (jet_selectedPatJetsAK15PFPuppi_nConsti_reco >= 3) & (jet_selectedPatJetsAK15PFPuppi_nearestGenTopDR_reco > 1)" \
    #    --constiCut \
    #        "abs({{jet_selectedPatJetsAK15PFPuppi_consti_id_reco}}) == {pdgid}" \
    #    --nJetMax -1 \
    #    --xVar "jet_selectedPatJetsAK15PFPuppi_constiTrans_x_reco" \
    #    --yVar "jet_selectedPatJetsAK15PFPuppi_constiTrans_y_reco" \
    #    --wVar "jet_selectedPatJetsAK15PFPuppi_constiTrans_w_reco" \
    #    --resolverOperation "{{new}}+{{old}}" \
    #    --xMin -1 \
    #    --xMax +1 \
    #    --nBinX 50 \
    #    --yMin -1 \
    #    --yMax +1 \
    #    --nBinY 50 \
    #    --zMin 1e-6 \
    #    --zMax 1 \
    #    --xRange 0 50 \
    #    --yRange 0 65 \
    #    --logZ \
    #    --xTitle "x-axis pixel \#" \
    #    --yTitle "y-axis pixel \#" \
    #    --zTitle "Fraction of jet energy" \
    #    --title "QCD jet (AK15) image ({pdgidName} component)\n\$\\mathrm{{p_{{T, \\text{{jet}}}} > 200~\\text{{GeV}},\\ |\\eta_\\text{{jet}}| < 2.4}}\$" \
    #    --titlePos 2 63 \
    #    --outFileName "jetImage_qcd_energyFrac_constiPdgid{pdgid}_QCD_Pt_470to600.pdf" \
    #""".format(
    #    pdgid = pdgid,
    #    pdgidName = pdgidName,
    #)
    #
    #os.system(command)
    #print("\n")
    
    
    
    command = """
        python -u plot_jetImage.py \
        --fileAndTreeNames \
            "/home/soham/naf_dust/work/TopTagPol/TreeMaker/CMSSW_10_5_0/src/ntupleTree_ZprimeToTT_M1000_W10_new.root:treeMaker/tree" \
        --cut \
            "(jet_selectedPatJetsAK15PFPuppi_pT_reco > 200) & (fabs(jet_selectedPatJetsAK15PFPuppi_eta_reco) < 2.4) & (jet_selectedPatJetsAK15PFPuppi_nConsti_reco >= 3) & (jet_selectedPatJetsAK15PFPuppi_nearestGenTopDR_reco < 1) & (jet_selectedPatJetsAK15PFPuppi_nearestGenTopIsLeptonic_reco > 0.5)" \
        --constiCut \
            "abs({{jet_selectedPatJetsAK15PFPuppi_consti_id_reco}}) == {pdgid}" \
        --nJetMax -1 \
        --xVar "jet_selectedPatJetsAK15PFPuppi_constiTrans_x_reco" \
        --yVar "jet_selectedPatJetsAK15PFPuppi_constiTrans_y_reco" \
        --wVar "jet_selectedPatJetsAK15PFPuppi_consti_dxy_reco" \
        --wTransform "(1 - min(20, {{w}})/20.0) if ({{w}} >= 0) else 0" "w" \
        --resolverOperation "{{new}} if ({{newResolver}} > {{oldResolver}}) else {{old}}" \
        --resolverUpdate "max({{newResolver}}, {{oldResolver}})" \
        --resolverVar "jet_selectedPatJetsAK15PFPuppi_consti_pT_reco" \
        --xMin -1 \
        --xMax +1 \
        --nBinX 50 \
        --yMin -1 \
        --yMax +1 \
        --nBinY 50 \
        --zMin 1e-6 \
        --zMax 1 \
        --xRange 0 50 \
        --yRange 0 65 \
        --logZ \
        --xTitle "x-axis pixel \#" \
        --yTitle "y-axis pixel \#" \
        --zTitle "Transformed \$\\mathrm{{\\abs{{d_{{xy}}}}}}\$ (w.r.t. SV in the jet)" \
        --title "\$\\mathrm{{t^\\text{{lep}}}}\$ jet (AK15) image ({pdgidName} component)\n\$\\mathrm{{Z^\\prime\\to t\\bar{{t}}}}\$ (\$\\mathrm{{m_{{Z^\\prime}}=1}}\$ TeV)\n\$\\mathrm{{p_{{T, \\text{{jet}}}} > 200~\\text{{GeV}},\\ |\\eta_\\text{{jet}}| < 2.4}}\$" \
        --titlePos 2 63 \
        --outFileName "jetImage_lepTop_dxyWrtSV_constiPdgid{pdgid}_ZprimeToTT_M1000_W10.pdf" \
    """.format(
        pdgid = pdgid,
        pdgidName = pdgidName,
    )
    
    os.system(command)
    print("\n")
    
    
    command = """
        python -u plot_jetImage.py \
        --fileAndTreeNames \
            "/home/soham/naf_dust/work/TopTagPol/TreeMaker/CMSSW_10_5_0/src/ntupleTree_QCD_Pt_470to600_PREMIX_RECODEBUG_new.root:treeMaker/tree" \
        --cut \
            "(jet_selectedPatJetsAK15PFPuppi_pT_reco > 200) & (fabs(jet_selectedPatJetsAK15PFPuppi_eta_reco) < 2.4) & (jet_selectedPatJetsAK15PFPuppi_nConsti_reco >= 3) & (jet_selectedPatJetsAK15PFPuppi_nearestGenTopDR_reco > 1)" \
        --constiCut \
            "abs({{jet_selectedPatJetsAK15PFPuppi_consti_id_reco}}) == {pdgid}" \
        --nJetMax -1 \
        --xVar "jet_selectedPatJetsAK15PFPuppi_constiTrans_x_reco" \
        --yVar "jet_selectedPatJetsAK15PFPuppi_constiTrans_y_reco" \
        --wVar "jet_selectedPatJetsAK15PFPuppi_consti_dxy_reco" \
        --wTransform "(1 - min(20, {{w}})/20.0) if ({{w}} >= 0) else 0" "w" \
        --resolverOperation "{{new}} if ({{newResolver}} > {{oldResolver}}) else {{old}}" \
        --resolverUpdate "max({{newResolver}}, {{oldResolver}})" \
        --resolverVar "jet_selectedPatJetsAK15PFPuppi_consti_pT_reco" \
        --xMin -1 \
        --xMax +1 \
        --nBinX 50 \
        --yMin -1 \
        --yMax +1 \
        --nBinY 50 \
        --zMin 1e-6 \
        --zMax 1 \
        --xRange 0 50 \
        --yRange 0 65 \
        --logZ \
        --xTitle "x-axis pixel \#" \
        --yTitle "y-axis pixel \#" \
        --zTitle "Transformed \$\\mathrm{{\\abs{{d_{{xy}}}}}}\$ (w.r.t. SV in the jet)" \
        --title "QCD jet (AK15) image ({pdgidName} component)\n\$\\mathrm{{p_{{T, \\text{{jet}}}} > 200~\\text{{GeV}},\\ |\\eta_\\text{{jet}}| < 2.4}}\$" \
        --titlePos 2 63 \
        --outFileName "jetImage_qcd_dxyWrtSV_constiPdgid{pdgid}_QCD_Pt_470to600.pdf" \
    """.format(
        pdgid = pdgid,
        pdgidName = pdgidName,
    )
    
    os.system(command)
    print("\n")
