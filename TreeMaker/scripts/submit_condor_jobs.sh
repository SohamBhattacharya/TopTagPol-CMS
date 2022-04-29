#!/usr/bin/env python

from __future__ import print_function

import argparse
import os
import sortedcontainers


# Argument parser
parser = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter)


parser.add_argument(
    "--samples",
    help = "List of samples",
    type = str,
    nargs = "*",
    required = True,
)


# Parse arguments
args = parser.parse_args()
d_args = vars(args)


#l_sampleName = d_sample[args.sample][args.era]

l_sampleName = []
l_sourceFile = []

for sampleName in args.samples :
    
    sampleName = sampleName.strip()
    
    if (not len(sampleName) or sampleName[0] == "#") :
        
        continue
    
    if (sampleName[0] == "/") :
        
        sampleName = sampleName[1:]
    
    sampleName = sampleName.replace("/", "_")
    
    l_sampleName.append(sampleName)
    
    l_sourceFile.append(
        "sourceFiles/{sampleName}/{sampleName}.txt".format(sampleName = sampleName)
    )

print("\n".join(l_sourceFile))
#exit()


cmd = ("python scripts/run_condor.py "
    "--processNames {processNames} "
    "--inputFileLists {inputFileList} "
    "--cmsRunFile MyTools/EDAnalyzers/python/ConfFile_cfg.py "
    "--outputDir condorJobs "
    "--nUnitPerJob 1 "
    #"--nInputFileMax 2 "
    "--movetoT2 "
    #"--test "
).format(
    processNames = " ".join(l_sampleName),
    inputFileList = " ".join(l_sourceFile),
)

print(cmd)


os.system(cmd)
