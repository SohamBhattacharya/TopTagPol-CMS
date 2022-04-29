import argparse
import awkward
import boost_histogram
import copy
import dataclasses
import gc
import io
import matplotlib
import matplotlib.colors
import matplotlib.pyplot
#import mplhep
import multiprocessing
import numpy
import os
import psutil
import re
import sortedcontainers
import sparse
import subprocess
#import tensorflow
import time
import uproot
import yaml

import ROOT

from typing import List, Set, Dict, Tuple, Optional


uproot_lang = uproot.language.python.PythonLanguage()
uproot_lang.functions["min"] = numpy.minimum
uproot_lang.functions["max"] = numpy.maximum
uproot_lang.functions["where"] = numpy.where
uproot_lang.functions["sum"] = numpy.sum


d_sliceInfo_template = {
    "a_catNum":             [],
    
    "a_sampleIdx":          [],
    "a_fileIdx":            [],
    
    "a_evtIdx_start":       [],
    "a_jetIdx_start":       [],
    
    "a_evtIdx_end":         [],
    "a_jetIdx_end":         [],
}


class ColorPalette :
    
    def __init__(
        self,
        a_r,
        a_g,
        a_b,
        a_stop,
    ) :
        
        
        self.a_r = a_r
        self.a_g = a_g
        self.a_b = a_b
        self.a_stop = a_stop
        
        self.nStop = len(a_stop)
    
    def set(self, nContour = 500) :
        
        ROOT.gStyle.SetNumberContours(nContour)
        ROOT.TColor.CreateGradientColorTable(self.nStop, self.a_stop, self.a_r, self.a_g, self.a_b, nContour)


cpalette_nipy_spectral = ColorPalette(
    a_r = numpy.array([0.0, 0.4667, 0.5333, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7333, 0.9333, 1.0, 1.0, 1.0, 0.8667, 0.8, 0.8]),
    a_g = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.4667, 0.6, 0.6667, 0.6667, 0.6, 0.7333, 0.8667, 1.0, 1.0, 0.9333, 0.8, 0.6, 0.0, 0.0, 0.0, 0.8]),
    a_b = numpy.array([0.0, 0.5333, 0.6, 0.6667, 0.8667, 0.8667, 0.8667, 0.6667, 0.5333, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.8]),
    a_stop = numpy.array([0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]),
)


def print_boostHist(hist, scale_by_binWidth = False) :
    
    nAx = hist.ndim
    
    for iAx in range(0, nAx) :
        
        print("Projecting axis %d (%d/%d):" %(iAx, iAx+1, nAx))
        
        hist_proj = hist.project(iAx)
        
        if (scale_by_binWidth) :
            
            hist_proj /= hist_proj.axes[0].widths
        
        print(hist_proj)


def get_boostHist(
    l_histAxis,
    d_uproot_iterate_kwargs,
    maxEntries = -1,
) :
    
    hist = boost_histogram.Histogram(*l_histAxis)
    
    d_uproot_iterate_kwargs["language"] = uproot_lang
    
    for branches in uproot.iterate(
        **d_uproot_iterate_kwargs
    ) :
        
        l_data = [awkward.flatten(branches[_key], axis = None) for _key in d_uproot_iterate_kwargs["aliases"].keys()]
        
        if (
            maxEntries > 0 and
            hist.sum()+len(l_data[0]) > maxEntries
        ) :
            
            last_idx = int(maxEntries - hist.sum())
            l_data = [_arr[0: last_idx] for _arr in l_data]
        
        hist.fill(
            *l_data
        )
        
        if (
            maxEntries > 0 and
            hist.sum() >= maxEntries
        ) : 
            
            break
    
    #print("Returning from get_boostHist(...)...")
    return hist


