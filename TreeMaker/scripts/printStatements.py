#!bin/sh python

import os


outfileName = "statements.txt"

toReplace = "$$$"

l_str = [
"genTop_b_id",
"genTop_b_E",
"genTop_b_px",
"genTop_b_py",
"genTop_b_pz",
"genTop_b_pT",
"genTop_b_eta",
"genTop_b_y",
"genTop_b_phi",
"genTop_b_m",

"genTop_Wq1_id",
"genTop_Wq1_E",
"genTop_Wq1_px",
"genTop_Wq1_py",
"genTop_Wq1_pz",
"genTop_Wq1_pT",
"genTop_Wq1_eta",
"genTop_Wq1_y",
"genTop_Wq1_phi",
"genTop_Wq1_m",

"genTop_Wq2_id",
"genTop_Wq2_E",
"genTop_Wq2_px",
"genTop_Wq2_py",
"genTop_Wq2_pz",
"genTop_Wq2_pT",
"genTop_Wq2_eta",
"genTop_Wq2_y",
"genTop_Wq2_phi",
"genTop_Wq2_m",

"genTop_Wlep_id",
"genTop_Wlep_E",
"genTop_Wlep_px",
"genTop_Wlep_py",
"genTop_Wlep_pz",
"genTop_Wlep_pT",
"genTop_Wlep_eta",
"genTop_Wlep_y",
"genTop_Wlep_phi",
"genTop_Wlep_m",
]


templateStr = (
    "sprintf(name, \"{name}\");\n"
    "tree->Branch(name, &v_{name});"
)
linegaps = 1

#templateStr = (
#    "sprintf(brName, \"jet_%s_{name}\", str_jetName.c_str());\n"
#    "tree->Branch(brName, &v_jet_{name});"
#)
#linegaps = 1

#templateStr = (
#    "sprintf(brName, \"jet_%s_{name}\", str_jetName.c_str());\n"
#    "tree->Branch(brName, &vv_jet_{name});"
#)
#linegaps = 1

#templateStr = (
#    "jetInfo->vv_jet_{name}.push_back(v_jet_{name});"
#)
#linegaps = 0


with open(outfileName, "w") as f :
    
    for iEntry in range(0, len(l_str)) :
        
        #temp_str = templateStr %(l_str[iEntry])
        temp_str = templateStr
        temp_str = temp_str.format(name = l_str[iEntry])
        
        print(temp_str + "\n" * linegaps)
        
        temp_str += "\n"
        temp_str += "\n" * linegaps
        
        f.write(temp_str)
        

