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
import numpy
import math
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from datetime import datetime


def process_arguments():
    """ Process command-line arguments """

    parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--inputLFN", choices=["B", "C", "D", "E", "F", "DEF", "CDEF", "all"],
                        default="tttt102", help="Set era in 2017 to be checked")
    parser.add_argument("-o", "--outputName", default="Scales", help="Set name of output file")
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
    lx.DrawLatex(0.10, 0.70, "Pre-selection Requisites for:")
    lx.DrawLatex(0.16, 0.65, "#bullet Jets: #bf{number > %s}" % preCuts["nJet"])
    lx.DrawLatex(0.16, 0.60, "#bullet Leptons (Muons or Electrons): #bf{number > %s }" % preCuts["nLepton"])
    lx.DrawLatex(0.10, 0.50, "Event Limit: #bf{None (see last page)}")
    lx.DrawLatex(0.10, 0.40, "Baseline selection Requisites for:")
    lx.DrawLatex(0.16, 0.35, "#bullet Jets: #bf{jetId > %s , p_{T} > %s and |#eta|<%s (for at least 6 jets)}"
                 % (selCrit["minJetId"], selCrit["minJetPt"], selCrit["maxObjEta"]))
    lx.DrawLatex(0.16, 0.30, "      #bf{btagDeepFlavB > 0.7489 (for at least one jet)}")
    lx.DrawLatex(0.16, 0.25, "#bullet Muons: #bf{has tightId, |#eta|<%s and PFRelIso_all<%s (for at least 1)}"
                 % (selCrit["maxObjEta"], selCrit["maxPfRelIso04"]))
    lx.DrawLatex(0.16, 0.20, "#bullet #bf{HT >500 GeV}")


def cmsPlotString(args):
    """

    Args:
        args (string): command line arguments

    Returns:
        legStr (string): string containing channel details

    """
    if args == "17B":
        #legStr = "CMS Run2017B"
        legStr = "CMS #bf{                                        Data Run2017B                                            5.61 fb^{-1} (13TeV)}"
    elif args == "17C":
        #legStr = "CMS Run2017C"
        legStr = "CMS #bf{                                        Data Run2017C                                           10.83 fb^{-1} (13TeV)}"
    elif args == "17D":
        #legStr = "CMS Run2017D"
        legStr = "CMS #bf{                                        Data Run2017D                                            4.62 fb^{-1} (13TeV)}"
    elif args == "17E":
        #legStr = "CMS Run2017E"
        legStr = "CMS #bf{                                        Data Run2017E                                            9.83 fb^{-1} (13TeV)}"
    elif args == "17F":
        #legStr = "CMS Run2017F"
        legStr = "CMS #bf{                                        Data Run2017F                                           13.16 fb^{-1} (13TeV)}"
    elif args == "17DEF":
        # legStr = "CMS Run2017D-F"
        legStr = "CMS #bf{                                        Data Run2017D-F                                           27.61 fb^{-1} (13TeV)}"
    elif args == "17CDEF":
        legStr = "CMS Run2017C-F"
    elif args == "all":
        legStr = "CMS All Run2017"
    else:
        legStr = "CMS"

    return legStr


def getFileContents(fileName, elmList):
    """

    Args:
        fileName (string): path/to/file
        elmList (bool): if true then dictionary elements are lists else strings

    Returns:
        fileContents: file contents given as a dictionary or list

    """
    if elmList is False: fileContents = []  # {}
    else: fileContents = {}
    try:
        with open(fileName) as f:
            for line in f:
                if line.find(":") == -1: continue
                (key1, val) = line.split(": ")
                c = len(val) - 1
                val = val[0:c]
                if elmList is False:
                    fileContents.append(val)
                else:
                    fileContents[key1] = val
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
    if era == "17DEF": era = "17D"
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
    if verbose: print(files)
    return files


def findTrigList(file):
    """

    Args:
        file:  file name

    Returns: Trigger List

    """
    if "17B" in file and "data" in file: trigList = getFileContents("../myInFiles/2017ABtrigList.txt", False)
    elif "17B" in file and "TTT" in file: trigList = getFileContents("../myInFiles/trigList.txt", False)
    elif "17C" in file: trigList = getFileContents("../myInFiles/2017CtrigList.txt", False)
    else: trigList = getFileContents("../myInFiles/2017DEFtrigList.txt", False)

    return trigList


