#!/usr/bin/env python

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

# Parse arguments
args = parser.parse_args()
d_args = vars(args)

era = args.era

jetName = "jet_selectedPatJetsAK8PFPuppi_boost_2_1"
#jetName = "jet_selectedPatJetsAK8PFPuppi_boost_2_1_sd_z0p1_b0_R1"

username = subprocess.check_output(["whoami"]).strip().decode("UTF-8")

commonCut_sig = "({jet}_pT_reco > 400) && (abs({jet}_eta_reco) < 2.5) && ({jet}_nConsti_reco >= 1) && ({jet}_nearestGenTopDR_reco < 0.6) && ({jet}_nearestGenTopIsLeptonic_reco > 0.5) && ({jet}_nearestGenTopbDR_reco < 0.6) && ({jet}_nearestGenTopWlepDR_reco < 0.6)"
commonCut_bkg = "({jet}_pT_reco > 400) && (abs({jet}_eta_reco) < 2.5) && ({jet}_nConsti_reco >= 1) && ({jet}_nearestGenTopDR_reco > 1)"

d_curveInfo_template = {
    "label": None,
    "sig": {
        "sample":         None,
        "tree":           "treeMaker/tree",
        "source":         "ntupleLists/{sample}_{tag}.txt",
        "weight":         commonCut_sig,
    },
    "bkg": {
        "sample":         None,
        "tree":           "treeMaker/tree",
        "source":         "ntupleLists/{sample}_{tag}.txt",
        "weight":         commonCut_bkg,
    },
    "friends": [],
    "vardict": {
        "jet":        jetName,
    },
    "classifier":     (
        "(({jet}_pfParticleNetJetTags_probTbel + {jet}_pfParticleNetJetTags_probTbmu)"
        "/ "
        "({jet}_pfParticleNetJetTags_probTbel+{jet}_pfParticleNetJetTags_probTbmu + "
        "{jet}_pfParticleNetJetTags_probQCDbb + {jet}_pfParticleNetJetTags_probQCDb + "
        "{jet}_pfParticleNetJetTags_probQCDcc + {jet}_pfParticleNetJetTags_probQCDc + "
        "{jet}_pfParticleNetJetTags_probQCDothers))"
    ),
    "classifiercut":  "{classifier} > {value}",
    "color": None,
    "linestyle": 1,
}


sampleYml = f"ntupleDicts/ntupleDict_{era}.yml"

with open(sampleYml, "r") as fopen :
    
    d_sample = yaml.load(fopen.read(), Loader = yaml.FullLoader)


l_curveInfo = []

l_pdgid = [0]#, 11, 13]
l_pdgidName = ["lep"]#, "el", "mu"]
l_pdgidTex = ["lep"]#, "e", "#mu"]


for pdgidIdx in range(0, len(l_pdgid)) :
    
    pdgid = l_pdgid[pdgidIdx]
    pdgidName = l_pdgidName[pdgidIdx]
    pdgidTex = l_pdgidTex[pdgidIdx]
    
    l_curveInfo = []
    l_curveInfoUpdate_sample = []
    
    #if (era == "2018") :
    #    
    #    l_curveInfoUpdate_sample.append({
    #        "label": f"t^{{{pdgidTex}}} (t#bar{{t}}) vs. QCD",
    #        "sig": {"sample": "TTJets"},
    #        "bkg": {"sample": "QCD"},
    #        "color": 1,
    #    })
    
    l_curveInfoUpdate_sample.append({
        "label": f"t^{{{pdgidTex}}} (Z'_{{2 TeV}}) vs. QCD",
        "sig": {"sample": "ZprimeToTT_M2000_W20"},
        "bkg": {"sample": "QCD"},
        "color": 2,
    })
    
    l_curveInfoUpdate_sample.append({
        "label": f"t^{{{pdgidTex}}} (Z'_{{4 TeV}}) vs. QCD",
        "sig": {"sample": "ZprimeToTT_M4000_W40"},
        "bkg": {"sample": "QCD"},
        "color": 6,
    })
    
    l_curveInfoUpdate_sample.append({
        "label": f"t^{{{pdgidTex}}} (W'_{{4 TeV}}) vs. QCD",
        "sig": {"sample": "Wprimetotb_M4000W40"},
        "bkg": {"sample": "QCD"},
        "color": 7,
    })
    
    l_curveInfoUpdate_sample.append({
        "label": f"t^{{{pdgidTex}}} (W'_{{6 TeV}}) vs. QCD",
        "sig": {"sample": "Wprimetotb_M6000W60"},
        "bkg": {"sample": "QCD"},
        "color": 9,
    })
    
    
    d_curveInfo_pdgid_template = copy.deepcopy(d_curveInfo_template)
    
    if (pdgid > 0) :
        
        d_curveInfo_pdgid_template["sig"]["weight"] = "%s && ({jet}_nearestGenTopIsLeptonic_reco == %d)" %(
            d_curveInfo_pdgid_template["sig"]["weight"],
            pdgid,
        )
    
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
        "yrange": [1.0e-6, 1.0],
        "logx": False,
        "logy": True,
        "gridx": True,
        "gridy": True,
        "legendpos": "UL",
        "legendtextsize": 0.04,
        "cpufrac": 0.9,
        "outtag": f"{pdgidName}Top-vs-QCD",
        "outdir": f"plots/ROCs/pfParticleNetJetTags/{era}/{jetName}",
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
