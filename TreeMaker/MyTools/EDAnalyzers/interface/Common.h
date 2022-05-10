# ifndef Common_H
# define Common_H


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
# include <TTree.h>
# include <TVectorD.h>
# include <Math/Point3D.h>
# include <Math/Point3Dfwd.h>
# include <Math/VectorUtil.h>

# include "fastjet/contrib/AxesDefinition.hh"
# include "fastjet/contrib/EnergyCorrelator.hh"
# include "fastjet/contrib/MeasureDefinition.hh"
# include "fastjet/contrib/Nsubjettiness.hh"
# include "fastjet/contrib/SoftDrop.hh"
# include "fastjet/PseudoJet.hh"
# include "fastjet/ClusterSequence.hh"

# include "Constants.h"


namespace Common
{
    bool isAfromB(const reco::GenParticle &particleA, int particleBid)
    {
        for(unsigned int iMother = 0; iMother < particleA.numberOfMothers(); iMother++)
        {
            const reco::GenParticle *mother = particleA.motherRef(iMother).get();
            
            int motherId = mother->pdgId();
            
            if(motherId == particleBid)
            {
                return true;
            }
        }
        
        return false;
    }
    
    
    bool isAfromB(const reco::GenParticle &particleA, std::vector <int> v_particleBid)
    {
        for(unsigned int iB = 0; iB < v_particleBid.size(); iB++)
        {
            if(isAfromB(particleA, v_particleBid[iB]))
            {
                return true;
            }
        }
        
        return false;
    }
    
    
    bool isPromptPhoton(const reco::GenParticle &photon)
    {
        if(std::abs(photon.pdgId()) != 22 || photon.status() != 1)
        {
            return false;
        }
        
        for(unsigned int iMother = 0; iMother < photon.numberOfMothers(); iMother++)
        {
            const reco::GenParticle *mother = photon.motherRef(iMother).get();
            
            int motherId = std::abs(mother->pdgId());
            
            if(motherId <= 22 || motherId == 2212)
            {
                return true;
            }
        }
        
        return false;
    }
    
    
    const reco::GenParticle* getLastCopy(const reco::GenParticle* part)
    {
        int id = part->pdgId();
        
        for(unsigned int iDaughter = 0; iDaughter < part->numberOfDaughters(); iDaughter++)
        {
            const reco::GenParticle *daughter = part->daughterRef(iDaughter).get();
            
            int daughterId = daughter->pdgId();
            
            // If the daugher is the same, then recurse
            if(daughterId == id)
            {
                return getLastCopy(daughter);
            }
        }
        
        return part;
    }
    
    
    int isLeptonicTopWZ(const reco::GenParticle *partOrig, bool includeTaus = false)
    {
        const reco::GenParticle *part = getLastCopy(partOrig);
        
        int id = std::abs(part->pdgId());
        
        for(unsigned int iDaughter = 0; iDaughter < part->numberOfDaughters(); iDaughter++)
        {
            const reco::GenParticle *daughter = part->daughterRef(iDaughter).get();
            
            int daughterId = std::abs(daughter->pdgId());
            
            if(id == 23 || id == 24)
            {
                if(daughterId == 11 || daughterId == 13 || (includeTaus && daughterId == 15))
                {
                    return daughterId;
                }
            }
            
            else
            {
                if(daughterId == 23 || daughterId == 24)
                {
                    return isLeptonicTopWZ(daughter, includeTaus);
                }
            }
        }
        
        return 0;
    }
    
    
    math::XYZTLorentzVector getInvisibleCompnent(int depth, const reco::GenParticle *part, std::vector <int> v_invId = {12, 14, 16}, std::vector <int> v_invSourceId = {23, 24})
    {
        int id = std::abs(part->pdgId());
        
        math::XYZTLorentzVector p4_inv(0, 0, 0, 0);
        
        for(unsigned int iDaughter = 0; iDaughter < part->numberOfDaughters(); iDaughter++)
        {
            const reco::GenParticle *daughter = getLastCopy(part->daughterRef(iDaughter).get());
            
            int daughterId = std::abs(daughter->pdgId());
            
            //if(std::find(v_invSourceId.begin(), v_invSourceId.end(), daughterId) == v_invSourceId.end())
            //{
            //    continue;
            //}
            
            if(daughter->isLastCopy() && std::find(v_invId.begin(), v_invId.end(), daughterId) != v_invId.end())
            {
                //printf("[%d] Got inv (%d): id %d, mother id %d, status %d, p4 (%0.2f, %+0.2f, %+0.2f, %+0.2f) \n", depth, (int) iDaughter, daughterId, id, daughter->status(), daughter->p4().E(), daughter->p4().Px(), daughter->p4().Py(), daughter->p4().Pz());
                p4_inv += daughter->p4();
            }
            
            else if(std::find(v_invSourceId.begin(), v_invSourceId.end(), daughterId) != v_invSourceId.end())
            {
                p4_inv += getInvisibleCompnent(depth+1, daughter, v_invId, v_invSourceId);
            }
        }
        
        return p4_inv;
    }
    
    
    math::XYZTLorentzVector getVisibleCompnent(const reco::GenParticle *part, std::vector <int> v_invId = {12, 14, 16}, std::vector <int> v_invSourceId = {23, 24})
    {
        math::XYZTLorentzVector p4_inv = getInvisibleCompnent(0, getLastCopy(part), v_invId, v_invSourceId);
        math::XYZTLorentzVector p4_vis = part->p4() - p4_inv;
        
        return p4_vis;
    }
    
    
    CLHEP::HepLorentzVector lorentzVector2clhep(const math::XYZTLorentzVector &lv)
    {
        CLHEP::HepLorentzVector lv_clhep;
        
        lv_clhep.setT(lv.E());
        lv_clhep.setX(lv.Px());
        lv_clhep.setY(lv.Py());
        lv_clhep.setZ(lv.Pz());
        
        return lv_clhep;
    }
    
    
    int getPileup(edm::Handle <std::vector <PileupSummaryInfo> > pileUps_reco)
    {
        int pileup_n = 0;
        
        // Start from the end to reach the In-time bunch-crossing quicker
        for(int iPileUp = (int) pileUps_reco->size() - 1; iPileUp >= 0; iPileUp--)
        {
            PileupSummaryInfo pileUpInfo = (*pileUps_reco)[iPileUp];
            
            int bunchCrossingNumber = pileUpInfo.getBunchCrossing();
            
            // In-time bunch-crossing pile-up
            if(bunchCrossingNumber == 0)
            {
                pileup_n = pileUpInfo.getPU_NumInteractions();
                
                break;
            }
        }
        
        return pileup_n;
    }
    
    
    std::pair <std::pair <int, int>, double> findMatrixMinimum(TMatrixD matrix)
    {
        int minRow = -1;
        int minCol = -1;
        
        double minVal = matrix.Max() + 1;
        
        for(int iRow = 0; iRow < matrix.GetNrows(); iRow++)
        {
            for(int iCol = 0; iCol < matrix.GetNcols(); iCol++)
            {
                if(matrix(iRow, iCol) < minVal)
                {
                    minVal = matrix(iRow, iCol);
                    
                    minRow = iRow;
                    minCol = iCol;
                }
            }
        }
        
        std::pair <std::pair <int, int>, double> result = std::make_pair(
            std::make_pair(minRow, minCol),
            minVal
        );
        
        return result;
    }
    
    
    double getRapidityDeltaR(
        CLHEP::HepLorentzVector obj1,
        CLHEP::HepLorentzVector obj2
    )
    {
        double dy = obj1.rapidity() - obj2.rapidity();
        double dPhi = obj1.v().deltaPhi(obj2.v());
        
        double deltaR = sqrt(dy*dy + dPhi*dPhi);
        
        return deltaR;
    }
    
    
    //double getRapidityDeltaR(
    //    TLorentzVector obj1,
    //    TLorentzVector obj2
    //)
    //{
    //    return getRapidityDeltaR(
    //        TLorentzVectorToHepLorentzVector(obj1),
    //        TLorentzVectorToHepLorentzVector(obj2)
    //    );
    //}
    
    
    // Will return {dRmin1, ... dRminN} of size v_obj1_4mom.size()
    std::vector <double> getMinDeltaR(
        std::vector <CLHEP::HepLorentzVector> v_obj1_4mom,
        std::vector <CLHEP::HepLorentzVector> v_obj2_4mom,
        TMatrixD &mat_deltaR_result, // Will fill this with the dR values
        std::vector <int> &v_obj1_matchedObj2_index, // Will be of v_obj1_4mom.size(). Will be filled with the index of the matched obj2; if not matched, then -1.
        bool useRapidity = false,
        double defaultVal = Constants::LARGEVAL_POS
    )
    {
        int nObj1 = v_obj1_4mom.size();
        int nObj2 = v_obj2_4mom.size();
        
        TMatrixD tmat_deltaR(nObj1, nObj2);
        
        for(int iObj1 = 0; iObj1 < nObj1; iObj1++)
        {
            for(int iObj2 = 0; iObj2 < nObj2; iObj2++)
            {
                double deltaR = 0;
                
                if(useRapidity)
                {
                    deltaR = getRapidityDeltaR(v_obj1_4mom.at(iObj1), v_obj2_4mom.at(iObj2));
                }
                
                else
                {
                    deltaR = v_obj1_4mom.at(iObj1).deltaR(v_obj2_4mom.at(iObj2));
                }
                
                tmat_deltaR(iObj1, iObj2) = deltaR;
            }
        }
        
        mat_deltaR_result.ResizeTo(nObj1, nObj2);
        
        mat_deltaR_result = tmat_deltaR;
        
        std::vector <double> v_deltaR_min(nObj1, defaultVal);
        
        v_obj1_matchedObj2_index.clear();
        v_obj1_matchedObj2_index.resize(v_obj1_4mom.size(), -1);
        
        int nIter = std::min(nObj1, nObj2);
        
        for(int iIter = 0; iIter < nIter; iIter++)
        {
            std::pair <std::pair <int, int>, double> matrixMinResult = findMatrixMinimum(tmat_deltaR);
            
            int minRow = matrixMinResult.first.first;
            int minCol = matrixMinResult.first.second;
            
            double minVal = matrixMinResult.second;
            
            if(minVal == defaultVal)
            {
                break;
            }
            
            v_deltaR_min.at(minRow) = minVal;
            v_obj1_matchedObj2_index.at(minRow) = minCol;
            
            //printf("tmat_deltaR before masking: \n");
            //tmat_deltaR.Print();
            
            // Mask minRow and minCol
            TMatrixDRow(tmat_deltaR, minRow).Assign(defaultVal);
            TMatrixDColumn(tmat_deltaR, minCol).Assign(defaultVal);
            
            //printf("tmat_deltaR after masking: \n");
            //tmat_deltaR.Print();
            
            //v_deltaR_min.at(iIter) = minVal;
            //
            //deleteMatrixRowCol(tmat_deltaR, minRow, minCol);
            //
            //if(!tmat_deltaR.GetNrows() || !tmat_deltaR.GetNcols())
            //{
            //    break;
            //}
        }
        
        return v_deltaR_min;
    }
    
    
    CLHEP::HepLorentzVector PseudoJetToHepLorentzVector(fastjet::PseudoJet pseudoJet)
    {
        CLHEP::HepLorentzVector obj_4mom;
        obj_4mom.setT(pseudoJet.e());
        obj_4mom.setX(pseudoJet.px());
        obj_4mom.setY(pseudoJet.py());
        obj_4mom.setZ(pseudoJet.pz());
        
        return obj_4mom;
    }
    
    
    CLHEP::HepLorentzVector getHepLorentzVectorSum(
        std::vector <CLHEP::HepLorentzVector> v_4mom
    )
    {
        CLHEP::HepLorentzVector sum_4mom(0, 0, 0, 0);
        
        //#pragma omp parallel for
        for(int iObj = 0; iObj < (int) v_4mom.size(); iObj++)
        {
            sum_4mom += v_4mom.at(iObj);
        }
        
        return sum_4mom;
    }
    
    
    // {..., (dEta, dPhi), ... } --> {..., (dEta_trans, dPhi_trans), ...}
    std::vector <std::vector <double> > getTransformedDetaDphi(
        std::vector <fastjet::PseudoJet> v_pseudoJet,
        fastjet::PseudoJet pseudoJet_ref,
        TVectorD direc1,
        TVectorD direc2,
        TVectorD finalTranslation
    )
    {
        int nConsti = v_pseudoJet.size();
        
        TMatrixD mat_rotate(2, 2);
        TMatrixD mat_reflect(2, 2);
        
        TMatrixD mat_DetaDphi(2, nConsti);
        
        for(int iConsti = 0; iConsti < nConsti; iConsti++)
        {
            fastjet::PseudoJet consti = v_pseudoJet.at(iConsti);
            
            double dEta = consti.eta() - pseudoJet_ref.eta();
            double dPhi = pseudoJet_ref.delta_phi_to(consti);
            
            mat_DetaDphi(0, iConsti) = dEta;
            mat_DetaDphi(1, iConsti) = dPhi;
        }
        
        double direc1_norm = sqrt(direc1.Norm2Sqr());
        double direc2_norm = sqrt(direc2.Norm2Sqr());
        
        //bool isReflected = false;
        
        if(direc1_norm)
        {
            direc1 *= (1.0 / direc1_norm);
            
            mat_rotate(0, 0) = +direc1(0);
            mat_rotate(0, 1) = +direc1(1);
            
            mat_rotate(1, 0) = -direc1(1);
            mat_rotate(1, 1) = +direc1(0);
            
            mat_DetaDphi = mat_rotate * mat_DetaDphi;
            
            finalTranslation = mat_rotate * finalTranslation;
            
            if(direc2_norm)
            {
                direc2 *= (1.0 / direc2_norm);
                
                // Reflect
                TVectorD direc2_transformed(2);
                direc2_transformed = mat_rotate * direc2;
                
                if(direc2_transformed(1) < 0)
                {
                    mat_reflect(0, 0) = +1.0;
                    mat_reflect(1, 1) = -1.0;
                    
                    mat_reflect(1, 0) = 0.0;
                    mat_reflect(0, 1) = 0.0;
                    
                    mat_DetaDphi = mat_reflect * mat_DetaDphi;
                    
                    //isReflected = true;
                    finalTranslation(1) *= -1;
                }
            }
        }
        
        
        std::vector <std::vector <double> > v_result(nConsti);
        
        
        //#pragma omp parallel for
        for(int iConsti = 0; iConsti < nConsti; iConsti++)
        {
            std::vector <double> v_temp = {
                mat_DetaDphi(0, iConsti) - finalTranslation(0),
                mat_DetaDphi(1, iConsti) - finalTranslation(1),
            };
            
            // Keep ref-axis in the +ve x-axis
            if(finalTranslation(0) && mat_DetaDphi(0, iConsti) < 0)
            {
                mat_DetaDphi(0, iConsti) *= -1;
            }
            
            v_result.at(iConsti) = v_temp;
        }
        
        return v_result;
    }
    
    
    std::vector <CLHEP::HepLorentzVector> getGStranformed4mom(
        std::vector <fastjet::PseudoJet> v_axis_psJet,
        std::vector <fastjet::PseudoJet> v_psJet
    )
    {
        // Find the GS axes
        std::vector <CLHEP::Hep3Vector> v_GSaxis;
        
        for(int iAxis = 0; iAxis < (int) v_axis_psJet.size(); iAxis++)
        {
            CLHEP::Hep3Vector GSaxis = PseudoJetToHepLorentzVector(v_axis_psJet.at(iAxis)).v().unit();
            
            for(int iGSaxis = 0; iGSaxis < (int) v_GSaxis.size(); iGSaxis++)
            {
                GSaxis -= GSaxis.dot(v_GSaxis.at(iGSaxis)) * v_GSaxis.at(iGSaxis);
            }
            
            GSaxis = GSaxis.unit();
            
            v_GSaxis.push_back(GSaxis);
        }
        
        
        //printf("GSaxis: \n");
        //
        //for(int iGSaxis = 0; iGSaxis < (int) v_GSaxis.size(); iGSaxis++)
        //{
        //    printf(
        //        "\t %d (%0.2e, %0.2e, %0.2e):  ",
        //        iGSaxis+1,
        //        v_GSaxis.at(iGSaxis).x(), v_GSaxis.at(iGSaxis).y(), v_GSaxis.at(iGSaxis).z()
        //    );
        //    
        //    for(int jGSaxis = 0; jGSaxis < (int) v_GSaxis.size(); jGSaxis++)
        //    {
        //        printf(
        //            "\t %d*%d %0.2e, ",
        //            iGSaxis+1, jGSaxis+1,
        //            v_GSaxis.at(iGSaxis).dot(v_GSaxis.at(jGSaxis))
        //        );
        //    }
        //    
        //    printf("\n");
        //}
        
        
        std::vector <CLHEP::HepLorentzVector> v_GStransformed_4mom(v_psJet.size());
        
        // Transform the 3 momenta
        //#pragma omp parallel for
        for(int iJet = 0; iJet < (int) v_psJet.size(); iJet++)
        {
            CLHEP::HepLorentzVector jet_4mom = PseudoJetToHepLorentzVector(v_psJet.at(iJet));
            
            CLHEP::HepLorentzVector GStransformed_4mom;
            CLHEP::Hep3Vector GStransformed_3mom;;
            
            //#pragma omp parallel for
            for(int iGSaxis = 0; iGSaxis < (int) v_GSaxis.size(); iGSaxis++)
            {
                //printf("\t %d, %0.2e \n", iGSaxis+1, jet_4mom.v().dot(v_GSaxis.at(iGSaxis)));
                
                GStransformed_3mom(iGSaxis) = jet_4mom.v().dot(v_GSaxis.at(iGSaxis));
            }
            
            GStransformed_4mom.setE(jet_4mom.e());
            GStransformed_4mom.setVect(GStransformed_3mom);
            
            v_GStransformed_4mom.at(iJet) = GStransformed_4mom;
            
            //printf(
            //    "Jet %d/%d: "
            //    "(%0.2e, %0.2e, %0.2e, %0.2e) |p| %0.2e, m %0.2e "
            //    "--> "
            //    "(%0.2e, %0.2e, %0.2e, %0.2e) |p| %0.2e, m %0.2e "
            //    "\n ",
            //    
            //    iJet+1, v_psJet.size(),
            //    jet_4mom.e(), jet_4mom.px(), jet_4mom.py(), jet_4mom.pz(), jet_4mom.v().mag(), jet_4mom.m(),
            //    GStransformed_4mom.e(), GStransformed_4mom.px(), GStransformed_4mom.py(), GStransformed_4mom.pz(), GStransformed_4mom.v().mag(), GStransformed_4mom.m()
            //);
        }
        
        //printf("\n\n");
        
        return v_GStransformed_4mom;
    }
    
    
    double catchNansInfs(double val, double replace_val)
    {
        if(std::isnan(val) || std::isinf(val))
        {
            return replace_val;
        }
        
        return val;
    }
    
    
    // From: https://github.com/CMSDeepFlavour/DeepNTuples/blob/master/DeepNtuplizer/interface/ntuple_content.h
    double catchInfs(double in, double replace_value){
        if(in==in){
            if(std::isinf(in))
                return replace_value;
            else if(in < -1e32 || in > 1e32)
                return replace_value;
            return in;
        }
        return replace_value;
    }
    
