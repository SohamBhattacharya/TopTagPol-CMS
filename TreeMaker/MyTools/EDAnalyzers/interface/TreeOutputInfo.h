# ifndef TreeOutputInfo_H
# define TreeOutputInfo_H


# include "CommonTools/UtilAlgos/interface/TFileService.h"
# include "DataFormats/CaloTowers/interface/CaloTowerDefs.h"
# include "DataFormats/Common/interface/MapOfVectors.h"
# include "DataFormats/EcalRecHit/interface/EcalRecHit.h"
# include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
# include "DataFormats/EgammaCandidates/interface/Photon.h"
# include "DataFormats/FWLite/interface/ESHandle.h"
# include "DataFormats/GsfTrackReco/interface/GsfTrack.h"
# include "DataFormats/HepMCCandidate/interface/GenParticle.h"
# include "DataFormats/JetReco/interface/PFJet.h"
# include "DataFormats/Math/interface/LorentzVector.h"
# include "DataFormats/ParticleFlowReco/interface/PFRecHit.h"
# include "DataFormats/PatCandidates/interface/Jet.h"
# include "DataFormats/PatCandidates/interface/MET.h"
# include "DataFormats/PatCandidates/interface/Muon.h"
# include "DataFormats/PatCandidates/interface/Electron.h"
# include "DataFormats/PatCandidates/interface/Photon.h"
# include "DataFormats/PatCandidates/interface/PackedGenParticle.h"
# include "DataFormats/RecoCandidate/interface/RecoCandidate.h"
# include "DataFormats/TrackReco/interface/Track.h"
# include "DataFormats/TrackReco/interface/TrackFwd.h"
# include "DataFormats/VertexReco/interface/Vertex.h"
# include "FWCore/Framework/interface/ConsumesCollector.h"
# include "FWCore/Framework/interface/Event.h"
# include "FWCore/Framework/interface/ESHandle.h"
# include "FWCore/Framework/interface/Frameworkfwd.h"
# include "FWCore/Framework/interface/MakerMacros.h"
# include "FWCore/Framework/interface/one/EDAnalyzer.h"
# include "FWCore/ParameterSet/interface/ParameterSet.h"
# include "FWCore/ServiceRegistry/interface/Service.h"
# include "FWCore/Utilities/interface/InputTag.h"
# include "Geometry/Records/interface/CaloGeometryRecord.h"
# include "Geometry/Records/interface/IdealGeometryRecord.h"
# include "RecoVertex/VertexTools/interface/VertexDistance3D.h"
# include "SimDataFormats/CaloAnalysis/interface/CaloParticle.h"
# include "SimDataFormats/CaloAnalysis/interface/SimCluster.h"
# include "SimDataFormats/CaloHit/interface/PCaloHit.h"
# include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
# include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"

# include <algorithm>
# include <iostream>
# include <map>
# include <stdlib.h>
# include <string>
# include <type_traits>
# include <utility>
# include <vector>

# include <TH1F.h>
# include <TH2F.h>
# include <TMatrixD.h>
# include <TROOT.h>
# include <TTree.h> 
# include <TVectorD.h> 

# include "MyTools/EDAnalyzers/interface/Constants.h"


namespace TreeOutputInfo
{
    /*class GenParticleInfo
    {
        public :
        
        int n;
        std::vector <double> v_id;
        std::vector <double> v_E;
        std::vector <double> v_px;
        std::vector <double> v_py;
        std::vector <double> v_pz;
        std::vector <double> v_pT;
        std::vector <double> v_eta;
        std::vector <double> v_y;
        std::vector <double> v_phi;
        std::vector <double> v_m;
        
        std::vector <double> v_isLeptonic;
        
        
        GenParticleInfo(std::string tag)
        {
            char name[2000];
            
            sprintf(name, "%s_n", tag.c_str());
            tree->Branch(name, &genTop_n);
            
            sprintf(name, "%s_id", tag.c_str());
            tree->Branch(name, &v_id);
            
            sprintf(name, "%s_E", tag.c_str());
            tree->Branch(name, &v_E);
            
            sprintf(name, "%s_px", tag.c_str());
            tree->Branch(name, &v_px);
            
            sprintf(name, "%s_py", tag.c_str());
            tree->Branch(name, &v_py);
            
            sprintf(name, "%s_pz", tag.c_str());
            tree->Branch(name, &v_pz);
            
            sprintf(name, "%s_pT", tag.c_str());
            tree->Branch(name, &v_pT);
            
            sprintf(name, "%s_eta", tag.c_str());
            tree->Branch(name, &v_eta);
            
            sprintf(name, "%s_y", tag.c_str());
            tree->Branch(name, &v_y);
            
            sprintf(name, "%s_phi", tag.c_str());
            tree->Branch(name, &v_phi);
            
            sprintf(name, "%s_m", tag.c_str());
            tree->Branch(name, &v_m);
            
            sprintf(name, "%s_isLeptonic", tag.c_str());
            tree->Branch(name, &v_isLeptonic);
        }
        
        
        void fill(
            const reco::GenParticle *part,
            
            
        )
        {
            v_genTop_id.push_back(Common::LARGEVAL_NEG);;
            v_genTop_E.push_back(Common::LARGEVAL_NEG);;
            v_genTop_px.push_back(Common::LARGEVAL_NEG);;
            v_genTop_py.push_back(Common::LARGEVAL_NEG);;
            v_genTop_pz.push_back(Common::LARGEVAL_NEG);;
            v_genTop_pT.push_back(Common::LARGEVAL_NEG);;
            v_genTop_eta.push_back(Common::LARGEVAL_NEG);;
            v_genTop_y.push_back(Common::LARGEVAL_NEG);;
            v_genTop_phi.push_back(Common::LARGEVAL_NEG);;
            v_genTop_m.push_back(Common::LARGEVAL_NEG);;
            v_genTop_isLeptonic.push_back(Common::LARGEVAL_NEG);;
            
            if(part)
            {
                v_id.at(n) = part->pdgId();
                v_E.at(n) = part->energy();
                v_px.at(n) = part->px();
                v_py.at(n) = part->py();
                v_pz.at(n) = part->pz();
                v_pT.at(n) = part->pt();
                v_eta.at(n) = part->eta();
                v_y.at(n) = part->y();
                v_phi.at(n) = part->phi();
                v_m.at(n) = part->mass();
            }
            
            n++;
        }
        
        
        void clear()
        {
            n = 0;
            v_id.clear();
            v_E.clear();
            v_px.clear();
            v_py.clear();
            v_pz.clear();
            v_pT.clear();
            v_eta.clear();
            v_y.clear();
            v_phi.clear();
            v_m.clear();
            v_isLeptonic.clear();
        }
    };*/
    
    class JetInfo
    {
        public :
        
        edm::InputTag tag_jet;
        edm::EDGetTokenT <std::vector <pat::Jet> > tok_jet;
        
        double rParam;
        
        double minPt;
        
        double jetRescale_m0;
        std::string str_jetRescale_m0;
        
        double jetLorentzBoost_e0;
        std::string str_jetLorentzBoost_e0;
        
        double jetLorentzBoost_p0;
        
        bool apply_sd;
        
        double sd_zcut;
        std::string str_sd_zcut;
        
        double sd_beta;
        std::string str_sd_beta;
        
        double sd_R0;
        std::string str_sd_R0;
        
        int maxTauN;
        
        std::string str_jetName;
        
        
        int jet_n_reco;
        
        std::vector <double> v_jet_raw_E_reco;
        std::vector <double> v_jet_raw_px_reco;
        std::vector <double> v_jet_raw_py_reco;
        std::vector <double> v_jet_raw_pz_reco;
        std::vector <double> v_jet_raw_pT_reco;
        std::vector <double> v_jet_raw_eta_reco;
        std::vector <double> v_jet_raw_y_reco;
        std::vector <double> v_jet_raw_phi_reco;
        std::vector <double> v_jet_raw_m_reco;
        
        std::vector <double> v_jet_E_reco;
        std::vector <double> v_jet_px_reco;
        std::vector <double> v_jet_py_reco;
        std::vector <double> v_jet_pz_reco;
        std::vector <double> v_jet_pT_reco;
        std::vector <double> v_jet_eta_reco;
        std::vector <double> v_jet_y_reco;
        std::vector <double> v_jet_phi_reco;
        std::vector <double> v_jet_m_reco;
        
        std::vector <double> v_jet_nearestGenTopIdx_reco;
        std::vector <double> v_jet_nearestGenTopDR_reco;
        std::vector <double> v_jet_nearestGenTopbDR_reco;
        std::vector <double> v_jet_nearestGenTopWlepDR_reco;
        std::vector <double> v_jet_nearestGenTopWq1DR_reco;
        std::vector <double> v_jet_nearestGenTopWq2DR_reco;
        std::vector <double> v_jet_nearestGenTopIsLeptonic_reco;
        
