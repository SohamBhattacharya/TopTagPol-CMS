from __future__ import print_function

import argparse
import gc
import glob
import multiprocessing
import numpy
import pprint

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
    
    l_hist = []
    l_graph = []
    l_graph_ROC = []
    l_graph_sigEff = []
    l_graph_bkgEff = []
    
    outtag = ""
    outsuffix = ""
    
    if (
        "outtag" in d_config and
        d_config["outtag"] is not None and
        len(d_config["outtag"].strip())
    ) :
        
        outtag = d_config["outtag"].strip()
        outsuffix = "_%s" %(outtag)
    
    a_bin = eval(d_config["bins"])
    
    for iCurve, d_curve in enumerate(d_config["curves"]) :
        
        d_rdframe = {}
        d_h1_plot = {}
        
        for type_key in ["num", "den"] :
            
            d_h1_plot[type_key] = None
            
            d_rdframe[type_key] = []
            
            l_tree_sample = []
            l_tree_friend = []
            
            l_sample_name   = d_config["samples"][d_curve[type_key]["sample"]]["names"]
            l_sample_weight = d_config["samples"][d_curve[type_key]["sample"]]["weights"]
            l_sample_norm   = [1.0] * len(l_sample_weight)
            
            weight_expr = d_curve[type_key]["weight"].format(**d_curve["vardict"])
            plot_expr = d_curve[type_key]["plot"].format(**d_curve["vardict"])
            
            print(f"[{type_key}] plot_expr: {plot_expr}", )
            print(f"[{type_key}] weight_expr: {weight_expr}")
            
            for iSample, sample_entry in enumerate(l_sample_name) :
                
                verbosetag_sample = "[sample %d/%d]" %(iSample+1, len(l_sample_name))
                
                sample, tag = sample_entry.split(":")
                sample_weight = l_sample_weight[iSample]
                
                sample_source = d_curve[type_key]["source"].format(
                    sample = sample,
                    tag = tag,
                )
                
                l_sample_file = []
                
                if (sample_source.endswith(".txt")) :
                    
                    l_sample_file = numpy.loadtxt(sample_source, dtype = str, delimiter = "x"*100)
                
                elif (sample_source.endswith(".root")) :
                    
                    l_sample_file = glob.glob(sample_source)
                
                l_sample_file = utils.natural_sort(l_sample_file)
                
                l_sample_filename = [entry.split("/")[-1] for entry in l_sample_file]
                
                print(f"l_sample_file [{sample_source}]:\n", "\n".join(l_sample_file))
                
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
                    
                    if ("usefriendlist" in d_friend) :
                        
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
                
                if ("event_no_br" in d_curve) :
                    
                    event_no_br = d_curve["event_no_br"]
                    a_event_no = rdframe_sample.Take["long long"](event_no_br).GetValue()
                    nevent = len(numpy.unique(a_event_no))
                    l_sample_norm[iSample] = float(sample_weight)/nevent
                    
                else :
                    
                    l_sample_norm[iSample] = float(sample_weight)/tree_sample.GetEntries()
                
                d_rdframe[type_key].append(rdframe_sample)
            
            
            global eval_hist
            
            def eval_hist(iSample):
                
                #print("eval_counts", iSample, iCut, evalDen)
                
                #log_str = []
                ##log_str.append(l_sample_name[iSample])
                #
                #rdframe = d_rdframe[type_key][iSample]
                #
                #plot_expr = d_curve[type_key]["plot"]
                #
                #plot_expr_mod = plot_expr.format(
                #    **d_curve["vardict"],
                #)
                #
                #
                #print(weight_expr)
                #print(plot_expr_mod)
                ##rdframe_mod = rdframe.Filter(f"{final_weight_name} > 0").Define("plot_expr", plot_expr_mod)
                #rdframe_mod = rdframe.Define("plot_expr", plot_expr_mod)
                #
                #h1_temp_name = f"h1_temp_{type_key}_sample{iSample}"
                ##h1_temp = ROOT.TH1F(h1_temp_name, h1_temp_name, len(a_bin)-1, a_bin)
                #
                ##draw_expr = f"({plot_expr_mod}) >> {h1_temp_name}"
                #
                ##count = rdframe_mod.Sum("plot_expr").GetValue()
                ##print(count)
                #
                #h1_temp = rdframe_mod.Histo1D(
                #    (h1_temp_name, h1_temp_name, len(a_bin)-1, a_bin),
                #    "plot_expr"
                #).GetPtr()
                #
                #print(h1_temp)
                #
                ##h1_temp.Scale(l_sample_norm[iSample])
                #
                #return h1_temp
                #
                ##return 0
                
                h1_temp_name = f"h1_curve{iCurve}_{type_key}_sample{iSample}"
                h1_temp = ROOT.TH1F(h1_temp_name, h1_temp_name, len(a_bin)-1, a_bin)
                #h1_temp.SetDirectory(0)
                h1_temp.Sumw2()
                #print(a_bin)
                
                draw_expr = f"({plot_expr}) >> {h1_temp_name}"
                #print(draw_expr)
                #print(weight_expr)
                
                l_tree_sample[iSample].Draw(draw_expr, weight_expr)
                
                h1_temp.Scale(l_sample_norm[iSample])
                #print(h1_temp, l_sample_norm[iSample], h1_temp.Integral(), h1_temp.GetEntries())
                
                return h1_temp
            
            
            ncpu_use = int(multiprocessing.cpu_count() * d_config["cpufrac"] / nThread)
            #ncpu_use = int(multiprocessing.cpu_count() * d_config["cpufrac"])
            
            ncpu_use = max(1, ncpu_use)
            
            pool = multiprocessing.Pool(processes = ncpu_use, maxtasksperchild = 1)
            l_job = []
            
            for iSample, rdframe in enumerate(d_rdframe[type_key]) :
                
                print("Submiting job: type %s, iSample %d" %(type_key, iSample))
                
                l_job.append(pool.apply_async(
                    eval_hist,
                    (),
                    dict(
                        iSample = iSample,
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
                        
                        h1_jobResult = job.get()
                        print(h1_jobResult)
                        print(h1_jobResult.Integral())
                        
                        if (d_h1_plot[type_key] is None) :
                            
                            d_h1_plot[type_key] = h1_jobResult.Clone(f"h1_curve{iCurve}_{type_key}_sum")
                        
                        else :
                            
                            d_h1_plot[type_key].Add(h1_jobResult)
            
            gc.collect()
            
            pool.join()
            
            #for iSample, sample_entry in enumerate(l_sample_name) :
            #    
            #    h1_temp_name = f"h1_temp_{type_key}_sample{iSample}"
            #    h1_temp = ROOT.TH1F(h1_temp_name, h1_temp_name, len(a_bin)-1, a_bin)
            #    #h1_temp = ROOT.TH1F(h1_temp_name, h1_temp_name, 100, 0, 5000)
            #    #h1_temp.SetDirectory(0)
            #    h1_temp.Sumw2()
            #    print(a_bin)
            #    
            #    draw_expr = f"({plot_expr}) >> {h1_temp_name}"
            #    print(draw_expr)
            #    print(weight_expr)
            #    
            #    l_tree_sample[iSample].Draw(draw_expr, weight_expr)
            #    
            #    h1_temp.Scale(l_sample_norm[iSample])
            #    print(h1_temp, l_sample_norm[iSample], h1_temp.Integral(), h1_temp.GetEntries())
            #    
            #    if (d_h1_plot[type_key] is None) :
            #        
            #        d_h1_plot[type_key] = h1_temp.Clone()
            #    
            #    else :
            #        
            #        d_h1_plot[type_key].Add(h1_temp)
        
        
        h1_ratio = d_h1_plot["num"].Clone(f"h1_curve{iCurve}_ratio")
        h1_ratio.Divide(d_h1_plot["den"])
        
        #for iBin in range(d_h1_plot["num"].GetNbinsX()) :
        #    
        #    num = d_h1_plot["num"].GetBinContent(iBin+1)
        #    den = d_h1_plot["den"].GetBinContent(iBin+1)
        #    
        #    if (num > den) :
        #        
        #        print(f"bin{iBin+1}: num ({num}) > den ({den})")
        #        
        #        if (not den) :
        #            
        #            d_h1_plot["num"].SetBinContent(iBin+1, 0.0)
        #            d_h1_plot["num"].SetBinError(iBin+1, 0.0)
        #
        #h1_ratio = ROOT.TEfficiency(d_h1_plot["num"], d_h1_plot["den"]).CreateGraph()
        #h1_ratio.SetName(f"h1_curve{iCurve}_ratio")
        
        #h1_ratio.GetXaxis().SetRangeUser(*d_config["xrange"])
        ##h1_ratio.SetMaximum(1.0)
        #
        #h1_ratio.SetLineColor(d_curve["color"])
        #h1_ratio.SetLineStyle(d_curve["linestyle"])
        #h1_ratio.SetLineWidth(3)
        #h1_ratio.SetMarkerColor(d_curve["color"])
        #h1_ratio.SetMarkerSize(0)
        #h1_ratio.SetFillStyle(0)
        #h1_ratio.SetTitle(d_curve["label"])
        #print(h1_ratio.GetTitle())
        #
        #l_hist.append(h1_ratio)
        
        
        gr_ratio = ROOT.TGraphAsymmErrors(d_h1_plot["num"], d_h1_plot["den"], "pois")
        gr_ratio.SetLineColor(d_curve["color"])
        gr_ratio.SetLineStyle(d_curve["linestyle"])
        gr_ratio.SetLineWidth(3)
        gr_ratio.SetMarkerColor(d_curve["color"])
        gr_ratio.SetMarkerSize(0)
        gr_ratio.SetFillStyle(0)
        gr_ratio.SetTitle(d_curve["label"])
        gr_ratio.GetXaxis().SetRangeUser(*d_config["xrange"])
        
        # Error bars should not exceed 1
        for iPoint in range(gr_ratio.GetN()) :
            
            val = gr_ratio.GetPointY(iPoint)
            err = gr_ratio.GetErrorYhigh(iPoint)
            
            if (err+val > 1) :
                
                err = 1 - val
                err = gr_ratio.SetPointEYhigh(iPoint, err)
        
        l_graph.append(gr_ratio)
        

    
    outdir = d_config["outdir"].strip()
    
    
    #h1_xRange = ROOT.TH1F("h1_xRange", "h1_xRange", 1, d_config["xrange"][0], d_config["xrange"][1])
    
    outname_base = "efficiency"
    
    if (d_config["outname"] and len(d_config["outname"])) :
        
        outname_base = d_config["outname"]
    
    utils.root_plot1D(
        #l_hist = l_hist,
        l_hist = [],
        l_graph = l_graph,
        canvassize = (800, 600),
        #outfile = d_config["outfile"],
        outfile = "%s/%s/%s%s.pdf" %(outdir, outtag, outname_base, outsuffix),
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
        legendncol = d_config["legendncol"],
        legendtextsize = d_config["legendtextsize"],
        legendheightscale = 1.0,
        legendwidthscale = 2.0 if (d_config["legendncol"] > 1) else 1.0,
        histdrawopt = "hist E1",
        graphdrawopt = "E1",
    )
    
    


if (__name__ == "__main__") :
    
    main()
