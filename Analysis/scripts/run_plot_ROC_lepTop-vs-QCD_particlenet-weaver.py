#!/usr/bin/env python -u

import argparse
import copy
import os
import pydantic
import subprocess
import yaml


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

era = args.era

jetName = "fj"

username = subprocess.check_output(["whoami"]).strip().decode("UTF-8")

commonCut_sig = (
    "({jet}_pt > 400) && "
    "(abs({jet}_eta) < 2.5)"
)

commonCut_bkg = (
    "({jet}_pt > 400) && "
    "(abs({jet}_eta) < 2.5) && "
    "(label_QCD_bb || label_QCD_cc || label_QCD_b || label_QCD_c || label_QCD_others)"
)

d_jetLabel = {
    "lep"   : "(label_Top_bele || label_Top_bmu)",
    "el"    : "label_Top_bele",
    "mu"    : "label_Top_bmu",
}

d_classifier = {
    "lep"   : "(score_label_Top_bele + score_label_Top_bmu)",
    "el"    : "score_label_Top_bele",
    "mu"    : "score_label_Top_bmu",
    "qcd"   : "(score_label_QCD_bb + score_label_QCD_cc + score_label_QCD_b + score_label_QCD_c + score_label_QCD_others)"
}

d_curveInfo_template = {
    "label": None,
    "sig": {
        "sample":         None,
        "frac":           1,
        "tree":           "Events",
        "source":         f"/nfs/dust/cms/user/sobhatta/work/TopTagPol/weaver-core/output/{args.training}/prediction/{args.state}/{args.ntuple}/{{sample}}/*.root",
        "weight":         commonCut_sig,
    },
    "bkg": {
        "sample":         None,
        "frac":           1,
        "tree":           "Events",
        "source":         f"/nfs/dust/cms/user/sobhatta/work/TopTagPol/weaver-core/output/{args.training}/prediction/{args.state}/{args.ntuple}/{{sample}}/*.root",
        "weight":         commonCut_bkg,
    },
    "friends": [],
    "vardict": {
        "jet":        jetName,
    },
    "classifier":     None,
    "classifiercut":  "{classifier} > {value}",
    "color": None,
    "linestyle": 1,
}


sampleYml = f"common/ntupleDicts/ntupleDict_dnntuples_{era}.yml"

with open(sampleYml, "r") as fopen :
    
    d_sample = yaml.load(fopen.read(), Loader = yaml.FullLoader)


l_curveInfo = []

l_pdgid = [0, 11, 13]
l_pdgidName = ["lep", "el", "mu"]
l_pdgidTex = ["lep", "e", "#mu"]


for pdgidIdx in range(0, len(l_pdgid)) :
    
    pdgid = l_pdgid[pdgidIdx]
    pdgidName = l_pdgidName[pdgidIdx]
    pdgidTex = l_pdgidTex[pdgidIdx]
    
    l_curveInfo = []
    l_curveInfoUpdate_sample = []
    
    classifier = (
        f"({d_classifier[pdgidName]})"
        "/"
        f"({d_classifier[pdgidName]}+{d_classifier['qcd']})"
    )
    
    weight_sig = f"{commonCut_sig} && {d_jetLabel[pdgidName]}"
    
    l_curveInfoUpdate_sample.append({
        "label": f"t^{{{pdgidTex}}} (Z'_{{1 TeV}}) vs. QCD",
        "sig": {"sample": "ZprimeToTTJets_M1000_W10", "weight": weight_sig},
        "bkg": {"sample": "QCD", "frac": 0.5},
        "classifier": classifier,
        "color": 2,
    })
    
    l_curveInfoUpdate_sample.append({
        "label": f"t^{{{pdgidTex}}} (Z'_{{3 TeV}}) vs. QCD",
        "sig": {"sample": "ZprimeToTT_M3000_W30", "weight": weight_sig},
        "bkg": {"sample": "QCD", "frac": 0.5},
        "classifier": classifier,
        "color": 4,
    })
    
    l_curveInfoUpdate_sample.append({
        "label": f"t^{{{pdgidTex}}} (Z'_{{6 TeV}}) vs. QCD",
        "sig": {"sample": "ZprimeToTTJets_M6000_W60", "weight": weight_sig},
        "bkg": {"sample": "QCD", "frac": 0.5},
        "classifier": classifier,
        "color": 6,
    })
    
    d_curveInfo_pdgid_template = copy.deepcopy(d_curveInfo_template)
    
    #if (pdgid > 0) :
    #    
    #    d_curveInfo_pdgid_template["sig"]["weight"] = "%s && ({jet}_nearestGenTopIsLeptonic_reco == %d)" %(
    #        d_curveInfo_pdgid_template["sig"]["weight"],
    #        pdgid,
    #    )
    
    for iCurve, d_curveInfoUpdate in enumerate(l_curveInfoUpdate_sample) :
        
        d_curveInfo_sample = copy.deepcopy(d_curveInfo_pdgid_template)
        d_curveInfo_sample = pydantic.utils.deep_update(d_curveInfo_sample, d_curveInfoUpdate)
        
        l_curveInfo.append(d_curveInfo_sample)
    
    d_config = {
        "samples": d_sample,
        "curves": l_curveInfo,
        "xtitle": "Signal efficiency",
        "ytitle": "Background efficiency",
        "xrange": [0.0, 1.0],
        "yrange": [1.0e-8, 1.0],
        "logx": False,
        "logy": True,
        "gridx": True,
        "gridy": True,
        "legendpos": "UL",
        "legendtextsize": 0.04,
        "cpufrac": 0.6,
        "outtag": f"{pdgidName}Top-vs-QCD",
        "outdir": f"plots/ROCs/{args.training}/{args.state}/{args.ntuple}/{era}/{jetName}",
    }
    
    #print(d_config)
    
    timestamp = subprocess.check_output(["date", "+%Y-%m-%d_%H-%M-%N"]).strip().decode("UTF-8")
    
    os.system(f"mkdir -p /tmp/{username}")
    tmpCfgName = f"/tmp/{username}/config_plot_ROC_{d_config['outtag']}_{timestamp}.yml"
    
    with open(tmpCfgName, "w") as fOut :
        
        fOut.write(yaml.dump(d_config, width = float("inf")))
    
    print(f"Created temporary config file: {tmpCfgName}")
    
    cmd = f"python -u python/plot_ROC.py --config {tmpCfgName}"
    print(cmd)
    
    cmd_retVal = os.system(cmd)
    
    if (cmd_retVal) :
        
        exit(cmd_retVal)
