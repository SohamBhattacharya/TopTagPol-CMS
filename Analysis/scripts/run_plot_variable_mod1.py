#!/usr/bin/env python

import os
import multiprocessing

def cleanSpaces(string) :

    while ("  " in string) :

        string = string.replace("  ", " ")

    return string


jetName = "fj"
outDir = "plots/variables/dnntuples"

commonCut_sig = (
    f"({jetName}_pt > 200) & "
    f"(abs({jetName}_eta) < 2.5) & "
    f"(fj_isTop == 1)"
)

commonCut_bkg = (
    f"({jetName}_pt > 200) & "
    f"(abs({jetName}_eta) < 2.5) & "
    f"(fj_isQCD == 1)"
)

l_varName = [
    "pfcand_ptWrtJet",
]


niceness = 10
nCPU = max(1, int(multiprocessing.cpu_count()*0.33))
pool = multiprocessing.Pool(processes = nCPU, initializer = os.nice, initargs = (niceness,))
l_job = []
l_jobName = []
l_jobCmd = []

for iVar, varName in enumerate(l_varName) :

    d_format = {}
    #d_format["pdgid"]           = pdgid
    #d_format["pdgidName"]       = pdgidName
    d_format["outDir"]          = outDir
    d_format["jetName"]         = jetName
    d_format["varName"]         = varName

    d_format["commonCut_sig"]       = commonCut_sig
    d_format["commonCut_bkg"]       = commonCut_bkg

    command = """
        python -u python/plot_variable_transform.py \
        --fileAndTreeNames \
            /pnfs/desy.de/cms/tier2/store/user/sobhatta/TopTagPol/DeepNtuples/v3/TTJets*/*/*/*/*.root:deepntuplizer/tree \
            /pnfs/desy.de/cms/tier2/store/user/sobhatta/TopTagPol/DeepNtuples/v3/TTJets*/*/*/*/*.root:deepntuplizer/tree \
            /pnfs/desy.de/cms/tier2/store/user/sobhatta/TopTagPol/DeepNtuples/v3/QCD*/*/*/*/*.root:deepntuplizer/tree \
        --plotVars \
            "{varName}" \
            "{varName}" \
            "{varName}" \
        --cuts \
            "({commonCut_sig}) " \
            "({commonCut_sig})" \
            "({commonCut_bkg})" \
        --labels \
            "PF cand. in t^{lep} jet" \
            "PF cand. in t^{had} jet" \
            "PF cand. in QCD jet" \
        --lineColors \
            4 \
            6 \
        --lineStyles \
            1 \
            1 \
        --fileFraction 0.1 \
        --filePrefix "root://dcache-cms-xrootd.desy.de:/" \
        --skipFileList common/misc/dcache-cms185-186.user-files-lost_DeepNtuples.txt \
        --yRange 1e-5 1e2 \
        --logY \
        --nDivX 5 5 0 \
        --xTitle "{varName}" \
        --yTitle "arbitrary unit" \
        --legendPos UL \
        --varNameSummary "{varName}" \
        --outFileName "{outDir}/{varName}.pdf" \
    """.format(
        **d_format
    )

    #os.system(command)
    #print("\n")

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