    double catchInfsAndBound(double in, double replace_value, 
            double lowerbound, double upperbound, const double offset=0){
        double withoutinfs=catchInfs(in, replace_value);
        if(withoutinfs+offset<lowerbound) return lowerbound;
        if(withoutinfs+offset>upperbound) return upperbound;
        //if(useoffsets)
        withoutinfs+=offset;
        return withoutinfs;
    }
    
    Measurement1D vertexDxy(const reco::VertexCompositePtrCandidate &svcand, const reco::Vertex &pv)  {
        VertexDistanceXY dist;
        reco::Vertex::CovarianceMatrix csv; svcand.fillVertexCovariance(csv);
        reco::Vertex svtx(svcand.vertex(), csv);
        return dist.distance(svtx, pv);
    }
    
    Measurement1D vertexD3d(const reco::VertexCompositePtrCandidate &svcand, const reco::Vertex &pv)  {
        VertexDistance3D dist;
        reco::Vertex::CovarianceMatrix csv; svcand.fillVertexCovariance(csv);
        reco::Vertex svtx(svcand.vertex(), csv);
        return dist.distance(svtx, pv);
    }
    
    double vertexDdotP(const reco::VertexCompositePtrCandidate &sv, const reco::Vertex &pv)  {
        reco::Candidate::Vector p = sv.momentum();
        reco::Candidate::Vector d(sv.vx() - pv.x(), sv.vy() - pv.y(), sv.vz() - pv.z());
        return p.Unit().Dot(d.Unit());
    }
    
}


# endif
