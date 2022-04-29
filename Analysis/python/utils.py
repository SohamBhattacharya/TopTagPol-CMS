import argparse
import ctypes
import gc
import io
import matplotlib
import matplotlib.colors
import matplotlib.pyplot
#import mplhep
import numpy
import os
import psutil
import re
import sortedcontainers
import sparse
import subprocess
import time
import uproot
import yaml

import ROOT
ROOT.gROOT.SetBatch(1)

import CMS_lumi


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
uproot_lang.functions["nonzero"] = numpy.nonzero


def load_config(fileName) :
    
    with open(fileName, "r") as fopen :
        
        fileContent = fopen.read()
        print("Loading config:")
        print(fileContent)
        
        d_loadConfig = yaml.load(fileContent, Loader = yaml.FullLoader)
        
        #jetNameKey = d_loadConfig["jetName"].split(":")[0]
        #jetName = d_loadConfig["jetName"].split(":")[1]
        #
        #fileContent = fileContent.replace(jetNameKey, jetName)
        #
        #d_loadConfig = yaml.load(fileContent, Loader = yaml.FullLoader)
        
        d_loadConfig["fileContent"] = fileContent
        
        d_loadConfig = sortedcontainers.SortedDict(d_loadConfig)
        
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


def root_TGraph_to_TH1(graph, setError = True) :
    
    hist = graph.GetHistogram().Clone()
    hist.SetDirectory(0)
    
    nPoint = graph.GetN()
    
    for iPoint in range(0, nPoint) :
        
        if (hasattr(ROOT, "Double")) :
            
            pointValX = ROOT.Double(0)
            pointValY = ROOT.Double(0)
        
        else :
            
            pointValX = ctypes.c_double(0)
            pointValY = ctypes.c_double(0)
        
        graph.GetPoint(iPoint, pointValX, pointValY)
        #print(iPoint, pointValX, pointValY)
        
        pointErrX = graph.GetErrorX(iPoint)
        pointErrY = graph.GetErrorY(iPoint)
        
        binNum = hist.FindBin(pointValX)
        
        hist.SetBinContent(binNum, pointValY)
        
        if (setError) :
            
            hist.SetBinError(binNum, pointErrY)
    
    return hist


def wait_for_asyncpool(l_job) :
    
    l_isJobDone = [False] * len(l_job)
    
    while(False in l_isJobDone) :
        
        for iJob, job in enumerate(l_job) :
            
            if (job is None) :
                
                continue
            
            if (not l_isJobDone[iJob] and job.ready()) :
                
                l_isJobDone[iJob] = True
                
                retVal = job.get()
                
                l_job[iJob] = None
                
                if (not sum(l_isJobDone) % 10) :
                    
                    gc.collect()
    
    gc.collect()


