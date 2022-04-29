import os

import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras
from Configuration.AlCa.GlobalTag import GlobalTag


processName = "Demo"
process = cms.Process(processName)

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag = GlobalTag(process.GlobalTag, "auto:run2_mc", "")

process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")

process.load("RecoMET.METFilters.primaryVertexFilter_cfi")
process.primaryVertexFilter.vertexCollection = cms.InputTag("offlineSlimmedPrimaryVertices")

process.load("RecoMET.METFilters.BadPFMuonFilter_cfi")
process.BadPFMuonFilter.muons = cms.InputTag("slimmedMuons")
process.BadPFMuonFilter.PFCandidates = cms.InputTag("packedPFCandidates")

process.load("RecoMET.METFilters.BadChargedCandidateFilter_cfi")
process.BadChargedCandidateFilter.muons = cms.InputTag("slimmedMuons")
process.BadChargedCandidateFilter.PFCandidates = cms.InputTag("packedPFCandidates")

process.load("RecoMET.METFilters.eeBadScFilter_cfi")
process.eeBadScFilter.EERecHitSource = cms.InputTag("reducedEgamma", "reducedEERecHits")

process.load("RecoMET.METFilters.ecalBadCalibFilter_cfi")
process.load("PhysicsTools.PatAlgos.slimming.metFilterPaths_cff")
process.load("FWCore.MessageService.MessageLogger_cfi")


############################## Parse arguments ##############################

import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing("analysis")


options.register("sourceFile",
    "", # Default value
    VarParsing.VarParsing.multiplicity.singleton, # singleton or list
    VarParsing.VarParsing.varType.string, # string, int, or float
    "File containing list of input files" # Description
)

options.register("outputDir",
    "", # Default value
    VarParsing.VarParsing.multiplicity.singleton, # singleton or list
    VarParsing.VarParsing.varType.string, # string, int, or float
    "Output directory" # Description
)

options.register("outFileBaseName",
    "ntupleTree", # Default value
    VarParsing.VarParsing.multiplicity.singleton, # singleton or list
    VarParsing.VarParsing.varType.string, # string, int, or float
    "Output file base name (w/o extension): [base name].root" # Description
)

options.register("outFileNumber",
    -1, # Default value
    VarParsing.VarParsing.multiplicity.singleton, # singleton or list
    VarParsing.VarParsing.varType.int, # string, int, or float
    "File number (will be added to the filename if >= 0)" # Description
)

options.register("eventRange",
    [], # Default value
    VarParsing.VarParsing.multiplicity.list, # singleton or list
    VarParsing.VarParsing.varType.string, # string, int, or float
    "Syntax: Run1:Event1-Run2:Event2 Run3:Event3-Run4:Event4(includes both)" # Description
)

options.register("debug",
    0, # Default value
    VarParsing.VarParsing.multiplicity.singleton, # singleton or list
    VarParsing.VarParsing.varType.int, # string, int, or float
    "Print debug statements" # Description
)

options.register("debugFile",
    0, # Default value
    VarParsing.VarParsing.multiplicity.singleton, # singleton or list
    VarParsing.VarParsing.varType.int, # string, int, or float
    "Create debug file" # Description
)

options.register("isGunSample",
    0, # Default value
    VarParsing.VarParsing.multiplicity.singleton, # singleton or list
    VarParsing.VarParsing.varType.int, # string, int, or float
    "Is it a particle gun sample" # Description
)

options.register("genPartonFilter",
    0, # Default value
    VarParsing.VarParsing.multiplicity.singleton, # singleton or list
    VarParsing.VarParsing.varType.int, # string, int, or float
    "Apply gen-parton filter" # Description
)

options.register("eleMvaVariablesFile",
    #"RecoEgamma/ElectronIdentification/data/ElectronMVAEstimatorRun2Fall17V1Variables.txt", # Default value
    "MyTools/EDAnalyzers/data/ElectronMVAEstimatorRun2Variables.txt", # Default value
    VarParsing.VarParsing.multiplicity.singleton, # singleton or list
    VarParsing.VarParsing.varType.string, # string, int, or float
    "MVA variables file" # Description
)

