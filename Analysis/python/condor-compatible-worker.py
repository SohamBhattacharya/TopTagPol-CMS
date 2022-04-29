from __future__ import print_function

#import mxnet
import argparse
import awkward
import collections
#import cppyy
#import cppyy.ll
import concurrent.futures
import datetime
import gc
import keras
import matplotlib
import matplotlib.colors
import matplotlib.pyplot
import memory_profiler
import multiprocessing
import multiprocessing.managers
import multiprocessing.shared_memory
import numpy
import os
import PIL
#import pprint
import psutil
import pympler
import ROOT
import sklearn
import sklearn.metrics
import sortedcontainers
import sparse
import sys
import tabulate
#import tensorflow
#import tensorflow.keras
import time
import uproot
import yaml

#from tensorflow.keras import datasets, layers, models
#from tensorflow.keras import mixed_precision

#policy = mixed_precision.Policy("mixed_float16")
#mixed_precision.set_global_policy(policy)

import utils


def main() :
    
    # Argument parser
    parser = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter)
    
    parser.add_argument(
        "--config",
        help = "Configuration file",
        type = str,
        required = True,
    )
    
    parser.add_argument(
        "--inFileNames",
        help = "Input file names (file1:tree1 file2:tree2 ...)",
        type = str,
        nargs = "*",
        required = False,
        default = None,
    )
    
    parser.add_argument(
        "--outFileName",
        help = "Output file name",
        type = str,
        required = True,
    )
    
    
    args = parser.parse_args()
    d_args = vars(args)
    
    
    d_config = utils.load_config(args.config)
    fileAndTreeNames = utils.get_fileAndTreeNames(args.inFileNames) if (args.inFileNames) is not None else d_config["samples"]
    
    nFile = len(fileAndTreeNames)
    
    if ("/" in args.outFileName) :
        
        outDir = args.outFileName[0: args.outFileName.rfind("/")]
        os.system("mkdir -p %s" %(outDir))
    
    outFileName = "file:%s" %(args.outFileName) if (args.outFileName.find("file:") != 0) else args.outFileName
    outFile = ROOT.TFile.Open(outFileName, "RECREATE")
    outFile.cd()
    
    print(fileAndTreeNames)
    
    for fntname in fileAndTreeNames :
        
        print(fntname)
        split_idx = fntname.rfind(":")
        fname = fntname[: split_idx]
        treename = fntname[split_idx+1:]
        print(fname)
        print(treename)
    
    # Loop over fileAndTreeNames
    
    outFile.Close()
    
    return 0



if (__name__ == "__main__") :
    
    main()
