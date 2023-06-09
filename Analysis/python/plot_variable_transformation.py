import argparse
import collections
import awkward
import logging
import matplotlib
import matplotlib.colors
import matplotlib.pyplot
import numpy
import os
import random
import re
import scipy.stats
import sortedcontainers
import sys
import tdigest
import time
import uproot
import yaml

import ROOT
ROOT.gROOT.SetBatch(1)

import CMS_lumi
#import tdrstyle

import utils


logging.basicConfig(format = "[%(asctime)s] %(levelname)s: %(message)s", level = logging.INFO)

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
        default = 0.1,
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
        help = "Plot variables",
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
        "--varNameSummary",
        help = "Name to use in the summary (such as storing the transformation)",
        type = str,
        required = False,
        default = "var",
    )
    
    parser.add_argument(
        "--trRange",
        help = "Transformation not needed if the variable does not exceed this range. Syntax: lwr upr",
        type = float,
        nargs = 2,
        required = False,
        default = [-5, 5],
    )
    
    parser.add_argument(
        "--nJetMax",
        help = "Maximum number of jets to plot",
        type = int,
        required = False,
        default = 100000,
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
        "--legendPos",
        help = "Legend position",
        type = str,
        required = False,
        choices = ["UL", "UR", "LR", "LL"],
        default = "UR",
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
    l_histTr = []
    l_varData = []
    nEntry_total = 0
    varMin = sys.float_info.max
    varMax = -sys.float_info.max
    
    # combine percentiles of datasets (for e.g. when streaming data): https://github.com/CamDavidsonPilon/tdigest
    digest = tdigest.TDigest()
    
    l_tranformationStr = []
    
    for iVar, varName in enumerate(args.plotVars) :
        
        l_varData.append(collections.deque())
        
        print(f"files: {args.fileAndTreeNames[iVar]}")
        print(f"plot: {varName}")
        print(f"cut: {args.cuts[iVar]}")
        
        plotVarName = "plotVar"
        weightVarName = "wVar"
        
        d_branchName_alias = {}
        d_branchName_alias[plotVarName] = args.plotVars[iVar]
        
        if (args.wVars is not None) :
            
            d_branchName_alias[weightVarName] = args.wVars[iVar]
        
        fileAndTreeNames = utils.get_fileAndTreeNames([args.fileAndTreeNames[iVar]], filePrefix = args.filePrefix, skip = args.skipFileList)
        nFilesToUse = max(1, int(args.fileFraction * len(fileAndTreeNames)))
        fileAndTreeNames = random.choices(fileAndTreeNames, k = nFilesToUse)
        #print(fileAndTreeNames)
        
        l_branchName = list(d_branchName_alias.keys())
        
        #print(l_branchName)
        #print(d_branchName_alias)
        #print(args.cuts[iVar])
        
        for iFile, fName in enumerate(fileAndTreeNames) :
            
            nTry = 1
            maxTry = 10
            success = False
            
            while (not success and nTry < maxTry) :
                
                try :
                    
                    tree_branches = uproot.concatenate(
                        files = fName,
                        expressions = l_branchName,
                        aliases = d_branchName_alias,
                        cut = args.cuts[iVar],
                        #language = utils.uproot_lang,
                        num_workers = 10,
                        timeout = None,
                    )
                    
                    success = True
                
                except Exception as exc:
                    
                    nTry += 1
                    success = False
                    logging.warning(exc)
                    wait = 10
                    logging.info(f"Wait for {wait}s and retry (trial {nTry}/{maxTry}) {fName}")
                    time.sleep(wait)
            
            if (not success) :
                
                logging.warning(f"Could not file, hence skipped: {fName}")
                continue
            
            a_plotVar = awkward.flatten(tree_branches[plotVarName], axis = None).to_numpy().astype(dtype = numpy.float64)
            l_varData[iVar].extend(a_plotVar)
            nEntry_total += len(a_plotVar)
            
            digest.batch_update(a_plotVar)
            #digest.compress()
            
            varMin = min(min(a_plotVar), varMin)
            varMax = max(max(a_plotVar), varMax)
    
    # Convert dequeue to array
    l_varData = [numpy.array(_ele) for _ele in l_varData]
    
    ptile_lwr = digest.percentile(16)
    ptile_med = digest.percentile(50)
    ptile_upr = digest.percentile(84)
    sigma = 0.5*(ptile_upr-ptile_lwr)
    
    l_tranformationStr.append(f"")
    
    # Freedman-Diaconis rule
    nEntry = int(numpy.median(([len(_ele) for _ele in l_varData])))
    binSize = 2.0 * (digest.percentile(75) - digest.percentile(25)) * (nEntry**(-1.0/3))
    range_lwr = min(ptile_med-1.5*sigma, digest.percentile(2.5))
    range_upr = max(ptile_med+1.5*sigma, digest.percentile(97.5))
    nBin = int((range_upr - range_lwr) / binSize)
    
    histMax = None
    
    for iVar, varName in enumerate(args.plotVars) :
        
        a_plotVar = l_varData[iVar]
        
        histName = "h1_var%d" %(iVar+1)
        h1_var = ROOT.TH1F(histName, histName, nBin, range_lwr, range_upr)
        h1_var.FillN(len(a_plotVar), a_plotVar, ROOT.nullptr)
        
        utils.root_TH1_fixFlowBins(h1_var)
        
        if (h1_var.Integral()) :
            
            h1_var.Scale(1.0 / h1_var.Integral())
        
        h1_var.SetLineColor(args.lineColors[iVar])
        h1_var.SetLineStyle(args.lineStyles[iVar])
        h1_var.SetLineWidth(args.lineWidths[iVar])
        
        h1_var.SetMarkerColor(args.lineColors[iVar])
        h1_var.SetMarkerSize(0)
        h1_var.SetFillStyle(0)
        h1_var.SetTitle(args.labels[iVar])
        
        l_hist.append(h1_var)
        
        if (histMax is None or h1_var.GetMaximum() > histMax) :
            
            histMax = h1_var.GetMaximum()
    
    #print(digest.to_dict())
    
    print(ptile_lwr, ptile_med, ptile_upr)
    
    lwr = ptile_med-sigma
    upr = ptile_med+sigma
    
    tl_ptile_lwr = ROOT.TLine(lwr, args.yRange[0], lwr, 1.5*histMax)
    tl_ptile_med = ROOT.TLine(ptile_med, args.yRange[0], ptile_med, 1.5*histMax)
    tl_ptile_upr = ROOT.TLine(upr, args.yRange[0], upr, 1.5*histMax)
    
    tl_ptile_lwr.SetLineColor(2)
    tl_ptile_lwr.SetLineStyle(3)
    tl_ptile_lwr.SetLineWidth(2)
    
    tl_ptile_med.SetLineColor(2)
    tl_ptile_med.SetLineStyle(7)
    tl_ptile_med.SetLineWidth(2)
    
    tl_ptile_upr.SetLineColor(2)
    tl_ptile_upr.SetLineStyle(3)
    tl_ptile_upr.SetLineWidth(2)
    
    l_line = [tl_ptile_med]
    
    if (range_lwr < tl_ptile_lwr.GetX1()) :
        
        l_line.append(tl_ptile_lwr)
    
    if (range_upr > tl_ptile_upr.GetX1()) :
        
        l_line.append(tl_ptile_upr)
    
    utils.root_plot1D(
        l_hist = l_hist,
        l_line = l_line,
        xrange = (range_lwr, range_upr),
        yrange = args.yRange,
        logx = args.logX,
        logy = args.logY,
        title = args.title,
        xtitle = args.xTitle,
        ytitle = args.yTitle,
        centertitlex = True,
        centertitley = True,
        centerlabelx = args.centerLabelX,
        gridx = True,
        gridy = True,
        ndivisionsx = args.nDivX,
        stackdrawopt = "nostack",
        legendpos = args.legendPos,
        legendncol = 1,
        legendtextsize = 0.04,
        outfile = args.outFileName,
    )
    
    xRangeTr = args.trRange
    trNeeded = bool((varMin < xRangeTr[0]) or (varMax > xRangeTr[1]))
    
    for iVar, varName in enumerate(args.plotVars) :
        
        a_plotVar = l_varData[iVar]
        
        histName = "h1_varTr%d" %(iVar+1)
        h1_var = ROOT.TH1F(histName, histName, 100, xRangeTr[0], xRangeTr[1])
        h1_var.FillN(len(a_plotVar), (a_plotVar-ptile_med)/sigma, ROOT.nullptr)
        
        utils.root_TH1_fixFlowBins(h1_var)
        
        if (h1_var.Integral()) :
            
            h1_var.Scale(1.0 / h1_var.Integral())
        
        h1_var.SetLineColor(args.lineColors[iVar])
        h1_var.SetLineStyle(args.lineStyles[iVar])
        h1_var.SetLineWidth(args.lineWidths[iVar])
        
        h1_var.SetMarkerColor(args.lineColors[iVar])
        h1_var.SetMarkerSize(0)
        h1_var.SetFillStyle(0)
        h1_var.SetTitle(args.labels[iVar])
        
        l_histTr.append(h1_var)
    
    # Compute pairwise KS
    for iVar in range(len(args.plotVars)-1) :
        
        for jVar in range(iVar+1, len(args.plotVars)) :
            
            a_plotVar_1 = l_varData[iVar]
            a_plotVar_2 = l_varData[jVar]
            
            #result_kstest = scipy.stats.ks_2samp(a_plotVar_1, a_plotVar_2)
            #print(result_kstest)
            #print(f"\t * KS {result_kstest.statistic:0.4e}, {result_kstest.pvalue:0.4e}")
    
    result_adtest = scipy.stats.anderson_ksamp(l_varData)
    #print(result_adtest)
    #print(f"\t * AD {result_adtest.statistic:0.4e}, {result_adtest.pvalue:0.4e}")
    
    outfname, outfext = os.path.splitext(args.outFileName)
    
    utils.root_plot1D(
        l_hist = l_histTr,
        xrange = xRangeTr,
        yrange = args.yRange,
        logx = args.logX,
        logy = args.logY,
        title = args.title,
        xtitle = f"#hat{{#sigma}}({args.xTitle})",
        ytitle = args.yTitle,
        centertitlex = True,
        centertitley = True,
        centerlabelx = args.centerLabelX,
        gridx = True,
        gridy = True,
        ndivisionsx = [5, 5, 0],
        forcedivs = True,
        stackdrawopt = "nostack",
        legendpos = args.legendPos,
        legendncol = 1,
        legendtextsize = 0.04,
        outfile = f"{outfname}_transformed{outfext}",
    )
    
    print(sigma)
    d_trans = {
        args.varNameSummary: {
            "needed": trNeeded,
            "center": float(ptile_med),
            "scale": float(1.0/sigma),
            "ADtest": {
                "statistic": float(result_adtest.statistic),
            },
        },
    }
    
    yaml_trans = yaml.dump(d_trans)
    outyamlname = f"{outfname}_transformation.yaml"
    print(f"Saving tranformation of {args.varNameSummary} to: {outyamlname}")
    
    with open(outyamlname, "w") as outfile :
        
        outfile.write(yaml_trans)
    
    
    return 0


if (__name__ == "__main__") :
    
    main()
