import FWCore.ParameterSet.Config as cms

##########################################################################################
# Setup

# this is the process run by cmsRun
process = cms.Process('LLDJ')
process.options = cms.untracked.PSet( allowUnscheduled = cms.untracked.bool(True) )

#Setup FWK for multithreaded
process.options.numberOfThreads=cms.untracked.uint32(4)
process.options.numberOfStreams=cms.untracked.uint32(0)

process.load("RecoTracker.TkNavigation.NavigationSchoolESProducer_cfi")

# log output
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(500) )  ## number of events -1 does all
process.MessageLogger.cerr.FwkReport.reportEvery = 100
#process.MessageLogger.cerr.FwkReport.reportEvery = 1
#process.Tracer = cms.Service('Tracer')

# input files
process.source = cms.Source('PoolSource',
                            fileNames = cms.untracked.vstring(
          #'file:MuEG.root'
        #'root://cms-xrd-global.cern.ch//store/data/Run2016G/SingleElectron/AOD/23Sep2016-v1/100000/62B0D6B4-D58A-E611-9F51-002590AC4B5C.root'
        'file:/uscms/home/ddiaz/nobackup/DataSP.root'
 ),
)

# output name
process.TFileService = cms.Service('TFileService', fileName = cms.string('lldjntuple_data_AOD.root'));

#process.out = cms.OutputModule(
#'PoolOutputModule',
#     fileName = cms.untracked.string('output6.root'),
#     outputCommands = cms.untracked.vstring( 
#      'keep *', )  
#)

# cms geometry
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')

# global tag
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = '94X_mc2017_realistic_v12'
#newer recommendation is v14


# for AOD Photons
from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
dataFormat = DataFormat.AOD
#switchOnVIDPhotonIdProducer(process, dataFormat)
#my_id_modules = ['RecoEgamma.PhotonIdentification.Identification.cutBasedPhotonID_Fall17_94X_V1_TrueVtx_cff']
#for idmod in my_id_modules:
#    setupAllVIDIdsInModule(process,idmod,setupVIDPhotonSelection) 


# 2017 AOD Electron ID: https://twiki.cern.ch/twiki/bin/view/CMS/EgammaPostRecoRecipes#Running_on_2016_2017_AOD
# 2017 ID recommendations: https://twiki.cern.ch/twiki/bin/view/CMS/EgammaRunIIRecommendations#Fall17v1 
from RecoEgamma.EgammaTools.EgammaPostRecoTools import setupEgammaPostRecoSeq
setupEgammaPostRecoSeq(process,
                       runVID=True,
                       era='2017-Nov17ReReco', 
		       isMiniAOD=False)

### for AOD Electrons
##switchOnVIDElectronIdProducer(process, dataFormat)
###my_id_modules = ['RecoEgamma.ElectronIdentification.Identification.cutBasedElectronHLTPreselecition_Summer16_V1_cff']
##my_id_modules = ['RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID-Fall17-94X-V1_cff']
##my_id_modules = ['RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Fall17_94X_V1_cff']
##for idmod in my_id_modules:
##    setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)





# pat for trigger
process.load( 'PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff' )

# pat for muons
process.load('PhysicsTools.PatAlgos.patSequences_cff')

from PhysicsTools.PatAlgos.tools.coreTools import *
runOnData( process, names=['All'], outputModules = [])

# load the coreTools of PAT
from PhysicsTools.PatAlgos.tools.jetTools import *

# For AOD Track variables
process.MaterialPropagator = cms.ESProducer('PropagatorWithMaterialESProducer',
    ComponentName = cms.string('PropagatorWithMaterial'),
    Mass = cms.double(0.105),
    MaxDPhi = cms.double(1.6),
    PropagationDirection = cms.string('alongMomentum'),
    SimpleMagneticField = cms.string(''),
    ptMin = cms.double(-1.0),
    useRungeKutta = cms.bool(False)
)

process.TransientTrackBuilderESProducer = cms.ESProducer('TransientTrackBuilderESProducer',
    ComponentName = cms.string('TransientTrackBuilder')
)

