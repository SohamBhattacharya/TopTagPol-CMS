#!/usr/bin/env python

import os


jetName = "jet_selectedPatJetsAK15PFPuppi_boost_2_1_sd_z0p1_b0_R1"
nJetMax = 100000


l_pdgid = [11, 13, 211]#, 13, 22, 211, 130]
l_pdgidName = ["e", "#mu", "CH"]#, "#mu", "#gamma", "CH", "NH"]

outDir = "plots/variables/%s" %(jetName)


commonCut = (
    "({jetName}_pT_reco > 200) & (fabs({jetName}_eta_reco) < 2.5) & "
    "({jetName}_nConsti_reco >= 3) "
)


for i in range(0, 1) :
#for pdgid, pdgidName in zip(l_pdgid, l_pdgidName) :
    
    d_format = {}
    #d_format["pdgid"]           = pdgid
    #d_format["pdgidName"]       = pdgidName
    d_format["outDir"]          = outDir
    d_format["jetName"]         = jetName
    d_format["nJetMax"]         = nJetMax
    
    d_format["commonCut"]       = commonCut.format(**d_format)
    
    
    
    #command = """
    #    python -u python/plot_variable.py \
    #    --fileAndTreeNames \
    #        "/nfs/dust/cms/user/sobhatta/work/TopTagPol/TreeMaker/CMSSW_10_5_0/src/output/ntupleTree_ZprimeToTT_M2000_W20.root:treeMaker/tree" \
    #        "/nfs/dust/cms/user/sobhatta/work/TopTagPol/TreeMaker/CMSSW_10_5_0/src/output/ntupleTree_ZprimeToTT_M2000_W20.root:treeMaker/tree" \
    #        "/nfs/dust/cms/user/sobhatta/work/TopTagPol/TreeMaker/CMSSW_10_5_0/src/output/ntupleTree_QCD_Pt_470to600.root:treeMaker/tree" \
    #        "/nfs/dust/cms/user/sobhatta/work/TopTagPol/TreeMaker/CMSSW_10_5_0/src/output/ntupleTree_QCD_Pt_470to600.root:treeMaker/tree" \
    #    --plotVars \
    #        "{jetName}_consti_ele_oldsigmaietaieta_reco" \
    #        "{jetName}_consti_ele_oldsigmaietaieta_reco" \
    #        "{jetName}_consti_ele_oldsigmaietaieta_reco" \
    #        "{jetName}_consti_ele_oldsigmaietaieta_reco" \
    #    --cuts \
    #        "({commonCut}) & ({jetName}_nearestGenTopDR_reco < 1) & (abs({jetName}_nearestGenTopIsLeptonic_reco) == 11) & ({jetName}_consti_pT_reco > 5) & (abs({jetName}_consti_id_reco) == 11) " \
    #        "({commonCut}) & ({jetName}_nearestGenTopDR_reco < 1) & (abs({jetName}_nearestGenTopIsLeptonic_reco) == 11) & ({jetName}_consti_pT_reco > 5) & (abs({jetName}_consti_id_reco) == 211)" \
    #        "({commonCut}) & ({jetName}_consti_pT_reco > 5) & (abs({jetName}_consti_id_reco) == 11) " \
    #        "({commonCut}) & ({jetName}_consti_pT_reco > 5) & (abs({jetName}_consti_id_reco) == 211)" \
    #    --labels \
    #        "PF-e in t^{{lep}} jet" \
    #        "PF-CH in t^{{lep}} jet" \
    #        "PF-e in QCD jet" \
    #        "PF-CH in QCD jet" \
    #    --lineColors \
    #        2 \
    #        4 \
    #        2 \
    #        4 \
    #    --lineStyles \
    #        1 \
    #        1 \
    #        7 \
    #        7 \
    #    --plotBin 1000 0 1 \
    #    --xRange 0 0.05 \
    #    --yRange 1e-4 1e2 \
    #    --nJetMax {nJetMax} \
    #    --logY \
    #    --xTitle "#sigma_{{i#etai#eta}}" \
    #    --yTitle "arbitrary unit" \
    #    --title "title" \
    #    --titlePos 0 0 \
    #    --outFileName "{outDir}/consti_ele_sigmaietaieta.pdf" \
    #""".format(
    #    **d_format
    #)
    #
    #os.system(command)
    #print("\n")
    #
    #
    #command = """
    #    python -u python/plot_variable.py \
    #    --fileAndTreeNames \
    #        "/nfs/dust/cms/user/sobhatta/work/TopTagPol/TreeMaker/CMSSW_10_5_0/src/output/ntupleTree_ZprimeToTT_M2000_W20.root:treeMaker/tree" \
    #        "/nfs/dust/cms/user/sobhatta/work/TopTagPol/TreeMaker/CMSSW_10_5_0/src/output/ntupleTree_ZprimeToTT_M2000_W20.root:treeMaker/tree" \
    #        "/nfs/dust/cms/user/sobhatta/work/TopTagPol/TreeMaker/CMSSW_10_5_0/src/output/ntupleTree_QCD_Pt_470to600.root:treeMaker/tree" \
    #        "/nfs/dust/cms/user/sobhatta/work/TopTagPol/TreeMaker/CMSSW_10_5_0/src/output/ntupleTree_QCD_Pt_470to600.root:treeMaker/tree" \
    #    --plotVars \
    #        "{jetName}_consti_ele_oldsigmaiphiiphi_reco" \
    #        "{jetName}_consti_ele_oldsigmaiphiiphi_reco" \
    #        "{jetName}_consti_ele_oldsigmaiphiiphi_reco" \
    #        "{jetName}_consti_ele_oldsigmaiphiiphi_reco" \
    #    --cuts \
    #        "({commonCut}) & ({jetName}_nearestGenTopDR_reco < 1) & (abs({jetName}_nearestGenTopIsLeptonic_reco) == 11) & ({jetName}_consti_pT_reco > 5) & (abs({jetName}_consti_id_reco) == 11) " \
    #        "({commonCut}) & ({jetName}_nearestGenTopDR_reco < 1) & (abs({jetName}_nearestGenTopIsLeptonic_reco) == 11) & ({jetName}_consti_pT_reco > 5) & (abs({jetName}_consti_id_reco) == 211)" \
    #        "({commonCut}) & ({jetName}_consti_pT_reco > 5) & (abs({jetName}_consti_id_reco) == 11) " \
    #        "({commonCut}) & ({jetName}_consti_pT_reco > 5) & (abs({jetName}_consti_id_reco) == 211)" \
    #    --labels \
    #        "PF-e in t^{{lep}} jet" \
    #        "PF-CH in t^{{lep}} jet" \
    #        "PF-e in QCD jet" \
    #        "PF-CH in QCD jet" \
    #    --lineColors \
    #        2 \
    #        4 \
    #        2 \
    #        4 \
    #    --lineStyles \
    #        1 \
    #        1 \
    #        7 \
    #        7 \
    #    --plotBin 1000 0 1 \
    #    --xRange 0 0.05 \
    #    --yRange 1e-4 1e2 \
    #    --nJetMax {nJetMax} \
    #    --logY \
    #    --xTitle "#sigma_{{i#phii#phi}}" \
    #    --yTitle "arbitrary unit" \
    #    --title "title" \
    #    --titlePos 0 0 \
    #    --outFileName "{outDir}/consti_ele_oldsigmaiphiiphi.pdf" \
    #""".format(
    #    **d_format
    #)
    #
    #os.system(command)
    #print("\n")
    
    
    command = """
        python -u python/plot_variable.py \
        --fileAndTreeNames \
            "/nfs/dust/cms/user/sobhatta/work/TopTagPol/TreeMaker/CMSSW_10_5_0/src/output/ntupleTree_ZprimeToTT_M2000_W20.root:treeMaker/tree" \
            "/nfs/dust/cms/user/sobhatta/work/TopTagPol/TreeMaker/CMSSW_10_5_0/src/output/ntupleTree_ZprimeToTT_M2000_W20.root:treeMaker/tree" \
            "/nfs/dust/cms/user/sobhatta/work/TopTagPol/TreeMaker/CMSSW_10_5_0/src/output/ntupleTree_QCD_Pt_470to600.root:treeMaker/tree" \
            "/nfs/dust/cms/user/sobhatta/work/TopTagPol/TreeMaker/CMSSW_10_5_0/src/output/ntupleTree_QCD_Pt_470to600.root:treeMaker/tree" \
        --plotVars \
            "{jetName}_consti_ele_oldr9_reco" \
            "{jetName}_consti_ele_oldr9_reco" \
            "{jetName}_consti_ele_oldr9_reco" \
            "{jetName}_consti_ele_oldr9_reco" \
        --cuts \
            "({commonCut}) & ({jetName}_nearestGenTopDR_reco < 1) & (abs({jetName}_nearestGenTopIsLeptonic_reco) == 11) & ({jetName}_consti_pT_reco > 5) & (abs({jetName}_consti_id_reco) == 11) " \
            "({commonCut}) & ({jetName}_nearestGenTopDR_reco < 1) & (abs({jetName}_nearestGenTopIsLeptonic_reco) == 11) & ({jetName}_consti_pT_reco > 5) & (abs({jetName}_consti_id_reco) == 211)" \
            "({commonCut}) & ({jetName}_consti_pT_reco > 5) & (abs({jetName}_consti_id_reco) == 11) " \
            "({commonCut}) & ({jetName}_consti_pT_reco > 5) & (abs({jetName}_consti_id_reco) == 211)" \
        --labels \
            "PF-e in t^{{lep}} jet" \
            "PF-CH in t^{{lep}} jet" \
            "PF-e in QCD jet" \
            "PF-CH in QCD jet" \
        --lineColors \
            2 \
            4 \
            2 \
            4 \
        --lineStyles \
            1 \
            1 \
            7 \
            7 \
        --plotBin 500 0 5 \
        --xRange 0 2 \
        --yRange 1e-4 1e2 \
        --nJetMax {nJetMax} \
        --logY \
        --xTitle "R_{{9}}" \
        --yTitle "arbitrary unit" \
        --title "title" \
        --titlePos 0 0 \
        --outFileName "{outDir}/consti_ele_oldr9.pdf" \
    """.format(
        **d_format
    )
    
    os.system(command)
    print("\n")
