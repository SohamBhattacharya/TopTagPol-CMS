import argparse
import matplotlib
import matplotlib.colors
import matplotlib.pyplot
import mplhep
import numpy
import os
import psutil
import re
import sortedcontainers
import time
import uproot
import yaml

import ROOT


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


uproot_lang = uproot.language.python.PythonLanguage()
uproot_lang.functions["min"] = numpy.minimum
uproot_lang.functions["max"] = numpy.maximum
uproot_lang.functions["where"] = numpy.where


def getMemoryMB(process = -1) :
    
    if (process < 0) :
        
        process = psutil.Process(os.getpid())
    
    mem = process.memory_info().rss / 1024.0**2
    
    return mem


def load_config(fileName) :
    
    with open(fileName, "r") as fopen :
        
        fileContent = fopen.read()
        print("Loading config:")
        print(fileContent)
        
        d_loadConfig = yaml.load(fileContent, Loader = yaml.FullLoader)
        
        jetNameKey = d_loadConfig["jetName"].split(":")[0]
        jetName = d_loadConfig["jetName"].split(":")[1]
        
        fileContent = fileContent.replace(jetNameKey, jetName)
        
        d_loadConfig = yaml.load(fileContent, Loader = yaml.FullLoader)
        
        d_loadConfig["fileContent"] = fileContent
        
        return d_loadConfig


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


if (__name__ == "__main__") :
    
    exit()