def getHistNames(file, verbose=False):
    """

    Args:
        file:
        verbose:
    Returns:
        hNames (list) : list of histogram names

    """
    # objList = ["jetHt", "jetMult", "jetBMult", "jetEta", "jetPhi", "muonPt", "muonEta", "muonPhi",
    #            "metPt", "metPhi"]
    objList = ["jetHt", "jetMult", "jetBMult", "jetEta", "jetPhi", "electronPt", "electronEta", "electronPhi",
               "metPt", "metPhi"]
    trgList = findTrigList(file)
    hNames = []
    for obj in objList:
        hNames.append("h_" + obj + "_notrigger")
        for trg in trgList:
            if "Mu" in trg: continue
            hNames.append("h_" + obj + "_" + trg)
    if verbose: print(hNames)
    return hNames


def getHistograms(fileList, era):
    """

    Args:
        fileList (list):
        era (string):
    Returns:
        h_mcTTTT (dictionary):
    """
    h_mcTTTT = {}
    h_mcTTToSemiLep = {}
    h_dataHTMHT = {}
    h_dataSMu = {}
    h_dataSEl = {}
    f = []
    counter = 0
    for fName in fileList:
        f.append(ROOT.TFile.Open(fName))
        f[counter].cd("plots")
        if "dataSEl" in fName:
            names = getHistNames(fName)
            for name in names:
                h_dataSEl[name] = ROOT.gDirectory.Get(name)
                if not h_dataSEl[name]: print('[ERROR]: No histogram "' + name + '" found in ' + fName)
                hName = name.replace("h_", "h_dataSEl" + era + "_")
                h_dataSEl[name].SetName(hName)
                h_dataSEl[name].SetDirectory(0)  # = h_dataSEl[name].Clone("El" + name)
        if "dataSMu" in fName:
            names = getHistNames(fName)
            for name in names:
                h_dataSMu[name] = ROOT.gDirectory.Get(name)
                if not h_dataSMu[name]: print('[ERROR]: No histogram "' + name + '" found in ' + fName)
                hName = name.replace("h_", "h_dataSMu" + era + "_")
                h_dataSMu[name].SetName(hName)
                h_dataSMu[name].SetDirectory(0)  # = h_dataSMu[name].Clone("Mu" + name)
        if "dataHTMHT" in fName:
            names = getHistNames(fName)
            for name in names:
                h_dataHTMHT[name] = ROOT.gDirectory.Get(name)
                if not h_dataHTMHT[name]: print('[ERROR]: No histogram "' + name + '" found in ' + fName)
                hName = name.replace("h_", "h_dataHTMHT" + era + "_")
                h_dataHTMHT[name].SetName(hName)
                h_dataHTMHT[name].SetDirectory(0)  # = h_dataHTMHT[name].Clone("Ht" + name)
        if "TTTT" in fName:
            names = getHistNames(fName)
            for name in names:
                h_mcTTTT[name] = ROOT.gDirectory.Get(name)
                if not h_mcTTTT[name]: print('[ERROR]: No histogram "' + name + '" found in ' + fName)
                hName = name.replace("h_", "h_mcTTTT" + era + "_")
                h_mcTTTT[name].SetName(hName)
                h_mcTTTT[name].SetDirectory(0)  # = h_mcTTTT[name].Clone("tt" + name)
        if "TTToSemiLep" in fName:
            names = getHistNames(fName)
            for name in names:
                h_mcTTToSemiLep[name] = ROOT.gDirectory.Get(name)
                if not h_mcTTToSemiLep[name]: print('[ERROR]: No histogram "' + name + '" found in ' + fName)
                hName = name.replace("h_", "h_mcTTToSemiLep" + era + "_")
                h_mcTTToSemiLep[name].SetName(hName)
                h_mcTTToSemiLep[name].SetDirectory(0)  # = h_mcTTTT[name].Clone("tt" + name)
        f[counter].Close()
        counter += 1
    return h_mcTTTT, h_mcTTToSemiLep, h_dataHTMHT, h_dataSMu, h_dataSEl


