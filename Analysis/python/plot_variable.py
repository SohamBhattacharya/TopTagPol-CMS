import argparse
import awkward
import matplotlib
import matplotlib.colors
import matplotlib.pyplot
import mplhep
import numpy
import os
import random
import re
import sortedcontainers
import time
import uproot

import ROOT
ROOT.gROOT.SetBatch(1)

import CMS_lumi
#import tdrstyle

import utils


def main() :
    
    
    # Argument parser
    parser = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter)
    
    parser.add_argument(
        "--fileAndTreeNames",
        help = "Syntax: fileName1:treeName1 fileName2:treeName2 ...",
        type = str,
        nargs = "*",
        required = True,
    )
    
    parser.add_argument(
        "--fileFraction",
        help = "Fraction of input files (from each entry) to use.",
        type = float,
        required = False,
        default = 1,
    )
    
    parser.add_argument(
        "--skipFileList",
        help = "File containing list of files to skip",
        type = str,
        required = False,
        default = None,
    )
    
    parser.add_argument(
        "--filePrefix",
        help = "File prefix (for e.g. root://dcache-cms-xrootd.desy.de:/)",
        type = str,
        required = False,
        default = "",
    )
    
    parser.add_argument(
        "--cuts",
        help = "Cuts",
        type = str,
        nargs = "*",
        required = True,
    )
    
    parser.add_argument(
        "--plotVars",
        help = (
            "Plot variables. A variable can be one of:\n"
            "1. A simple expression. For e.g. var1*var2\n"
            "2. A profile along 'X' or 'Y' from a 2D distribution, in the form: <y_expr>:<x_expr>:<profile_axis>. For e.g. var1:var2:X or var1:var2:Y"
        ),
        type = str,
        nargs = "*",
        required = True,
    )
    
    parser.add_argument(
        "--wVars",
        help = "Weight variables",
        type = str,
        nargs = "*",
        required = False,
        default = None,
    )
    
    parser.add_argument(
        "--nJetMax",
        help = "Maximum number of jets to plot",
        type = int,
        required = False,
        default = -1,
    )
    
    parser.add_argument(
        "--labels",
        help = "Plot labels",
        type = str,
        nargs = "*",
        required = True,
    )
    
    parser.add_argument(
        "--lineColors",
        help = "Line colors",
        type = int,
        nargs = "*",
        required = True,
    )
    
    parser.add_argument(
        "--lineStyles",
        help = "Line styles",
        type = int,
        nargs = "*",
        required = False,
        default = None,
    )
    
    parser.add_argument(
        "--lineWidths",
        help = "Line widths",
        type = int,
        nargs = "*",
        required = False,
        default = None,
    )
    
    parser.add_argument(
        "--plotBinX",
        help = "Bins: nBin min max",
        type = float,
        nargs = 3,
        required = True,
    )
    
    parser.add_argument(
        "--plotBinY",
        help = "Bins: nBin min max (only needed when plotVar is profiled from a 2D distribution. See above)",
        type = float,
        nargs = 3,
        required = False,
        default = (1, 0, 1),
    )
    
    parser.add_argument(
        "--xRange",
        help = "x-axis display range",
        type = float,
        nargs = 2,
        required = True,
    )
    
    parser.add_argument(
        "--yRange",
        help = "y-axis range",
        type = float,
        nargs = 2,
        required = True,
    )
    
    parser.add_argument(
        "--logX",
        help = "x-axis in log scale",
        default = False,
        action = "store_true",
    )
    
    parser.add_argument(
        "--logY",
        help = "y-axis in log scale",
        default = False,
        action = "store_true",
    )
    
    parser.add_argument(
        "--centerLabelX",
        help = "Center x-axis labels",
        default = False,
        action = "store_true",
    )
    
    parser.add_argument(
        "--xTitle",
        help = "X-axis title",
        type = str,
        required = False,
        default = "X",
    )
    
    parser.add_argument(
        "--yTitle",
        help = "Y-axis title",
        type = str,
        required = False,
        default = "Y",
    )
    
    parser.add_argument(
        "--nDivX",
        help = "X-axis divisions (ROOT): primary seconday tertiary. E.g. 5 5 0",
        type = int,
        nargs = 3,
        required = False,
        default = None,
    )
    
    parser.add_argument(
        "--nDivY",
        help = "Y-axis divisions (ROOT): primary seconday tertiary. E.g. 5 5 0",
        type = int,
        nargs = 3,
        required = False,
        default = None,
    )
    
    parser.add_argument(
        "--title",
        help = "Plot title",
        type = str,
        required = False,
        default = "",
    )
    
    parser.add_argument(
        "--titlePos",
        help = "Title position (in data coordinates): x y",
        type = float,
        nargs = 2,
        required = False,
        default = [0, 0],
    )
    
    parser.add_argument(
        "--histdrawopt",
        help = "Histogram draw option",
        type = str,
        required = False,
        default = "hist",
    )
    
    parser.add_argument(
        "--legendPos",
        help = "Legend position",
        type = str,
        required = False,
        choices = ["UL", "UR", "LR", "LL"],
        default = "UR",
    )
    
    parser.add_argument(
        "--legendncol",
        help = "Legend columns",
        type = int,
        required = False,
        default = 1,
    )
    
    parser.add_argument(
        "--outFileName",
        help = "Output file name",
        type = str,
        required = True,
    )
    
    
    # Parse arguments
    args = parser.parse_args()
    d_args = vars(args)
    
    
    if (args.lineStyles is None) :
        
        args.lineStyles = [1] * len(args.plotVars)
    
    if (args.lineWidths is None) :
        
        args.lineWidths = [2] * len(args.plotVars)
    
    
    l_hist = []
    
    for iVar, varExpr in enumerate(args.plotVars) :
        
        print("")
        print("="*50)
        
        print(args.fileAndTreeNames[iVar])
        
        histName = "hist_plotVar%d" %(iVar+1)
        
        
        plotVarNameX = "plotVarX"
        plotVarNameY = "plotVarY"
        weightVarName = "wVar"
        
        varExprY = None
        varExprX = varExpr
        profAx = None
        
        if (":" in varExpr) :
            
            varExprY, varExprX, profAx = varExpr.split(":")
            
            varExprX = varExprX.strip()
            varExprY = varExprY.strip()
            profAx = profAx.strip()
            
            assert(profAx in ["X", "Y"])
            
            hist_plotVar = ROOT.TH2F(
                histName, histName,
                int(args.plotBinX[0]), args.plotBinX[1], args.plotBinX[2],
                int(args.plotBinY[0]), args.plotBinY[1], args.plotBinY[2],
            )
        
        else :
            
            hist_plotVar = ROOT.TH1F(
                histName, histName,
                int(args.plotBinX[0]), args.plotBinX[1], args.plotBinX[2],
            )
        
        d_branchName_alias = {}
        d_branchName_alias[plotVarNameX] = varExprX
        
        if (varExprY is not None) :
            
            d_branchName_alias[plotVarNameY] = varExprY
        
        if (args.wVars is not None) :
            
            d_branchName_alias[weightVarName] = args.wVars[iVar]
        
        fileAndTreeNames = utils.get_fileAndTreeNames([args.fileAndTreeNames[iVar]], filePrefix = args.filePrefix)
        nFilesToUse = max(1, int(args.fileFraction * len(fileAndTreeNames)))
        fileAndTreeNames = random.choices(fileAndTreeNames, k = nFilesToUse)
        
        l_branchName = list(d_branchName_alias.keys())
        
        nJet = 0
        
        for tree_branches in uproot.iterate(
            files = fileAndTreeNames,
            expressions = l_branchName,
            aliases = d_branchName_alias,
            cut = args.cuts[iVar],
            language = utils.uproot_lang,
            step_size = 10000,
            num_workers = 10,
        ) :
            
            #print(fileAndTreeNames)
            
            a_plotVarX = awkward.flatten(tree_branches[plotVarNameX], axis = None).to_numpy().astype(dtype = numpy.float64)
            a_plotVarY = None
            
            if (not len(a_plotVarX)) :
                
                continue
            
            #print(a_plotVarX)
            #print(len(a_plotVarX), numpy.sum(numpy.isfinite(a_plotVarX)))
            
            a_wVar = awkward.flatten(tree_branches[weightVarName], axis = None).to_numpy() if (args.wVars is not None) else numpy.ones(len(a_plotVarX))
            
            if (varExprY is not None) :
                
                a_plotVarY = awkward.flatten(tree_branches[plotVarNameY], axis = None).to_numpy().astype(dtype = numpy.float64)
                hist_plotVar.FillN(len(a_plotVarX), a_plotVarX, a_plotVarY, a_wVar)
            
            else :
                
                hist_plotVar.FillN(len(a_plotVarX), a_plotVarX, a_wVar)
            
            nJet += len(a_plotVarX)
            
            if (args.nJetMax > 0 and nJet > args.nJetMax) :
                
                break
        
        
        print("Plot: %s" %(args.plotVars[iVar]))
        print("Cut : %s" %(args.cuts[iVar]))
        #print("Weight:  %s" %(str(...))
        print(" |-- Integral: %f, Entries: %f" %(hist_plotVar.Integral(), hist_plotVar.GetEntries()))
        #print(" |-- Underflow: %f, Overflow: %f" %(hist_plotVar.GetBinContent(0), hist_plotVar.GetBinContent(hist_plotVar.GetNbinsX()+1)))
        
        if (profAx is None and hist_plotVar.Integral()) :
            
            hist_plotVar.Scale(1.0 / hist_plotVar.Integral())
        
        ##hist_plotVar.Scale(1.0 / hist_plotVar.GetEntries())
        
        if (profAx == "X") :
            
            hist_plotVar = hist_plotVar.ProfileX("_pfx", 1, -1, "i")
        
        elif (profAx == "Y") :
            
            hist_plotVar = hist_plotVar.ProfileY("_pfy", 1, -1, "i")
        
        hist_plotVar.SetLineColor(args.lineColors[iVar])
        hist_plotVar.SetLineStyle(args.lineStyles[iVar])
        hist_plotVar.SetLineWidth(args.lineWidths[iVar])
        
        hist_plotVar.SetMarkerColor(args.lineColors[iVar])
        hist_plotVar.SetMarkerSize(0)
        hist_plotVar.SetFillStyle(0)
        hist_plotVar.SetTitle(args.labels[iVar])
        
        l_hist.append(hist_plotVar)
        
        print("="*50)
        print("")
    
    
    utils.root_plot1D(
        l_hist = l_hist,
        xrange = args.xRange,
        yrange = args.yRange,
        logx = args.logX, logy = args.logY,
        title = args.title,
        xtitle = args.xTitle, ytitle = args.yTitle,
        centertitlex = True, centertitley = True,
        centerlabelx = args.centerLabelX,
        gridx = True, gridy = True,
        ndivisionsx = args.nDivX,
        stackdrawopt = "nostack",
        histdrawopt = args.histdrawopt,
        legendpos = args.legendPos,
        legendncol = args.legendncol,
        legendtextsize = 0.03,
        legendwidthscale = 1.8,
        legendheightscale = 0.6,
        outfile = args.outFileName,
    )
    
    
    return 0


if (__name__ == "__main__") :
    
    main()