def root_plot1D(
    l_hist,
    outfile,
    xrange,
    yrange,
    l_graph = [],
    canvassize = (600, 600),
    logx = False, logy = False,
    title = "",
    xtitle = "", ytitle = "",
    centertitlex = True, centertitley = True,
    centerlabelx = False, centerlabely = False,
    gridx = False, gridy = False,
    #ndivisionsx = [5, 5, 0],
    ndivisionsx = None,
    stackdrawopt = "nostack",
    legendpos = "UR",
    legendncol = 1,
    legendtextsize = 0.04,
    legendheightscale = 1.0, legendwidthscale = 1.0,
    lumiText = "(13 TeV)",
    cmsExtraText = "Simulation Preliminary",
) :
    
    ROOT.gROOT.LoadMacro("utils/tdrstyle.C")
    ROOT.gROOT.ProcessLine("setTDRStyle()")
    
    ROOT.gROOT.SetStyle("tdrStyle")
    ROOT.gROOT.ForceStyle(True)
    
    canvas = ROOT.TCanvas("canvas", "canvas", canvassize[0], canvassize[1])
    canvas.UseCurrentStyle()
    
    canvas.SetLeftMargin(0.16)
    canvas.SetRightMargin(0.05)
    canvas.SetTopMargin(0.1)
    canvas.SetBottomMargin(0.135)
    
    
    legendHeight = legendheightscale * 0.06 * (len(l_hist)+len(l_graph))
    legendWidth = legendwidthscale * 0.4
    
    padTop = 1 - canvas.GetTopMargin() - 1*ROOT.gStyle.GetTickLength("y")
    padRight = 1 - canvas.GetRightMargin() - 0.6*ROOT.gStyle.GetTickLength("x")
    padBottom = canvas.GetBottomMargin() + 0.6*ROOT.gStyle.GetTickLength("y")
    padLeft = canvas.GetLeftMargin() + 0.6*ROOT.gStyle.GetTickLength("x")
    
    if(legendpos == "UR") :
        
        legend = ROOT.TLegend(padRight-legendWidth, padTop-legendHeight, padRight, padTop)
    
    elif(legendpos == "LR") :
        
        legend = ROOT.TLegend(padRight-legendWidth, padBottom, padRight, padBottom+legendHeight)
    
    elif(legendpos == "LL") :
        
        legend = ROOT.TLegend(padLeft, padBottom, padLeft+legendWidth, padBottom+legendHeight)
    
    elif(legendpos == "UL") :
        
        legend = ROOT.TLegend(padLeft, padTop-legendHeight, padLeft+legendWidth, padTop)
    
    else :
        
        print("Wrong legend position option:", legendpos)
        exit(1)
    
    
    legend.SetNColumns(legendncol)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.SetTextSize(legendtextsize)
    
    stack = ROOT.THStack()
    
    for hist in l_hist :
        
        hist.GetXaxis().SetRangeUser(xrange[0], xrange[1])
        #hist.SetFillStyle(0)
        
        stack.Add(hist, "hist")
        legend.AddEntry(hist, hist.GetTitle(), "LP")
    
    # Add a dummy histogram so that the X-axis range can be beyond the histogram range
    h1_xRange = ROOT.TH1F("h1_xRange", "h1_xRange", 1, xrange[0], xrange[1])
    stack.Add(h1_xRange)
    
    stack.Draw(stackdrawopt)
    
    for gr in l_graph :
        
        gr.GetXaxis().SetRangeUser(xrange[0], xrange[1])
        #hist.SetFillStyle(0)
        
        gr.Draw("L SAME")
        legend.AddEntry(gr, gr.GetTitle(), "L")
    
    legend.Draw()
    
    stack.GetXaxis().SetRangeUser(xrange[0], xrange[1])
    stack.SetMinimum(yrange[0])
    stack.SetMaximum(yrange[1])
    
    if (ndivisionsx is not None) :
        
        stack.GetXaxis().SetNdivisions(ndivisionsx[0], ndivisionsx[1], ndivisionsx[2], False)
    
    #stack.GetXaxis().SetLabelSize(ROOT.gStyle.GetLabelSize("X") * xLabelSizeScale)
    #stack.GetYaxis().SetLabelSize(ROOT.gStyle.GetLabelSize("Y") * yLabelSizeScale)
    
    stack.GetXaxis().SetTitle(xtitle)
    #stack.GetXaxis().SetTitleSize(ROOT.gStyle.GetTitleSize("X") * xTitleSizeScale)
    stack.GetXaxis().SetTitleOffset(ROOT.gStyle.GetTitleOffset("X") * 1.1)
    
    stack.GetYaxis().SetTitle(ytitle)
    #stack.GetYaxis().SetTitleSize(ROOT.gStyle.GetTitleSize("Y") * yTitleSizeScale)
    stack.GetYaxis().SetTitleOffset(ROOT.gStyle.GetTitleOffset("Y") * 1)
    
    #stack.SetTitle(title)

    stack.GetXaxis().CenterTitle(centertitlex)
    stack.GetYaxis().CenterTitle(centertitley)
    
    stack.GetXaxis().CenterLabels(centerlabelx)
    stack.GetYaxis().CenterLabels(centerlabely)
    
    canvas.SetLogx(logx)
    canvas.SetLogy(logy)
    
    canvas.SetGridx(gridx)
    canvas.SetGridy(gridy)
    
    CMS_lumi.CMS_lumi(pad = canvas, iPeriod = 0, iPosX = 0, CMSextraText = cmsExtraText, lumiText = lumiText)
    
    if ("/" in outfile) :
        
        outdir = outfile
        outdir = outdir[0: outdir.rfind("/")]
        
        os.system("mkdir -p %s" %(outdir))
    
    canvas.SaveAs(outfile)
    
    return 0


if (__name__ == "__main__") :
    
    exit()

