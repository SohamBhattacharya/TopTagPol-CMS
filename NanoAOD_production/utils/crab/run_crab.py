#!/usr/bin/env python3

from __future__ import print_function

import argparse
import http
import logging
import math
import os
import subprocess
import sys

from CRABClient.UserUtilities import ClientException
from CRABClient.UserUtilities import getUsernameFromCRIC
from CRABAPI.RawCommand import crabCommand

import crab_config

#logging.basicConfig(format = "%(asctime)s %(message)s", level = logging.ERROR)
#logging.basicConfig(format = "%(asctime)s %(message)s")#, level = logging.ERROR)


def main() :
    
    # Argument parser
    parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument(
        "--samples",
        help = "List of samples to submit",
        type = str,
        nargs = "*",
        required = "--pycfg" in sys.argv,
        #default = None,
    )
    
    parser.add_argument(
        "--pycfg",
        help = "Python file to run",
        type = str,
        required = "--samples" in sys.argv,
        #default = None,
    )
    
    parser.add_argument(
        "--dryrun",
        help = "Dry CRAB run",
        default = False,
        action = "store_true",
    )
    
    parser.add_argument(
        "--maxunits",
        help = "If the splitting is FileBased and the total no. of files is greater than <maxunits>, then unitsPerJob will be increased accordingly.",
        type = int,
        required = False,
        default = 5000,
    )
    
    parser.add_argument(
        "--dirs",
        help = "CRAB directories to check",
        type = str,
        nargs = "*",
        required = False,
        #default = None,
    )
    
    parser.add_argument(
        "--crabop",
        help = "CRAB operation",
        type = str,
        required = True,
        choices = ["submit", "resubmit", "status"]#, "kill"],
    )
    
    parser.add_argument(
        "--resubmitopt",
        help = (
            "Options to pass to crab resubmit. For e.g. sitewhitelist=* maxmemory=4000 \n"
            "All options: https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3Commands"
        ),
        type = str,
        nargs = "*",
        required = False,
        default = [],
    )
    
    parser.add_argument(
        "--outDAS",
        help = "File where the output DAS dataset names will be logged",
        type = str,
        default = None,
        required = False
    )
    
    args = parser.parse_args()
    d_args = vars(args)
    
    
    #assert(
    #    args.samples & 
    #)
    
    if (args.crabop == "submit") :
        
        args.samples = [_ele for _ele in args.samples if not _ele.startswith("#")]
        
        for iSample, sample in enumerate(args.samples) :
            
            print("\n")
            print("*"*80)
            print(f"[{iSample+1}/{len(args.samples)}] {sample}")
            print("*"*80)
            
            jobName = sample.strip().split("/")[1]
            #print(jobName)
            
            crab_cfg = crab_config.get_config_default()
            
            crab_cfg.General.requestName = jobName
            crab_cfg.JobType.psetName = args.pycfg
            crab_cfg.Data.inputDataset = sample
            
            #crab_cfg.JobType.inputFiles.append(args.pycfg)
            
            # Arguments to pass to the python cfg file
            #crab_cfg.JobType.pyCfgParams.append("isFastSim=1")
            
            if (crab_cfg.Data.splitting == "FileBased") :
                
                nFile = subprocess.check_output(
                    f"dasgoclient -query=\"file dataset={sample}\" | wc -l",
                    shell = True
                )
                
                nFile = int(nFile)
                
                assert(nFile > 0)
                
                if (nFile > args.maxunits) :
                    
                    unitsPerJob = int(math.ceil(nFile / args.maxunits))
                    print(f"Dataset has {nFile} units. Changing unitsPerJob to {unitsPerJob}.")
                    crab_cfg.Data.unitsPerJob = unitsPerJob
            
            try :
                
                crabCmd_ret = crabCommand(
                    args.crabop,
                    config = crab_cfg,
                    dryrun = args.dryrun,
                )
            
            except http.client.HTTPException as exc:
                
                print("HTTPException")
                print(exc)
            
            except ClientException as exc :
                
                print("ClientException")
                print(exc)
                
    
    
    elif (args.crabop in ["status", "resubmit"]) :
        
        d_crabProjInfo = {}
        
        args.dirs = [_ele for _ele in args.dirs if not _ele.startswith("#")]
        
        for iDir, crabDir in enumerate(args.dirs) :
            
            print("\n")
            print("*"*80)
            print(f"[{iDir+1}/{len(args.dirs)}] {crabDir}")
            print("*"*80)
            
            d_crabProjInfo[crabDir] = {}
            
            try :
                
                crabCmd_ret = crabCommand(
                    "status",
                    dir = crabDir,
                )
                
                if (crabCmd_ret["publicationEnabled"] and "outdatasets" in crabCmd_ret and crabCmd_ret["outdatasets"]) :
                    
                    d_crabProjInfo[crabDir]["DASoutput"] = eval(crabCmd_ret["outdatasets"])[0]
                
                if (args.crabop == "resubmit" and "failed" in crabCmd_ret["jobsPerStatus"]) :
                    
                    d_resubmitopt = {}
                    
                    for opt in args.resubmitopt :
                        
                        _key, _val = opt.strip().split("=")
                        
                        if (_val.isdigit()) :
                            
                            val = int(_val)
                        
                        d_resubmitopt[_key] = _val
                    
                    crabCmd_ret = crabCommand(
                        "resubmit",
                        dir = crabDir,
                        **d_resubmitopt,
                    )
            
            except http.client.HTTPException as exc:
                
                print("HTTPException")
                print(exc)
            
            except ClientException as exc :
                
                print("ClientException")
                print(exc)
        
        
        if (args.outDAS) :
            
            if ("/" in args.outDAS) :
                
                os.system(f"mkdir -p {outDAS[0: outDAS.rfind('/')]}")
            
            with open(args.outDAS, "w") as outFile :
                
                #print(d_crabProjInfo)
                outFile.write(
                    "\n".join([d_crabProjInfo[_key]["DASoutput"] for _key in d_crabProjInfo if ("DASoutput" in d_crabProjInfo[_key])])
                )
                
                outFile.write("\n")
    
    
    return 0
    
    
    


if (__name__ == "__main__") :
    
    main()
