import argparse
import matplotlib
import matplotlib.colors
import matplotlib.pyplot
import mplhep
import numpy
import os
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
        help = "Syntanx: fileName1:treeName1 fileName2:treeName2 ...",
        type = str,
        nargs = "*",
        required = True,
    )
    
    parser.add_argument(
        "--cut",
        help = "Cut (jet level, like pT, eta, etc.)",
        type = str,
        required = True,
    )
    
    parser.add_argument(
        "--constiCut",
        help = "Cut (constituent level, like pdgid). E.g. \"abs(jet_selectedPatJetsAK15PFPuppi_consti_id_reco) == 11\"",
        type = str,
        required = False,
        default = None,
    )
    
    parser.add_argument(
        "--nJetMax",
        help = "Maximum number of jets to plot",
        type = int,
        required = False,
        default = 100000,
    )
    
    parser.add_argument(
        "--xVar",
        help = "x variable branch name",
        type = str,
        required = True,
    )
    
    parser.add_argument(
        "--yVar",
        help = "y variable branch name",
        type = str,
        required = True,
    )
    
    parser.add_argument(
        "--wVar",
        help = "weight (z) variable branch name",
        type = str,
        required = True,
    )
    
    parser.add_argument(
        "--resolverOperation",
        help = "How to update the bin (pixel) value if another constituent is found in the same bin. E.g. (any python expression) \"{new}+{old}\", \"{new} if ({newResolver} > {oldResolver}) else {old}\", etc.",
        type = str,
        required = True,
    )
    
    parser.add_argument(
        "--resolverVar",
        help = "Variable (branch name) to use to resolve the conflict if another constituent is found in the same bin (can be the constituent pT, for example).",
        type = str,
        required = False,
        default = None,
    )
    
    parser.add_argument(
        "--resolverUpdate",
        help = "How to update the resolver variable. E.g. (any python expression) \"max({newResolver}, {oldResolver})\"",
        type = str,
        required = False,
        default = None,
    )
    
    parser.add_argument(
        "--xRange",
        help = "x-axis range (the histogram will have int(max-min) bins in this range): min max",
        type = float,
        nargs = 2,
        required = True,
    )
    
    parser.add_argument(
        "--yRange",
        help = "y-axis range (the histogram will have int(max-min) bins in this range): min max",
        type = float,
        nargs = 2,
        required = True,
    )
    
    parser.add_argument(
        "--zRange",
        help = "z-axis range: min max",
        type = float,
        nargs = 2,
        required = True,
    )
    
    parser.add_argument(
        "--logZ",
        help = "Z-axis in log scale",
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
        "--zTitle",
        help = "Z-axis title",
        type = str,
        required = False,
        default = "Z",
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
        "--outFileName",
        help = "Output file name",
        type = str,
        required = True,
    )
    
    
    # Parse arguments
    args = parser.parse_args()
    d_args = vars(args)
    
    
    xVarName = "xVar"
    yVarName = "yVar"
    wVarName = "wVar"
    resolverVarName = "resolverVar"
    constiCutVarName = "constiCutVar"
    
    d_branchName_alias = {
        xVarName: args.xVar,
        yVarName: args.yVar,
        wVarName: args.wVar,
    }
    
    if (args.resolverVar is not None) :
        
        d_branchName_alias[resolverVarName] = args.resolverVar
    
    if (args.constiCut is not None) :
        
        d_branchName_alias[constiCutVarName] = args.constiCut
    
    h2_jetImg = ROOT.TH2F("h2_jetImg", "", int(args.xRange[1]-args.xRange[0]), args.xRange[0], args.xRange[1], int(args.yRange[1]-args.yRange[0]), args.yRange[0], args.yRange[1])
    
    nJet_selected = 0
    breakFromLoop = False
    
    l_branchName = list(d_branchName_alias.keys())
    
    fileAndTreeNames = utils.get_fileAndTreeNames(args.fileAndTreeNames)
    
    for iFile, fileAndTreeName in enumerate(fileAndTreeNames) :
        
        for tree_branches in uproot.iterate(
            files = fileAndTreeName,
            expressions = l_branchName,
            aliases = d_branchName_alias,
            cut = args.cut,
            language = utils.uproot_lang,
            step_size = 100000,
        ) :
            
            nEvent = len(tree_branches[l_branchName[0]])
            #nEvent = 1000
            
            print(h2_jetImg.GetEntries())
            
            for iEvent in range(0, nEvent) :
                
                nJet = len(tree_branches[l_branchName[0]][iEvent])
                
                for iJet in range(0, nJet) :
                    
                    nJet_selected += 1
                    
                    a_x = tree_branches[xVarName][iEvent][iJet].to_numpy().astype(dtype = numpy.uint32)
                    a_y = tree_branches[yVarName][iEvent][iJet].to_numpy().astype(dtype = numpy.uint32)
                    a_w = tree_branches[wVarName][iEvent][iJet].to_numpy()
                    
                    jet_nConsti = len(a_x)
                    
                    a_resolver = tree_branches[resolverVarName][iEvent][iJet].to_numpy() if (args.resolverVar is not None) else None
                    a_constiCut = tree_branches[constiCutVarName][iEvent][iJet].to_numpy() if (args.constiCut is not None) else numpy.ones(jet_nConsti, dtype = bool)
                    
                    a_constiIdx = numpy.column_stack((
                        a_y,
                        a_x,
                    ))
                    
                    d_arrayIdx = sortedcontainers.SortedDict()
                    d_arrayResolver = sortedcontainers.SortedDict()
                    
                    for iConsti in range(0, jet_nConsti) :
                        
                        # CHeck against 0.5 to avoid precision issues
                        if (a_constiCut[iConsti] < 0.5) :
                            
                            continue
                        
                        key = tuple(a_constiIdx[iConsti])
                        val = a_w[iConsti]
                        
                        resolver = a_resolver[iConsti] if (args.resolverVar is not None) else None
                        
                        if (key in d_arrayIdx) :
                            
                            if (args.resolverVar is not None) :
                                
                                resolver = eval(args.resolverUpdate.format(
                                    oldResolver = d_arrayResolver[key],
                                    newResolver = resolver,
                                ))
                            
                            val = eval(args.resolverOperation.format(
                                oldResolver = d_arrayResolver[key],
                                newResolver = resolver,
                                old = d_arrayIdx[key],
                                new = val,
                            ))
                        
                        
                        d_arrayIdx[key] = val
                        d_arrayResolver[key] = resolver
                    
                    
                    rr = numpy.array([ele[0] for ele in d_arrayIdx.keys()], dtype = float)
                    cc = numpy.array([ele[1] for ele in d_arrayIdx.keys()], dtype = float)
                    ww = numpy.array(d_arrayIdx.values(), dtype = float)
                    
                    if (len(rr)) :
                        
                        h2_jetImg.FillN(len(rr), cc, rr, ww)
                    
                    
                    if (args.nJetMax > 0 and nJet_selected >= args.nJetMax) :
                        
                        breakFromLoop = True
                        break
                
                if (iEvent == 0 or iEvent == nEvent-1 or not (iEvent+1)%1000) :
                    
                    print("Processed event %d/%d of file %d/%d: selected %d jets." %(iEvent+1, nEvent, iFile+1, len(fileAndTreeNames), nJet_selected))
                
                if (breakFromLoop) : break
            
            if (breakFromLoop) : break
        
        if (breakFromLoop) : break
    
    h2_jetImg.Scale(1.0/nJet_selected)
    
    
    #ROOT.gStyle.SetOptStat(0)
    
    ROOT.gROOT.LoadMacro("utils/tdrstyle.C")
    ROOT.gROOT.ProcessLine("setTDRStyle()")
    
    ROOT.gROOT.SetStyle("tdrStyle")
    ROOT.gROOT.ForceStyle(True)
    
    canvas = ROOT.TCanvas("canvas", "canvas", 1000, 875)
    canvas.UseCurrentStyle()
    
    canvas.SetLeftMargin(0.13)
    canvas.SetRightMargin(0.225)
    canvas.SetTopMargin(0.08)
    canvas.SetBottomMargin(0.13)
    
    h2_jetImg.GetXaxis().SetTitle(args.xTitle)
    h2_jetImg.GetXaxis().SetTitleSize(0.06)
    h2_jetImg.GetXaxis().SetTitleOffset(0.9)
    h2_jetImg.GetXaxis().CenterTitle(True)
    h2_jetImg.GetXaxis().SetLabelSize(0.05)
    if (args.nDivX is not None) : h2_jetImg.GetXaxis().SetNdivisions(*args.nDivX, True)
    
    h2_jetImg.GetYaxis().SetTitle(args.yTitle)
    h2_jetImg.GetYaxis().SetTitleSize(0.06)
    h2_jetImg.GetYaxis().SetTitleOffset(0.9)
    h2_jetImg.GetYaxis().CenterTitle(True)
    h2_jetImg.GetYaxis().SetLabelSize(0.05)
    if (args.nDivY is not None) : h2_jetImg.GetYaxis().SetNdivisions(*args.nDivY, True)
    
    h2_jetImg.GetZaxis().SetTitle(args.zTitle)
    h2_jetImg.GetZaxis().SetTitleSize(0.05)
    h2_jetImg.GetZaxis().SetTitleOffset(1.55)
    h2_jetImg.GetZaxis().CenterTitle(True)
    h2_jetImg.GetZaxis().SetLabelSize(0.05)
    
    h2_jetImg.SetMinimum(args.zRange[0])
    h2_jetImg.SetMaximum(args.zRange[1])
    
    
    utils.cpalette_nipy_spectral.set()
    
    h2_jetImg.Draw("colz")
    
    
    latex = ROOT.TLatex()
    #latex.SetTextFont(62)
    latex.SetTextSize(0.04)
    latex.SetTextAlign(13)
    
    latex.DrawLatex(args.titlePos[0], args.titlePos[1], args.title)
    
    
    canvas.SetLogz(args.logZ)
    
    CMS_lumi.CMS_lumi(pad = canvas, iPeriod = 0, iPosX = 0, CMSextraText = "Simulation Preliminary", lumiText = "(13 TeV)")
    
    
    if ("/" in args.outFileName) :
        
        outDir = args.outFileName[: args.outFileName.rfind("/")]
        os.system("mkdir -p %s" %(outDir))
    
    canvas.SaveAs(args.outFileName)
    
    
    return 0



if (__name__ == "__main__") :
    
    main()
