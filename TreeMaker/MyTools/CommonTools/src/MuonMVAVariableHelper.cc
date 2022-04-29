#include "RecoEgamma/EgammaTools/interface/MVAVariableHelper.h"

/////////////
// Specializations for the Muons
/////////////

#include "DataFormats/EgammaCandidates/interface/Conversion.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "RecoEgamma/EgammaTools/interface/ConversionTools.h"
#include "RecoEgamma/ElectronIdentification/interface/ElectronMVAEstimatorRun2.h"

template<>
MVAVariableHelper<pat::Muon>::MVAVariableHelper(edm::ConsumesCollector && cc) {}

template<>
const std::vector<float> MVAVariableHelper<pat::Muon>::getAuxVariables(
        edm::Ptr<pat::Muon> const& particlePtr, const edm::Event& iEvent) const
{
    return {};
}

template<>
MVAVariableIndexMap<pat::Muon>::MVAVariableIndexMap() {}
