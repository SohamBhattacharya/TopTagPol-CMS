from CRABClient.UserUtilities import config
from CRABClient.UserUtilities import getUsernameFromCRIC


def get_config_default() :
    
    crab_cfg = config()
    
    crab_cfg.section_("General")
    crab_cfg.General.requestName = ""
    crab_cfg.General.workArea = "crab_projects"
    crab_cfg.General.transferOutputs = True
    crab_cfg.General.transferLogs = True
    crab_cfg.JobType.allowUndistributedCMSSW = True
    
    crab_cfg.section_("JobType")
    crab_cfg.JobType.pluginName = "Analysis"
    crab_cfg.JobType.psetName = ""
    crab_cfg.JobType.inputFiles = []
    #crab_cfg.JobType.maxJobRuntimeMin = 5*60
    crab_cfg.JobType.maxMemoryMB = 4000
    
    
    crab_cfg.section_("Data")
    crab_cfg.Data.inputDataset = ""
    crab_cfg.Data.inputDBS = "global"
    crab_cfg.Data.splitting = "FileBased"
    crab_cfg.Data.unitsPerJob = 1
    #crab_cfg.Data.outLFNDirBase = "/store/user/sobhatta/TopTagPol/NanoAOD"
    crab_cfg.Data.outLFNDirBase = f"/store/user/{getUsernameFromCRIC()}/TopTagPol/mc"
    crab_cfg.Data.publication = True
    crab_cfg.Data.outputDatasetTag = "NanoAOD"
    
    crab_cfg.section_("Site")
    #crab_cfg.Site.whitelist = ["T2_DE_DESY"]
    crab_cfg.Site.storageSite = "T2_DE_DESY"
    
    
    return crab_cfg