@dataclasses.dataclass
class CategoryInfo :
    
    catNum                  : int
    catName                 : str
    l_sample                : List[str]
    cut                     : str
    nCpu                    : int
    l_reweightBrDict        : List[Dict]            = None
    
    def __post_init__(
        self,
    ) :
        
        self.nJet = 0
        
        self.l_sample_fileAndTreeName = [None] * len(self.l_sample)
        self.l_sample_weight = [1] * len(self.l_sample)
        self.l_sample_nJet = [0] * len(self.l_sample)
        self.l_sample_nJetMax = [-1] * len(self.l_sample)
        
        self.reweightHist = None
        self.reweightHistWeight = None
        self.l_reweightHistAxis = None
        
        for iSample, sample in enumerate(self.l_sample) :
            
            l_token = sample.strip().split(":")
            
            fName = l_token[0]
            treeName = l_token[1]
            
            if (".txt" in fName) :
                
                #self.l_sample_fileAndTreeName[iSample] = ["%s:%s" %(ele, treeName) for ele in numpy.loadtxt(fName, dtype = str, delimiter = "*"*100)]
                self.l_sample_fileAndTreeName[iSample] = ["root://dcache-cms-xrootd.desy.de/%s:%s" %(_ele, treeName) for _ele in numpy.loadtxt(fName, dtype = str, delimiter = "*"*100)]
            
            elif (".root" in fName) :
                
                self.l_sample_fileAndTreeName[iSample] = ["root://dcache-cms-xrootd.desy.de/%s:%s" %(fName, treeName)]
            
            else :
                
                print("Invalid entry for sample: %s" %(sample))
                exit(1)
            
            if (len(l_token) > 2) :
                
                weight = float(l_token[2])
                self.l_sample_weight[iSample] = weight
            
            if (len(l_token) > 3) :
                
                nJetMax = int(l_token[3])
                self.l_sample_nJetMax[iSample] = nJetMax
        
        
        if (self.l_reweightBrDict is not None) :
            
            self.d_reweightBrName_alias  = sortedcontainers.SortedDict({"reweightBr%d" %(_idx): _dct["name"] for _idx, _dct in enumerate(self.l_reweightBrDict)})
            self.d_reweightBrBinEdges    = sortedcontainers.SortedDict({"reweightBr%d" %(_idx): eval(_dct["bins"]) for _idx, _dct in enumerate(self.l_reweightBrDict)})
            
            self.l_reweightHistAxis = [boost_histogram.axis.Variable(_bins) for _bins in self.d_reweightBrBinEdges.values()]
            
            self.reweightHist = boost_histogram.Histogram(*self.l_reweightHistAxis)
            
            print(self.reweightHist)
            print(self.d_reweightBrName_alias)
            
            self.create_reweightHist()
    
    
    def create_reweightHist(self) :
        
        l_job = []
        
        with multiprocessing.Pool(
            processes = self.nCpu,
            #maxtasksperchild = 1
        ) as pool :
            
            for iSample, sample in enumerate(self.l_sample) :
                
                if (self.reweightHist is not None) :
                    
                    d_uproot_iterate_kwargs = {
                        "files" : self.l_sample_fileAndTreeName[iSample],
                        "expressions" : list(self.d_reweightBrName_alias.keys()),
                        "cut" : self.cut,
                        "aliases" : self.d_reweightBrName_alias,
                        #"language" : uproot_lang, # Cannot pickle the language
                        "step_size" : int(1e6),
                        "num_workers" : 30,
                        #xrootd_handler" : uproot.MultithreadedXRootDSource,
                        "timeout" : None,
                    }
                    
                    l_job.append(pool.apply_async(
                        get_boostHist,
                        (),
                        dict(
                            l_histAxis = self.l_reweightHistAxis,
                            d_uproot_iterate_kwargs = d_uproot_iterate_kwargs,
                            maxEntries = self.l_sample_nJetMax[iSample],
                        ),
                    ))
            
            
            pool.close()
            
            l_isJobDone = [False] * len(l_job)
            
            while(False in l_isJobDone) :
                
                for iJob, job in enumerate(l_job) :
                    
                    if (job is None) :
                        
                        continue
                    
                    if (not l_isJobDone[iJob] and job.ready()) :
                        
                        l_isJobDone[iJob] = True
                        
                        hist_job = job.get()
                        self.reweightHist += hist_job
                        
                        print("Loaded histogram %d for cat %d. Jobs done: %d/%d." %(iJob, self.catNum, sum(l_isJobDone), len(l_isJobDone)))
                        
                        l_job[iJob] = None
                        
                        if (not sum(l_isJobDone) % 10) :
                            
                            gc.collect()
            
            pool.join()
        
        gc.collect()
        
        if (self.reweightHist is not None) :
            
            # Normalize histogram
            print(self.reweightHist.sum())
            self.reweightHist /= self.reweightHist.sum()
            
            print_boostHist(self.reweightHist, scale_by_binWidth = True)
    
    
    def set_reweightInfo(
        self,
        reweightHist,
        reweightHistWeight,
    ) :
        
        self.reweightHist = reweightHist.copy(deep = True)
        self.reweightHistWeight = reweightHistWeight.copy(deep = True)


