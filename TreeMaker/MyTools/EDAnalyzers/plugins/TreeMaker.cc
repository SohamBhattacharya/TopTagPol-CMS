// -*- C++ -*-
//
// Package:    EDAnalyzers/TreeMaker
// Class:      TreeMaker
//
/**\class TreeMaker TreeMaker.cc EDAnalyzers/TreeMaker/plugins/TreeMaker.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  
//         Created:  Sat, 11 May 2019 13:14:55 GMT
//
//


// system include files
# include <algorithm>
# include <memory>

// user include files

# include "CommonTools/UtilAlgos/interface/TFileService.h"
# include "DataFormats/CaloTowers/interface/CaloTowerDefs.h"
# include "DataFormats/Candidate/interface/VertexCompositePtrCandidate.h"
# include "DataFormats/Common/interface/MapOfVectors.h"
# include "DataFormats/EcalRecHit/interface/EcalRecHit.h"
# include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
# include "DataFormats/EgammaCandidates/interface/Photon.h"
# include "DataFormats/FWLite/interface/ESHandle.h"
# include "DataFormats/GeometryCommonDetAlgo/interface/Measurement1D.h"
# include "DataFormats/GsfTrackReco/interface/GsfTrack.h"
# include "DataFormats/HepMCCandidate/interface/GenParticle.h"
# include "DataFormats/JetReco/interface/PFJet.h"
# include "DataFormats/Math/interface/LorentzVector.h"
# include "DataFormats/Math/interface/deltaR.h"
# include "DataFormats/ParticleFlowReco/interface/PFRecHit.h"
# include "DataFormats/PatCandidates/interface/Electron.h"
# include "DataFormats/PatCandidates/interface/Jet.h"
# include "DataFormats/PatCandidates/interface/MET.h"
# include "DataFormats/PatCandidates/interface/Muon.h"
# include "DataFormats/PatCandidates/interface/PackedGenParticle.h"
# include "DataFormats/PatCandidates/interface/Photon.h"
# include "DataFormats/RecoCandidate/interface/RecoCandidate.h"
# include "DataFormats/TrackReco/interface/Track.h"
# include "DataFormats/TrackReco/interface/TrackFwd.h"
# include "DataFormats/VertexReco/interface/Vertex.h"
# include "DataFormats/VertexReco/interface/VertexFwd.h"
# include "FWCore/Framework/interface/ConsumesCollector.h"
# include "FWCore/Framework/interface/ESHandle.h"
# include "FWCore/Framework/interface/Event.h"
# include "FWCore/Framework/interface/Frameworkfwd.h"
# include "FWCore/Framework/interface/MakerMacros.h"
# include "FWCore/Framework/interface/one/EDAnalyzer.h"
# include "FWCore/ParameterSet/interface/ParameterSet.h"
# include "FWCore/ServiceRegistry/interface/Service.h"
# include "FWCore/Utilities/interface/InputTag.h"
# include "Geometry/Records/interface/CaloGeometryRecord.h"
# include "Geometry/Records/interface/IdealGeometryRecord.h"
# include "RecoEgamma/EgammaTools/interface/MVAVariableHelper.h"
# include "RecoEgamma/EgammaTools/interface/MVAVariableManager.h"
# include "RecoVertex/VertexTools/interface/VertexDistance3D.h"
# include "SimDataFormats/CaloAnalysis/interface/CaloParticle.h"
# include "SimDataFormats/CaloAnalysis/interface/SimCluster.h"
# include "SimDataFormats/CaloHit/interface/PCaloHit.h"
# include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
# include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
# include "TrackingTools/IPTools/interface/IPTools.h"

# include <Compression.h>
# include <Math/VectorUtil.h>
# include <TH1F.h>
# include <TH2F.h>
# include <TLorentzVector.h>
# include <TMatrixD.h>
# include <TTree.h> 
# include <TVector2.h> 
# include <TVectorD.h> 


# include <CLHEP/Matrix/Matrix.h>
# include <CLHEP/Vector/LorentzVector.h>
# include <CLHEP/Vector/ThreeVector.h>
# include <CLHEP/Vector/ThreeVector.h>

# include "fastjet/contrib/AxesDefinition.hh"
# include "fastjet/contrib/EnergyCorrelator.hh"
# include "fastjet/contrib/MeasureDefinition.hh"
# include "fastjet/contrib/Nsubjettiness.hh"
# include "fastjet/contrib/SoftDrop.hh"
# include "fastjet/PseudoJet.hh"
# include "fastjet/ClusterSequence.hh"

# include "MyTools/EDAnalyzers/interface/Common.h"
# include "MyTools/EDAnalyzers/interface/Constants.h"
# include "MyTools/EDAnalyzers/interface/TreeOutputInfo.h"

//
// class declaration
//

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDAnalyzer<>
// This will improve performance in multithreaded jobs.



class TreeMaker : public edm::one::EDAnalyzer<edm::one::SharedResources>
{
    public:
    
    explicit TreeMaker(const edm::ParameterSet&);
    ~TreeMaker();
    
    static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
    
    
    private:
    
    virtual void beginJob() override;
    virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
    virtual void endJob() override;
    
    
    TreeOutputInfo::TreeOutput *treeOutput;
    
    
    // My stuff //
    bool debug;
    bool isGunSample;
    
    fastjet::Strategy fj_strategy;
    fastjet::RecombinationScheme fj_recombScheme;
    
    fastjet::JetDefinition *fj_fatJetExcSubJetDef;
    fastjet::JetDefinition *fj_akJetReclusterDef;
    
    
    // GenEventInfoProduct //
    edm::EDGetTokenT <GenEventInfoProduct> tok_generator;
    
    
    // Gen particles //
    edm::EDGetTokenT <std::vector <reco::GenParticle> > tok_genParticle;
    
    
    // PV //
    edm::EDGetTokenT <std::vector <reco::Vertex> > tok_primaryVertex;
    
    
    // SV //
    edm::EDGetTokenT <std::vector <reco::VertexCompositePtrCandidate> > tok_secondaryVertex;
    
    
    // Pileup //
    edm::EDGetTokenT <std::vector <PileupSummaryInfo> > tok_pileup;
    
    
    // Rho //
    edm::EDGetTokenT <double> tok_rho;
    
    
    // Electrons //
    edm::EDGetTokenT <std::vector <pat::Electron> > tok_electron_reco;
    
    std::string eleMvaVariablesFile;
    MVAVariableManager <pat::Electron> eleMvaVarManager;
    //MVAVariableManager <reco::GsfElectron> eleMvaVarManager;
    
    MVAVariableHelper <pat::Electron> eleMvaVarHelper;
    //MVAVariableHelper <reco::GsfElectron> eleMvaVarHelper;
    
    
    // Muons //
    edm::EDGetTokenT <std::vector <pat::Muon> > tok_muon_reco;
    
    std::string muMvaVariablesFile;
    MVAVariableManager <pat::Muon> muMvaVarManager;
    MVAVariableHelper <pat::Muon> muMvaVarHelper; // Just a dummy, don't need it for muons
    
    
    
    // Jets //
    std::vector <edm::InputTag> v_jetCollectionTag;
    std::vector <std::string> v_jetCollectionName;
    std::vector <edm::EDGetTokenT <std::vector <pat::Jet> > > v_tok_jet_reco;
    
    std::vector <edm::ParameterSet> v_recoJetPSet;
    
    
    // Other stuff //
    
    
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
TreeMaker::TreeMaker(const edm::ParameterSet& iConfig) :
    eleMvaVarManager(iConfig.getParameter <std::string>("eleMvaVariablesFile")),
    eleMvaVarHelper(consumesCollector()),
    muMvaVarManager(iConfig.getParameter <std::string>("muMvaVariablesFile")),
    muMvaVarHelper(consumesCollector())
{
    usesResource("TFileService");
    edm::Service<TFileService> fs;
    
    // Compression
    //fs->file().SetCompressionAlgorithm(ROOT::kLZMA);
    //fs->file().SetCompressionLevel(8);
    
    
    //now do what ever initialization is needed
    
    treeOutput = new TreeOutputInfo::TreeOutput("tree", fs);
    
    
    // My stuff //
    debug = iConfig.getParameter <bool>("debug");
    isGunSample = iConfig.getParameter <bool>("isGunSample");
    
    fj_strategy = fastjet::Best;
    fj_recombScheme = fastjet::E_scheme;
    
    //fj_jetDef = new fastjet::JetDefinition(fastjet::antikt_algorithm, _jetR, fj_recombScheme, fj_strategy);
    //fj_fatJetDef = new fastjet::JetDefinition(fastjet::cambridge_algorithm, _fatJetR, fj_recombScheme, fj_strategy);
    fj_fatJetExcSubJetDef = new fastjet::JetDefinition(fastjet::kt_algorithm, 1.0, fj_recombScheme, fj_strategy);
    fj_akJetReclusterDef = new fastjet::JetDefinition(fastjet::antikt_algorithm, 1000.0, fj_recombScheme, fj_strategy);
    
    
    // GenEventInfoProduct //
    tok_generator = consumes <GenEventInfoProduct>(iConfig.getParameter <edm::InputTag>("label_generator"));

    
    // Gen particles //
    tok_genParticle = consumes <std::vector <reco::GenParticle> >(iConfig.getParameter <edm::InputTag>("label_genParticle"));
    
    
    // PV //
    tok_primaryVertex = consumes <std::vector <reco::Vertex> >(iConfig.getParameter <edm::InputTag>("label_primaryVertex"));
    
    
    // SV //
    tok_secondaryVertex = consumes <std::vector <reco::VertexCompositePtrCandidate> >(iConfig.getParameter <edm::InputTag>("label_secondaryVertex"));
    
    
    // Pileup //
    tok_pileup = consumes <std::vector <PileupSummaryInfo> >(iConfig.getParameter <edm::InputTag>("label_pileup"));
    
    
    // Rho //
    tok_rho = consumes <double>(iConfig.getParameter <edm::InputTag>("label_rho"));
    
    
    // Electrons //
    tok_electron_reco = consumes <std::vector <pat::Electron> >(iConfig.getParameter <edm::InputTag>("label_slimmedElectron"));
    
    //eleMvaVariablesFile = iConfig.getParameter <std::string>("eleMvaVariablesFile");
    //eleMvaVarManager(eleMvaVariablesFile, MVAVariableHelper::indexMap());
    
    
    // Muons //
    tok_muon_reco = consumes <std::vector <pat::Muon> >(iConfig.getParameter <edm::InputTag>("label_slimmedMuon"));
    
    
    // Jets //
    v_recoJetPSet = iConfig.getParameter <std::vector <edm::ParameterSet> >("v_recoJetPSet");
    
    for(const auto &jetPSet : v_recoJetPSet)
    {
        edm::ConsumesCollector ccollector = consumesCollector();
        
        std::string jetName = treeOutput->addJetInfo(jetPSet, ccollector, treeOutput->tree, eleMvaVarManager, muMvaVarManager);
        
        v_jetCollectionName.push_back(jetName);
    }
    
    
    // Other stuff
    //mvaVarHelper(consumesCollector());
}


TreeMaker::~TreeMaker()
{
    // do anything here that needs to be done at desctruction time
    // (e.g. close files, deallocate resources etc.)
    
    delete treeOutput;
}


//
// member functions
//


// ------------ method called for each event  ------------
void TreeMaker::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    using namespace edm;
    
    long long eventNumber = iEvent.id().event();
    //printf("Event %llu \n", eventNumber);
    
    
    treeOutput->clear();
    
    //recHitTools.getEventSetup(iSetup);
    
    //////////////////// Run info ////////////////////
    treeOutput->runNumber = iEvent.id().run();
    treeOutput->eventNumber = iEvent.id().event();
    treeOutput->luminosityNumber = iEvent.id().luminosityBlock();
    treeOutput->bunchCrossingNumber = iEvent.bunchCrossing();
    
    
    
    //////////////////// GenEventInfoProduct ////////////////////
    edm::Handle <GenEventInfoProduct> generatorHandle;
    iEvent.getByToken(tok_generator, generatorHandle);
    GenEventInfoProduct generator = *generatorHandle;
    
    if(debug)
    {
        printf("[%llu] Gen. evt. wt. %0.4g \n", eventNumber, generator.weight());
    }
    
    treeOutput->genEventWeight = generator.weight();
    
    
    //////////////////// Gen particle ////////////////////
    edm::Handle <std::vector <reco::GenParticle> > v_genParticle;
    iEvent.getByToken(tok_genParticle, v_genParticle);
    
    
    std::vector <CLHEP::HepLorentzVector> v_genTopVis_4mom;
    std::vector <CLHEP::HepLorentzVector> v_genWvis_4mom;
    std::vector <CLHEP::HepLorentzVector> v_genZ_4mom;
    
    std::vector <CLHEP::HepLorentzVector> v_genTop_b_4mom;
    std::vector <CLHEP::HepLorentzVector> v_genTop_Wlep_4mom;
    std::vector <CLHEP::HepLorentzVector> v_genTop_Wq1_4mom;
    std::vector <CLHEP::HepLorentzVector> v_genTop_Wq2_4mom;
    
    std::vector <CLHEP::HepLorentzVector> v_genW_lep_4mom;
    std::vector <CLHEP::HepLorentzVector> v_genW_q1_4mom;
    std::vector <CLHEP::HepLorentzVector> v_genW_q2_4mom;
    
    std::vector <CLHEP::HepLorentzVector> v_genZ_lep1_4mom;
    std::vector <CLHEP::HepLorentzVector> v_genZ_lep2_4mom;
    std::vector <CLHEP::HepLorentzVector> v_genZ_q1_4mom;
    std::vector <CLHEP::HepLorentzVector> v_genZ_q2_4mom;
    
    for(int iPart = 0; iPart < (int) v_genParticle->size(); iPart++)
    {
        reco::GenParticle part = v_genParticle->at(iPart);
        
        int pdgId = part.pdgId();
        int status = part.status();
        
        if(std::abs(pdgId) == 6 && part.isLastCopy())
        {
            treeOutput->v_genTop_id.push_back(pdgId);
            treeOutput->v_genTop_E.push_back(part.energy());
            treeOutput->v_genTop_px.push_back(part.px());
            treeOutput->v_genTop_py.push_back(part.py());
            treeOutput->v_genTop_pz.push_back(part.pz());
            treeOutput->v_genTop_pT.push_back(part.pt());
            treeOutput->v_genTop_eta.push_back(part.eta());
            treeOutput->v_genTop_y.push_back(part.y());
            treeOutput->v_genTop_phi.push_back(part.phi());
            treeOutput->v_genTop_m.push_back(part.mass());
            
            int isLeptonicTop = Common::isLeptonicTopWZ(&part);
            
            treeOutput->v_genTop_isLeptonic.push_back(isLeptonicTop);
            
            CLHEP::HepLorentzVector genTopVis_4mom = Common::lorentzVector2clhep(Common::getVisibleCompnent(&part));
            v_genTopVis_4mom.push_back(genTopVis_4mom);
            
            const reco::GenParticle *genTop_b = part.daughterRef(0).get();
            const reco::GenParticle *genTop_W = part.daughterRef(1).get();
            
            if(std::abs(genTop_b->pdgId()) == 24)
            {
                genTop_b = part.daughterRef(1).get();
                genTop_W = part.daughterRef(0).get();
            }
            
            genTop_W = Common::getLastCopy(genTop_W);
            
            CLHEP::HepLorentzVector genTop_b_4mom;
            CLHEP::HepLorentzVector genTop_Wlep_4mom;
            CLHEP::HepLorentzVector genTop_Wq1_4mom;
            CLHEP::HepLorentzVector genTop_Wq2_4mom;
            
            genTop_b_4mom = Common::lorentzVector2clhep(genTop_b->p4());
            v_genTop_b_4mom.push_back(genTop_b_4mom);
            
            const reco::GenParticle *genTop_Wlep = 0;
            const reco::GenParticle *genTop_Wq1 = 0;
            const reco::GenParticle *genTop_Wq2 = 0;
            
            if(isLeptonicTop)
            {
                genTop_Wlep = genTop_W->daughterRef(0).get();
                
                if(std::abs(genTop_Wlep->pdgId()) == 12 || std::abs(genTop_Wlep->pdgId()) == 14 || std::abs(genTop_Wlep->pdgId()) == 16)
                {
                    genTop_Wlep = genTop_W->daughterRef(1).get();
                }
                
                genTop_Wlep_4mom = Common::lorentzVector2clhep(genTop_Wlep->p4());
            }
            
            else
            {
                genTop_Wq1 = genTop_W->daughterRef(0).get();
                genTop_Wq2 = genTop_W->daughterRef(1).get();
                
                if(genTop_Wq1->pt() < genTop_Wq2->pt())
                {
                    genTop_Wq1 = genTop_W->daughterRef(1).get();
                    genTop_Wq2 = genTop_W->daughterRef(0).get();
                }
                
                genTop_Wq1_4mom = Common::lorentzVector2clhep(genTop_Wq1->p4());
                genTop_Wq2_4mom = Common::lorentzVector2clhep(genTop_Wq2->p4());
            }
            
            v_genTop_Wlep_4mom.push_back(genTop_Wlep_4mom);
            v_genTop_Wq1_4mom.push_back(genTop_Wq1_4mom);
            v_genTop_Wq2_4mom.push_back(genTop_Wq2_4mom);
            
            if(debug)
            {
                printf(
                    "[%llu] "
                    "Gen t (isLeptonic %d) found (orig/vis): E %0.2f/%0.2f, pT %0.2f/%0.2f, eta %+0.2f/%+0.2f, phi %+0.2f/%+0.2f, "
                    "\n",
                    eventNumber,
                    (int) isLeptonicTop,
                    part.energy(), genTopVis_4mom.e(),
                    part.pt(), genTopVis_4mom.perp(),
                    part.eta(), genTopVis_4mom.eta(),
                    part.phi(), genTopVis_4mom.phi()
                );
            }
            
            
            treeOutput->v_genTop_b_id.push_back(genTop_b->pdgId());
            treeOutput->v_genTop_b_E.push_back(genTop_b->energy());
            treeOutput->v_genTop_b_px.push_back(genTop_b->px());
            treeOutput->v_genTop_b_py.push_back(genTop_b->py());
            treeOutput->v_genTop_b_pz.push_back(genTop_b->pz());
            treeOutput->v_genTop_b_pT.push_back(genTop_b->pt());
            treeOutput->v_genTop_b_eta.push_back(genTop_b->eta());
            treeOutput->v_genTop_b_y.push_back(genTop_b->y());
            treeOutput->v_genTop_b_phi.push_back(genTop_b->phi());
            treeOutput->v_genTop_b_m.push_back(genTop_b->mass());
            
            
            // Fill lepton
            if(genTop_Wlep)
            {
                treeOutput->v_genTop_Wlep_id.push_back(genTop_Wlep->pdgId());
                treeOutput->v_genTop_Wlep_E.push_back(genTop_Wlep->energy());
                treeOutput->v_genTop_Wlep_px.push_back(genTop_Wlep->px());
                treeOutput->v_genTop_Wlep_py.push_back(genTop_Wlep->py());
                treeOutput->v_genTop_Wlep_pz.push_back(genTop_Wlep->pz());
                treeOutput->v_genTop_Wlep_pT.push_back(genTop_Wlep->pt());
                treeOutput->v_genTop_Wlep_eta.push_back(genTop_Wlep->eta());
                treeOutput->v_genTop_Wlep_y.push_back(genTop_Wlep->y());
                treeOutput->v_genTop_Wlep_phi.push_back(genTop_Wlep->phi());
                treeOutput->v_genTop_Wlep_m.push_back(genTop_Wlep->mass());
            }
            
            else
            {
                treeOutput->v_genTop_Wlep_id.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genTop_Wlep_E.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genTop_Wlep_px.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genTop_Wlep_py.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genTop_Wlep_pz.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genTop_Wlep_pT.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genTop_Wlep_eta.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genTop_Wlep_y.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genTop_Wlep_phi.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genTop_Wlep_m.push_back(Constants::LARGEVAL_NEG);
            }
            
            
            // Fill quarks
            if(genTop_Wq1 && genTop_Wq2)
            {
                treeOutput->v_genTop_Wq1_id.push_back(genTop_Wq1->pdgId());
                treeOutput->v_genTop_Wq1_E.push_back(genTop_Wq1->energy());
                treeOutput->v_genTop_Wq1_px.push_back(genTop_Wq1->px());
                treeOutput->v_genTop_Wq1_py.push_back(genTop_Wq1->py());
                treeOutput->v_genTop_Wq1_pz.push_back(genTop_Wq1->pz());
                treeOutput->v_genTop_Wq1_pT.push_back(genTop_Wq1->pt());
                treeOutput->v_genTop_Wq1_eta.push_back(genTop_Wq1->eta());
                treeOutput->v_genTop_Wq1_y.push_back(genTop_Wq1->y());
                treeOutput->v_genTop_Wq1_phi.push_back(genTop_Wq1->phi());
                treeOutput->v_genTop_Wq1_m.push_back(genTop_Wq1->mass());
                
                treeOutput->v_genTop_Wq2_id.push_back(genTop_Wq2->pdgId());
                treeOutput->v_genTop_Wq2_E.push_back(genTop_Wq2->energy());
                treeOutput->v_genTop_Wq2_px.push_back(genTop_Wq2->px());
                treeOutput->v_genTop_Wq2_py.push_back(genTop_Wq2->py());
                treeOutput->v_genTop_Wq2_pz.push_back(genTop_Wq2->pz());
                treeOutput->v_genTop_Wq2_pT.push_back(genTop_Wq2->pt());
                treeOutput->v_genTop_Wq2_eta.push_back(genTop_Wq2->eta());
                treeOutput->v_genTop_Wq2_y.push_back(genTop_Wq2->y());
                treeOutput->v_genTop_Wq2_phi.push_back(genTop_Wq2->phi());
                treeOutput->v_genTop_Wq2_m.push_back(genTop_Wq2->mass());
            }
            
            else
            {
                treeOutput->v_genTop_Wq1_id.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genTop_Wq1_E.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genTop_Wq1_px.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genTop_Wq1_py.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genTop_Wq1_pz.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genTop_Wq1_pT.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genTop_Wq1_eta.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genTop_Wq1_y.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genTop_Wq1_phi.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genTop_Wq1_m.push_back(Constants::LARGEVAL_NEG);
                
                treeOutput->v_genTop_Wq2_id.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genTop_Wq2_E.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genTop_Wq2_px.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genTop_Wq2_py.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genTop_Wq2_pz.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genTop_Wq2_pT.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genTop_Wq2_eta.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genTop_Wq2_y.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genTop_Wq2_phi.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genTop_Wq2_m.push_back(Constants::LARGEVAL_NEG);
            }
            
            
            treeOutput->v_genTopVis_E.push_back(genTopVis_4mom.e());
            treeOutput->v_genTopVis_px.push_back(genTopVis_4mom.px());
            treeOutput->v_genTopVis_py.push_back(genTopVis_4mom.py());
            treeOutput->v_genTopVis_pz.push_back(genTopVis_4mom.pz());
            treeOutput->v_genTopVis_pT.push_back(genTopVis_4mom.perp());
            treeOutput->v_genTopVis_eta.push_back(genTopVis_4mom.eta());
            treeOutput->v_genTopVis_y.push_back(genTopVis_4mom.rapidity());
            treeOutput->v_genTopVis_phi.push_back(genTopVis_4mom.phi());
            treeOutput->v_genTopVis_m.push_back(genTopVis_4mom.m());
        }
        
        
        if(std::abs(pdgId) == 24 && part.isLastCopy())
        {
            treeOutput->v_genW_id.push_back(pdgId);
            treeOutput->v_genW_E.push_back(part.energy());
            treeOutput->v_genW_px.push_back(part.px());
            treeOutput->v_genW_py.push_back(part.py());
            treeOutput->v_genW_pz.push_back(part.pz());
            treeOutput->v_genW_pT.push_back(part.pt());
            treeOutput->v_genW_eta.push_back(part.eta());
            treeOutput->v_genW_y.push_back(part.y());
            treeOutput->v_genW_phi.push_back(part.phi());
            treeOutput->v_genW_m.push_back(part.mass());
            
            int isLeptonic = Common::isLeptonicTopWZ(&part);
            
            treeOutput->v_genW_isLeptonic.push_back(isLeptonic);
            
            CLHEP::HepLorentzVector genWvis_4mom = Common::lorentzVector2clhep(Common::getVisibleCompnent(&part));
            v_genWvis_4mom.push_back(genWvis_4mom);
            
            
            if(debug)
            {
                printf(
                    "[%llu] "
                    "Gen W (isLeptonic %d) found (orig/vis): E %0.2f/%0.2f, pT %0.2f/%0.2f, eta %+0.2f/%+0.2f, phi %+0.2f/%+0.2f, "
                    "\n",
                    eventNumber,
                    (int) isLeptonic,
                    part.energy(), genWvis_4mom.e(),
                    part.pt(), genWvis_4mom.perp(),
                    part.eta(), genWvis_4mom.eta(),
                    part.phi(), genWvis_4mom.phi()
                );
            }
            
            
            treeOutput->v_genWvis_E.push_back(genWvis_4mom.e());
            treeOutput->v_genWvis_px.push_back(genWvis_4mom.px());
            treeOutput->v_genWvis_py.push_back(genWvis_4mom.py());
            treeOutput->v_genWvis_pz.push_back(genWvis_4mom.pz());
            treeOutput->v_genWvis_pT.push_back(genWvis_4mom.perp());
            treeOutput->v_genWvis_eta.push_back(genWvis_4mom.eta());
            treeOutput->v_genWvis_y.push_back(genWvis_4mom.rapidity());
            treeOutput->v_genWvis_phi.push_back(genWvis_4mom.phi());
            treeOutput->v_genWvis_m.push_back(genWvis_4mom.m());
            
            
            CLHEP::HepLorentzVector genW_lep_4mom;
            CLHEP::HepLorentzVector genW_q1_4mom;
            CLHEP::HepLorentzVector genW_q2_4mom;
            
            const reco::GenParticle *genW_lep = 0;
            const reco::GenParticle *genW_q1 = 0;
            const reco::GenParticle *genW_q2 = 0;
            
            if(isLeptonic)
            {
                genW_lep = part.daughterRef(0).get();
                
                if(std::abs(genW_lep->pdgId()) == 12 || std::abs(genW_lep->pdgId()) == 14 || std::abs(genW_lep->pdgId()) == 16)
                {
                    genW_lep = part.daughterRef(1).get();
                }
                
                genW_lep_4mom = Common::lorentzVector2clhep(genW_lep->p4());
            }
            
            else
            {
                genW_q1 = part.daughterRef(0).get();
                genW_q2 = part.daughterRef(1).get();
                
                if(genW_q1->pt() < genW_q2->pt())
                {
                    genW_q1 = part.daughterRef(1).get();
                    genW_q2 = part.daughterRef(0).get();
                }
                
                genW_q1_4mom = Common::lorentzVector2clhep(genW_q1->p4());
                genW_q2_4mom = Common::lorentzVector2clhep(genW_q2->p4());
            }
            
            v_genW_lep_4mom.push_back(genW_lep_4mom);
            v_genW_q1_4mom.push_back(genW_q1_4mom);
            v_genW_q2_4mom.push_back(genW_q2_4mom);
            
            // Fill lepton
            if(genW_lep)
            {
                treeOutput->v_genW_lep_id.push_back(genW_lep->pdgId());
                treeOutput->v_genW_lep_E.push_back(genW_lep->energy());
                treeOutput->v_genW_lep_px.push_back(genW_lep->px());
                treeOutput->v_genW_lep_py.push_back(genW_lep->py());
                treeOutput->v_genW_lep_pz.push_back(genW_lep->pz());
                treeOutput->v_genW_lep_pT.push_back(genW_lep->pt());
                treeOutput->v_genW_lep_eta.push_back(genW_lep->eta());
                treeOutput->v_genW_lep_y.push_back(genW_lep->y());
                treeOutput->v_genW_lep_phi.push_back(genW_lep->phi());
                treeOutput->v_genW_lep_m.push_back(genW_lep->mass());
            }
            
            else
            {
                treeOutput->v_genW_lep_id.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genW_lep_E.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genW_lep_px.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genW_lep_py.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genW_lep_pz.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genW_lep_pT.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genW_lep_eta.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genW_lep_y.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genW_lep_phi.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genW_lep_m.push_back(Constants::LARGEVAL_NEG);
            }
            
            
            // Fill quarks
            if(genW_q1 && genW_q2)
            {
                treeOutput->v_genW_q1_id.push_back(genW_q1->pdgId());
                treeOutput->v_genW_q1_E.push_back(genW_q1->energy());
                treeOutput->v_genW_q1_px.push_back(genW_q1->px());
                treeOutput->v_genW_q1_py.push_back(genW_q1->py());
                treeOutput->v_genW_q1_pz.push_back(genW_q1->pz());
                treeOutput->v_genW_q1_pT.push_back(genW_q1->pt());
                treeOutput->v_genW_q1_eta.push_back(genW_q1->eta());
                treeOutput->v_genW_q1_y.push_back(genW_q1->y());
                treeOutput->v_genW_q1_phi.push_back(genW_q1->phi());
                treeOutput->v_genW_q1_m.push_back(genW_q1->mass());
                
                treeOutput->v_genW_q2_id.push_back(genW_q2->pdgId());
                treeOutput->v_genW_q2_E.push_back(genW_q2->energy());
                treeOutput->v_genW_q2_px.push_back(genW_q2->px());
                treeOutput->v_genW_q2_py.push_back(genW_q2->py());
                treeOutput->v_genW_q2_pz.push_back(genW_q2->pz());
                treeOutput->v_genW_q2_pT.push_back(genW_q2->pt());
                treeOutput->v_genW_q2_eta.push_back(genW_q2->eta());
                treeOutput->v_genW_q2_y.push_back(genW_q2->y());
                treeOutput->v_genW_q2_phi.push_back(genW_q2->phi());
                treeOutput->v_genW_q2_m.push_back(genW_q2->mass());
            }
            
            else
            {
                treeOutput->v_genW_q1_id.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genW_q1_E.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genW_q1_px.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genW_q1_py.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genW_q1_pz.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genW_q1_pT.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genW_q1_eta.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genW_q1_y.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genW_q1_phi.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genW_q1_m.push_back(Constants::LARGEVAL_NEG);
                
                treeOutput->v_genW_q2_id.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genW_q2_E.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genW_q2_px.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genW_q2_py.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genW_q2_pz.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genW_q2_pT.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genW_q2_eta.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genW_q2_y.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genW_q2_phi.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genW_q2_m.push_back(Constants::LARGEVAL_NEG);
            }
        }
        
        
        if(std::abs(pdgId) == 23 && part.isLastCopy())
        {
            treeOutput->v_genZ_id.push_back(pdgId);
            treeOutput->v_genZ_E.push_back(part.energy());
            treeOutput->v_genZ_px.push_back(part.px());
            treeOutput->v_genZ_py.push_back(part.py());
            treeOutput->v_genZ_pz.push_back(part.pz());
            treeOutput->v_genZ_pT.push_back(part.pt());
            treeOutput->v_genZ_eta.push_back(part.eta());
            treeOutput->v_genZ_y.push_back(part.y());
            treeOutput->v_genZ_phi.push_back(part.phi());
            treeOutput->v_genZ_m.push_back(part.mass());
            
            int isLeptonic = Common::isLeptonicTopWZ(&part);
            
            treeOutput->v_genZ_isLeptonic.push_back(isLeptonic);
            
            CLHEP::HepLorentzVector genZ_4mom = Common::lorentzVector2clhep(part.p4());
            v_genZ_4mom.push_back(genZ_4mom);
            
            if(debug)
            {
                printf(
                    "[%llu] "
                    "Gen Z (isLeptonic %d) found: E %0.2f, pT %0.2f, eta %+0.2f, phi %+0.2f, "
                    "\n",
                    eventNumber,
                    (int) isLeptonic,
                    part.energy(),
                    part.pt(),
                    part.eta(),
                    part.phi()
                );
            }
            
            
            CLHEP::HepLorentzVector genZ_lep1_4mom;
            CLHEP::HepLorentzVector genZ_lep2_4mom;
            CLHEP::HepLorentzVector genZ_q1_4mom;
            CLHEP::HepLorentzVector genZ_q2_4mom;
            
            const reco::GenParticle *genZ_lep1 = 0;
            const reco::GenParticle *genZ_lep2 = 0;
            const reco::GenParticle *genZ_q1 = 0;
            const reco::GenParticle *genZ_q2 = 0;
            
            
            if(isLeptonic)
            {
                genZ_lep1 = part.daughterRef(0).get();
                genZ_lep2 = part.daughterRef(1).get();
                
                if(genZ_lep1->pt() < genZ_lep2->pt())
                {
                    genZ_lep1 = part.daughterRef(1).get();
                    genZ_lep2 = part.daughterRef(0).get();
                }
                
                genZ_lep1_4mom = Common::lorentzVector2clhep(genZ_lep1->p4());
                genZ_lep2_4mom = Common::lorentzVector2clhep(genZ_lep2->p4());
            }
            
            else
            {
                genZ_q1 = part.daughterRef(0).get();
                genZ_q2 = part.daughterRef(1).get();
                
                if(genZ_q1->pt() < genZ_q2->pt())
                {
                    genZ_q1 = part.daughterRef(1).get();
                    genZ_q2 = part.daughterRef(0).get();
                }
                
                genZ_q1_4mom = Common::lorentzVector2clhep(genZ_q1->p4());
                genZ_q2_4mom = Common::lorentzVector2clhep(genZ_q2->p4());
            }
            
            v_genZ_lep1_4mom.push_back(genZ_lep1_4mom);
            v_genZ_lep2_4mom.push_back(genZ_lep2_4mom);
            v_genZ_q1_4mom.push_back(genZ_q1_4mom);
            v_genZ_q2_4mom.push_back(genZ_q2_4mom);
            
            
            // Fill leptons
            if(genZ_lep1 && genZ_lep2)
            {
                treeOutput->v_genZ_lep1_id.push_back(genZ_lep1->pdgId());
                treeOutput->v_genZ_lep1_E.push_back(genZ_lep1->energy());
                treeOutput->v_genZ_lep1_px.push_back(genZ_lep1->px());
                treeOutput->v_genZ_lep1_py.push_back(genZ_lep1->py());
                treeOutput->v_genZ_lep1_pz.push_back(genZ_lep1->pz());
                treeOutput->v_genZ_lep1_pT.push_back(genZ_lep1->pt());
                treeOutput->v_genZ_lep1_eta.push_back(genZ_lep1->eta());
                treeOutput->v_genZ_lep1_y.push_back(genZ_lep1->y());
                treeOutput->v_genZ_lep1_phi.push_back(genZ_lep1->phi());
                treeOutput->v_genZ_lep1_m.push_back(genZ_lep1->mass());
                
                treeOutput->v_genZ_lep2_id.push_back(genZ_lep2->pdgId());
                treeOutput->v_genZ_lep2_E.push_back(genZ_lep2->energy());
                treeOutput->v_genZ_lep2_px.push_back(genZ_lep2->px());
                treeOutput->v_genZ_lep2_py.push_back(genZ_lep2->py());
                treeOutput->v_genZ_lep2_pz.push_back(genZ_lep2->pz());
                treeOutput->v_genZ_lep2_pT.push_back(genZ_lep2->pt());
                treeOutput->v_genZ_lep2_eta.push_back(genZ_lep2->eta());
                treeOutput->v_genZ_lep2_y.push_back(genZ_lep2->y());
                treeOutput->v_genZ_lep2_phi.push_back(genZ_lep2->phi());
                treeOutput->v_genZ_lep2_m.push_back(genZ_lep2->mass());
            }
            
            else
            {
                treeOutput->v_genZ_lep1_id.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_lep1_E.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_lep1_px.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_lep1_py.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_lep1_pz.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_lep1_pT.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_lep1_eta.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_lep1_y.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_lep1_phi.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_lep1_m.push_back(Constants::LARGEVAL_NEG);
                
                treeOutput->v_genZ_lep2_id.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_lep2_E.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_lep2_px.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_lep2_py.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_lep2_pz.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_lep2_pT.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_lep2_eta.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_lep2_y.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_lep2_phi.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_lep2_m.push_back(Constants::LARGEVAL_NEG);
            }
            
            // Fill quarks
            if(genZ_q1 && genZ_q2)
            {
                treeOutput->v_genZ_q1_id.push_back(genZ_q1->pdgId());
                treeOutput->v_genZ_q1_E.push_back(genZ_q1->energy());
                treeOutput->v_genZ_q1_px.push_back(genZ_q1->px());
                treeOutput->v_genZ_q1_py.push_back(genZ_q1->py());
                treeOutput->v_genZ_q1_pz.push_back(genZ_q1->pz());
                treeOutput->v_genZ_q1_pT.push_back(genZ_q1->pt());
                treeOutput->v_genZ_q1_eta.push_back(genZ_q1->eta());
                treeOutput->v_genZ_q1_y.push_back(genZ_q1->y());
                treeOutput->v_genZ_q1_phi.push_back(genZ_q1->phi());
                treeOutput->v_genZ_q1_m.push_back(genZ_q1->mass());
                
                treeOutput->v_genZ_q2_id.push_back(genZ_q2->pdgId());
                treeOutput->v_genZ_q2_E.push_back(genZ_q2->energy());
                treeOutput->v_genZ_q2_px.push_back(genZ_q2->px());
                treeOutput->v_genZ_q2_py.push_back(genZ_q2->py());
                treeOutput->v_genZ_q2_pz.push_back(genZ_q2->pz());
                treeOutput->v_genZ_q2_pT.push_back(genZ_q2->pt());
                treeOutput->v_genZ_q2_eta.push_back(genZ_q2->eta());
                treeOutput->v_genZ_q2_y.push_back(genZ_q2->y());
                treeOutput->v_genZ_q2_phi.push_back(genZ_q2->phi());
                treeOutput->v_genZ_q2_m.push_back(genZ_q2->mass());
            }
            
            else
            {
                treeOutput->v_genZ_q1_id.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_q1_E.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_q1_px.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_q1_py.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_q1_pz.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_q1_pT.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_q1_eta.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_q1_y.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_q1_phi.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_q1_m.push_back(Constants::LARGEVAL_NEG);
                
                treeOutput->v_genZ_q2_id.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_q2_E.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_q2_px.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_q2_py.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_q2_pz.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_q2_pT.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_q2_eta.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_q2_y.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_q2_phi.push_back(Constants::LARGEVAL_NEG);
                treeOutput->v_genZ_q2_m.push_back(Constants::LARGEVAL_NEG);
            }
        }
    }
    
    treeOutput->genTop_n = treeOutput->v_genTop_id.size();
    treeOutput->genW_n = treeOutput->v_genW_id.size();
    treeOutput->genZ_n = treeOutput->v_genZ_id.size();
    
    
    //// Sort the electrons
    //std::sort(
    //    treeOutput->v_genEl_HGCalEEP_EsortedIndex.begin(), treeOutput->v_genEl_HGCalEEP_EsortedIndex.end(),
    //    [&](int iEle1, int iEle2)
    //    {
    //        return (treeOutput->v_genEl_E[iEle1] > treeOutput->v_genEl_E[iEle2]);
    //    }
    //);
    
    
    // PV
    edm::Handle <std::vector <reco::Vertex> > handle_primaryVertex;
    iEvent.getByToken(tok_primaryVertex, handle_primaryVertex);
    const auto &v_primaryVertex = *handle_primaryVertex;
    
    int iPV = -1;
    int pmVtx_idx = -1;
    int nGoodVertex = 0;
    reco::Vertex pmVtx;
    
    //for(int iVtx = 0; iVtx < (int) v_primaryVertex->size(); iVtx++)
    for(const auto &vertex : v_primaryVertex)
    {
        iPV++;
        
        bool isGoodVertex = (
            !vertex.isFake() &&
            vertex.ndof() >= 4 &&
            fabs(vertex.z()) <= 24.0 &&
            fabs(vertex.position().rho()) <= 2.0
        );
        
        nGoodVertex += (int) isGoodVertex;
        
        // The first good vertex
        if(pmVtx_idx < 0 && nGoodVertex == 1)
        {
            pmVtx_idx = iPV;
            pmVtx = vertex;
        }
    }
    
    
    // SV
    edm::Handle <std::vector <reco::VertexCompositePtrCandidate> > handle_secondaryVertex;
    iEvent.getByToken(tok_secondaryVertex, handle_secondaryVertex);
    const auto &v_secondaryVertex = *handle_secondaryVertex;
    
    int iSV = -1;
    int nSecVtx = 0;
    
    std::vector <math::XYZVectorD> v_secVtxDir;
    
    for(const auto &sv : v_secondaryVertex)
    {
        iSV++;
        
        //VertexDistance3D vertTool;
        //double distance = vertTool.distance(sv, pmVtx).value();
        //double dist_err = vertTool.distance(sv, pmVtx).error();
        
        //if(nGoodVertex && sv.vertexNdof() >= 4)
        if(nGoodVertex)
        {
            math::XYZVectorD xyz_secVtxDir = sv.position() - pmVtx.position();
            
            v_secVtxDir.push_back(xyz_secVtxDir);
            
            if(debug)
            {
                printf(
                    "[%llu] "
                    "SV (%d) found: "
                    "(x, y, z) (%0.4f, %0.4f, %0.4f), "
                    "(vx, vy, vz) (%0.4f, %0.4f, %0.4f), "
                    "flight dist %f, ndof %f, chi2/ndof %f, "
                    "\n",
                    eventNumber,
                    iSV,
                    sv.position().x(), sv.position().y(), sv.position().z(),
                    sv.vx(), sv.vy(), sv.vz(),
                    std::sqrt(xyz_secVtxDir.mag2()), sv.vertexNdof(), sv.vertexNormalizedChi2()
                );
            }
        }
        
        nSecVtx++;
    }
    
    treeOutput->sv_n = nSecVtx;
    
    
    // Pileup
    edm::Handle <std::vector <PileupSummaryInfo> > pileUps_reco;
    iEvent.getByToken(tok_pileup, pileUps_reco);
    treeOutput->pileup_n = Common::getPileup(pileUps_reco);
    
    
    // Rho
    edm::Handle <double> handle_rho;
    iEvent.getByToken(tok_rho, handle_rho);
    double rho = *handle_rho;
    
    treeOutput->rho = rho;
    
    
    // Electrons
    edm::Handle <std::vector <pat::Electron> > handle_electron_reco;
    iEvent.getByToken(tok_electron_reco, handle_electron_reco);
    auto electrons_reco = *handle_electron_reco;
    
    int nEle = 0;
    
    std::vector <CLHEP::HepLorentzVector> v_ele_4mom;
    
    for(const auto &ele : electrons_reco)
    {
        edm::Ptr <pat::Electron> elePtr(handle_electron_reco, nEle);
        
        nEle++;
        
        CLHEP::HepLorentzVector ele_4mom = Common::lorentzVector2clhep(ele.p4());
        v_ele_4mom.push_back(ele_4mom);
        
        auto sc = ele.superCluster();
        
        if(debug)
        {
            printf(
                "[%llu] "
                "ele (%d) found: E %0.2f, pT %0.2f, eta %+0.2f, phi %+0.2f, "
                "SC E %0.2f, eta %+0.2f, phi %+0.2f"
                "\n",
                eventNumber,
                nEle,
                ele.energy(), ele.pt(), ele.eta(), ele.phi(),
                sc->energy(), sc->eta(), sc->phi()
            );
        }
        
        
        //std::vector <float> extraVariables = eleMvaVarHelper.getAuxVariables(elePtr, iEvent);
        //
        //for(int iVar = 0; iVar < eleMvaVarManager.getNVars(); iVar++)
        //{
        //    printf("%s %0.4f, ", eleMvaVarManager.getName(iVar).c_str(), eleMvaVarManager.getValue(iVar, ele, extraVariables));
        //}
        //printf("\n");
    }
    
    
    // Muons
    edm::Handle <std::vector <pat::Muon> > handle_muon_reco;
    iEvent.getByToken(tok_muon_reco, handle_muon_reco);
    auto muons_reco = *handle_muon_reco;
    
    int nMu = 0;
    
    std::vector <CLHEP::HepLorentzVector> v_mu_4mom;
    
    for(const auto &mu : muons_reco)
    {
        nMu++;
        
        if(debug)
        {
            printf(
                "[%llu] "
                "mu (%d) found: E %0.2f, pT %0.2f, eta %+0.2f, phi %+0.2f, "
                "\n",
                eventNumber,
                nMu,
                mu.energy(), mu.pt(), mu.eta(), mu.phi()
            );
        }
    }
    
    
    int iJetCollection = -1;
    
    for(const auto &jetName : v_jetCollectionName)
    {
        iJetCollection++;
        
        if(treeOutput->m_jetInfo.find(jetName) == treeOutput->m_jetInfo.end())
        {
            printf("Error in analyze(...): Key \"%s\" not found in JetInfo map. Add it to the map first. Exiting...", jetName.c_str());
            exit(EXIT_FAILURE);
        }
        
        const auto &jetInfo = treeOutput->m_jetInfo[jetName];
        
        edm::Handle <std::vector <pat::Jet> > handle_jet_reco;
        //iEvent.getByToken(v_tok_jet_reco.at(iJetCollection), handle_jet_reco);
        iEvent.getByToken(jetInfo->tok_jet, handle_jet_reco);
        auto jets_reco = *handle_jet_reco;
        
        int iJet = -1;
        int nJet = 0;
        
        std::vector <CLHEP::HepLorentzVector> v_jet_4mom;
        
        for(const auto &jet : jets_reco)
        {
            iJet++;
            
            if(jet.pt() < jetInfo->minPt)
            {
                continue;
            }
            
            nJet++;
            
            //edm::Ptr <pat::Jet> jetPtr(handle_jet_reco, iJet);
            //const reco::PFJet *cj = dynamic_cast<const reco::PFJet *>(jetPtr.get());
            ////pat::PFCandidateFwdPtrCollection iparticlesRef;
            //std::vector<reco::PFCandidatePtr> iparticles = cj->getPFConstituents();
            
            if(debug)
            {
                printf(
                    "[%llu] "
                    "%s jet (%d) found: E %0.2f, pT %0.2f, eta %+0.2f, phi %+0.2f, "
                    "isPF %d, "
                    "nConsti %d, nDaughter %d, "
                    //"%d, "
                    "\n",
                    eventNumber,
                    jetName.c_str(),
                    nJet,
                    jet.energy(), jet.pt(), jet.eta(), jet.phi(),
                    (int) jet.isPFJet(),
                    (int) jet.getJetConstituents().size(), (int) jet.numberOfDaughters()
                    //(jet.isPFJet()? (int) jet.getPFConstituents().size() : -1),
                    //jet.isPFJet()
                    //(int) jet.pfCandidatesFwdPtr().size(),
                    //(int) jet.pfCandidatesFwdPtr().size()
                    //(int) iparticles.size()
                );
                
                //printf(
                //    "mEmEnergyInEB %0.2f, "
                //    "mEmEnergyInEE %0.2f, "
                //    "mHadEnergyInHB %0.2f, "
                //    "mHadEnergyInHE %0.2f, "
                //    "mMaxEInEmTowers %0.2f, "
                //    "mMaxEInHadTowers %0.2f, "
                //    "mTowersArea %0.2f, "
                //    "\n",
                //    jet.caloSpecific().mEmEnergyInEB,
                //    jet.caloSpecific().mEmEnergyInEE,
                //    jet.caloSpecific().mHadEnergyInHB,
                //    jet.caloSpecific().mHadEnergyInHE,
                //    jet.caloSpecific().mMaxEInEmTowers,
                //    jet.caloSpecific().mMaxEInHadTowers,
                //    jet.caloSpecific().mTowersArea
                //);
            }
            
            std::vector <fastjet::PseudoJet> fj_input_jet;
            
            auto const &v_jet_consti = jet.getJetConstituents();
            
            //std::vector <int> v_jet_consti_PtSortedIdx(v_jet_consti.size());
            //std::iota(v_jet_consti_PtSortedIdx.begin(), v_jet_consti_PtSortedIdx.end(), 0);
            //
            //std::sort(
            //    v_jet_consti_PtSortedIdx.begin(), v_jet_consti_PtSortedIdx.end(),
            //    [&](int idx1, int idx2)
            //    {
            //        return (v_jet_consti[idx1]->pt() > v_jet_consti[idx2]->pt());
            //    }
            //);
            
            int iConsti = -1;
            int consti_n = 0;
            double constiE_sum = 0;
            
            for(auto const &consti : v_jet_consti)
            //for(int &sortedIdx : v_jet_consti_PtSortedIdx)
            {
                iConsti++;
                
                //auto const &consti = v_jet_consti.at(sortedIdx);
                
                fastjet::PseudoJet fj_pseudoJet(
                    consti->px(),
                    consti->py(),
                    consti->pz(),
                    consti->energy()
                );
                
                fj_pseudoJet.set_user_index(iConsti);
                //fj_pseudoJet.set_user_index(sortedIdx);
                
                fj_input_jet.push_back(fj_pseudoJet);
                
                consti_n++;
                constiE_sum += consti->energy();
                
                //printf("    consti %d/%d: sortedIdx %d, pT %0.2f, \n", iConsti, (int) v_jet_consti.size(), sortedIdx, consti->pt());
            }
            
            fastjet::ClusterSequence fj_jet_clustSeq(fj_input_jet, *fj_akJetReclusterDef);
            std::vector <fastjet::PseudoJet> fj_jets = fj_jet_clustSeq.inclusive_jets();
            fastjet::PseudoJet fj_jet = fj_jets.at(0);
            
            
            // For soft-drop
            fastjet::PseudoJet fj_jet_softDrop = fj_jet;
            
            if(jetInfo->apply_sd)
            {
                double sd_zcut = jetInfo->sd_zcut;
                double sd_beta = jetInfo->sd_beta;
                double sd_R0   = jetInfo->sd_R0;
                fastjet::contrib::SoftDrop fj_softDrop(sd_beta, sd_zcut, sd_R0);
                
                fj_jet_softDrop = fj_softDrop(fj_jet_softDrop);
            }
            
            
            fastjet::PseudoJet fj_jet_raw = fj_jet;
            fj_jet = fj_jet_softDrop;
            
            CLHEP::HepLorentzVector jet_raw_4mom = Common::PseudoJetToHepLorentzVector(fj_jet_raw);
            
            jetInfo->v_jet_raw_E_reco.push_back(jet_raw_4mom.e());
            jetInfo->v_jet_raw_px_reco.push_back(jet_raw_4mom.px());
            jetInfo->v_jet_raw_py_reco.push_back(jet_raw_4mom.py());
            jetInfo->v_jet_raw_pz_reco.push_back(jet_raw_4mom.pz());
            jetInfo->v_jet_raw_pT_reco.push_back(jet_raw_4mom.perp());
            jetInfo->v_jet_raw_eta_reco.push_back(jet_raw_4mom.eta());
            jetInfo->v_jet_raw_y_reco.push_back(jet_raw_4mom.rapidity());
            jetInfo->v_jet_raw_phi_reco.push_back(jet_raw_4mom.phi());
            jetInfo->v_jet_raw_m_reco.push_back(jet_raw_4mom.m());
            
            CLHEP::HepLorentzVector jet_4mom = Common::PseudoJetToHepLorentzVector(fj_jet);
            v_jet_4mom.push_back(jet_4mom);
            
            jetInfo->v_jet_E_reco.push_back(jet_4mom.e());
            jetInfo->v_jet_px_reco.push_back(jet_4mom.px());
            jetInfo->v_jet_py_reco.push_back(jet_4mom.py());
            jetInfo->v_jet_pz_reco.push_back(jet_4mom.pz());
            jetInfo->v_jet_pT_reco.push_back(jet_4mom.perp());
            jetInfo->v_jet_eta_reco.push_back(jet_4mom.eta());
            jetInfo->v_jet_y_reco.push_back(jet_4mom.rapidity());
            jetInfo->v_jet_phi_reco.push_back(jet_4mom.phi());
            jetInfo->v_jet_m_reco.push_back(jet_4mom.m());
            
            
            // Secondary vertex stuff
            int iSV = -1;
            std::vector <const reco::VertexCompositePtrCandidate*> v_secVtx_inJet;
            
            std::vector <double> v_jet_sv_pT_reco;
            std::vector <double> v_jet_sv_eta_reco;
            std::vector <double> v_jet_sv_phi_reco;
            std::vector <double> v_jet_sv_m_reco;
            std::vector <double> v_jet_sv_E_reco;
            std::vector <double> v_jet_sv_etarel_reco;
            std::vector <double> v_jet_sv_phirel_reco;
            std::vector <double> v_jet_sv_deltaR_reco;
            std::vector <double> v_jet_sv_ntracks_reco;
            std::vector <double> v_jet_sv_chi2_reco;
            std::vector <double> v_jet_sv_ndf_reco;
            std::vector <double> v_jet_sv_normchi2_reco;
            std::vector <double> v_jet_sv_dxy_reco;
            std::vector <double> v_jet_sv_dxyerr_reco;
            std::vector <double> v_jet_sv_dxysig_reco;
            std::vector <double> v_jet_sv_d3d_reco;
            std::vector <double> v_jet_sv_d3derr_reco;
            std::vector <double> v_jet_sv_d3dsig_reco;
            std::vector <double> v_jet_sv_costhetasvpv_reco;
            
            // Following: https://github.com/CMSDeepFlavour/DeepNTuples/blob/master/DeepNtuplizer/src/ntuple_SV.cc
            for(const auto &sv : v_secondaryVertex)
            {
                iSV++;
                
                //math::XYZTLorentzVectorD lv_temp(jet_4mom.px(), jet_4mom.py(), jet_4mom.pz(), jet_4mom.e());
                
                //double secVtxDR = ROOT::Math::VectorUtil::DeltaR(v_secVtxDir.at(iSV), lv_temp);
                
                //printf("dR(jet %d, sv %d) %f \n", nJet, iSV+1, secVtxDR);
                
                // A somewhat relaxed threshold
                //if(secVtxDR < jet.maxDistance() * 1.5)
                if(nGoodVertex && reco::deltaR(sv, jet) < jetInfo->rParam)
                {
                    v_secVtx_inJet.push_back(&sv);
                    
                    v_jet_sv_pT_reco.push_back(                                 sv.pt());
                    v_jet_sv_eta_reco.push_back(                                sv.eta());
                    v_jet_sv_phi_reco.push_back(                                sv.phi());
                    v_jet_sv_m_reco.push_back(                                  sv.mass());
                    v_jet_sv_E_reco.push_back(                                  sv.energy());
                    v_jet_sv_etarel_reco.push_back(                             std::fabs(sv.eta()-jet.eta()));
                    v_jet_sv_phirel_reco.push_back(                             std::fabs(reco::deltaPhi(sv.phi(), jet.phi())));
                    v_jet_sv_deltaR_reco.push_back(                             reco::deltaR(sv, jet));
                    v_jet_sv_ntracks_reco.push_back(                            sv.numberOfDaughters());
                    v_jet_sv_chi2_reco.push_back(                               sv.vertexChi2());
                    v_jet_sv_ndf_reco.push_back(                                sv.vertexNdof());
                    v_jet_sv_normchi2_reco.push_back(                           Common::catchInfsAndBound(sv.vertexNormalizedChi2(), 1000, -1000, 1000));
                    v_jet_sv_dxy_reco.push_back(                                Common::vertexDxy(sv, pmVtx).value());
                    v_jet_sv_dxyerr_reco.push_back(                             Common::catchInfsAndBound(Common::vertexDxy(sv, pmVtx).error()-2, 0, -2, 0));
                    v_jet_sv_dxysig_reco.push_back(                             Common::catchInfsAndBound(Common::vertexDxy(sv, pmVtx).value()/Common::vertexDxy(sv, pmVtx).error() , 0, -1, 800));
                    v_jet_sv_d3d_reco.push_back(                                Common::vertexD3d(sv, pmVtx).value());
                    v_jet_sv_d3derr_reco.push_back(                             Common::catchInfsAndBound(Common::vertexD3d(sv, pmVtx).error()-2, 0, -2, 0));
                    v_jet_sv_d3dsig_reco.push_back(                             Common::catchInfsAndBound(Common::vertexD3d(sv, pmVtx).value()/Common::vertexD3d(sv, pmVtx).error(), 0, -1, 800));
                    v_jet_sv_costhetasvpv_reco.push_back(                       Common::vertexDdotP(sv, pmVtx)); // the pointing angle (i.e. the angle between the sum of the momentum
                }
            }
            
            jetInfo->v_jet_nSecVtxInJet_reco.push_back(v_secVtx_inJet.size());
            
            jetInfo->vv_jet_sv_pT_reco.push_back(v_jet_sv_pT_reco);
            jetInfo->vv_jet_sv_eta_reco.push_back(v_jet_sv_eta_reco);
            jetInfo->vv_jet_sv_phi_reco.push_back(v_jet_sv_phi_reco);
            jetInfo->vv_jet_sv_m_reco.push_back(v_jet_sv_m_reco);
            jetInfo->vv_jet_sv_E_reco.push_back(v_jet_sv_E_reco);
            jetInfo->vv_jet_sv_etarel_reco.push_back(v_jet_sv_etarel_reco);
            jetInfo->vv_jet_sv_phirel_reco.push_back(v_jet_sv_phirel_reco);
            jetInfo->vv_jet_sv_deltaR_reco.push_back(v_jet_sv_deltaR_reco);
            jetInfo->vv_jet_sv_ntracks_reco.push_back(v_jet_sv_ntracks_reco);
            jetInfo->vv_jet_sv_chi2_reco.push_back(v_jet_sv_chi2_reco);
            jetInfo->vv_jet_sv_ndf_reco.push_back(v_jet_sv_ndf_reco);
            jetInfo->vv_jet_sv_normchi2_reco.push_back(v_jet_sv_normchi2_reco);
            jetInfo->vv_jet_sv_dxy_reco.push_back(v_jet_sv_dxy_reco);
            jetInfo->vv_jet_sv_dxyerr_reco.push_back(v_jet_sv_dxyerr_reco);
            jetInfo->vv_jet_sv_dxysig_reco.push_back(v_jet_sv_dxysig_reco);
            jetInfo->vv_jet_sv_d3d_reco.push_back(v_jet_sv_d3d_reco);
            jetInfo->vv_jet_sv_d3derr_reco.push_back(v_jet_sv_d3derr_reco);
            jetInfo->vv_jet_sv_d3dsig_reco.push_back(v_jet_sv_d3dsig_reco);
            jetInfo->vv_jet_sv_costhetasvpv_reco.push_back(v_jet_sv_costhetasvpv_reco);
            
            
            fastjet::PseudoJet fj_subStruc = fj_jet;
            
            // N-subjettiness
            double tauNm1 = 1;
            
            for(int iTauN = 0; iTauN <= jetInfo->maxTauN; iTauN++)
            {
                double tauN = 1;
                double tauNratio = 0;
                
                if(iTauN)
                {
                    fastjet::contrib::Nsubjettiness nSubjettiness(
                        iTauN,
                        fastjet::contrib::OnePass_KT_Axes(),
                        fastjet::contrib::UnnormalizedMeasure(1.0)
                    );
                    
                    tauN = nSubjettiness.result(fj_subStruc);
                    
                    if(tauNm1)
                    {
                        tauNratio = tauN / tauNm1;
                    }
                }
                
                jetInfo->vv_jet_tauN_reco.at(iTauN).push_back(tauN);
                jetInfo->vv_jet_tauNratio_reco.at(iTauN).push_back(tauNratio);
                
                //printf(
                //    "Fat jet %d: "
                //    "tau%d (ratio) %0.2f (%0.2f) "
                //    "\n",
                //    
                //    nJet,
                //    iTauN, tauN, tauNratio
                //);
                
                tauNm1 = tauN;
            }
            
            //printf("Starting image stuff... \n");
            
            
            // For jet image formation
            fastjet::PseudoJet fj_image = fj_jet;
            
            // Cluster into exactly jets
            // If there are fewer than 3, returns the constituents
            fastjet::ClusterSequence fj_jetExcSubJet_clustSeq(fj_image.constituents(), *fj_fatJetExcSubJetDef);
            std::vector <fastjet::PseudoJet> fj_jetExcSubJets = fj_jetExcSubJet_clustSeq.exclusive_jets_up_to(3);
            fj_jetExcSubJets = sorted_by_E(fj_jetExcSubJets);
            
            int nConsti = fj_image.constituents().size();
            int nFatJetExcSubJet = fj_jetExcSubJets.size();
            
            jetInfo->v_jet_nConsti_reco.push_back(nConsti);
            
            TVectorD direc1(2);
            TVectorD direc2(2);
            TVectorD finalTranslation(2);
            
            finalTranslation(0) = fj_image.eta() - fj_jetExcSubJets.at(0).eta();
            finalTranslation(1) = fj_jetExcSubJets.at(0).delta_phi_to(fj_image);
            
            std::vector <fastjet::PseudoJet> v_GSaxis;
            
            v_GSaxis.push_back(fj_image);
            
            if(nFatJetExcSubJet >= 2)
            {
                direc1(0) = fj_jetExcSubJets.at(1).eta() - fj_jetExcSubJets.at(0).eta();
                direc1(1) = fj_jetExcSubJets.at(0).delta_phi_to(fj_jetExcSubJets.at(1));
                
                v_GSaxis.push_back(fj_jetExcSubJets.at(0));
            }
            
            else
            {
                v_GSaxis.push_back(fastjet::PseudoJet(0, 0, 0, 0));
            }
            
            
            if(nFatJetExcSubJet >= 3)
            {
                direc2(0) = fj_jetExcSubJets.at(2).eta() - fj_jetExcSubJets.at(0).eta();
                direc2(1) = fj_jetExcSubJets.at(0).delta_phi_to(fj_jetExcSubJets.at(2));
                
                v_GSaxis.push_back(fj_jetExcSubJets.at(1));
            }
            
            else
            {
                v_GSaxis.push_back(fastjet::PseudoJet(0, 0, 0, 0));
            }
            
            
            // Rotation in pt-eta plane
            std::vector <std::vector <double> > v_consti_dEta_dPhi_transformed = Common::getTransformedDetaDphi(
                fj_image.constituents(),
                
                fj_jetExcSubJets.at(0),
                //fj_image,
                
                direc1,
                direc2,
                finalTranslation
            );
            
            
            // GS transform
            std::vector <CLHEP::HepLorentzVector> v_consti_boosted = Common::getGStranformed4mom(
                v_GSaxis,
                fj_image.constituents()
            );
            
            CLHEP::HepLorentzVector jet_4mom_boosted = Common::getHepLorentzVectorSum(v_consti_boosted);
            
            // Rescale
            // NOTE: Do not use jet_4mom_boosted.m() as it can occasionally be zero (due to precision) if jet_4mom.m() is very small
            // Also, very rarely, the mass can be a very small -ve value. Hence use fabs().
            double rescaleFactor = jetInfo->jetRescale_m0 / std::fabs(jet_4mom.m());
            jet_4mom_boosted *= rescaleFactor;
            
            double boostDir = -1;
            
            if(jet_4mom_boosted.e() < jetInfo->jetLorentzBoost_e0)
            {
                boostDir *= -1;
            }
            
            // Boost
            double boostGamma = 1.0/(jetInfo->jetRescale_m0*jetInfo->jetRescale_m0) * (
                jet_4mom_boosted.e() * jetInfo->jetLorentzBoost_e0 -
                jetInfo->jetLorentzBoost_p0 * jet_4mom_boosted.v().mag()
            );
            
            double boostBeta = boostDir * std::sqrt(1.0 - 1.0/(boostGamma*boostGamma));
            jet_4mom_boosted.boostX(boostBeta);
            
            
            // Rescale and boost the constituents
            //#pragma omp parallel for
            for(int iConsti = 0; iConsti < nConsti; iConsti++)
            {
                v_consti_boosted.at(iConsti) *= rescaleFactor;
                v_consti_boosted.at(iConsti).boostX(boostBeta);
            }
            
            CLHEP::HepLorentzVector jet_4mom_boosted_sumConsti = Common::getHepLorentzVectorSum(v_consti_boosted);
            
            std::vector <double> v_jet_consti_E_reco;
            std::vector <double> v_jet_consti_px_reco;
            std::vector <double> v_jet_consti_py_reco;
            std::vector <double> v_jet_consti_pz_reco;
            std::vector <double> v_jet_consti_pT_reco;
            std::vector <double> v_jet_consti_eta_reco;
            std::vector <double> v_jet_consti_phi_reco;
            std::vector <double> v_jet_consti_m_reco;
            
            std::vector <double> v_jet_consti_id_reco;
            
            std::vector <double> v_jet_consti_vx_reco;
            std::vector <double> v_jet_consti_vy_reco;
            std::vector <double> v_jet_consti_vz_reco;
            std::vector <double> v_jet_consti_v2d_reco;
            std::vector <double> v_jet_consti_v3d_reco;
            
            std::vector <double> v_jet_consti_pvdxy_reco;
            std::vector <double> v_jet_consti_pvdz_reco;
            
            std::vector <double> v_jet_consti_svdxy_reco;
            std::vector <double> v_jet_consti_svdz_reco;
            
            std::vector <double> v_jet_consti_dEta_reco;
            std::vector <double> v_jet_consti_dPhi_reco;
            
            std::vector <double> v_jet_consti_EtaPhiRot_dEta_reco;
            std::vector <double> v_jet_consti_EtaPhiRot_dPhi_reco;
            
            std::vector <double> v_jet_consti_LBGS_x_reco;
            std::vector <double> v_jet_consti_LBGS_y_reco;
            
            std::vector <double> v_jet_consti_enFrac_reco;
            
            std::vector <double> v_jet_consti_pTwrtJet_reco;
            std::vector <double> v_jet_consti_dRwrtJet_reco;
            
            
            std::unordered_map <std::string, std::vector <double> > m_jet_consti_electronInfo_reco;
            
            for(int iVar = 0; iVar < eleMvaVarManager.getNVars(); iVar++)
            {
                std::string varName = eleMvaVarManager.getName(iVar);
                
                std::vector <double> v_temp(nConsti, Constants::DEFAULT_BRANCH_ENTRY);
                m_jet_consti_electronInfo_reco[varName] = v_temp;
            }
            
            std::unordered_map <std::string, std::vector <double> > m_jet_consti_muonInfo_reco;
            
            for(int iVar = 0; iVar < muMvaVarManager.getNVars(); iVar++)
            {
                std::string varName = muMvaVarManager.getName(iVar);
                
                std::vector <double> v_temp(nConsti, Constants::DEFAULT_BRANCH_ENTRY);
                m_jet_consti_muonInfo_reco[varName] = v_temp;
            }
            
            
            //int iEle = 0;
            //std::vector v_jet_consti_nearestEleIdx;
            //
            //for(const auto &ele : electrons_reco)
            //{
            //    iEle++;
            //    
            //    int nearestEleIdx = -1;
            //    double minDR = 9999;
            //    nearest
            //    
            //    for(int iConsti = 0; iConsti < nConsti; iConsti++)
            //    {
            //        int idx = pseudoJet_consti.user_index();
            //        const auto &consti = v_jet_consti.at(idx);
            //        
            //        double dR = ROOT::Math::VectorUtil::DeltaR(ele.p4(), consti->p4());
            //        
            //        if(dR < minDR)
            //        {
            //            nearestEleIdx = iEle;
            //            minDR = dR;
            //        }
            //    }
            //}
            
            
            ////std::vector <fastjet::PseudoJet> v_fj_consti_sortedByPt = sorted_by_pt(fj_image.constituents());
            
            std::vector <int> v_jet_consti_PtSortedIdx(nConsti);
            std::iota(v_jet_consti_PtSortedIdx.begin(), v_jet_consti_PtSortedIdx.end(), 0);
            
            std::sort(
                v_jet_consti_PtSortedIdx.begin(), v_jet_consti_PtSortedIdx.end(),
                [&](int idx1, int idx2)
                {
                    return (fj_image.constituents()[idx1].pt() > fj_image.constituents()[idx2].pt());
                }
            );
            
            
            int nMatchedEl = 0;
            int nMatchedMu = 0;
            
            //for(int iConsti = 0; iConsti < nConsti; iConsti++)
            for(int iConsti : v_jet_consti_PtSortedIdx)
            {
                ////fastjet::PseudoJet pseudoJet_consti = v_fj_consti_sortedByPt.at(iConsti);
                fastjet::PseudoJet pseudoJet_consti = fj_image.constituents().at(iConsti);
                int idx = pseudoJet_consti.user_index();
                const auto &consti = v_jet_consti.at(idx);
                
                const pat::PackedCandidate* consti_pc = dynamic_cast<const pat::PackedCandidate*>(consti.get());
                //const pat::PackedCandidate* consti_pc = dynamic_cast<const pat::PackedCandidate*>(jet.daughter(idx));
                
                if(debug)
                {
                    printf("    consti idx %d (total %d): user_index %d, pT %0.2f, \n", iConsti, (int) nConsti, idx, consti->pt());
                    //printf("    hcalFraction %0.4f, \n", consti_pc->hcalFraction());
                    //printf("    puppiWeight %0.4f, \n", consti_pc->puppiWeight());
                    //printf("    pvAssociationQuality %0.4f, \n", (double) consti_pc->pvAssociationQuality());
                    //printf("    vertexMass %0.4f, \n", consti_pc->vertexRef()->p4().M());
                }
                
                double x_LBGS = v_consti_boosted.at(iConsti).py() / v_consti_boosted.at(iConsti).e();
                double y_LBGS = v_consti_boosted.at(iConsti).pz() / v_consti_boosted.at(iConsti).e();
                double enFrac = v_consti_boosted.at(iConsti).e() / jetInfo->jetLorentzBoost_e0;
                
                //edm::Ptr <reco::PFCandidate> constiPF(consti);
                //std::cout << iConsti << " " << constiPF.isNonnull() << "\n"; std::fflush(stdout);
                //std::cout << iConsti << " " << constiPF->gsfElectronRef().isNonnull() << "\n"; std::fflush(stdout);
                
                //In the rare cases that a jet as < 3 constituents, the ratio can slightly exceed 1 due to precision, etc.
                enFrac = std::min(enFrac, 1.0);
                
                if(fabs(x_LBGS) > 1 || fabs(y_LBGS) > 1 || fabs(enFrac) > 1)
                {
                    std::cout << x_LBGS << ", " << y_LBGS << ", " << enFrac << "\n";
                }
                
                v_jet_consti_dEta_reco.push_back(consti->eta() - jet_4mom.eta());
                v_jet_consti_dPhi_reco.push_back(reco::deltaPhi(consti->phi(), jet_4mom.phi()));
                
                v_jet_consti_EtaPhiRot_dEta_reco.push_back(v_consti_dEta_dPhi_transformed.at(iConsti).at(0));
                v_jet_consti_EtaPhiRot_dPhi_reco.push_back(v_consti_dEta_dPhi_transformed.at(iConsti).at(1));
                
                v_jet_consti_LBGS_x_reco.push_back(x_LBGS);
                v_jet_consti_LBGS_y_reco.push_back(y_LBGS);
                
                v_jet_consti_enFrac_reco.push_back(enFrac);
                
                v_jet_consti_E_reco.push_back(consti->energy());
                v_jet_consti_px_reco.push_back(consti->px());
                v_jet_consti_py_reco.push_back(consti->py());
                v_jet_consti_pz_reco.push_back(consti->pz());
                v_jet_consti_pT_reco.push_back(consti->pt());
                v_jet_consti_eta_reco.push_back(consti->eta());
                v_jet_consti_phi_reco.push_back(consti->phi());
                v_jet_consti_m_reco.push_back(consti->mass());
                v_jet_consti_id_reco.push_back(consti->pdgId());
                
                v_jet_consti_vx_reco.push_back(consti->vx());
                v_jet_consti_vy_reco.push_back(consti->vy());
                v_jet_consti_vz_reco.push_back(consti->vz());
                v_jet_consti_v2d_reco.push_back(std::sqrt(consti->vertex().perp2()));
                v_jet_consti_v3d_reco.push_back(std::sqrt(consti->vertex().mag2()));
                
                // wrt PV
                double pvdxy = -1;
                double pvdz = -1;
                
                if(consti->bestTrack() && nGoodVertex)
                {
                    pvdxy = std::fabs(consti->bestTrack()->dxy(pmVtx.position()));
                    pvdz = std::fabs(consti->bestTrack()->dz(pmVtx.position()));
                }
                
                if(!std::isnan(pvdxy) && !std::isinf(pvdxy) && !std::isnan(pvdz) && !std::isinf(pvdz))
                {
                    v_jet_consti_pvdxy_reco.push_back(pvdxy);
                    v_jet_consti_pvdz_reco.push_back(pvdz);
                }
                
                
                // wrt SV
                double svdxy_min = -1;
                double svdz_min = -1;
                
                if(consti->bestTrack())
                {
                    for(const auto svptr : v_secVtx_inJet)
                    {
                        const auto &sv = *svptr;
                        
                        double svdxy = std::fabs(consti->bestTrack()->dxy(sv.position()));
                        double svdz = std::fabs(consti->bestTrack()->dz(sv.position()));
                        
                        if(!std::isnan(svdxy) && !std::isinf(svdxy) && !std::isnan(svdz) && !std::isinf(svdz))
                        {
                            if(svdxy_min < 0 || svdxy < svdxy_min)
                            {
                                svdxy_min = svdxy;
                                svdz_min = svdz;
                            }
                        }
                    }
                }
                
                v_jet_consti_svdxy_reco.push_back(svdxy_min);
                v_jet_consti_svdz_reco.push_back(svdz_min);
                
                
                // 2D isolation
               TLorentzVector lv_jet;
               TLorentzVector lv_consti;
                
                lv_jet.SetXYZT(
                    jet.px(),
                    jet.py(),
                    jet.pz(),
                    jet.energy()
                );
                
                lv_consti.SetXYZT(
                    consti->px(),
                    consti->py(),
                    consti->pz(),
                    consti->energy()
                );
                
                double pTwrtJet = lv_consti.Vect().Perp(lv_jet.Vect());
                double dRwrtJet = lv_consti.DeltaR(lv_jet);
                
                v_jet_consti_pTwrtJet_reco.push_back(pTwrtJet);
                v_jet_consti_dRwrtJet_reco.push_back(dRwrtJet);
                
                
                // Get matching electron
                int iEle = -1;
                int nearestEleIdx = -1;
                int nearestElePt = -1;
                //double minDR = 9999;
                
                for(const auto &ele : electrons_reco)
                {
                    iEle++;
                    double dR = ROOT::Math::VectorUtil::DeltaR(ele.p4(), consti->p4());
                    
                    if(dR < Constants::CONSTI_EL_DR_MAX && ele.pt() > nearestElePt)
                    {
                        nearestEleIdx = iEle;
                        nearestElePt = ele.pt();
                        //minDR = dR;
                    }
                }
                
                if(nearestEleIdx >= 0)
                {
                    nMatchedEl++;
                    
                    edm::Ptr <pat::Electron> elePtr(handle_electron_reco, nearestEleIdx);
                    
                    std::vector <float> extraVariables = eleMvaVarHelper.getAuxVariables(elePtr, iEvent);
                    
                    for(int iVar = 0; iVar < eleMvaVarManager.getNVars(); iVar++)
                    {
                        std::string varName = eleMvaVarManager.getName(iVar);
                        
                        double val = eleMvaVarManager.getValue(iVar, *elePtr, extraVariables);
                        
                        if(!std::isnan(val) && !std::isinf(val))
                        {
                            m_jet_consti_electronInfo_reco[varName].at(iConsti) = val;
                        }
                    }
                }
                
                
                // Get matching muon
                int iMu = -1;
                int nearestMuIdx = -1;
                int nearestMuPt = -1;
                //double minDR = 9999;
                
                for(const auto &mu : muons_reco)
                {
                    iMu++;
                    
                    if (!(mu.isGlobalMuon() && mu.isPFMuon()))
                    {
                        continue;
                    }
                    
                    double dR = ROOT::Math::VectorUtil::DeltaR(mu.p4(), consti->p4());
                    
                    if(dR < Constants::CONSTI_MU_DR_MAX && mu.pt() > nearestMuPt)
                    {
                        nearestMuIdx = iMu;
                        nearestMuPt = mu.pt();
                        //minDR = dR;
                    }
                }
                
                if(nearestMuIdx >= 0)
                {
                    nMatchedMu++;
                    
                    edm::Ptr <pat::Muon> muPtr(handle_muon_reco, nearestMuIdx);
                    
                    //printf("Muon segmentCompatibility %f \n", muPtr->segmentCompatibility());
                    
                    std::vector <float> extraVariables = muMvaVarHelper.getAuxVariables(muPtr, iEvent);
                    
                    for(int iVar = 0; iVar < muMvaVarManager.getNVars(); iVar++)
                    {
                        std::string varName = muMvaVarManager.getName(iVar);
                        
                        double val = muMvaVarManager.getValue(iVar, *muPtr, extraVariables);
                        
                        if(!std::isnan(val) && !std::isinf(val))
                        {
                            m_jet_consti_muonInfo_reco[varName].at(iConsti) = val;
                        }
                    }
                }
            }
            
            
            jetInfo->v_jet_nMatchedEl_reco.push_back(nMatchedEl);
            jetInfo->v_jet_nMatchedMu_reco.push_back(nMatchedMu);
            
            jetInfo->vv_jet_consti_E_reco.push_back(v_jet_consti_E_reco);
            jetInfo->vv_jet_consti_px_reco.push_back(v_jet_consti_px_reco);
            jetInfo->vv_jet_consti_py_reco.push_back(v_jet_consti_py_reco);
            jetInfo->vv_jet_consti_pz_reco.push_back(v_jet_consti_pz_reco);
            jetInfo->vv_jet_consti_pT_reco.push_back(v_jet_consti_pT_reco);
            jetInfo->vv_jet_consti_eta_reco.push_back(v_jet_consti_eta_reco);
            jetInfo->vv_jet_consti_phi_reco.push_back(v_jet_consti_phi_reco);
            jetInfo->vv_jet_consti_m_reco.push_back(v_jet_consti_m_reco);
            
            jetInfo->vv_jet_consti_id_reco.push_back(v_jet_consti_id_reco);
            
            jetInfo->vv_jet_consti_vx_reco.push_back(v_jet_consti_vx_reco);
            jetInfo->vv_jet_consti_vy_reco.push_back(v_jet_consti_vy_reco);
            jetInfo->vv_jet_consti_vz_reco.push_back(v_jet_consti_vz_reco);
            jetInfo->vv_jet_consti_v2d_reco.push_back(v_jet_consti_v2d_reco);
            jetInfo->vv_jet_consti_v3d_reco.push_back(v_jet_consti_v3d_reco);
            
            jetInfo->vv_jet_consti_pvdxy_reco.push_back(v_jet_consti_pvdxy_reco);
            jetInfo->vv_jet_consti_pvdz_reco.push_back(v_jet_consti_pvdz_reco);
            
            jetInfo->vv_jet_consti_svdxy_reco.push_back(v_jet_consti_svdxy_reco);
            jetInfo->vv_jet_consti_svdz_reco.push_back(v_jet_consti_svdz_reco);
            
            jetInfo->vv_jet_consti_dEta_reco.push_back(v_jet_consti_dEta_reco);
            jetInfo->vv_jet_consti_dPhi_reco.push_back(v_jet_consti_dPhi_reco);
            
            jetInfo->vv_jet_consti_EtaPhiRot_dEta_reco.push_back(v_jet_consti_EtaPhiRot_dEta_reco);
            jetInfo->vv_jet_consti_EtaPhiRot_dPhi_reco.push_back(v_jet_consti_EtaPhiRot_dPhi_reco);
            
            jetInfo->vv_jet_consti_LBGS_x_reco.push_back(v_jet_consti_LBGS_x_reco);
            jetInfo->vv_jet_consti_LBGS_y_reco.push_back(v_jet_consti_LBGS_y_reco);
            
            jetInfo->vv_jet_consti_enFrac_reco.push_back(v_jet_consti_enFrac_reco);
            
            jetInfo->vv_jet_consti_pTwrtJet_reco.push_back(v_jet_consti_pTwrtJet_reco);
            jetInfo->vv_jet_consti_dRwrtJet_reco.push_back(v_jet_consti_dRwrtJet_reco);
            
            
            for(int iVar = 0; iVar < eleMvaVarManager.getNVars(); iVar++)
            {
                std::string varName = eleMvaVarManager.getName(iVar);
                
                jetInfo->m_jet_consti_electronInfo_reco[varName].push_back(m_jet_consti_electronInfo_reco[varName]);
            }
            
            for(int iVar = 0; iVar < muMvaVarManager.getNVars(); iVar++)
            {
                std::string varName = muMvaVarManager.getName(iVar);
                
                jetInfo->m_jet_consti_muonInfo_reco[varName].push_back(m_jet_consti_muonInfo_reco[varName]);
            }
        }
        
        
        jetInfo->jet_n_reco = jetInfo->v_jet_E_reco.size();
        
        
        // Matching to gen top
        TMatrixD mat_genTopMatch;
        std::vector <int> v_matchedGenTop_idx;
        
        std::vector <double> v_genTop_deltaR = Common::getMinDeltaR(
            v_jet_4mom,
            v_genTopVis_4mom,
            mat_genTopMatch,
            v_matchedGenTop_idx,
            true
        );
        
        
        for(int iJet = 0; iJet < jetInfo->jet_n_reco; iJet++)
        {
            int genTop_idx = v_matchedGenTop_idx.at(iJet);
            double genTop_minDR = v_genTop_deltaR.at(iJet);
            int genTop_isLeptonic = (genTop_idx >= 0)? (int) treeOutput->v_genTop_isLeptonic.at(genTop_idx) : 0;
            
            jetInfo->v_jet_nearestGenTopIdx_reco.push_back(genTop_idx);
            jetInfo->v_jet_nearestGenTopDR_reco.push_back(genTop_minDR);
            jetInfo->v_jet_nearestGenTopIsLeptonic_reco.push_back(genTop_isLeptonic);
            
            double nearestGenTopbDR = Constants::LARGEVAL_POS;
            double nearestGenTopWlepDR = Constants::LARGEVAL_POS;
            double nearestGenTopWq1DR = Constants::LARGEVAL_POS;
            double nearestGenTopWq2DR = Constants::LARGEVAL_POS;
            
            if(genTop_idx >= 0)
            {
                nearestGenTopbDR = v_genTop_b_4mom.at(genTop_idx).deltaR(v_jet_4mom.at(iJet));
                
                if(genTop_isLeptonic)
                {
                    nearestGenTopWlepDR = v_genTop_Wlep_4mom.at(genTop_idx).deltaR(v_jet_4mom.at(iJet));
                }
                
                else
                {
                    nearestGenTopWq1DR = v_genTop_Wq1_4mom.at(genTop_idx).deltaR(v_jet_4mom.at(iJet));
                    nearestGenTopWq2DR = v_genTop_Wq2_4mom.at(genTop_idx).deltaR(v_jet_4mom.at(iJet));
                }
            }
            
            jetInfo->v_jet_nearestGenTopbDR_reco.push_back(nearestGenTopbDR);
            jetInfo->v_jet_nearestGenTopWlepDR_reco.push_back(nearestGenTopWlepDR);
            jetInfo->v_jet_nearestGenTopWq1DR_reco.push_back(nearestGenTopWq1DR);
            jetInfo->v_jet_nearestGenTopWq2DR_reco.push_back(nearestGenTopWq2DR);
        }
        
        
        // Matching to gen W
        TMatrixD mat_genWMatch;
        std::vector <int> v_matchedGenW_idx;
        
        std::vector <double> v_genW_deltaR = Common::getMinDeltaR(
            v_jet_4mom,
            v_genWvis_4mom,
            mat_genWMatch,
            v_matchedGenW_idx,
            true
        );
        
        for(int iJet = 0; iJet < jetInfo->jet_n_reco; iJet++)
        {
            int genW_idx = v_matchedGenW_idx.at(iJet);
            double genW_minDR = v_genW_deltaR.at(iJet);
            int genW_isLeptonic = (genW_idx >= 0)? (int) treeOutput->v_genW_isLeptonic.at(genW_idx) : 0;
            
            jetInfo->v_jet_nearestGenWIdx_reco.push_back(genW_idx);
            jetInfo->v_jet_nearestGenWDR_reco.push_back(genW_minDR);
            jetInfo->v_jet_nearestGenWIsLeptonic_reco.push_back(genW_isLeptonic);
            
            double nearestGenWlepDR = Constants::LARGEVAL_POS;
            double nearestGenWq1DR = Constants::LARGEVAL_POS;
            double nearestGenWq2DR = Constants::LARGEVAL_POS;
            
            if(genW_idx >= 0)
            {
                if(genW_isLeptonic)
                {
                    nearestGenWlepDR = v_genW_lep_4mom.at(genW_idx).deltaR(v_jet_4mom.at(iJet));
                }
                
                else
                {
                    nearestGenWq1DR = v_genW_q1_4mom.at(genW_idx).deltaR(v_jet_4mom.at(iJet));
                    nearestGenWq2DR = v_genW_q2_4mom.at(genW_idx).deltaR(v_jet_4mom.at(iJet));
                }
            }
            
            jetInfo->v_jet_nearestGenWlepDR_reco.push_back(nearestGenWlepDR);
            jetInfo->v_jet_nearestGenWq1DR_reco.push_back(nearestGenWq1DR);
            jetInfo->v_jet_nearestGenWq2DR_reco.push_back(nearestGenWq2DR);
        }
        
        
        // Matching to gen Z
        TMatrixD mat_genZMatch;
        std::vector <int> v_matchedGenZ_idx;
        
        std::vector <double> v_genZ_deltaR = Common::getMinDeltaR(
            v_jet_4mom,
            v_genZ_4mom,
            mat_genZMatch,
            v_matchedGenZ_idx,
            true
        );
        
        for(int iJet = 0; iJet < jetInfo->jet_n_reco; iJet++)
        {
            int genZ_idx = v_matchedGenZ_idx.at(iJet);
            double genZ_minDR = v_genZ_deltaR.at(iJet);
            int genZ_isLeptonic = (genZ_idx >= 0)? (int) treeOutput->v_genZ_isLeptonic.at(genZ_idx) : 0;
            
            jetInfo->v_jet_nearestGenZIdx_reco.push_back(genZ_idx);
            jetInfo->v_jet_nearestGenZDR_reco.push_back(genZ_minDR);
            jetInfo->v_jet_nearestGenZIsLeptonic_reco.push_back(genZ_isLeptonic);
            
            double nearestGenZlep1DR = Constants::LARGEVAL_POS;
            double nearestGenZlep2DR = Constants::LARGEVAL_POS;
            double nearestGenZq1DR = Constants::LARGEVAL_POS;
            double nearestGenZq2DR = Constants::LARGEVAL_POS;
            
            if(genZ_idx >= 0)
            {
                if(genZ_isLeptonic)
                {
                    nearestGenZlep1DR = v_genZ_lep1_4mom.at(genZ_idx).deltaR(v_jet_4mom.at(iJet));
                    nearestGenZlep2DR = v_genZ_lep2_4mom.at(genZ_idx).deltaR(v_jet_4mom.at(iJet));
                }
                
                else
                {
                    nearestGenZq1DR = v_genZ_q1_4mom.at(genZ_idx).deltaR(v_jet_4mom.at(iJet));
                    nearestGenZq2DR = v_genZ_q2_4mom.at(genZ_idx).deltaR(v_jet_4mom.at(iJet));
                }
            }
            
            jetInfo->v_jet_nearestGenZlep1DR_reco.push_back(nearestGenZlep1DR);
            jetInfo->v_jet_nearestGenZlep2DR_reco.push_back(nearestGenZlep2DR);
            jetInfo->v_jet_nearestGenZq1DR_reco.push_back(nearestGenZq1DR);
            jetInfo->v_jet_nearestGenZq2DR_reco.push_back(nearestGenZq2DR);
        }
    }
    
    
    // Fill tree
    treeOutput->fill();
    
    //#ifdef THIS_IS_AN_EVENTSETUP_EXAMPLE
    //ESHandle<SetupData> pSetup;
    //iSetup.get<SetupRecord>().get(pSetup);
    //#endif
    
    if(debug)
    {
        printf("\n\n");
    }
    
    fflush(stdout);
    fflush(stderr);
}


// ------------ method called once each job just before starting event loop  ------------
void
TreeMaker::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void
TreeMaker::endJob()
{
    fflush(stdout);
    fflush(stderr);
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
TreeMaker::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);

  //Specify that only 'tracks' is allowed
  //To use, remove the default given above and uncomment below
  //ParameterSetDescription desc;
  //desc.addUntracked<edm::InputTag>("tracks","ctfWithMaterialTracks");
  //descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(TreeMaker);
