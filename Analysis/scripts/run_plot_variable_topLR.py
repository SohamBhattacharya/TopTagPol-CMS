#!/usr/bin/env python

import argparse
import os
import multiprocessing

def cleanSpaces(string) :

    while ("  " in string) :

        string = string.replace("  ", " ")

    return string


def main() :
    
    # Argument parser
    parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument(
        "--era",
        help = "Era",
        type = str,
        required = True,
        choices = ["2017", "2018"],
    )
    
    parser.add_argument(
        "--training",
        help = "Training name (for e.g. YYYY-MM-DD_hh-mm-ss_particlenet)",
        type = str,
        required = True,
    )
    
    parser.add_argument(
        "--state",
        help = "Model state name",
        type = str,
        required = False,
        default = "result_best_epoch_state",
    )
    
    parser.add_argument(
        "--ntuple",
        help = "Ntuple name (for e.g. DeepNtuplesAK8-v4)",
        type = str,
        required = True,
    )
    
    # Parse arguments
    args = parser.parse_args()
    d_args = vars(args)
    
    jetName = "fj"
    outDir = f"plots/variables/{args.training}/{args.state}/{args.ntuple}/{args.era}/{jetName}"
    
    d_type = {
        "lep": {
            "cut_topL": "(label_TopL_bele | label_TopL_bmu)",
            "cut_topR": "(label_TopR_bele | label_TopR_bmu)",
            "cut_others": "(label_TopL_bele | label_TopL_bmu | label_TopR_bele | label_TopR_bmu)",
            "vars": {
                #"score_lepTop_LvsR": {
                #    "xtitle": "t^{lep}_{L} vs. t^{lep}_{R} classifier",
                #    "expr": "(score_label_TopR_bele+score_label_TopR_bmu) / ((score_label_TopL_bele+score_label_TopL_bmu) + (score_label_TopR_bele+score_label_TopR_bmu))",
                #},
                "score_lepTop_LvsR_vs_genpt": {
                    "xtitle": "p_{T}(t_{gen})",
                    "expr": "fj_gen_pt : (score_label_TopR_bele+score_label_TopR_bmu) / ((score_label_TopL_bele+score_label_TopL_bmu) + (score_label_TopR_bele+score_label_TopR_bmu)) : Y",
                },
            },
        },
        
        "had": {
            "cut_topL": "(label_TopL_bcq | label_TopL_bqq | label_TopL_bc | label_TopL_bq)",
            "cut_topR": "(label_TopR_bcq | label_TopR_bqq | label_TopR_bc | label_TopR_bq)",
            "cut_others": "(label_TopL_bcq | label_TopL_bqq | label_TopL_bc | label_TopL_bq | label_TopR_bcq | label_TopR_bqq | label_TopR_bc | label_TopR_bq)",
            "vars": {
                #"score_hadTop_LvsR": {
                #    "xtitle": "t^{had}_{L} vs. t^{had}_{R} classifier",
                #    "expr": "(score_label_TopR_bcq+score_label_TopR_bqq+score_label_TopR_bc+score_label_TopR_bq) / ((score_label_TopL_bcq+score_label_TopL_bqq+score_label_TopL_bc+score_label_TopL_bq) + (score_label_TopR_bcq+score_label_TopR_bqq+score_label_TopR_bc+score_label_TopR_bq))",
                #},
                "score_hadTop_LvsR_vs_genpt": {
                    "xtitle": "t^{had}_{L} vs. t^{had}_{R} classifier",
                    "expr": "fj_gen_pt : (score_label_TopR_bcq+score_label_TopR_bqq+score_label_TopR_bc+score_label_TopR_bq) / ((score_label_TopL_bcq+score_label_TopL_bqq+score_label_TopL_bc+score_label_TopL_bq) + (score_label_TopR_bcq+score_label_TopR_bqq+score_label_TopR_bc+score_label_TopR_bq)) : Y",
                },
            },
        }
    }
    
    commonCut = (
        f"({jetName}_pt > 400) & "
        f"(abs({jetName}_eta) < 2.5)"
    )
    
    commonCut_topL = (
        f"({jetName}_pt > 400) & "
        f"(abs({jetName}_eta) < 2.5)"
    )
    
    commonCut_topR = (
        f"({jetName}_pt > 400) & "
        f"(abs({jetName}_eta) < 2.5)"
    )
    
    niceness = 10
    nCPU = max(1, int(multiprocessing.cpu_count()*0.33))
    pool = multiprocessing.Pool(processes = nCPU, initializer = os.nice, initargs = (niceness,))
    l_job = []
    l_jobName = []
    l_jobCmd = []
    
    for iType, jetType in enumerate(d_type.keys()) :
        
        for iVar, (varName, varInfo) in enumerate(d_type[jetType]['vars'].items()) :
            
            cut_topL = f"({commonCut_topL}) & ({d_type[jetType]['cut_topL']})"
            cut_topR = f"({commonCut_topR}) & ({d_type[jetType]['cut_topR']})"
            cut_others = f"({commonCut}) & ({d_type[jetType]['cut_others']})"
            
            command = f"""
                python -u python/plot_variable.py \
                --fileAndTreeNames \
                    /nfs/dust/cms/user/sobhatta/work/TopTagPol/weaver-core/output/{args.training}/prediction/{args.state}/{args.ntuple}/Wprimetotb_M3000W30_LH/*.root:Events \
                    /nfs/dust/cms/user/sobhatta/work/TopTagPol/weaver-core/output/{args.training}/prediction/{args.state}/{args.ntuple}/Wprimetotb_M6000W60_LH/*.root:Events \
                    /nfs/dust/cms/user/sobhatta/work/TopTagPol/weaver-core/output/{args.training}/prediction/{args.state}/{args.ntuple}/Wprimetotb_M3000W30_RH/*.root:Events \
                    /nfs/dust/cms/user/sobhatta/work/TopTagPol/weaver-core/output/{args.training}/prediction/{args.state}/{args.ntuple}/Wprimetotb_M6000W60_RH/*.root:Events \
                    /nfs/dust/cms/user/sobhatta/work/TopTagPol/weaver-core/output/{args.training}/prediction/{args.state}/{args.ntuple}/TTJets_HT-*_TuneCP5_13TeV-madgraphMLM-pythia8/*.root:Events \
                    /nfs/dust/cms/user/sobhatta/work/TopTagPol/weaver-core/output/{args.training}/prediction/{args.state}/{args.ntuple}/ST_t-channel_*_5f_InclusiveDecays_TuneCP5_13TeV-powheg-pythia8/*.root:Events \
                --fileFraction 1.0 \
                --plotVars \
                    "{varInfo['expr']}" \
                    "{varInfo['expr']}" \
                    "{varInfo['expr']}" \
                    "{varInfo['expr']}" \
                    "{varInfo['expr']}" \
                    "{varInfo['expr']}" \
                --cuts \
                    "{cut_topL}" \
                    "{cut_topL}" \
                    "{cut_topR}" \
                    "{cut_topR}" \
                    "{cut_others}" \
                    "{cut_others}" \
                --labels \
                    "t^{{{jetType}}}_{{L}} (W'_{{3 TeV}})" \
                    "t^{{{jetType}}}_{{L}} (W'_{{6 TeV}})" \
                    "t^{{{jetType}}}_{{R}} (W'_{{3 TeV}})" \
                    "t^{{{jetType}}}_{{R}} (W'_{{6 TeV}})" \
                    "t^{{{jetType}}} (t#bar{{t}})" \
                    "t^{{{jetType}}} (single t)" \
                --lineColors \
                    4 \
                    4 \
                    6 \
                    6 \
                    1 \
                    2 \
                --lineStyles \
                    1 \
                    7 \
                    1 \
                    7 \
                    1 \
                    1 \
                --plotBinX 50 0.0 1.0 \
                --plotBinY 50 0 10000 \
                --xRange 0 3000 \
                --yRange 0 1 \
                --nDivX 5 5 0 \
                --xTitle "{varInfo['xtitle']}" \
                --yTitle "arbitrary unit" \
                --histdrawopt "hist E" \
                --legendPos UL \
                --legendncol 2 \
                --outFileName "{outDir}/{varName}.pdf" \
            """
            
            cmdStr = cleanSpaces(command)
            job = pool.apply_async(os.system, (), dict(command = cmdStr))
            l_job.append(job)
            l_jobCmd.append(cmdStr)
            l_jobName.append(varName)
    
    
    
    # Close the pool and wait for jobs to complete
    pool.close()
    pool.join()
    
    print("\n\n")
    
    for iJob, job in enumerate(l_job) :
    
        retVal = job.get()
    
        if (retVal) :
        
            print(f"Failed job: {l_jobName[iJob]}")
    
    
    return 0


if (__name__ == "__main__") :
    
    main()