def load_catInfo_from_config(
    d_loadConfig,
    loadReweightInfo = True,
) :
    
    d_catInfo = sortedcontainers.SortedDict()
    
    reweightBrKey = "reweightBranches"
    reweightRefCatNum = None
    reweightRefCatName = None
    
    if (loadReweightInfo and reweightBrKey in d_loadConfig) :
        
        key = "reweightRefCategory"
        assert(key in d_loadConfig)
        reweightRefCatName = d_loadConfig[key]
    
    nCpu = int(d_loadConfig["cpuFrac"] * multiprocessing.cpu_count())
    nCpu = max(1, nCpu)
    
    for iCat, cat in enumerate(d_loadConfig["categories"]) :
        
        d_catInfo[iCat] = CategoryInfo(
            catNum = iCat,
            catName = cat["name"],
            l_sample = cat["samples"],
            cut = cat["cut"],
            l_reweightBrDict = d_loadConfig[reweightBrKey] if (loadReweightInfo and reweightBrKey in d_loadConfig) else None,
            nCpu = nCpu,
        )
        
        if (reweightRefCatName == cat["name"]) :
            
            reweightRefCatNum = iCat
    
    if (loadReweightInfo and reweightRefCatName is not None) :
        
        assert(reweightRefCatNum is not None)
        
        for iCat, catInfo in enumerate(d_catInfo.values()) :
            
            catInfo.reweightHistWeight = d_catInfo[reweightRefCatNum].reweightHist / catInfo.reweightHist
            
            catInfo.reweightHistWeight.values(flow = True)[numpy.isnan(catInfo.reweightHistWeight.values(flow = True))] = 0
            catInfo.reweightHistWeight.values(flow = True)[numpy.isinf(catInfo.reweightHistWeight.values(flow = True))] = 0
    
    return d_catInfo


def replace_in_list(l, find, repl) :
    
    return [s.replace(find, repl) for s in l]
    
    for idx in range(0, len(l)) :
        
        if (isinstance(d[key], str)) :
            
            d[key] = d[key].replace(find, repl)
        
        elif (isinstance(d[key], list)) :
            
            d[key] = replace_in_list(d[key], find, repl)
        
        elif (isinstance(d[key], dict)) :
            
            replace_in_dict(d[key], find, repl)


def replace_in_dict(d, find, repl) :
    
    for key in d :
        
        if (isinstance(d[key], str)) :
            
            d[key] = d[key].replace(find, repl)
        
        elif (isinstance(d[key], list)) :
            
            d[key] = replace_in_list(d[key], find, repl)
        
        elif (isinstance(d[key], dict)) :
            
            replace_in_dict(d[key], find, repl)
    
    
    #return d


def load_config(fileName) :
    
    with open(fileName, "r") as fopen :
        
        fileContent = fopen.read()
        print("Loading config:")
        print(fileContent)
        
        d_loadConfig = yaml.load(fileContent, Loader = yaml.FullLoader)
        
        if ("jetName" in d_loadConfig.keys()) :
            
            jetNameKey = d_loadConfig["jetName"].split(":")[0]
            jetName = d_loadConfig["jetName"].split(":")[1]
            
            fileContent = fileContent.replace(jetNameKey, jetName)
        
        d_loadConfig = yaml.load(fileContent, Loader = yaml.FullLoader)
        
        d_loadConfig["fileContent"] = fileContent
        
        return d_loadConfig


def run_cmd_list(l_cmd) :
    
    for cmd in l_cmd :
        
        retval = os.system(cmd)
        
        if (retval) :
            
            exit()


def getMemoryMB(process = -1) :
    
    if (process < 0) :
        
        process = psutil.Process(os.getpid())
    
    mem = process.memory_info().rss / 1024.0**2
    
    return mem


def get_fileAndTreeNames(in_list) :
    
    fileAndTreeNames = []
    
    for fName in in_list :
        
        if (".root" in fName) :
            
            fileAndTreeNames.append(fName)
        
        elif (".txt" in fName) :
            
            sourceFile, treeName = fName.strip().split(":")
            
            rootFileNames = numpy.loadtxt(sourceFile, dtype = str, delimiter = "*"*100)
            
            for rootFileName in rootFileNames :
                
                fileAndTreeNames.append("%s:%s" %(rootFileName, treeName))
        
        else :
            
            print("Error. Invalid syntax for fileAndTreeNames: %s" %(fName))
            exit(1)
    
    return fileAndTreeNames


def format_file(filename, d, execute = False) :
    
    l_cmd = []
    
    for key in d :
        
        val = d[key]
        
        l_cmd.append("sed -i \"s#{find}#{repl}#g\" {filename}".format(
            find = key,
            repl = val,
            filename = filename,
        ))
    
    if (execute) :
        
        run_cmd_list(l_cmd)
    
    else :
        
        return l_cmd


def get_name_withtimestamp(dirname) :
    
    if (os.path.exists(dirname)) :
        
        timestamp = subprocess.check_output(["date", "+%Y-%m-%d_%H-%M-%S", "-r", dirname]).strip()
        timestamp = timestamp.decode("UTF-8") # Convert from bytes to string
        
        dirname_new = "%s_%s" %(dirname, str(timestamp))
        
        return dirname_new
    
    return None


def benchmark(dataset, num_epochs = 5):
    start_time = time.perf_counter()
    for epoch_num in range(num_epochs):
        print("Training epoch %d/%d" %(epoch_num+1, num_epochs))
        for sample in dataset:
            
            x, y = sample
            print({key: x[key].get_shape() for key in x.keys()}, y.get_shape())
            # Performing a training step
            time.sleep(0.1)
    print("Execution time:", time.perf_counter() - start_time)