options.register("muMvaVariablesFile",
    "MyTools/EDAnalyzers/data/MuonVariables.txt", # Default value
    VarParsing.VarParsing.multiplicity.singleton, # singleton or list
    VarParsing.VarParsing.varType.string, # string, int, or float
    "MVA variables file" # Description
)

options.register("trace",
    0, # Default value
    VarParsing.VarParsing.multiplicity.singleton, # singleton or list
    VarParsing.VarParsing.varType.int, # string, int, or float
    "Trace modules" # Description
)

options.register("memoryCheck",
    0, # Default value
    VarParsing.VarParsing.multiplicity.singleton, # singleton or list
    VarParsing.VarParsing.varType.int, # string, int, or float
    "Check memory usage" # Description
)

options.register("printTime",
    0, # Default value
    VarParsing.VarParsing.multiplicity.singleton, # singleton or list
    VarParsing.VarParsing.varType.int, # string, int, or float
    "Print timing information" # Description
)

options.register("depGraph",
    0, # Default value
    VarParsing.VarParsing.multiplicity.singleton, # singleton or list
    VarParsing.VarParsing.varType.int, # string, int, or float
    "Produce dependency graph only" # Description
)

options.parseArguments()


process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(options.maxEvents))


#sourceFile = "sourceFiles/TT_Mtt-700to1000_TuneCP5_PSweights_13TeV-powheg-pythia8_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v8_MINIAODSIM/TT_Mtt-700to1000_TuneCP5_PSweights_13TeV-powheg-pythia8_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v8_MINIAODSIM.txt"
#sourceFile = "sourceFiles/TT_Mtt-1000toInf_TuneCP5_PSweights_13TeV-powheg-pythia8_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1_MINIAODSIM/TT_Mtt-1000toInf_TuneCP5_PSweights_13TeV-powheg-pythia8_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1_MINIAODSIM.txt"
#sourceFile = "sourceFiles/ZprimeToTT_M1000_W10_TuneCP2_PSweights_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM/ZprimeToTT_M1000_W10_TuneCP2_PSweights_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM.txt"
sourceFile = "sourceFiles/ZprimeToTT_M2000_W20_TuneCP2_PSweights_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM/ZprimeToTT_M2000_W20_TuneCP2_PSweights_13TeV-madgraphMLM-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_MINIAODSIM.txt"

if (len(options.sourceFile)) :
    
    sourceFile = options.sourceFile


fNames = []

if (len(options.inputFiles)) :
    
    fNames = options.inputFiles

else :
    
    with open(sourceFile) as f:
        
        fNames = f.readlines()

fNames = [f for f in fNames if f[0] != "#"]

for iFile, fName in enumerate(fNames) :
    
    if (
        "file:" not in fName and
        "root:" not in fName
    ) :
        
        fNames[iFile] = "file:%s" %(fName)


outFileSuffix = ""


if (options.outFileNumber >= 0) :
    
    outFileSuffix = "%s_%d" %(outFileSuffix, options.outFileNumber)


outFile = "%s%s.root" %(options.outFileBaseName, outFileSuffix)

if (len(options.outputDir)) :
    
    os.system("mkdir -p %s" %(options.outputDir))
    
    outFile = "%s/%s" %(options.outputDir, outFile)


sourceFileNames = cms.untracked.vstring(fNames)

process.source = cms.Source("PoolSource",
    fileNames = sourceFileNames,
    
    # Run1:Event1 to Run2:Event2
    #eventsToProcess = cms.untracked.VEventRange("1:78722-1:78722"),
    
    #duplicateCheckMode = cms.untracked.string("noDuplicateCheck"),
)


if (len(options.eventRange)) :
    
    process.source.eventsToProcess = cms.untracked.VEventRange(options.eventRange)


