import argparse
import datetime
import numpy
import os
import subprocess


#cwd = os.getcwd()
cwd = "%s/src" %(subprocess.check_output(["echo", "$CMSSW_BASE"]).strip())
proxy = subprocess.check_output(["voms-proxy-info", "--path"]).strip()


# Argument parser
parser = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter)

# TreeMaker_SingleElectron_PT2to100_PhaseIITDRSpring19DR-PU200_106X_upgrade2023_realistic_v3-v1_GEN-SIM-DIGI-RAW
parser.add_argument(
    "--processNames",
    help = "Name of the processes to be run",
    type = str,
    nargs = "*",
    required = True,
)

# sourceFiles/SingleElectron_PT2to100_PhaseIITDRSpring19DR-PU200_106X_upgrade2023_realistic_v3-v1_GEN-SIM-DIGI-RAW/SingleElectron_PT2to100_PhaseIITDRSpring19DR-PU200_106X_upgrade2023_realistic_v3-v1_GEN-SIM-DIGI-RAW.txt
parser.add_argument(
    "--inputFileLists",
    help = "Files containing the list of input files (for each process)",
    type = str,
    nargs = "*",
    required = True,
)

# EDAnalyzers/TreeMaker/python/ConfFile_cfg.py
parser.add_argument(
    "--cmsRunFile",
    help = "cmsRun file",
    type = str,
    required = True,
)

parser.add_argument(
    "--cmsRunOptions",
    help = "Options for the cmsRun file",
    type = str,
    required = False,
    default = "",
)

# /eos/cms/store/group/phys_egamma/sobhatta/HGCal_TreeMaker
parser.add_argument(
    "--outputDir",
    help = "cmsRun output directory",
    type = str,
    required = True,
)

parser.add_argument(
    "--suffix",
    help = "suffix",
    type = str,
    required = False,
    default = "",
)

parser.add_argument(
    "--nUnitPerJob",
    help = "Numbers of units to process per job",
    type = int,
    required = False,
    default = 5,
)

parser.add_argument(
    "--nInputFileMax",
    help = "Maximum number of units to process",
    type = int,
    required = False,
    default = -1,
)

parser.add_argument(
    "--movetoT2",
    help = "Whether to move output to T2",
    default = False,
    action = "store_true",
)

parser.add_argument(
    "--pathT2",
    help = "T2 Grid-FTP path to move output to",
    type = str,
    default = "gsiftp://dcache-cms-gridftp.desy.de:2811/pnfs/desy.de/cms/tier2/store/user/sobhatta/TopTagPol/ntuples",
    required = False
)

parser.add_argument(
    "--test",
    help = "Only create job files (do not submit)",
    default = False,
    action = "store_true",
)


# Parse arguments
args = parser.parse_args()


condorConfig = "scripts/condor_config.sub"
condorScript = "scripts/condor_script.sh"

condorConfig_name = condorConfig[condorConfig.rfind("/")+1: condorConfig.rfind(".")]
condorConfig_ext = condorConfig[condorConfig.rfind("."):]

condorScript_name = condorScript[condorConfig.rfind("/")+1: condorScript.rfind(".")]
condorScript_ext = condorScript[condorScript.rfind("."):]


