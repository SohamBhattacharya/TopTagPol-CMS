import numpy
import ROOT
import root_numpy
import uproot


l_file_1 = [
"/pnfs/desy.de/cms/tier2/store/user/sobhatta/TopTagPol/ntuples/QCD_Pt_170to300_TuneCP5_13TeV_pythia8_RunIIAutumn18MiniAOD-PREMIX_RECODEBUG_102X_upgrade2018_realistic_v15-v1_MINIAODSIM/2021-07-22_15-54-05/ntupleTree_1.root",
]

l_file_2 = [
"/nfs/dust/cms/user/sobhatta/work/TopTagPol/Training/training_results/classifier_trees/from-Hala_CNN1_5cat_2021-10-02_17-50-33/QCD_Pt_170to300_TuneCP5_13TeV_pythia8_RunIIAutumn18MiniAOD-PREMIX_RECODEBUG_102X_upgrade2018_realistic_v15-v1_MINIAODSIM_2021-07-22_15-54-05/ntupleTree_1.root",
]

tree1 = ROOT.TChain("treeMaker/tree")

for f in l_file_1 :
    tree1.Add(f)

tree2 = ROOT.TChain("tree")

for f in l_file_2 :
    tree2.Add(f)

tree1.AddFriend(tree2)

#tree1.SetWeight(2)

print("Created chains.")

#arr = uproot.concatenate(l_file, ["jet_selectedPatJetsAK15PFPuppi_boost_2_1_sd_0p1_0_1_pT_reco"])
#arr = uproot.concatenate(l_file, ["jet_selectedPatJetsAK15PFPuppi_boost_2_1_sd_0p1_0_1_pT_reco", "epoch50_0vs2"], allow_missing = True)

#print(arr)


#uproot_tree = uproot.pyroot.from_pyroot(tree1)
#print(uproot_tree)


#for arr in uproot.iterate(tree1) :
#    
#    print(arr.keys())

#arr = root_numpy.tree2array(
#    tree1,
#    branches = ["jet_selectedPatJetsAK15PFPuppi_boost_2_1_sd_0p1_0_1_pT_reco", "epoch50_0vs2"],
#    selection = "1",
#    #start=0, stop=10, step=2
#)
#print(arr)


rdframe_orig = ROOT.RDataFrame(tree1)

cut_func = "for (auto x : epoch50_0vs2) { if(x > 0.1) return true; } return false;"

#rdframe = rdframe_orig.Define("cut", "epoch50_0vs2 > 0.1 && rho > 15")
rdframe = rdframe_orig.Define("cut", "epoch50_0vs2 > 0.1")

#cols = rdframe.AsNumpy(["jet_selectedPatJetsAK15PFPuppi_boost_2_1_sd_0p1_0_1_pT_reco", "epoch50_0vs2", "cut", "rho"])
#cols = rdframe.AsNumpy(["jet_selectedPatJetsAK15PFPuppi_boost_2_1_sd_0p1_0_1_pT_reco", "epoch50_0vs2"])
#cols = rdframe.Filter(cut_func).AsNumpy(["jet_selectedPatJetsAK15PFPuppi_boost_2_1_sd_0p1_0_1_pT_reco", "epoch50_0vs2", "rho", "cut"])
cols = rdframe.Filter(cut_func).AsNumpy(["jet_selectedPatJetsAK15PFPuppi_boost_2_1_sd_0p1_0_1_pT_reco", "epoch50_0vs2", "rho", "cut"])
#cols = rdframe.Filter("! epoch50_0vs2[epoch50_0vs2 > 0.1].empty()").AsNumpy(["jet_selectedPatJetsAK15PFPuppi_boost_2_1_sd_0p1_0_1_pT_reco", "epoch50_0vs2"])

print(cols["jet_selectedPatJetsAK15PFPuppi_boost_2_1_sd_0p1_0_1_pT_reco"], type(cols["jet_selectedPatJetsAK15PFPuppi_boost_2_1_sd_0p1_0_1_pT_reco"]))
print(numpy.asarray(cols["epoch50_0vs2"][0]))
print(numpy.asarray(cols["cut"][0]))
print(numpy.asarray(cols["rho"]))
##print(numpy.stack(cols["cut"]))

#print(numpy.asarray([numpy.asarray(entry) for entry in cols["epoch50_0vs2"]]))

print(numpy.asarray(cols["cut"] == 1).shape)

#print(numpy.concatenate([numpy.asarray(e) for e in cols["epoch50_0vs2"]]))

#rdframe = rdframe.Define("var1", "epoch50_0vs2[cut]")
#cols = rdframe.AsNumpy(["var1"])
#print(cols["var1"].Sum())


print(rdframe.Sum("cut"))
print(rdframe.Sum("cut").GetValue())
#print(rdframe.Sum("w").GetValue())
