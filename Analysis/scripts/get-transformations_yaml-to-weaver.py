#!/usr/bin/env python3

import argparse
import functools
import glob
import operator
import tabulate
import yaml
import sortedcontainers


def main() :
    
    # Argument parser
    parser = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter)
    
    parser.add_argument(
        "--yamlpaths",
        help = "Path to yaml files. Can also be glob paths: a/b/*.yaml",
        type = str,
        nargs = "*",
        required = True,
    )
    
    parser.add_argument(
        "--sortkey",
        help = "List of (nested) keys to use for getting the sorting parameter (like some test statistic). Pass an empty string to prevent sorting.",
        type = str,
        nargs = "*",
        required = False,
        default = ["ADtest", "statistic"],
    )
    
    # Parse arguments
    args = parser.parse_args()
    d_trans = sortedcontainers.SortedDict()
    l_trans = []
    l_sortval = []
    
    dosort = bool(len(args.sortkey[0]))
    
    for ymlpath in args.yamlpaths :
        
        fNames = glob.glob(ymlpath)
        
        for fName in fNames :
            
            with open(fName, "r") as fopen :
                    
                d_tmp = yaml.load(fopen.read(), Loader = yaml.FullLoader)
                d_trans.update(d_tmp)
    
    for key in d_trans :
        
        center = d_trans[key]["center"]
        scale = d_trans[key]["scale"]
        
        if (dosort) :
            
            test_statistic = functools.reduce(operator.getitem, args.sortkey, d_trans[key])
            l_sortval.append(test_statistic)
        
        l_trans.append(
            f"[{key}, {center:0.4e}, {scale:0.4e}]"
        )
    
    if (dosort) :
        
        # Higher statistic => greater separation
        l_sortedIdx = sorted(range(0, len(l_sortval)), key = lambda _x: l_sortval[_x], reverse = True)
        l_sortval = [l_sortval[_idx] for _idx in l_sortedIdx]
        l_trans = [l_trans[_idx] for _idx in l_sortedIdx]
        
        print(f"\nSorted using {'.'.join(args.sortkey)}:\n")
    
    else :
        
        print(f"\nNo sorting performed:\n")
    
    #print(list(zip(l_trans, l_sortval)))
    
    #print("\n".join(l_trans))
    
    table = tabulate.tabulate(
        {
            "weaver format [name, center, scale]": l_trans,
            ".".join(args.sortkey): l_sortval
        },
        headers = "keys"
    )
    
    print(table)
    
    print("")


if __name__ == "__main__" :
    
    main()