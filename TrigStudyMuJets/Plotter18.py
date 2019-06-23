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

histFilesDir = "/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/TrigStudyMuJets/v5_HistFiles/"
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
    if args == "18A":
        legStr = "#bf{CMS Preliminary}            Run2018A      14.00 fb^{-1} (13TeV)"
    if args == "18B":
        legStr = "#bf{CMS Preliminary}            Run2018B      7.10 fb^{-1} (13TeV)"
    elif args == "18C":
        legStr = "#bf{CMS Preliminary}            Run2018C      6.94 fb^{-1} (13TeV)"
    elif args == "18D":
        legStr = "#bf{CMS Preliminary}            Run2018D      31.93 fb^{-1} (13TeV)"
    elif args == "18AB":
        legStr = "#bf{CMS Preliminary}            Run2018A-B    21.10 fb^{-1} (13TeV)"
    elif args == "18CD":
        legStr = "#bf{CMS Preliminary}            Run2018C-D    38.87 fb^{-1} (13TeV)"
    elif args == "all":
        legStr = "#bf{CMS Preliminary}           All Run2018    41.53 fb^{-1} (13TeV)"
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
    # if era == "17DEF": era = "17D"
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
    trigList = getFileContents("../myInFiles/2018trigList.txt", True)

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


def rebinHist(hIn, dirName):
    """
    Args:
       hIn: Input histogram List
       htype: string describing the type of sample
    Returns:
       hOut: Output histogram List
    """
    muonpT_rebin = numpy.array(
        (0., 10., 20., 22., 24., 26., 28., 30., 35., 40., 50., 75., 100., 125., 150., 200., 300.))
    ht_rebin = numpy.array(
        (0., 100., 200., 220., 240., 260., 280., 300., 350., 400., 500., 750., 1000., 1250., 1500., 2000., 3000.))

    hOut = {}
    #print(hOut)
    #print(hType)
    for hName in hIn:
        # if hIn[hName].GetEntries() == 0: continue
        histName = hIn[hName].GetName()
        if "HT_" in hName:
            print(hName)
            hOut[hName] = hIn[hName].Rebin(16, histName, ht_rebin)
            #newYtitle = hOut[hName].GetYaxis().GetTitle()  + " per GeVc^{-1}"
            #hOut[hName].GetYaxis().SetTitle(newYtitle)
            # print(hType + hOut[hName].GetName() + hName)
        elif "pt_" in hName:
            hOut[hName] = hIn[hName].Rebin(16, histName, muonpT_rebin)
            #newYtitle = hOut[hName].GetYaxis().GetTitle()  + " per GeVc^{-1}"
            #hOut[hName].GetYaxis().SetTitle(newYtitle)
        else:
            hOut[hName] = hIn[hName]
        hOut[hName].SetDirectory(dirName)
    #print(hOut["h_El_HT_El_OR_Jets"].GetName())
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

    if (era == "18A"):
        intgrLumi = 14.00  # /fb
    elif era == "18B":
        intgrLumi = 7.10  # /fb
    elif era == "18C":
        intgrLumi = 6.94  # /fb
    elif (era == "18D"):
        intgrLumi = 31.93 # /fb
    elif (era == "18AB"):
        intgrLumi = 21.10 # /fb
    elif (era == "18CD"):
        intgrLumi = 38.87 # /fb
    else:
        intgrLumi = 59.69  # /fb
        print("No actions yet for this option")


    counter = 0
    for fName in fileList:
        f.append(ROOT.TFile.Open(fName))
        f[counter].cd("plots")
        print(fName)
        print(era)
        if ("dataSEl" in fName) or ("SingleEl" in fName) or ("sel18" in fName):
            names = getHistNames(fName)
            for name in names:
                hName = name.replace("h_", "h_dataSEl" + era + "_")
                h_dataSEl[name] = ROOT.gDirectory.Get(name)
                if not h_dataSEl[name]: print('[ERROR]: No histogram "' + name + '" found in ' + fName)
                h_dataSEl[name].SetName(hName)
                h_dataSEl[name].SetDirectory(newDir)
            h_dataSEl = rebinHist(h_dataSEl, newDir)
        elif ("dataSMu" in fName) or ("SingleMu" in fName) or ("smu" in fName):
            names = getHistNames(fName)
            for name in names:
                hName = name.replace("h_", "h_dataSMu" + era + "_")
                h_dataSMu[name] = ROOT.gDirectory.Get(name)
                if not h_dataSMu[name]: print('[ERROR]: No histogram "' + name + '" found in ' + fName)
                h_dataSMu[name].SetName(hName)
                h_dataSMu[name].SetDirectory(newDir)
            h_dataSMu = rebinHist(h_dataSMu, newDir)
        elif ("HTMHT" in fName) or ("ht" in fName):
            names = getHistNames(fName)
            for name in names:
                hName = name.replace("h_", "h_dataHTMHT" + era + "_")
                h_dataHTMHT[name] = ROOT.gDirectory.Get(name)
                if not h_dataHTMHT[name]: print('[ERROR]: No histogram "' + name + '" found in ' + fName)
                h_dataHTMHT[name].SetName(hName)
                h_dataHTMHT[name].SetDirectory(newDir)
            h_dataHTMHT = rebinHist(h_dataHTMHT, newDir)
        elif ("TTTT" in fName) or ("tttt" in fName):
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
            h_mcTTTT = rebinHist(h_mcTTTT, newDir)
        elif ("TTToSemiLep" in fName) or ("ttsemi" in fName):
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
            h_mcTTToSemiLep = rebinHist(h_mcTTToSemiLep, newDir)
        elif "ttdilep" in fName:
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
            h_mcTTJets_DiLep = rebinHist(h_mcTTJets_DiLep, newDir)
        elif "tthad" in fName:
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
            h_mcTTHadronic = rebinHist(h_mcTTHadronic, newDir)
        elif "ttjet" in fName:
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
            h_mcTTJets = rebinHist(h_mcTTJets, newDir)
        f[counter].Close()
        counter += 1
        #if ("TTToSemiLep" in fName) or ("ttsemi" in fName): print(h_mcTTToSemiLep["h_El_HT_El_OR_Jets"].GetName())

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

    hltTypes = ["Muon", "Electron", "Jet", "El_CROSS_Jets", "El_OR_Jets", "Mu_OR_Jets", "Jet2", "El_OR_Jets2", "Mu_OR_Jets2"]
    channels = ["Mu_", "El_"]
    xAxes = ["HT_", "pt_", "nJet_", "nBJet_", "lepEta_", "lepPhi_"]
    n_count = 0
    for channel in channels:
        for xAxis in xAxes:
            n_count += 1
            histNameDen = "h_" + channel + xAxis + "no-HLT"
            for hlt in hltTypes:
                #if hlt == "Mu_CROSS_Jets": continue #  and "18B" in title and args.inputLFN == "18B": continue
                if channel == "El_" and "Mu" in hlt: continue
                if channel == "Mu_" and "El" in hlt: continue
                histNameNum = "h_" + channel + xAxis + hlt
                effName = histNameNum.replace("h_", "h_eff")
                effName2 = histNameNum.replace("h_", "h_eff2")
                # hh, tg = histNameNum.split(histNameDen)
                if h1[histNameNum].GetEntries() == 0: continue
                h_TH1DOut[histNameNum] = h1[histNameNum].Clone(effName)
                h_TH1DOut[histNameNum].Sumw2()
                h_TH1DOut[histNameNum].SetStats(0)
                if h_TH1DOut[histNameNum].GetNbinsX() != h1[histNameDen].GetNbinsX():
                    print("%s  %d  %d " % (histNameNum, h_TH1DOut[histNameNum].GetNbinsX(), h1[histNameDen].GetNbinsX()))
                print(histNameNum)
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
            if (hName2[-3:] == "Jet" or hName2[-7:] == "OR_Jets"): hName2 = hName2 + "2"
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
    xAxesOptions = ["HT_", "pt_", "nJet", "nBJet", "lepEta", "lepPhi"]
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
    parser.add_argument("-f", "--inputLFN", choices=["18A", "18B", "18C", "18D", "18AB", "18CD", "all"],
                        default="D", help="Set era in 2018 to be checked")
    parser.add_argument("-o", "--outputName", default="unknown", help="Set name of output file")
    parser.add_argument("-i", "--imageName", default="v5_HistFiles/plotImages/", help="Set directory to save images")
    parser.add_argument("-pdf", "--pdfName", default="v5_HistFiles/plotPDFs/", help="Set directory to save pdfs")
    args = parser.parse_args()

    preSelCuts = getFileContents("../myInFiles/preSelectionCuts.txt", True)
    selCriteria = getFileContents("selectionCriteria.txt", True)

    era = args.inputLFN
    if era == "18A":
        runName = "RunII 2018A"
        inLumi = "14.00"  # /fb
    elif era == "18B":
        runName = "RunII 2018B"
        inLumi = "7.10"  # /fb
    elif era == "18C":
        runName = "RunII 2018C"
        inLumi = "6.94"  # /fb
    elif (era == "18D"):
        runName = "RunII 2018D"
        inLumi = "31.93" # /fb
    elif (era == "18AB"):
        runName = "RunII 2018A-B"
        inLumi = "21.10" # /fb
    elif (era == "18CD"):
        runName = "RunII 2018C-D"
        inLumi = "38.87" # /fb
    else:
        inLumi = "41.53"  # /fb

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
    #h_mcTTTTs18AB = {}
    #h_mcTTJets18AB = {}
    #h_mcTTToHads18AB = {}
    #h_mcTTToSemiLeps18AB = {}
    #h_mcTTJets_Dileps18AB = {}
    h_dataHTMHTs18AB = {}
    h_dataSMus18AB = {}
    h_dataSEls18AB = {}
    #h_mcTTTTs18CD = {}
    #h_mcTTJets18CD = {}
    #h_mcTTToHads18CD = {}
    #h_mcTTToSemiLeps18CD = {}
    #h_mcTTJets_Dileps18CD = {}
    h_dataHTMHTs18CD = {}
    h_dataSMus18CD = {}
    h_dataSEls18CD = {}
    files18A = findEraRootFiles(path=histFilesDir, era="18A", FullPaths=True)
    h_mcTTTTs18A, h_mcTTToSemiLeps18A, h_mcTTJets_DiLeps18A, h_mcTTHadronics18A, h_mcTTJets18A, h_dataHTMHTs18A, h_dataSMus18A, h_dataSEls18A = getHistograms(
        files18A, "18A", eventDIR)
    files18B = findEraRootFiles(path=histFilesDir, era="18B", FullPaths=True)
    h_mcTTTTs18B, h_mcTTToSemiLeps18B, h_mcTTJets_DiLeps18B, h_mcTTHadronics18B, h_mcTTJets18B, h_dataHTMHTs18B, h_dataSMus18B, h_dataSEls18B = getHistograms(
        files18B, "18B", eventDIR)
    files18C = findEraRootFiles(path=histFilesDir, era="18C", FullPaths=True)
    h_mcTTTTs18C, h_mcTTToSemiLeps18C, h_mcTTJets_DiLeps18C, h_mcTTHadronics18C, h_mcTTJets18C, h_dataHTMHTs18C, h_dataSMus18C, h_dataSEls18C = getHistograms(
        files18C, "18C", eventDIR)
    files18D = findEraRootFiles(path=histFilesDir, era="18D", FullPaths=True)
    h_mcTTTTs18D, h_mcTTToSemiLeps18D, h_mcTTJets_DiLeps18D, h_mcTTHadronics18D, h_mcTTJets18D, h_dataHTMHTs18D, h_dataSMus18D, h_dataSEls18D = getHistograms(
        files18D, "18D", eventDIR)

    #print(h_mcTTToSemiLeps18B["h_El_HT_El_OR_Jets"].GetName())

    eventDIR.cd()

    h_mcTTTTs = h_mcTTTTs18A
    h_mcTTJets = h_mcTTJets18A
    if args.outputName == "ttsemi": h_HLTcompare = h_mcTTToSemiLepsA
    elif args.outputName == "ttjets": h_HLTcompare = h_mcTTJets18A
    elif args.outputName == "smu": h_HLTcompare = h_dataSMus18A
    elif args.outputName == "sel": h_HLTcompare = h_dataSElsA
    elif args.outputName == "ht": h_HLTcompare = h_dataHTMHTsA
    else: h_HLTcompare = h_mcTTTTs18A
    #if args.inputLFN == "18AB":
    for hname1 in h_dataHTMHTs18A:
        # h_mcTTJets[hname1] = h_mcTTToSemiLeps18D[hname1]
        # h_mcTTJets[hname1].Add(h_mcTTJets_DiLeps18D[hname1])
        # h_mcTTJets[hname1].Add(h_mcTTHadronics18D[hname1])
        # eventDIR.cd()
        # h_mcTTJets[hname1].Write(hname1)
        for hname2 in h_dataHTMHTs18D:
            if hname1 == hname2:
                h_dataHTMHTs18AB[hname1] = h_dataHTMHTs18A[hname1]
                h_dataSMus18AB[hname1] = h_dataSMus18A[hname1]
                h_dataSEls18AB[hname1] = h_dataSEls18A[hname1]
                h_dataHTMHTs18AB[hname1].Add(h_dataHTMHTs18B[hname1])
                h_dataSMus18AB[hname1].Add(h_dataSMus18B[hname1])
                h_dataSEls18AB[hname1].Add(h_dataSEls18B[hname1])
    # elif args.inputLFN == "18CD":
    for hname1 in h_dataHTMHTs18C:
        # h_mcTTJetsCD[hname1] = h_mcTTToSemiLeps18D[hname1]
        # h_mcTTJetsCD[hname1].Add(h_mcTTJets_DiLeps18D[hname1])
        # h_mcTTJetsCD[hname1].Add(h_mcTTHadronics18D[hname1])
        # eventDIR.cd()
        # h_mcTTJets[hname1].Write(hname1)
        for hname2 in h_dataHTMHTs18D:
            if hname1 == hname2:
                h_dataHTMHTs18CD[hname1] = h_dataHTMHTs18C[hname1]
                h_dataSMus18CD[hname1] = h_dataSMus18C[hname1]
                h_dataSEls18CD[hname1] = h_dataSEls18C[hname1]
                h_dataHTMHTs18CD[hname1].Add(h_dataHTMHTs18D[hname1])
                h_dataSMus18CD[hname1].Add(h_dataSMus18D[hname1])
                h_dataSEls18CD[hname1].Add(h_dataSEls18D[hname1])

    #  - Find efficiency ratio histogram dictionaries
    tr_HLTcompare, tr2_HLTcompare = findTrigRatio(h_HLTcompare, "Four Top MC", effDIR)
    tr_mcTTJet, tr2_mcTTJet = findTrigRatio(h_mcTTJets18A, "Top-AntiTop MC", effDIR)

    tr_dataHTMHT_AB, tr2_dataHTMHT_AB = findTrigRatio(h_dataHTMHTs18AB, "HTMHT Data 18AB", effDIR)
    tr_dataSMu_AB, tr2_dataSMu_AB = findTrigRatio(h_dataSMus18AB, "Single Muon Data 18AB", effDIR)
    tr_dataSEl_AB, tr2_dataSEl_AB = findTrigRatio(h_dataSEls18AB, "Single Electron Data 18AB", effDIR)

    tr_dataHTMHT_CD, tr2_dataHTMHT_CD = findTrigRatio(h_dataHTMHTs18CD, "HTMHT Data", effDIR)
    tr_dataSMu_CD, tr2_dataSMu_CD = findTrigRatio(h_dataSMus18CD, "Single Muon Data", effDIR)
    tr_dataSEl_CD, tr2_dataSEl_CD = findTrigRatio(h_dataSEls18CD, "Single Electron Data", effDIR)

    # - Find scale factor histogram dictionaries
    effDIR.cd()
    s_HTMHT_AB, hNames_AB = scaleFactor(tr_dataHTMHT_AB, tr_mcTTJet, "HTMHT Data", args.inputLFN, sfDIR)
    s_dataSMu_AB, hNamesMu_AB = scaleFactor(tr_dataSMu_AB, tr_mcTTJet, "Single Muon Data", args.inputLFN, sfDIR)
    s_dataSEl_AB, hNamesEl_AB = scaleFactor(tr_dataSEl_AB, tr_mcTTJet, "Single Electron Data", args.inputLFN, sfDIR)

    s_HTMHT_CD, hNames = scaleFactor(tr_dataHTMHT_CD, tr_mcTTJet, "HTMHT Data", args.inputLFN, sfDIR)
    s_dataSMu_CD, hNamesMu_CD = scaleFactor(tr_dataSMu_CD, tr_mcTTJet, "Single Muon Data", args.inputLFN, sfDIR)
    s_dataSEl_CD, hNamesEl_CD = scaleFactor(tr_dataSEl_CD, tr_mcTTJet, "Single Electron Data", args.inputLFN, sfDIR)

    if args.inputLFN == "18AB":
        h_dataHTMHTs = h_dataHTMHTs18AB
        h_dataSMus = h_dataSMus18AB
        h_dataSEls = h_dataSEls18AB
    elif args.inputLFN == "18CD":
        h_dataHTMHTs = h_dataHTMHTs18CD
        h_dataSMus = h_dataSMus18CD
        h_dataSEls = h_dataSEls18CD
    else:
        print("no era option set")
        return 0

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
    if args.outputName == "ttsemi": t1.AddText("#bf{CMS Preliminary}                                #sigma(t#bar{t}) = 374 pb (13TeV)")
    elif args.outputName == "ttjets": t1.AddText("#bf{CMS Preliminary}                                #sigma(t#bar{t}) = 831 pb (13TeV)")
    elif args.outputName == "smu": t1.AddText("#bf{CMS Preliminary}    " + runName + "    " + inLumi + " fb^{-1}(13TeV)")
    elif args.outputName == "sel": t1.AddText("#bf{CMS Preliminary}    " + runName + "    " + inLumi + " fb^{-1}(13TeV)")
    elif args.outputName == "ht":  t1.AddText("#bf{CMS Preliminary}    " + runName + "    " + inLumi + " fb^{-1}(13TeV)")
    else: t1.AddText("#bf{CMS Preliminary}                           #sigma(t#bar{t}t#bar{t}) = 9.2 fb (13TeV)")
    t2 = ROOT.TPaveText(0.2, 0.95, 0.93, 1, "nbNDC")
    t2.SetFillColorAlpha(0, 0.9)
    t2.SetTextSize(0.03)
    t2.AddText(legString)
    ROOT.gStyle.SetLegendTextSize(0.028)

    hNames.sort()

    # Draw MC TTTT Motivation
    hltTypes = ["Muon", "Electron", "Jet", "El_CROSS_Jets", "El_OR_Jets", "Mu_OR_Jets", "Jet2", "El_OR_Jets2", "Mu_OR_Jets2"]
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
            for i in range(0, 18):
                binWidth = h_HLTcompare[histName].GetXaxis().GetBinWidth(i)
                binContent = h_HLTcompare[histName].GetBinContent(i)
                newBinContent = round(binContent / binWidth)
                h_HLTcompare[histName].SetBinContent(i, newBinContent)
            #h_HLTcompare[histName].SetLineWidth(3)
            h_HLTcompare[histName].SetLineColor(1)
            h_HLTcompare[histName].GetXaxis().SetTitleOffset(1.4)
            xTitle = h_HLTcompare[histName].GetXaxis().GetTitle()
            if "Mu" in histName:
                newxTitle = xTitle.replace("Lepton", "Muon")
                h_HLTcompare[histName].GetXaxis().SetTitle(newxTitle)
            elif "El" in histName:
                newxTitle = xTitle.replace("Lepton", "Electron")
                h_HLTcompare[histName].GetXaxis().SetTitle(newxTitle)
            # h_HLTcompare[histName].GetYaxis().SetTitleOffset(1.4)
            h_HLTcompare[histName].SetLabelFont(42,"x")
            h_HLTcompare[histName].SetTitleFont(42,"x")
            h_HLTcompare[histName].SetLabelFont(42,"y")
            h_HLTcompare[histName].SetTitleFont(42,"y")
            h_HLTcompare[histName].SetLabelFont(42,"z")
            h_HLTcompare[histName].SetTitleFont(42,"z")
            h_HLTcompare[histName].SetLabelSize(0.04,"x")
            h_HLTcompare[histName].SetTitleSize(0.04,"x")
            h_HLTcompare[histName].SetLabelSize(0.04,"y")
            h_HLTcompare[histName].SetTitleSize(0.04,"y")
            h_HLTcompare[histName].Draw("hist")
            histEntries = h_HLTcompare[histName].GetEntries()
            if xAxis == "nBJet_": h_HLTcompare[histName].GetXaxis().SetRangeUser(2, 10)
            elif xAxis == "nJet_": h_HLTcompare[histName].GetXaxis().SetRangeUser(6, 20)
            elif xAxis == "HT_": h_HLTcompare[histName].GetXaxis().SetRangeUser(400, 3000)
            legEntry = "Baseline (%d)" % histEntries
            legend[n_count].AddEntry(h_HLTcompare[histName], legEntry, 'l')
            colourL = 2
            for hlt in hltTypes:
                if (channel == "El_") and ("Mu" in hlt): continue
                if (channel == "Mu_") and ("El" in hlt): continue
                histName = "h_" + channel + xAxis + hlt
                histEntries = h_HLTcompare[histName].GetEntries()
                if histEntries == 0: continue
                for i in range(0, 18):
                    binWidth = h_HLTcompare[histName].GetXaxis().GetBinWidth(i)
                    binContent = h_HLTcompare[histName].GetBinContent(i)
                    newBinContent = round(binContent / binWidth)
                    h_HLTcompare[histName].SetBinContent(i, newBinContent)
                h_HLTcompare[histName].SetLineColor(colourL)
                h_HLTcompare[histName].Draw("hist same")
                histEntries = h_HLTcompare[histName].GetEntries()
                legEntry = hlt.replace("El_", "e^{#pm} ")
                legEntry = legEntry.replace("Mu_", "#mu^{#pm} ")
                legEntry = legEntry.replace("Jets", "")
                legEntry = legEntry.replace("Jet", "Hadronic")
                legEntry = legEntry.replace("Electron", "e^{#pm} ")
                legEntry = legEntry.replace("Muon", "#mu^{#pm}  ")
                legEntry = legEntry.replace("_", " ")
                legEntry = legEntry + " HLT (%d)" % histEntries
                legend[n_count].AddEntry(h_HLTcompare[histName], legEntry, 'l')
                colourL += 2
            t1.Draw("same")
            if args.outputName == "ttjets":
                legHeader = "#bf{t#bar{t} MC with" + runName + " HLTs}"
                legend[n_count].SetHeader(legHeader, "C")
            elif args.outputName == "smu": legend[n_count].SetHeader("#bf{SingleMuon Samples after:}", "C")
            elif args.outputName == "sel": legend[n_count].SetHeader("#bf{SingleElectron Samples after:}", "C")
            elif args.outputName == "ht": legend[n_count].SetHeader("#bf{HTMHT Samples after:}", "C")
            else:
                legHeader = "#bf{t#bar{t}t#bar{t} MC with " + runName + " HLTs}"
                legend[n_count].SetHeader(legHeader, "C")
            legend[n_count].Draw("same")
            triggerCanvas.Print(args.imageName + channel + xAxis + "ttttEv.png", "png")

            cv4[n_count] = triggerCanvas.cd(1)
            colourM = 2
            legend2[n_count] = ROOT.TLegend(0.5, 0.16, 0.95, 0.5)
            nhlt = 0
            for hlt in hltTypes:
                if (channel == "El_") and ("Mu" in hlt): continue
                if (channel == "Mu_") and ("El" in hlt): continue
                histName = "h_" + channel + xAxis + hlt
                histEntries = h_HLTcompare[histName].GetEntries()
                if histEntries == 0: continue
                print(histEntries)
                tr2_HLTcompare[histName].SetMarkerColor(colourM)
                tr2_HLTcompare[histName].SetLineColor(colourM)
                if nhlt == 0:
                    tr2_HLTcompare[histName].Draw()
                    cv4[n_count].Update()
                    graph1 = tr2_HLTcompare[histName].GetPaintedGraph()
                    graph1.SetMinimum(0)
                    graph1.SetMaximum(1.2)
                    cv4[n_count].Update()
                    histEntries = h_HLTcompare[histName].GetEntries()
                    nhlt += 1
                else:
                    tr2_HLTcompare[histName].Draw("same")
                    histEntries = h_HLTcompare[histName].GetEntries()
                effname = histName.replace("h_", "h_eff2")
                legEntry = hlt.replace("El_", "e^{#pm} ")
                legEntry = legEntry.replace("Mu_", "#mu^{#pm} ")
                legEntry = legEntry.replace("Jets", "")
                legEntry = legEntry.replace("Jet", "Hadronic")
                legEntry = legEntry.replace("Electron", "e^{#pm}  ")
                legEntry = legEntry.replace("Muon", "#mu^{#pm}  ")
                legEntry = legEntry.replace("_", " ")
                legEntry = legEntry + " HLT (%d)" % histEntries
                legend2[n_count].AddEntry(h_HLTcompare[histName], legEntry, "lep")
                colourM += 2
            t1.Draw("same")
            if args.outputName == "ttjets":
                legHeader = "#bf{t#bar{t} MC with" + runName + " HLTs}"
                legend2[n_count].SetHeader(legHeader, "C")
            elif args.outputName == "smu": legend2[n_count].SetHeader("#bf{SingleMuon Samples after:}", "C")
            elif args.outputName == "sel": legend2[n_count].SetHeader("#bf{SingleElectron Samples after:}", "C")
            elif args.outputName == "ht": legend2[n_count].SetHeader("#bf{HTMHT Samples after:}", "C")
            else:
                legHeader = "#bf{t#bar{t}t#bar{t} MC with " + runName + " HLTs}"
                legend2[n_count].SetHeader(legHeader, "C")
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
        for i in range(0, 18):
            binWidth = h_mcTTJets[hName].GetXaxis().GetBinWidth(i)
            binContent = h_mcTTJets[hName].GetBinContent(i)
            newBinContent = round(binContent / binWidth)
            h_mcTTJets[hName].SetBinContent(i, newBinContent)
            binContent = h_dataHTMHTs[hName].GetBinContent(i)
            newBinContent = round(binContent / binWidth)
            h_dataHTMHTs[hName].SetBinContent(i, newBinContent)
            binContent = h_dataSMus[hName].GetBinContent(i)
            newBinContent = round(binContent / binWidth)
            h_dataSMus[hName].SetBinContent(i, newBinContent)
            binContent = h_dataSEls[hName].GetBinContent(i)
            newBinContent = round(binContent / binWidth)
            h_dataSEls[hName].SetBinContent(i, newBinContent)
        maxYs = getMaxY([h_mcTTJets[hName], h_dataSMus[hName], h_dataHTMHTs[hName], h_dataSEls[hName]])
        h_mcTTJets[hName].SetMaximum(maxYs + 100)
        h_mcTTJets[hName].SetLineColor(1)
        h_mcTTJets[hName].Draw("hist")
        histEntries = h_mcTTJets[hName].GetEntries()
        h_mcTTJets[hName].SetTitle("t#bar{t} pair MC (%d)" % histEntries)
        newName = h_mcTTJets[hName].GetName()
        print(newName)
        legend3[n_count].AddEntry(h_mcTTJets[hName], "t#bar{t} pair MC (%d)" % histEntries, 'l')

        h_dataHTMHTs[hName].SetLineColor(4)
        h_dataHTMHTs[hName].SetMarkerStyle(20)
        h_dataHTMHTs[hName].SetMarkerColor(4)
        h_dataHTMHTs[hName].SetMarkerSize(1.2)
        h_dataHTMHTs[hName].Draw('E0 X0 same')
        histEntries = h_dataHTMHTs[hName].GetEntries()
        h_dataHTMHTs[hName].SetTitle("HTMHT Data (%d)" % histEntries)
        newName = h_dataHTMHTs[hName].GetName()
        legend3[n_count].AddEntry(h_dataHTMHTs[hName], "HTMHT Data (%d)" % histEntries, 'lep')

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
            legend3[n_count].AddEntry(h_dataSMus[hName], "Single Muon Data (%d) " % histEntries, 'lep')
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
            legend3[n_count].AddEntry(h_dataSEls[hName], "Single Electron Data (%d)" % histEntries, 'lep')

        t2.Draw("same")
        legend3[n_count].Draw("same")
        pdfCreator(args, 1, triggerCanvas)
        triggerCanvas.Print(args.imageName + "{0}events.png".format(hName), "png")

        ####################################
        # - Draw trigger efficiency hists  #
        ####################################
        if  args.inputLFN == "18AB":
            tr2_dataHTMHT = tr2_dataHTMHT_AB
            tr2_dataSMu = tr2_dataSMu_AB
            tr2_dataSEl = tr2_dataSEl_AB
        elif  args.inputLFN == "18CD":
            tr2_dataHTMHT = tr2_dataHTMHT_CD
            tr2_dataSMu= tr2_dataSMu_CD
            tr2_dataSEl= tr2_dataSEl_CD
        else: return 0

        cv1[n_count] = triggerCanvas.cd(1)
        legend4[n_count] = ROOT.TLegend(0.5, 0.16, 0.95, 0.5)
        tr2_mcTTJet[hName].SetLineColor(1)
        tr2_mcTTJet[hName].Draw()
        newName = tr2_mcTTJet[hName].GetName()
        legend4[n_count].AddEntry(newName, "t#bar{t} pair MC", 'lep')
        cv1[n_count].Update()
        graph1 = tr2_mcTTJet[hName].GetPaintedGraph()
        graph1.SetMinimum(0)
        graph1.SetMaximum(1.2)
        #cv1[n_count].SetLogy(1)
        cv1[n_count].Update()

        if "Mu" in hName:
            legend4[n_count].SetHeader("#bf{#mu^{#pm} + jets  selection}", "C")
            tr2_dataSMu_AB[hName].SetLineColor(2)
            tr2_dataSMu[hName].SetMarkerStyle(20)
            tr2_dataSMu[hName].SetMarkerColor(2)
            tr2_dataSMu[hName].SetMarkerSize(1.2)
            tr2_dataSMu[hName].Draw('same')
            newName = tr2_dataSMu[hName].GetName()
            legend4[n_count].AddEntry(tr2_dataSMu[hName], "SingleMuon Data", 'lep')
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
            legend4[n_count].AddEntry(tr2_dataSEl[hName], "SingleElectron Data", 'lep')

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
        s_HTMHT_AB[hName].SetLineColor(4)
        #s_dataSMu_AB[hName].SetMarkerStyle(20)
        #s_dataSMu_AB[hName].SetMarkerColor(2)
        #s_dataSMu_AB[hName].SetMarkerSize(1.2)
        s_HTMHT_AB[hName].SetMinimum(0)
        s_HTMHT_AB[hName].SetMaximum(1.2)
        #s_HTMHT[hName].Draw('E0 X0')
        newName = s_HTMHT_AB[hName].GetName()
        #legend5[n_count].AddEntry(newName, "HTMHT Data", 'lep')
        if "Mu" in hName:
            legend5[n_count].SetHeader("#bf{SingleMuon Data}", "C")
            s_dataSMu_AB[hName].SetLineColor(2)
            s_dataSMu_AB[hName].SetMarkerStyle(20)
            s_dataSMu_AB[hName].SetMarkerColor(2)
            s_dataSMu_AB[hName].SetMarkerSize(1.2)
            s_dataSMu_AB[hName].SetMinimum(0)
            s_dataSMu_AB[hName].SetMaximum(1.2)
            s_dataSMu_AB[hName].Draw('E0 X0')
            newName = s_dataSMu_AB[hName].GetName()
            legend5[n_count].AddEntry(s_dataSMu_AB[hName], "RunII 2018AB", 'lep')

            s_dataSMu_CD[hName].SetLineColor(4)
            s_dataSMu_CD[hName].SetMarkerStyle(20)
            s_dataSMu_CD[hName].SetMarkerColor(4)
            s_dataSMu_CD[hName].SetMarkerSize(1.2)
            s_dataSMu_CD[hName].Draw('E0 X0 same')
            newName = s_dataSMu_CD[hName].GetName()
            legend5[n_count].AddEntry(s_dataSMu_CD[hName], "RunII 2018CD", 'lep')

        elif "El" in hName:
            legend5[n_count].SetHeader("#bf{SingleElectron Data}", "C")
            s_dataSEl_AB[hName].SetLineColor(2)
            s_dataSEl_AB[hName].SetMarkerStyle(20)
            s_dataSEl_AB[hName].SetMarkerColor(2)
            s_dataSEl_AB[hName].SetMarkerSize(1.2)
            s_dataSEl_AB[hName].SetMinimum(0)
            s_dataSEl_AB[hName].SetMaximum(1.2)
            s_dataSEl_AB[hName].Draw('E0 X0')
            newName = s_dataSEl_AB[hName].GetName()
            legend5[n_count].AddEntry(s_dataSEl_AB[hName], "RunII 2018AB", 'lep')

            s_dataSEl_CD[hName].SetLineColor(4)
            s_dataSEl_CD[hName].SetMarkerStyle(20)
            s_dataSEl_CD[hName].SetMarkerColor(4)
            s_dataSEl_CD[hName].SetMarkerSize(1.2)
            s_dataSEl_CD[hName].Draw('E0 X0 same')
            newName = s_dataSEl_CD[hName].GetName()
            legend5[n_count].AddEntry(s_dataSEl_CD[hName], "RunII 2018CD", 'lep')
        t2.Draw("same")
        legend5[n_count].Draw("same")
        pdfCreator(args, 1, triggerCanvas)
        triggerCanvas.Print(args.imageName + "{0}_sf.png".format(hName), "png")

        eventDIR.cd()
        mcName = hName.replace("h_", "h_mcTTJet_")
        h_mcTTJets[hName].Write(mcName)
        htName = hName.replace("h_", "h_dataHTMHT_")
        h_dataHTMHTs[hName].Write(htName)
        muName = hName.replace("h_", "h_dataMu_")
        h_dataSMus[hName].Write(muName)
        eleName = hName.replace("h_", "h_dataEle_")
        h_dataSEls[hName].Write(eleName)

        effDIR.cd()
        #tr_mcTTJet[hName].Write(mcName)
        #tr_dataHTMHT_AB[hName].Write(htName)
        #tr_dataSMu_AB[hName].Write(muName)
        #tr_dataSEl_AB[hName].Write(eleName)

        sfDIR.cd()
        #s_HTMHT_AB[hName].Write(htName)
        #s_dataSMu_AB[hName].Write(muName)
        #s_dataSEl_AB[hName].Write(eleName)
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
