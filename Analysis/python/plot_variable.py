import argparse
import awkward
import collections
import matplotlib
import matplotlib.colors
import matplotlib.pyplot
import mplhep
import numpy
import os
import random
import re
import scipy.stats
import sortedcontainers
import time
import uproot
import yaml

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
        "--sampleYaml",
        help = "Yaml file with the sample dictionary (names, cross sections). Needed only if fileAndTreeNames contains {sampleName} (for e.g. {QCD}) -- then sampleName will be read from the yaml.",
        type = str,
        required = False,
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
            "2. A profile along 'X' or 'Y' from a 2D distribution, in the form: <y_expr>:<x_expr>:<profile_axis>. For e.g. var1:var2:X or var1:var2:Y\n"
            #"Note that in option 2, this will also plot the projection along X for each bin in Y, if Y is chosen as the profile axis.\n"
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
        "--testW1",
        help = "Calculate the Wassetstein distance w.r.t. a reference distribution. Provide the index (indices start from 0) of the reference distribution (plotVars entry)",
        type = int,
        required = False,
        default = None,
    )
    
    #parser.add_argument(
    #    "--nJetMax",
    #    help = "Maximum number of jets to plot",
    #    type = int,
    #    required = False,
    #    default = -1,
    #)
    
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
        help = (
            "Uniform binning: nBin min max\n"
            "Non-uniform bin boundaries (start with 3 zeros): 0 0 0 boundary1 boundary2 ... "
        ),
        type = float,
        nargs = "*",
        required = True,
    )
    
    parser.add_argument(
        "--plotBinY",
        help = (
            "Only needed when plotVar is profiled from a 2D distribution. See above.\n"
            "Uniform binning: nBin min max\n"
            "Non-uniform bin boundaries (start with 3 zeros): 0 0 0 boundary1 boundary2 ... "
        ),
        type = float,
        nargs = "*",
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
    
    d_sample = None
    
    if (args.sampleYaml) :
        
        with open(args.sampleYaml, "r") as fopen :
            
            d_sample = yaml.load(fopen.read(), Loader = yaml.FullLoader)
    
    l_hist = []
    l_histGroup = []
    l_histGroup_outFileName = []
    
    l_hist_ref = []
    
    l_varData = []
    l_varWeight = []
    
    for iVar, varExpr in enumerate(args.plotVars) :
        
        print("")
        print("="*50)
        
        print(args.fileAndTreeNames[iVar])
        
        if (args.testW1) :
            
            l_varData.append(collections.deque())
            l_varWeight.append(collections.deque())
        
        histName = "hist_plotVar%d" %(iVar+1)
        
        plotVarNameX = "plotVarX"
        plotVarNameY = "plotVarY"
        weightVarName = "wVar"
        
        varExprY = None
        varExprX = varExpr
        profAx = None
        a_binsX = None
        a_binsY = None
        
        if (":" in varExpr) :
            
            varExprY, varExprX, profAx = varExpr.split(":")
            
            varExprX = varExprX.strip()
            varExprY = varExprY.strip()
            profAx = profAx.strip()
            
            assert(profAx in ["X", "Y"])
            
            l_args = []
            
            if (len(args.plotBinX) > 4 and (args.plotBinX[0] == args.plotBinX[1] == args.plotBinX[2] == 0)) :
                
                a_binsX = numpy.array(args.plotBinX[3:], dtype = numpy.float64)
                
                l_args.extend([len(a_binsX)-1, a_binsX])
            
            else :
                
                l_args.extend([int(args.plotBinX[0]), args.plotBinX[1], args.plotBinX[2]])
            
            if (len(args.plotBinY) > 4 and (args.plotBinY[0] == args.plotBinY[1] == args.plotBinY[2] == 0)) :
                
                a_binsY = numpy.array(args.plotBinY[3:], dtype = numpy.float64)
                
                l_args.extend([len(a_binsY)-1, a_binsY])
            
            else :
                
                l_args.extend([int(args.plotBinY[0]), args.plotBinY[1], args.plotBinY[2]])
            
            hist_plotVar = ROOT.TH2F(
                histName, histName,
                *l_args,
            )
            #    
            #else :
            #    
            #    hist_plotVar = ROOT.TH2F(
            #        histName, histName,
            #        int(args.plotBinX[0]), args.plotBinX[1], args.plotBinX[2],
            #        int(args.plotBinY[0]), args.plotBinY[1], args.plotBinY[2],
            #    )
        
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
        
        l_sample = [args.fileAndTreeNames[iVar]]
        l_sample_weight = [1.0]
        sample_key = None
        
        if ("{" in l_sample[0] and "}" in l_sample[0]) :
            
            sample_key = re.findall(r"{([^{}]*?)}", args.fileAndTreeNames[iVar])[0] # Should only have 1 key
            
            assert (sample_key in d_sample), f"{sample_key} not found in {list(d_sample.keys())}"
            
            l_sample = [
                args.fileAndTreeNames[iVar].format(**{sample_key: _name})
                for _name in d_sample[sample_key]["names"]
            ]
            
            l_sample_weight = d_sample[sample_key]["weights"]
        
        #print(l_sample)
        
        for iSample, sample in enumerate(l_sample):
            
            fileAndTreeNames = utils.get_fileAndTreeNames([sample], filePrefix = args.filePrefix)
            nFilesToUse = max(1, int(args.fileFraction * len(fileAndTreeNames)))
            fileAndTreeNames = random.choices(fileAndTreeNames, k = nFilesToUse)
            
            nJet = 0
            event_no_br = None
            sample_nevent = 0
            
            if (sample_key and "event_no_br" in d_sample[sample_key]) :
                
                event_no_br = d_sample[sample_key]["event_no_br"]
                
                a_event_no = awkward.flatten(
                    uproot.concatenate(
                        files = fileAndTreeNames,
                        expressions = [event_no_br],
                        language = utils.uproot_lang,
                        num_workers = 10,
                    ),
                    axis = None,
                ).to_numpy()
                
                sample_nevent = len(numpy.unique(a_event_no))
            
            l_branchName = list(d_branchName_alias.keys())
            
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
                
                if (event_no_br and sample_nevent) :
                    
                    a_wVar *= float(l_sample_weight[iSample]) / sample_nevent
                
                if (varExprY is not None) :
                    
                    a_plotVarY = awkward.flatten(tree_branches[plotVarNameY], axis = None).to_numpy().astype(dtype = numpy.float64)
                    hist_plotVar.FillN(len(a_plotVarX), a_plotVarX, a_plotVarY, a_wVar)
                
                else :
                    
                    hist_plotVar.FillN(len(a_plotVarX), a_plotVarX, a_wVar)
                    
                    if (args.testW1) :
                        
                        l_varData[-1].extend(a_plotVarX)
                        l_varWeight[-1].extend(a_wVar)
                
                nJet += len(a_plotVarX)
        
        
        print("Sample: %s" %(sample))
        print("Plot: %s" %(args.plotVars[iVar]))
        print("Cut : %s" %(args.cuts[iVar]))
        #print("Weight:  %s" %(str(...))
        print(" |-- Integral: %f, Entries: %f" %(hist_plotVar.Integral(), hist_plotVar.GetEntries()))
        #print(" |-- Underflow: %f, Overflow: %f" %(hist_plotVar.GetBinContent(0), hist_plotVar.GetBinContent(hist_plotVar.GetNbinsX()+1)))
        print(f" |-- Sample xsec: {l_sample_weight[iSample]}, nEvent: {sample_nevent}")
        
        #if (args.testW1 is not None) :
        #    
        #    hist_plotVar_ref = hist_plotVar.Clone(f"{hist_plotVar.GetName()}_ref")
        #    l_hist_ref.append(hist_plotVar_ref)
        
        if (profAx is None and hist_plotVar.Integral()) :
            
            hist_plotVar.Scale(1.0 / hist_plotVar.Integral())
        
        
        ##hist_plotVar.Scale(1.0 / hist_plotVar.GetEntries())
        
        # Projection
        #l_projBin_start_end = [(1, -1)]
        #
        #if (profAx == "X") :
        #    
        #    l_projBin_start_end.extend([(_binNum, _binNum) for _binNum in range(1, hist_plotVar.GetNbinsX()+1)])
        #
        #elif (profAx == "Y") :
        #    
        #    l_projBin_start_end.extend([(_binNum, _binNum) for _binNum in range(1, hist_plotVar.GetNbinsY()+1)])
        #
        #for idx, (binStart, binEnd) in enumerate(l_projBin_start_end) :
        #    
        #    l_histGroup.append([])
        #    
        #    if (profAx == "X") :
        #        
        #        projAx = "Y"
        #        hist_plotVar_tmp = hist_plotVar.ProjectionY(f"_smp{iSample+1}_prjy{idx+1}", binStart, binEnd)
        #    
        #    elif (profAx == "Y") :
        #        
        #        projAx = "X"
        #        hist_plotVar_tmp = hist_plotVar.ProjectionX(f"_smp{iSample+1}_prjx{idx+1}", binStart, binEnd)
        #    
        #    hist_plotVar_tmp.SetLineColor(args.lineColors[iVar])
        #    hist_plotVar_tmp.SetLineStyle(args.lineStyles[iVar])
        #    hist_plotVar_tmp.SetLineWidth(args.lineWidths[iVar])
        #    hist_plotVar_tmp.SetMarkerColor(args.lineColors[iVar])
        #    hist_plotVar_tmp.SetMarkerSize(0)
        #    hist_plotVar_tmp.SetFillStyle(0)
        #    hist_plotVar_tmp.SetTitle(args.labels[iVar])
        #    l_histGroup[-1].append(hist_plotVar_tmp)
        #    #l_histGroup_outFileName.append(f"{args.outFileName.replace('.', '_bin{idx+1}.')}")
        #    fName, fExt = os.path.splitext(args.outFileName)
        #    l_histGroup_outFileName.append(f"{fName}_proj{projAx}-bin{idx+1}{fExt}")
        
        hist_plotVar_tmp = hist_plotVar
        
        # Profile
        if (profAx == "X") :
            
            hist_plotVar_tmp = hist_plotVar.ProfileX("_pfx", 1, -1, "i")
        
        elif (profAx == "Y") :
            
            hist_plotVar_tmp = hist_plotVar.ProfileY("_pfy", 1, -1, "i")
        
        hist_plotVar_tmp.SetLineColor(args.lineColors[iVar])
        hist_plotVar_tmp.SetLineStyle(args.lineStyles[iVar])
        hist_plotVar_tmp.SetLineWidth(args.lineWidths[iVar])
        hist_plotVar_tmp.SetMarkerColor(args.lineColors[iVar])
        hist_plotVar_tmp.SetMarkerSize(0)
        hist_plotVar_tmp.SetFillStyle(0)
        hist_plotVar_tmp.SetTitle(args.labels[iVar])
        l_hist.append(hist_plotVar_tmp)
        
        print("="*50)
        print("")
    
    #l_histGroup.append(l_hist)
    #l_histGroup_outFileName.append(args.outFileName)
    
    # Convert dequeue to array
    for idx in range(0, len(l_varData)) :
        
        l_varData[idx] = numpy.array(l_varData[idx])
        l_varWeight[idx] = numpy.array(l_varWeight[idx])
        
        # Normalize
        l_varWeight[idx] /= numpy.sum(l_varWeight[idx])
    
    for idx in range(0, len(l_varData)) :
        
        dist_wass_str = "NA"
        
        if (len(l_varData[args.testW1]) and len(l_varData[idx])) :
            
            dist_wass = scipy.stats.wasserstein_distance(
                u_values = l_varData[args.testW1],
                v_values = l_varData[idx],
                u_weights = l_varWeight[args.testW1],
                v_weights = l_varWeight[idx],
            )
            
            dist_wass_str = f"{dist_wass:.2e}"
        
        l_hist[idx].SetTitle(f"#splitline{{{l_hist[idx].GetTitle()}}}{{(W_{{1}} {dist_wass_str})}}")
    
    #for iHist, hist in enumerate(l_hist_ref) :
    #    
    #    #test_statistic_AD = l_hist_ref[args.testW1].AndersonDarlingTest(hist, "")
    #    test_statistic_AD = l_hist_ref[args.testW1].KolmogorovTest(hist, "M")
    #    l_hist[iHist].SetTitle(f"{l_hist[iHist].GetTitle()} (AD {test_statistic_AD:.2e})")
    
    utils.root_plot1D(
        l_hist = l_hist,
        xrange = args.xRange,
        yrange = args.yRange,
        logx = args.logX, logy = args.logY,
        #title = args.title,
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
        legendheightscale = 0.6 if (args.testW1 is None) else 1.0,
        legendtitle = args.title,
        outfile = args.outFileName,
    )
    
    #for l_hist, outFileName in zip(l_histGroup, l_histGroup_outFileName) :
    #    
    #    if (profAx == "X") :
    #        
    #        d_plotArgs = {
    #            
    #        }
    #    
    #    utils.root_plot1D(
    #        l_hist = l_hist,
    #        xrange = args.xRange,
    #        yrange = args.yRange,
    #        logx = args.logX, logy = args.logY,
    #        title = args.title,
    #        xtitle = args.xTitle, ytitle = args.yTitle,
    #        centertitlex = True, centertitley = True,
    #        centerlabelx = args.centerLabelX,
    #        gridx = True, gridy = True,
    #        ndivisionsx = args.nDivX,
    #        stackdrawopt = "nostack",
    #        histdrawopt = args.histdrawopt,
    #        legendpos = args.legendPos,
    #        legendncol = args.legendncol,
    #        legendtextsize = 0.03,
    #        legendwidthscale = 1.8,
    #        legendheightscale = 0.6,
    #        outfile = outFileName,
    #    )
    
    
    return 0


if (__name__ == "__main__") :
    
    main()
