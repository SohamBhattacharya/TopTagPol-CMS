import argparse
import matplotlib
import matplotlib.colors
import matplotlib.pyplot
import mplhep
import numpy
import os
import re
import sortedcontainers
import time
import uproot

mplhep.style.use("CMS")
#mplhep.style.use("CMSTex")

#matplotlib.pyplot.rc("text", usetex = True)

matplotlib.rcParams["text.latex.preamble"] += r"\usepackage{amsmath}"
matplotlib.rcParams["text.latex.preamble"] += r"\usepackage{slashed}"
matplotlib.rcParams["text.latex.preamble"] += r"\usepackage{bm}"
matplotlib.rcParams["text.latex.preamble"] += r"\usepackage{commath}"
#
##matplotlib.rcParams['mathtext.fontset'] = 'custom'
##matplotlib.rcParams['mathtext.rm'] = 'Bitstream Vera Sans:bold'
#
##matplotlib.pyplot.rcParams.update({
##    "font.family": "sans-serif",
##    "font.sans-serif": ["Helvetica"]
##})
#
#
#font = {
#    "family" : "sans-serif",
#    "sans-serif": ["Helvetica"],
#    "weight" : "bold",
#    "size"   : 22,
#}
#
#matplotlib.pyplot.rc("font", **font)

