#!/usr/bin/env python

from __future__ import print_function

import argparse
import numpy
import os
import subprocess


# Argument parser
#parser = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter)
parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter) # Will show the defaults


parser.add_argument(
    "--getCount",
    help = "Get the number of events and dataset size",
    default = False,
    action = "store_true",
)

parser.add_argument(
    "--getFiles",
    help = "Get the list of files",
    default = False,
    action = "store_true",
)

parser.add_argument(
    "--dasOptions",
    help = "Additional DAS options (such as \"instance=prod/phys03\")",
    type = str,
    required = False,
    default = "",
)

parser.add_argument(
    "--replace",
    help = "Will replace \"str1\" with \"str2\": \"str1\" \"str2\" (e.g. \"/store\" \"root://dcache-cms-xrootd.desy.de://pnfs/desy.de/cms/tier2/store\")",
    type = str,
    nargs = 2,
    required = False,
    default = ["/store", "root://cms-xrd-global.cern.ch//store"],
)

parser.add_argument(
    "--maxEvents",
    help = "Will get a subset of the file list s.t. its total event count is close to \"maxEvents\"",
    type = int,
    required = False,
    default = None,
)

parser.add_argument(
    "--createRucioRule",
    help = "Create Rucio rules to copy datasets",
    default = False,
    action = "store_true",
)

parser.add_argument(
    "--tier2site",
    help = "T2 site name for Rucio rules (e.g. T2_DE_DESY)",
    type = str,
    required = False,
    default = None,
)

parser.add_argument(
    "--sampleNames",
    help = "Sample names (if provided, will not use the internal list)",
    type = str,
    nargs = "*",
    required = True,
)

parser.add_argument(
    "--outDir",
    help = "Output directory",
    type = str,
    required = False,
    default = "sourceFiles"
)



# Parse arguments
args = parser.parse_args()
d_args = vars(args)




prefix = args.replace[1]
toReplace = args.replace[0]

l_sampleName = args.sampleNames

# Reconfirm rucio rule creation request with user input
rucioConfirmed = False

if (args.createRucioRule and args.tier2site is not None) :
    
    print("Samples:")
    print("\n".join(l_sampleName))
    print("")
    
    print("REALLY create Rucio rules?")
    inputStr = str(raw_input("Enter CONFIRM to confirm: ")).strip()
    
    rucioConfirmed = (inputStr == "CONFIRM")
    
    if (not rucioConfirmed) :
        
        print("Rucio rule creation not confirmed. Exiting...")
        exit()


l_sampleName = [_name.strip() for _name in l_sampleName]
l_sampleName = [_name for _name in l_sampleName if (_name[0] != "#")]

dataset_size_tot = 0

for iSample, sampleName in enumerate(l_sampleName) :
    
    print("\n")
    print("*"*50)
    print("Sample %d/%d: %s" %(iSample+1, len(l_sampleName), sampleName))
    print("*"*50)
    
    
    if (args.getCount) :
        
        command = "dasgoclient -query=\"file dataset=%s %s | sum(file.nevents)\"" %(sampleName, args.dasOptions)
        os.system(command)
        
        command = "dasgoclient -query=\"dataset=%s %s | grep dataset.size\"" %(sampleName, args.dasOptions)
        dataset_size = float(subprocess.check_output(command, shell = True).strip())
        dataset_size /= (1024**4) # TB
        dataset_size_tot += dataset_size
        print("Dataset size: %0.4f TB" %(dataset_size))
    
    
    if (args.getFiles) :
        
        sampleName_mod = sampleName[1:].replace("/", "_")
        
        outDir_mod = "%s/%s" %(args.outDir, sampleName_mod)
        
        command = "mkdir -p %s" %(outDir_mod)
        print("Command:", command)
        print("")
        os.system(command)
        
        outFile = "%s/%s.txt" %(outDir_mod, sampleName_mod)
        
        if (args.maxEvents is None) :
            
            command = "dasgoclient -query=\"file dataset=%s %s\" | sort -V > %s" %(sampleName, args.dasOptions, outFile)
            print("Command:", command)
            print("")
            os.system(command)
        
        else :
            
            command = "dasgoclient -query=\"file dataset=%s %s | grep file.name, file.nevents\" | sort -nr -k 2" %(args.dasOptions, sampleName)
            print("Command:", command)
            print("")
            cmd_result = subprocess.check_output(command, shell = True).strip()
            #print(cmd_result)
            l_file = cmd_result.split("\n")
            l_file = [_line.split() for _line in l_file]
            #print(l_file)
            
            nEvent_tot = 0
            
            l_file_selected = []
            
            for fName, nEvent in l_file :
                
                fName = fName.strip()
                nEvent = int(nEvent.strip())
                
                #print(fName, nEvent)
                
                l_file_selected.append(fName)
                nEvent_tot += nEvent
                
                if (nEvent_tot >= args.maxEvents) :
                    
                    break
            
            fileContent = "\n".join(l_file_selected)
            
            with open(outFile, "w") as f :
                
                f.write(fileContent)
        
        fileContent = ""
        
        print("Replacing \"%s\" with \"%s\" in file." %(toReplace, prefix))
        print("")
        
        print("Number of lines:")
        os.system("wc -l %s" %(outFile))
        print("")
        
        with open(outFile, "r") as f :
            
            fileContent = f.read()
        
        fileContent = fileContent.replace(toReplace, prefix)
        
        with open(outFile, "w") as f :
            
            f.write(fileContent)
    
    # https://twiki.cern.ch/twiki/bin/view/CMS/Rucio
    # https://twiki.cern.ch/twiki/bin/view/CMSPublic/RucioUserDocsQuotas
    # https://twiki.cern.ch/twiki/bin/view/CMSPublic/RucioUserDocsRules
    if (rucioConfirmed) :
        
        #command = "rucio add-rule cms:%s 1 %s" %(sampleName, args.tier2site)
        command = "rucio add-rule --ask-approval --lifetime 15552000 cms:%s 1 %s" %(sampleName, args.tier2site)
        print("Command:", command)
        print("")
        os.system(command)


if (args.getCount) :
    
    print("\n")
    print("="*50, "Summary", "="*50)
    print("")
    print("Total size: %0.4f TB" %(dataset_size_tot))

print("")