        std::vector <double> v_jet_nearestGenWIdx_reco;
        std::vector <double> v_jet_nearestGenWDR_reco;
        std::vector <double> v_jet_nearestGenWlepDR_reco;
        std::vector <double> v_jet_nearestGenWq1DR_reco;
        std::vector <double> v_jet_nearestGenWq2DR_reco;
        std::vector <double> v_jet_nearestGenWIsLeptonic_reco;
        
        std::vector <double> v_jet_nearestGenZIdx_reco;
        std::vector <double> v_jet_nearestGenZDR_reco;
        std::vector <double> v_jet_nearestGenZlep1DR_reco;
        std::vector <double> v_jet_nearestGenZlep2DR_reco;
        std::vector <double> v_jet_nearestGenZq1DR_reco;
        std::vector <double> v_jet_nearestGenZq2DR_reco;
        std::vector <double> v_jet_nearestGenZIsLeptonic_reco;
        
        std::vector <double> v_jet_nSecVtxInJet_reco;
        
        std::vector <std::vector <double> > vv_jet_sv_pT_reco;
        std::vector <std::vector <double> > vv_jet_sv_eta_reco;
        std::vector <std::vector <double> > vv_jet_sv_phi_reco;
        std::vector <std::vector <double> > vv_jet_sv_m_reco;
        std::vector <std::vector <double> > vv_jet_sv_E_reco;
        std::vector <std::vector <double> > vv_jet_sv_etarel_reco;
        std::vector <std::vector <double> > vv_jet_sv_phirel_reco;
        std::vector <std::vector <double> > vv_jet_sv_deltaR_reco;
        std::vector <std::vector <double> > vv_jet_sv_ntracks_reco;
        std::vector <std::vector <double> > vv_jet_sv_chi2_reco;
        std::vector <std::vector <double> > vv_jet_sv_ndf_reco;
        std::vector <std::vector <double> > vv_jet_sv_normchi2_reco;
        std::vector <std::vector <double> > vv_jet_sv_dxy_reco;
        std::vector <std::vector <double> > vv_jet_sv_dxyerr_reco;
        std::vector <std::vector <double> > vv_jet_sv_dxysig_reco;
        std::vector <std::vector <double> > vv_jet_sv_d3d_reco;
        std::vector <std::vector <double> > vv_jet_sv_d3derr_reco;
        std::vector <std::vector <double> > vv_jet_sv_d3dsig_reco;
        std::vector <std::vector <double> > vv_jet_sv_costhetasvpv_reco;
        
        std::vector <std::vector <double> >  vv_jet_tauN_reco;
        std::vector <std::vector <double> >  vv_jet_tauNratio_reco;
        
        std::vector <double> v_jet_nConsti_reco;
        std::vector <double> v_jet_nMatchedEl_reco;
        std::vector <double> v_jet_nMatchedMu_reco;
        
        std::vector <std::vector <double> > vv_jet_consti_E_reco;
        std::vector <std::vector <double> > vv_jet_consti_px_reco;
        std::vector <std::vector <double> > vv_jet_consti_py_reco;
        std::vector <std::vector <double> > vv_jet_consti_pz_reco;
        std::vector <std::vector <double> > vv_jet_consti_pT_reco;
        std::vector <std::vector <double> > vv_jet_consti_eta_reco;
        std::vector <std::vector <double> > vv_jet_consti_phi_reco;
        std::vector <std::vector <double> > vv_jet_consti_m_reco;
        
        std::vector <std::vector <double> > vv_jet_consti_id_reco;
        
        std::vector <std::vector <double> > vv_jet_consti_vx_reco;
        std::vector <std::vector <double> > vv_jet_consti_vy_reco;
        std::vector <std::vector <double> > vv_jet_consti_vz_reco;
        std::vector <std::vector <double> > vv_jet_consti_v2d_reco;
        std::vector <std::vector <double> > vv_jet_consti_v3d_reco;
        
        std::vector <std::vector <double> > vv_jet_consti_pvdxy_reco;
        std::vector <std::vector <double> > vv_jet_consti_pvdz_reco;
        
        std::vector <std::vector <double> > vv_jet_consti_svdxy_reco;
        std::vector <std::vector <double> > vv_jet_consti_svdz_reco;
        
        std::vector <std::vector <double> > vv_jet_consti_dEta_reco;
        std::vector <std::vector <double> > vv_jet_consti_dPhi_reco;
        
        std::vector <std::vector <double> > vv_jet_consti_EtaPhiRot_dEta_reco;
        std::vector <std::vector <double> > vv_jet_consti_EtaPhiRot_dPhi_reco;
        
        std::vector <std::vector <double> > vv_jet_consti_LBGS_x_reco;
        std::vector <std::vector <double> > vv_jet_consti_LBGS_y_reco;
        
        std::vector <std::vector <double> > vv_jet_consti_enFrac_reco;
        
        std::vector <std::vector <double> > vv_jet_consti_pTwrtJet_reco;
        std::vector <std::vector <double> > vv_jet_consti_dRwrtJet_reco;
        
