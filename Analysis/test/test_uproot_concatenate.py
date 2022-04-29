import uproot


l_file = [
"/pnfs/desy.de/cms/tier2/store/user/sobhatta/TopTagPol/ntuples/QCD_Pt_170to300_TuneCP5_13TeV_pythia8_RunIIAutumn18MiniAOD-PREMIX_RECODEBUG_102X_upgrade2018_realistic_v15-v1_MINIAODSIM/2021-07-22_15-54-05/ntupleTree_1.root:treeMaker/tree",
#"/nfs/dust/cms/user/sobhatta/work/TopTagPol/Training/training_results/classifier_trees/from-Hala_CNN1_5cat_2021-10-02_17-50-33/QCD_Pt_170to300_TuneCP5_13TeV_pythia8_RunIIAutumn18MiniAOD-PREMIX_RECODEBUG_102X_upgrade2018_realistic_v15-v1_MINIAODSIM_2021-07-22_15-54-05/ntupleTree_1.root:tree",
]


arr = uproot.concatenate(l_file, ["jet_selectedPatJetsAK15PFPuppi_boost_2_1_sd_0p1_0_1_pT_reco"])
#arr = uproot.concatenate(l_file, ["jet_selectedPatJetsAK15PFPuppi_boost_2_1_sd_0p1_0_1_pT_reco", "epoch50_0vs2"], allow_missing = True)

print(arr)
