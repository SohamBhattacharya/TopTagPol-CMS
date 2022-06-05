import argparse
import awkward
import gc
import matplotlib
import matplotlib.colors
import matplotlib.pyplot
import mplhep
import multiprocessing
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
    parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument(
        "--config",
        help = "Configuration yaml file or the yaml content as string",
        type = str,
        required = True,
    )
    
    # Parse arguments
    args = parser.parse_args()
    d_args = vars(args)
    
    d_config = utils.load_config(args.config)
    
    a_binsX = numpy.array(eval(d_config["binsX"]))
    a_binsY = numpy.array(eval(d_config["binsY"]))
    
    plotX_expr = d_config["plotX"].format(**d_config["vardict"])
    plotY_expr = d_config["plotY"].format(**d_config["vardict"])
    weight_expr = d_config["wVar"].format(**d_config["vardict"])
    
    d_sample = utils.load_sampleFilesAndTrees(d_config, d_config)
    
    l_tree_sample = d_sample["l_tree_sample"]
    l_tree_friend = d_sample["l_tree_friend"]
    l_sample_norm = d_sample["l_sample_norm"]
    
    global eval_hist
    
    def eval_hist(iSample):
        
        h2_temp_name = f"h2_sample{iSample}"
        h2_temp = ROOT.TH2F(h2_temp_name, h2_temp_name, len(a_binsX)-1, a_binsX, len(a_binsY)-1, a_binsY)
        h2_temp.Sumw2()
        
        draw_expr = f"({plotY_expr}) : ({plotX_expr}) >> {h2_temp_name}"
        
        l_tree_sample[iSample].Draw(draw_expr, weight_expr)
        
        h2_temp.Scale(l_sample_norm[iSample])
        
        return h2_temp
    
    
    ncpu_use = int(multiprocessing.cpu_count() * d_config["cpufrac"])
    ncpu_use = max(1, ncpu_use)
    
    pool = multiprocessing.Pool(processes = ncpu_use, maxtasksperchild = 1)
    l_job = []
    
    for iSample in range(0, len(l_tree_sample)) :
        
        print("Submiting job: iSample %d" %(iSample))
        
        l_job.append(pool.apply_async(
            eval_hist,
            (),
            dict(
                iSample = iSample,
            ),
        ))
    
    pool.close()
    
    h2_result = None
    l_isJobDone = [False] * len(l_job)
    
    while(False in l_isJobDone) :
        
        for iJob, job in enumerate(l_job) :
            
            if (job is None) :
                
                continue
            
            if (not l_isJobDone[iJob] and job.ready()) :
                
                l_isJobDone[iJob] = True
                
                h2_jobResult = job.get()
                print(h2_jobResult)
                print(h2_jobResult.Integral())
                
                if (h2_result is None) :
                    
                    h2_result = h2_jobResult.Clone("h2_result")
                
                else :
                    
                    h2_result.Add(h2_jobResult)
    
    gc.collect()
    pool.join()
    
    if (h2_result.Integral()) :
        
        h2_result.Scale(1.0 / h2_result.Integral())
    
    
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
    
    h2_result.GetXaxis().SetRangeUser(*d_config["xRange"])
    h2_result.GetXaxis().SetTitle(d_config["xTitle"])
    h2_result.GetXaxis().SetTitleSize(0.05)
    h2_result.GetXaxis().SetTitleOffset(1.1)
    h2_result.GetXaxis().CenterTitle(True)
    h2_result.GetXaxis().SetLabelSize(0.045)
    if (d_config["nDivX"] is not None) : h2_result.GetXaxis().SetNdivisions(*d_config["nDivX"], True)
    
    h2_result.GetYaxis().SetRangeUser(*d_config["yRange"])
    h2_result.GetYaxis().SetTitle(d_config["yTitle"])
    h2_result.GetYaxis().SetTitleSize(0.05)
    h2_result.GetYaxis().SetTitleOffset(1.1)
    h2_result.GetYaxis().CenterTitle(True)
    h2_result.GetYaxis().SetLabelSize(0.045)
    if (d_config["nDivY"] is not None) : h2_result.GetYaxis().SetNdivisions(*d_config["nDivY"], True)
    
    h2_result.GetZaxis().SetTitle(d_config["zTitle"])
    h2_result.GetZaxis().SetTitleSize(0.05)
    h2_result.GetZaxis().SetTitleOffset(1.55)
    h2_result.GetZaxis().CenterTitle(True)
    h2_result.GetZaxis().SetLabelSize(0.045)
    
    h2_result.SetMinimum(d_config["zRange"][0])
    h2_result.SetMaximum(d_config["zRange"][1])
    
    utils.cpalette_nipy_spectral.set()
    
    h2_result.Draw("colz")
    
    latex = ROOT.TLatex()
    #latex.SetTextFont(62)
    latex.SetTextSize(0.035)
    latex.SetTextAlign(13)
    
    latex.DrawLatex(d_config["titlePos"][0], d_config["titlePos"][1], d_config["title"])
    
    canvas.SetLogz(d_config["logZ"])
    
    CMS_lumi.CMS_lumi(pad = canvas, iPeriod = 0, iPosX = 0, CMSextraText = "Simulation Preliminary", lumiText = "(13 TeV)")
    
    
    if ("/" in d_config["outFileName"]) :
        
        outDir = d_config["outFileName"][: d_config["outFileName"].rfind("/")]
        os.system("mkdir -p %s" %(outDir))
    
    canvas.SaveAs(d_config["outFileName"])
    canvas.SaveAs(d_config["outFileName"].replace(".pdf", ".png"))
    
    
    return 0


if (__name__ == "__main__") :
    
    main()