        std::unordered_map <std::string, std::vector <std::vector <double> > > m_jet_consti_electronInfo_reco;
        std::unordered_map <std::string, std::vector <std::vector <double> > > m_jet_consti_muonInfo_reco;
        
        
        JetInfo(const edm::ParameterSet &jetPSet, edm::ConsumesCollector &ccollector)
        {
            tag_jet = jetPSet.getParameter <edm::InputTag>("jetCollection");
            tok_jet = ccollector.consumes <std::vector <pat::Jet> >(tag_jet);
            
            
            rParam = jetPSet.getParameter <double>("rParam");
            
            // Kinematic cut
            minPt = jetPSet.getParameter <double>("minPt");
            
            
            // Preprocessing
            str_jetRescale_m0 = jetPSet.getParameter <std::string>("jetRescale_m0").c_str();
            jetRescale_m0 = std::stod(str_jetRescale_m0);
            std::replace(str_jetRescale_m0.begin(), str_jetRescale_m0.end(), '.', 'p');
            
            str_jetLorentzBoost_e0 = jetPSet.getParameter <std::string>("jetLorentzBoost_e0").c_str();
            jetLorentzBoost_e0 = std::stod(str_jetLorentzBoost_e0);
            std::replace(str_jetLorentzBoost_e0.begin(), str_jetLorentzBoost_e0.end(), '.', 'p');
            
            jetLorentzBoost_p0 = std::sqrt(jetLorentzBoost_e0*jetLorentzBoost_e0 - jetRescale_m0*jetRescale_m0);
            
            
            // Soft drop
            apply_sd = jetPSet.getParameter <bool>("apply_sd");
            
            str_sd_zcut = jetPSet.getParameter <std::string>("sd_zcut").c_str();
            sd_zcut = std::stod(str_sd_zcut);
            std::replace(str_sd_zcut.begin(), str_sd_zcut.end(), '.', 'p');
            
            str_sd_beta = jetPSet.getParameter <std::string>("sd_beta").c_str();
            sd_beta = std::stod(str_sd_beta);
            std::replace(str_sd_beta.begin(), str_sd_beta.end(), '.', 'p');
            
            str_sd_R0 = jetPSet.getParameter <std::string>("sd_R0").c_str();
            sd_R0 = std::stod(str_sd_R0);
            std::replace(str_sd_R0.begin(), str_sd_R0.end(), '.', 'p');
            
            
            // N-subjettiness
            maxTauN = jetPSet.getParameter <int>("maxTauN");
            
            
            char jetName[1000];
            
            sprintf(
                jetName,
                "%s_"
                "boost_%s_%s"
                ,
                tag_jet.encode().c_str(),
                str_jetLorentzBoost_e0.c_str(), str_jetRescale_m0.c_str()
            );
            
            if(apply_sd)
            {
                sprintf(
                    jetName,
                    "%s_"
                    "sd_z%s_b%s_R%s"
                    ,
                    jetName,
                    str_sd_zcut.c_str(), str_sd_beta.c_str(), str_sd_R0.c_str()
                );
            }
            
            
            str_jetName = jetName;
        }
        
        
        void createBranches(TTree *tree)
        {
            char brName[2000];
            
            sprintf(brName, "jet_%s_n_reco", str_jetName.c_str());
            tree->Branch(brName, &jet_n_reco);
            
            //
            sprintf(brName, "jet_%s_raw_E_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_raw_E_reco);
            
            sprintf(brName, "jet_%s_raw_px_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_raw_px_reco);
            
            sprintf(brName, "jet_%s_raw_py_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_raw_py_reco);
            
            sprintf(brName, "jet_%s_raw_pz_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_raw_pz_reco);
            
            sprintf(brName, "jet_%s_raw_pT_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_raw_pT_reco);
            
            sprintf(brName, "jet_%s_raw_eta_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_raw_eta_reco);
            
            sprintf(brName, "jet_%s_raw_y_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_raw_y_reco);
            
            sprintf(brName, "jet_%s_raw_phi_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_raw_phi_reco);
            
            sprintf(brName, "jet_%s_raw_m_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_raw_m_reco);
            
            //
            sprintf(brName, "jet_%s_E_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_E_reco);
            
            sprintf(brName, "jet_%s_px_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_px_reco);
            
            sprintf(brName, "jet_%s_py_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_py_reco);
            
            sprintf(brName, "jet_%s_pz_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_pz_reco);
            
            sprintf(brName, "jet_%s_pT_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_pT_reco);
            
            sprintf(brName, "jet_%s_eta_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_eta_reco);
            
            sprintf(brName, "jet_%s_y_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_y_reco);
            
            sprintf(brName, "jet_%s_phi_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_phi_reco);
            
            sprintf(brName, "jet_%s_m_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_m_reco);
            
            //
            sprintf(brName, "jet_%s_nearestGenTopIdx_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_nearestGenTopIdx_reco);
            
            sprintf(brName, "jet_%s_nearestGenTopDR_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_nearestGenTopDR_reco);
            
            sprintf(brName, "jet_%s_nearestGenTopbDR_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_nearestGenTopbDR_reco);
            
            sprintf(brName, "jet_%s_nearestGenTopWlepDR_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_nearestGenTopWlepDR_reco);
            
            sprintf(brName, "jet_%s_nearestGenTopWq1DR_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_nearestGenTopWq1DR_reco);
            
            sprintf(brName, "jet_%s_nearestGenTopWq2DR_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_nearestGenTopWq2DR_reco);
            
            sprintf(brName, "jet_%s_nearestGenTopIsLeptonic_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_nearestGenTopIsLeptonic_reco);
            
            //
            sprintf(brName, "jet_%s_nearestGenWIdx_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_nearestGenWIdx_reco);
            
            sprintf(brName, "jet_%s_nearestGenWDR_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_nearestGenWDR_reco);
            
            sprintf(brName, "jet_%s_nearestGenWlepDR_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_nearestGenWlepDR_reco);
            
            sprintf(brName, "jet_%s_nearestGenWq1DR_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_nearestGenWq1DR_reco);
            
            sprintf(brName, "jet_%s_nearestGenWq2DR_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_nearestGenWq2DR_reco);
            
            sprintf(brName, "jet_%s_nearestGenWIsLeptonic_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_nearestGenWIsLeptonic_reco);
            
            //
            sprintf(brName, "jet_%s_nearestGenZIdx_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_nearestGenZIdx_reco);
            
            sprintf(brName, "jet_%s_nearestGenZDR_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_nearestGenZDR_reco);
            
            sprintf(brName, "jet_%s_nearestGenZlep1DR_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_nearestGenZlep1DR_reco);
            
            sprintf(brName, "jet_%s_nearestGenZlep2DR_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_nearestGenZlep2DR_reco);
            
            sprintf(brName, "jet_%s_nearestGenZq1DR_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_nearestGenZq1DR_reco);
            
            sprintf(brName, "jet_%s_nearestGenZq2DR_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_nearestGenZq2DR_reco);
            
            sprintf(brName, "jet_%s_nearestGenZIsLeptonic_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_nearestGenZIsLeptonic_reco);
            
            //
            sprintf(brName, "jet_%s_nSecVtxInJet_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_nSecVtxInJet_reco);
            
            sprintf(brName, "jet_%s_sv_pT_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_sv_pT_reco);
            
            sprintf(brName, "jet_%s_sv_eta_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_sv_eta_reco);
            
            sprintf(brName, "jet_%s_sv_phi_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_sv_phi_reco);
            
            sprintf(brName, "jet_%s_sv_m_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_sv_m_reco);
            
            sprintf(brName, "jet_%s_sv_E_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_sv_E_reco);
            
            sprintf(brName, "jet_%s_sv_etarel_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_sv_etarel_reco);
            
            sprintf(brName, "jet_%s_sv_phirel_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_sv_phirel_reco);
            
            sprintf(brName, "jet_%s_sv_deltaR_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_sv_deltaR_reco);
            
            sprintf(brName, "jet_%s_sv_ntracks_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_sv_ntracks_reco);
            
            sprintf(brName, "jet_%s_sv_chi2_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_sv_chi2_reco);
            
            sprintf(brName, "jet_%s_sv_ndf_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_sv_ndf_reco);
            
            sprintf(brName, "jet_%s_sv_normchi2_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_sv_normchi2_reco);
            
            sprintf(brName, "jet_%s_sv_dxy_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_sv_dxy_reco);
            
            sprintf(brName, "jet_%s_sv_dxyerr_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_sv_dxyerr_reco);
            
            sprintf(brName, "jet_%s_sv_dxysig_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_sv_dxysig_reco);
            
            sprintf(brName, "jet_%s_sv_d3d_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_sv_d3d_reco);
            
            sprintf(brName, "jet_%s_sv_d3derr_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_sv_d3derr_reco);
            
            sprintf(brName, "jet_%s_sv_d3dsig_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_sv_d3dsig_reco);
            
            sprintf(brName, "jet_%s_sv_costhetasvpv_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_sv_costhetasvpv_reco);
            
            
            //
            vv_jet_tauN_reco.resize(maxTauN+1, {});
            vv_jet_tauNratio_reco.resize(maxTauN+1, {});
            
            for(int iTauN = 0; iTauN <= maxTauN; iTauN++)
            {
                sprintf(brName, "jet_%s_tau%d_reco", str_jetName.c_str(), iTauN);
                tree->Branch(brName, &vv_jet_tauN_reco.at(iTauN));
                
                sprintf(brName, "jet_%s_tau%dratio_reco", str_jetName.c_str(), iTauN);
                tree->Branch(brName, &vv_jet_tauNratio_reco.at(iTauN));
            }
            
            
            //
            sprintf(brName, "jet_%s_nConsti_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_nConsti_reco);
            
            sprintf(brName, "jet_%s_nMatchedEl_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_nMatchedEl_reco);
            
            sprintf(brName, "jet_%s_nMatchedMu_reco", str_jetName.c_str());
            tree->Branch(brName, &v_jet_nMatchedMu_reco);
            
            //
            sprintf(brName, "jet_%s_consti_E_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_consti_E_reco);
            
            sprintf(brName, "jet_%s_consti_px_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_consti_px_reco);
            
            sprintf(brName, "jet_%s_consti_py_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_consti_py_reco);
            
            sprintf(brName, "jet_%s_consti_pz_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_consti_pz_reco);
            
            sprintf(brName, "jet_%s_consti_pT_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_consti_pT_reco);
            
            sprintf(brName, "jet_%s_consti_eta_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_consti_eta_reco);
            
            sprintf(brName, "jet_%s_consti_phi_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_consti_phi_reco);
            
            sprintf(brName, "jet_%s_consti_m_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_consti_m_reco);
            
            //
            sprintf(brName, "jet_%s_consti_id_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_consti_id_reco);
            
            //
            sprintf(brName, "jet_%s_consti_vx_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_consti_vx_reco);
            
            sprintf(brName, "jet_%s_consti_vy_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_consti_vy_reco);
            
            sprintf(brName, "jet_%s_consti_vz_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_consti_vz_reco);
            
            sprintf(brName, "jet_%s_consti_v2d_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_consti_v2d_reco);
            
            sprintf(brName, "jet_%s_consti_v3d_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_consti_v3d_reco);
            
            //
            sprintf(brName, "jet_%s_consti_pvdxy_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_consti_pvdxy_reco);
            
            sprintf(brName, "jet_%s_consti_pvdz_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_consti_pvdz_reco);
            
            //
            sprintf(brName, "jet_%s_consti_svdxy_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_consti_svdxy_reco);
            
            sprintf(brName, "jet_%s_consti_svdz_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_consti_svdz_reco);
            
            //
            sprintf(brName, "jet_%s_consti_dEta_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_consti_dEta_reco);
            
            sprintf(brName, "jet_%s_consti_dPhi_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_consti_dPhi_reco);
            
            //
            sprintf(brName, "jet_%s_consti_EtaPhiRot_dEta_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_consti_EtaPhiRot_dEta_reco);
            
            sprintf(brName, "jet_%s_consti_EtaPhiRot_dPhi_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_consti_EtaPhiRot_dPhi_reco);
            
            //
            sprintf(brName, "jet_%s_consti_LBGS_x_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_consti_LBGS_x_reco);
            
            sprintf(brName, "jet_%s_consti_LBGS_y_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_consti_LBGS_y_reco);
            
            //
            sprintf(brName, "jet_%s_consti_enFrac_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_consti_enFrac_reco);
            
            //
            sprintf(brName, "jet_%s_consti_pTwrtJet_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_consti_pTwrtJet_reco);
            
            sprintf(brName, "jet_%s_consti_dRwrtJet_reco", str_jetName.c_str());
            tree->Branch(brName, &vv_jet_consti_dRwrtJet_reco);
        }
        
        
        void createElectronBranches(TTree *tree, const MVAVariableManager <pat::Electron> &eleMvaVarManager)
        {
            for(int iVar = 0; iVar < eleMvaVarManager.getNVars(); iVar++)
            {
                char brName[2000];
                sprintf(brName, "jet_%s_consti_%s_reco", str_jetName.c_str(), eleMvaVarManager.getName(iVar).c_str());
                
                std::string varName = eleMvaVarManager.getName(iVar);
                
                std::vector <std::vector <double> > v_temp;
                m_jet_consti_electronInfo_reco[varName] = v_temp;
                
                tree->Branch(brName, &m_jet_consti_electronInfo_reco[varName]);
            }
        }
        
        
        void createMuonBranches(TTree *tree, const MVAVariableManager <pat::Muon> &muMvaVarManager)
        {
            for(int iVar = 0; iVar < muMvaVarManager.getNVars(); iVar++)
            {
                char brName[2000];
                sprintf(brName, "jet_%s_consti_%s_reco", str_jetName.c_str(), muMvaVarManager.getName(iVar).c_str());
                
                std::string varName = muMvaVarManager.getName(iVar);
                
                std::vector <std::vector <double> > v_temp;
                m_jet_consti_muonInfo_reco[varName] = v_temp;
                
                tree->Branch(brName, &m_jet_consti_muonInfo_reco[varName]);
            }
        }
        
        
        void clear()
        {
            jet_n_reco = 0;
            
            v_jet_raw_E_reco.clear();
            v_jet_raw_px_reco.clear();
            v_jet_raw_py_reco.clear();
            v_jet_raw_pz_reco.clear();
            v_jet_raw_pT_reco.clear();
            v_jet_raw_eta_reco.clear();
            v_jet_raw_y_reco.clear();
            v_jet_raw_phi_reco.clear();
            v_jet_raw_m_reco.clear();
            
            v_jet_E_reco.clear();
            v_jet_px_reco.clear();
            v_jet_py_reco.clear();
            v_jet_pz_reco.clear();
            v_jet_pT_reco.clear();
            v_jet_eta_reco.clear();
            v_jet_y_reco.clear();
            v_jet_phi_reco.clear();
            v_jet_m_reco.clear();
            
            v_jet_nearestGenTopIdx_reco.clear();
            v_jet_nearestGenTopDR_reco.clear();
            v_jet_nearestGenTopbDR_reco.clear();
            v_jet_nearestGenTopWlepDR_reco.clear();
            v_jet_nearestGenTopWq1DR_reco.clear();
            v_jet_nearestGenTopWq2DR_reco.clear();
            v_jet_nearestGenTopIsLeptonic_reco.clear();
            
            v_jet_nearestGenWIdx_reco.clear();
            v_jet_nearestGenWDR_reco.clear();
            v_jet_nearestGenWlepDR_reco.clear();
            v_jet_nearestGenWq1DR_reco.clear();
            v_jet_nearestGenWq2DR_reco.clear();
            v_jet_nearestGenWIsLeptonic_reco.clear();
            
            v_jet_nearestGenZIdx_reco.clear();
            v_jet_nearestGenZDR_reco.clear();
            v_jet_nearestGenZlep1DR_reco.clear();
            v_jet_nearestGenZlep2DR_reco.clear();
            v_jet_nearestGenZq1DR_reco.clear();
            v_jet_nearestGenZq2DR_reco.clear();
            v_jet_nearestGenZIsLeptonic_reco.clear();
            
            v_jet_nSecVtxInJet_reco.clear();
            
            vv_jet_sv_pT_reco.clear();
            vv_jet_sv_eta_reco.clear();
            vv_jet_sv_phi_reco.clear();
            vv_jet_sv_m_reco.clear();
            vv_jet_sv_E_reco.clear();
            vv_jet_sv_etarel_reco.clear();
            vv_jet_sv_phirel_reco.clear();
            vv_jet_sv_deltaR_reco.clear();
            vv_jet_sv_ntracks_reco.clear();
            vv_jet_sv_chi2_reco.clear();
            vv_jet_sv_ndf_reco.clear();
            vv_jet_sv_normchi2_reco.clear();
            vv_jet_sv_dxy_reco.clear();
            vv_jet_sv_dxyerr_reco.clear();
            vv_jet_sv_dxysig_reco.clear();
            vv_jet_sv_d3d_reco.clear();
            vv_jet_sv_d3derr_reco.clear();
            vv_jet_sv_d3dsig_reco.clear();
            vv_jet_sv_costhetasvpv_reco.clear();
            
            
            for(int iTauN = 0; iTauN <= maxTauN; iTauN++)
            {
                vv_jet_tauN_reco.at(iTauN).clear();
                vv_jet_tauNratio_reco.at(iTauN).clear();
            }
            
            v_jet_nConsti_reco.clear();
            v_jet_nMatchedEl_reco.clear();
            v_jet_nMatchedMu_reco.clear();
            
            vv_jet_consti_E_reco.clear();
            vv_jet_consti_px_reco.clear();
            vv_jet_consti_py_reco.clear();
            vv_jet_consti_pz_reco.clear();
            vv_jet_consti_pT_reco.clear();
            vv_jet_consti_eta_reco.clear();
            vv_jet_consti_phi_reco.clear();
            vv_jet_consti_m_reco.clear();
            
            vv_jet_consti_id_reco.clear();
            
            vv_jet_consti_vx_reco.clear();
            vv_jet_consti_vy_reco.clear();
            vv_jet_consti_vz_reco.clear();
            vv_jet_consti_v2d_reco.clear();
            vv_jet_consti_v3d_reco.clear();
            
            vv_jet_consti_pvdxy_reco.clear();
            vv_jet_consti_pvdz_reco.clear();
            
            vv_jet_consti_svdxy_reco.clear();
            vv_jet_consti_svdz_reco.clear();
            
            vv_jet_consti_dEta_reco.clear();
            vv_jet_consti_dPhi_reco.clear();
            
            vv_jet_consti_EtaPhiRot_dEta_reco.clear();
            vv_jet_consti_EtaPhiRot_dPhi_reco.clear();
            
            vv_jet_consti_LBGS_x_reco.clear();
            vv_jet_consti_LBGS_y_reco.clear();
            
            vv_jet_consti_enFrac_reco.clear();
            
            vv_jet_consti_pTwrtJet_reco.clear();
            vv_jet_consti_dRwrtJet_reco.clear();
            
            
            for(auto &kv : m_jet_consti_electronInfo_reco)
            {
                kv.second.clear();
            }
            
            for(auto &kv : m_jet_consti_muonInfo_reco)
            {
                kv.second.clear();
            }
        }
    };
    
    class TreeOutput
    {
        public :
        
        
        TTree *tree;
        
        
        // Run info //
        ULong64_t runNumber;
        ULong64_t eventNumber;
        ULong64_t luminosityNumber;
        ULong64_t bunchCrossingNumber;
        
        
        // Gen event info //
        double genEventWeight;
        
        
        // Gen top //
        int genTop_n;
        std::vector <double> v_genTop_id;
        std::vector <double> v_genTop_E;
        std::vector <double> v_genTop_px;
        std::vector <double> v_genTop_py;
        std::vector <double> v_genTop_pz;
        std::vector <double> v_genTop_pT;
        std::vector <double> v_genTop_eta;
        std::vector <double> v_genTop_y;
        std::vector <double> v_genTop_phi;
        std::vector <double> v_genTop_m;
        std::vector <double> v_genTop_isLeptonic;
        
        // Gen top decay products //
        std::vector <double> v_genTop_b_id;
        std::vector <double> v_genTop_b_E;
        std::vector <double> v_genTop_b_px;
        std::vector <double> v_genTop_b_py;
        std::vector <double> v_genTop_b_pz;
        std::vector <double> v_genTop_b_pT;
        std::vector <double> v_genTop_b_eta;
        std::vector <double> v_genTop_b_y;
        std::vector <double> v_genTop_b_phi;
        std::vector <double> v_genTop_b_m;
        
        std::vector <double> v_genTop_Wq1_id;
        std::vector <double> v_genTop_Wq1_E;
        std::vector <double> v_genTop_Wq1_px;
        std::vector <double> v_genTop_Wq1_py;
        std::vector <double> v_genTop_Wq1_pz;
        std::vector <double> v_genTop_Wq1_pT;
        std::vector <double> v_genTop_Wq1_eta;
        std::vector <double> v_genTop_Wq1_y;
        std::vector <double> v_genTop_Wq1_phi;
        std::vector <double> v_genTop_Wq1_m;
        
        std::vector <double> v_genTop_Wq2_id;
        std::vector <double> v_genTop_Wq2_E;
        std::vector <double> v_genTop_Wq2_px;
        std::vector <double> v_genTop_Wq2_py;
        std::vector <double> v_genTop_Wq2_pz;
        std::vector <double> v_genTop_Wq2_pT;
        std::vector <double> v_genTop_Wq2_eta;
        std::vector <double> v_genTop_Wq2_y;
        std::vector <double> v_genTop_Wq2_phi;
        std::vector <double> v_genTop_Wq2_m;
        
        std::vector <double> v_genTop_Wlep_id;
        std::vector <double> v_genTop_Wlep_E;
        std::vector <double> v_genTop_Wlep_px;
        std::vector <double> v_genTop_Wlep_py;
        std::vector <double> v_genTop_Wlep_pz;
        std::vector <double> v_genTop_Wlep_pT;
        std::vector <double> v_genTop_Wlep_eta;
        std::vector <double> v_genTop_Wlep_y;
        std::vector <double> v_genTop_Wlep_phi;
        std::vector <double> v_genTop_Wlep_m;
        
        // Gen top visible component //
        std::vector <double> v_genTopVis_E;
        std::vector <double> v_genTopVis_px;
        std::vector <double> v_genTopVis_py;
        std::vector <double> v_genTopVis_pz;
        std::vector <double> v_genTopVis_pT;
        std::vector <double> v_genTopVis_eta;
        std::vector <double> v_genTopVis_y;
        std::vector <double> v_genTopVis_phi;
        std::vector <double> v_genTopVis_m;
        
        
        // Gen W //
        int genW_n;
        std::vector <double> v_genW_id;
        std::vector <double> v_genW_E;
        std::vector <double> v_genW_px;
        std::vector <double> v_genW_py;
        std::vector <double> v_genW_pz;
        std::vector <double> v_genW_pT;
        std::vector <double> v_genW_eta;
        std::vector <double> v_genW_y;
        std::vector <double> v_genW_phi;
        std::vector <double> v_genW_m;
        std::vector <double> v_genW_isLeptonic;
        
        // Gen W decay products //
        std::vector <double> v_genW_q1_id;
        std::vector <double> v_genW_q1_E;
        std::vector <double> v_genW_q1_px;
        std::vector <double> v_genW_q1_py;
        std::vector <double> v_genW_q1_pz;
        std::vector <double> v_genW_q1_pT;
        std::vector <double> v_genW_q1_eta;
        std::vector <double> v_genW_q1_y;
        std::vector <double> v_genW_q1_phi;
        std::vector <double> v_genW_q1_m;
        
        std::vector <double> v_genW_q2_id;
        std::vector <double> v_genW_q2_E;
        std::vector <double> v_genW_q2_px;
        std::vector <double> v_genW_q2_py;
        std::vector <double> v_genW_q2_pz;
        std::vector <double> v_genW_q2_pT;
        std::vector <double> v_genW_q2_eta;
        std::vector <double> v_genW_q2_y;
        std::vector <double> v_genW_q2_phi;
        std::vector <double> v_genW_q2_m;
        
        std::vector <double> v_genW_lep_id;
        std::vector <double> v_genW_lep_E;
        std::vector <double> v_genW_lep_px;
        std::vector <double> v_genW_lep_py;
        std::vector <double> v_genW_lep_pz;
        std::vector <double> v_genW_lep_pT;
        std::vector <double> v_genW_lep_eta;
        std::vector <double> v_genW_lep_y;
        std::vector <double> v_genW_lep_phi;
        std::vector <double> v_genW_lep_m;
        
        // Gen W visible component //
        std::vector <double> v_genWvis_E;
        std::vector <double> v_genWvis_px;
        std::vector <double> v_genWvis_py;
        std::vector <double> v_genWvis_pz;
        std::vector <double> v_genWvis_pT;
        std::vector <double> v_genWvis_eta;
        std::vector <double> v_genWvis_y;
        std::vector <double> v_genWvis_phi;
        std::vector <double> v_genWvis_m;
        
        
        // Gen Z //
        int genZ_n;
        std::vector <double> v_genZ_id;
        std::vector <double> v_genZ_E;
        std::vector <double> v_genZ_px;
        std::vector <double> v_genZ_py;
        std::vector <double> v_genZ_pz;
        std::vector <double> v_genZ_pT;
        std::vector <double> v_genZ_eta;
        std::vector <double> v_genZ_y;
        std::vector <double> v_genZ_phi;
        std::vector <double> v_genZ_m;
        std::vector <double> v_genZ_isLeptonic;
        
        // Gen Z decay products //
        std::vector <double> v_genZ_q1_id;
        std::vector <double> v_genZ_q1_E;
        std::vector <double> v_genZ_q1_px;
        std::vector <double> v_genZ_q1_py;
        std::vector <double> v_genZ_q1_pz;
        std::vector <double> v_genZ_q1_pT;
        std::vector <double> v_genZ_q1_eta;
        std::vector <double> v_genZ_q1_y;
        std::vector <double> v_genZ_q1_phi;
        std::vector <double> v_genZ_q1_m;
        
        std::vector <double> v_genZ_q2_id;
        std::vector <double> v_genZ_q2_E;
        std::vector <double> v_genZ_q2_px;
        std::vector <double> v_genZ_q2_py;
        std::vector <double> v_genZ_q2_pz;
        std::vector <double> v_genZ_q2_pT;
        std::vector <double> v_genZ_q2_eta;
        std::vector <double> v_genZ_q2_y;
        std::vector <double> v_genZ_q2_phi;
        std::vector <double> v_genZ_q2_m;
        
        std::vector <double> v_genZ_lep1_id;
        std::vector <double> v_genZ_lep1_E;
        std::vector <double> v_genZ_lep1_px;
        std::vector <double> v_genZ_lep1_py;
        std::vector <double> v_genZ_lep1_pz;
        std::vector <double> v_genZ_lep1_pT;
        std::vector <double> v_genZ_lep1_eta;
        std::vector <double> v_genZ_lep1_y;
        std::vector <double> v_genZ_lep1_phi;
        std::vector <double> v_genZ_lep1_m;
        
        std::vector <double> v_genZ_lep2_id;
        std::vector <double> v_genZ_lep2_E;
        std::vector <double> v_genZ_lep2_px;
        std::vector <double> v_genZ_lep2_py;
        std::vector <double> v_genZ_lep2_pz;
        std::vector <double> v_genZ_lep2_pT;
        std::vector <double> v_genZ_lep2_eta;
        std::vector <double> v_genZ_lep2_y;
        std::vector <double> v_genZ_lep2_phi;
        std::vector <double> v_genZ_lep2_m;
        
        // SV //
        int sv_n;
        
        
        // Pileup //
        int pileup_n;
        
        
        // Rho //
        double rho;
        
        
        // Jets //
        std::map <std::string, JetInfo*> m_jetInfo;
        
        
        char name[2000];
        
        
        TreeOutput(std::string details, edm::Service<TFileService> fs)
        {
            printf("Loading custom ROOT dictionaries. \n");
            gROOT->ProcessLine(".L MyTools/EDAnalyzers/interface/CustomRootDict.cc+");
            printf("Loaded custom ROOT dictionaries. \n");
            
            tree = fs->make<TTree>(details.c_str(), details.c_str());
            
            
            // Run info //
            tree->Branch("runNumber", &runNumber);
            tree->Branch("eventNumber", &eventNumber);
            tree->Branch("luminosityNumber", &luminosityNumber);
            tree->Branch("bunchCrossingNumber", &bunchCrossingNumber);
            
            
            // Gen event info //
            sprintf(name, "genEventWeight");
            tree->Branch(name, &genEventWeight);
            
            
            // Gen top //
            sprintf(name, "genTop_n");
            tree->Branch(name, &genTop_n);
            
            sprintf(name, "genTop_id");
            tree->Branch(name, &v_genTop_id);
            
            sprintf(name, "genTop_E");
            tree->Branch(name, &v_genTop_E);
            
            sprintf(name, "genTop_px");
            tree->Branch(name, &v_genTop_px);
            
            sprintf(name, "genTop_py");
            tree->Branch(name, &v_genTop_py);
            
            sprintf(name, "genTop_pz");
            tree->Branch(name, &v_genTop_pz);
            
            sprintf(name, "genTop_pT");
            tree->Branch(name, &v_genTop_pT);
            
            sprintf(name, "genTop_eta");
            tree->Branch(name, &v_genTop_eta);
            
            sprintf(name, "genTop_y");
            tree->Branch(name, &v_genTop_y);
            
            sprintf(name, "genTop_phi");
            tree->Branch(name, &v_genTop_phi);
            
            sprintf(name, "genTop_m");
            tree->Branch(name, &v_genTop_m);
            
            sprintf(name, "genTop_isLeptonic");
            tree->Branch(name, &v_genTop_isLeptonic);
            
            
            // Gen top decay products //
            sprintf(name, "genTop_b_id");
            tree->Branch(name, &v_genTop_b_id);
            
            sprintf(name, "genTop_b_E");
            tree->Branch(name, &v_genTop_b_E);
            
            sprintf(name, "genTop_b_px");
            tree->Branch(name, &v_genTop_b_px);
            
            sprintf(name, "genTop_b_py");
            tree->Branch(name, &v_genTop_b_py);
            
            sprintf(name, "genTop_b_pz");
            tree->Branch(name, &v_genTop_b_pz);
            
            sprintf(name, "genTop_b_pT");
            tree->Branch(name, &v_genTop_b_pT);
            
            sprintf(name, "genTop_b_eta");
            tree->Branch(name, &v_genTop_b_eta);
            
            sprintf(name, "genTop_b_y");
            tree->Branch(name, &v_genTop_b_y);
            
            sprintf(name, "genTop_b_phi");
            tree->Branch(name, &v_genTop_b_phi);
            
            sprintf(name, "genTop_b_m");
            tree->Branch(name, &v_genTop_b_m);
            
            //
            sprintf(name, "genTop_Wq1_id");
            tree->Branch(name, &v_genTop_Wq1_id);
            
            sprintf(name, "genTop_Wq1_E");
            tree->Branch(name, &v_genTop_Wq1_E);
            
            sprintf(name, "genTop_Wq1_px");
            tree->Branch(name, &v_genTop_Wq1_px);
            
            sprintf(name, "genTop_Wq1_py");
            tree->Branch(name, &v_genTop_Wq1_py);
            
            sprintf(name, "genTop_Wq1_pz");
            tree->Branch(name, &v_genTop_Wq1_pz);
            
            sprintf(name, "genTop_Wq1_pT");
            tree->Branch(name, &v_genTop_Wq1_pT);
            
            sprintf(name, "genTop_Wq1_eta");
            tree->Branch(name, &v_genTop_Wq1_eta);
            
            sprintf(name, "genTop_Wq1_y");
            tree->Branch(name, &v_genTop_Wq1_y);
            
            sprintf(name, "genTop_Wq1_phi");
            tree->Branch(name, &v_genTop_Wq1_phi);
            
            sprintf(name, "genTop_Wq1_m");
            tree->Branch(name, &v_genTop_Wq1_m);
            
            //
            sprintf(name, "genTop_Wq2_id");
            tree->Branch(name, &v_genTop_Wq2_id);
            
            sprintf(name, "genTop_Wq2_E");
            tree->Branch(name, &v_genTop_Wq2_E);
            
            sprintf(name, "genTop_Wq2_px");
            tree->Branch(name, &v_genTop_Wq2_px);
            
            sprintf(name, "genTop_Wq2_py");
            tree->Branch(name, &v_genTop_Wq2_py);
            
            sprintf(name, "genTop_Wq2_pz");
            tree->Branch(name, &v_genTop_Wq2_pz);
            
            sprintf(name, "genTop_Wq2_pT");
            tree->Branch(name, &v_genTop_Wq2_pT);
            
            sprintf(name, "genTop_Wq2_eta");
            tree->Branch(name, &v_genTop_Wq2_eta);
            
            sprintf(name, "genTop_Wq2_y");
            tree->Branch(name, &v_genTop_Wq2_y);
            
            sprintf(name, "genTop_Wq2_phi");
            tree->Branch(name, &v_genTop_Wq2_phi);
            
            sprintf(name, "genTop_Wq2_m");
            tree->Branch(name, &v_genTop_Wq2_m);
            
            //
            sprintf(name, "genTop_Wlep_id");
            tree->Branch(name, &v_genTop_Wlep_id);
            
            sprintf(name, "genTop_Wlep_E");
            tree->Branch(name, &v_genTop_Wlep_E);
            
            sprintf(name, "genTop_Wlep_px");
            tree->Branch(name, &v_genTop_Wlep_px);
            
            sprintf(name, "genTop_Wlep_py");
            tree->Branch(name, &v_genTop_Wlep_py);
            
            sprintf(name, "genTop_Wlep_pz");
            tree->Branch(name, &v_genTop_Wlep_pz);
            
            sprintf(name, "genTop_Wlep_pT");
            tree->Branch(name, &v_genTop_Wlep_pT);
            
            sprintf(name, "genTop_Wlep_eta");
            tree->Branch(name, &v_genTop_Wlep_eta);
            
            sprintf(name, "genTop_Wlep_y");
            tree->Branch(name, &v_genTop_Wlep_y);
            
            sprintf(name, "genTop_Wlep_phi");
            tree->Branch(name, &v_genTop_Wlep_phi);
            
            sprintf(name, "genTop_Wlep_m");
            tree->Branch(name, &v_genTop_Wlep_m);
            
            
            // Gen top visible component //
            sprintf(name, "genTopVis_E");
            tree->Branch(name, &v_genTopVis_E);
            
            sprintf(name, "genTopVis_px");
            tree->Branch(name, &v_genTopVis_px);
            
            sprintf(name, "genTopVis_py");
            tree->Branch(name, &v_genTopVis_py);
            
            sprintf(name, "genTopVis_pz");
            tree->Branch(name, &v_genTopVis_pz);
            
            sprintf(name, "genTopVis_pT");
            tree->Branch(name, &v_genTopVis_pT);
            
            sprintf(name, "genTopVis_eta");
            tree->Branch(name, &v_genTopVis_eta);
            
            sprintf(name, "genTopVis_y");
            tree->Branch(name, &v_genTopVis_y);
            
            sprintf(name, "genTopVis_phi");
            tree->Branch(name, &v_genTopVis_phi);
            
            sprintf(name, "genTopVis_m");
            tree->Branch(name, &v_genTopVis_m);
            
            
            // Gen W //
            sprintf(name, "genW_n");
            tree->Branch(name, &genW_n);
            
            sprintf(name, "genW_id");
            tree->Branch(name, &v_genW_id);
            
            sprintf(name, "genW_E");
            tree->Branch(name, &v_genW_E);
            
            sprintf(name, "genW_px");
            tree->Branch(name, &v_genW_px);
            
            sprintf(name, "genW_py");
            tree->Branch(name, &v_genW_py);
            
            sprintf(name, "genW_pz");
            tree->Branch(name, &v_genW_pz);
            
            sprintf(name, "genW_pT");
            tree->Branch(name, &v_genW_pT);
            
            sprintf(name, "genW_eta");
            tree->Branch(name, &v_genW_eta);
            
            sprintf(name, "genW_y");
            tree->Branch(name, &v_genW_y);
            
            sprintf(name, "genW_phi");
            tree->Branch(name, &v_genW_phi);
            
            sprintf(name, "genW_m");
            tree->Branch(name, &v_genW_m);
            
            sprintf(name, "genW_isLeptonic");
            tree->Branch(name, &v_genW_isLeptonic);
            
            
            // Gen W decay products //
            sprintf(name, "genW_q1_id");
            tree->Branch(name, &v_genW_q1_id);
            
            sprintf(name, "genW_q1_E");
            tree->Branch(name, &v_genW_q1_E);
            
            sprintf(name, "genW_q1_px");
            tree->Branch(name, &v_genW_q1_px);
            
            sprintf(name, "genW_q1_py");
            tree->Branch(name, &v_genW_q1_py);
            
            sprintf(name, "genW_q1_pz");
            tree->Branch(name, &v_genW_q1_pz);
            
            sprintf(name, "genW_q1_pT");
            tree->Branch(name, &v_genW_q1_pT);
            
            sprintf(name, "genW_q1_eta");
            tree->Branch(name, &v_genW_q1_eta);
            
            sprintf(name, "genW_q1_y");
            tree->Branch(name, &v_genW_q1_y);
            
            sprintf(name, "genW_q1_phi");
            tree->Branch(name, &v_genW_q1_phi);
            
            sprintf(name, "genW_q1_m");
            tree->Branch(name, &v_genW_q1_m);
            
            //
            sprintf(name, "genW_q2_id");
            tree->Branch(name, &v_genW_q2_id);
            
            sprintf(name, "genW_q2_E");
            tree->Branch(name, &v_genW_q2_E);
            
            sprintf(name, "genW_q2_px");
            tree->Branch(name, &v_genW_q2_px);
            
            sprintf(name, "genW_q2_py");
            tree->Branch(name, &v_genW_q2_py);
            
            sprintf(name, "genW_q2_pz");
            tree->Branch(name, &v_genW_q2_pz);
            
            sprintf(name, "genW_q2_pT");
            tree->Branch(name, &v_genW_q2_pT);
            
            sprintf(name, "genW_q2_eta");
            tree->Branch(name, &v_genW_q2_eta);
            
            sprintf(name, "genW_q2_y");
            tree->Branch(name, &v_genW_q2_y);
            
            sprintf(name, "genW_q2_phi");
            tree->Branch(name, &v_genW_q2_phi);
            
            sprintf(name, "genW_q2_m");
            tree->Branch(name, &v_genW_q2_m);
            
            //
            sprintf(name, "genW_lep_id");
            tree->Branch(name, &v_genW_lep_id);
            
            sprintf(name, "genW_lep_E");
            tree->Branch(name, &v_genW_lep_E);
            
            sprintf(name, "genW_lep_px");
            tree->Branch(name, &v_genW_lep_px);
            
            sprintf(name, "genW_lep_py");
            tree->Branch(name, &v_genW_lep_py);
            
            sprintf(name, "genW_lep_pz");
            tree->Branch(name, &v_genW_lep_pz);
            
            sprintf(name, "genW_lep_pT");
            tree->Branch(name, &v_genW_lep_pT);
            
            sprintf(name, "genW_lep_eta");
            tree->Branch(name, &v_genW_lep_eta);
            
            sprintf(name, "genW_lep_y");
            tree->Branch(name, &v_genW_lep_y);
            
            sprintf(name, "genW_lep_phi");
            tree->Branch(name, &v_genW_lep_phi);
            
            sprintf(name, "genW_lep_m");
            tree->Branch(name, &v_genW_lep_m);
            
            
            // Gen W visible component //
            sprintf(name, "genWvis_E");
            tree->Branch(name, &v_genWvis_E);
            
            sprintf(name, "genWvis_px");
            tree->Branch(name, &v_genWvis_px);
            
            sprintf(name, "genWvis_py");
            tree->Branch(name, &v_genWvis_py);
            
            sprintf(name, "genWvis_pz");
            tree->Branch(name, &v_genWvis_pz);
            
            sprintf(name, "genWvis_pT");
            tree->Branch(name, &v_genWvis_pT);
            
            sprintf(name, "genWvis_eta");
            tree->Branch(name, &v_genWvis_eta);
            
            sprintf(name, "genWvis_y");
            tree->Branch(name, &v_genWvis_y);
            
            sprintf(name, "genWvis_phi");
            tree->Branch(name, &v_genWvis_phi);
            
            sprintf(name, "genWvis_m");
            tree->Branch(name, &v_genWvis_m);
            
            
            // Gen Z //
            sprintf(name, "genZ_n");
            tree->Branch(name, &genZ_n);
            
            sprintf(name, "genZ_id");
            tree->Branch(name, &v_genZ_id);
            
            sprintf(name, "genZ_E");
            tree->Branch(name, &v_genZ_E);
            
            sprintf(name, "genZ_px");
            tree->Branch(name, &v_genZ_px);
            
            sprintf(name, "genZ_py");
            tree->Branch(name, &v_genZ_py);
            
            sprintf(name, "genZ_pz");
            tree->Branch(name, &v_genZ_pz);
            
            sprintf(name, "genZ_pT");
            tree->Branch(name, &v_genZ_pT);
            
            sprintf(name, "genZ_eta");
            tree->Branch(name, &v_genZ_eta);
            
            sprintf(name, "genZ_y");
            tree->Branch(name, &v_genZ_y);
            
            sprintf(name, "genZ_phi");
            tree->Branch(name, &v_genZ_phi);
            
            sprintf(name, "genZ_m");
            tree->Branch(name, &v_genZ_m);
            
            sprintf(name, "genZ_isLeptonic");
            tree->Branch(name, &v_genZ_isLeptonic);
            
            // Gen Z decay products //
            sprintf(name, "genZ_q1_id");
            tree->Branch(name, &v_genZ_q1_id);
            
            sprintf(name, "genZ_q1_E");
            tree->Branch(name, &v_genZ_q1_E);
            
            sprintf(name, "genZ_q1_px");
            tree->Branch(name, &v_genZ_q1_px);
            
            sprintf(name, "genZ_q1_py");
            tree->Branch(name, &v_genZ_q1_py);
            
            sprintf(name, "genZ_q1_pz");
            tree->Branch(name, &v_genZ_q1_pz);
            
            sprintf(name, "genZ_q1_pT");
            tree->Branch(name, &v_genZ_q1_pT);
            
            sprintf(name, "genZ_q1_eta");
            tree->Branch(name, &v_genZ_q1_eta);
            
            sprintf(name, "genZ_q1_y");
            tree->Branch(name, &v_genZ_q1_y);
            
            sprintf(name, "genZ_q1_phi");
            tree->Branch(name, &v_genZ_q1_phi);
            
            sprintf(name, "genZ_q1_m");
            tree->Branch(name, &v_genZ_q1_m);
            
            //
            sprintf(name, "genZ_q2_id");
            tree->Branch(name, &v_genZ_q2_id);
            
            sprintf(name, "genZ_q2_E");
            tree->Branch(name, &v_genZ_q2_E);
            
            sprintf(name, "genZ_q2_px");
            tree->Branch(name, &v_genZ_q2_px);
            
            sprintf(name, "genZ_q2_py");
            tree->Branch(name, &v_genZ_q2_py);
            
            sprintf(name, "genZ_q2_pz");
            tree->Branch(name, &v_genZ_q2_pz);
            
            sprintf(name, "genZ_q2_pT");
            tree->Branch(name, &v_genZ_q2_pT);
            
            sprintf(name, "genZ_q2_eta");
            tree->Branch(name, &v_genZ_q2_eta);
            
            sprintf(name, "genZ_q2_y");
            tree->Branch(name, &v_genZ_q2_y);
            
            sprintf(name, "genZ_q2_phi");
            tree->Branch(name, &v_genZ_q2_phi);
            
            sprintf(name, "genZ_q2_m");
            tree->Branch(name, &v_genZ_q2_m);
            
            //
            sprintf(name, "genZ_lep1_id");
            tree->Branch(name, &v_genZ_lep1_id);
            
            sprintf(name, "genZ_lep1_E");
            tree->Branch(name, &v_genZ_lep1_E);
            
            sprintf(name, "genZ_lep1_px");
            tree->Branch(name, &v_genZ_lep1_px);
            
            sprintf(name, "genZ_lep1_py");
            tree->Branch(name, &v_genZ_lep1_py);
            
            sprintf(name, "genZ_lep1_pz");
            tree->Branch(name, &v_genZ_lep1_pz);
            
            sprintf(name, "genZ_lep1_pT");
            tree->Branch(name, &v_genZ_lep1_pT);
            
            sprintf(name, "genZ_lep1_eta");
            tree->Branch(name, &v_genZ_lep1_eta);
            
            sprintf(name, "genZ_lep1_y");
            tree->Branch(name, &v_genZ_lep1_y);
            
            sprintf(name, "genZ_lep1_phi");
            tree->Branch(name, &v_genZ_lep1_phi);
            
            sprintf(name, "genZ_lep1_m");
            tree->Branch(name, &v_genZ_lep1_m);
            
            //
            sprintf(name, "genZ_lep2_id");
            tree->Branch(name, &v_genZ_lep2_id);
            
            sprintf(name, "genZ_lep2_E");
            tree->Branch(name, &v_genZ_lep2_E);
            
            sprintf(name, "genZ_lep2_px");
            tree->Branch(name, &v_genZ_lep2_px);
            
            sprintf(name, "genZ_lep2_py");
            tree->Branch(name, &v_genZ_lep2_py);
            
            sprintf(name, "genZ_lep2_pz");
            tree->Branch(name, &v_genZ_lep2_pz);
            
            sprintf(name, "genZ_lep2_pT");
            tree->Branch(name, &v_genZ_lep2_pT);
            
            sprintf(name, "genZ_lep2_eta");
            tree->Branch(name, &v_genZ_lep2_eta);
            
            sprintf(name, "genZ_lep2_y");
            tree->Branch(name, &v_genZ_lep2_y);
            
            sprintf(name, "genZ_lep2_phi");
            tree->Branch(name, &v_genZ_lep2_phi);
            
            sprintf(name, "genZ_lep2_m");
            tree->Branch(name, &v_genZ_lep2_m);
            
            
            // SV //
            sprintf(name, "sv_n");
            tree->Branch(name, &sv_n);
            
            
            // Pileup //
            sprintf(name, "pileup_n");
            tree->Branch(name, &pileup_n);
            
            
            // Rho //
            sprintf(name, "rho");
            tree->Branch(name, &rho);
        }
        
        
        std::string addJetInfo(
            const edm::ParameterSet &jetPSet,
            edm::ConsumesCollector &ccollector,
            TTree *tree,
            const MVAVariableManager <pat::Electron> &eleMvaVarManager,
            const MVAVariableManager <pat::Muon> &muMvaVarManager
        )
        {
            JetInfo *jetInfo = new JetInfo(jetPSet, ccollector);
            
            if(m_jetInfo.find(jetInfo->str_jetName) != m_jetInfo.end())
            {
                printf("Error in TreeOutputInfo:addJetInfo(...): key \"%s\" already added. Provide a different string.", jetInfo->str_jetName.c_str());
                exit(EXIT_FAILURE);
            }
            
            jetInfo->createBranches(tree);
            jetInfo->createElectronBranches(tree, eleMvaVarManager);
            jetInfo->createMuonBranches(tree, muMvaVarManager);
            
            m_jetInfo[jetInfo->str_jetName] = jetInfo;
            
            printf("Added info for: %s \n", jetInfo->str_jetName.c_str());
            
            return jetInfo->str_jetName;
        }
        
        
        void fill()
        {
            tree->Fill();
        }
        
        
        void clear()
        {
            // Gen top //
            genTop_n = 0;
            v_genTop_id.clear();
            v_genTop_E.clear();
            v_genTop_px.clear();
            v_genTop_py.clear();
            v_genTop_pz.clear();
            v_genTop_pT.clear();
            v_genTop_eta.clear();
            v_genTop_y.clear();
            v_genTop_phi.clear();
            v_genTop_m.clear();
            v_genTop_isLeptonic.clear();
            
            // Gen top decay products //
            v_genTop_b_id.clear();
            v_genTop_b_E.clear();
            v_genTop_b_px.clear();
            v_genTop_b_py.clear();
            v_genTop_b_pz.clear();
            v_genTop_b_pT.clear();
            v_genTop_b_eta.clear();
            v_genTop_b_y.clear();
            v_genTop_b_phi.clear();
            v_genTop_b_m.clear();
            
            v_genTop_Wq1_id.clear();
            v_genTop_Wq1_E.clear();
            v_genTop_Wq1_px.clear();
            v_genTop_Wq1_py.clear();
            v_genTop_Wq1_pz.clear();
            v_genTop_Wq1_pT.clear();
            v_genTop_Wq1_eta.clear();
            v_genTop_Wq1_y.clear();
            v_genTop_Wq1_phi.clear();
            v_genTop_Wq1_m.clear();
            
            v_genTop_Wq2_id.clear();
            v_genTop_Wq2_E.clear();
            v_genTop_Wq2_px.clear();
            v_genTop_Wq2_py.clear();
            v_genTop_Wq2_pz.clear();
            v_genTop_Wq2_pT.clear();
            v_genTop_Wq2_eta.clear();
            v_genTop_Wq2_y.clear();
            v_genTop_Wq2_phi.clear();
            v_genTop_Wq2_m.clear();
            
            v_genTop_Wlep_id.clear();
            v_genTop_Wlep_E.clear();
            v_genTop_Wlep_px.clear();
            v_genTop_Wlep_py.clear();
            v_genTop_Wlep_pz.clear();
            v_genTop_Wlep_pT.clear();
            v_genTop_Wlep_eta.clear();
            v_genTop_Wlep_y.clear();
            v_genTop_Wlep_phi.clear();
            v_genTop_Wlep_m.clear();
            
            // Gen top visible component //
            v_genTopVis_E.clear();
            v_genTopVis_px.clear();
            v_genTopVis_py.clear();
            v_genTopVis_pz.clear();
            v_genTopVis_pT.clear();
            v_genTopVis_eta.clear();
            v_genTopVis_y.clear();
            v_genTopVis_phi.clear();
            v_genTopVis_m.clear();
            
            
            // Gen W //
            genW_n = 0;
            v_genW_id.clear();
            v_genW_E.clear();
            v_genW_px.clear();
            v_genW_py.clear();
            v_genW_pz.clear();
            v_genW_pT.clear();
            v_genW_eta.clear();
            v_genW_y.clear();
            v_genW_phi.clear();
            v_genW_m.clear();
            v_genW_isLeptonic.clear();
            
            // Gen W decay products //
            v_genW_q1_id.clear();
            v_genW_q1_E.clear();
            v_genW_q1_px.clear();
            v_genW_q1_py.clear();
            v_genW_q1_pz.clear();
            v_genW_q1_pT.clear();
            v_genW_q1_eta.clear();
            v_genW_q1_y.clear();
            v_genW_q1_phi.clear();
            v_genW_q1_m.clear();
            
            v_genW_q2_id.clear();
            v_genW_q2_E.clear();
            v_genW_q2_px.clear();
            v_genW_q2_py.clear();
            v_genW_q2_pz.clear();
            v_genW_q2_pT.clear();
            v_genW_q2_eta.clear();
            v_genW_q2_y.clear();
            v_genW_q2_phi.clear();
            v_genW_q2_m.clear();
            
            v_genW_lep_id.clear();
            v_genW_lep_E.clear();
            v_genW_lep_px.clear();
            v_genW_lep_py.clear();
            v_genW_lep_pz.clear();
            v_genW_lep_pT.clear();
            v_genW_lep_eta.clear();
            v_genW_lep_y.clear();
            v_genW_lep_phi.clear();
            v_genW_lep_m.clear();
            
            // Gen W visible component //
            v_genWvis_E.clear();
            v_genWvis_px.clear();
            v_genWvis_py.clear();
            v_genWvis_pz.clear();
            v_genWvis_pT.clear();
            v_genWvis_eta.clear();
            v_genWvis_y.clear();
            v_genWvis_phi.clear();
            v_genWvis_m.clear();
            
            
            // Gen Z //
            genZ_n = 0;
            v_genZ_id.clear();
            v_genZ_E.clear();
            v_genZ_px.clear();
            v_genZ_py.clear();
            v_genZ_pz.clear();
            v_genZ_pT.clear();
            v_genZ_eta.clear();
            v_genZ_y.clear();
            v_genZ_phi.clear();
            v_genZ_m.clear();
            v_genZ_isLeptonic.clear();
            
            // Gen Z decay products //
            v_genZ_q1_id.clear();
            v_genZ_q1_E.clear();
            v_genZ_q1_px.clear();
            v_genZ_q1_py.clear();
            v_genZ_q1_pz.clear();
            v_genZ_q1_pT.clear();
            v_genZ_q1_eta.clear();
            v_genZ_q1_y.clear();
            v_genZ_q1_phi.clear();
            v_genZ_q1_m.clear();
            
            v_genZ_q2_id.clear();
            v_genZ_q2_E.clear();
            v_genZ_q2_px.clear();
            v_genZ_q2_py.clear();
            v_genZ_q2_pz.clear();
            v_genZ_q2_pT.clear();
            v_genZ_q2_eta.clear();
            v_genZ_q2_y.clear();
            v_genZ_q2_phi.clear();
            v_genZ_q2_m.clear();
            
            v_genZ_lep1_id.clear();
            v_genZ_lep1_E.clear();
            v_genZ_lep1_px.clear();
            v_genZ_lep1_py.clear();
            v_genZ_lep1_pz.clear();
            v_genZ_lep1_pT.clear();
            v_genZ_lep1_eta.clear();
            v_genZ_lep1_y.clear();
            v_genZ_lep1_phi.clear();
            v_genZ_lep1_m.clear();
            
            v_genZ_lep2_id.clear();
            v_genZ_lep2_E.clear();
            v_genZ_lep2_px.clear();
            v_genZ_lep2_py.clear();
            v_genZ_lep2_pz.clear();
            v_genZ_lep2_pT.clear();
            v_genZ_lep2_eta.clear();
            v_genZ_lep2_y.clear();
            v_genZ_lep2_phi.clear();
            v_genZ_lep2_m.clear();
            
            
            // SV //
            sv_n = 0;
            
            
            // Pileup //
            pileup_n = 0;
            
            
            // Rho //
            rho = 0;
            
            
            for(auto const &kv : m_jetInfo)
            {
                kv.second->clear();
            }
        }
    };
}


# endif
