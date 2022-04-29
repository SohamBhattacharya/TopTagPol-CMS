from __future__ import print_function

import argparse
import array
import copy
import getpass
#import matplotlib
#matplotlib.use("Agg")
#import matplotlib.pyplot
#import mxnet
import multiprocessing
import numpy
import os
import pprint
import scipy
import scipy.interpolate
import scipy.special
import tabulate
import time

import Common
import mxnet_train_info

import ROOT

ROOT.gROOT.SetBatch(1)


pprinter = pprint.PrettyPrinter(width = 500, depth = 2)


def main() :
    
    # Argument parser
    parser = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter)
    
    
    parser.add_argument(
        "--sigSamples",
        help = "List of signal samples (sample1.txt:tree1 sample2.txt:tree2 ...)",
        type = str,
        nargs = "*",
        required = True,
    )
    
    parser.add_argument(
        "--bkgSamples",
        help = "List of background files (sample1.txt:tree1 sample2.txt:tree2 ...)",
        type = str,
        nargs = "*",
        required = True,
    )
    
    parser.add_argument(
        "--classifierDirs",
        help = "List of classifier ntuple directories (will look for the same sig/bkg samples and add them as friend trees)",
        type = str,
        nargs = "*",
        required = False,
    )
    
    parser.add_argument(
        "--nEventMaxs",
        help = "Number of signal and background (each) events to be used",
        type = int,
        nargs = "*",
        required = True,
    )
    
    parser.add_argument(
        "--varsROC",
        help = "List of variables to be used for evaluating the ROC (for TMVA: provide name of TMVA xml file)",
        type = str,
        nargs = "*",
        required = True,
    )
    
    parser.add_argument(
        "--cutsSig",
        help = "List of selections on signal",
        type = str,
        nargs = "*",
        required = False,
    )
    
    parser.add_argument(
        "--cutsBkg",
        help = "List of selections on background",
        type = str,
        nargs = "*",
        required = False,
    )
    
    parser.add_argument(
        "--comparisons",
        help = "List of comparisons to use for the variable cut (>, <)",
        type = str,
        nargs = "*",
        required = True,
        choices = [">", "<"],
    )
    
    parser.add_argument(
        "--omitAUC",
        help = "Do not print the AUC in the labels",
        default = False,
        action = "store_true",
    )
    
    parser.add_argument(
        "--xTitle",
        help = "X-axis title",
        type = str,
        required = False,
        default = "Signal efficiency",
    )
    
    parser.add_argument(
        "--yTitle",
        help = "Y-axis title",
        type = str,
        required = False,
        default = "Background efficiency",
    )
    
    parser.add_argument(
        "--yMin",
        help = "Y-axis minumum",
        type = float,
        required = False,
        default = 1e-5,
    )
    
    parser.add_argument(
        "--yMax",
        help = "Y-axis maximum",
        type = float,
        required = False,
        default = 1.0,
    )
    
    parser.add_argument(
        "--logY",
        help = "Y-axis in log scale",
        default = False,
        action = "store_true",
    )
    
    parser.add_argument(
        "--moreLogGridsY",
        help = "Draw finer Y-axis log grid",
        default = False,
        action = "store_true",
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
        required = True,
    )
    
    parser.add_argument(
        "--labels",
        help = "Plot labels",
        type = str,
        nargs = "*",
        required = True,
    )
    
    parser.add_argument(
        "--legendPos",
        help = "Plot labels",
        type = str,
        required = False,
        default = "UR",
        choices = ["UR", "LR", "LL", "UL"],
    )
    
    parser.add_argument(
        "--legendTextSize",
        help = "Legent text size",
        type = float,
        required = False,
        default = 0.03,
    )
    
    parser.add_argument(
        "--legendHeightScale",
        help = "Scale legend height",
        type = float,
        required = False,
        default = 1.0,
    )
    
    parser.add_argument(
        "--title",
        help = "Plot title",
        type = str,
        required = False,
        default = "",
    )
    
    parser.add_argument(
        "--detailROC",
        help = "ROC variable detail",
        type = str,
        required = False,
        default = "",
    )
    
    parser.add_argument(
        "--detailSig",
        help = "Training detail for signal",
        type = str,
        required = False,
        default = "",
    )
    
    parser.add_argument(
        "--detailBkg",
        help = "Training detail for background",
        type = str,
        required = False,
        default = "",
    )
    
    parser.add_argument(
        "--detailPos",
        help = "Position of the detail (LL coordinate)",
        type = float,
        nargs = 2,
        required = False,
        default = [0, 0],
    )
    
    parser.add_argument(
        "--outFileName",
        help = "Output file name (\"ROC_\" will be appended to this)",
        type = str,
        required = True,
    )
    
    
    # Parse arguments
    args = parser.parse_args()
    d_args = vars(args)
    
    
    outFileName_ROC = "plots/ROC/ROC_%s" %(args.outFileName)
    outFileName_config = "plots/ROC/ROC_%s_config.txt" %(args.outFileName)
    
    
    os.system("mkdir -p %s" %(outFileName_ROC[:outFileName_ROC.rfind("/")]))
    
    
    # Save the configuration
    
    print("Saving the configuration to: %s" %(outFileName_config))
    
    with open(outFileName_config, "w") as configOutFile :
        
        configOutFile.write(pprint.pformat(d_args, width = 1))
        configOutFile.write("\n")
    
    print("\n")
    
    
    def getEfficiency(arr, val, comparison, norm = 1.0) :
        
        if (comparison == ">") :
            
            eff = float(sum(arr > val)) / norm
        
        elif (comparison == "<") :
            
            eff = float(sum(arr < val)) / norm
        
        else :
            
            print("Error in getEfficiency(...): Invalid comparison \"%s\"" %(comparison))
        
        return eff
    
    
    l_histDetail_ROC = []
    
    for iPlot in range(0, len(args.sigFiles)) :
        
        l_inFileName_sig = mxnet_train_info.d_ntupleFile[args.sigFiles[iPlot]]
        l_inFileName_bkg = mxnet_train_info.d_ntupleFile[args.bkgFiles[iPlot]]
        
        tree_sig = ROOT.TChain("tree")
        tree_bkg = ROOT.TChain("tree")
        
        for iFile in range(0, len(l_inFileName_sig)) :
            
            tree_sig.Add(l_inFileName_sig[iFile])
        
        for iFile in range(0, len(l_inFileName_bkg)) :
            
            tree_bkg.Add(l_inFileName_bkg[iFile])
        
        l_extraTree_sig = []
        l_extraTree_bkg = []
        
        if (len(args.extraDirSuffixes[iPlot])) :
            
            extraDirSuffixes = args.extraDirSuffixes[iPlot].split(":")
            
            for iExtra, extraDirSuffix in enumerate(extraDirSuffixes) :
                
                if (not len(extraDirSuffix)) :
                    
                    continue
                
                # Sig
                tree_extra_sig = ROOT.TChain("tree")
                
                for iFile, iFileName in enumerate(l_inFileName_sig) :
                    
                    iFileName_extra = "%s_%s%s" %(
                        iFileName[0: iFileName.rfind("/")],
                        extraDirSuffix,
                        iFileName[iFileName.rfind("/"):],
                    )
                    
                    #l_inFileName_extra.extend([iFileName_extra])
                    
                    #print("Adding file: %s" %(iFileName_extra))
                    tree_extra_sig.Add(iFileName_extra)
                
                l_extraTree_sig.append(tree_extra_sig)
                
                tree_sig.AddFriend(tree_extra_sig)
                
                
                # Bkg
                tree_extra_bkg = ROOT.TChain("tree")
                
                for iFile, iFileName in enumerate(l_inFileName_bkg) :
                    
                    iFileName_extra = "%s_%s%s" %(
                        iFileName[0: iFileName.rfind("/")],
                        extraDirSuffix,
                        iFileName[iFileName.rfind("/"):],
                    )
                    
                    #l_inFileName_extra.extend([iFileName_extra])
                    
                    #print("Adding file: %s" %(iFileName_extra))
                    tree_extra_bkg.Add(iFileName_extra)
                
                l_extraTree_bkg.append(tree_extra_bkg)
                
                tree_bkg.AddFriend(tree_extra_bkg)
        
        nEvent_tree_sig = tree_sig.GetEntries()
        nEvent_tree_bkg = tree_bkg.GetEntries()
        
        l_cutVar = []
        #    "hepTop_pT_reco",
        #    "hepTop_genHadTop_deltaR_reco",
        #    "hepTop_isMayBeTop_reco",
        #]
        
        
        a_var_sig = None
        a_var_bkg = None
        
        
        if (".xml" in args.varsROC[iPlot]) :
            
            a_var_sig = Common.evaluateTMVAandGetDiscr(
                xmlFileName = args.varsROC[iPlot],
                tree = tree_sig,
                cutStr = args.cutsSig[iPlot],
                nSel_max = args.nEventMaxs[iPlot],
            )
            
            
            a_var_bkg = Common.evaluateTMVAandGetDiscr(
                xmlFileName = args.varsROC[iPlot],
                tree = tree_bkg,
                cutStr = args.cutsBkg[iPlot],
                nSel_max = args.nEventMaxs[iPlot],
            )
        
        else :
            
            a_var_sig = Common.getArrayFromTBranch(
                tree = tree_sig,
                varName = args.varsROC[iPlot],
                l_cutVar = l_cutVar,
                cutStr = args.cutsSig[iPlot],
                nSel_max = args.nEventMaxs[iPlot],
            )
            
            
            a_var_bkg = Common.getArrayFromTBranch(
                tree = tree_bkg,
                varName = args.varsROC[iPlot],
                l_cutVar = l_cutVar,
                cutStr = args.cutsBkg[iPlot],
                nSel_max = args.nEventMaxs[iPlot],
            )
        
        
        discMin = min(min(a_var_sig), min(a_var_bkg))
        #print(discMin)
        discMax = max(max(a_var_sig), max(a_var_bkg))
        #print(discMax)
        disc_nSample = 1000
        disc_stepSize = float(discMax-discMin) / disc_nSample
        disc_stepSize_small = disc_stepSize / 500.0
        
        l_discr = numpy.arange(discMin, discMax, disc_stepSize)
        
        #if (l_discr[-1] < discMax - disc_stepSize_small) :
        #    
        #    l_discr = numpy.append(
        #        l_discr,
        #        [discMax]
        #    )
        
        # If the lowest signal efficiency is too large, add a very small increment(s) near discMax
        if (float(sum(a_var_sig > l_discr[-1]))/a_var_sig.shape[0] > 0.05 and (discMax-l_discr[-1] > disc_stepSize_small)) :
            
            l_discr = numpy.append(
                l_discr,
                numpy.arange(l_discr[-1], discMax, disc_stepSize_small)
            )
        
        elif (float(sum(a_var_sig > l_discr[-2]))/a_var_sig.shape[0] > 0.05) :
            
            l_discr = numpy.insert(
                l_discr,
                -1,
                numpy.arange(l_discr[-2], l_discr[-1], disc_stepSize_small)
            )
        
        l_eff_sig = numpy.zeros(len(l_discr)+2)
        l_eff_bkg = numpy.zeros(len(l_discr)+2)
        
        # The first/last point will be (1, 1)/(0, 0)
        # So include these
        #l_eff_sig = [1.0]
        #l_eff_bkg = [1.0]
        l_eff_sig[0] = 1.0
        l_eff_bkg[0] = 1.0
        
        
        nCPU = min(multiprocessing.cpu_count(), len(l_eff_sig))
        
        pool = multiprocessing.Pool(processes = nCPU)
        
        l_job_sig = []
        l_job_bkg = []
        
        nEventTot_sig = a_var_sig.shape[0]
        nEventTot_bkg = a_var_bkg.shape[0]
        
        print("\n")
        print("Calculating signal and background efficiencies. \n")
        
        
        for iDiscr, discVal in enumerate(l_discr) :
            
            #nEventTot_sig = a_var_sig.shape[0]
            #nEventTot_bkg = a_var_bkg.shape[0]
            #
            #nEventSel_sig = float(sum(a_var_sig > discVal))
            #nEventSel_bkg = float(sum(a_var_bkg > discVal))
            #
            #eff_sig = nEventSel_sig / nEventTot_sig
            #eff_bkg = nEventSel_bkg / nEventTot_bkg
            #
            ## Background rejection efficiency
            ##eff_bkg = 1 - eff_bkg
            #eff_bkg = eff_bkg
            #
            #print(
            #    "%d/%d: %0.8f: "
            #    "eff_sig %0.8f, "
            #    "eff_bkg %0.8f, "
            #    "\n" %(
            #    
            #    iDiscr+1, len(l_discr),
            #    discVal,
            #    eff_sig,
            #    eff_bkg
            #))
            #
            #l_eff_sig.append(eff_sig)
            #l_eff_bkg.append(eff_bkg)
            
            
            job = pool.apply_async(
                getEfficiency,
                (),
                dict(
                    arr = a_var_sig,
                    val = discVal,
                    norm = nEventTot_sig,
                    comparison = args.comparisons[iPlot],
                ),
            )
            
            l_job_sig.append(job)
            
            
            job = pool.apply_async(
                getEfficiency,
                (),
                dict(
                    arr = a_var_bkg,
                    val = discVal,
                    norm = nEventTot_bkg,
                    comparison = args.comparisons[iPlot],
                ),
            )
            
            l_job_bkg.append(job)
        
        
        pool.close()
        pool.join()
        
        
        for iJob in range(0, len(l_job_sig)) :
            
            l_eff_sig[iJob+1] = l_job_sig[iJob].get()
            l_eff_bkg[iJob+1] = l_job_bkg[iJob].get()
            
            
            if (iJob == 0 or iJob == len(l_job_sig)-1 or not (iJob+1)%20) :
            
                print(
                    "%d/%d: %0.8f: "
                    "eff_sig %0.8f, "
                    "eff_bkg %0.8f, "
                    "\n" %(
                    
                    iJob+1, len(l_discr),
                    l_discr[iJob],
                    l_eff_sig[iJob+1],
                    l_eff_bkg[iJob+1]
                ))
        
        
        
        ## The last point will be (0, 0)
        ## So include this
        #l_eff_sig.extend([0.0])
        #l_eff_bkg.extend([0.0])
        
        #print(list(zip(l_eff_sig, l_eff_bkg)))
        
        
        # Get the unique x-values (i.e. the signal efficiency)
        # Required for the interpolation
        l_uniqueIndex = numpy.unique(l_eff_sig, return_index = True)[1]
        
        l_eff_sig_unique = numpy.array(l_eff_sig)[l_uniqueIndex]
        l_eff_bkg_unique = numpy.array(l_eff_bkg)[l_uniqueIndex]
        
        #l_significance_unique = numpy.array(l_significance)[l_uniqueIndex]
        
        #print(list(zip(l_eff_sig_unique, l_eff_bkg_unique)))
        
        # Add the x=0 point by hand if not already there
        if (0 not in l_eff_sig_unique) :
            
            l_eff_sig_unique = numpy.append(l_eff_sig_unique, 0.0)
            #l_eff_bkg_unique = numpy.append(l_eff_bkg_unique, max(l_eff_bkg_unique))
            l_eff_bkg_unique = numpy.append(l_eff_bkg_unique, 0.0)
            
            #l_significance_unique = numpy.append(l_significance_unique, 0.0)
        
        # Sort by the x-axis values (i.e. the signal efficiency)
        # Required for the interpolation
        l_sortedIndex = numpy.argsort(l_eff_sig_unique)
        
        l_eff_sig_unique = l_eff_sig_unique[l_sortedIndex]
        l_eff_bkg_unique = l_eff_bkg_unique[l_sortedIndex]
        
        #l_significance_unique = l_significance_unique[l_sortedIndex]
        
        #fInter_ROC = scipy.interpolate.InterpolatedUnivariateSpline(l_eff_sig_unique, l_eff_bkg_unique, bbox = [0, 1], ext = "zeros")
        fInter_ROC = scipy.interpolate.InterpolatedUnivariateSpline(l_eff_sig_unique, l_eff_bkg_unique, bbox = [0, 1], k = 1, ext = "zeros")
        print([fInter_ROC(ele) for ele in numpy.arange(0, 1, 0.0999)])
        
        areaROC = fInter_ROC.integral(0, 1)
        print("Area under ROC: %0.4f" %(areaROC))
        
        
        #print(len(l_discr), len(l_significance))
        ##fInter_signi_vs_disc = scipy.interpolate.InterpolatedUnivariateSpline(l_discr, l_significance, bbox = [0, 1], k = 1, ext = "zeros")
        #fInter_signi_vs_sigEff = scipy.interpolate.InterpolatedUnivariateSpline(l_eff_sig_unique, l_significance_unique, bbox = [0, 1], k = 1, ext = "zeros")
        
        
        colorAxis1 = "r"
        colorAxis2 = "b"
        
        
        #################### Plot ROC ####################
        
        #AUC_str = "#scale[1.65]{AUC=%0.2g}" %(areaROC)
        AUC_str = ("[AUC=%0.2g]" %(areaROC)) * (not args.omitAUC)
        
        a_x = array.array("f", numpy.linspace(0, 1, 1000))
        a_y = array.array("f", [fInter_ROC(ele) for ele in a_x])
        
        #print(list(zip(a_x, a_y)))
        
        gr_ROC = ROOT.TGraph(len(a_x), a_x, a_y)
        #gr_ROC = ROOT.TGraph(len(l_eff_sig_unique), array.array("f", l_eff_sig_unique), array.array("f", l_eff_bkg_unique))
        gr_ROC.SetName("graph_%d" %(iPlot+1))
        h1_ROC = Common.TGraphToTH1(graph = gr_ROC, setError = False)
        
        h1_ROC.GetXaxis().SetRangeUser(0.0, 1.0)
        h1_ROC.SetMinimum(args.yMin)
        h1_ROC.SetMaximum(args.yMax)
        
        histDetail_ROC = Common.HistogramDetails()
        histDetail_ROC.hist = h1_ROC.Clone()
        histDetail_ROC.drawOption = "L"
        histDetail_ROC.lineColor = args.lineColors[iPlot]
        histDetail_ROC.lineStyle = args.lineStyles[iPlot]
        histDetail_ROC.lineWidth = 3
        histDetail_ROC.markerSize = 0
        histDetail_ROC.fillStyle = 0
        histDetail_ROC.histLabel = "%s %s" %(args.labels[iPlot], AUC_str)
        histDetail_ROC.histTitle = args.title
        
        l_histDetail_ROC.append(histDetail_ROC)
        
        
        detailStr = "#splitline{%s}{%s}" %(args.detailSig, args.detailBkg)
        detailStr = "#splitline{%s}{%s}" %(AUC_str, detailStr)
        detailStr = "#splitline{#scale[1.75]{%s}}{%s}" %(args.detailROC, detailStr)
        
        
        print("\n")
    
    
    Common.plot1D(
        list_histDetails = l_histDetail_ROC,
        stackDrawOption = "nostack",
        title = args.title,
        titleSizeScale = 0.9,
        xTitle = args.xTitle,
        yTitle = args.yTitle,
        xTitleSizeScale = 0.75,
        yTitleSizeScale = 0.75,
        xTitleOffsetScale = 1.4,
        yTitleOffsetScale = 1.35,
        xMin = 0.0, xMax = 1.0,
        yMin = args.yMin, yMax = args.yMax,
        logX = False, logY = args.logY,
        gridX = True, gridY = True,
        nDivisionsX = [5, 2, 5],
        nDivisionsY = [5, 2, 5],
        moreLogGridsY = args.moreLogGridsY,
        #xTitleSizeScale = 1.0, yTitleSizeScale = 1.0,
        #xTitleOffset = 1.0, yTitleOffset = 1.0,
        #xLabelSizeScale = 1.0, yLabelSizeScale = 1.0,
        #centerLabelsX = True, centerLabelsY = True,
        drawLegend = True,
        #legendDrawOption = "",
        #legendNcol = 1,
        #legendWidthScale = 1,
        legendHeightScale = args.legendHeightScale,
        transparentLegend = True,
        legendTextSize = args.legendTextSize,
        legendBorderSize = 0,
        legendPos = args.legendPos,
        legendTitle = "",
        #l_extraText = [[args.detailPos[0], args.detailPos[1], detailStr]], #[[x, y, text], ...]
        outFileName = outFileName_ROC.replace(".pdf", ""),
        outFileName_suffix = "",
    )
    
    
    return 0


if (__name__ == "__main__") :
    
    main()
