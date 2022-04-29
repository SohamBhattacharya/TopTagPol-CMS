#!/usr/bin/env xonsh


from __future__ import print_function

import argparse
import numpy
import os
import subprocess
import termcolor


# Argument parser
#parser = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter)
parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter) # Will show the defaults


parser.add_argument(
    "--path",
    help = "ntuple path (this path should contain the directory structure <sample>/<date_time>).",
    type = str,
    required = False,
    default = "/pnfs/desy.de/cms/tier2/store/user/sobhatta/TopTagPol/ntuples",
)

parser.add_argument(
    "--samplepaths",
    help = "Each of these paths should contain <date_time> directories (providing this will ignore --path).",
    type = str,
    nargs = "*",
    required = False,
    default = None,
)

parser.add_argument(
    "--gfalprefix",
    help = "The GFAL prefix for the path.",
    type = str,
    required = False,
    default = "gsiftp://dcache-cms-gridftp.desy.de:2811",
)

parser.add_argument(
    "--keepiters",
    help = (
        "If <keepiters> is not negative, will delete all iterations except the latest (sorted by <date_time>) <keepiters>."
    ),
    type = int,
    required = False,
    default = -1,
)

parser.add_argument(
    "--delete",
    help = "Will run the delete command.",
    default = False,
    action = "store_true",
)


# Parse arguments
args = parser.parse_args()
d_args = vars(args)


l_samplepath = args.samplepaths

if (l_samplepath is None) :
    
    # Pipes need to be added separately; cannot be included in the command string
    cmd = "find {path}/ -mindepth 1 -maxdepth 1".format(path = args.path)
    print(cmd)
    l_samplepath = $(@(cmd.split()) | sort -V).strip().split()

l_delCmd = []

for iSample, samplepath in enumerate(l_samplepath) :
    
    sample = samplepath.split("/")[-1]
    print("[sample %d/%d]" %(iSample+1, len(l_samplepath)), sample)
    
    cmd = "find {path}/ -mindepth 1 -maxdepth 1".format(path = samplepath)
    l_tagpath = $(@(cmd.split()) | sort -rV).strip().split()
    
    for iTag, tagpath in enumerate(l_tagpath) :
        
        tag = tagpath.split("/")[-1]
        
        willDel = False
        
        if (args.keepiters >= 0 and iTag+1 > args.keepiters) :
            
            willDel = True
            
            cmd = "gfal-rm -r {gfalprefix}/{tagpath}".format(gfalprefix = args.gfalprefix, tagpath = tagpath)
            #print(cmd)
            l_delCmd.append(cmd)
        
        print("    ", tag, termcolor.colored("*** WILL BE DELETED ***"*willDel, "red"))


if (args.delete and len(l_delCmd)) :
    
    print("REALLY delete?")
    inputStr = str(input("Enter CONFIRM to confirm: ")).strip()
    
    deleteConfirmed = (inputStr == "CONFIRM")
    
    if (deleteConfirmed) :
        
        print("Starting delete operations...")
        
        for iCmd, cmd in enumerate(l_delCmd) :
            
            print("[Operation %d/%d]" %(iCmd+1, len(l_delCmd)))
            print(cmd)
            @(cmd.split())
        
        print("Delete operations complete.")
