from __future__ import print_function

import argparse
import array
import copy
import ctypes
import gc
import matplotlib
import matplotlib.pyplot
import multiprocessing
import numpy
import os
import pprint
import scipy
import scipy.interpolate
import scipy.special
import sklearn
import sklearn.metrics
#import tabulate
import time
import uproot

import CMS_lumi
import utils

import ROOT
ROOT.gROOT.SetBatch(1)

nThread = 5

ROOT.ROOT.EnableImplicitMT(nThread)
#ROOT.ROOT.EnableImplicitMT()


pprinter = pprint.PrettyPrinter(width = 500, depth = 2)


def main() :
    
    # Argument parser
    parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    
    
    parser.add_argument(
        "--config",
        help = "Configuration file",
        type = str,
        required = True,
    )
    
    
    # Parse arguments
    args = parser.parse_args()
    d_args = vars(args)
    
    
    d_config = utils.load_config(args.config)
    
    final_weight_name = "final_weight"
    classifier_name = "classifier"
    
    l_hist = []
    l_graph_ROC = []
    l_graph_sigEff = []
    l_graph_bkgEff = []
    
    l_classifiercut = [0.0, 1e-3, 1e-2, 1e-1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.97, 0.99, 0.995]
    l_classifiercut.extend([1-_val for _val in [1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 0.0]])
    
    l_classifiercut_logit = scipy.special.logit(l_classifiercut)
    
    classifier_logit_limLwr = numpy.nanmin(l_classifiercut_logit)
    classifier_logit_limUpr = numpy.nanmax(l_classifiercut_logit)
    
    if (numpy.isinf(l_classifiercut_logit[0])) :
        
        l_classifiercut_logit[0] = -1e9
        classifier_logit_limLwr = l_classifiercut_logit[1]
    
    if (numpy.isinf(l_classifiercut_logit[-1])) :
        
        l_classifiercut_logit[-1] = +1e9
        classifier_logit_limUpr = l_classifiercut_logit[-2]
    
    classifier_logit_limLwr = numpy.sign(classifier_logit_limLwr) * numpy.ceil(abs(classifier_logit_limLwr) / 10) * 10
    classifier_logit_limUpr = numpy.sign(classifier_logit_limUpr) * numpy.ceil(abs(classifier_logit_limUpr) / 10) * 10
    
    print(classifier_logit_limLwr, classifier_logit_limUpr)
    print(l_classifiercut_logit)
    
    outtag = ""
    outsuffix = ""
    
    if (
        "outtag" in d_config and
        d_config["outtag"] is not None and
        len(d_config["outtag"].strip())
    ) :
        
        outtag = d_config["outtag"].strip()
        outsuffix = "_%s" %(outtag)
    
    for iCurve, d_curve in enumerate(d_config["curves"]) :
        
        mpmanager = multiprocessing.Manager()
        
        d_rdframe = {}
        
        d_count_num = {}
        d_count_den = {}
        
        #d_rdframe = mpmanager.dict()
        #
        #d_count_num_mp = mpmanager.dict()
        #d_count_den_mp = mpmanager.dict()
        #
        #d_count_num = mpmanager.dict()
        #d_count_den = mpmanager.dict()
        
        
        for type_key in ["sig", "bkg"] :
            
            d_rdframe[type_key] = []
            
            l_tree_sample = []
            l_tree_friend = []
            
            l_sample_name   = d_config["samples"][d_curve[type_key]["sample"]]["names"]
            l_sample_weight = d_config["samples"][d_curve[type_key]["sample"]]["weights"]
            l_sample_norm   = [1] * len(l_sample_weight)
            
            weight_expr = d_curve[type_key]["weight"].format(**d_curve["vardict"])
            classifier_expr = d_curve["classifier"].format(**d_curve["vardict"])
            
            d_count_num[type_key] = numpy.zeros((len(l_sample_name), len(l_classifiercut)))
            d_count_den[type_key] = numpy.zeros((len(l_sample_name), len(l_classifiercut)))
            
            #d_count_num_mp[type_key] = mpmanager.Array("d", [0.0] * (len(l_sample_name) * len(l_classifiercut)))
            #d_count_den_mp[type_key] = mpmanager.Array("d", [0.0] * (len(l_sample_name) * len(l_classifiercut)))
            #
            ##d_count_num_mp[type_key] = multiprocessing.Array(ctypes.c_double, len(l_sample_name) * len(l_classifiercut))
            ##d_count_den_mp[type_key] = multiprocessing.Array(ctypes.c_double, len(l_sample_name) * len(l_classifiercut))
            #
            #d_count_num[type_key] = numpy.frombuffer(d_count_num_mp[type_key].get_obj()).reshape((len(l_sample_name), len(l_classifiercut)))
            #d_count_den[type_key] = numpy.frombuffer(d_count_den_mp[type_key].get_obj()).reshape((len(l_sample_name), len(l_classifiercut)))
            
            for iSample, sample_entry in enumerate(l_sample_name) :
                
                verbosetag_sample = "[sample %d/%d]" %(iSample+1, len(l_sample_name))
                
                sample, tag = sample_entry.split(":")
                sample_weight = l_sample_weight[iSample]
                
                sample_source = d_curve[type_key]["source"].format(
                    sample = sample,
                    tag = tag,
                )
                
                l_sample_file = numpy.loadtxt(sample_source, dtype = str, delimiter = "x"*100) ##[0: 1]
                l_sample_filename = [entry.split("/")[-1] for entry in l_sample_file]
                
                print("l_sample_file:\n", "\n".join(l_sample_file))
                
                tree_sample = ROOT.TChain(d_curve[type_key]["tree"])
                
                for entry in l_sample_file :
                    
                    if (tag == "latest") :
                        
                        tag = entry.split(sample)[-1].split("/")[1]
                    
                    print("%s adding file: %s" %(verbosetag_sample, entry))
                    tree_sample.Add(entry)
                
                l_tree_friend.append([])
                
                for iFriend, d_friend in enumerate(d_curve["friends"]) :
                    
                    verbosetag_friend = "[friend %d/%d]" %(iFriend+1, len(d_curve["friends"]))
                    
                    sample_fr = sample
                    tag_fr = d_friend["tag"] if (d_friend["tag"] is not None) else tag
                    
                    if ("usefriendlist" in d_friend and d_friend["usefriendlist"] is not None) :
                        
                        for fr in d_config["friendlist"][d_friend["usefriendlist"]] :
                            
                            if sample in fr :
                                
                                sample_fr, tag_fr = fr.split(":")
                                break
                    
                    l_sample_friend = [
                        "{dir}/{sample}_{tag}/{entry}".format(
                            dir = d_friend["dir"],
                            sample = sample_fr,
                            tag = tag_fr,
                            entry = entry,
                        ) for entry in l_sample_filename
                    ]
                    
                    print("l_sample_friend:\n", "\n".join(l_sample_friend))
                    
                    tree_friend = ROOT.TChain(d_friend["tree"])
                    
                    for entry in l_sample_friend :
                        
                        print("%s %s adding file: %s" %(verbosetag_sample, verbosetag_friend, entry))
                        tree_friend.Add(entry)
                    
                    # Need to keep a reference to the tree chain
                    l_tree_friend[-1].append(tree_friend)
                    
                    tree_sample.AddFriend(tree_friend)
                
                # Need to keep a reference to the tree chain
                l_tree_sample.append(tree_sample)
                
                
                rdframe_sample = ROOT.RDataFrame(tree_sample)
                
                weight_expr_sample = weight_expr
                l_sample_norm[iSample] = float(sample_weight)/tree_sample.GetEntries()
                
                rdframe_sample = rdframe_sample.Define(final_weight_name, weight_expr_sample)
                rdframe_sample = rdframe_sample.Define(classifier_name, classifier_expr)
                
                d_rdframe[type_key].append(rdframe_sample)
            
            
            #for iSample, rdframe in enumerate(d_rdframe[type_key]) :
            #    
            #    print("")
            #    print(l_sample_name[iSample])
            #    
            #    weight = l_sample_norm[iSample]
            #    
            #    count = rdframe.Sum(final_weight_name).GetValue()
            #    weighted_count = count * weight
            #    
            #    classifiercut_expr = "(%s) * (%s)" %(final_weight_name, d_curve["classifiercut"])
            #    
            #    d_count_den[type_key][iSample:] = weighted_count
            #    
            #    for iCut, cutval in enumerate(l_classifiercut) :
            #        
            #        classifiercut_expr_mod = classifiercut_expr.format(
            #            classifier = classifier_name,
            #            value = cutval,
            #        )
            #        
            #        rdframe_mod = rdframe.Define("classifier_cut", classifiercut_expr_mod)
            #        
            #        count = rdframe_mod.Sum("classifier_cut").GetValue()
            #        weighted_count = count * weight
            #        
            #        d_count_num[type_key][iSample, iCut] = weighted_count
            #        
            #        eff = d_count_num[type_key][iSample, iCut] / d_count_den[type_key][iSample, iCut] if (d_count_den[type_key][iSample, iCut]) else 0
            #        
            #        print("[%s: %s] cut %0.8f, num %0.6e, den %0.6e, eff %0.4e" %(type_key, d_curve[type_key]["sample"], cutval, d_count_num[type_key][iSample, iCut], d_count_den[type_key][iSample, iCut], eff))
            
            global eval_counts
            
            def eval_counts(iSample, iCut, evalDen):
                
                #print("eval_counts", iSample, iCut, evalDen)
                
                log_str = []
                #log_str.append(l_sample_name[iSample])
                
                rdframe = d_rdframe[type_key][iSample]
                
                weight = l_sample_norm[iSample]
                
                count_den = None
                weighted_count_den = None
                
                if (evalDen) :
                    
                    count_den = rdframe.Sum(final_weight_name).GetValue()
                    weighted_count_den = count_den * weight
                
                #d_count_den[type_key][iSample:] = weighted_count_den
                
                classifiercut_expr = "(%s) * (%s)" %(final_weight_name, d_curve["classifiercut"])
                
                cutval = l_classifiercut[iCut]
                
                classifiercut_expr_mod = classifiercut_expr.format(
                    classifier = classifier_name,
                    value = cutval,
                    **d_curve["vardict"],
                )
                #print(classifiercut_expr_mod)
                
                rdframe_mod = rdframe.Define("classifier_cut", classifiercut_expr_mod)
                
                count_num = rdframe_mod.Sum("classifier_cut").GetValue()
                weighted_count_num = count_num * weight
                
                #d_count_num[type_key][iSample, iCut] = weighted_count_num
                
                #eff = d_count_num[type_key][iSample, iCut] / d_count_den[type_key][iSample, iCut] if (d_count_den[type_key][iSample, iCut]) else 0
                eff = weighted_count_num / weighted_count_den if (weighted_count_den) else 0
                
                #log_str.append("[%s: %s] cut %0.8f, num %0.6e, den %0.6e, eff %0.4e" %(type_key, d_curve[type_key]["sample"], cutval, d_count_num[type_key][iSample, iCut], d_count_den[type_key][iSample, iCut], eff))
                log_str.append(
                    "[%s: %s] "
                    "cut %0.8f (logit %0.4f), "
                    "num %0.6e (count %0.4f), "
                    "den %0.6e (count %0.4f), "
                    "eff %0.6e, "
                    "" %(
                    type_key, d_curve[type_key]["sample"],
                    cutval, scipy.special.logit(cutval),
                    weighted_count_num, count_num,
                    weighted_count_den if (weighted_count_den) else 0, count_den if (count_den) else 0,
                    eff
                ))
                
                print("\n".join(log_str))
                
                #return 0
                
                return (iSample, iCut, weighted_count_num, weighted_count_den)
            
            
            ncpu_use = int(multiprocessing.cpu_count() * d_config["cpufrac"] / nThread)
            #ncpu_use = int(multiprocessing.cpu_count() * d_config["cpufrac"])
            
            ncpu_use = max(1, ncpu_use)
            
            pool = multiprocessing.Pool(processes = ncpu_use, maxtasksperchild = 1)
            l_job = []
            
            for iSample, rdframe in enumerate(d_rdframe[type_key]) :
                
                for iCut, cutval in enumerate(l_classifiercut) :
                    
                    print("Submiting job: iSample %d, iCut %d" %(iSample, iCut))
                    
                    l_job.append(pool.apply_async(
                        eval_counts,
                        (),
                        dict(
                            iSample = iSample,
                            iCut = iCut,
                            evalDen = not iCut,
                        ),
                    ))
            
            pool.close()
            
            #utils.wait_for_asyncpool(l_job)
            
            l_isJobDone = [False] * len(l_job)
            
            while(False in l_isJobDone) :
                
                for iJob, job in enumerate(l_job) :
                    
                    if (job is None) :
                        
                        continue
                    
                    if (not l_isJobDone[iJob] and job.ready()) :
                        
                        l_isJobDone[iJob] = True
                        
                        retVal = job.get()
                        iSample, iCut, weighted_count_num, weighted_count_den = retVal
                        
                        d_count_num[type_key][iSample, iCut] = weighted_count_num
                        
                        if (weighted_count_den is not None) :
                            
                            d_count_den[type_key][iSample:] = weighted_count_den
                        
                        l_job[iJob] = None
                        
                        if (not sum(l_isJobDone) % 10) :
                            
                            gc.collect()
            
            gc.collect()
            
            pool.join()
        
        
        print("")
        print("Final:")
        
        
        a_eff_sig = numpy.zeros(len(l_classifiercut))
        a_eff_bkg = numpy.zeros(len(l_classifiercut))
        
        for iCut, cutval in enumerate(l_classifiercut) :
            
            num_sig = numpy.sum(d_count_num["sig"][:, iCut])
            den_sig = numpy.sum(d_count_den["sig"][:, iCut])
            eff_sig = num_sig/den_sig if (den_sig) else 0
            a_eff_sig[iCut] = eff_sig
            
            num_bkg = numpy.sum(d_count_num["bkg"][:, iCut])
            den_bkg = numpy.sum(d_count_den["bkg"][:, iCut])
            eff_bkg = num_bkg/den_bkg if (den_bkg) else 0
            a_eff_bkg[iCut] = eff_bkg
            
            
            print("cut %0.8f (logit %0.4f), eff_sig %0.4e, eff_bkg %0.4e" %(cutval, l_classifiercut_logit[iCut], eff_sig, eff_bkg))
        
        
        #a_eff_sig = array.array("f", numpy.linspace(0.1, 1, 1000))
        #a_eff_bkg = array.array("f", numpy.linspace(0.1, 1, 1000))
        
        auc = sklearn.metrics.auc(a_eff_bkg, a_eff_sig)
        
        gr_ROC = ROOT.TGraph(len(a_eff_sig), a_eff_sig, a_eff_bkg)
        gr_ROC.SetName("gr_ROC_%d" %(iCurve+1))
        #h1_ROC = utils.root_TGraph_to_TH1(graph = gr_ROC, setError = False)
        
        #gr_sigEff = ROOT.TGraph(len(l_classifiercut), numpy.array(l_classifiercut), a_eff_sig)
        gr_sigEff = ROOT.TGraph(len(l_classifiercut_logit), numpy.array(l_classifiercut_logit), a_eff_sig)
        gr_sigEff.SetName("gr_sigEff_%d" %(iCurve+1))
        
        #gr_bkgEff = ROOT.TGraph(len(l_classifiercut), numpy.array(l_classifiercut), a_eff_bkg)
        gr_bkgEff = ROOT.TGraph(len(l_classifiercut_logit), numpy.array(l_classifiercut_logit), a_eff_bkg)
        gr_bkgEff.SetName("gr_bkgEff_%d" %(iCurve+1))
        
        gr_ROC.GetXaxis().SetRangeUser(d_config["xrange"][0], d_config["xrange"][1])
        
        #gr_sigEff.GetXaxis().SetRangeUser(0.0, 1.0)
        #gr_bkgEff.GetXaxis().SetRangeUser(0.0, 1.0)
        
        gr_sigEff.GetXaxis().SetRangeUser(classifier_logit_limLwr, classifier_logit_limUpr)
        gr_bkgEff.GetXaxis().SetRangeUser(classifier_logit_limLwr, classifier_logit_limUpr)
        
        for gr in [gr_ROC, gr_sigEff, gr_bkgEff] :
            
            gr.SetLineColor(d_curve["color"])
            gr.SetLineStyle(d_curve["linestyle"])
            gr.SetLineWidth(3)
            gr.SetMarkerSize(0)
            gr.SetFillStyle(0)
            gr.SetTitle(d_curve["label"])
        
        gr_ROC.SetTitle("%s [AUC=%0.4f]" %(gr_ROC.GetTitle(), auc))
        
        #h1_ROC.GetXaxis().SetRangeUser(d_config["xrange"][0], d_config["xrange"][1])
        #h1_ROC.SetLineColor(d_curve["color"])
        #h1_ROC.SetLineStyle(d_curve["linestyle"])
        #h1_ROC.SetLineWidth(3)
        #h1_ROC.SetMarkerSize(0)
        #h1_ROC.SetFillStyle(0)
        
        #print(h1_ROC.GetEntries())
        #print(h1_ROC.GetNbinsX())
        
        #l_hist.append(h1_ROC)
        l_graph_ROC.append(gr_ROC)
        
        l_graph_sigEff.append(gr_sigEff)
        l_graph_bkgEff.append(gr_bkgEff)
    
    
    #outdir = "."
    #
    #if ("/" in d_config["outfile"]) :
    #    
    #    outdir = d_config["outfile"]
    #    outdir = outdir[0: outdir.rfind("/")]
    #    
    #    os.system("mkdir -p %s" %(outdir))
    
    outdir = d_config["outdir"].strip()
    
    
    h1_xRange = ROOT.TH1F("h1_xRange", "h1_xRange", 1, d_config["xrange"][0], d_config["xrange"][1])
    
    utils.root_plot1D(
        l_hist = [],
        l_graph = l_graph_ROC,
        canvassize = (800, 600),
        #outfile = d_config["outfile"],
        outfile = "%s/%s/ROC%s.pdf" %(outdir, outtag, outsuffix),
        xrange = d_config["xrange"],
        yrange = d_config["yrange"],
        logx = d_config["logx"],
        logy = d_config["logy"],
        xtitle = d_config["xtitle"],
        ytitle = d_config["ytitle"],
        gridx = d_config["gridx"],
        gridy = d_config["gridy"],
        #ndivisionsx = [5, 5, 0],
        ndivisionsx = None,
        legendpos = d_config["legendpos"],
        #legendncol = 1,
        legendtextsize = d_config["legendtextsize"],
        legendheightscale = 1.0, legendwidthscale = 1.0,
    )
    
    
    utils.root_plot1D(
        l_hist = [],
        l_graph = l_graph_sigEff,
        canvassize = (800, 600),
        outfile = "%s/%s/sigEff_vs_classifierCut%s.pdf" %(outdir, outtag, outsuffix),
        #xrange = (min(l_classifiercut), max(l_classifiercut)),
        #xrange = (0.0, 1.0),
        xrange = (classifier_logit_limLwr, classifier_logit_limUpr),
        yrange = d_config["xrange"],
        logx = False, logy = d_config["logx"],
        xtitle = "Classifier cut [logit]",
        ytitle = d_config["xtitle"],
        gridx = d_config["gridx"],
        gridy = d_config["gridy"],
        #ndivisionsx = [5, 5, 0],
        ndivisionsx = None,
        #legendpos = d_config["legendpos"],
        legendpos = "LL",
        #legendncol = 1,
        legendtextsize = d_config["legendtextsize"],
        legendheightscale = 1.0, legendwidthscale = 1.0,
    )
    
    utils.root_plot1D(
        l_hist = [],
        l_graph = l_graph_bkgEff,
        canvassize = (800, 600),
        outfile = "%s/%s/bkgEff_vs_classifierCut%s.pdf" %(outdir, outtag, outsuffix),
        #xrange = (min(l_classifiercut), max(l_classifiercut)),
        #xrange = (0.0, 1.0),
        xrange = (classifier_logit_limLwr, classifier_logit_limUpr),
        yrange = d_config["yrange"],
        logx = False, logy = d_config["logy"],
        xtitle = "Classifier cut [logit]",
        ytitle = d_config["ytitle"],
        gridx = d_config["gridx"], gridy = d_config["gridy"],
        #ndivisionsx = [5, 5, 0],
        ndivisionsx = None,
        #legendpos = d_config["legendpos"],
        legendpos = "LL",
        #legendncol = 1,
        legendtextsize = d_config["legendtextsize"],
        legendheightscale = 1.0, legendwidthscale = 1.0,
    )
    


if (__name__ == "__main__") :
    
    main()
