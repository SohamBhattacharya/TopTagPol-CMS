#!/usr/bin/env python

import argparse
import itertools
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
    
    #parser.add_argument(
    #"--sampleYaml",
    #    help = "YAML file with same dictionary (names, cross sections)",
    #    type = str,
    #    required = True,
    #)
    
    # Parse arguments
    args = parser.parse_args()
    d_args = vars(args)
    
    sampleYaml = f"common/ntupleDicts/ntupleDict_dnntuples_{args.era}.yml"

    #with open(sampleYml, "r") as fopen :
    #    
    #    d_sample = yaml.load(fopen.read(), Loader = yaml.FullLoader)
    
    jetName = "fj"
    outDir = f"plots/variables/{args.training}/{args.state}/{args.ntuple}/{args.era}/{jetName}"
    #outDir = f"plots/variables/{args.training}/{args.state}/{args.ntuple}/{args.era}/{jetName}_recopt-gt-400"
    
    #cthstd_symb = "cos#theta*#kern[-0.75]{{}_{d}}"
    
    d_type = {
        "lep": {
            "cut_topL": "(label_TopL_bele | label_TopL_bmu)",
            "cut_topR": "(label_TopR_bele | label_TopR_bmu)",
            "cut_others": "(label_TopL_bele | label_TopL_bmu | label_TopR_bele | label_TopR_bmu)",
            "vars": {
                
                #"lepTop_genpt": {
                #    "xtitle": "p_{T}(t^{gen}) [GeV]",
                #    "ytitle": "arbitrary unit",
                #    "plotBinX": "50 0 10000",
                #    "plotBinY": "0 0 0",
                #    "xRange": "0 3000",
                #    "yRange": "0 1.5",
                #    "expr": "fj_gen_pt",
                #},
                #
                #"lepTop_jet-pt": {
                #    "xtitle": "p_{T}(jet) [GeV]",
                #    "ytitle": "arbitrary unit",
                #    "plotBinX": "50 0 10000",
                #    "plotBinY": "0 0 0",
                #    "xRange": "0 3000",
                #    "yRange": "0 1.5",
                #    "expr": "fj_pt",
                #},
                #
                #"lepTop_jet-pt_by_genpt": {
                #    "xtitle": "p_{T}(jet) / p_{T}(t^{gen})",
                #    "ytitle": "arbitrary unit",
                #    "plotBinX": "200 0 10",
                #    "plotBinY": "0 0 0",
                #    "xRange": "0 5",
                #    "yRange": "0 2e-1",
                #    "expr": "fj_pt / fj_gen_pt",
                #},
                #
                "lepTop_gen_cosThetaStar": {
                    "xtitle": "cos#theta*^{, gen}",
                    "ytitle": "arbitrary unit",
                    "plotBinX": "25 0.0 1.0",
                    "plotBinY": "0 0 0",
                    "xRange": "0 1",
                    "yRange": "0 0.2",
                    "expr": "((1.0+fj_gen_cosThetaStar)/2.0)",
                    "exprBins": {
                        "genpt": {
                            "expr": "fj_gen_pt",
                            "label": "p_{T}(t^{gen})",
                            "bins": [
                                (0, 100000),
                                (0, 200),
                                (200, 400),
                                (400, 600),
                                (600, 800),
                                (800, 1000),
                                (1000, 1200),
                                (1200, 1600),
                                (1600, 2000),
                                (2000, 3000),
                                (3000, 5000),
                            ]
                        }
                    }
                },
                
                #"lepTop_gen_cosThetaStar_vs_genpt": {
                #    "xtitle": "p_{T}(t^{gen}) [GeV]",
                #    "ytitle": "#LTcos#theta*^{, gen}#GT",
                #    "plotBinX": "25 0.0 1.0",
                #    "plotBinY": "0 0 0 0 200 400 600 800 1000 1200 1600 2000 3000 5000 10000",
                #    "xRange": "0 3000",
                #    "yRange": "0 1.5",
                #    "expr": "fj_gen_pt : ((1.0+fj_gen_cosThetaStar)/2.0) : Y",
                #},
                
                "lepTop_gen_zl": {
                    "xtitle": "z^{gen}_{l}",
                    "ytitle": "arbitrary unit",
                    "plotBinX": "25 0.0 1.0",
                    "plotBinY": "0 0 0",
                    "xRange": "0 1",
                    "yRange": "0 0.3",
                    "expr": "fj_gen_zl",
                    "exprBins": {
                        "genpt": {
                            "expr": "fj_gen_pt",
                            "label": "p_{T}(t^{gen})",
                            "bins": [
                                (0, 100000),
                                (0, 200),
                                (200, 400),
                                (400, 600),
                                (600, 800),
                                (800, 1000),
                                (1000, 1200),
                                (1200, 1600),
                                (1600, 2000),
                                (2000, 3000),
                                (3000, 5000),
                            ]
                        }
                    }
                },
                
                #"lepTop_gen_zl_vs_genpt": {
                #    "xtitle": "p_{T}(t^{gen}) [GeV]",
                #    "ytitle": "#LTz^{gen}_{l}#GT",
                #    "plotBinX": "25 0.0 1.0",
                #    "plotBinY": "0 0 0 0 200 400 600 800 1000 1200 1600 2000 3000 5000 10000",
                #    "xRange": "0 3000",
                #    "yRange": "0 1.5",
                #    "expr": "fj_gen_pt : fj_gen_zl : Y",
                #},
                
                "lepTop_classifier_LvsR": {
                    "xtitle": "c^{lep}_{LvR}",
                    "ytitle": "arbitrary unit",
                    "plotBinX": "25 0.0 1.0",
                    "plotBinY": "0 0 0",
                    "xRange": "0 1",
                    "yRange": "0 0.3",
                    "expr": "(score_label_TopR_bele+score_label_TopR_bmu) / ((score_label_TopL_bele+score_label_TopL_bmu) + (score_label_TopR_bele+score_label_TopR_bmu))",
                    "exprBins": {
                        "genpt": {
                            "expr": "fj_gen_pt",
                            "label": "p_{T}(t^{gen})",
                            "bins": [
                                (0, 100000),
                                (0, 200),
                                (200, 400),
                                (400, 600),
                                (600, 800),
                                (800, 1000),
                                (1000, 1200),
                                (1200, 1600),
                                (1600, 2000),
                                (2000, 3000),
                                (3000, 5000),
                            ]
                        }
                    }
                },
                
                #"lepTop_classifier_LvsR_vs_genpt": {
                #    "xtitle": "p_{T}(t^{gen}) [GeV]",
                #    "ytitle": "#LTc^{lep}_{LvR}#GT",
                #    "plotBinX": "25 0.0 1.0",
                #    "plotBinY": "50 0 10000",
                #    "xRange": "0 3000",
                #    "yRange": "0 1.5",
                #    "expr": "fj_gen_pt : (score_label_TopR_bele+score_label_TopR_bmu) / ((score_label_TopL_bele+score_label_TopL_bmu) + (score_label_TopR_bele+score_label_TopR_bmu)) : Y",
                #},
            },
        },
        
        "had": {
            "cut_topL": "(label_TopL_bcq | label_TopL_bqq | label_TopL_bc | label_TopL_bq)",
            "cut_topR": "(label_TopR_bcq | label_TopR_bqq | label_TopR_bc | label_TopR_bq)",
            "cut_others": "(label_TopL_bcq | label_TopL_bqq | label_TopL_bc | label_TopL_bq | label_TopR_bcq | label_TopR_bqq | label_TopR_bc | label_TopR_bq)",
            "vars": {
                
                #"hadTop_genpt": {
                #    "xtitle": "p_{T}(t^{gen}) [GeV]",
                #    "ytitle": "arbitrary unit",
                #    "plotBinX": "50 0 10000",
                #    "plotBinY": "0 0 0",
                #    "xRange": "0 3000",
                #    "yRange": "0 1.5",
                #    "expr": "fj_gen_pt",
                #},
                #
                #"hadTop_jet-pt": {
                #    "xtitle": "p_{T}(jet) [GeV]",
                #    "ytitle": "arbitrary unit",
                #    "plotBinX": "50 0 10000",
                #    "plotBinY": "0 0 0",
                #    "xRange": "0 3000",
                #    "yRange": "0 1.5",
                #    "expr": "fj_pt",
                #},
                #
                #"hadTop_jet-pt_by_genpt": {
                #    "xtitle": "p_{T}(jet) / p_{T}(t^{gen})",
                #    "ytitle": "arbitrary unit",
                #    "plotBinX": "200 0 10",
                #    "plotBinY": "0 0 0",
                #    "xRange": "0 5",
                #    "yRange": "0 0.5",
                #    "expr": "fj_pt / fj_gen_pt",
                #},
                
                "hadTop_gen_cosThetaStar": {
                    "xtitle": "cos#theta*^{, gen}",
                    "ytitle": "arbitrary unit",
                    "plotBinX": "25 0.0 1.0",
                    "plotBinY": "0 0 0",
                    "xRange": "0 1",
                    "yRange": "0 0.2",
                    "expr": "((1.0+fj_gen_cosThetaStar)/2.0)",
                    "exprBins": {
                        "genpt": {
                            "expr": "fj_gen_pt",
                            "label": "p_{T}(t^{gen})",
                            "bins": [
                                (0, 100000),
                                (0, 200),
                                (200, 400),
                                (400, 600),
                                (600, 800),
                                (800, 1000),
                                (1000, 1200),
                                (1200, 1600),
                                (1600, 2000),
                                (2000, 3000),
                                (3000, 5000),
                            ]
                        }
                    }
                },
                
                #"hadTop_gen_cosThetaStar_vs_genpt": {
                #    "xtitle": "p_{T}(t^{gen}) [GeV]",
                #    "ytitle": "#LTcos#theta*^{, gen}#GT",
                #    "plotBinX": "25 0.0 1.0",
                #    "plotBinY": "0 0 0 0 200 400 600 800 1000 1200 1600 2000 3000 5000 10000",
                #    "xRange": "0 3000",
                #    "yRange": "0 1.5",
                #    "expr": "fj_gen_pt : ((1.0+fj_gen_cosThetaStar)/2.0) : Y",
                #},
                
                "hadTop_gen_cosThetaStar_d": {
                    "xtitle": "cos#theta*^{, gen}_{d}",
                    "ytitle": "arbitrary unit",
                    "plotBinX": "25 0.0 1.0",
                    "plotBinY": "0 0 0",
                    "xRange": "0 1",
                    "yRange": "0 0.2",
                    "expr": "((1.0+fj_gen_cosThetaStar_d)/2.0)",
                    "exprBins": {
                        "genpt": {
                            "expr": "fj_gen_pt",
                            "label": "p_{T}(t^{gen})",
                            "bins": [
                                (0, 100000),
                                (0, 200),
                                (200, 400),
                                (400, 600),
                                (600, 800),
                                (800, 1000),
                                (1000, 1200),
                                (1200, 1600),
                                (1600, 2000),
                                (2000, 3000),
                                (3000, 5000),
                            ]
                        }
                    }
                },
                
                #"hadTop_gen_cosThetaStar_d_vs_genpt": {
                #    "xtitle": "p_{T}(t^{gen}) [GeV]",
                #    "ytitle": "#LTcos#theta*^{, gen}_{d}#GT",
                #    "plotBinX": "25 0.0 1.0",
                #    "plotBinY": "0 0 0 0 200 400 600 800 1000 1200 1600 2000 3000 5000 10000",
                #    "xRange": "0 3000",
                #    "yRange": "0 1.5",
                #    "expr": "fj_gen_pt : ((1.0+fj_gen_cosThetaStar_d)/2.0) : Y",
                #},
                
                "hadTop_classifier_LvsR": {
                    "xtitle": "c^{had}_{LvR}",
                    "ytitle": "arbitrary unit",
                    "plotBinX": "25 0.0 1.0",
                    "plotBinY": "0 0 0",
                    "xRange": "0 1",
                    "yRange": "0 0.3",
                    "expr": "(score_label_TopR_bcq+score_label_TopR_bqq+score_label_TopR_bc+score_label_TopR_bq) / ((score_label_TopL_bcq+score_label_TopL_bqq+score_label_TopL_bc+score_label_TopL_bq) + (score_label_TopR_bcq+score_label_TopR_bqq+score_label_TopR_bc+score_label_TopR_bq))",
                    "exprBins": {
                        "genpt": {
                            "expr": "fj_gen_pt",
                            "label": "p_{T}(t^{gen})",
                            "bins": [
                                (0, 100000),
                                (0, 200),
                                (200, 400),
                                (400, 600),
                                (600, 800),
                                (800, 1000),
                                (1000, 1200),
                                (1200, 1600),
                                (1600, 2000),
                                (2000, 3000),
                                (3000, 5000),
                            ]
                        }
                    }
                },
                
                #"hadTop_classifier_LvsR_vs_genpt": {
                #    "xtitle": "p_{T}(t^{gen}) [GeV]",
                #    "ytitle": "#LTc^{had}_{LvR}#GT",
                #    "plotBinX": "25 0.0 1.0",
                #    "plotBinY": "50 0 10000",
                #    "xRange": "0 3000",
                #    "yRange": "0 1.5",
                #    "expr": "fj_gen_pt : (score_label_TopR_bcq+score_label_TopR_bqq+score_label_TopR_bc+score_label_TopR_bq) / ((score_label_TopL_bcq+score_label_TopL_bqq+score_label_TopL_bc+score_label_TopL_bq) + (score_label_TopR_bcq+score_label_TopR_bqq+score_label_TopR_bc+score_label_TopR_bq)) : Y",
                #},
            },
        }
    }
    
    commonCut = (
        f"({jetName}_pt > 200) & "
        #f"({jetName}_gen_pt > 600) & "
        f"(abs({jetName}_eta) < 2.5)"
    )
    
    commonCut_topL = (
        f"({jetName}_pt > 200) & "
        #f"({jetName}_gen_pt > 600) & "
        f"(abs({jetName}_eta) < 2.5)"
    )
    
    commonCut_topR = (
        f"({jetName}_pt > 200) & "
        #f"({jetName}_gen_pt > 600) & "
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
                
                # Dummy when there is no binning
                l_binCombo = [(0, 0)]
                
                if "exprBins" in varInfo :
                    
                    # Bin combinations
                    l_binCombo = list(itertools.product(*[_tmp["bins"] for _tmp in varInfo["exprBins"].values()]))
                
                #print(l_binCombo)
                
                # Iterate over bin combinations
                for iComb, binCombo in enumerate(l_binCombo) :
                    
                    extraCut = ""
                    binLabel = ""
                    outFileName = varName
                    
                    l_extraCut_tmp = []
                    l_binLabel_tmp = []
                    
                    if "exprBins" in varInfo :
                        
                        # Iterate over bin combinations
                        for ibinVar, binVarKey in enumerate(varInfo["exprBins"].keys()) :
                            
                            expr = varInfo["exprBins"][binVarKey]["expr"]
                            label = varInfo["exprBins"][binVarKey]["label"]
                            binLwr = binCombo[ibinVar][0]
                            binUpr = binCombo[ibinVar][1]
                            binLwr_str = str(binLwr).replace(".", "p").replace("-", "m")
                            binUpr_str = str(binUpr).replace(".", "p").replace("-", "m")
                            
                            l_extraCut_tmp.append(f"({binLwr} <= ({expr})) & (({expr}) < {binUpr})")
                            l_binLabel_tmp.append(f"{binLwr}#leq{label}<{binUpr}")
                            outFileName = f"{outFileName}_{binVarKey}-{binLwr_str}-{binUpr_str}"
                        
                        extraCut = " & " + " & ".join(l_extraCut_tmp)
                        binLabel = ", ".join(l_binLabel_tmp)
                    
                    cut_topL = f"({commonCut_topL}) & ({d_type[jetType]['cut_topL']}) {extraCut}"
                    cut_topR = f"({commonCut_topR}) & ({d_type[jetType]['cut_topR']}) {extraCut}"
                    cut_others = f"({commonCut}) & ({d_type[jetType]['cut_others']}) {extraCut}"
                    
                    command = f"""
                        python -u python/plot_variable.py \
                        --fileAndTreeNames \
                            /nfs/dust/cms/user/sobhatta/work/TopTagPol/weaver-core/output/{args.training}/prediction/{args.state}/{args.ntuple}/Wprimetotb_M3000W30_LH_TuneCP5_13TeV-madgraph-pythia8/*.root:Events \
                            /nfs/dust/cms/user/sobhatta/work/TopTagPol/weaver-core/output/{args.training}/prediction/{args.state}/{args.ntuple}/Wprimetotb_M6000W60_LH_TuneCP5_13TeV-madgraph-pythia8/*.root:Events \
                            /nfs/dust/cms/user/sobhatta/work/TopTagPol/weaver-core/output/{args.training}/prediction/{args.state}/{args.ntuple}/Wprimetotb_M3000W30_RH_TuneCP5_13TeV-madgraph-pythia8/*.root:Events \
                            /nfs/dust/cms/user/sobhatta/work/TopTagPol/weaver-core/output/{args.training}/prediction/{args.state}/{args.ntuple}/Wprimetotb_M6000W60_RH_TuneCP5_13TeV-madgraph-pythia8/*.root:Events \
                            /nfs/dust/cms/user/sobhatta/work/TopTagPol/weaver-core/output/{args.training}/prediction/{args.state}/{args.ntuple}/{{TTJets_HT}}/*.root:Events \
                            /nfs/dust/cms/user/sobhatta/work/TopTagPol/weaver-core/output/{args.training}/prediction/{args.state}/{args.ntuple}/{{ST_t-channel}}/*.root:Events \
                        --sampleYaml {sampleYaml} \
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
                        --testW1 4 \
                        --plotBinX {varInfo['plotBinX']} \
                        --plotBinY {varInfo['plotBinY']} \
                        --xRange {varInfo['xRange']} \
                        --yRange {varInfo['yRange']} \
                        --nDivX 5 5 0 \
                        --xTitle "{varInfo['xtitle']}" \
                        --yTitle "{varInfo['ytitle']}" \
                        --histdrawopt "hist E" \
                        --legendPos UL \
                        --legendncol 2 \
                        --title "{binLabel}" \
                        --outFileName "{outDir}/{outFileName}.pdf" \
                    """
                    
                    cmdStr = cleanSpaces(command)
                    print(cmdStr)
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
