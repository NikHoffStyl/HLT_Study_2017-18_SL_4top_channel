#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Jan 2019

Plotter of many event distributions ,
HLT efficiency dirtibutions and
their scale factors for run period 
RunII 2017 and 2018

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
import csv

SetPlotStyle()

histFilesDir = "/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/TrigStudyMuJets/v8_HistFiles/"
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
        legStr = "#bf{CMS Preliminary} Run2017B   4.82 fb^{-1} (13TeV)"
    elif args == "17C":
        legStr = "#bf{CMS Preliminary} Run2017C  9.66 fb^{-1} (13TeV)"
    elif args == "17D":
        legStr = "#bf{CMS Preliminary} Run2017D  4.25 fb^{-1} (13TeV)"
    elif args == "17E":
        legStr = "#bf{CMS Preliminary} Run2017E  9.28 fb^{-1} (13TeV)"
    elif args == "17F":
        legStr = "#bf{CMS Preliminary} Run2017F  13.52 fb^{-1} (13TeV)"
    elif args == "17DEF":
        legStr = "#bf{CMS Preliminary} Run2017D-F  27.05 fb^{-1} (13TeV)"
    elif args == "17CDEF":
        legStr = "#bf{CMS Preliminary} Run2017C-F  36.71 fb^{-1} (13TeV)"
    elif args == "all":
        legStr = "#bf{CMS Preliminary} All Run2017  41.53 fb^{-1} (13TeV)"
    elif args == "18A":
        legStr = "#bf{CMS Preliminary} Run2018A  14.00 fb^{-1} (13TeV)"
    elif args == "18B":
        legStr = "#bf{CMS Preliminary} Run2018B  7.10 fb^{-1} (13TeV)"
    elif args == "18C":
        legStr = "#bf{CMS Preliminary} Run2018C   6.94 fb^{-1} (13TeV)"
    elif args == "18D":
        legStr = "#bf{CMS Preliminary} Run2018D   31.93 fb^{-1} (13TeV)"
    elif args == "18AB":
        legStr = "#bf{CMS Preliminary} Run2018A-B  21.10 fb^{-1} (13TeV)"
    elif args == "18CD":
        legStr = "#bf{CMS Preliminary} Run2018C-D  38.87 fb^{-1} (13TeV)"
    else:
        legStr = "#bf{CMS Preliminary}"

    return legStr


def cmsPlotStringBase(args):
    """

    Args:
        args (string): command line arguments

    Returns:
        legStr (string): string containing channel details

    """
    if args == "17B":
        legStr = "#bf{CMS Preliminary} Run2017B Baseline 4.82 fb^{-1} (13TeV)"
    elif args == "17C":
        legStr = "#bf{CMS Preliminary} Run2017C Baseline 9.66 fb^{-1} (13TeV)"
    elif args == "17D":
        legStr = "#bf{CMS Preliminary} Run2017D Baseline 4.25 fb^{-1} (13TeV)"
    elif args == "17E":
        legStr = "#bf{CMS Preliminary} Run2017E Baseline 9.28 fb^{-1} (13TeV)"
    elif args == "17F":
        legStr = "#bf{CMS Preliminary} Run2017F Baseline 13.52 fb^{-1} (13TeV)"
    elif args == "17DEF":
        legStr = "#bf{CMS Preliminary} Run2017D-F Baseline 27.05 fb^{-1} (13TeV)"
    elif args == "17CDEF":
        legStr = "#bf{CMS Preliminary} Run2017C-F Baseline 36.71 fb^{-1} (13TeV)"
    elif args == "all":
        legStr = "#bf{CMS Preliminary} All Run2017 Baseline 41.53 fb^{-1} (13TeV)"
    elif args == "18A":
        legStr = "#bf{CMS Preliminary} Run2018A Baseline 14.00 fb^{-1} (13TeV)"
    elif args == "18B":
        legStr = "#bf{CMS Preliminary} Run2018B Baseline 7.10 fb^{-1} (13TeV)"
    elif args == "18C":
        legStr = "#bf{CMS Preliminary} Run2018C Baseline 6.94 fb^{-1} (13TeV)"
    elif args == "18D":
        legStr = "#bf{CMS Preliminary} Run2018D Baseline 31.93 fb^{-1} (13TeV)"
    elif args == "18AB":
        legStr = "#bf{CMS Preliminary} Run2018A-B Baseline 21.10 fb^{-1} (13TeV)"
    elif args == "18CD":
        legStr = "#bf{CMS Preliminary} Run2018C-D Baseline 38.87 fb^{-1} (13TeV)"
    else:
        legStr = "#bf{CMS Preliminary} Baseline"

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
    elif "18" in fileName:
        if "18C" in fileName or "18D" in fileName or "tt" in fileName:
            trigList = getFileContents("../myInFiles/2018CDtrigList.txt", True)
        else:
            trigList = getFileContents("../myInFiles/2018ABtrigList.txt", True)
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
    xAxesOptions = ["HTpt"
                    ]
                    # "lepEta", "lepPhi",
                    # "nJet", "nBJet"
    trgList = findTrigList(fileName)
    hNames = []
    for xAxisLabel in xAxesOptions:
        for lep in ["Mu", "El"]:
            for key in trgList:
                if lep == "El" and "Mu" in key: continue
                if lep == "Mu" and "El" in key: continue
                hNames.append("h_" + lep + "_" + xAxisLabel + "_" + key)
            if ("18C" in fileName) or ("18D" in fileName) or  ("18ABCD" in fileName): 
                hNames.append("h_" + lep + "_" + xAxisLabel + "_no-HLT2")
            else: hNames.append("h_" + lep + "_" + xAxisLabel + "_no-HLT")
    if verbose: print(hNames)
    return hNames


def rebinHist(hIn, dirName):
    """
    Args: 
       hIn: Input histogram List
       htype: string describing the type of sample
    Returns:
       hIn: Output histogram List
    """
    for hName in hIn:
        xTitle = hIn[hName].GetXaxis().GetTitle()
        xTitle = xTitle.replace("/ GeVc^{-1}", " [GeV]")
        yTitle = hIn[hName].GetYaxis().GetTitle()
        yTitle = yTitle.replace("/ GeVc^{-1}", " [GeV]")
        zTitle = hIn[hName].GetZaxis().GetTitle()
        zTitle = zTitle.replace("GeVc^{-1}", "GeV")
        if "Mu" in hName: 
            yTitle = yTitle.replace("Lepton", "Muon")
        elif "El" in hName: 
            yTitle = yTitle.replace("Lepton", "Electron")
        hIn[hName].SetTitle("; {0}; {1}; {2}".format(xTitle, yTitle, zTitle))
        hIn[hName].SetDirectory(dirName)

    return hIn


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


    #  Integrated Luminosity of Era in /fb
    if era == "17B":
        intgrLumi = 4.823
    elif era == "17C":
        intgrLumi = 9.664 
    elif (era == "17D"):
        intgrLumi = 27.052 # 4.252 
    elif (era == "17E"):
        intgrLumi = 9.278  
    elif (era == "17F"):
        intgrLumi = 13.522
    elif (era == "17DEF"):
        intgrLumi = 27.052
    elif (era == "18A"):
        intgrLumi = 21.10 #14.00 /fb
    elif era == "18B":
        intgrLumi = 7.10  # /fb
    elif era == "18C":
        intgrLumi = 38.87 #6.94 /fb
    elif (era == "18D"):
        intgrLumi = 31.93 # /fb
    elif (era == "18AB"):
        intgrLumi = 21.10 # /fb
    elif (era == "18CD"):
        intgrLumi = 38.87 # /fb
    else:
        intgrLumi = 41.53
        print("No actions yet for this option")


    counter = 0
    for fName in fileList:
        f.append(ROOT.TFile.Open(fName))
        f[counter].cd("plots")
        print(fName)
        if ("dataSEl" in fName) or ("SingleEl" in fName) or ("sel2D1" in fName):
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
    
    if  bool(h1) == False: 
        print("removed" + title)
        return h_TH1DOut, h_TEffOut    
    else:
        hltTypes = ["Muon", "Electron", "Jet", "El_CROSS_Jets", "Mu_CROSS_Jets", "El_OR_Jets", "Mu_OR_Jets"]
        if "18AB" in title: hltTypes = ["Muon", "Electron", "Jet", "El_CROSS_Jets", "El_OR_Jets", "Mu_OR_Jets"]
        if "18CD" in title or "18ABtt" in title: hltTypes = ["Muon", "Electron", "Jet2", "El_CROSS_Jets", "El_OR_Jets2", "Mu_OR_Jets2"]
        channels = ["Mu_", "El_"]
        xAxes = ["HTpt_"] #, "pt_", "nJet_", "nBJet_", "lepEta_", "lepPhi_"]
        n_count = 0
        for channel in channels:
            for xAxis in xAxes:
                n_count += 1
                histNameDen = "h_" + channel + xAxis + "no-HLT"
                if "18CD" in title or "18ABtt" in title: histNameDen = "h_" + channel + xAxis + "no-HLT2"                
                for hlt in hltTypes:
                    if hlt == "Mu_CROSS_Jets" and ("18" in title): continue
                    if hlt == "Mu_CROSS_Jets" and ("17B" in title): continue # and args.inputLFN == "17B": continue
                    if channel == "El_" and "Mu" in hlt: continue
                    if channel == "Mu_" and "El" in hlt: continue
                    histNameNum = "h_" + channel + xAxis + hlt
                    effName = histNameNum.replace("h_", "h_eff")
                    effName2 = histNameNum.replace("h_", "h_eff2")
                    # hh, tg = histNameNum.split(histNameDen)
                    if h1[histNameNum].GetNbinsX() != h1[histNameDen].GetNbinsX():
                        print("\n ERROR different hists size: %s  %d  %d " % (histNameNum, h_TH1DOut[histNameNum].GetNbinsX(), h1[histNameDen].GetNbinsX()))
                        print("returned empty efficiency plots!!! \n")
                        continue
                    h_TH1DOut[histNameNum] = h1[histNameNum].Clone(effName)
                    h_TH1DOut[histNameNum].Sumw2()
                    h_TH1DOut[histNameNum].SetStats(0)
                    h_TH1DOut[histNameNum].Divide(h1[histNameDen])
                    #xTitle = h1[histNameDen].GetXaxis().GetTitle()
                    #xTitle = xTitle.replace("/ GeVc^{-1}", " [GeV]")
                    xBinWidth = h1[histNameDen].GetXaxis().GetBinWidth(1)
                    #if "Mu" in histNameDen: 
                    #    newxTitle = xTitle.replace("Lepton", "Muon")
                    #elif "El" in histNameDen: 
                    #    newxTitle = xTitle.replace("Lepton", "Electron")
                    #h_TH1DOut[histNameNum].SetTitle(title + ";{0};Trigger Efficiency".format(newxTitle))
                    h_TH1DOut[histNameNum].GetZaxis().SetTitle("Trigger Efficiency")
                    h_TH1DOut[histNameNum].SetDirectory(newDir)
                    #if not ROOT.TEfficiency.CheckConsistency(h1[histNameNum], h1[histNameDen]):
                     #   print(histNameNum + " could not get efficiency")
                      #  continue
                    #h_TEffOut[histNameNum] = ROOT.TEfficiency(h1[histNameNum], h1[histNameDen])
                    #h_TEffOut[histNameNum].SetTitle(title + ";{0};Trigger Efficiency".format(newxTitle))
                    #h_TEffOut[histNameNum].SetName(effName2)
                    # print(histNameNum)

        #if not h_TEffOut: print("\n ")
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
    if bool(h1) == False or bool(h2) == False: 
        print("SF plots removed: " + title)
        return h_scale, hNameList
    else:
        for hName in h1:
            for hName2 in h2:
                if "18AB" in title:
                    if ("Jet2" in hName2 or "OR_Jets2" in hName2):
                        hName3 = hName2.replace("2","")
                    else: hName3 = hName2
                else: hName3 = hName2
                if not hName == hName3:
                    continue
                # if "18CD" in title: print("CD      "+ hName + "  ==  " + hName2)
                # elif "18AB" in title: print("AB      "+ hName + "  ==  " + hName2)
                # print("{0}   {1} ".format(hName, hName2))
                sfName = hName.replace("h_", "h_sf")
                hNameList.append(hName)
                h_scale[hName] = h1[hName].Clone(sfName)
                # h_scale[hName].Sumw2()
                h_scale[hName].SetStats(0)
                h_scale[hName].Divide(h2[hName2])
                #xTitle = h2[hName2].GetXaxis().GetTitle()
                xBinWidth = h2[hName2].GetXaxis().GetBinWidth(1)
                #h_scale[hName].SetTitle(title + ";{0};Scale Factors".format(xTitle))
                h_scale[hName].GetZaxis().SetTitle("Scale Factors")
                h_scale[hName].SetDirectory(newDir)
        if title == "Single Electron Data 17B": 
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            print(hNameList)

        return h_scale, hNameList