#NTuplizer
process.lldjNtuple = cms.EDAnalyzer('lldjNtuple',

 doAOD                     = cms.bool(True),
 doMiniAOD                 = cms.bool(False),

 electronSrc               = cms.InputTag('selectedElectrons','','LLDJ'),
 rhoLabel                  = cms.InputTag('fixedGridRhoFastjetAll'),
 eleVetoIdMap              = cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V1-veto'),
 eleLooseIdMap             = cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V1-loose'),
 eleMediumIdMap            = cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V1-medium'),
 eleTightIdMap             = cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V1-tight'),
 eleHLTIdMap               = cms.InputTag('egmGsfElectronIDs:cutBasedElectronHLTPreselection-Summer16-V1'),

 rhoCentralLabel           = cms.InputTag('fixedGridRhoFastjetCentralNeutral'),
 pileupCollection          = cms.InputTag('slimmedAddPileupInfo'),
 AODpileupCollection       = cms.InputTag('addPileupInfo', '', 'HLT'),
 VtxLabel                  = cms.InputTag('offlineSlimmedPrimaryVertices'),
 triggerResults            = cms.InputTag('TriggerResults', '', 'HLT'),

 AODTriggerInputTag           = cms.InputTag("TriggerResults","","HLT"),
 AODTriggerEventInputTag      = cms.InputTag("hltTriggerSummaryAOD","","HLT"),

 beamspotLabel_            = cms.InputTag('offlineBeamSpot'),

 #ak4JetSrc                 = cms.InputTag('slimmedJets'),
 AODak4CaloJetsSrc         = cms.InputTag('ak4CaloJets' , '', 'RECO'),
 #AODak4PFJetsSrc           = cms.InputTag('ak4PFJets'   , '', 'RECO'),
 #AODak4PFJetsCHSSrc        = cms.InputTag('ak4PFJetsCHS', '', 'RECO'),
 #selectedPatJetsSrc        = cms.InputTag('selectedPatJets'),                                   
 AODVertexSrc              = cms.InputTag('offlinePrimaryVertices', '', 'RECO'),
 AODTrackSrc               = cms.InputTag('generalTracks', '', 'RECO'),
 vertexFitterConfig = cms.PSet(
        finder = cms.string('avf'),
        sigmacut = cms.double(10.),
        Tini = cms.double(256.),
        ratio = cms.double(0.25),
        ),

 patTriggerResults         = cms.InputTag('TriggerResults', '', 'PAT'),
 BadChargedCandidateFilter = cms.InputTag('BadChargedCandidateFilter'),
 BadPFMuonFilter           = cms.InputTag('BadPFMuonFilter'),
 pfMETLabel                = cms.InputTag('slimmedMETsMuEGClean', '', 'LLDJ'),
 AODCaloMETlabel           = cms.InputTag('caloMet','','RECO'),    
 AODpfChMETlabel           = cms.InputTag('pfChMet','','RECO'),    
 AODpfMETlabel             = cms.InputTag('pfMet','','RECO'),  

 muonSrc                   = cms.InputTag('slimmedMuons'),
 muonAODSrc                = cms.InputTag('selectedPatMuons'),

 photonSrc                 = cms.InputTag('selectedPhotons','','LLDJ'),
# phoLooseIdMap             = cms.InputTag('egmPhotonIDs:cutBasedPhotonID-Fall17-94X-V1-loose'),
# phoMediumIdMap            = cms.InputTag('egmPhotonIDs:cutBasedPhotonID-Fall17-94X-V1-medium'),
# phoTightIdMap             = cms.InputTag('egmPhotonIDs:cutBasedPhotonID-Fall17-94X-V1-tight'),
# phoChargedIsolation       = cms.InputTag('photonIDValueMapProducer:phoChargedIsolation'),
# phoNeutralHadronIsolation = cms.InputTag('photonIDValueMapProducer:phoNeutralHadronIsolation'),
# phoPhotonIsolation        = cms.InputTag('photonIDValueMapProducer:phoPhotonIsolation'),
# phoWorstChargedIsolation  = cms.InputTag('photonIDValueMapProducer:phoWorstChargedIsolation'),
 #photonAODSrc              = cms.InputTag('selectedPatPhotons'),
 photonAODSrc              = cms.InputTag('gedPhotons'),

# AOD_phoLooseIdMap  = cms.InputTag("egmPhotonIDs:cutBasedPhotonID-Fall17-94X-V1-loose"),
# AOD_phoMediumIdMap = cms.InputTag("egmPhotonIDs:cutBasedPhotonID-Fall17-94X-V1-medium"),
# AOD_phoTightIdMap  = cms.InputTag("egmPhotonIDs:cutBasedPhotonID-Fall17-94X-V1-tight"),
# AOD_phoChargedIsolationMap       = cms.InputTag("photonIDValueMapProducer", "phoChargedIsolation"),
# AOD_phoNeutralHadronIsolationMap = cms.InputTag("photonIDValueMapProducer", "phoNeutralHadronIsolation"),
# AOD_phoPhotonIsolationMap        = cms.InputTag("photonIDValueMapProducer", "phoPhotonIsolation"),
# AOD_phoWorstChargedIsolationMap  = cms.InputTag("photonIDValueMapProducer", "phoWorstChargedIsolation"),

 electronAODSrc = cms.InputTag("gedGsfElectrons"),
 #AOD_eleIdMap = cms.InputTag("egmGsfElectronIDs:cutBasedElectronHLTPreselection-Summer16-V1"),#doesn't work with AOD
 AOD_eleLooseIdMap = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V1-loose"),
 AOD_eleMediumIdMap = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V1-loose"),
 AOD_eleTightIdMap = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V1-loose"),
 conversions  = cms.InputTag('allConversions'),

 genParticleSrc    = cms.InputTag("genParticles"),

 bits = cms.InputTag("TriggerResults","","HLT"),
 prescales = cms.InputTag("patTrigger"),
 objects = cms.InputTag("selectedPatTrigger"),

)


#builds Ntuple
process.p = cms.Path(
    process.lldjNtuple
    )
# process.egmPhotonIDSequence *
#process.ep = cms.EndPath(process.out)
#print process.dumpPython()
#print process.egmGsfElectronIDSequence.dumpPython()

