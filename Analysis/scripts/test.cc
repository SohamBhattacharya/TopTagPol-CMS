
//#include <boost/algorithm/string/join.hpp>

#include <cstdlib>
#include <iostream>
#include <map>
#include <string>


int openTChain(std::vector <std::string> v_fileList, TChain *chain, int nFileMax = -1)
{
    //std::ifstream inFileList;
    //inFileList.open(listFileName.c_str());
    //
    //std::string inFileName;
    //
    ////TChain *chain = new TChain(treeName.c_str());
    
    int nFile = 0;
    
    //while(std::getline(inFileList, inFileName))
    for(const auto inFileName : v_fileList)
    {
        char inFileName_mod[1000];
        
        // Commented out lines
        if(inFileName.find("#") == 0)
        {
            continue;
        }
        
        if(inFileName.find("/eos/cms") == 0)
        {
            sprintf(inFileName_mod, "root://eoscms.cern.ch/%s", inFileName.c_str());
        }
        
        else
        {
            sprintf(inFileName_mod, "%s", inFileName.c_str());
        }
        
        printf("Checking file: %s \n", inFileName_mod);
        TFile *inFile = (TFile*) TFile::Open(inFileName_mod);
        
        if(inFile && !inFile->IsZombie())
        {
            printf("Adding to chain...\n");
            
            //v_inFile.push_back(inFile);
            
            chain->Add(inFileName_mod);
            
            inFile->Close();
            
            nFile++;
        }
        
        if(nFileMax > 0 && nFile >= nFileMax)
        {
            break;
        }
    }
    
    
    return 0;
}

int test()
{
    //std::vector <std::string> v_fileList1 = {
    //    "/home/soham/desy_dcache/TopTagPol/ntuples/ZprimeToTT_M2000_W20_TuneCP2_PSweights_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM/2021-07-22_15-56-51/ntupleTree_1.root",
    //    "/home/soham/desy_dcache/TopTagPol/ntuples/ZprimeToTT_M2000_W20_TuneCP2_PSweights_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM/2021-07-22_15-56-51/ntupleTree_2.root",
    //};
    //
    //std::vector <std::string> v_fileList2 = {
    //    "/home/soham/naf_dust/work/TopTagPol/Training/training_results/classifier_trees/from-Hala_CNN1_5cat_2021-10-02_17-50-33/ZprimeToTT_M2000_W20_TuneCP2_PSweights_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM_2021-07-22_15-56-51/ntupleTree_1.root",
    //    "/home/soham/naf_dust/work/TopTagPol/Training/training_results/classifier_trees/from-Hala_CNN1_5cat_2021-10-02_17-50-33/ZprimeToTT_M2000_W20_TuneCP2_PSweights_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM_2021-07-22_15-56-51/ntupleTree_2.root",
    //};
    
    
    std::vector <std::string> v_fileList1 = {
        "/home/soham/desy_dcache/TopTagPol/ntuples/QCD_Pt_470to600_TuneCP5_13TeV_pythia8_RunIIAutumn18MiniAOD-PREMIX_RECODEBUG_102X_upgrade2018_realistic_v15_ext1-v1_MINIAODSIM/2021-07-22_15-54-16/ntupleTree_1.root",
        "/home/soham/desy_dcache/TopTagPol/ntuples/QCD_Pt_470to600_TuneCP5_13TeV_pythia8_RunIIAutumn18MiniAOD-PREMIX_RECODEBUG_102X_upgrade2018_realistic_v15_ext1-v1_MINIAODSIM/2021-07-22_15-54-16/ntupleTree_2.root",
    };
    
    std::vector <std::string> v_fileList2 = {
        "/home/soham/naf_dust/work/TopTagPol/Training/training_results/classifier_trees/from-Hala_CNN1_5cat_2021-10-02_17-50-33/QCD_Pt_470to600_TuneCP5_13TeV_pythia8_RunIIAutumn18MiniAOD-PREMIX_RECODEBUG_102X_upgrade2018_realistic_v15_ext1-v1_MINIAODSIM_2021-07-22_15-54-16/ntupleTree_1.root",
        "/home/soham/naf_dust/work/TopTagPol/Training/training_results/classifier_trees/from-Hala_CNN1_5cat_2021-10-02_17-50-33/QCD_Pt_470to600_TuneCP5_13TeV_pythia8_RunIIAutumn18MiniAOD-PREMIX_RECODEBUG_102X_upgrade2018_realistic_v15_ext1-v1_MINIAODSIM_2021-07-22_15-54-16/ntupleTree_2.root",
    };
    
    //std::string str_fileList1 = boost::algorithm::join(v_fileList1, "\n");
    //std::string str_fileList2 = boost::algorithm::join(v_fileList2, "\n");
    
    
    TChain *ch1 = new TChain("treeMaker/tree");
    TChain *ch2 = new TChain("tree");
    
    openTChain(v_fileList1, ch1);
    openTChain(v_fileList2, ch2);
    
    ch1->AddFriend(ch2);
    
    
    TCanvas *canvas = new TCanvas("canvas");
    
    //ch1->Draw(
    //    "epoch50_0vs2 : jet_selectedPatJetsAK15PFPuppi_boost_2_1_sd_0p1_0_1_m_reco",
    //    "(jet_selectedPatJetsAK15PFPuppi_boost_2_1_sd_0p1_0_1_pT_reco > 200) && (fabs(jet_selectedPatJetsAK15PFPuppi_boost_2_1_sd_0p1_0_1_eta_reco) < 2.5) && (jet_selectedPatJetsAK15PFPuppi_boost_2_1_sd_0p1_0_1_nConsti_reco >= 3) && (jet_selectedPatJetsAK15PFPuppi_boost_2_1_sd_0p1_0_1_nearestGenTopDR_reco > 1)",
    //    "colz norm"
    //);
    
    ch1->Draw(
        "jet_selectedPatJetsAK15PFPuppi_boost_2_1_sd_0p1_0_1_m_reco",
        "(epoch50_0vs2 > 0.5) && (jet_selectedPatJetsAK15PFPuppi_boost_2_1_sd_0p1_0_1_pT_reco > 200) && (fabs(jet_selectedPatJetsAK15PFPuppi_boost_2_1_sd_0p1_0_1_eta_reco) < 2.5) && (jet_selectedPatJetsAK15PFPuppi_boost_2_1_sd_0p1_0_1_nConsti_reco >= 3) && (jet_selectedPatJetsAK15PFPuppi_boost_2_1_sd_0p1_0_1_nearestGenTopDR_reco > 1)",
        "colz norm"
    );
    
    
    return 0;
}