def findTrigRatio(h1, title):
    """

    Args:
        h1 (dictionary): dictionary of histograms
        title (string): title given in legend
    Returns:
        h_Out (dictionary): trigger ratio TH1D histogram

    """
    h_TH1DOut = {}
    h_TEffOut = {}
    h2 = {}

    propList = ["jetHt_", "electronPt_", "jetMult_", "jetBMult_"]
    electronpT_rebin = numpy.array((0., 10., 20., 22., 24., 26., 28., 30., 35., 40., 50., 75., 100., 125., 150., 200., 300.))
    ht_rebin = numpy.array((0., 100., 200., 220., 240., 260., 280., 300., 350., 400., 500., 750., 1000., 1250., 1500., 2000., 3000.))
    for prop in propList:
        for hName in h1:
            if prop not in hName: continue
            # numBins = h1[hName].GetNbinsX()
            if prop == "jetHt_": h1[hName] = h1[hName].Rebin(16, hName, ht_rebin)
            if prop == "electronPt_": h1[hName] = h1[hName].Rebin(16, hName, electronpT_rebin)
            # else: if numBins > 100: h1[hName].RebinX(numBins / 30, "")
            
            if "_notrigger" in hName: h2[prop] = h1[hName]

    for prop in propList:
        for hName in h1:
            if prop not in hName: continue
            if "_notrigger" not in hName:
                if h2 is None: continue
                effName = hName.replace("h_", "h_eff")
                effName2 = hName.replace("h_", "h_eff2")
                # hh, tg = hName.split(prop)
                h_TH1DOut[hName] = h1[hName].Clone(effName)
                h_TH1DOut[hName].Sumw2()
                h_TH1DOut[hName].SetStats(0)
                h_TH1DOut[hName].Divide(h2[prop])
                xTitle = h2[prop].GetXaxis().GetTitle()
                xBinWidth = h2[prop].GetXaxis().GetBinWidth(1)
                h_TH1DOut[hName].SetTitle(title + ";{0};Trigger Efficiency".format(xTitle))
                if not ROOT.TEfficiency.CheckConsistency(h1[hName], h2[prop]): continue
                h_TEffOut[hName] = ROOT.TEfficiency(h1[hName], h2[prop])
                h_TEffOut[hName].SetTitle(title + ";{0};Trigger Efficiency".format(xTitle))
                h_TEffOut[hName].SetName(effName2)

    return h_TH1DOut, h_TEffOut


def scaleFactor(h1, h2, title, era):
    """

    Args:
        h1: numerator
        h2: denominator
        title (string): title given to legend
        era:
    Returns:

    """
    h_scale = {}
    hNameList = []
    for hName in h1:
        for hName2 in h2:
            #print("1  {0}   {1}".format(hName, hName2))
            if not hName == hName2:
                if era == "17B":
                    if hName.find("Ele35_WPTight_Gsf_PFHT380_SixJet32_DoubleBTagCSV_p075") == -1 or hName2.find("Ele35_WPTight_Gsf_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2") == -1:
                        #print("2 {0}   {1}".format(hName, hName2))
                        continue
                    else:
                        #print("1 {0}   {1}".format(hName, hName2))
                        str1 = hName.replace("Ele35_WPTight_Gsf_PFHT380_SixJet32_DoubleBTagCSV_p075", "lala")
                        str2 = hName2.replace("Ele35_WPTight_Gsf_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2", "lala")
                        #print("2 {0}   {1}".format(hName, hName2))
                        if not str1 == str2:
                            #print("str  {0}   {1}".format(str1, str2))
                            #print("3 {0}   {1}".format(hName, hName2))
                            continue
                else: continue  # hNameList.append(hName2)
            print("{0}   {1} ".format(hName, hName2))
            sfName = hName.replace("h_eff", "h_sf")
            hNameList.append(hName)
            h_scale[hName] = h1[hName].Clone(sfName)
            # h_scale[hName].Sumw2()
            h_scale[hName].SetStats(0)
            h_scale[hName].Divide(h2[hName2])
            xTitle = h2[hName2].GetXaxis().GetTitle()
            xBinWidth = h2[hName2].GetXaxis().GetBinWidth(1)
            h_scale[hName].SetTitle(title + ";{0};Scale Factors".format(xTitle))

    return h_scale, hNameList


