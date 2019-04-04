#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Jan 2019

@author: NikHoffStyl
"""
import os
import errno
import ROOT
from ROOT import TLatex
import math
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from datetime import datetime


def process_arguments():
    """ Process command-line arguments """

    parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--inputLFN", choices=["B", "C", "D", "E", "F", "DEF", "CDEF", "all"],
                        default="tttt102", help="Set era in 2017 to be checked")
    parser.add_argument("-o", "--outputName", default="NoPreTrig", help="Set name of output file")
    args = parser.parse_args()

    return args


def pdfCreator(parg, arg, canvas):
    """
    Create a pdf of histograms

    Args:
        parg (class): commandline arguments
        arg (int): print argument
        canvas (TCanvas): canvas which includes plot

    """
    time_ = datetime.now()
    filename = time_.strftime("TriggerPlots/" + parg.outputName + "%V_%y/Era" + parg.inputLFN + ".pdf")
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    if arg == 0:
        canvas.Print(filename + "(", "pdf")
    if arg == 1:
        canvas.Print(filename, "pdf")
    if arg == 2:
        canvas.Print(filename + ")", "pdf")


def turnOnFit(x, par):
    """
    Write turn-on efficiency fit function

    Args:
        x: list of the dimensions
        par: list of the parameters

    Returns:
        fitval: function

    """
    subFunc = (x[0] - par[2]) / (par[1] * math.sqrt(x[0]))
    fitval = (0.5 * par[0] * (1 + ROOT.TMath.Erf(subFunc))) + par[3]
    return fitval


def fitInfo(fit, fitName, args):
    """

    Args:
        fit: fitted function
        fitName: fit name
        args: cmd arguments

    Returns:

    """
    fitFile = open("InfoEra17" + args.inputLFN + ".txt", "a+")
    try:
        with fitFile:
            plateau = fit.GetParameter(0) + fit.GetParameter(3)
            plateauError = fit.GetParError(0) + fit.GetParError(3)
            fitFile.write("{0}, {1}, {2:.3f}, +/-, {3:.3f}, {4:.3f}, +/-, {5:.3f}, {6:.3f}, {7:.3f}, {8}, "
                          "{9:.3f}, +/- ,{10:.3f}, {11:.3f}, +/-, {12:.3f}\n " .format
                          (args.inputLFN, fitName, plateau, plateauError, fit.GetParameter(2), fit.GetParError(2),
                           fit.GetChisquare(), fit.GetNDF(), fit.GetProb(), fit.GetParameter(1), fit.GetParError(1),
                           fit.GetParameter(3), fit.GetParError(3)))

    except OSError:
        print("Could not open file!")


def append2File(info, arg):
    """
    Args:
        info (string): information to be written to file
        arg (string): key name

    Returns:

    """
    fitFile = open("InfoEra17" + arg + ".txt", "a+")
    try:
        with fitFile:
            fitFile.write(info)
    except OSError:
        print("Could not open file!")


def cutInfoPage(lx, selCrit, preCuts):
    """

    Args:
        lx (TLatex): latex string
        selCrit (dictionary): selection criteria
        preCuts (dictionary): pre selection criteria

    Returns:

    """
    lx.SetTextSize(0.04)
    lx.DrawLatex(0.10, 0.70, "On-line (pre-)selection Requisites for:")
    lx.DrawLatex(0.16, 0.65, "#bullet Jets: #bf{number > %s}" % preCuts["nJet"])
    lx.DrawLatex(0.16, 0.60, "#bullet Muons plus Electrons: #bf{number > %s }" % preCuts["nLepton"])
    lx.DrawLatex(0.10, 0.50, "Event Limit: #bf{None (see last page)}")
    lx.DrawLatex(0.10, 0.40, "Off-line (post-)selection Requisites for:")
    lx.DrawLatex(0.16, 0.35, "#bullet Jets: #bf{jetId > %s , p_{T} > %s and |#eta|<%s (for at least 6 jets)}"
                 % (selCrit["minJetId"], selCrit["minJetPt"], selCrit["maxObjEta"]))
    lx.DrawLatex(0.16, 0.30, "      #bf{btagDeepFlavB > 0.7489 (for at least one jet)}")
    lx.DrawLatex(0.16, 0.25, "#bullet Muons: #bf{has tightId, |#eta|<%s and miniPFRelIso_all<%s (for at least 1)}"
                 % (selCrit["maxObjEta"], selCrit["maxPfRelIso04"]))


def cmsPlotString(args):
    """

    Args:
        args (string): command line arguments

    Returns:
        legStr (string): string containing channel details

    """
    if not args.find("TTToSemiLep") == -1:
        legStr = "#splitline{CMS}{t#bar{t} #rightarrow l #nu_{l} #plus jets}"
    elif not args.find("ttjets") == -1:
        legStr = "#splitline{CMS}{t#bar{t} #rightarrow l #nu_{l} #plus jets}"
    elif args.find("TTTT") != -1 and args.find("TTTT_") == -1:
        legStr = "#splitline{CMS}{t#bar{t}t#bar{t} #rightarrow l #nu_{l} #plus jets}"
    elif args == "tttt_weights":
        legStr = "#splitline{CMS}{t#bar{t}t#bar{t} #rightarrow l #nu_{l} #plus jets}"
    elif not args.find("dataHTMHT17B") == -1:
        legStr = "#splitline{CMS}{HTMHT Data Run2017B}"
    elif not args.find("dataHTMHT17C") == -1:
        legStr = "#splitline{CMS}{HTMHT Data Run2017C}"
    elif not args.find("dataHTMHT17D") == -1:
        legStr = "#splitline{CMS}{HTMHT Data Run2017D}"
    elif not args.find("dataHTMHT17E") == -1:
        legStr = "#splitline{CMS}{HTMHT Data Run2017E}"
    elif not args.find("dataHTMHT17F") == -1:
        legStr = "#splitline{CMS}{HTMHT Data Run2017F}"
    elif not args.find("dataSMu17B") == -1:
        legStr = "#splitline{CMS}{Single Muon Data Run2017B}"
    elif not args.find("dataSMu17C") == -1:
        legStr = "#splitline{CMS}{Single Muon Data Run2017C}"
    elif not args.find("dataSMu17D") == -1:
        legStr = "#splitline{CMS}{Single Muon Data Run2017D}"
    elif not args.find("dataSMu17E") == -1:
        legStr = "#splitline{CMS}{Single Muon Data Run2017E}"
    elif not args.find("dataSMu17F") == -1:
        legStr = "#splitline{CMS}{Single Muon Data Run2017F}"
    elif not args.find("dataSEl17B") == -1:
        legStr = "#splitline{CMS}{Single Electron Data Run2017B}"
    elif not args.find("dataSEl17C") == -1:
        legStr = "#splitline{CMS}{Single Electron Data Run2017C}"
    elif not args.find("dataSEl17D") == -1:
        legStr = "#splitline{CMS}{Single Electron Data Run2017D}"
    elif not args.find("dataSEl17E") == -1:
        legStr = "#splitline{CMS}{Single Electron Data Run2017E}"
    elif not args.find("dataSEl17F") == -1:
        legStr = "#splitline{CMS}{Single Electron Data Run2017F}"
    elif not args.find("Wjets") == -1:
        legStr = "#splitline{CMS}{W #rightarrow jets}"
    else:
        legStr = "CMS"

    return legStr


def getFileContents(fileName, elmList):
    """

    Args:
        fileName (string): path/to/file
        elmList (bool): if true then dictionary elements are lists else strings

    Returns:
        fileContents (dictionary): file contents given as a dictionary

    """
    fileContents = [] #{}
    try:
        with open(fileName) as f:
            for line in f:
                if line.find(":") == -1: continue
                (key1, val) = line.split(": ")
                c = len(val) - 1
                val = val[0:c]
                if elmList is False:
                    fileContents.append(val)
                #else:
                    #fileContents[key1] = val.split(", ")
    except OSError as fnf_error:
        print(fnf_error)

    return fileContents


def findEraRootFiles(path, era="all", verbose=False, FullPaths=False):
    """
    Find Root files in a given directory/path.
    Args:
        path (string): directory
        era (string): specifies which era to look at
        verbose (bool): print to stdout if true
        FullPaths (bool): return path plus file name in list elements

    Returns: files (list): list of names of root files in the directory given as argument

    """
    files = []
    if not path[-1] == '/': path += '/'
    if verbose: print(' >> Looking for files in path: ' + path)
    for f in os.listdir(path):
        if not f[-5:] == '.root': continue
        if era != "all" and era not in f[:-5]: continue
        if verbose: print(' >> Adding file: ', f)
        files.append(f)
    if FullPaths: files = [path + x for x in files]
    if len(files) == 0: print('[ERROR]: No root files found in: ' + path)
    return files


def findTrigList(file):
    """

    Args:
        file:  file name

    Returns: Trigger List

    """
    if "17B" in file: trigList = getFileContents("../myInFiles/2017ABtrigList.txt", False)
    elif "17C" in file: trigList = getFileContents("../myInFiles/2017CtrigList.txt", False)
    else: trigList = getFileContents("../myInFiles/2017DEFtrigList.txt", False)

    return trigList


def getHistNames(file):
    """

    Args:
        file:

    Returns:
        hNames (list) : list of histogram names

    """
    objList = ["jetHT", "jetMult", "jetBMult", "jestEta", "jetEta", "jetPhi", "muonPt", "muonEta", "muonPhi",
               "metPt", "metPhi"]
    # objList = ["jetHT", "jetMult", "jetBMult", "jestEta", "jetEta", "jetPhi", "elPt", "elEta", "elPhi",
    #            "metPt", "metPhi"]
    trgList = findTrigList(file)
    hNames = []
    for obj in objList:
        hNames.append(obj + "_notrigger")
        for trg in trgList:
            hNames.append(obj + "_" + trg)

    return hNames


def getHistograms(files, era):
    """

    Args:
        files (list):
        era (string):
    Returns:

    """
    if not era == "all": histNames = getHistNames(files[0])
    h_mcTTTT = {}
    h_mcTTToSemiLep = {}
    h_dataHTMHT = {}
    h_dataSMu = {}
    h_dataSEl = {}
    for file in files:
        if era == "all":
            histNames = getHistNames(file)
        histFile = ROOT.TFile.Open(file)
        histFile.cd("plots")
        for name in histNames:
            if "TTTT" in file:
                h_mcTTTT[name] = ROOT.gDirectory.Get("h_" + name)
                if not (h_mcTTTT[name]):
                    print('[ERROR]: No histogram "' + name + '" found in' + file)
            elif "TTToSemi" in file:
                h_mcTTToSemiLep[name] = ROOT.gDirectory.Get("h_" + name)
                if not (h_mcTTToSemiLep[name]):
                    print('[ERROR]: No histogram "' + name + '" found in' + file)
            elif "dataHTMHT" in file:
                h_dataHTMHT[name] = ROOT.gDirectory.Get("h_" + name)
                if not (h_dataHTMHT[name]):
                    print('[ERROR]: No histogram "' + name + '" found in' + file)
            elif "dataSMu" in file:
                h_dataSMu[name] = ROOT.gDirectory.Get("h_" + name)
                if not (h_dataSMu[name]):
                    print('[ERROR]: No histogram "' + name + '" found in' + file)
            elif "dataSEl" in file:
                h_dataSEl[name] = ROOT.gDirectory.Get("h_" + name)
                if not (h_dataSEl[name]):
                    print('[ERROR]: No histogram "' + name + '" found in' + file)

    return h_mcTTTT, h_mcTTToSemiLep, h_dataHTMHT, h_dataSMu, h_dataSEl


def findTrigRatio(h1):
    """

    Args:
        h1 (dictionary): dictionary of histograms

    Returns:
        h_Out (dictionary): trigger ratio TH!D histogram

    """
    h_Out = {}
    h2 = None
    propList = ["jetHT", "muonPt", "jetMult", "jetBMult"]
    for prop in propList:
        for hName in h1:
            if prop not in hName: continue
            numBins = h1[hName].GetNbinsX()
            h1[hName].RebinX(numBins / 10, "")
            if "_notrigger" in hName: h2 = h1[hName]
            if "_notrigger" not in hName:
                if h2 is None: continue
                prop, tg = hName.split("_")
                h_Out[hName] = h1[hName].Clone("h_jetHtRatio" + tg)
                h_Out[hName].Sumw2()
                h_Out[hName].SetStats(0)
                h_Out[hName].Divide(h2)
                xTitle = h2.GetXaxis().GetTitle()
                xBinWidth = h2.GetXaxis().GetBinWidth(1)
                h_Out[hName].SetTitle(";{0};Trigger Efficiency per {1} GeV/c".format(xTitle, round(xBinWidth)))
                h_Out[hName].SetName(hName)

    return h_Out


def scaleFactor(h1, h2):
    """

    Args:
        h1:
        h2:

    Returns:

    """
    h_scale = {}
    hNameList = []
    for hName in h1:
        for hName2 in h2:
            if not hName == hName2: continue
            hNameList.append(hName)
            h_scale[hName] = h1[hName].Clone("h_scale" + hName)
            h_scale[hName].Sumw2()
            h_scale[hName].SetStats(0)
            h_scale[hName].Divide(h2[hName])
            xTitle = h2[hName].GetXaxis().GetTitle()
            xBinWidth = h2[hName].GetXaxis().GetBinWidth(1)
            h_scale[hName].SetTitle(";{0};Scale Factors per {1} GeV/c".format(xTitle, round(xBinWidth)))
            h_scale[hName].SetName(hName)

    return h_scale, hNameList


def main():
    """
    Draw scale factors across HT and lep Pt and jet mult
    Returns: nothing

    """
    parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--inputLFN", choices=["17B", "17C", "17D", "17E", "17F", "all"],
                        default="D", help="Set era in 2017 to be checked")
    parser.add_argument("-o", "--outputName", default="NoPreTrig", help="Set name of output file")
    args = parser.parse_args()

    # - Create canvases
    triggerCanvas = ROOT.TCanvas('triggerCanvas', 'Triggers', 750, 500)  # 1100 600
    triggerCanvas.SetFillColor(17)
    triggerCanvas.SetFrameFillColor(18)
    triggerCanvas.SetGrid()

    # - Create text for legend
    legString = cmsPlotString(args.inputLFN)

    # - Get File Names and create histogram dictionaries
    files = findEraRootFiles(path="OutFiles/Histograms", era=args.inputLFN, FullPaths=True)
    h_mcTTTT, h_mcTTToSemiLep, h_dataHTMHT, h_dataSMu, h_dataSEl = getHistograms(files, args.inputLFN)

    #  - Find efficiency ratio histogram dictionaries
    tr_mcTTTT = findTrigRatio(h_mcTTTT)
    # tr_mcTTToSemiLep = findTrigRatio(h_mcTTToSemiLep)
    tr_dataHTMHT = findTrigRatio(h_dataHTMHT)
    tr_dataSMu = findTrigRatio(h_dataSMu)
    tr_dataSEl = findTrigRatio(h_dataSEl)

    # - Find scale factor histogram dictionaries
    s_HTMHT, hNames = scaleFactor(tr_dataHTMHT, tr_mcTTTT)
    s_dataSMu, hNamesMu = scaleFactor(tr_dataSMu, tr_mcTTTT)
    s_dataSEl, hNamesEl = scaleFactor(tr_dataSEl, tr_mcTTTT)

    #  - Draw scale factor hists
    cv1 = triggerCanvas.cd(1)
    for hn, hName in enumerate(hNames):
        if hn == 0:
            s_HTMHT[hName].Draw()
            tX1 = 0.6 * (s_HTMHT[hName].GetXaxis().GetXmax())
            tY1 = 1 * (s_HTMHT[hName].GetMaximum())
        s_HTMHT[hName].Draw("same")
    cv1.BuildLegend(0.4, 0.1, 0.9, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx = TLatex()
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(args, 0, triggerCanvas)

    cv2 = triggerCanvas.cd(1)
    for hn, hName in enumerate(hNamesMu):
        if hn == 0:
            s_dataSMu[hName].Draw()
            tX1 = 0.6 * (s_dataSMu[hName].GetXaxis().GetXmax())
            tY1 = 1 * (s_dataSMu[hName].GetMaximum())
        s_dataSMu[hName].Draw("same")
    cv2.BuildLegend(0.4, 0.1, 0.9, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx = TLatex()
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(args, 1, triggerCanvas)

    cv3 = triggerCanvas.cd(1)
    for hn, hName in enumerate(hNamesEl):
        if hn == 0:
            s_dataSEl[hName].Draw()
            tX1 = 0.6 * (s_dataSEl[hName].GetXaxis().GetXmax())
            tY1 = 1 * (s_dataSEl[hName].GetMaximum())
        s_dataSEl[hName].Draw("same")
    cv3.BuildLegend(0.4, 0.1, 0.9, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx = TLatex()
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(args, 2, triggerCanvas)


if __name__ == '__main__':
    main()