#process.options = cms.untracked.PSet(
#    #SkipEvent = cms.untracked.vstring("ProductNotFound"),
#    
#    #printDependencies = cms.untracked.bool(True),
#)


if (options.depGraph) :
    
    process.DependencyGraph = cms.Service("DependencyGraph")
    process.source = cms.Source("EmptySource")
    process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(0))


from JMEAnalysis.JetToolbox.jetToolbox_cff import jetToolbox

l_akJetPuppi_rParam = [4, 8, 15]
l_jetPuppiCollection = []

for rParam in l_akJetPuppi_rParam :
    
    # AK4 is already present
    if (rParam == 4) :
        
        l_jetPuppiCollection.append("slimmedJetsPuppi")
    
    else :
        
        jetToolbox(
            proc = process,
            jetType = "ak%d" %(rParam),
            jetSequence = "jetSequenceAK%d" %(rParam),
            outputFile = "noOutput",
            PUMethod = "Puppi",
            dataTier = "miniAOD",
            runOnMC = True,
            #JETCorrPayload = "",
            #addSoftDrop = True,
        )
        
        l_jetPuppiCollection.append("selectedPatJetsAK%dPFPuppi" %(rParam))


from RecoBTag.SecondaryVertex.bVertexFilter_cfi import *

process.bVertexFilter = cms.EDFilter(
    "CandidateBVertexFilter",
    primaryVertices  = cms.InputTag("offlineSlimmedPrimaryVertices"),
    secondaryVertices = cms.InputTag("slimmedSecondaryVertices"),
    vertexFilter = bVertexFilter.vertexFilter,
    useVertexKinematicAsJetAxis = bVertexFilter.useVertexKinematicAsJetAxis,
    minVertices = bVertexFilter.minVertices,
)


recoJetPSet = cms.PSet(
    jetCollection = cms.InputTag(""),
    
    rParam = cms.double(0.0),
    
    minPt = cms.double(100),
    
    apply_sd = cms.bool(True),
    sd_zcut = cms.string("0.1"),
    sd_beta = cms.string("0"),
    sd_R0 = cms.string("1"),  # 1.0 is the default value
    
    jetRescale_m0 = cms.string("1"),
    jetLorentzBoost_e0 = cms.string("2"),
    
    maxTauN = cms.int32(4),
)

l_recoJetPSet = []

for iJet in range(0, len(l_akJetPuppi_rParam)) :
    
    minPt = 100.0
    
    if (l_akJetPuppi_rParam[iJet] <= 4) :
        
        minPt = 10.0
    
    l_recoJetPSet.append(recoJetPSet.clone(
        jetCollection = cms.InputTag(l_jetPuppiCollection[iJet]),
        rParam = cms.double(l_akJetPuppi_rParam[iJet]/10.0),
        minPt = cms.double(minPt),
    ))
    
    l_recoJetPSet.append(recoJetPSet.clone(
        jetCollection = cms.InputTag(l_jetPuppiCollection[iJet]),
        rParam = cms.double(l_akJetPuppi_rParam[iJet]/10.0),
        minPt = cms.double(minPt),
        apply_sd = cms.bool(False),
    ))


process.treeMaker = cms.EDAnalyzer(
    "TreeMaker",
    
    ############################## My stuff ##############################
    debug = cms.bool(bool(options.debug)),
    isGunSample = cms.bool(bool(options.isGunSample)),
    
    eleMvaVariablesFile = cms.string(options.eleMvaVariablesFile),
    muMvaVariablesFile = cms.string(options.muMvaVariablesFile),
    
    ############################## GEN ##############################
    
    label_lheEvent = cms.InputTag("externalLHEProducer"),
    label_generator = cms.InputTag("generator"),
    label_genParticle = cms.InputTag("prunedGenParticles"),
    
    
    ############################## RECO ##############################
    
    label_primaryVertex = cms.InputTag("offlineSlimmedPrimaryVertices"),
    #label_secondaryVertex = cms.InputTag("slimmedSecondaryVertices"),
    label_secondaryVertex = cms.InputTag("bVertexFilter"),
    label_pileup = cms.InputTag("slimmedAddPileupInfo"),
    label_rho = cms.InputTag("fixedGridRhoFastjetAll"),
    
    
    label_slimmedElectron = cms.InputTag("slimmedElectrons"),
    label_slimmedMuon = cms.InputTag("slimmedMuons"),
    
    v_recoJetPSet = cms.VPSet(l_recoJetPSet),
)


