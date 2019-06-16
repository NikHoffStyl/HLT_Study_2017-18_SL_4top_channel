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
from tools import *
from plotStyle import *
import math
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from datetime import datetime

SetPlotStyle()

histFilesDir = "/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/TrigStudyMuJets/v2_HistFiles/"
pwd = "/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/TrigStudyMuJets/"


def pdfCreator(parg, arg, canvas):
    """
    Create a pdf of histograms

    Args:
        parg (class): commandline arguments
        arg (int): print argument
        canvas (TCanvas): canvas which includes plot

    """
    filename = parg.pdfName + "Era" + parg.inputLFN + ".pdf"
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


def fitInfo(fit, fitName, args, writeOpt):
    """

    Args:
        fit: fitted function
        fitName: fit name
        args: cmd arguments
        writeOpt: string a+ TODO-assert options
    Returns:

    """
    filename = pwd + "/fitInfo/Era" + parg.inputLFN + ".txt"
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    fitFile = open(filename, writeOpt)
    try:
        with fitFile:
            plateau = fit.GetParameter(0) + fit.GetParameter(3)
            plateauError = fit.GetParError(0) + fit.GetParError(3)
            fitFile.write("{0}, {1}, {2:.3f}, +/-, {3:.3f}, {4:.3f}, +/-, {5:.3f}, {6:.3f}, {7:.3f}, {8}, "
                          "{9:.3f}, +/- ,{10:.3f}, {11:.3f}, +/-, {12:.3f}\n ".format
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
    fitFile = open(pwd + "/fitInfo/Era" + arg + ".txt", "a+")
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
        legStr = "#bf{CMS Preliminary}            Run2017B      4.82 fb^{-1} (13TeV)"
    elif args == "17C":
        legStr = "#bf{CMS Preliminary}            Run2017C      9.66 fb^{-1} (13TeV)"
    elif args == "17D":
        legStr = "#bf{CMS Preliminary}            Run2017D      4.25 fb^{-1} (13TeV)"
    elif args == "17E":
        legStr = "#bf{CMS Preliminary}            Run2017E      9.28 fb^{-1} (13TeV)"
    elif args == "17F":
        legStr = "#bf{CMS Preliminary}            Run2017F      13.52 fb^{-1} (13TeV)"
    elif args == "17DEF":
        legStr = "#bf{CMS Preliminary}            Run2017D-F    27.05 fb^{-1} (13TeV)"
    elif args == "17CDEF":
        legStr = "#bf{CMS Preliminary}            Run2017C-F    36.71 fb^{-1} (13TeV)"
    elif args == "all":
        legStr = "#bf{CMS Preliminary}           All Run2017    41.53 fb^{-1} (13TeV)"
    else:
        legStr = "#bf{CMS Preliminary}"

    return legStr


def getFileContents(fileName, elmList):
    """

    Args:
        fileName (string): path/to/file
        elmList (bool): if true then dictionary elements are lists else strings

    Returns:
        fileContents: file contents given as a dictionary or list

    """
    if elmList is False:
        fileContents = []  # {}
    else:
        fileContents = {}
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


def findTrigList(fileName):
    """

    Args:
        fileName:  fileName name

    Returns: Trigger List

    """
    trigList = []
    if "17B" in fileName:
        if "ht" in fileName or "smu" in fileName or "sel" in fileName:
            trigList = getFileContents("../myInFiles/2017ABtrigList.txt", True)
        elif "tt" in fileName or "TT" in fileName or "bbbar" in fileName:
            trigList = getFileContents("../myInFiles/trigList.txt", True)
    elif "17C" in fileName:
        trigList = getFileContents("../myInFiles/2017CtrigList.txt", True)
    else:
        trigList = getFileContents("../myInFiles/2017DEFtrigList.txt", True)

    return trigList


def getHistNames(fileName, verbose=False):
    """

    Args:
        fileName:
        verbose:
    Returns:
        hNames (list) : list of histogram names

    """
    xAxesOptions = ["HT", "pt",
                    "lepEta", "lepPhi",
                    "nJet", "nBJet"
                    ]
    trgList = findTrigList(fileName)
    hNames = []
    for xAxisLabel in xAxesOptions:
        for lep in ["Mu", "El"]:
            for key in trgList:
                if lep == "El" and "Mu" in key: continue
                if lep == "Mu" and "El" in key: continue
                hNames.append("h_" + lep + "_" + xAxisLabel + "_" + key)
            hNames.append("h_" + lep + "_" + xAxisLabel + "_no-HLT")
    if verbose: print(hNames)
    return hNames


def rebinHist(hIn):
    """
    Args: 
       hIn: Input histogram List
    Returns:
       hOut: Output histogram List
    """
    muonpT_rebin = numpy.array(
        (0., 10., 20., 22., 24., 26., 28., 30., 35., 40., 50., 75., 100., 125., 150., 200., 300.))
    ht_rebin = numpy.array(
        (0., 100., 200., 220., 240., 260., 280., 300., 350., 400., 500., 750., 1000., 1250., 1500., 2000., 3000.))

    hOut = {}
    for hName in hIn:
        if "HT_" in hName:
            hOut[hName] = hIn[hName].Rebin(16, hName, ht_rebin)
            newXtitle = hOut[hName].GetXaxis().GetTitle()
            hOut[hName].GetYaxis().SetTitle(newXtitle + "per GeV")
        elif "pt_" in hName:
            hOut[hName] = hIn[hName].Rebin(16, hName, muonpT_rebin)
            newXtitle = hOut[hName].GetXaxis().GetTitle()
            hOut[hName].GetYaxis().SetTitle(newXtitle + "per GeV")
        else:
            hOut[hName] = hIn[hName]
        # print(hOut[hName].GetNbinsX())

    return hOut


def getHistograms(fileList, era, newDir):
    """

    Args:
        fileList (list):
        era (string):
        newDir (TDirectory):
    Returns:
        h_mcTTTT (dictionary):
    """
    h_dataSEl = {}
    h_dataSMu = {}
    h_dataHTMHT = {}
    h_mcTTTT = {}
    h_mcTTToSemiLep = {}
    h_mcTTJets_DiLep = {}
    h_mcTTHadronic = {}
    h_mcTTJets = {}
    f = []

    if era == "17B":
        intgrLumi = 4.823  # /fb
    elif era == "17C":
        intgrLumi = 9.664  # /fb
    elif (era == "17D"):
        intgrLumi = 27.052 # 4.252  # /fb
    elif (era == "17E"):
        intgrLumi = 9.278  # /fb
    elif (era == "17F"):
        intgrLumi = 13.522  # /fb
    elif (era == "17DEF"):
        intgrLumi = 27.052  # /fb
    else:
        intgrLumi = 41.53  # /fb
        print("No actions yet for this option")


    counter = 0
    for fName in fileList:
        f.append(ROOT.TFile.Open(fName))
        f[counter].cd("plots")
        print(fName)
        if ("dataSEl" in fName) or ("SingleEl" in fName) or ("sel" in fName):
            names = getHistNames(fName)
            for name in names:
                hName = name.replace("h_", "h_dataSEl" + era + "_")
                h_dataSEl[name] = ROOT.gDirectory.Get(name)
                if not h_dataSEl[name]: print('[ERROR]: No histogram "' + name + '" found in ' + fName)
                h_dataSEl[name].SetName(hName)
                h_dataSEl[name].SetDirectory(newDir)
        if ("dataSMu" in fName) or ("SingleMu" in fName) or ("smu" in fName):
            names = getHistNames(fName)
            for name in names:
                hName = name.replace("h_", "h_dataSMu" + era + "_")
                h_dataSMu[name] = ROOT.gDirectory.Get(name)
                if not h_dataSMu[name]: print('[ERROR]: No histogram "' + name + '" found in ' + fName)
                h_dataSMu[name].SetName(hName)
                h_dataSMu[name].SetDirectory(newDir)
        if ("HTMHT" in fName) or ("ht" in fName):
            names = getHistNames(fName)
            for name in names:
                hName = name.replace("h_", "h_dataHTMHT" + era + "_")
                h_dataHTMHT[name] = ROOT.gDirectory.Get(name)
                if not h_dataHTMHT[name]: print('[ERROR]: No histogram "' + name + '" found in ' + fName)
                h_dataHTMHT[name].SetName(hName)
                h_dataHTMHT[name].SetDirectory(newDir)
        if ("TTTT" in fName) or ("tttt" in fName):
            names = getHistNames(fName)
            for name in names:
                hName = name.replace("h_", "h_mcTTTT" + era + "_")
                h_mcTTTT[name] = ROOT.gDirectory.Get(name)
                cross_section = intgrLumi * 9.2  # fb
                initial_NrEvents = 43732445
                normFactor = cross_section / initial_NrEvents
                if not h_mcTTTT[name]: print('[ERROR]: No histogram "' + name + '" found in ' + fName)
                # h_mcTTTT[name].Scale(normFactor)
                h_mcTTTT[name].SetName(hName)
                h_mcTTTT[name].SetDirectory(newDir)
        if ("TTToSemiLep" in fName) or ("ttsemi" in fName):
            names = getHistNames(fName)
            for name in names:
                hName = name.replace("h_", "h_mcTTToSemiLep" + era + "_")
                h_mcTTToSemiLep[name] = ROOT.gDirectory.Get(name)
                cross_section = intgrLumi * 831000 * 0.45  # 365.34
                initial_NrEvents = 43732445
                normFactor = cross_section / initial_NrEvents
                if not h_mcTTToSemiLep[name]: print('[ERROR]: No histogram "' + name + '" found in ' + fName)
                h_mcTTToSemiLep[name].Scale(normFactor)
                h_mcTTToSemiLep[name].SetName(hName)
                h_mcTTToSemiLep[name].SetDirectory(newDir)
        if "ttdilep" in fName:
            names = getHistNames(fName)
            for name in names:
                hName = name.replace("h_", "h_mcTTJetsDiLep" + era + "_")
                h_mcTTJets_DiLep[name] = ROOT.gDirectory.Get(name)
                cross_section = intgrLumi * 83100
                initial_NrEvents = 28380110
                normFactor = cross_section / initial_NrEvents
                if not h_mcTTJets_DiLep[name]: print('[ERROR]: No histogram "' + name + '" found in ' + fName)
                h_mcTTJets_DiLep[name].Scale(normFactor)
                h_mcTTJets_DiLep[name].SetName(hName)
                h_mcTTJets_DiLep[name].SetDirectory(newDir)
        if "tthad" in fName:
            names = getHistNames(fName)
            for name in names:
                hName = name.replace("h_", "h_mcTTHadronic" + era + "_")
                h_mcTTHadronic[name] = ROOT.gDirectory.Get(name)
                cross_section = intgrLumi * 831000 * 0.45  # 327200
                initial_NrEvents = 41646112
                normFactor = cross_section / initial_NrEvents
                if not h_mcTTHadronic[name]: print('[ERROR]: No histogram "' + name + '" found in ' + fName)
                h_mcTTHadronic[name].Scale(normFactor)
                h_mcTTHadronic[name].SetName(hName)
                h_mcTTHadronic[name].SetDirectory(newDir)
        if "ttjet" in fName:
            names = getHistNames(fName)
            for name in names:
                hName = name.replace("h_", "h_mcTTJets" + era + "_")
                h_mcTTJets[name] = ROOT.gDirectory.Get(name)
                cross_section = intgrLumi * 831000
                initial_NrEvents = 8026103
                normFactor = cross_section / initial_NrEvents
                if not h_mcTTJets[name]: print('[ERROR]: No histogram "' + name + '" found in ' + fName)
                # h_mcTTJets[name].Scale(normFactor)
                h_mcTTJets[name].SetName(hName)
                h_mcTTJets[name].SetDirectory(newDir)
        f[counter].Close()
        counter += 1
        h_mcTTTT = rebinHist(h_mcTTTT)
        h_mcTTToSemiLep = rebinHist(h_mcTTToSemiLep)
        h_mcTTJets_DiLep = rebinHist(h_mcTTJets_DiLep)
        h_mcTTHadronic = rebinHist(h_mcTTHadronic)
        h_mcTTJets = rebinHist(h_mcTTJets)
        h_dataHTMHT = rebinHist(h_dataHTMHT)
        h_dataSMu = rebinHist(h_dataSMu)
        h_dataSEl = rebinHist(h_dataSEl)

    return h_mcTTTT, h_mcTTToSemiLep, h_mcTTJets_DiLep, h_mcTTHadronic, h_mcTTJets, h_dataHTMHT, h_dataSMu, h_dataSEl


def findTrigRatio(h1, title, newDir):
    """

    Args:
        h1 (dictionary): dictionary of histograms
        title (string): title given in legend
        newDir (TDirectory):
    Returns:
        h_Out (dictionary): trigger ratio TH1D histogram

    """
    h_TH1DOut = {}
    h_TEffOut = {}

    hltTypes = ["Muon", "Electron", "Jet", "El_CROSS_Jets", "Mu_CROSS_Jets", "El_OR_Jets", "Mu_OR_Jets"]
    channels = ["Mu_", "El_"]
    xAxes = ["HT_", "pt_", "nJet_", "nBJet_", "lepEta_", "lepPhi_"]
    n_count = 0
    for channel in channels:
        for xAxis in xAxes:
            n_count += 1
            histNameDen = "h_" + channel + xAxis + "no-HLT"
            for hlt in hltTypes:
                #if hlt == "Mu_CROSS_Jets": continue # and args.inputLFN == "17B": continue
                if channel == "El_" and "Mu" in hlt: continue
                if channel == "Mu_" and "El" in hlt: continue
                histNameNum = "h_" + channel + xAxis + hlt
                effName = histNameNum.replace("h_", "h_eff")
                effName2 = histNameNum.replace("h_", "h_eff2")
                # hh, tg = histNameNum.split(histNameDen)
                h_TH1DOut[histNameNum] = h1[histNameNum].Clone(effName)
                h_TH1DOut[histNameNum].Sumw2()
                h_TH1DOut[histNameNum].SetStats(0)
                if h_TH1DOut[histNameNum].GetNbinsX() != h1[histNameDen].GetNbinsX():
                    print("%s  %d  %d " % (histNameNum, h_TH1DOut[histNameNum].GetNbinsX(), h1[histNameDen].GetNbinsX()))
                h_TH1DOut[histNameNum].Divide(h1[histNameDen])
                xTitle = h1[histNameDen].GetXaxis().GetTitle()
                xBinWidth = h1[histNameDen].GetXaxis().GetBinWidth(1)
                if "Mu" in histNameDen: 
                    newxTitle = xTitle.replace("Lepton", "Muon")
#                    newxTitle = xTitle.replace("Jet", "Muon")
                elif "El" in histNameDen: 
                    newxTitle = xTitle.replace("Lepton", "Electron")
 #                   newxTitle = xTitle.replace("Jet", "Electron")
                h_TH1DOut[histNameNum].SetTitle(title + ";{0};Trigger Efficiency".format(newxTitle))
                h_TH1DOut[histNameNum].SetDirectory(newDir)
                if not ROOT.TEfficiency.CheckConsistency(h1[histNameNum], h1[histNameDen]):
                    print(histNameNum + " could not get efficiency")
                    continue
                h_TEffOut[histNameNum] = ROOT.TEfficiency(h1[histNameNum], h1[histNameDen])
                h_TEffOut[histNameNum].SetTitle(title + ";{0};Trigger Efficiency".format(newxTitle))
                h_TEffOut[histNameNum].SetName(effName2)

    return h_TH1DOut, h_TEffOut


def scaleFactor(h1, h2, title, era, newDir):
    """

    Args:
        h1: numerator
        h2: denominator
        title (string): title given to legend
        era:
        newDir (TDirectory):
    Returns:

    """
    h_scale = {}
    hNameList = []
    for hName in h1:
        for hName2 in h2:
            if not hName == hName2:
                continue
            # print("{0}   {1} ".format(hName, hName2))
            sfName = hName.replace("h_", "h_sf")
            hNameList.append(hName)
            h_scale[hName] = h1[hName].Clone(sfName)
            # h_scale[hName].Sumw2()
            h_scale[hName].SetStats(0)
            h_scale[hName].Divide(h2[hName2])
            xTitle = h2[hName2].GetXaxis().GetTitle()
            xBinWidth = h2[hName2].GetXaxis().GetBinWidth(1)
            h_scale[hName].SetTitle(title + ";{0};Scale Factors".format(xTitle))
            h_scale[hName].SetDirectory(newDir)

    return h_scale, hNameList


def whatTrig(h_name):
    """

    Args:
        h_name:

    Returns:

    """
    xAxesOptions = ["HT_", "pt_", "nJet", "nBJet"]
    trig = ""
    for xAxisLabel in xAxesOptions:
        if xAxisLabel in h_name:
            hh, trig = h_name.split(xAxisLabel)
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
    # parser.add_argument("-o", "--outputName", default="NoPreTrig", help="Set name of output file")
    parser.add_argument("-o", "--imageName", default="v2_HistFiles/plotImages/", help="Set directory to save images")
    parser.add_argument("-pdf", "--pdfName", default="v2_HistFiles/plotPDFs/", help="Set directory to save pdfs")
    args = parser.parse_args()

    preSelCuts = getFileContents("../myInFiles/preSelectionCuts.txt", True)
    selCriteria = getFileContents("selectionCriteria.txt", True)

    # - Create canvases
    triggerCanvas = ROOT.TCanvas('triggerCanvas', 'Triggers', 800, 800)
    triggerCanvas.SetGrid()

    legString = cmsPlotString(args.inputLFN)  # Create text for legend

    outputSFfile = ROOT.TFile("scaleFactors.root", "recreate")
    outDIR = outputSFfile.mkdir("muChannel_Era" + args.inputLFN)
    # outputSFfile.cd("muChannel")
    # outDIR = ROOT.gDirectory.pwd()
    # eraDIR = outDIR.mkdir("Era_" + args.inputLFN)
    eventDIR = outDIR.mkdir("EventDistributions")
    effDIR = outDIR.mkdir("TriggerEfficiencies")
    sfDIR = outDIR.mkdir("ScaleFactors")
    outDIR.cd()
    # - Get File Names and create histogram dictionaries
    h_mcTTTTs = {}
    h_mcTTToSemiLeps = {}
    h_dataHTMHTs = {}
    h_dataSMus = {}
    h_dataSEls = {}
    # files = findEraRootFiles(path="OutFiles/Histograms_LooseMuInfo_vetoing", era="17DEF", FullPaths=True)
    # h_mcTTTTs, h_mcTTToSemiLeps, h_dataHTMHTs, h_dataSMus, h_dataSEls = getHistograms(files, "17DEF")
    files17B = findEraRootFiles(path=histFilesDir, era="17B", FullPaths=True)
    h_mcTTTTs17B, h_mcTTToSemiLeps17B, h_mcTTJets_DiLeps17B, h_mcTTHadronics17B, h_mcTTJets17B, h_dataHTMHTs17B, h_dataSMus17B, h_dataSEls17B = getHistograms(
        files17B, "17B", eventDIR)
    files17C = findEraRootFiles(path=histFilesDir, era="17C", FullPaths=True)
    h_mcTTTTs17C, h_mcTTToSemiLeps17C, h_mcTTJets_DiLeps17C, h_mcTTHadronics17C, h_mcTTJets17C, h_dataHTMHTs17C, h_dataSMus17C, h_dataSEls17C = getHistograms(
        files17C, "17C", eventDIR)
    files17D = findEraRootFiles(path=histFilesDir, era="17D", FullPaths=True)
    h_mcTTTTs17D, h_mcTTToSemiLeps17D, h_mcTTJets_DiLeps17D, h_mcTTHadronics17D, h_mcTTJets17D, h_dataHTMHTs17D, h_dataSMus17D, h_dataSEls17D = getHistograms(
        files17D, "17D", eventDIR)
    files17E = findEraRootFiles(path=histFilesDir, era="17E", FullPaths=True)
    h_mcTTTTs17E, h_mcTTToSemiLeps17E, h_mcTTJets_DiLeps17E, h_mcTTHadronics17E, h_mcTTJets17E, h_dataHTMHTs17E, h_dataSMus17E, h_dataSEls17E = getHistograms(
        files17E, "17E", eventDIR)
    files17F = findEraRootFiles(path=histFilesDir, era="17F", FullPaths=True)
    h_mcTTTTs17F, h_mcTTToSemiLeps17F, h_mcTTJets_DiLeps17F, h_mcTTHadronics17F, h_mcTTJets17F, h_dataHTMHTs17F, h_dataSMus17F, h_dataSEls17F = getHistograms(
        files17F, "17F", eventDIR)

    eventDIR.cd()

    if args.inputLFN == "17B":
        for hName in h_mcTTToSemiLeps17B:
            h_mcTTTTs[hName] = h_mcTTTTs17B[hName]
            h_mcTTToSemiLeps[hName] = h_mcTTToSemiLeps17B[hName]
            # h_mcTTToSemiLeps[hName].Write(hName)
        for hName in h_dataHTMHTs17B:
            h_dataHTMHTs[hName] = h_dataHTMHTs17B[hName]
            h_dataSMus[hName] = h_dataSMus17B[hName]
            h_dataSEls[hName] = h_dataSEls17B[hName]
            # h_dataHTMHTs[hName].Write(hName)
            # h_dataSMus[hName].Write(hName)
            # h_dataSEls[hName].Write(hName)
    elif args.inputLFN == "17C":
        for hName in h_mcTTToSemiLeps17C:
            h_mcTTTTs[hName] = h_mcTTTTs17C[hName]
            h_mcTTToSemiLeps[hName] = h_mcTTToSemiLeps17C[hName]
            h_dataHTMHTs[hName] = h_dataHTMHTs17C[hName]
            h_dataSMus[hName] = h_dataSMus17C[hName]
            h_dataSEls[hName] = h_dataSEls17C[hName]
            # h_mcTTToSemiLeps[hName].Write(hName)
            # h_dataHTMHTs[hName].Write(hName)
            # h_dataSMus[hName].Write(hName)
            # h_dataSEls[hName].Write(hName)
    else:

        for hname1 in h_dataHTMHTs17D:
            h_mcTTTTs[hname1] = h_mcTTTTs17D[hname1]
            h_mcTTToSemiLeps[hname1] = h_mcTTToSemiLeps17D[hname1]
            h_mcTTToSemiLeps[hname1].Add(h_mcTTJets_DiLeps17D[hname1])
            h_mcTTToSemiLeps[hname1].Add(h_mcTTHadronics17D[hname1])

            # h_mcTTTTs[hname1] = h_mcTTToSemiLeps[hname1]
            # h_mcTTTTs[hname1] = h_mcTTJets17D[hname1]
            # h_mcTTToSemiLeps[hname1] = h_mcTTJets17D[hname1]
            # eventDIR.cd()
            # h_mcTTToSemiLeps[hname1].Write(hname1)
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
            h_mcTTTTs[hname1] = h_dataSMus[hname1]

    #  - Find efficiency ratio histogram dictionaries
    tr_mcTTTT, tr2_mcTTTT = findTrigRatio(h_mcTTTTs, "Four Top MC", effDIR)
    tr_mcTTToSemiLep, tr2_mcTTToSemiLep = findTrigRatio(h_mcTTToSemiLeps, "Top-AntiTop MC", effDIR)
    tr_dataHTMHT, tr2_dataHTMHT = findTrigRatio(h_dataHTMHTs, "HTMHT Data", effDIR)
    tr_dataSMu, tr2_dataSMu = findTrigRatio(h_dataSMus, "Single Muon Data", effDIR)
    tr_dataSEl, tr2_dataSEl = findTrigRatio(h_dataSEls, "Single Electron Data", effDIR)

    # - Find scale factor histogram dictionaries
    effDIR.cd()
    s_HTMHT, hNames = scaleFactor(tr_dataHTMHT, tr_mcTTToSemiLep, "HTMHT Data", args.inputLFN, sfDIR)
    s_dataSMu, hNamesMu = scaleFactor(tr_dataSMu, tr_mcTTToSemiLep, "Single Muon Data", args.inputLFN, sfDIR)
    s_dataSEl, hNamesEl = scaleFactor(tr_dataSEl, tr_mcTTToSemiLep, "Single Electron Data", args.inputLFN, sfDIR)

    #    ROOT.gStyle.SetOptTitle(0)
    #    ROOT.gStyle.SetOptStat(0)

    triggerCanvas.cd(1)
    ltx = TLatex()
    cutInfoPage(ltx, selCriteria, preSelCuts)
    pdfCreator(args, 0, triggerCanvas)

    # - Create text for legend
    # legString = cmsPlotString(arg.inputLFN)
    t1 = ROOT.TPaveText(0.2, 0.95, 0.93, 1, "nbNDC")
    t1.SetFillColorAlpha(0, 0.9)
    t1.SetTextSize(0.03)
    #t1.AddText("#bf{CMS Preliminary}                                #sigma(t#bar{t}) = 831 pb (13TeV)")
    # t1.AddText("#bf{CMS Preliminary}                           #sigma(t#bar{t}t#bar{t}) = 9.2 fb (13TeV)")
    t1.AddText("#bf{CMS Preliminary}          Run2017D-F    27.05 fb^{-1}(13TeV)")
    t2 = ROOT.TPaveText(0.2, 0.95, 0.93, 1, "nbNDC")
    t2.SetFillColorAlpha(0, 0.9)
    t2.SetTextSize(0.03)
    t2.AddText(legString)
    ROOT.gStyle.SetLegendTextSize(0.028)

    hNames.sort()

    # Draw MC TTTT Motivation
    hltTypes = ["Muon", "Electron", "Jet", "El_CROSS_Jets", "Mu_CROSS_Jets", "El_OR_Jets", "Mu_OR_Jets"]
    channels = ["Mu_", "El_"]
    xAxes = ["HT_", "pt_", "nJet_", "nBJet_", "lepEta_", "lepPhi_"] 
    cv3 = [None] * 30
    cv4 = [None] * 30
    legend = [None] * 30
    legend2 = [None] * 30
    n_count = 0
    for channel in channels:
        for xAxis in xAxes:
            n_count += 1
            print(n_count)
            cv3[n_count] = triggerCanvas.cd(1)
            if "lep" in xAxis: legend[n_count] = ROOT.TLegend(0.55, 0.16, 0.95, 0.58)
            else: legend[n_count] = ROOT.TLegend(0.55, 0.53, 0.95, 0.95)
            histName = "h_" + channel + xAxis + "no-HLT"
            # h_mcTTTTs[histName].Scale(1)
            for i in range(0, 17):
                binWidth = h_mcTTTTs[histName].GetXaxis().GetBinWidth(i)
                binContent = h_mcTTTTs[histName].GetBinContent(i)
                newBinContent = round(binContent / binWidth)
                h_mcTTTTs[histName].SetBinContent(i, newBinContent)
            #h_mcTTTTs[histName].SetLineWidth(3)
            h_mcTTTTs[histName].SetLineColor(1)
            h_mcTTTTs[histName].GetXaxis().SetTitleOffset(1.4)
            xTitle = h_mcTTTTs[histName].GetXaxis().GetTitle()
            if "Mu" in histName: 
                newxTitle = xTitle.replace("Lepton", "Muon")
                if "lep" in xAxis: newxTitle = xTitle.replace("Jet", "Muon")
                h_mcTTTTs[histName].GetXaxis().SetTitle(newxTitle)
            elif "El" in histName: 
                newxTitle = xTitle.replace("Lepton", "Electron")
                if "lep" in xAxis: newxTitle = xTitle.replace("Jet", "Electron")
                h_mcTTTTs[histName].GetXaxis().SetTitle(newxTitle)
            # h_mcTTTTs[histName].GetYaxis().SetTitleOffset(1.4)
            h_mcTTTTs[histName].SetLabelFont(42,"x")
            h_mcTTTTs[histName].SetTitleFont(42,"x")
            h_mcTTTTs[histName].SetLabelFont(42,"y")
            h_mcTTTTs[histName].SetTitleFont(42,"y")
            h_mcTTTTs[histName].SetLabelFont(42,"z")
            h_mcTTTTs[histName].SetTitleFont(42,"z")
            h_mcTTTTs[histName].SetLabelSize(0.04,"x")
            h_mcTTTTs[histName].SetTitleSize(0.04,"x")
            h_mcTTTTs[histName].SetLabelSize(0.04,"y")
            h_mcTTTTs[histName].SetTitleSize(0.04,"y")
            h_mcTTTTs[histName].Draw("hist")
            histEntries = h_mcTTTTs[histName].GetEntries()
            if xAxis == "nBJet_": h_mcTTTTs[histName].GetXaxis().SetRangeUser(2, 10)
            elif xAxis == "nJet_": h_mcTTTTs[histName].GetXaxis().SetRangeUser(6, 20)
            elif xAxis == "HT_": h_mcTTTTs[histName].GetXaxis().SetRangeUser(400, 3000)
            legEntry = "Baseline (%d)" % histEntries
            legend[n_count].AddEntry(histName, legEntry, 'l')
            colourL = 2
            for hlt in hltTypes:
                if hlt == "Mu_CROSS_Jets" and args.inputLFN == "17B": continue
                if (channel == "El_") and ("Mu" in hlt): continue
                if (channel == "Mu_") and ("El" in hlt): continue
                histName = "h_" + channel + xAxis + hlt
                for i in range(0, 17):
                    binWidth = h_mcTTTTs[histName].GetXaxis().GetBinWidth(i)
                    binContent = h_mcTTTTs[histName].GetBinContent(i)
                    newBinContent = round(binContent / binWidth)
                    h_mcTTTTs[histName].SetBinContent(i, newBinContent)
                h_mcTTTTs[histName].SetLineColor(colourL)
                # if "Mu_OR_Jets" not in hlt: 
                h_mcTTTTs[histName].Draw("hist same")
                histEntries = h_mcTTTTs[histName].GetEntries()
                legEntry = hlt.replace("El_", "e^{#pm} ")
                legEntry = legEntry.replace("Mu_", "#mu^{#pm} ")
                legEntry = legEntry.replace("Jets", "")
                legEntry = legEntry.replace("Jet", "Hadronic")
                legEntry = legEntry.replace("Electron", "e^{#pm} ")
                legEntry = legEntry.replace("Muon", "#mu^{#pm}  ")
                legEntry = legEntry.replace("_", " ")
                legEntry = legEntry + " HLT (%d)" % histEntries
                #legend[n_count].AddEntry(histName, legEntry, 'l')
                legend[n_count].AddEntry(h_mcTTTTs[histName], legEntry, 'l')
                colourL += 2
            t1.Draw("same")
            #legend[n_count].SetHeader("#bf{t#bar{t} inclusive MC after:}", "C")
            #legend[n_count].SetHeader("#bf{t#bar{t}t#bar{t} inclusive MC after:}", "C")
            legend[n_count].SetHeader("#bf{SingleMuon Samples after:}", "C")
            legend[n_count].Draw("same")
            triggerCanvas.Print(args.imageName + channel + xAxis + "ttttEv.png", "png")

            cv4[n_count] = triggerCanvas.cd(1)
            colourM = 2
            # ROOT.gStyle.SetErrorX(0.0001)
            legend2[n_count] = ROOT.TLegend(0.5, 0.16, 0.95, 0.5)
            nhlt = 0
            for hlt in hltTypes:
                if hlt == "Mu_CROSS_Jets" and args.inputLFN == "17B": continue
                if (channel == "El_") and ("Mu" in hlt): continue
                if (channel == "Mu_") and ("El" in hlt): continue
                histName = "h_" + channel + xAxis + hlt
                tr2_mcTTTT[histName].SetMarkerColor(colourM)
                tr2_mcTTTT[histName].SetLineColor(colourM)
                if nhlt == 0:
                    tr2_mcTTTT[histName].Draw()
                    cv4[n_count].Update()
                    graph1 = tr2_mcTTTT[histName].GetPaintedGraph()
                    graph1.SetMinimum(0)
                    graph1.SetMaximum(1.2)
                    # graph1.GetXaxis().SetLabelSize(0.05)
                    cv4[n_count].Update()
                    histEntries = h_mcTTTTs[histName].GetEntries()                    
                    nhlt += 1
                else:
                    tr2_mcTTTT[histName].Draw("same")
                    histEntries = h_mcTTTTs[histName].GetEntries()
                effname = histName.replace("h_", "h_eff2")
                legEntry = hlt.replace("El_", "e^{#pm} ")
                legEntry = legEntry.replace("Mu_", "#mu^{#pm} ")
                legEntry = legEntry.replace("Jets", "")
                legEntry = legEntry.replace("Jet", "Hadronic")
                legEntry = legEntry.replace("Electron", "e^{#pm}  ")
                legEntry = legEntry.replace("Muon", "#mu^{#pm}  ")
                legEntry = legEntry.replace("_", " ")
                legEntry = legEntry + " HLT (%d)" % histEntries
                #legend2[n_count].AddEntry(effname, legEntry, "lep")
                legend2[n_count].AddEntry(h_mcTTTTs[histName], legEntry, "lep")
                colourM += 2
            t1.Draw("same")
            #legend2[n_count].SetHeader("#bf{t#bar{t} inclusive MC after:}", "C")
            # legend2[n_count].SetHeader("#bf{t#bar{t}t#bar{t} inclusive MC after:}", "C")
            legend2[n_count].SetHeader("#bf{SingleMuon Samples after:}", "C")
            legend2[n_count].Draw("same")
            triggerCanvas.Print(args.imageName + channel + xAxis + "ttttEf.png", "png")

    cv0 = [None] * 30
    cv1 = [None] * 30
    cv2 = [None] * 30
    legend3 = [None] * 30
    legend4 = [None] * 30
    legend5 = [None] * 30
    n_count = 0
    for hn, hName in enumerate(hNames):
        # - Draw trigger hists
        trg = whatTrig(hName)
        era = args.inputLFN
        ##############################################
        #  Draw event distributions MC Data Compare  #
        ##############################################
        if "_OR_" not in trg: continue
        n_count += 1
        print(">>>>>>>  {0}".format(hName))
        cv0[n_count] = triggerCanvas.cd(1)
        legend3[n_count] = ROOT.TLegend(0.55, 0.55, 0.95, 0.95)
        for i in range(0, 17):
            binWidth = h_mcTTToSemiLeps[hName].GetXaxis().GetBinWidth(i)
            binContent = h_mcTTToSemiLeps[hName].GetBinContent(i)
            newBinContent = round(binContent / binWidth)
            h_mcTTToSemiLeps[hName].SetBinContent(i, newBinContent)
            binContent = h_dataHTMHTs[hName].GetBinContent(i)
            newBinContent = round(binContent / binWidth)
            h_dataHTMHTs[hName].SetBinContent(i, newBinContent)
            binContent = h_dataSMus[hName].GetBinContent(i)
            newBinContent = round(binContent / binWidth)
            h_dataSMus[hName].SetBinContent(i, newBinContent)
            binContent = h_dataSEls[hName].GetBinContent(i)
            newBinContent = round(binContent / binWidth)
            h_dataSEls[hName].SetBinContent(i, newBinContent)
        maxYs = getMaxY([h_mcTTToSemiLeps[hName], h_dataSMus[hName], h_dataHTMHTs[hName], h_dataSEls[hName]])
        h_mcTTToSemiLeps[hName].SetMaximum(maxYs + 100)
        h_mcTTToSemiLeps[hName].SetLineColor(1)
        h_mcTTToSemiLeps[hName].Draw("hist")
        histEntries = h_mcTTToSemiLeps[hName].GetEntries()
        h_mcTTToSemiLeps[hName].SetTitle("t#bar{t} pair MC (%d)" % histEntries)
        newName = h_mcTTToSemiLeps[hName].GetName()
        print(newName)
        legend3[n_count].AddEntry(newName, "t#bar{t} pair MC (%d)" % histEntries, 'l')

        h_dataHTMHTs[hName].SetLineColor(4)
        h_dataHTMHTs[hName].SetMarkerStyle(20)
        h_dataHTMHTs[hName].SetMarkerColor(4)
        h_dataHTMHTs[hName].SetMarkerSize(1.2)
        h_dataHTMHTs[hName].Draw('E0 X0 same')
        histEntries = h_dataHTMHTs[hName].GetEntries()
        h_dataHTMHTs[hName].SetTitle("HTMHT Data (%d)" % histEntries)
        newName = h_dataHTMHTs[hName].GetName()
        legend3[n_count].AddEntry(newName, "HTMHT Data (%d)" % histEntries, 'lep')

        if hName.find("Mu") != -1:
            legend3[n_count].SetHeader("#bf{#mu^{#pm} + jets  selection}", "C")
            h_dataSMus[hName].SetLineColor(2)
            h_dataSMus[hName].SetMarkerStyle(20)
            h_dataSMus[hName].SetMarkerColor(2)
            h_dataSMus[hName].SetMarkerSize(1.2)
            h_dataSMus[hName].Draw('E0 X0 same')
            histEntries = h_dataSMus[hName].GetEntries()
            h_dataSMus[hName].SetTitle("Single Muon Data (%d) " % histEntries)
            newName = h_dataSMus[hName].GetName()
            legend3[n_count].AddEntry(newName, "Single Muon Data (%d) " % histEntries, 'lep')
        elif hName.find("El") != -1: 
            legend3[n_count].SetHeader("#bf{e^{#pm} + jets  selection}", "C")
            h_dataSEls[hName].SetLineColor(2)
            h_dataSEls[hName].SetMarkerStyle(20)
            h_dataSEls[hName].SetMarkerColor(2)
            h_dataSEls[hName].SetMarkerSize(1.2)
            h_dataSEls[hName].Draw('E0 X0 same')
            histEntries = h_dataSEls[hName].GetEntries()
            h_dataSEls[hName].SetTitle("Single Electron Data (%d)" % histEntries)
            newName = h_dataSEls[hName].GetName()
            legend3[n_count].AddEntry(newName, "Single Electron Data (%d)" % histEntries, 'lep')

        t2.Draw("same")
        legend3[n_count].Draw("same")
        pdfCreator(args, 1, triggerCanvas)
        triggerCanvas.Print(args.imageName + "{0}events.png".format(hName), "png")

        ####################################
        # - Draw trigger efficiency hists  #
        ####################################
        cv1[n_count] = triggerCanvas.cd(1)
        legend4[n_count] = ROOT.TLegend(0.5, 0.16, 0.95, 0.5)
        tr2_mcTTToSemiLep[hName].SetLineColor(1)
        tr2_mcTTToSemiLep[hName].Draw()
        newName = tr2_mcTTToSemiLep[hName].GetName()
        legend4[n_count].AddEntry(newName, "t#bar{t} pair MC", 'lep')
        cv1[n_count].Update()
        graph1 = tr2_mcTTToSemiLep[hName].GetPaintedGraph()
        graph1.SetMinimum(0.7)
        graph1.SetMaximum(1.1)
        #cv1[n_count].SetLogy(1)
        cv1[n_count].Update()

        if "Mu" in hName:
            legend4[n_count].SetHeader("#bf{#mu^{#pm} + jets  selection}", "C")
            tr2_dataSMu[hName].SetLineColor(2)
            tr2_dataSMu[hName].SetMarkerStyle(20)
            tr2_dataSMu[hName].SetMarkerColor(2)
            tr2_dataSMu[hName].SetMarkerSize(1.2)
            tr2_dataSMu[hName].Draw('same')
            newName = tr2_dataSMu[hName].GetName()
            #legend4[n_count].AddEntry(newName, "Single Muon Data", 'lep')
            legend4[n_count].AddEntry(tr2_dataSMu[hName], "Single Muon Data", 'lep')
        elif "El" in hName:
            legend4[n_count].SetHeader("#bf{e^{#pm} + jets  selection}", "C")
            tr2_dataSEl[hName].SetLineColor(2)
            tr2_dataSEl[hName].SetMarkerStyle(20)
            tr2_dataSEl[hName].SetMarkerColor(2)
            tr2_dataSEl[hName].SetMarkerSize(1.2)
            tr2_dataSEl[hName].Draw('same')
            tr2_dataSEl[hName].SetMarkerStyle(20)
            tr2_dataSEl[hName].SetMarkerColor(2)
            tr2_dataSEl[hName].SetMarkerSize(1.2)
            tr2_dataSEl[hName].SetLineColor(2)
            newName = tr2_dataSEl[hName].GetName()
            #legend4[n_count].AddEntry(newName, "Single Electron Data", 'lep')
            legend4[n_count].AddEntry(tr2_dataSEl[hName], "Single Electron Data", 'lep')

        tr2_dataHTMHT[hName].SetLineColor(4)
        tr2_dataHTMHT[hName].SetMarkerStyle(20)
        tr2_dataHTMHT[hName].SetMarkerColor(4)
        tr2_dataHTMHT[hName].SetMarkerSize(1.2)
        tr2_dataHTMHT[hName].Draw('same')
        tr2_dataHTMHT[hName].SetLineColor(4)
        tr2_dataHTMHT[hName].SetMarkerStyle(20)
        tr2_dataHTMHT[hName].SetMarkerColor(4)
        tr2_dataHTMHT[hName].SetMarkerSize(1.2)
        newName = tr2_dataHTMHT[hName].GetName()
        #legend4[n_count].AddEntry(newName, "HTMHT Data", 'lep')
        legend4[n_count].AddEntry(tr2_dataHTMHT[hName], "HTMHT Data", 'lep')

        t2.Draw("same")
        legend4[n_count].Draw("same")
        pdfCreator(args, 1, triggerCanvas)
        triggerCanvas.Print(args.imageName + "{0}_teff.png".format(hName), "png")

        ##############################
        # - Draw scale factor hists  #
        ##############################
        cv2[n_count] = triggerCanvas.cd(1)
        legend5[n_count] = ROOT.TLegend(0.5, 0.16, 0.95, 0.5)
        s_HTMHT[hName].SetLineColor(4)
        s_dataSMu[hName].SetMarkerStyle(20)
        s_dataSMu[hName].SetMarkerColor(2)
        s_dataSMu[hName].SetMarkerSize(1.2)
        #s_HTMHT[hName].Draw('E0 X0')
        newName = s_HTMHT[hName].GetName()
        #legend5[n_count].AddEntry(newName, "HTMHT Data", 'lep')
        s_HTMHT[hName].SetMinimum(0.7)
        s_HTMHT[hName].SetMaximum(1.1)
        if "Mu" in hName:
            legend5[n_count].SetHeader("#bf{#mu^{#pm} + jets  selection}", "C")
            s_dataSMu[hName].SetLineColor(2)
            s_dataSMu[hName].SetMarkerStyle(20)
            s_dataSMu[hName].SetMarkerColor(2)
            s_dataSMu[hName].SetMarkerSize(1.2)
            s_dataSMu[hName].Draw('E0 X0')
            newName = s_dataSMu[hName].GetName()
            legend5[n_count].AddEntry(newName, "Single Muon Data", 'lep')
        elif "El" in hName:
            legend5[n_count].SetHeader("#bf{e^{#pm} + jets  selection}", "C")
            s_dataSEl[hName].SetLineColor(2)
            s_dataSEl[hName].SetMarkerStyle(20)
            s_dataSEl[hName].SetMarkerColor(2)
            s_dataSEl[hName].SetMarkerSize(1.2)
            s_dataSEl[hName].Draw('E0 X0')
            newName = s_dataSEl[hName].GetName()
            legend5[n_count].AddEntry(newName, "Single Electron Data", 'lep')
        t2.Draw("same")
        legend5[n_count].Draw("same")
        pdfCreator(args, 1, triggerCanvas)
        triggerCanvas.Print(args.imageName + "{0}_sf.png".format(hName), "png")

        eventDIR.cd()
        mcName = hName.replace("h_", "h_mcTTToSemiLep_")
        h_mcTTToSemiLeps[hName].Write(mcName)
        htName = hName.replace("h_", "h_dataHTMHT_")
        h_dataHTMHTs[hName].Write(htName)
        muName = hName.replace("h_", "h_dataMu_")
        h_dataSMus[hName].Write(muName)
        eleName = hName.replace("h_", "h_dataEle_")
        h_dataSEls[hName].Write(eleName)

        effDIR.cd()
        tr_mcTTToSemiLep[hName].Write(mcName)
        tr_dataHTMHT[hName].Write(htName)
        tr_dataSMu[hName].Write(muName)
        tr_dataSEl[hName].Write(eleName)

        sfDIR.cd()
        s_HTMHT[hName].Write(htName)
        s_dataSMu[hName].Write(muName)
        s_dataSEl[hName].Write(eleName)
    # cv1 = triggerCanvas.cd(1)
    # count = 0
    # for hn, hName in enumerate(hNames):
    #     if "HT" not in hName: continue
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
    triggerCanvas.cd(1)
    t3 = ROOT.TPaveText(0., 0., 1., 1., "nbNDC")
    t3.SetFillColor(0)
    t3.SetTextSize(0.03)
    t3.AddText("That's all folks")
    t3.Draw()
    pdfCreator(args, 2, triggerCanvas)

    # outputSFfile.Write()
    outputSFfile.Close()


if __name__ == '__main__':
    main()