if (__name__ == "__main__") :
    
    #print args.processNames
    #print args.inputFileLists
    
    for iProcess, (processName, inputFileList) in enumerate(zip(args.processNames, args.inputFileLists)) :
        
        nJob_total = 0
        nUnit_total = 0
        
        datetime_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        processName = "%s%s" %(processName, args.suffix)
        
        processName_output = "%s_%s" %(processName, datetime_str)
        processName_T2 = "%s/%s" %(processName, datetime_str)
        
        outputDir = "%s/%s" %(args.outputDir, processName_output)
        command = "mkdir -p " + outputDir
        print "Command:", command
        os.system(command)
        print ""
        
        #condorDir = "%s/condorJobs" %(outputDir)
        condorDir = "condorJobs/%s" %(processName_output)
        command = "mkdir -p " + condorDir
        print "Command:", command
        os.system(command)
        print ""
        
        
        inputFiles = numpy.loadtxt(inputFileList, dtype = str)
        nInputFile = inputFiles.shape[0]
        
        if (args.nInputFileMax > 0 and nInputFile > args.nInputFileMax) :
            
            inputFiles = inputFiles[0: args.nInputFileMax]
            nInputFile = inputFiles.shape[0]
        
        
        nJob = int(numpy.ceil(float(nInputFile)/args.nUnitPerJob))
        
        print "****************************************************************************************************"
        print "****************************************************************************************************"
        print "Process:", processName
        print "Input file:", inputFileList
        print "cmsRun file:", args.cmsRunFile
        print "Output directory:", outputDir
        print "Condor directory:", condorDir
        print "# units:", nInputFile
        print "# jobs:", nJob
        print "# units per job:", args.nUnitPerJob
        print "****************************************************************************************************"
        print "****************************************************************************************************"
        print ""
        
        
        inputFileList = inputFileList[inputFileList.rfind("/")+1:]
        inputFileList_name = inputFileList[0: inputFileList.rfind(".")]
        inputFileList_ext = inputFileList[inputFileList.rfind("."):]
        
        
        condorConfig_content = ""
        
        with open(condorConfig, "r") as f :
            
            condorConfig_content = f.read()
        
        
        condorScript_content = ""
        
        with open(condorScript, "r") as f :
            
            condorScript_content = f.read()
        
        
        nDigit = len(str(nJob))
        
        for iJob in range(0, nJob) :
            
            #jobNumberStr = "%0*d" %(nDigit, iJob+1)
            jobNumberStr = str(iJob+1)
            
            if (iJob < nJob-1) :
                
                inputFiles_mod = inputFiles[iJob*args.nUnitPerJob: (iJob+1)*args.nUnitPerJob]
                
            else :
                
                inputFiles_mod = inputFiles[iJob*args.nUnitPerJob:]
            
            condorConfig_mod = condorConfig_name + "_" + jobNumberStr + condorConfig_ext
            condorConfig_mod = "%s/%s" %(condorDir, condorConfig_mod)
            
            condorScript_mod = condorScript_name + "_" + jobNumberStr + condorScript_ext
            condorScript_mod = "%s/%s" %(condorDir, condorScript_mod)
            
            inputFileList_mod = inputFileList_name + "_" + jobNumberStr + inputFileList_ext
            inputFileList_mod = "%s/%s" %(condorDir, inputFileList_mod)
            
            # Input file list
            print "Writing: %s" %(inputFileList_mod)
            
            with open(inputFileList_mod, "w") as f :
                
                f.write("\n".join(inputFiles_mod) + "\n")
            
            
            # Condor config
            condorConfig_content_mod = condorConfig_content
            condorConfig_content_mod = condorConfig_content_mod.replace("@exe@", condorScript_mod)
            condorConfig_content_mod = condorConfig_content_mod.replace("@log@", condorDir + "/" + "job_%s" %(jobNumberStr) + ".log")
            condorConfig_content_mod = condorConfig_content_mod.replace("@out@", condorDir + "/" + "job_%s" %(jobNumberStr) + ".out")
            condorConfig_content_mod = condorConfig_content_mod.replace("@err@", condorDir + "/" + "job_%s" %(jobNumberStr) + ".err")
            
            print "Writing: %s" %(condorConfig_mod)
            
            with open(condorConfig_mod, "w") as f :
                
                f.write(condorConfig_content_mod)
            
            
            # Condor script
            lineBreakStr = " \\\n"
            
            cmsRun_cmd = "cmsRun %s" %(args.cmsRunFile) + lineBreakStr
            cmsRun_cmd += "\t print" + lineBreakStr
            cmsRun_cmd += "\t sourceFile=%s" %(inputFileList_mod) + lineBreakStr
            cmsRun_cmd += "\t outputDir=%s" %(outputDir) + lineBreakStr
            cmsRun_cmd += "\t outFileNumber=%d" %(iJob+1) + lineBreakStr
            
            cmsRun_cmd += "\t %s" %(args.cmsRunOptions) + lineBreakStr
            
            run_cmd = "%s" %(cmsRun_cmd)
            
            
            if (args.movetoT2) :
                
                src = "%s/ntupleTree_%d.root" %(outputDir, iJob+1)
                destT2 = "%s/%s/" %(args.pathT2, processName_T2)
                
                mv_cmd = (
                    "(env -i bash -lc \". ~/.bashrc && gfal-mkdir -p {destT2}\") && {lineBreak}"
                    "(env -i bash -lc \". ~/.bashrc && gfal-copy -f {src} {destT2}\") && {lineBreak}"
                    "rm {src}"
                ).format(
                    src = src,
                    destT2 = destT2,
                    lineBreak = lineBreakStr,
                )
                
                run_cmd = "(%s) && %s%s" %(cmsRun_cmd, lineBreakStr, mv_cmd)
            
            
            condorScript_content_mod = condorScript_content
            condorScript_content_mod = condorScript_content_mod.replace("@dir@", cwd)
            condorScript_content_mod = condorScript_content_mod.replace("@proxy@", proxy)
            condorScript_content_mod = condorScript_content_mod.replace("@cmd@", run_cmd)
            
            print "Writing: %s" %(condorScript_mod)
            
            with open(condorScript_mod, "w") as f :
                
                f.write(condorScript_content_mod)
            
            command = "chmod +x %s" %(condorScript_mod)
            print "Command:", command
            os.system(command)
            
            
            # Submit job
            command = "condor_submit %s" %(condorConfig_mod)
            #command = "_CONDOR_SCHEDD_HOST=bigbird15.cern.ch _CONDOR_CREDD_HOST=bigbird15.cern.ch condor_submit %s" %(condorConfig_mod)
            print "Command:", command
            
            commandReturn = 1
            
            if (not args.test) :
                
                # Repeat until job is submission is successful (returns 0)
                while (commandReturn) :
                    
                    commandReturn = os.system(command)
            
            
            print "\n"
            
        
        
        print "\n"
        print "****************************************************************************************************"
        print "****************************************************************************************************"
        print "Total # unit:", nInputFile
        print "Total # job:", nJob
        print "****************************************************************************************************"
        print "****************************************************************************************************"
        print "\n"
