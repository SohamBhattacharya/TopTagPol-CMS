#include "RecoEgamma/EgammaTools/interface/MVAVariableHelper.h"

/////////////
// Specializations for the Electrons
/////////////

#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/EgammaCandidates/interface/Conversion.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "RecoEgamma/EgammaTools/interface/ConversionTools.h"
#include "RecoEgamma/ElectronIdentification/interface/ElectronMVAEstimatorRun2.h"

template<>
MVAVariableHelper<pat::Electron>::MVAVariableHelper(edm::ConsumesCollector && cc)
    : tokens_({
            cc.consumes<reco::ConversionCollection>(edm::InputTag("allConversions")),
            cc.consumes<reco::ConversionCollection>(edm::InputTag("reducedEgamma:reducedConversions")),
            cc.consumes<reco::BeamSpot>(edm::InputTag("offlineBeamSpot")),
            cc.consumes<double>(edm::InputTag("fixedGridRhoFastjetAll"))
        })
{}

template<>
const std::vector<float> MVAVariableHelper<pat::Electron>::getAuxVariables(
        edm::Ptr<pat::Electron> const& particlePtr, const edm::Event& iEvent) const
{
    edm::Handle<reco::ConversionCollection> conversionsHandle;
    edm::Handle<reco::BeamSpot> beamSpotHandle;
    edm::Handle<double> rhoHandle;

    iEvent.getByToken(tokens_[0], conversionsHandle);
    if( !conversionsHandle.isValid() ) {
      iEvent.getByToken(tokens_[1], conversionsHandle);
      if( !conversionsHandle.isValid() )
        throw cms::Exception(" Collection not found: ")
            << " failed to find a standard AOD or miniAOD conversions collection " << std::endl;
    }

    iEvent.getByToken(tokens_[2], beamSpotHandle);
    iEvent.getByToken(tokens_[3], rhoHandle);

    return ElectronMVAEstimatorRun2::getExtraVars(*particlePtr,
                                                  conversionsHandle.product(),
                                                  beamSpotHandle.product(),
                                                  *rhoHandle);
}

template<>
MVAVariableIndexMap<pat::Electron>::MVAVariableIndexMap()
    : indexMap_({
            {"electronMVAVariableHelper:kfhits"        , 0},
            {"electronMVAVariableHelper:kfchi2"        , 1},
            {"electronMVAVariableHelper:convVtxFitProb", 2},
            {"fixedGridRhoFastjetAll"                  , 3}
        })
{}
