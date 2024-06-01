import FWCore.ParameterSet.Config as cms
'''
import shutil
print("copy yoda file")
dest = shutil.copyfile('/afs/cern.ch/user/m/mkaramsi/public/hepmc/CMSSW_11_2_4/src/Rivet/SMP/test/CMS_2024_PAS_SMP_24_005.yoda','./CMS_2024_PAS_SMP_24_005.yoda')
print("file have be copied")
'''
process = cms.Process("runRivetAnalysis")
process.load('FWCore.MessageService.MessageLogger_cfi')
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = 10000
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
   '/store/mc/RunIISummer20UL18MiniAODv2/GJets_SM_4f_TuneCP5_EWK_13TeV_amcatnlo-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/003DC763-6548-7B45-AB76-BC01642BB25C.root',

)
)
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")

process.generatorMix = cms.EDProducer("MergedGenParticleProducer",
    inputPacked = cms.InputTag("packedGenParticles"),
    inputPruned = cms.InputTag("prunedGenParticles")
)

process.generator = cms.EDProducer("GenParticles2HepMCConverter",
    genParticles = cms.InputTag("generatorMix"),
    genEventInfo = cms.InputTag("generator"),
    lheSrc = cms.InputTag("externalLHEProducer"),
    signalParticlePdgIds = cms.vint32()
)

process.load("GeneratorInterface.RivetInterface.rivetAnalyzer_cfi")
process.rivetAnalyzer.HepMCCollection = cms.InputTag('generator','unsmeared')
process.rivetAnalyzer.CrossSection = cms.double(25.75)
process.rivetAnalyzer.AnalysisNames = cms.vstring('CMS_2017_PAS_SMP_19_005')
process.p = cms.Path(process.generatorMix*
                     process.generator*process.rivetAnalyzer)
process.rivetAnalyzer.useLHEweights = cms.bool(True)
process.rivetAnalyzer.matchWeightNames=cms.string("lhapdf=306.*")
process.rivetAnalyzer.OutputFile = cms.string('out.yoda')
# Add the RivetAnalyzer to the path
#process.p = cms.Path(process.rivetAnalyzer)

# Set the environment variable within the script
#import os
#print("this is rivet path",os.environ.get('RIVET_DATA_PATH', '') + ':.')
#os.environ['RIVET_DATA_PATH'] = os.environ.get('RIVET_DATA_PATH', '') + ':.'
