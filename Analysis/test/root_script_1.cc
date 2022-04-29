int root_script_1()
{
    std::string fnameL = "/home/soham/naf_dust/work/TopTagPol/TreeMaker/CMSSW_10_5_0/src/output/ntupleTree_Wprimetotb_M3000W30_LH.root";
    std::string fnameR = "/home/soham/naf_dust/work/TopTagPol/TreeMaker/CMSSW_10_5_0/src/output/ntupleTree_Wprimetotb_M3000W30_RH.root";
    std::string fnamettbar = "/home/soham/naf_dust/work/TopTagPol/TreeMaker/CMSSW_10_5_0/src/output/ntupleTree_TTJets_HT-800to1200.root";
    
    TFile *fL = (TFile*) TFile::Open(fnameL.c_str());
    TFile *fR = (TFile*) TFile::Open(fnameR.c_str());
    TFile *fttbar = (TFile*) TFile::Open(fnamettbar.c_str());

    TTree *treeL = (TTree*) fL->Get("treeMaker/tree");
}
