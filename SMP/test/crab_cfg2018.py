from CRABClient.UserUtilities import config

config = config()
config.General.requestName = 'VJJ_Rivet2018'
config.General.transferOutputs = True
config.General.transferLogs = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'runRivetAnalyzer_VJJ_miniAOD2018.py'
config.JobType.outputFiles = ['out.yoda']
config.JobType.inputFiles = ['../data/CMS_2018_PAS_SMP_19_005.yoda','runRivetAnalyzer_VJJ_miniAOD2018.py','../../rivetSetup.sh']
config.JobType.scriptExe = 'crab_script2018.sh'
config.Data.inputDataset = '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM'
#config.Data.inputDataset = '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/AODSIM'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.outLFNDirBase = '/store/group/phys_smp/vbfA/Mhossein_Rivet_test'
config.Data.publication = False
config.Site.storageSite = 'T2_CH_CERN'