#from EDFilters.MyFilters.GenParticleFilter_cfi import *
#
## Gen-parton filter
#process.GenParticleFilter_part = GenParticleFilter.clone()
#process.GenParticleFilter_part.atLeastN = cms.int32(1)
#process.GenParticleFilter_part.pdgIds = cms.vint32(1, 2, 3, 4, 5, 21)
#process.GenParticleFilter_part.minPt = cms.double(10)
#process.GenParticleFilter_part.minEta = cms.double(1.479)
#process.GenParticleFilter_part.maxEta = cms.double(3.1)
#process.GenParticleFilter_part.isGunSample = cms.bool(bool(options.isGunSample))
##process.GenParticleFilter_part.debug = cms.bool(True)
#
#process.filter_seq_genPart = cms.Sequence()
#
#if (options.genPartonFilter) :
#
#    process.filter_seq_genPart = cms.Sequence(process.GenParticleFilter_part)


print "Deleting existing output file."
os.system("rm %s" %(outFile))


# Output file name modification
if (outFile.find("/eos/cms") ==  0) :
    
    outFile = outFile.replace("/eos/cms", "root://eoscms.cern.ch//eos/cms")


# Output
process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string(outFile)
)


process.schedule = cms.Schedule()


process.p = cms.Path(
    #process.filter_seq_genPart *
    
    process.bVertexFilter *
    
    process.treeMaker
)

# The endpath needs to be inserted, otherwise the JetToolBox is not running for some reason
process.schedule.insert(0, process.endpath)
process.schedule.insert(0, process.p)

print "\n"
print "*"*50
print "process:", process
print "process.schedule:", process.schedule
print "*"*50
#print "process.schedule.__dict__:", process.schedule.__dict__
#print "*"*50
print "\n"


# Tracer
if (options.trace) :
    
    process.Tracer = cms.Service("Tracer")


if (options.memoryCheck) :
    
    process.SimpleMemoryCheck = cms.Service(
        "SimpleMemoryCheck",
        moduleMemorySummary = cms.untracked.bool(True),
    )


#Timing
if (options.printTime) :

    process.Timing = cms.Service("Timing",
        summaryOnly = cms.untracked.bool(False),
        useJobReport = cms.untracked.bool(True)
    )


# Debug
if (options.debugFile) :
    
    process.out = cms.OutputModule("PoolOutputModule",
        fileName = cms.untracked.string("debug.root")
    )
    
    process.output_step = cms.EndPath(process.out)
    process.schedule.extend([process.output_step])


#process.MessageLogger = cms.Service(
#    "MessageLogger",
#    destinations = cms.untracked.vstring(
#        "cerr",
#    ),
#    cerr = cms.untracked.PSet(
#        #threshold  = cms.untracked.string("ERROR"),
#        DEBUG = cms.untracked.PSet(limit = cms.untracked.int32(0)),
#        WARNING = cms.untracked.PSet(limit = cms.untracked.int32(0)),
#        ERROR = cms.untracked.PSet(limit = cms.untracked.int32(0)),
#    )
#)

process.options = cms.untracked.PSet()
process.options.allowUnscheduled = cms.untracked.bool(True)

#from FWCore.ParameterSet.Utilities import convertToUnscheduled
#process = convertToUnscheduled(process)


# Add early deletion of temporary data products to reduce peak memory need
#from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
#process = customiseEarlyDelete(process)
# End adding early deletion