def main() :
    
    # Argument parser
    parser = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter)
    
    parser.add_argument(
        "--fileAndTreeNames",
        help = "Syntanx: fileName1:treeName1 fileName2:treeName2 ...",
        type = str,
        nargs = "*",
        required = True,
    )
    
    parser.add_argument(
        "--cut",
        help = "Cut (jet level, like pT, eta, etc)",
        type = str,
        required = True,
    )
    
    parser.add_argument(
        "--constiCut",
        help = "Cut (constituent level, like pdgid). E.g. \"{jet_selectedPatJetsAK15PFPuppi_consti_id_reco} == 11\"",
        type = str,
        required = False,
        default = None,
    )
    
    parser.add_argument(
        "--nJetMax",
        help = "Maximum number of jets to plot",
        type = int,
        required = False,
        default = 100000,
    )
    
    parser.add_argument(
        "--xVar",
        help = "x variable branch name",
        type = str,
        required = True,
    )
    
    parser.add_argument(
        "--yVar",
        help = "y variable branch name",
        type = str,
        required = True,
    )
    
    parser.add_argument(
        "--wVar",
        help = "weight (z) variable branch name",
        type = str,
        required = True,
    )
    
    parser.add_argument(
        "--wTransform",
        help = "Transformation  (any python expression) for the weight variable, followed by the key. E.g. \"{w}*10 if ({w} < 1) else {w}\" \"w\"",
        type = str,
        nargs = 2,
        required = False,
        default = None,
    )
    
    parser.add_argument(
        "--resolverOperation",
        help = "How to update the bin (pixel) value if another constituent is found in the same bin. E.g. (any python expression) \"{new}+{old}\", \"{new} if ({newResolver} > {oldResolver}) else {old}\", etc.",
        type = str,
        required = True,
    )
    
    parser.add_argument(
        "--resolverVar",
        help = "Variable (branch name) to use to resolve the conflict if another constituent is found in the same bin (can be the constituent pT, for example).",
        type = str,
        required = False,
        default = None,
    )
    
    parser.add_argument(
        "--resolverUpdate",
        help = "How to update the resolver variable. E.g. (any python expression) \"max({newResolver}, {oldResolver})\"",
        type = str,
        required = False,
        default = None,
    )
    
    parser.add_argument(
        "--xMin",
        help = "X-axis minumum",
        type = float,
        required = True,
    )
    
    parser.add_argument(
        "--xMax",
        help = "X-axis maximum",
        type = float,
        required = True,
    )
    
    parser.add_argument(
        "--nBinX",
        help = "Number of X-axis bins",
        type = int,
        required = True,
    )
    
    parser.add_argument(
        "--yMin",
        help = "Y-axis minumum",
        type = float,
        required = True,
    )
    
    parser.add_argument(
        "--yMax",
        help = "Y-axis maximum",
        type = float,
        required = True,
    )
    
    parser.add_argument(
        "--nBinY",
        help = "Number of Y-axis bins",
        type = int,
        required = True,
    )
    
    parser.add_argument(
        "--zMin",
        help = "Z-axis minumum",
        type = float,
        required = False,
        default = 1e-5,
    )
    
    parser.add_argument(
        "--zMax",
        help = "Z-axis maximum",
        type = float,
        required = False,
        default = 1,
    )
    
    parser.add_argument(
        "--logZ",
        help = "Z-axis in log scale",
        default = False,
        action = "store_true",
    )
    
    parser.add_argument(
        "--xRange",
        help = "X-axis range: min max",
        type = float,
        nargs = 2,
        required = True,
    )
    
    parser.add_argument(
        "--yRange",
        help = "Y-axis range: min max",
        type = float,
        nargs = 2,
        required = True,
    )
    
    parser.add_argument(
        "--xTitle",
        help = "X-axis title",
        type = str,
        required = False,
        default = "X",
    )
    
    parser.add_argument(
        "--yTitle",
        help = "Y-axis title",
        type = str,
        required = False,
        default = "Y",
    )
    
    parser.add_argument(
        "--zTitle",
        help = "Z-axis title",
        type = str,
        required = False,
        default = "Z",
    )
    
    parser.add_argument(
        "--title",
        help = "Plot title",
        type = str,
        required = False,
        default = "",
    )
    
    parser.add_argument(
        "--titlePos",
        help = "Title position (in data coordinates): x y",
        type = float,
        nargs = 2,
        required = False,
        default = [0, 0],
    )
    
    parser.add_argument(
        "--outFileName",
        help = "Output file name",
        type = str,
        required = True,
    )
    
    
    # Parse arguments
    args = parser.parse_args()
    d_args = vars(args)
    
    l_branchName = [
        args.xVar,
        args.yVar,
        args.wVar,
    ]
    
    if (args.resolverVar is not None) :
        
        l_branchName.append(args.resolverVar)
    
    l_constiCutVar = re.findall(r"\{(\w+)\}", args.constiCut)
    l_branchName.extend(l_constiCutVar)
    
    xBinSize = (args.xMax - args.xMin) / args.nBinX
    yBinSize = (args.yMax - args.yMin) / args.nBinY
    
    arr_jetImg = numpy.zeros((args.nBinY, args.nBinX))
    
    breakFromLoop = False
    
    nJet_selected = 0
    
    for iFile, fileAndTreeName in enumerate(args.fileAndTreeNames) :
        
        for tree_branches in uproot.iterate(
            files = fileAndTreeName,
            expressions = l_branchName,
            cut = args.cut,
            step_size = 10000,
        ) :
            
            nEvent = len(tree_branches[l_branchName[0]])
            #nEvent = 1000
            
            for iEvent in range(0, nEvent) :
                
                nJet = len(tree_branches[l_branchName[0]][iEvent])
                
                for iJet in range(0, nJet) :
                    
                    nJet_selected += 1
                    
                    a_x  = ((tree_branches[args.xVar][iEvent][iJet].to_numpy() - args.xMin) / xBinSize).astype(dtype = numpy.uint32)
                    a_y  = ((tree_branches[args.yVar][iEvent][iJet].to_numpy() - args.yMin) / yBinSize).astype(dtype = numpy.uint32)
                    a_w  = tree_branches[args.wVar][iEvent][iJet].to_numpy()
                    
                    a_resolver = None
                    
                    if (args.resolverVar is not None) :
                        
                        a_resolver = tree_branches[args.resolverVar][iEvent][iJet].to_numpy()
                    
                    a_constiIdx = numpy.column_stack((
                        a_y,
                        a_x,
                    ))
                    
                    d_arrayIdx = sortedcontainers.SortedDict()
                    d_arrayResolver = sortedcontainers.SortedDict()
                    
                    jet_nConsti = len(a_x)
                    
                    for iConsti in range(0, jet_nConsti) :
                        
                        if (args.constiCut is not None) :
                            
                            d_constiCutVar = {}
                            
                            for constiCutVar in l_constiCutVar :
                                
                                d_constiCutVar[constiCutVar] = tree_branches[constiCutVar][iEvent][iJet][iConsti]
                            
                            constiPassed = eval(args.constiCut.format(**d_constiCutVar))
                            
                            if (not constiPassed) :
                                
                                continue
                        
                        key = tuple(a_constiIdx[iConsti])
                        val = a_w[iConsti]
                        
                        if (args.wTransform is not None) :
                            
                            val = eval(args.wTransform[0].format(**{
                                args.wTransform[1]: val,
                            }))
                        
                        resolver = a_resolver[iConsti] if (args.resolverVar is not None) else None
                        
                        if (key in d_arrayIdx) :
                            
                            if (args.resolverVar is not None) :
                                
                                resolver = eval(args.resolverUpdate.format(
                                    oldResolver = d_arrayResolver[key],
                                    newResolver = resolver,
                                ))
                            
                            val = eval(args.resolverOperation.format(
                                oldResolver = d_arrayResolver[key],
                                newResolver = resolver,
                                old = d_arrayIdx[key],
                                new = val,
                            ))
                        
                        
                        d_arrayIdx[key] = val
                        d_arrayResolver[key] = resolver
                    
                    
                    arr_jetImg_temp = numpy.zeros((args.nBinY, args.nBinX))
                    
                    rr = [ele[0] for ele in d_arrayIdx.keys()]
                    cc = [ele[1] for ele in d_arrayIdx.keys()]
                    
                    arr_jetImg_temp[rr, cc] = d_arrayIdx.values()
                    
                    arr_jetImg += arr_jetImg_temp
                    
                    
                    if (args.nJetMax > 0 and nJet_selected >= args.nJetMax) :
                        
                        breakFromLoop = True
                        break
                
                if (iEvent == 0 or iEvent == nEvent-1 or not (iEvent+1)%1000) :
                    
                    print("Processed event %d/%d of file %d/%d: selected %d jets." %(iEvent+1, nEvent, iFile+1, len(args.fileAndTreeNames), nJet_selected))
                
                if (breakFromLoop) : break
            
            if (breakFromLoop) : break
        
        if (breakFromLoop) : break
    
    
    
    print("Selected jets: %d" %(nJet_selected))
    
    arr_jetImg /= nJet_selected
    
    fig = matplotlib.pyplot.figure(figsize = [10, 9])
    
    axis = fig.add_subplot(1, 1, 1)
    caxis = mplhep.make_square_add_cbar(ax = axis)
    
    #axis.set_aspect("auto", "datalim")
    #axis.set_aspect("auto", "box")
    #axis.set_aspect("equal", "datalim")
    
    #mplhep.make_square_add_cbar(ax = axis)
    #mplhep.rescale_to_axessize(ax = axis, w = 10, h = 8)
    
    img = axis.imshow(
        arr_jetImg,
        norm = matplotlib.colors.LogNorm(vmin = args.zMin, vmax = args.zMax),
        origin = "lower",
        #edgecolors = "face",
        #linewidths = 0,
        cmap = matplotlib.cm.get_cmap("nipy_spectral"),
        extent = [0, args.nBinX, 0, args.nBinY],
        aspect = (args.xRange[0]-args.xRange[1])/(args.yRange[0]-args.yRange[1]),
    )
    
    axis.set_xlim(args.xRange[0], args.xRange[1])
    axis.set_ylim(args.yRange[0], args.yRange[1])
    
    axis.set_xlabel(args.xTitle, horizontalalignment = "center", usetex = True)#, verticalalignment = "baseline")
    axis.set_ylabel(args.yTitle, horizontalalignment = "center", usetex = True)#, verticalalignment = "baseline")
    
    #caxis = mplhep.make_square_add_cbar(ax = axis)
    
    cbar = fig.colorbar(img, cax = caxis)
    cbar.ax.set_ylabel(args.zTitle, usetex = True)#, horizontalalignment = "center")
    
    axis.text(x = args.titlePos[0], y = args.titlePos[1], s = args.title, horizontalalignment = "left", verticalalignment = "top", usetex = True)
    
    mplhep.cms.label(label = "Preliminary", data = False, loc = 0, ax = axis)
    
    #mplhep.box_aspect(ax = axis)
    
    #mplhep.plot.xlow(ax = axis, xlow = 0)
    #mplhep.plot.ylow(ax = axis, ylow = 0)
    
    fig.tight_layout()
    
    print("Saving figure: %s" %(args.outFileName))
    fig.savefig(args.outFileName)



if (__name__ == "__main__") :
    
    main()