def whatTrig(h_name):
    """

    Args:
        h_name:

    Returns:

    """
    xAxesOptions = ["HTpt_"] # , "pt_", "nJet", "nBJet", "lepEta", "lepPhi"]
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
    parser.add_argument("-f", "--inputLFN", choices=["17B", "17C", "17D", "17E", "17F", "17DEF", "18CD", "18AB", "all"],
                        default="D", help="Set era in 2017 to be checked")
    parser.add_argument("-o", "--outputName", default="tttt", help="Set name of output file")
    parser.add_argument("-i", "--imageName", default="v8_HistFiles/plotImages/", help="Set directory to save images")
    parser.add_argument("-pdf", "--pdfName", default="v8_HistFiles/plotPDFs/", help="Set directory to save pdfs")
    args = parser.parse_args()

    preSelCuts = getFileContents("../myInFiles/preSelectionCuts.txt", True)
    selCriteria = getFileContents("selectionCriteria.txt", True)

    era = args.inputLFN
    if era == "17B":
        runName = "RunII 2017B"
        inLumi = "4.823"  # /fb
    elif era == "17C":
        runName = "RunII 2017C"
        inLumi = "9.664"  # /fb
    elif (era == "17D"):
        runName = "RunII 2017D"
        inLumi = "27.052" # 4.252  # /fb
    elif (era == "17E"):
        runName = "RunII 2017E"
        inLumi = "9.278"  # /fb
    elif (era == "17F"):
        runName = "RunII 2017F"
        inLumi = "13.522"  # /fb
    elif (era == "17DEF"):
        runName = "RunII 2017D-F"
        inLumi = "27.052"  # /fb
    elif era == "18AB":
        inLumi = "21.10" # /fb
        runName = "RunII 2018A-B"
    elif era == "18CD":
        runName = "RunII 2018C-D"
        inLumi = "38.87" # /fb
    else:
        inLumi = "41.53"  # /fb

    # - Create canvases
    triggerCanvas = ROOT.TCanvas('triggerCanvas', 'Triggers', 960, 800)
    triggerCanvas.SetGrid()

    legString = cmsPlotStringBase(args.inputLFN)  # Create text for legend
    # legString = cmsPlotString(args.inputLFN)  # Create text for legend

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
    h_HLTcompare = {}
    h_mcTTToSemiLeps = {}
    h_dataHTMHTs17DEF = {}
    h_dataSMus17DEF = {}
    h_dataSEls17DEF = {}
    h_dataHTMHTs18AB = {}
    h_dataSMus18AB = {}
    h_dataSEls18AB = {}
    h_dataHTMHTs18CD = {}
    h_dataSMus18CD = {}
    h_dataSEls18CD = {}
    h_dataHTMHTs = {}
    h_dataSMus = {}
    h_dataSEls = {}
    h_dataMuHTs = {}
    h_dataElHTs = {}
    tr_mcTTToSemiLep = {}
    tr_dataHTMHT = {}
    tr_dataSEl = {}
    tr_dataSMu = {}
    tr_dataMuHTs = {}
    tr_dataElHTs = {}
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

    eventDIR.cd()

    for hname1 in h_dataHTMHTs17D:
        for hname2 in h_dataHTMHTs17E:
            if hname1 == hname2:
                oldName = h_dataHTMHTs17D[hname1].GetName()
                newName = oldName.replace("h_", "h_def")
                h_dataHTMHTs17DEF[hname1] = h_dataHTMHTs17D[hname1].Clone(newName)
                oldName = h_dataSMus17D[hname1].GetName()
                newName = oldName.replace("h_", "h_def")
                h_dataSMus17DEF[hname1] = h_dataSMus17D[hname1].Clone(newName)
                oldName = h_dataSEls17D[hname1].GetName()
                newName = oldName.replace("h_", "h_def")
                h_dataSEls17DEF[hname1] = h_dataSEls17D[hname1].Clone(newName)
                h_dataHTMHTs17DEF[hname1].Add(h_dataHTMHTs17E[hname1])
                h_dataSMus17DEF[hname1].Add(h_dataSMus17E[hname1])
                h_dataSEls17DEF[hname1].Add(h_dataSEls17E[hname1])
                for hname3 in h_dataHTMHTs17F:
                    if hname3 == hname1:
                        h_dataHTMHTs17DEF[hname1].Add(h_dataHTMHTs17F[hname1])
                        h_dataSMus17DEF[hname1].Add(h_dataSMus17F[hname1])
                        h_dataSEls17DEF[hname1].Add(h_dataSEls17F[hname1])

    for hname1 in h_dataHTMHTs18A:
        for hname2 in h_dataHTMHTs18B:
            if hname1 == hname2:
                oldName = h_dataHTMHTs18A[hname1].GetName()
                newName = oldName.replace("h_", "h_ab")
                h_dataHTMHTs18AB[hname1] = h_dataHTMHTs18A[hname1].Clone(newName)
                oldName = h_dataSMus18A[hname1].GetName()
                newName = oldName.replace("h_", "h_ab")
                h_dataSMus18AB[hname1] = h_dataSMus18A[hname1].Clone(newName)
                oldName = h_dataSEls18A[hname1].GetName()
                newName = oldName.replace("h_", "h_ab")
                h_dataSEls18AB[hname1] = h_dataSEls18A[hname1].Clone(newName)
                h_dataHTMHTs18AB[hname1].Add(h_dataHTMHTs18B[hname1])
                h_dataSMus18AB[hname1].Add(h_dataSMus18B[hname1])
                h_dataSEls18AB[hname1].Add(h_dataSEls18B[hname1])

    for hname1 in h_dataHTMHTs18C:
        for hname2 in h_dataHTMHTs18D:
            if hname1 == hname2:
                oldName = h_dataHTMHTs18C[hname1].GetName()
                newName = oldName.replace("h_", "h_cd")
                h_dataHTMHTs18CD[hname1] = h_dataHTMHTs18C[hname1].Clone(newName)
                oldName = h_dataSMus18C[hname1].GetName()
                newName = oldName.replace("h_", "h_cd")
                h_dataSMus18CD[hname1] = h_dataSMus18C[hname1].Clone(newName)
                oldName = h_dataSEls18C[hname1].GetName()
                newName = oldName.replace("h_", "h_cd")
                h_dataSEls18CD[hname1] = h_dataSEls18C[hname1].Clone(newName)
                h_dataHTMHTs18CD[hname1].Add(h_dataHTMHTs18D[hname1])
                h_dataSMus18CD[hname1].Add(h_dataSMus18D[hname1])
                h_dataSEls18CD[hname1].Add(h_dataSEls18D[hname1])

    h_dataMuHTs17B = {} 
    h_dataElHTs17B ={} 
    h_dataMuHTs17C ={} 
    h_dataElHTs17C ={} 
    h_dataMuHTs17DEF ={}
    h_dataElHTs17DEF ={} 
    #print("3 h_El_HT_El_OR_Jets %d" % h_dataHTMHTs["h_El_HT_El_OR_Jets"].GetEntries())
    for hName in h_dataSMus17B:
        oldName = h_dataHTMHTs17B[hName].GetName()
        newName = oldName.replace("h_", "h_muhtB")
        h_dataMuHTs17B[hName] = h_dataHTMHTs17B[hName].Clone(newName)
        oldName = h_dataHTMHTs17B[hName].GetName()
        newName = oldName.replace("h_", "h_elhtC")
        h_dataElHTs17B[hName] = h_dataHTMHTs17B[hName].Clone(newName)
        h_dataMuHTs17B[hName].Add(h_dataSMus17B[hName])
        h_dataElHTs17B[hName].Add(h_dataSEls17B[hName])
    #print("4 h_El_HT_El_OR_Jets %d" % h_dataHTMHTs["h_El_HT_El_OR_Jets"].GetEntries())
    for hName in h_dataSMus17C:
        oldName = h_dataHTMHTs17C[hName].GetName()
        newName = oldName.replace("h_", "h_muhtC")
        h_dataMuHTs17C[hName] = h_dataHTMHTs17C[hName].Clone(newName)
        oldName = h_dataHTMHTs17C[hName].GetName()
        newName = oldName.replace("h_", "h_elhtC")
        h_dataElHTs17C[hName] = h_dataHTMHTs17C[hName].Clone(newName)
        h_dataMuHTs17C[hName].Add(h_dataSMus17C[hName])
        h_dataElHTs17C[hName].Add(h_dataSEls17C[hName])
    #print("2 h_El_HT_El_OR_Jets %d" % h_dataHTMHTs["h_El_HT_El_OR_Jets"].GetEntries())
    for hName in h_dataSMus17DEF:
        oldName = h_dataHTMHTs17DEF[hName].GetName()
        newName = oldName.replace("h_", "h_muhtDEF")
        h_dataMuHTs17DEF[hName] = h_dataHTMHTs17DEF[hName].Clone(newName)
        oldName = h_dataHTMHTs17DEF[hName].GetName()
        newName = oldName.replace("h_", "h_elhtDEF")
        h_dataElHTs17DEF[hName] = h_dataHTMHTs17DEF[hName].Clone(newName)
        h_dataMuHTs17DEF[hName].Add(h_dataSMus17DEF[hName])
        h_dataElHTs17DEF[hName].Add(h_dataSEls17DEF[hName])
    #print("5 h_El_HT_El_OR_Jets %d" % h_dataHTMHTs["h_El_HT_El_OR_Jets"].GetEntries())

    h_dataMuHTs18AB ={}
    h_dataElHTs18AB ={}
    for hName in h_dataSMus18AB:
        oldName = h_dataHTMHTs18AB[hName].GetName()
        newName = oldName.replace("h_", "h_muhtAB")
        h_dataMuHTs18AB[hName] = h_dataHTMHTs18AB[hName].Clone(newName)
        oldName = h_dataHTMHTs18AB[hName].GetName()
        newName = oldName.replace("h_", "h_elhtAB")
        h_dataElHTs18AB[hName] = h_dataHTMHTs18AB[hName].Clone(newName)
        h_dataMuHTs18AB[hName].Add(h_dataSMus18AB[hName])
        h_dataElHTs18AB[hName].Add(h_dataSEls18AB[hName])

    h_dataMuHTs18CD ={}
    h_dataElHTs18CD ={}
    for hName in h_dataSMus18CD:
        oldName = h_dataHTMHTs18CD[hName].GetName()
        newName = oldName.replace("h_", "h_muhtCD")
        h_dataMuHTs18CD[hName] = h_dataHTMHTs18CD[hName].Clone(newName)
        oldName = h_dataHTMHTs18CD[hName].GetName()
        newName = oldName.replace("h_", "h_elhtCD")
        h_dataElHTs18CD[hName] = h_dataHTMHTs18CD[hName].Clone(newName)
        h_dataMuHTs18CD[hName].Add(h_dataSMus18CD[hName])
        h_dataElHTs18CD[hName].Add(h_dataSEls18CD[hName])
        print(hName)

    tr_mcTTTT_B, tr2_mcTTTT_B = findTrigRatio(h_mcTTTTs17B, "Four Top MC 17B", effDIR)
    tr_mcTTToSemiLep_B, tr2_mcTTToSemiLep_B = findTrigRatio(h_mcTTJets17B, "Top-AntiTop MC 17B", effDIR)
    tr_dataHTMHT_B, tr2_dataHTMHT_B = findTrigRatio(h_dataHTMHTs17B, "HTMHT Data 17B", effDIR)
    tr_dataSMu_B, tr2_dataSMu_B = findTrigRatio(h_dataSMus17B, "Single Muon Data 17B", effDIR)
    tr_dataSEl_B, tr2_dataSEl_B = findTrigRatio(h_dataSEls17B, "Single Electron Data 17B", effDIR)
    tr_dataMuHTs17B, tr2_dataMuHTs17B = findTrigRatio(h_dataMuHTs17B, "All Data 17B", effDIR)
    tr_dataElHTs17B, tr2_dataElHTs17B = findTrigRatio(h_dataElHTs17B, "All Data 17B", effDIR)

    tr_mcTTTT_C, tr2_mcTTTT_C = findTrigRatio(h_mcTTTTs17C, "Four Top MC", effDIR)
    tr_mcTTToSemiLep_C, tr2_mcTTToSemiLep_C = findTrigRatio(h_mcTTJets17C, "Top-AntiTop MC", effDIR)
    tr_dataHTMHT_C, tr2_dataHTMHT_C = findTrigRatio(h_dataHTMHTs17C, "HTMHT Data", effDIR)
    tr_dataSMu_C, tr2_dataSMu_C = findTrigRatio(h_dataSMus17C, "Single Muon Data", effDIR)
    tr_dataSEl_C, tr2_dataSEl_C = findTrigRatio(h_dataSEls17C, "Single Electron Data", effDIR)
    tr_dataMuHTs17C, tr2_dataMuHTs17C = findTrigRatio(h_dataMuHTs17C, "All Data", effDIR)
    tr_dataElHTs17C, tr2_dataElHTs17C = findTrigRatio(h_dataElHTs17C, "All Data", effDIR)

    tr_mcTTTT, tr2_mcTTTT = findTrigRatio(h_mcTTTTs17D, "Four Top MC", effDIR)
    tr_mcTTToSemiLepDEF, tr2_mcTTToSemiLepDEF = findTrigRatio(h_mcTTJets17D, "Top-AntiTop MC", effDIR)
    tr_dataHTMHT_DEF, tr2_dataHTMHT_DEF = findTrigRatio(h_dataHTMHTs17DEF, "HTMHT Data", effDIR)
    tr_dataSMu_DEF, tr2_dataSMu_DEF = findTrigRatio(h_dataSMus17DEF, "Single Muon Data", effDIR)
    tr_dataSEl_DEF, tr2_dataSEl_DEF = findTrigRatio(h_dataSEls17DEF, "Single Electron Data", effDIR)
    tr_dataMuHTs17DEF, tr2_dataMuHTs17DEF = findTrigRatio(h_dataMuHTs17DEF, "All Data", effDIR)
    tr_dataElHTs17DEF, tr2_dataElHTs17DEF = findTrigRatio(h_dataElHTs17DEF, "All Data", effDIR)

    tr_mcTTTT_18A, tr2_mcTTTT_18A = findTrigRatio(h_mcTTTTs18A, "Four Top MC 18ABtt", effDIR)
    tr_mcTTToSemiLep_18A, tr2_mcTTToSemiLep_18A = findTrigRatio(h_mcTTJets18A, "Top-AntiTop MC 18ABtt", effDIR)
    tr_dataMuHTs18AB, tr2_dataMuHTs18AB = findTrigRatio(h_dataMuHTs18AB, "All Data 18AB", effDIR)
    tr_dataElHTs18AB, tr2_dataElHTs18AB = findTrigRatio(h_dataElHTs18AB, "All Data 18AB", effDIR)
    tr_dataMuHTs18CD, tr2_dataMuHTs18CD = findTrigRatio(h_dataMuHTs18CD, "All Data 18CD", effDIR)
    tr_dataElHTs18CD, tr2_dataElHTs18CD = findTrigRatio(h_dataElHTs18CD, "All Data 18CD", effDIR)

    # - Find scale factor histogram dictionaries
    effDIR.cd()
    s_HTMHT_B, hNames_B = scaleFactor(tr_dataHTMHT_B, tr_mcTTToSemiLep_B, "HTMHT Data 17B", args.inputLFN, sfDIR)
    s_dataSMu_B, hNamesMu_B = scaleFactor(tr_dataSMu_B, tr_mcTTToSemiLep_B, "Single Muon Data 17B", args.inputLFN, sfDIR)
    s_dataSEl_B, hNamesEl_B = scaleFactor(tr_dataSEl_B, tr_mcTTToSemiLep_B, "Single Electron Data 17B", args.inputLFN, sfDIR)
    s_dataMuHTs17B, hNamesHTMu_B = scaleFactor(tr_dataMuHTs17B, tr_mcTTToSemiLep_B, "All Data 17B", args.inputLFN, sfDIR)
    s_dataElHTs17B, hNamesHTEl_B = scaleFactor(tr_dataElHTs17B, tr_mcTTToSemiLep_B, "All Data 17B", args.inputLFN, sfDIR)

    s_HTMHT_C, hNames_C = scaleFactor(tr_dataHTMHT_C, tr_mcTTToSemiLep_C, "HTMHT Data", args.inputLFN, sfDIR)
    s_dataSMu_C, hNamesMu_C = scaleFactor(tr_dataSMu_C, tr_mcTTToSemiLep_C, "Single Muon Data", args.inputLFN, sfDIR)
    s_dataSEl_C, hNamesEl_C = scaleFactor(tr_dataSEl_C, tr_mcTTToSemiLep_C, "Single Electron Data", args.inputLFN, sfDIR)
    s_dataMuHTs17C, hNamesHTMu_C = scaleFactor(tr_dataMuHTs17C, tr_mcTTToSemiLep_C, "All Data", args.inputLFN, sfDIR)
    s_dataElHTs17C, hNamesHTEl_C = scaleFactor(tr_dataElHTs17C, tr_mcTTToSemiLep_C, "All Data 17C", args.inputLFN, sfDIR)

    s_HTMHT, hNames = scaleFactor(tr_dataHTMHT_DEF, tr_mcTTToSemiLepDEF, "HTMHT Data", args.inputLFN, sfDIR)
    s_dataSMu, hNamesMu = scaleFactor(tr_dataSMu_DEF, tr_mcTTToSemiLepDEF, "Single Muon Data", args.inputLFN, sfDIR)
    s_dataSEl, hNamesEl = scaleFactor(tr_dataSEl_DEF, tr_mcTTToSemiLepDEF, "Single Electron Data", args.inputLFN, sfDIR)
    s_dataMuHTs17DEF, hNamesHTMu_DEF = scaleFactor(tr_dataMuHTs17DEF, tr_mcTTToSemiLepDEF, "All Data", args.inputLFN, sfDIR)
    s_dataElHTs17DEF, hNamesHTEl_DEF = scaleFactor(tr_dataElHTs17DEF, tr_mcTTToSemiLepDEF, "All Data", args.inputLFN, sfDIR)

    s_dataMuHTs18AB, hNamesHTMu_AB = scaleFactor(tr_dataMuHTs18AB, tr_mcTTToSemiLep_18A, "All Data 18AB", args.inputLFN, sfDIR)
    s_dataElHTs18AB, hNamesHTEl_AB = scaleFactor(tr_dataElHTs18AB, tr_mcTTToSemiLep_18A, "All Data 18AB", args.inputLFN, sfDIR)
    s_dataMuHTs18CD, hNamesHTMu_CD = scaleFactor(tr_dataMuHTs18CD, tr_mcTTToSemiLep_18A, "All Data 18CD", args.inputLFN, sfDIR)
    s_dataElHTs18CD, hNamesHTEl_CD = scaleFactor(tr_dataElHTs18CD, tr_mcTTToSemiLep_18A, "All Data 18CD", args.inputLFN, sfDIR)

    effDIR.cd()

    if args.inputLFN == "17B":
        for hName in h_mcTTJets17B:
            h_HLTcompare[hName] = h_mcTTTTs17B[hName]
            if args.outputName == "ttsemi": h_HLTcompare[hName] = h_mcTTToSemiLeps17B[hName]
            elif args.outputName == "ttjets": h_HLTcompare[hName] = h_mcTTJets17B[hName]
            h_mcTTToSemiLeps[hName] = h_mcTTJets17B[hName]
            # h_mcTTToSemiLeps[hName].Write(hName)
        for hName in h_dataHTMHTs17B:
            h_dataHTMHTs[hName] = h_dataHTMHTs17B[hName]
            h_dataSMus[hName] = h_dataSMus17B[hName]
            h_dataSEls[hName] = h_dataSEls17B[hName]
            h_dataMuHTs[hName] = h_dataMuHTs17B[hName]
            h_dataElHTs[hName] = h_dataElHTs17B[hName]
            if "no-HLT" not in hName:
                tr_mcTTToSemiLep[hName] = tr_mcTTToSemiLep_B[hName]
                tr_dataHTMHT[hName] = tr_dataHTMHT_B[hName]
                tr_dataSEl[hName] = tr_dataSEl_B[hName]
                tr_dataSMu[hName] = tr_dataSMu_B[hName]
                tr_dataMuHTs[hName] = tr_dataMuHTs17B[hName]
                tr_dataElHTs[hName] = tr_dataElHTs17B[hName]
            # h_dataHTMHTs[hName].Write(hName)
            # h_dataSMus[hName].Write(hName)
            # h_dataSEls[hName].Write(hName)
            if args.outputName == "smu": h_HLTcompare[hName] = h_dataSMus17B[hName]
            elif args.outputName == "sel": h_HLTcompare[hName] = h_dataSEls17B[hName]
            elif args.outputName == "ht": h_HLTcompare[hName] = h_dataHTMHTs17B[hName]
            elif args.outputName == "htel": h_HLTcompare[hName] = h_dataElHTs17B[hName]
            elif args.outputName == "htmu": h_HLTcompare[hName] = h_dataMuHTs17B[hName]
    elif args.inputLFN == "17C":
        for hName in h_dataHTMHTs17C:
            h_HLTcompare[hName] = h_mcTTTTs17C[hName]
            h_mcTTToSemiLeps[hName] = h_mcTTJets17C[hName]
            h_dataHTMHTs[hName] = h_dataHTMHTs17C[hName]
            h_dataSMus[hName] = h_dataSMus17C[hName]
            h_dataSEls[hName] = h_dataSEls17C[hName]
            h_dataMuHTs[hName] = h_dataMuHTs17C[hName]
            h_dataElHTs[hName] = h_dataElHTs17C[hName]
            if "no-HLT" not in hName:
                tr_mcTTToSemiLep[hName] = tr_mcTTToSemiLep_C[hName]
                tr_dataHTMHT[hName] = tr_dataHTMHT_C[hName]
                tr_dataSEl[hName] = tr_dataSEl_C[hName]
                tr_dataSMu[hName] = tr_dataSMu_C[hName]
                tr_dataMuHTs[hName] = tr_dataMuHTs17C[hName]
                tr_dataElHTs[hName] = tr_dataElHTs17C[hName]
            # h_mcTTToSemiLeps[hName].Write(hName)
            # h_dataHTMHTs[hName].Write(hName)
            # h_dataSMus[hName].Write(hName)
            # h_dataSEls[hName].Write(hName)
            if args.outputName == "ttsemi": h_HLTcompare[hName] = h_mcTTToSemiLeps17C[hName]
            elif args.outputName == "ttjets": h_HLTcompare[hName] = h_mcTTJets17C[hName]
            elif args.outputName == "smu": h_HLTcompare[hName] = h_dataSMus17C[hName]
            elif args.outputName == "sel": h_HLTcompare[hName] = h_dataSEls17C[hName]
            elif args.outputName == "ht": h_HLTcompare[hName] = h_dataHTMHTs17C[hName]
            elif args.outputName == "htel": h_HLTcompare[hName] = h_dataElHTs17C[hName]
            elif args.outputName == "htmu": h_HLTcompare[hName] = h_dataMuHTs17C[hName]
    elif args.inputLFN == "17DEF":
        for hName in h_dataHTMHTs17DEF:
            h_HLTcompare[hName] = h_mcTTTTs17D[hName]
            #print(hName)
            #print(h_mcTTToSemiLeps17D[hName].GetName())
            #h_mcTTToSemiLeps[hName] = h_mcTTToSemiLeps17D[hName]
            #h_mcTTToSemiLeps[hName].Add(h_mcTTJets_DiLeps17D[hName])
            #h_mcTTToSemiLeps[hName].Add(h_mcTTHadronics17D[hName])
            h_mcTTToSemiLeps[hName] = h_mcTTJets17D[hName]
            # h_mcTTToSemiLeps[hName].Write(hName)
            h_dataHTMHTs[hName] = h_dataHTMHTs17DEF[hName]
            h_dataSMus[hName] = h_dataSMus17DEF[hName]
            h_dataSEls[hName] = h_dataSEls17DEF[hName]
            h_dataMuHTs[hName] = h_dataMuHTs17DEF[hName]
            h_dataElHTs[hName] = h_dataElHTs17DEF[hName]
            if "no-HLT" not in hName:
                tr_mcTTToSemiLep[hName] = tr_mcTTToSemiLepDEF[hName]
                tr_dataHTMHT[hName] = tr_dataHTMHT_DEF[hName]
                tr_dataSEl[hName] = tr_dataSEl_DEF[hName]
                tr_dataSMu[hName] = tr_dataSMu_DEF[hName]
                tr_dataMuHTs[hName] = tr_dataMuHTs17DEF[hName]
                tr_dataElHTs[hName] = tr_dataElHTs17DEF[hName]
            if args.outputName == "ttsemi": h_HLTcompare[hName] = h_mcTTToSemiLeps[hName]
            elif args.outputName == "ttjets": h_HLTcompare[hName] = h_mcTTJets17D[hName]
            elif args.outputName == "smu": h_HLTcompare[hName] = h_dataSMus17DEF[hName]
            elif args.outputName == "sel": h_HLTcompare[hName] = h_dataSEls17DEF[hName]
            elif args.outputName == "ht": h_HLTcompare[hName] = h_dataHTMHTs17DEF[hName]
            elif args.outputName == "htel": h_HLTcompare[hName] = h_dataElHTs17DEF[hName]
            elif args.outputName == "htmu": h_HLTcompare[hName] = h_dataMuHTs17DEF[hName]
    elif args.inputLFN == "18AB":
        #print(" ")
        for hName in h_dataHTMHTs18AB:
            if hName[-3:] == "Jet" or hName[-7:] == "OR_Jets" or hName[-6:] == "no-HLT": hName2 = hName + "2"
            else: hName2 = hName
            print(hName2)
            h_HLTcompare[hName2] = h_mcTTTTs18A[hName2]
            h_mcTTToSemiLeps[hName2] = h_mcTTJets18A[hName2]
            h_dataMuHTs[hName] = h_dataMuHTs18AB[hName]
            h_dataElHTs[hName] = h_dataElHTs18AB[hName]
            if "no-HLT" not in hName:
                tr_mcTTToSemiLep[hName2] = tr_mcTTToSemiLep_18A[hName2]
                tr_dataMuHTs[hName] = tr_dataMuHTs18AB[hName]
                tr_dataElHTs[hName] = tr_dataElHTs18AB[hName]
            if args.outputName == "ttsemi": h_HLTcompare[hName2] = h_mcTTToSemiLeps[hName2]
            elif args.outputName == "ttjets": h_HLTcompare[hName2] = h_mcTTJets18A[hName2]
            elif args.outputName == "htel": h_HLTcompare[hName] = h_dataElHTs18AB[hName]
            elif args.outputName == "htmu": h_HLTcompare[hName] = h_dataMuHTs18AB[hName]
    elif args.inputLFN == "18CD":
        for hName in h_dataHTMHTs18CD:
            if hName[-3:] == "Jet" or hName[-7:] == "OR_Jets" or hName[-6:] == "no-HLT": hName2 = hName + "2"
            else: hName2 = hName
            # h_HLTcompare[hName2] = h_mcTTTTs18A[hName2]
            h_mcTTToSemiLeps[hName2] = h_mcTTJets18A[hName2]
            h_dataMuHTs[hName] = h_dataMuHTs18CD[hName]
            h_dataElHTs[hName] = h_dataElHTs18CD[hName]
            if "no-HLT2" not in hName:
                tr_mcTTToSemiLep[hName2] = tr_mcTTToSemiLep_18A[hName2]
                tr_dataMuHTs[hName] = tr_dataMuHTs18CD[hName]
                tr_dataElHTs[hName] = tr_dataElHTs18CD[hName]
            if args.outputName == "ttsemi": h_HLTcompare[hName2] = h_mcTTToSemiLeps[hName2]
            elif args.outputName == "ttjets": h_HLTcompare[hName2] = h_mcTTJets18A[hName2]
            elif args.outputName == "htel": h_HLTcompare[hName2] = h_dataElHTs18CD[hName2]
            elif args.outputName == "htmu": h_HLTcompare[hName2] = h_dataMuHTs18CD[hName2]


    #  - Find efficiency ratio histogram dictionaries
    hltCompareTitle = "HLT comparison" + args.inputLFN + args.outputName
    tr_HLTcompare, tr2_HLTcompare = findTrigRatio(h_HLTcompare, hltCompareTitle, effDIR)

    #    ROOT.gStyle.SetOptTitle(0)
    #    ROOT.gStyle.SetOptStat(0)

    triggerCanvas.cd(1)
    ltx = TLatex()
    cutInfoPage(ltx, selCriteria, preSelCuts)
    pdfCreator(args, 0, triggerCanvas)

    # - Create text for legend
    # legString = cmsPlotString(arg.inputLFN)
    t1 = ROOT.TPaveText(0.18, 0.95, 0.93, 1, "nbNDC")
    t1.SetFillColorAlpha(0, 0.9)
    t1.SetTextSize(0.03)
    if args.outputName == "ttsemi": t1.AddText("#bf{CMS Preliminary}                                #sigma(t#bar{t}) = 374 pb (13TeV)")
    elif args.outputName == "ttjets": t1.AddText("#bf{CMS Preliminary}                                #sigma(t#bar{t}) = 831 pb (13TeV)")
    elif args.outputName == "smu": t1.AddText("#bf{CMS Preliminary}    " + runName + "    " + inLumi + " fb^{-1} (13TeV)")
    elif args.outputName == "sel": t1.AddText("#bf{CMS Preliminary}    " + runName + "    " + inLumi + " fb^{-1} (13TeV)")
    elif args.outputName == "htmu": t1.AddText("#bf{CMS Preliminary}    " + runName + "    " + inLumi + " fb^{-1} (13TeV)")
    elif args.outputName == "htel": t1.AddText("#bf{CMS Preliminary}    " + runName + "    " + inLumi + " fb^{-1} (13TeV)")
    elif args.outputName == "ht":  t1.AddText("#bf{CMS Preliminary}    " + runName + "    " + inLumi + " fb^{-1} (13TeV)")
    else: t1.AddText("#bf{CMS Preliminary}                           #sigma(t#bar{t}t#bar{t}) = 9.2 fb (13TeV)")
    t2 = ROOT.TPaveText(0.18, 0.95, 0.85, 1, "nbNDC")
    t2.SetFillColorAlpha(0, 0.9)
    t2.SetTextSize(0.03)
    t2.AddText(legString)
    ROOT.gStyle.SetLegendTextSize(0.028)

    hNames.sort()

    # Draw MC TTTT Motivation
    #hltTypes = ["Muon", "Electron", "Jet", "El_CROSS_Jets", "Mu_CROSS_Jets", "El_OR_Jets", "Mu_OR_Jets"]
    #if args.inputLFN == "18CD" or ("tt" in args.outputName and "18" in args.inputLFN): hltTypes = ["Muon", "Electron", "Jet2", "El_CROSS_Jets", "El_OR_Jets2", "Mu_OR_Jets2"] 
    #channels = ["Mu_", "El_"]
    #xAxes = ["HTpt_"] 
    #cv3 = [None] * 30
    #cv4 = [None] * 30
    #legend = [None] * 30
    #legend2 = [None] * 30
    #n_count = 0
    #n_count2 = 0
    #for channel in channels:
    #    for xAxis in xAxes:
    #        n_count += 2
    #        print(n_count)
    #        cv3[n_count] = triggerCanvas.cd(1)
    #        histName = "h_" + channel + xAxis + "no-HLT"
    #        histEntries = h_HLTcompare[histName].GetEntries()
    #        # h_HLTcompare[histName].GetXaxis().SetTitleOffset(1.3)
    #        xTitle = h_HLTcompare[histName].GetXaxis().GetTitle()
    #        xTitle = xTitle.replace("/ GeVc^{-1}", " [GeV]")
    #        yTitle = h_HLTcompare[histName].GetYaxis().GetTitle()
    #        yTitle = yTitle.replace("/ GeVc^{-1}", " [GeV]")
    #        zTitle = h_HLTcompare[histName].GetZaxis().GetTitle()
    #        zTitle = zTitle.replace("GeVc^{-1}", "GeV")
    #        h_HLTcompare[histName].GetZaxis().SetTitle(zTitle)
    #        #maxYs = h_HLTcompare[histName].GetMaximum()
    #        #h_HLTcompare[histName].SetMaximum(1.3 * maxYs)
    #        if "Mu" in histName: 
    #            newyTitle = yTitle.replace("Lepton", "Muon")
    #            h_HLTcompare[histName].GetYaxis().SetTitle(newyTitle)
    #        elif "El" in histName: 
    #            newyTitle = yTitle.replace("Lepton", "Electron")
    #            h_HLTcompare[histName].GetYaxis().SetTitle(newyTitle)
    #        h_HLTcompare[histName].SetLabelFont(42,"x")
    #        h_HLTcompare[histName].SetTitleFont(42,"x")
    #        h_HLTcompare[histName].SetLabelFont(42,"y")
    #        h_HLTcompare[histName].SetTitleFont(42,"y")
    #        h_HLTcompare[histName].SetLabelFont(42,"z")
    #        h_HLTcompare[histName].SetTitleFont(42,"z")
    #        h_HLTcompare[histName].SetLabelSize(0.04,"x")
    #        h_HLTcompare[histName].SetTitleSize(0.04,"x")
    #        h_HLTcompare[histName].SetLabelSize(0.04,"y")
    #        h_HLTcompare[histName].SetTitleSize(0.04,"y")
    #        h_HLTcompare[histName].Draw("COLZ")
    #        t1.Draw("same")
    #        triggerCanvas.Print(args.imageName + channel + xAxis + "no-HLT_ttttEv.png", "png")
    #        if xAxis == "nBJet_": h_HLTcompare[histName].GetXaxis().SetRangeUser(0, 7)
    #        elif xAxis == "nJet_": h_HLTcompare[histName].GetXaxis().SetRangeUser(6, 14)
    #        elif xAxis == "lepEta_": h_HLTcompare[histName].GetXaxis().SetRangeUser(-4, 4)
    #        elif xAxis == "lepPhi_": h_HLTcompare[histName].GetXaxis().SetRangeUser(-4, 4)
    #        elif xAxis == "HT_": h_HLTcompare[histName].GetXaxis().SetRangeUser(0, 3000)
    #        for hlt in hltTypes:
    #            if hlt == "Mu_CROSS_Jets" and (args.inputLFN == "17B" or "18" in args.inputLFN): continue
    #            if (channel == "El_") and ("Mu" in hlt): continue
    #            if (channel == "Mu_") and ("El" in hlt): continue
    #            histName = "h_" + channel + xAxis + hlt
    #            histEntries = h_HLTcompare[histName].GetEntries()                
                #for i in range(0, 17):
                #    binWidth = h_HLTcompare[histName].GetXaxis().GetBinWidth(i)
                #    binContent = h_HLTcompare[histName].GetBinContent(i)
                #    newBinContent = round(binContent / binWidth)
                #    h_HLTcompare[histName].SetBinContent(i, newBinContent)
                #h_HLTcompare[histName].SetLineColor(colourL)
                #if "OR" in histName: h_HLTcompare[histName].SetLineColor(6)
                #elif "CROSS" in histName: h_HLTcompare[histName].SetLineColor(8)
                # if "Mu_OR_Jets" not in hlt: 
     #           n_count += 1
     #           cv3[n_count] = triggerCanvas.cd(1)
     #           h_HLTcompare[histName].Draw("COLZ")
                #legEntry = hlt.replace("El_", "e^{#pm} ")
                #legEntry = legEntry.replace("Mu_", "#mu^{#pm} ")
                #legEntry = legEntry.replace("Jets2", "")
                #legEntry = legEntry.replace("Jets", "")
                #if era == "18CD" or (era == "18AB" and "tt" in args.outputName):
                #    legEntry = legEntry.replace("Jet2", "Hadronic")
                #else:
                #    legEntry = legEntry.replace("Jet", "Hadronic")
                #legEntry = legEntry.replace("Electron", "e^{#pm} ")
                #legEntry = legEntry.replace("Muon", "#mu^{#pm}  ")
                #legEntry = legEntry.replace("_", " ")
                #legEntry = legEntry + " HLT (%d)" % histEntries
                #legend[n_count].AddEntry(h_HLTcompare[histName], legEntry, 'l')
                #colourL += 2
      #          t1.Draw("same")
      #          triggerCanvas.Print(args.imageName + channel + xAxis + hlt + "ttttEv.png", "png")
            #if args.outputName == "ttjets": 
            #    legHeader = "#bf{t#bar{t} MC with " + runName + " HLTs}"
            #    legend[n_count].SetHeader(legHeader, "C")
            #elif args.outputName == "smu": legend[n_count].SetHeader("#bf{SingleMuon Samples after:}", "C")
            #elif args.outputName == "sel": legend[n_count].SetHeader("#bf{SingleElectron Samples after:}", "C")
            #elif args.outputName == "htmu": legend[n_count].SetHeader("#bf{#mu + jets Samples after:}", "C")
            #elif args.outputName == "htel": legend[n_count].SetHeader("#bf{e + jets Samples after:}", "C")
            #elif args.outputName == "ht": legend[n_count].SetHeader("#bf{HTMHT Samples after:}", "C")
            #else: 
            #    legHeader = "#bf{t#bar{t}t#bar{t} MC with " + runName + " HLTs}"
            #    legend[n_count].SetHeader(legHeader, "C")
            #legend[n_count].Draw("same")
            #triggerCanvas.Print(args.imageName + channel + xAxis + "ttttEv.png", "png")

            #n_count2 += 1
            #cv4[n_count2] = triggerCanvas.cd(1)
            #colourM = 2
            # ROOT.gStyle.SetErrorX(0.0001)
            #legend2[n_count2] = ROOT.TLegend(0.5, 0.16, 0.95, 0.5)
            #legend2[n_count2] = ROOT.TLegend(0.3, 0.8, 0.95, 0.95)
            #legend2[n_count2].SetFillColorAlpha(0, 0.9)
            #legend2[n_count2].SetBorderSize(0)
            #legend2[n_count2].SetNColumns(2)
       #     nhlt = 0
       #     for hlt in hltTypes:
       #         if hlt == "Mu_CROSS_Jets" and args.inputLFN == "17B": continue
       #         if hlt == "Mu_CROSS_Jets" and "18" in args.inputLFN: continue
       #         if (channel == "El_") and ("Mu" in hlt): continue
       #         if (channel == "Mu_") and ("El" in hlt): continue
       #         histName = "h_" + channel + xAxis + hlt
       #         n_count2 += 1
       #         cv4[n_count2] = triggerCanvas.cd(1)
            #    tr_HLTcompare[histName].SetMarkerColor(colourM)
            #    tr_HLTcompare[histName].SetLineColor(colourM)
            #    if "OR" in histName:
            #        tr_HLTcompare[histName].SetMarkerColor(6)
            #        tr_HLTcompare[histName].SetLineColor(6)
            #    elif "CROSS" in histName:
            #        tr_HLTcompare[histName].SetMarkerColor(8)
            #        tr_HLTcompare[histName].SetLineColor(8)
            #    tr_HLTcompare[histName].SetMarkerStyle(20)
            #    tr_HLTcompare[histName].SetMarkerSize(1.2)
            #    if nhlt == 0:
        #        tr_HLTcompare[histName].Draw("COLZ")
            #        cv4[n_count2].Update()
            #        graph1 = tr2_HLTcompare[histName].GetPaintedGraph()
            #        graph1.SetMinimum(0)
            #        graph1.SetMaximum(1.4)
            #        if xAxis == "nBJet_": graph1.GetXaxis().SetRangeUser(0, 7)
            #        elif xAxis == "nJet_": graph1.GetXaxis().SetRangeUser(6, 14)
            #        elif xAxis == "lepEta_": graph1.GetXaxis().SetRangeUser(-4, 4)
            #        elif xAxis == "lepPhi_": graph1.GetXaxis().SetRangeUser(-4, 4)
            #        elif xAxis == "HT_": graph1.GetXaxis().SetRangeUser(0, 3000)
            #        # graph1.GetXaxis().SetLabelSize(0.05)
            #        cv4[n_count2].Update()
            #        histEntries = h_HLTcompare[histName].GetEntries()
            #        nhlt += 1
            #    else:
            #        tr2_HLTcompare[histName].Draw("same")
            #        histEntries = h_HLTcompare[histName].GetEntries()
            #    effname = histName.replace("h_", "h_eff2")
            #    legEntry = hlt.replace("El_", "e^{#pm} ")
            #    legEntry = legEntry.replace("Mu_", "#mu^{#pm} ")
            #    legEntry = legEntry.replace("Jets2", "")
            #    legEntry = legEntry.replace("Jets", "")
            #    if era == "18CD" or (era == "18AB" and "tt" in args.outputName):
            #        legEntry = legEntry.replace("Jet2", "Hadronic")
            #    else:
            #        legEntry = legEntry.replace("Jet", "Hadronic")
            #    legEntry = legEntry.replace("Electron", "e^{#pm}  ")
            #    legEntry = legEntry.replace("Muon", "#mu^{#pm}  ")
            #    legEntry = legEntry.replace("_", " ")
            #    legEntry = legEntry + " HLT"
            #    legend2[n_count2].AddEntry(tr2_HLTcompare[histName], legEntry, "lep")
            #    colourM += 2
         #       t1.Draw("same")
         #       triggerCanvas.Print(args.imageName + channel + xAxis + hlt + "ttttEv.png", "png")
            #legend2[n_count2].SetHeader("#bf{t#bar{t} inclusive MC after:}", "C")
            # legend2[n_count2].SetHeader("#bf{t#bar{t}t#bar{t} inclusive MC after:}", "C")
            #legend2[n_count2].SetHeader("#bf{SingleMuon Samples after:}", "C")
            #if args.outputName == "ttjets": 
            #    legHeader = "#bf{t#bar{t} MC with" + runName + " HLTs}"
            #    legend2[n_count2].SetHeader(legHeader, "C")
            #elif args.outputName == "smu": legend2[n_count2].SetHeader("#bf{SingleMuon Samples after:}", "C")
            #elif args.outputName == "sel": legend2[n_count2].SetHeader("#bf{SingleElectron Samples after:}", "C")
            #elif args.outputName == "ht": legend2[n_count2].SetHeader("#bf{HTMHT Samples after:}", "C")
            #elif args.outputName == "htmu": legend2[n_count2].SetHeader("#bf{#mu + jets Samples after:}", "C")
            #elif args.outputName == "htel": legend2[n_count2].SetHeader("#bf{e + jets Samples after:}", "C")
            #else: 
            #    legHeader = "#bf{t#bar{t}t#bar{t} MC with " + runName + " HLTs}"
            #    legend2[n_count2].SetHeader(legHeader, "C")
            #legend2[n_count2].Draw("same")
            #triggerCanvas.Print(args.imageName + channel + xAxis + "ttttEf.png", "png")

    cv0 = [None] * 30
    cv1 = [None] * 30
    cv2 = [None] * 30
    n_count = 0

    #channels = ["Mu_", "El_"]
    #xAxes = ["HTpt_"] #, "pt_", "nJet_", "nBJet_", "lepEta_", "lepPhi_"]                                                                                                         
    #n_count = 0
    #for channel in channels:
    #    for xAxis in xAxes:
    #        n_count += 1
    #        hName = "h_" + channel + xAxis + "no-HLT"
    #        if "18CD" in era: hName = "h_" + channel + xAxis + "no-HLT2"
    #        cv0[n_count] = triggerCanvas.cd(1)
    #        if "18AB" in era: hName2 = hName + "2"
    #        else: hName2 = hName
    #        histEntries = h_mcTTToSemiLeps[hName2].GetEntries()
    #        histEntriesSMu = h_dataMuHTs[hName].GetEntries()
    #        histEntriesSEl = h_dataElHTs[hName].GetEntries()
    #        h_mcTTToSemiLeps[hName2].Draw("COLZ")
    #        h_mcTTToSemiLeps[hName2].GetZaxis().SetTitleOffset(1.8)
    #        t2.Clear()
    #        t2.AddText("#bf{CMS Preliminary} " + runName + " Baseline  #sigma(t#bar{t}) = 831 pb (13TeV)")
    #        t2.Draw("same")
    #        triggerCanvas.Print(args.imageName + "events/ttMC_{0}events{1}.png".format(hName2, era), "png")
    #        if "nBJet_" in hName: h_mcTTToSemiLeps[hName2].GetXaxis().SetRangeUser(0, 7)
    #        elif "nJet_" in hName: h_mcTTToSemiLeps[hName2].GetXaxis().SetRangeUser(6, 14)
    #        elif "lepEta_" in hName: h_mcTTToSemiLeps[hName2].GetXaxis().SetRangeUser(-4, 4)
    #        elif "lepPhi_" in hName: h_mcTTToSemiLeps[hName2].GetXaxis().SetRangeUser(-4, 4)
    #        elif "HT_" in hName: h_mcTTToSemiLeps[hName2].GetXaxis().SetRangeUser(0, 3000)
    #        h_mcTTToSemiLeps[hName2].SetTitle("t#bar{t} pair MC (%d)" % histEntries)

     #       if hName.find("Mu") != -1:
     #           n_count += 1
     #           print(">>>>>>>  {0}".format(hName))
     #           cv0[n_count] = triggerCanvas.cd(1)
     #           h_dataMuHTs[hName].Draw('COLZ')
     #           h_dataMuHTs[hName].GetZaxis().SetTitleOffset(1.8)
     #           t2String = legString.replace("Run", "#mu-chan. Run")
     #           t2.Clear()
     #           t2.AddText(t2String)
     #           imageName2 = args.imageName + "events/MU_{0}events{1}.png".format(hName, era)
     #       elif hName.find("El") != -1: 
     #           n_count += 1
     #           print(">>>>>>>  {0}".format(hName))
     #           cv0[n_count] = triggerCanvas.cd(1)
     #           h_dataElHTs[hName].Draw('COLZ')
     #           h_dataElHTs[hName].GetZaxis().SetTitleOffset(1.8)
     #           t2String = legString.replace("Run", "e-chan. Run")
     #           t2.Clear()
     #           t2.AddText(t2String)
     #           imageName2 = args.imageName + "events/EL_{0}events{1}.png".format(hName, era)
     #       t2.Draw("same")
        #pdfCreator(args, 1, triggerCanvas)
      #      triggerCanvas.Print(imageName2, "png")



    imageName2 = "default.png"
    if era == "18CD": 
        hNames = hNamesHTMu_CD
        hNames.append("h_El_HTpt_no-HLT2")
        hNames.append("h_Mu_HTpt_no-HLT2")
    else:
        hNames.append("h_El_HTpt_no-HLT")
        hNames.append("h_Mu_HTpt_no-HLT")
    for hn, hName in enumerate(hNames):
        # - Draw trigger hists
        trg = whatTrig(hName)
        era = args.inputLFN
        ##############################################
        #  Draw event distributions MC Data Compare  #
        ##############################################
        print("Histogram Name: " + hName)
        # if "_OR_" not in trg: continue
        if "no-HLT" not in hName: continue
        n_count += 1
        print(">>>>>>>  {0}".format(hName))
        cv0[n_count] = triggerCanvas.cd(1)
        if "18AB" in era: hName2 = hName + "2"
        else: hName2 = hName
        histEntries = h_mcTTToSemiLeps[hName2].GetEntries()
        histEntriesSMu = h_dataMuHTs[hName].GetEntries()
        histEntriesSEl = h_dataElHTs[hName].GetEntries()
        # for i in range(0, 17):
            # binWidth = h_mcTTToSemiLeps[hName2].GetXaxis().GetBinWidth(i)
            # binContent = h_mcTTToSemiLeps[hName2].GetBinContent(i)
            # newBinContent = round(binContent / binWidth)
            # h_mcTTToSemiLeps[hName2].SetBinContent(i, newBinContent)

            # binContent = h_dataMuHTs[hName].GetBinContent(i)
            # newBinContent = round(binContent / binWidth)
            # h_dataMuHTs[hName].SetBinContent(i, newBinContent)

            # binContent = h_dataElHTs[hName].GetBinContent(i)
            # newBinContent = round(binContent / binWidth)
            # h_dataElHTs[hName].SetBinContent(i, newBinContent)

        h_mcTTToSemiLeps[hName2].Draw("TEXT COLZ")
        h_mcTTToSemiLeps[hName2].GetZaxis().SetTitleOffset(1.8)
        t2.Clear()
        t2.AddText("#bf{CMS Preliminary}  " + runName + " Baseline #sigma(t#bar{t}) = 831 pb (13TeV)")
        t2.Draw("same")
        triggerCanvas.Print(args.imageName + "events/ttMC_{0}events{1}.png".format(hName2, era), "png")
        if "nBJet_" in hName: h_mcTTToSemiLeps[hName2].GetXaxis().SetRangeUser(0, 7)
        elif "nJet_" in hName: h_mcTTToSemiLeps[hName2].GetXaxis().SetRangeUser(6, 14)
        elif "lepEta_" in hName: h_mcTTToSemiLeps[hName2].GetXaxis().SetRangeUser(-4, 4)
        elif "lepPhi_" in hName: h_mcTTToSemiLeps[hName2].GetXaxis().SetRangeUser(-4, 4)
        elif "HT_" in hName: h_mcTTToSemiLeps[hName2].GetXaxis().SetRangeUser(0, 3000)
        h_mcTTToSemiLeps[hName2].SetTitle("t#bar{t} pair MC (%d)" % histEntries)

        if hName.find("Mu") != -1:
            n_count += 1
            print(">>>>>>>  {0}".format(hName))
            cv0[n_count] = triggerCanvas.cd(1)
            h_dataMuHTs[hName].Draw('TEXT COLZ')
            h_dataMuHTs[hName].GetZaxis().SetTitleOffset(1.8)
            t2String = legString.replace("Run", "#mu-chan. Run")
            t2.Clear()
            t2.AddText(t2String)
            imageName2 = args.imageName + "events/MU_{0}events{1}.png".format(hName, era)
        elif hName.find("El") != -1: 
            n_count += 1
            print(">>>>>>>  {0}".format(hName))
            cv0[n_count] = triggerCanvas.cd(1)
            h_dataElHTs[hName].Draw('TEXT COLZ')
            h_dataElHTs[hName].GetZaxis().SetTitleOffset(1.8)
            t2String = legString.replace("Run", "e-chan. Run")
            t2.Clear()
            t2.AddText(t2String)
            imageName2 = args.imageName + "events/EL_{0}events{1}.png".format(hName, era)
        t2.Draw("same")
        #pdfCreator(args, 1, triggerCanvas)
        triggerCanvas.Print(imageName2, "png")

        if "_OR_" not in trg: continue
        ####################################
        # - Draw trigger efficiency hists  #
        ####################################
        cv1[n_count] = triggerCanvas.cd(1)
        if "18" in era:
            if hName[-3:] == "Jet" or hName[-7:] == "OR_Jets": hName2 = hName + "2"
            else: hName2 = hName
        else: hName2 = hName
        tr_mcTTToSemiLep[hName2].Draw('TEXT COLZ')
        tr_mcTTToSemiLep[hName2].SetMinimum(0)
        tr_mcTTToSemiLep[hName2].SetMaximum(1.2)
        t2.Clear()
        t2.AddText("#bf{CMS Preliminary}  " + runName + " #sigma(t#bar{t}) = 831 pb (13TeV)")
        t2.Draw("same")
        triggerCanvas.Print(args.imageName + "teff/ttMC_{0}teff{1}.png".format(hName, era), "png")
        newName = tr_mcTTToSemiLep[hName2].GetName()
        if "nBJet_" in hName: graph1.GetXaxis().SetRangeUser(0, 7)
        elif "nJet_" in hName: graph1.GetXaxis().SetRangeUser(6, 14)
        elif "lepEta_" in hName: graph1.GetXaxis().SetRangeUser(-4, 4)
        elif "lepPhi_" in hName: graph1.GetXaxis().SetRangeUser(-4, 4)
        elif "HT_" in hName: graph1.GetXaxis().SetRangeUser(0, 3000)

        if "Mu" in hName:
            tr_dataMuHTs[hName].Draw('TEXT COLZ')
            tr_dataMuHTs[hName].SetMinimum(0)
            tr_dataMuHTs[hName].SetMaximum(1.2)
            t2String = legString.replace("Run", "#mu-chan. Run")
            t2.Clear()
            t2.AddText(t2String)            
        elif "El" in hName:
            tr_dataElHTs[hName].SetMinimum(0)
            tr_dataElHTs[hName].SetMaximum(1.2)
            tr_dataElHTs[hName].Draw('TEXT COLZ')
            t2String = legString.replace("Run", "e-chan. Run")
            t2.Clear()
            t2.AddText(t2String)
        t2.Draw("same")
        #pdfCreator(args, 1, triggerCanvas)
        triggerCanvas.Print(args.imageName + "teff/{0}_teff{1}.png".format(hName, era), "png")

        ##############################
        # - Draw scale factor hists  #
        ##############################
        cv2[n_count] = triggerCanvas.cd(1)
        t3 = ROOT.TPaveText(0.18, 0.95, 0.5, 1, "nbNDC")
        t3.SetFillColorAlpha(0, 0.9)
        t3.SetTextSize(0.03)
        t3.AddText("#bf{CMS Preliminary}")
        if era == "18CD":
            if "Jet2" in hName or "OR_Jets2" in hName: hName3 = hName.replace("2", "")
            else: hName3 = hName
        else: hName3 = hName
        if "Mu" in hName:
            if "nBJet_" in hName3: s_dataMuHTs17B[hName3].GetXaxis().SetRangeUser(0, 7)
            elif "nJet_" in hName3: s_dataMuHTs17B[hName3].GetXaxis().SetRangeUser(6, 14)
            elif "lepEta_" in hName3: s_dataMuHTs17B[hName3].GetXaxis().SetRangeUser(-4, 4)
            elif "lepPhi_" in hName3: s_dataMuHTs17B[hName3].GetXaxis().SetRangeUser(-4, 4)
            elif "HT_" in hName3: s_dataMuHTs17B[hName3].GetXaxis().SetRangeUser(0, 3000)
            s_dataMuHTs17B[hName3].Draw('TEXT COLZ')
            s_dataMuHTs17B[hName3].SetMinimum(0)
            s_dataMuHTs17B[hName3].SetMaximum(1.2)
            t2.Draw("same")
            #pdfCreator(args, 1, triggerCanvas)
            triggerCanvas.Print(args.imageName + "sf/MU_{0}_sf17B.png".format(hName), "png")


            s_dataMuHTs17C[hName3].Draw('TEXT COLZ')
            s_dataMuHTs17C[hName3].SetMinimum(0)
            s_dataMuHTs17C[hName3].SetMaximum(1.2)
            t2.Draw("same")
            #pdfCreator(args, 1, triggerCanvas)
            triggerCanvas.Print(args.imageName + "sf/MU_{0}_sf17C.png".format(hName), "png")


            s_dataMuHTs17DEF[hName3].Draw('TEXT COLZ')
            s_dataMuHTs17DEF[hName3].SetMinimum(0)
            s_dataMuHTs17DEF[hName3].SetMaximum(1.2)
            t2.Draw("same")
           # pdfCreator(args, 1, triggerCanvas)
            triggerCanvas.Print(args.imageName + "sf/MU_{0}_sf17DEF.png".format(hName), "png")


            s_dataMuHTs18AB[hName3].Draw('TEXT COLZ')
            s_dataMuHTs18AB[hName3].SetMinimum(0)
            s_dataMuHTs18AB[hName3].SetMaximum(1.2)
            t2.Draw("same")
            #pdfCreator(args, 1, triggerCanvas)
            triggerCanvas.Print(args.imageName + "sf/MU_{0}_sf18AB.png".format(hName), "png")

            if hName[-3:] == "Jet" or hName[-7:] == "OR_Jets": hName2 = hName + "2"
            else: hName2 = hName
            s_dataMuHTs18CD[hName2].Draw('TEXT COLZ')
            s_dataMuHTs18CD[hName2].SetMinimum(0)
            s_dataMuHTs18CD[hName2].SetMaximum(1.2)
            t2.Draw("same")
            #pdfCreator(args, 1, triggerCanvas)
            triggerCanvas.Print(args.imageName + "sf/MU_{0}_sf18CD.png".format(hName), "png")

            if ("HT" in hName or "pt" in hName) and "OR" in hName:
                with open('SF_17DEF_file.csv', mode='a') as sf_file:
                    sf_writer = csv.writer(sf_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                    nXBins = s_dataMuHTs17DEF[hName3].GetNbinsX()
                    nYBins = s_dataMuHTs17DEF[hName3].GetNbinsY()
                    for binX in range(1, nXBins + 1):
                        bin_lowEdgeX = s_dataMuHTs17DEF[hName3].GetXaxis().GetBinLowEdge(binX)
                        bin_upEdgeX = bin_lowEdgeX + s_dataMuHTs17DEF[hName3].GetXaxis().GetBinWidth(binX)
                        for binY in range(1, nYBins + 1):
                            bin_lowEdgeY = s_dataMuHTs17DEF[hName3].GetYaxis().GetBinLowEdge(binY)
                            bin_upEdgeY = bin_lowEdgeY + s_dataMuHTs17DEF[hName3].GetYaxis().GetBinWidth(binY)
                            bin_sf = s_dataMuHTs17DEF[hName3].GetBinContent(binX, binY)
                            bin_error = s_dataMuHTs17DEF[hName3].GetBinError(binX, binY)
                            if bin_sf <  0.00001: 
                                bin_sf = 1
                                bin_error = 0.001
                            write_list = [ hName3 , bin_lowEdgeX, bin_upEdgeX, bin_lowEdgeY, bin_upEdgeY, bin_sf, bin_error ]
                            sf_writer.writerow(write_list)
            
        elif "El" in hName:
            if "nBJet_" in hName3: s_dataElHTs17B[hName3].GetXaxis().SetRangeUser(0, 7)
            elif "nJet_" in hName3: s_dataElHTs17B[hName3].GetXaxis().SetRangeUser(6, 14)
            elif "lepEta_" in hName3: s_dataElHTs17B[hName3].GetXaxis().SetRangeUser(-4, 4)
            elif "lepPhi_" in hName3: s_dataElHTs17B[hName3].GetXaxis().SetRangeUser(-4, 4)
            elif "HT_" in hName3: s_dataElHTs17B[hName3].GetXaxis().SetRangeUser(0, 3000)
            s_dataElHTs17B[hName3].Draw('TEXT COLZ')
            s_dataElHTs17B[hName3].SetMinimum(0)
            s_dataElHTs17B[hName3].SetMaximum(1.2)
            t2.Draw("same")
            #pdfCreator(args, 1, triggerCanvas)
            triggerCanvas.Print(args.imageName + "sf/EL_{0}_sf17B.png".format(hName), "png")

            s_dataElHTs17C[hName3].Draw('TEXT COLZ')
            s_dataElHTs17C[hName3].SetMinimum(0)
            s_dataElHTs17C[hName3].SetMaximum(1.2)
            t2.Draw("same")
            #pdfCreator(args, 1, triggerCanvas)
            triggerCanvas.Print(args.imageName + "sf/EL_{0}_sf17C.png".format(hName), "png")

            s_dataElHTs17DEF[hName3].Draw('TEXT COLZ')
            s_dataElHTs17DEF[hName3].SetMinimum(0)
            s_dataElHTs17DEF[hName3].SetMaximum(1.2)
            t2.Draw("same")
            #pdfCreator(args, 1, triggerCanvas)
            triggerCanvas.Print(args.imageName + "sf/EL_{0}_sf17DEF.png".format(hName), "png")

            s_dataElHTs18AB[hName3].Draw('TEXT COLZ')
            s_dataElHTs18AB[hName3].SetMinimum(0)
            s_dataElHTs18AB[hName3].SetMaximum(1.2)
            t2.Draw("same")
            #pdfCreator(args, 1, triggerCanvas)
            triggerCanvas.Print(args.imageName + "sf/EL_{0}_sf18AB.png".format(hName), "png")


            if hName[-3:] == "Jet" or hName[-7:] == "OR_Jets": hName2 = hName + "2"
            else: hName2 = hName
            s_dataElHTs18CD[hName2].Draw('TEXT COLZ')
            s_dataElHTs18CD[hName2].SetMinimum(0)
            s_dataElHTs18CD[hName2].SetMaximum(1.2)
            t2.Draw("same")
            #pdfCreator(args, 1, triggerCanvas)
            triggerCanvas.Print(args.imageName + "sf/EL_{0}_sf18CD.png".format(hName2), "png")


            if ("HT" in hName) and "OR" in hName:
                with open('SF_17B_file.csv', mode='w') as sf_file:
                    sf_writer = csv.writer(sf_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                    nXBins = s_dataElHTs17B[hName3].GetNbinsX()
                    nYBins = s_dataElHTs17B[hName3].GetNbinsY()
                    for binX in range(1, nXBins + 1):
                        bin_lowEdgeX = s_dataElHTs17B[hName3].GetXaxis().GetBinLowEdge(binX)
                        bin_upEdgeX = bin_lowEdgeX + s_dataElHTs17B[hName3].GetXaxis().GetBinWidth(binX)
                        for binY in range(1, nYBins + 1):
                            bin_lowEdgeY = s_dataElHTs17B[hName3].GetYaxis().GetBinLowEdge(binY)
                            bin_upEdgeY = bin_lowEdgeY + s_dataElHTs17B[hName3].GetYaxis().GetBinWidth(binY)
                            bin_sf = s_dataElHTs17B[hName3].GetBinContent(binX, binY)
                            bin_error = s_dataElHTs17B[hName3].GetBinError(binX, binY)
                            if bin_sf <  0.00001: 
                                bin_sf = 1
                                bin_error = 0.001
                            write_list = [ hName3 , bin_lowEdgeX, bin_upEdgeX, bin_lowEdgeY, bin_upEdgeY, bin_sf, bin_error ]
                            sf_writer.writerow(write_list)
                with open('SF_17C_file.csv', mode='w') as sf_file:
                    sf_writer = csv.writer(sf_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                    nXBins = s_dataElHTs17C[hName3].GetNbinsX()
                    nYBins = s_dataElHTs17C[hName3].GetNbinsY()
                    for binX in range(1, nXBins + 1):
                        bin_lowEdgeX = s_dataElHTs17C[hName3].GetXaxis().GetBinLowEdge(binX)
                        bin_upEdgeX = bin_lowEdgeX + s_dataElHTs17C[hName3].GetXaxis().GetBinWidth(binX)
                        for binY in range(1, nYBins + 1):
                            bin_lowEdgeY = s_dataElHTs17C[hName3].GetYaxis().GetBinLowEdge(binY)
                            bin_upEdgeY = bin_lowEdgeY + s_dataElHTs17C[hName3].GetYaxis().GetBinWidth(binY)
                            bin_sf = s_dataElHTs17C[hName3].GetBinContent(binX, binY)
                            bin_error = s_dataElHTs17C[hName3].GetBinError(binX, binY)
                            if bin_sf <  0.00001: 
                                bin_sf = 1
                                bin_error = 0.001
                            write_list = [ hName3 , bin_lowEdgeX, bin_upEdgeX, bin_lowEdgeY, bin_upEdgeY, bin_sf, bin_error ]
                            sf_writer.writerow(write_list)
                with open('SF_17DEF_file.csv', mode='w') as sf_file:
                    sf_writer = csv.writer(sf_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                    nXBins = s_dataElHTs17DEF[hName3].GetNbinsX()
                    nYBins = s_dataElHTs17DEF[hName3].GetNbinsY()
                    for binX in range(1, nXBins + 1):
                        bin_lowEdgeX = s_dataElHTs17DEF[hName3].GetXaxis().GetBinLowEdge(binX)
                        bin_upEdgeX = bin_lowEdgeX + s_dataElHTs17DEF[hName3].GetXaxis().GetBinWidth(binX)
                        for binY in range(1, nYBins + 1):
                            bin_lowEdgeY = s_dataElHTs17DEF[hName3].GetYaxis().GetBinLowEdge(binY)
                            bin_upEdgeY = bin_lowEdgeY + s_dataElHTs17DEF[hName3].GetYaxis().GetBinWidth(binY)
                            bin_sf = s_dataElHTs17DEF[hName3].GetBinContent(binX, binY)
                            bin_error = s_dataElHTs17DEF[hName3].GetBinError(binX, binY)
                            if bin_sf <  0.00001: 
                                bin_sf = 1
                                bin_error = 0.001
                            write_list = [ hName3 , bin_lowEdgeX, bin_upEdgeX, bin_lowEdgeY, bin_upEdgeY, bin_sf, bin_error ]
                            sf_writer.writerow(write_list)
                with open('SF_18AB_file.csv', mode='w') as sf_file:
                    sf_writer = csv.writer(sf_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                    nXBins = s_dataElHTs18AB[hName3].GetNbinsX()
                    nYBins = s_dataElHTs18AB[hName3].GetNbinsY()
                    for binX in range(1, nXBins + 1):
                        bin_lowEdgeX = s_dataElHTs18AB[hName3].GetXaxis().GetBinLowEdge(binX)
                        bin_upEdgeX = bin_lowEdgeX + s_dataElHTs18AB[hName3].GetXaxis().GetBinWidth(binX)
                        for binY in range(1, nYBins + 1):
                            bin_lowEdgeY = s_dataElHTs18AB[hName3].GetYaxis().GetBinLowEdge(binY)
                            bin_upEdgeY = bin_lowEdgeY + s_dataElHTs18AB[hName3].GetYaxis().GetBinWidth(binY)
                            bin_sf = s_dataElHTs18AB[hName3].GetBinContent(binX, binY)
                            bin_error = s_dataElHTs18AB[hName3].GetBinError(binX, binY)
                            if bin_sf <  0.00001: 
                                bin_sf = 1
                                bin_error = 0.001
                            write_list = [ hName3 , bin_lowEdgeX, bin_upEdgeX, bin_lowEdgeY, bin_upEdgeY, bin_sf, bin_error ]
                            sf_writer.writerow(write_list)
                with open('SF_18CD_file.csv', mode='w') as sf_file:
                    sf_writer = csv.writer(sf_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                    nXBins = s_dataElHTs18CD[hName2].GetNbinsX()
                    nYBins = s_dataElHTs18CD[hName2].GetNbinsY()
                    for binX in range(1, nXBins + 1):
                        bin_lowEdgeX = s_dataElHTs18CD[hName2].GetXaxis().GetBinLowEdge(binX)
                        bin_upEdgeX = bin_lowEdgeX + s_dataElHTs18CD[hName2].GetXaxis().GetBinWidth(binX)
                        for binY in range(1, nYBins + 1):
                            bin_lowEdgeY = s_dataElHTs18CD[hName2].GetYaxis().GetBinLowEdge(binY)
                            bin_upEdgeY = bin_lowEdgeY + s_dataElHTs18CD[hName2].GetYaxis().GetBinWidth(binY)
                            bin_sf = s_dataElHTs18CD[hName2].GetBinContent(binX, binY)
                            bin_error = s_dataElHTs18CD[hName2].GetBinError(binX, binY)
                            if bin_sf <  0.00001: 
                                bin_sf = 1
                                bin_error = 0.001
                            write_list = [ hName2 , bin_lowEdgeX, bin_upEdgeX, bin_lowEdgeY, bin_upEdgeY, bin_sf, bin_error ]
                            sf_writer.writerow(write_list)

        eventDIR.cd()
        mcName = hName.replace("h_", "h_mcTTToSemiLep_")
        #h_mcTTToSemiLeps[hName].Write(mcName) # hName for all other eras other than 18AB is fine
        # htName = hName2.replace("h_", "h_dataHTMHT_")
        # h_dataMuHTs[hName2].Write(htName)
        muName = hName.replace("h_", "h_dataMu_")
        h_dataMuHTs[hName].Write(muName)
        eleName = hName.replace("h_", "h_dataEle_")
        h_dataElHTs[hName].Write(eleName)

        effDIR.cd()
        #tr_mcTTToSemiLep[hName].Write(mcName)
        # tr_dataHTMHT[hName3].Write(hName3 + "_HTtef")
        tr_dataMuHTs[hName].Write(hName + "_Mutef")
        tr_dataElHTs[hName].Write(hName + "_Eltef")

        sfDIR.cd()
        s_HTMHT[hName3].Write(hName + "_HTsf")
        s_dataSMu[hName3].Write(hName + "_Musf")
        s_dataSEl[hName3].Write(hName + "_Elsf")

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