def whatTrig(h_name):
    """

    Args:
        h_name:

    Returns:

    """
    propList = ["jetHt_", "electronPt_", "jetMult_", "jetBMult_"]
    trig = ""
    for prop in propList:
        if prop in h_name:
            hh, trig = h_name.split(prop)
    # keyWords = h_name.split("_")
    # for nk, keyWord in enumerate(keyWords):
    #    if nk > 3: keyWord[3] += "_" + keyWord[nk]
    return trig


def main():
    """
    Draw scale factors across HT and lep Pt and jet mult
    Returns: nothing

    """
    parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--inputLFN", choices=["17B", "17C", "17D", "17E", "17F", "17DEF", "all"],
                        default="D", help="Set era in 2017 to be checked")
    parser.add_argument("-o", "--outputName", default="NoPreTrig", help="Set name of output file")
    args = parser.parse_args()

    preSelCuts = getFileContents("../myInFiles/preSelectionCuts.txt", True)
    selCriteria = getFileContents("selectionCriteria.txt", True)

    # - Create canvases
    triggerCanvas = ROOT.TCanvas('triggerCanvas', 'Triggers', 900, 500)
    # triggerCanvas.SetFillColor(17)
    # triggerCanvas.SetFrameFillColor(18)
    triggerCanvas.SetGrid()

    # - Create text for legend
    legString = cmsPlotString(args.inputLFN)

    # - Get File Names and create histogram dictionaries
    h_mcTTTTs = {}
    h_mcTTToSemiLeps = {}
    h_dataHTMHTs = {}
    h_dataSMus = {}
    h_dataSEls = {}
    # files = findEraRootFiles(path="OutFiles/Histograms_HTcut", era="17DEF", FullPaths=True)
    # h_mcTTTTs, h_mcTTToSemiLeps, h_dataHTMHTs, h_dataSMus, h_dataSEls = getHistograms(files, "17DEF")
    files17B = findEraRootFiles(path="OutFiles/Histograms_HTcut", era="17B", FullPaths=True)
    h_mcTTTTs17B, h_mcTTToSemiLeps17B, h_dataHTMHTs17B, h_dataSMus17B, h_dataSEls17B = getHistograms(files17B, "17B")
    files17C = findEraRootFiles(path="OutFiles/Histograms_HTcut", era="17C", FullPaths=True)
    h_mcTTTTs17C, h_mcTTToSemiLeps17C, h_dataHTMHTs17C, h_dataSMus17C, h_dataSEls17C = getHistograms(files17C, "17C")
    files17D = findEraRootFiles(path="OutFiles/Histograms_HTcut", era="17D", FullPaths=True)
    h_mcTTTTs17D, h_mcTTToSemiLeps17D, h_dataHTMHTs17D, h_dataSMus17D, h_dataSEls17D = getHistograms(files17D, "17D")
    files17E = findEraRootFiles(path="OutFiles/Histograms_HTcut", era="17E", FullPaths=True)
    h_mcTTTTs17E, h_mcTTToSemiLeps17E, h_dataHTMHTs17E, h_dataSMus17E, h_dataSEls17E = getHistograms(files17E, "17E")
    files17F = findEraRootFiles(path="OutFiles/Histograms_HTcut", era="17F", FullPaths=True)
    h_mcTTTTs17F, h_mcTTToSemiLeps17F, h_dataHTMHTs17F, h_dataSMus17F, h_dataSEls17F = getHistograms(files17F, "17F")

    if args.inputLFN == "17B":
        for hName in h_mcTTToSemiLeps17B:
            h_mcTTToSemiLeps[hName] = h_mcTTToSemiLeps17B[hName]
        for hName in h_dataHTMHTs17B:
            h_dataHTMHTs[hName] = h_dataHTMHTs17B[hName]
            h_dataSMus[hName] = h_dataSMus17B[hName]
            h_dataSEls[hName] = h_dataSEls17B[hName]
    elif args.inputLFN == "17C":
        for hName in h_mcTTToSemiLeps17C:
            h_mcTTToSemiLeps[hName] = h_mcTTToSemiLeps17C[hName]
            h_dataHTMHTs[hName] = h_dataHTMHTs17C[hName]
            h_dataSMus[hName] = h_dataSMus17C[hName]
            h_dataSEls[hName] = h_dataSEls17C[hName]
    else:
        for hname1 in h_dataHTMHTs17D:
            h_mcTTToSemiLeps[hname1] = h_mcTTToSemiLeps17D[hname1]
            for hname2 in h_dataHTMHTs17E:
                if hname1 == hname2:
                    h_dataHTMHTs[hname1] = h_dataHTMHTs17D[hname1]
                    h_dataSMus[hname1] = h_dataSMus17D[hname1]
                    h_dataSEls[hname1] = h_dataSEls17D[hname1]
                    h_dataHTMHTs[hname1].Add(h_dataHTMHTs17E[hname1])
                    h_dataSMus[hname1].Add(h_dataSMus17E[hname1])
                    h_dataSEls[hname1].Add(h_dataSEls17E[hname1])
                    for hname3 in h_dataHTMHTs17F:
                        if hname3 == hname1:
                            h_dataHTMHTs[hname1].Add(h_dataHTMHTs17F[hname1])
                            h_dataSMus[hname1].Add(h_dataSMus17F[hname1])
                            h_dataSEls[hname1].Add(h_dataSEls17F[hname1])
                            # h_dataHTMHTs[hName].Add(h_dataHTMHTs17D[hName], h_dataHTMHTs17E[hName], 1, 1)
                            # h_dataSMus[hName].Add(h_dataSMus17D[hName], h_dataSMus17E[hName], 1, 1)
                            # h_dataSEls[hName].Add(h_dataSEls17D[hName], h_dataSEls17E[hName], 1, 1)

    #  - Find efficiency ratio histogram dictionaries
    # tr_mcTTTT, tr2_mcTTTT = findTrigRatio(h_mcTTTTs, "Four Top MC")
    tr_mcTTToSemiLep, tr2_mcTTToSemiLep = findTrigRatio(h_mcTTToSemiLeps, "Top-AntiTop MC")
    tr_dataHTMHT, tr2_dataHTMHT = findTrigRatio(h_dataHTMHTs, "HTMHT Data")
    tr_dataSMu, tr2_dataSMu = findTrigRatio(h_dataSMus, "Single Muon Data")
    tr_dataSEl, tr2_dataSEl = findTrigRatio(h_dataSEls, "Single Electron Data")

    # - Find scale factor histogram dictionaries
    s_HTMHT, hNames = scaleFactor(tr_dataHTMHT, tr_mcTTToSemiLep, "HTMHT Data", args.inputLFN)
    s_dataSMu, hNamesMu = scaleFactor(tr_dataSMu, tr_mcTTToSemiLep, "Single Muon Data", args.inputLFN)
    s_dataSEl, hNamesEl = scaleFactor(tr_dataSEl, tr_mcTTToSemiLep, "Single Electron Data", args.inputLFN)

    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetOptStat(0)

    triggerCanvas.cd(1)
    ltx = TLatex()
    cutInfoPage(ltx, selCriteria, preSelCuts)
    pdfCreator(args, 0, triggerCanvas)

    cv0 = [None] * 30
    cv1 = [None] * 30
    cv2 = [None] * 30
    hNames.sort()
    for hn, hName in enumerate(hNames):
        
        # - Draw trigger hists
        cv0[hn] = triggerCanvas.cd(1)
        trg = whatTrig(hName)
        if args.inputLFN == "17B":
            intgrLumi = 5.61  # /fb
            if not trg == "Ele35_WPTight_Gsf_PFHT380_SixJet32_DoubleBTagCSV_p075": continue  # 1 is data 2 is mc
        elif args.inputLFN == "17C":
            intgrLumi = 10.83  # /fb
            if not trg == "Ele35_WPTight_Gsf_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2": continue
        elif args.inputLFN == "17D" or args.inputLFN == "17E" or args.inputLFN == "17F" or args.inputLFN == "17DEF":
            intgrLumi = 27.61  # /fb
            if not trg == "Ele32_WPTight_Gsf_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2": continue
        else:
            intgrLumi = 41.53  # /fb
            print("No actions yet for this option")
            continue
        print(">>>>>>>  {0}".format(hName))
        if not hName.find("DoubleBTagCSV_p075") == -1: hName2 = hName.replace("SixJet32_DoubleBTagCSV_p075", "SixPFJet32_DoublePFBTagDeepCSV_2p2")
        else: hName2 = hName
        t = ROOT.TPaveText(0.15, 0.91, 0.7, 0.98, "nbNDC")
        t2 = ROOT.TPaveText(0.08, 0.91, 0.92, 0.96, "nbNDC")
        t.SetFillColor(0)
        t2.SetFillColor(0)
        t.SetTextSize(0.03)
        t2.SetTextSize(0.035)
        t.AddText(trg)
        t2.AddText(legString)
        histEntries = h_mcTTToSemiLeps[hName2].GetEntries()
        h_mcTTToSemiLeps[hName2].SetTitle("Top-AntiTop MC (%d)" % histEntries)
        histEntries = h_dataHTMHTs[hName].GetEntries()
        h_dataHTMHTs[hName].SetTitle("HTMHT Data (%d)" % histEntries)
        histEntries = h_dataSMus[hName].GetEntries()
        h_dataSMus[hName].SetTitle("Single Muon Data (%d) " % histEntries)
        histEntries = h_dataSEls[hName].GetEntries()
        h_dataSEls[hName].SetTitle("Single Electron Data (%d)" % histEntries)
        normVal = (intgrLumi * 831000 * 0.45)/43732445  # (h_mcTTToSemiLeps[hName2].GetEntries())
        print(normVal)
        h_mcTTToSemiLeps[hName2].Scale(normVal)
        for i in range (0, 17):
            binWidth = h_mcTTToSemiLeps[hName2].GetXaxis().GetBinWidth(i)
            binContent = h_mcTTToSemiLeps[hName2].GetBinContent(i)
            newBinContent = round(binContent/binWidth)
            h_mcTTToSemiLeps[hName2].SetBinContent(i, newBinContent)
            binContent = h_dataHTMHTs[hName].GetBinContent(i)
            newBinContent = round(binContent/binWidth)
            h_dataHTMHTs[hName].SetBinContent(i, newBinContent)
            binContent = h_dataSMus[hName].GetBinContent(i)
            newBinContent = round(binContent/binWidth)
            h_dataSMus[hName].SetBinContent(i, newBinContent)
            binContent = h_dataSEls[hName].GetBinContent(i)
            newBinContent = round(binContent/binWidth)
            h_dataSEls[hName].SetBinContent(i, newBinContent)
        h_mcTTToSemiLeps[hName2].Draw('hist')
        h_mcTTToSemiLeps[hName2].SetLineColor(1)
        # tX1 = 0.05 * (h_mcTTToSemiLeps[hName].GetXaxis().GetXmax())
        # tY1 = 1.1*(h_mcTTToSemiLeps[hName].GetMaximum())
        h_dataSEls[hName].Draw('same')
        h_dataSEls[hName].SetLineColor(6)
        h_dataSEls[hName].SetFillColorAlpha(6, 0.4)
        h_dataHTMHTs[hName].Draw('same')
        h_dataHTMHTs[hName].SetLineColor(4)
        h_dataHTMHTs[hName].SetFillColorAlpha(4, 0.4)
        h_dataSMus[hName].Draw('same')
        h_dataSMus[hName].SetLineColor(2)
        h_dataSMus[hName].SetFillColorAlpha(2, 0.4)
        # t.Draw("same")
        t2.Draw("same")
        ROOT.gStyle.SetLegendTextSize(0.035)
        cv0[hn].BuildLegend(0.65, 0.55, 0.95, 0.9)
        # ltx = TLatex()
        # ltx.SetTextSize(0.03)
        # ltx.DrawLatex(tX1, tY1, legString)
        pdfCreator(args, 1, triggerCanvas)
        triggerCanvas.Print("TriggerPlots/images/{0}events.png".format(hn), "png")

        # - Draw trigger efficiency hists
        cv1[hn] = triggerCanvas.cd(1)
        # t.AddText(trg)
        tr2_mcTTToSemiLep[hName2].Draw('AP')
        tr2_mcTTToSemiLep[hName2].SetLineColor(1)
        cv1[hn].Update()
        graph1 = tr2_mcTTToSemiLep[hName2].GetPaintedGraph()
        graph1.SetMinimum(0)
        graph1.SetMaximum(1.2)
        cv1[hn].Update()
        # tX1 = 0.05 * (tr_dataHTMHT[hName].GetXaxis().GetXmax())
        # tY1 = 1.1
        tr2_dataSMu[hName].Draw('same')
        tr2_dataSMu[hName].SetLineColor(2)
        tr2_dataHTMHT[hName].Draw('same')
        tr2_dataHTMHT[hName].SetLineColor(4)
        tr2_dataSEl[hName].Draw('same')
        tr2_dataSEl[hName].SetLineColor(6)
        # t.Draw("same")
        t2.Draw("same")
        ROOT.gStyle.SetLegendTextSize(0.035)
        cv1[hn].BuildLegend(0.65, 0.1, 0.9, 0.38)
        # ltx = TLatex()
        # ltx.SetTextSize(0.03)
        # ltx.DrawLatex(tX1, tY1, legString)
        pdfCreator(args, 1, triggerCanvas)
        triggerCanvas.Print("TriggerPlots/images/{0}teff.png".format(hn), "png")

        # - Draw scale factor hists
        cv2[hn] = triggerCanvas.cd(1)
        # t.AddText(trg)
        s_HTMHT[hName].Draw('E1')
        s_HTMHT[hName].SetLineColor(4)
        s_HTMHT[hName].SetMinimum(0)
        s_HTMHT[hName].SetMaximum(1.8)
        # tX1 = 0.6 * (s_HTMHT[hName].GetXaxis().GetXmax())
        # tY1 = 1.2
        s_dataSMu[hName].Draw('E1 same')
        s_dataSMu[hName].SetLineColor(2)
        s_dataSEl[hName].Draw('E1 same')
        s_dataSEl[hName].SetLineColor(6)
        # t.Draw("same")
        t2.Draw("same")
        ROOT.gStyle.SetLegendTextSize(0.035)
        cv2[hn].BuildLegend(0.65, 0.1, 0.9, 0.28)
        # ltx = TLatex()
        # ltx.SetTextSize(0.03)
        # ltx.DrawLatex(tX1, tY1, legString)
        pdfCreator(args, 1, triggerCanvas)
        triggerCanvas.Print("TriggerPlots/images/{0}sf.png".format(hn), "png")

    # cv1 = triggerCanvas.cd(1)
    # count = 0
    # for hn, hName in enumerate(hNames):
    #     if "jetHt" not in hName: continue
    #     print(hName)
    #     count += 1
    #     s_HTMHT[hName].SetLineColor(count)
    #     if count == 1:
    #         s_HTMHT[hName].Draw('E1')
    #     tX1 = 0.1 * (s_HTMHT[hName].GetXaxis().GetXmax())
    #     tY1 = 1.2 * (s_HTMHT[hName].GetMaximum())
    #     s_HTMHT[hName].Draw('E1 same')
    # cv1.BuildLegend(0.4, 0.1, 0.9, 0.3)
    # ROOT.gStyle.SetLegendTextSize(0.02)
    # ltx = TLatex()
    # ltx.SetTextSize(0.03)
    # ltx.DrawLatex(tX1, tY1, legString)
    # pdfCreator(args, 1, triggerCanvas)
    
    # cv2 = triggerCanvas.cd(1)
    # for hn, hName in enumerate(hNamesMu):
    #     if hn == 0:
    #         s_dataSMu[hName].Draw('E1')
    #     tX1 = 0.1 * (s_dataSMu[hName].GetXaxis().GetXmax())
    #     tY1 = 1.2 * (s_dataSMu[hName].GetMaximum())
    #     s_dataSMu[hName].Draw('E1 same')
    # cv2.BuildLegend(0.4, 0.1, 0.9, 0.3)
    # ROOT.gStyle.SetLegendTextSize(0.02)
    # ltx = TLatex()
    # ltx.SetTextSize(0.03)
    # ltx.DrawLatex(tX1, tY1, legString)
    # pdfCreator(args, 1, triggerCanvas)
    #
    cv3 = triggerCanvas.cd(1)
    t3 = ROOT.TPaveText(0., 0., 1., 1., "nbNDC")
    t3.SetFillColor(0)
    t3.SetTextSize(0.03)
    t3.AddText("Values coming soon")
    t3.Draw()
    pdfCreator(args, 2, triggerCanvas)


if __name__ == '__main__':
    main()
