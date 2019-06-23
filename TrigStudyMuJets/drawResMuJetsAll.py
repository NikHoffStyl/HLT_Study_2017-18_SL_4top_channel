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
from plotStyle import *
from tools import *
#SetPlotStyle()
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)


def process_arguments():
    """ Process command-line arguments """

    parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--inputLFN", help="Set path to input file")
    parser.add_argument("-i", "--inputkey", default="_v2", help="Set name of input directory key")
    parser.add_argument("-o", "--outputName", default="NoPreTrig", help="Set name of output file")
    args = parser.parse_args()

    return args

def getFileName(pathToFile):
    """
        Find Root files in a given directory/path.
        Args:
        path (string): directory
        
        Returns: fileName (string): name of file given as input
        
        """
    foldersList = []
    foldersList = pathToFile.split("/")
    numberOfSteps = pathToFile.count("/")
    fileDir = "/".join(foldersList[:numberOfSteps]) + "/"
    fileName, fileExt = foldersList[-1].split(".")
    
    return fileDir, fileName


def pdfCreator(parg, arg, canvas, selCrit):
    """
    Create a pdf of histograms

    Args:
        parg (class): commandline arguments
        arg (int): print argument
        canvas (TCanvas): canvas which includes plot
        selCrit (dictionary): selection Criteria

    """
    time_ = datetime.now()
    minPt = selCrit["minJetPt"]
    inDir, inFile = getFileName(parg.inputLFN)
    filename = time_.strftime("TriggerPlots/" + parg.outputName + "%V_%y/" + inFile + "_" + minPt + "jetPt.pdf")
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


def sigmoidFit(x, par):
    """
    Write sigmoid function for TF1 class

    Args:
        x (list):  list of the dimension
        par (list): list of the parameters

    Returns:
        fitval : function
    """
    fitval = (par[0] / (1 + math.exp(-par[1] * (x[0]-par[2])))) + par[3]
    return fitval


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


def fitInfo(fit, printEqn, fitName, args):
    """

    Args:
        fit: fitted function
        printEqn: name of equation
        fitName: fit name
        args: cmd arguments

    Returns:

    """
    inDir, inFile = getFileName(args.inputLFN)
    fitFile = open("fitInfo" + inFile + ".txt", "a+")
    try:
        with fitFile:
            if printEqn == "s":
                fitFile.write("\n Equation given by: \n \t "
                              "y = (par[0] / (1 + math.exp(-par[1] * (x[0]-par[2])))) + par[3] \n\n")
                fitFile.write("Chi2, NDF, prob, par1, par2, par3, par4 \n")
            if printEqn == "t":
                fitFile.write("\n Equation given by: \n \t subFunc = (x[0] - par[1]) / (par[2] * math.sqrt(x[0])) \n \t"
                              "y = (0.5 * par[0] * (1 + ROOT.TMath.Erf(subFunc))) + par[3] \n\n")
                fitFile.write("Channel, Trigger, Plateau, Plateau Error, Turning Point, Turning Point Error, Chi2, NDF,"
                              "prob, Slope, Slope Error, Initial Plateau, Initial Plateau Error \n ")
            plateau = fit.GetParameter(0) + fit.GetParameter(3)
            plateauError = fit.GetParError(0) + fit.GetParError(3)
            fitFile.write("{0}, {1}, {2:.3f}, +/-, {3:.3f}, {4:.3f}, +/-, {5:.3f}, {6:.3f}, {7:.3f}, {8}, "
                          "{9:.3f}, +/- ,{10:.3f}, {11:.3f}, +/-, {12:.3f}\n " .format
                          (inFile, fitName, plateau, plateauError, fit.GetParameter(2), fit.GetParError(2),
                           fit.GetChisquare(), fit.GetNDF(), fit.GetProb(), fit.GetParameter(1), fit.GetParError(1),
                           fit.GetParameter(3), fit.GetParError(3)))

    except OSError:
        print("Could not open file!")


def inclusiveEfficiency(info, arg):
    """
    Args:
        info (string): information to be written to file
        arg (string): key name

    Returns:

    """
    inDir, inFile = getFileName(arg)
    fitFile = open("fitInfo" + inFile + ".txt", "a+")
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
    lx.DrawLatex(0.16, 0.25, "#bullet Muons: #bf{has tightId, |#eta|<%s and PFRelIso_all<%s (for at least 1)}"
                 % (selCrit["maxObjEta"], selCrit["maxPfRelIso04"]))


def cmsPlotString(args):
    """

    Args:
        args (string): command line arguments

    Returns:
        legStr (string): string containing channel details

    """
    if not args.find("TTToSemiLep") == -1:
        legStr = "CMS Preliminary #bf{                    t#bar{t} #rightarrow l #nu_{l} #plus jets                         117 pb^{-1} (13TeV)}"
    elif not args.find("ttjets") == -1:
        legStr = "CMS Preliminary #bf{                    t#bar{t} #rightarrow l #nu_{l} #plus jets                         117 pb^{-1} (13TeV)}"
    elif args.find("TTTT") != -1 and args.find("TTTT_") == -1:
        legStr = "#splitline{CMS}{t#bar{t}t#bar{t} #rightarrow l #nu_{l} #plus jets}"
        legStr = "CMS Preliminary #bf{                  t#bar{t}t#bar{t} #rightarrow l #nu_{l} #plus jets                    247 fb^{-1} (13TeV)}"
    elif args == "tttt_weights":
        legStr = "CMS Preliminary #bf{                t#bar{t}t#bar{t} #rightarrow l #nu_{l} #plus jets                    5.61 fb^{-1} (13TeV)}"
    elif not args.find("dataHTMHT17B") == -1:
        legStr = "CMS Preliminary #bf{                             HTMHT Data Run2017B                                      5.61 fb^{-1} (13TeV)}"
    elif not args.find("dataHTMHT17C") == -1:
        legStr = "CMS Preliminary #bf{                             HTMHT Data Run2017C                                      10.83 fb^{-1} (13TeV)}"
    elif not args.find("dataHTMHT17D") == -1:
        legStr = "CMS Preliminary #bf{                             HTMHT Data Run2017D-F                                    27.61 fb^{-1} (13TeV)}"
    elif not args.find("dataHTMHT17E") == -1:
        legStr = "CMS Preliminary #bf{                             HTMHT Data Run2017E                                      27.61 fb^{-1} (13TeV)}"
    elif not args.find("dataHTMHT17F") == -1:
        legStr = "CMS Preliminary #bf{                             HTMHT Data Run2017F                                      27.61 fb^{-1} (13TeV)}"
    elif not args.find("dataSMu17B") == -1:
        legStr = "CMS Preliminary #bf{                        Single Muon Data Run2017B                                      5.61 fb^{-1} (13TeV)}"
    elif not args.find("dataSMu17C") == -1:
        legStr = "CMS Preliminary #bf{                        Single Muon Data Run2017C                                      10.83 fb^{-1} (13TeV)}"
    elif not args.find("dataSMu17D") == -1:
        legStr = "CMS Preliminary #bf{                        Single Muon Data Run2017D-F                                    27.61 fb^{-1} (13TeV)}"
    elif not args.find("dataSMu17E") == -1:
        legStr = "CMS Preliminary #bf{                        Single Muon Data Run2017E                                      27.61 fb^{-1} (13TeV)}"
    elif not args.find("dataSMu17F") == -1:
        legStr = "CMS Preliminary #bf{                        Single Muon Data Run2017F                                      27.61 fb^{-1} (13TeV)}"
    elif not args.find("dataSEl17B") == -1:
        legStr = "CMS Preliminary #bf{                   Single Electron Data Run2017B                                       5.61 fb^{-1} (13TeV)}"
    elif not args.find("dataSEl17C") == -1:
        legStr = "CMS Preliminary #bf{                   Single Electron Data Run2017C                                       10.83 fb^{-1} (13TeV)}"
    elif not args.find("dataSEl17D") == -1:
        legStr = "CMS Preliminary #bf{                   Single Electron Data Run2017D-F                                     27.61 fb^{-1} (13TeV)}"
    elif not args.find("dataSEl17E") == -1:
        legStr = "CMS Preliminary #bf{                   Single Electron Data Run2017E                                       27.61 fb^{-1} (13TeV)}"
    elif not args.find("dataSEl17F") == -1:
        legStr = "CMS Preliminary #bf{                   Single Electron Data Run2017F                                       27.61 fb^{-1} (13TeV)}"
    elif not args.find("Wjets") == -1:
        legStr = "CMS Preliminary #bf{                    W #rightarrow l #nu_{l} #plus jets                         524.2 pb^{-1} (13TeV)}"
    else:
        legStr = "CMS Preliminary"

    return legStr


def getFileContents(fileName, elmList):
    """

    Args:
        fileName (string): path/to/file
        elmList (bool): if true then dictionary elements are lists else strings

    Returns:
        fileContents (dictionary): file contents given as a dictionary

    """
    fileContents = {}
    with open(fileName) as f:
        for line in f:
            if line.find(":") == -1: continue
            (key1, val) = line.split(": ")
            c = len(val) - 1
            val = val[0:c]
            if elmList is False:
                fileContents[key1] = val
            else:
                fileContents[key1] = val.split(", ")
    return fileContents


def inputFileName(arg, arg2):
    """

    Args:
        arg (string): string that specifies decay and decay channel
        selCrit (dictionary): dictionary of content selectionCriteria.txt

    Returns:
        inFile (string): input file name

    """
    #inFile = "OutFiles/Histograms" + arg2 + "/" + arg + ".root"
    inFile = arg
    return inFile

def getSingleHist(colour=1,lineStyle=1, histName="", fillColour=None ):
    hist = ROOT.gDirectory.Get(histName)
    if not (hist):
        print(histName + "is empty")
        return 0
    hist.SetLineColor(colour)
    hist.SetLineStyle(lineStyle)
    if not fillColour == None: hist.SetFillColorAlpha(fillColour, 0.35)
    hist.SetDirectory(0)
    return hist

def getHistogramsFrom(fileName, trigList, args):
    h_jetHt = {}
    h_jetMult = {}
    h_jetBMult = {}
    h_jetEta = {}
    h_jetPhi = {}
    h_jetMap = {}
    h_muonPt = {}
    h_muonEta = {}
    h_muonPhi = {}
    h_muonMap = {}
    h_muonIsolation = {}
    h_muonIsoPt ={}
    h_metPt = {}
    h_metPhi = {}

    h_mediumMuonMult = {}
    h_mediumMuonTightPt = {}
    h_muonEtaNomedium = {}
    h_muonPhiNomedium = {}
    h_muonMapNomedium = {}
    h_muonIsolationNomedium = {}
    h_muonIsoPtNomedium = {}

    print("Opening %s " % fileName)
    histFile = ROOT.TFile.Open(fileName)
    histFile.cd("plots")

    # - Histograms
    h_jetHt["notrigger"] = getSingleHist(histName="h_jetHt_notrigger")
    h_jetMult["notrigger"] = getSingleHist(histName="h_jetMult_notrigger")
    h_jetBMult["notrigger"] = getSingleHist(histName="h_jetBMult_notrigger")
    h_jetEta["notrigger"] = getSingleHist(histName="h_jetEta_notrigger")
    h_jetPhi["notrigger"] = getSingleHist(histName="h_jetPhi_notrigger")
    h_jetMap["notrigger"] = getSingleHist(histName="h_jetMap_notrigger")

    h_muonPfRelIso04_all = getSingleHist(histName="h_muonRelIso04_all")

    h_muonPt["notrigger"] = getSingleHist(histName="h_muonPt_notrigger")
    h_mediumMuonMult["notrigger"] = getSingleHist(histName="h_mediumMuonMult_notrigger")
    h_mediumMuonTightPt["notrigger"] = getSingleHist(histName="h_mediumMuonTightPt_notrigger")
    if not fileName.find("TTT") == -1 or not fileName.find("Wjets") == -1 or not fileName.find("pythia") == -1:
        h_jetHt["nobaseline"] = getSingleHist(histName="h_jetHt_nobaseline")
        h_muonGenPartFlav = getSingleHist(histName="h_muonGenPartFlav")
        h_muonGenPartIdx = getSingleHist(histName="h_muonGenPartIdx")

        h_muonPt["nobaseline"] = getSingleHist(1, 10, "h_muonPt_nobaseline")
        h_muonPt["prompt"] = getSingleHist(4, 1, "h_muonPt_prompt")
        h_muonPt["from_b"] = getSingleHist(2, 1, "h_muonPt_from_b")
        h_muonPt["from_c"] = getSingleHist(3, 1, "h_muonPt_from_c")
        h_muonPt["from_light_or_unknown"] = getSingleHist(6, 1, "h_muonPt_from_light_or_unknown")
        h_muonPt["unmatched"] = getSingleHist(9, 1, "h_muonPt_unmatched")
        h_muonPt["from_prompt_tau"] = getSingleHist(8, 1, "h_muonPt_from_prompt_tau")
        h_muonPt["prompt0"] = getSingleHist(4, 1, "h_muonPt_prompt0")
        h_muonPt["from_b0"] = getSingleHist(2, 1, "h_muonPt_from_b0")
        h_muonPt["from_c0"] = getSingleHist(3, 1, "h_muonPt_from_c0")
        h_muonPt["from_light_or_unknown0"] = getSingleHist(6, 1, "h_muonPt_from_light_or_unknown0")
        h_muonPt["unmatched0"] = getSingleHist(colour=9, histName="h_muonPt_unmatched0")
        h_muonPt["from_prompt_tau0"] = getSingleHist(colour=8, histName="h_muonPt_from_prompt_tau0")

        h_mediumMuonTightPt["prompt"] = getSingleHist(4, 1, "h_mediumMuonTightPt_prompt")
        h_mediumMuonTightPt["from_b"] = getSingleHist(2, 1, "h_mediumMuonTightPt_from_b")
        h_mediumMuonTightPt["from_c"] = getSingleHist(3, 1, "h_mediumMuonTightPt_from_c")
        h_mediumMuonTightPt["from_light_or_unknown"] = getSingleHist(6, 1, "h_mediumMuonTightPt_from_light_or_unknown")
        h_mediumMuonTightPt["unmatched"] = getSingleHist(9, 1, "h_mediumMuonTightPt_unmatched")
        h_mediumMuonTightPt["from_prompt_tau"] = getSingleHist(8, 1, "h_mediumMuonTightPt_from_prompt_tau")

        h_mediumMuonMult["prompt"] = getSingleHist(4, 1, "h_mediumMuonMult_prompt")
        h_mediumMuonMult["from_b"] = getSingleHist(2, 1, "h_mediumMuonMult_from_b")
        h_mediumMuonMult["from_c"] = getSingleHist(3, 1, "h_mediumMuonMult_from_c")
        h_mediumMuonMult["from_light_or_unknown"] = getSingleHist(6, 1, "h_mediumMuonMult_from_light_or_unknown")
        h_mediumMuonMult["unmatched"] = getSingleHist(9, 1, "h_mediumMuonMult_unmatched")
        h_mediumMuonMult["from_prompt_tau"] = getSingleHist(8, 1, "h_mediumMuonMult_from_prompt_tau")

    h_muonEta["notrigger"] = getSingleHist(histName="h_muonEta_notrigger")
    h_muonPhi["notrigger"] = getSingleHist(histName="h_muonPhi_notrigger")
    h_muonMap["notrigger"] = getSingleHist(histName="h_muonMap_notrigger")

    h_muonIsolation["notrigger"] = getSingleHist(histName="h_muonIsolation_notrigger")
    h_muonIsoPt["notrigger"] = getSingleHist(histName="h_muonIsoPt_notrigger") 

    h_muonEtaNomedium["notrigger"] = getSingleHist(histName="h_muonEtaNomedium_notrigger")
    h_muonPhiNomedium["notrigger"] = getSingleHist(histName="h_muonPhiNomedium_notrigger")
    h_muonMapNomedium["notrigger"] = getSingleHist(histName="h_muonMapNomedium_notrigger")

    h_muonIsolationNomedium["notrigger"] = getSingleHist(histName="h_muonIsolationNomedium_notrigger")
    h_muonIsoPtNomedium["notrigger"] = getSingleHist(histName="h_muonIsoPtNomedium_notrigger")

    h_metPt["notrigger"] = getSingleHist(histName="h_metPt_notrigger")
    h_metPhi["notrigger"] = getSingleHist(histName="h_metPhi_notrigger")

    i = 2
    style = [1, 8, 9, 10]
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            h_jetHt[tg] = getSingleHist(i , 1, "h_jetHt_" + tg, i)
            h_jetMult[tg] = getSingleHist(i , 1, "h_jetMult_" + tg, i)
            h_jetBMult[tg] = getSingleHist(i , 1, "h_jetBMult_" + tg, i)
            h_jetEta[tg] = getSingleHist(i , 1, "h_jetEta_" + tg, i)
            h_jetPhi[tg] = getSingleHist(i , 1, "h_jetPhi_" + tg, i)
            h_jetMap[tg] = getSingleHist(i , 1, "h_jetMap_" + tg, i)

            h_muonPt[tg] = getSingleHist(i , 1, "h_muonPt_" + tg, i)
            h_muonEta[tg] = getSingleHist(i , 1, "h_muonEta_" + tg, i)
            h_muonPhi[tg] = getSingleHist(i , 1, "h_muonPhi_" + tg, i)
            h_muonMap[tg] = getSingleHist(i , 1, "h_muonMap_" + tg, i)
            h_muonIsolation[tg] = getSingleHist(i , 1, "h_muonIsolation_" + tg, i)
            h_muonIsoPt[tg] = getSingleHist(i , 1, "h_muonIsoPt_" + tg, i)

            h_mediumMuonTightPt[tg] = getSingleHist(i , 1, "h_mediumMuonTightPt_" + tg, i)
            h_mediumMuonMult[tg] = getSingleHist(i , 1, "h_mediumMuonMult" + tg, i)

            h_muonEtaNomedium[tg] = getSingleHist(i , 1, "h_muonEtaNomedium_" + tg, i)
            h_muonPhiNomedium[tg] = getSingleHist(i , 1, "h_muonPhiNomedium_" + tg, i)
            h_muonMapNomedium[tg] = getSingleHist(i , 1, "h_muonMapNomedium_" + tg, i)

            h_muonIsolationNomedium[tg] = getSingleHist(i , 1, "h_muonIsolationNomedium_" + tg, i)
            h_muonIsoPtNomedium[tg] = getSingleHist(i , 1, "h_muonIsoPtNomedium_" + tg, i)

            if not fileName.find("TTT") == -1 or not fileName.find("Wjets") == -1 or not fileName.find("pythia") == -1:
                h_muonPt["prompt" + tg] = getSingleHist(4, 1, "h_muonPt_prompt" + tg, 4)
                h_muonPt["from_b" + tg] = getSingleHist(2, 1, "h_muonPt_from_b" + tg, 2)
                h_muonPt["from_c" + tg] = getSingleHist(3, 1, "h_muonPt_from_c" + tg, 3)
                h_muonPt["from_light_or_unknown" + tg] = getSingleHist(6, 1, "h_muonPt_from_light_or_unknown" + tg, 6)
                h_muonPt["unmatched" + tg] = getSingleHist(9, 1, "h_muonPt_unmatched" + tg, 8)
                h_muonPt["from_prompt_tau" + tg] = getSingleHist(8, 1, "h_muonPt_from_prompt_tau" + tg, 9)

                h_mediumMuonTightPt["prompt" + tg] = getSingleHist(4, 1, "h_mediumMuonTightPt_prompt" + tg, 4)
                h_mediumMuonTightPt["from_b" + tg] = getSingleHist(2, 1, "h_mediumMuonTightPt_from_b" + tg, 2)
                h_mediumMuonTightPt["from_c" + tg] = getSingleHist(3, 1, "h_mediumMuonTightPt_from_c" + tg, 3)
                h_mediumMuonTightPt["from_light_or_unknown" + tg] = getSingleHist(6, 1, "h_mediumMuonTightPt_from_light_or_unknown" + tg, 6)
                h_mediumMuonTightPt["unmatched" + tg] = getSingleHist(9, 1, "h_mediumMuonTightPt_unmatched" + tg, 8)
                h_mediumMuonTightPt["from_prompt_tau" + tg] = getSingleHist(8, 1, "h_mediumMuonTightPt_from_prompt_tau" + tg, 9)

                h_mediumMuonMult["prompt" + tg] = getSingleHist(4, 1, "h_mediumMuonMult_prompt" + tg, 4)
                h_mediumMuonMult["from_b" + tg] = getSingleHist(2, 1, "h_mediumMuonMult_from_b" + tg, 2)
                h_mediumMuonMult["from_c" + tg] = getSingleHist(3, 1, "h_mediumMuonMult_from_c" + tg, 3)
                h_mediumMuonMult["from_light_or_unknown" + tg] = getSingleHist(6, 1, "h_mediumMuonMult_from_light_or_unknown" + tg, 6)
                h_mediumMuonMult["unmatched" + tg] = getSingleHist(9, 1, "h_mediumMuonMult_unmatched" + tg, 8)
                h_mediumMuonMult["from_prompt_tau" + tg] = getSingleHist(8, 1, "h_mediumMuonMult_from_prompt_tau" + tg, 9)

            h_metPt[tg] = getSingleHist(i, 1, "h_metPt_" + tg, i)
            h_metPhi[tg] = getSingleHist(i, 1, "h_metPhi_" + tg, i)

            i += 2

    # - Events histogram
    #h_eventsPrg = getSingleHist("h_eventsPrg")
    #if not h_eventsPrg:
     #   print("h_eventsPrg histogram is empty")

    return h_jetHt, h_jetMult, h_jetBMult, h_jetEta, h_jetPhi, h_muonPt, h_muonEta, h_muonPhi, h_muonIsolation, h_metPt, h_metPhi


def addThreeHists(h1, h2,h3):
    h_sum = {}
    for hname1 in h1:
        for hname2 in h2:
            if hname1 == hname2:
                h_sum[hname1] = h1[hname1]
                h_sum[hname1].Add(h2[hname1])
                for hname3 in h3:
                    if hname3 == hname1:
                        h_sum[hname1].Add(h3[hname1])
    return h_sum

def divideHists(numeratr, denominatr):
    ratioHists = numeratr
    ratioHists.Divide(denominatr)
    return ratioHists


def drawEventHists(h1, trigList, xAxis, cvv, rebin, rebYN):
    nDim = (rebin.ndim) - 1
    if rebYN is True: h1["notrigger"] = h1["notrigger"].Rebin(16, "h_jetHT", rebin)
    histEntries = h1["notrigger"].GetEntries()
    h1["notrigger"].SetTitle("No HLT selection (%d) ; %s ;Number of Events" % (histEntries, xAxis))
    numBins = h1["notrigger"].GetNbinsX()
    for i in range (0, numBins):
        binWidth = h1["notrigger"].GetXaxis().GetBinWidth(i)
        binContent = h1["notrigger"].GetBinContent(i)
        newBinContent = round(binContent/binWidth)
        h1["notrigger"].SetBinContent(i, newBinContent)
    h1["notrigger"].Draw()
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            if rebYN is True: h1[tg] = h1[tg].Rebin(16, "h_jetHT_" + tg, rebin)
            histEntries = h1[tg].GetEntries()
            h1[tg].SetTitle("%s (%d) ;%s ;Number of Events" % (tg,histEntries, xAxis))
            for i in range (0,13):
                binWidth = h1[tg].GetXaxis().GetBinWidth(i)
                binContent = h1[tg].GetBinContent(i)
                newBinContent = round(binContent/binWidth)
                h1[tg].SetBinContent(i, newBinContent)
            h1[tg].Draw('same')
    ROOT.gStyle.SetLegendTextSize(0.025)
    cvv.BuildLegend(0.4, 0.55, 0.9, 0.9)


def main(argms):
    """ This code merges histograms, only for specific root file """

    if not argms.inputLFN.find("17B") == -1:
        if not argms.inputLFN.find("data") == -1: trigList = getFileContents("../myInFiles/2017ABtrigList.txt", True)  # fro data
        elif not argms.inputLFN.find("TTT") == -1: trigList = getFileContents("../myInFiles/trigList.txt", True)  # for mc
    elif not argms.inputLFN.find("17C") == -1:
        trigList = getFileContents("../myInFiles/2017CtrigList.txt", True)
    elif not argms.inputLFN.find("17D") or argms.inputLFN.find("17E") or argms.inputLFN.find("17F") == -1:
        trigList = getFileContents("../myInFiles/2017DEFtrigList.txt", True)
    else:
        trigList = getFileContents("../myInFiles/trigList.txt", True)
    preSelCuts = getFileContents("../myInFiles/preSelectionCuts.txt", False)
    selCriteria = getFileContents("selectionCriteria.txt", False)

    if not argms.inputLFN.find("17D") ==-1 and argms.inputLFN.find("TTT") == -1 and argms.inputLFN.find("Wjets") == -1 and argms.inputLFN.find("pythia") == -1:
        print(">>>> ADDING 3HISTS >>>")
        fileE = argms.inputLFN.replace("17D", "17E")
        fileF = argms.inputLFN.replace("17D", "17F")
        inputFile1 = argms.inputLFN  #inputFileName(argms.inputLFN, argms.inputkey)
        inputFile2 = fileE  #inputFileName(fileE, argms.inputkey)
        inputFile3 = fileF  #inputFileName(fileF, argms.inputkey)
        h_jetHt1, h_jetMult1, h_jetBMult1, h_jetEta1, h_jetPhi1, h_muonPt1, h_muonEta1, h_muonPhi1, h_muonIsolation1, h_metPt1, h_metPhi1 = getHistogramsFrom(inputFile1, trigList, argms)
        h_jetHt2, h_jetMult2, h_jetBMult2, h_jetEta2, h_jetPhi2, h_muonPt2, h_muonEta2, h_muonPhi2, h_muonIsolation2, h_metPt2, h_metPhi2 = getHistogramsFrom(inputFile2, trigList, argms)
        h_jetHt3, h_jetMult3, h_jetBMult3, h_jetEta3, h_jetPhi3, h_muonPt3, h_muonEta3, h_muonPhi3, h_muonIsolation3, h_metPt3, h_metPhi3 = getHistogramsFrom(inputFile3, trigList, argms)
        h_jetHt = addThreeHists(h_jetHt1, h_jetHt2, h_jetHt3)
        h_jetMult = addThreeHists(h_jetMult1, h_jetMult2, h_jetMult3)
        h_jetBMult = addThreeHists(h_jetBMult1, h_jetBMult2, h_jetBMult3)
        h_jetEta = addThreeHists(h_jetEta1, h_jetEta2, h_jetEta3)
        h_jetPhi = addThreeHists(h_jetPhi1, h_jetPhi2, h_jetPhi3)
        h_muonPt = addThreeHists(h_muonPt1, h_muonPt2, h_muonPt3)
        h_muonEta = addThreeHists(h_muonEta1, h_muonEta2, h_muonEta3)
        h_muonPhi = addThreeHists(h_muonPhi1, h_muonPhi2,h_muonPhi3)
        h_muonIsolation = addThreeHists(h_muonIsolation1, h_muonIsolation2, h_muonIsolation3)
        h_metPt = addThreeHists(h_metPt1, h_metPt2, h_metPt3)
        h_metPhi = addThreeHists(h_metPhi1, h_metPhi2, h_metPhi3)
    else:
#        inDir, inFile = getFileName(argms.inputLFN)
#        inputFile = inDir + inFile
        h_jetHt, h_jetMult, h_jetBMult, h_jetEta, h_jetPhi, h_muonPt, h_muonEta, h_muonPhi, h_muonIsolation, h_metPt, h_metPhi = getHistogramsFrom(argms.inputLFN, trigList, argms)

        if not argms.inputLFN.find("TTT") == -1 or not argms.inputLFN.find("Wjets") == -1 or not argms.inputLFN.find("pythia") == -1:
            if not argms.inputLFN.find("17B") ==-1:
                trigListB = getFileContents("../myInFiles/2017ABtrigList.txt", True)
                inputFiled = "OutFiles/Histograms_LooseMuInfo_vetoing/SingleMuon_Run2017B-Nano14Dec2018-v117B.root"
                h_jetHtd, h_jetMultd, h_jetBMultd, h_jetEtad, h_jetPhid, h_muonPtd, h_muonEtad, h_muonPhid, h_muonIsolationd, h_metPtd, h_metPhid = getHistogramsFrom(inputFiled, trigListB, argms)
            elif not argms.inputLFN.find("17C") ==-1:
                inputFiled = "OutFiles/Histograms_LooseMuInfo_vetoing/SingleMuon_Run2017C-Nano14Dec2018-v117C.root"  # dataSMu17C_6Jets1Mu30jPt-v117C.root"
                h_jetHtd, h_jetMultd, h_jetBMultd, h_jetEtad, h_jetPhid, h_muonPtd, h_muonEtad, h_muonPhid, h_muonIsolationd, h_metPtd, h_metPhid = getHistogramsFrom(inputFiled, trigList, argms)
            elif not argms.inputLFN.find("17D") ==-1:
                inputFiled1 = "OutFiles/Histograms_LooseMuInfo_vetoing/SingleMuon_Run2017D-Nano14Dec2018-v117DEF.root" # dataSMu17D_6Jets1Mu30jPt-v117DEF.root"
                h_jetHtd1, h_jetMultd1, h_jetBMultd1, h_jetEtad1, h_jetPhid1, h_muonPtd1, h_muonEtad1, h_muonPhid1, h_muonIsolationd1, h_metPtd1, h_metPhid1 = getHistogramsFrom(inputFiled1, trigList, argms)
                inputFiled2 = "OutFiles/Histograms_LooseMuInfo_vetoing/SingleMuon_Run2017E-Nano14Dec2018-v117DEF.root"  # dataSMu17E_6Jets1Mu30jPt-v117DEF.root"
                h_jetHtd2, h_jetMultd2, h_jetBMultd2, h_jetEtad2, h_jetPhid2, h_muonPtd2, h_muonEtad2, h_muonPhid2, h_muonIsolationd2, h_metPtd2, h_metPhid2 = getHistogramsFrom(inputFiled2, trigList, argms)
                inputFiled3 = "OutFiles/Histograms_LooseMuInfo_vetoing/SingleMuon_Run2017F-Nano14Dec2018-v117DEF.root"  # dataSMu17F_6Jets1Mu30jPt-v117DEF.root"
                h_jetHtd3, h_jetMultd3, h_jetBMultd3, h_jetEtad3, h_jetPhid3, h_muonPtd3, h_muonEtad3, h_muonPhid3, h_muonIsolationd3, h_metPtd3, h_metPhid3 = getHistogramsFrom(inputFiled3, trigList, argms)
                h_jetHtd = addThreeHists(h_jetHtd1, h_jetHtd2, h_jetHtd3)
                h_jetMultd = addThreeHists(h_jetMultd1, h_jetMultd2, h_jetMultd3)
                h_jetBMultd = addThreeHists(h_jetBMultd1, h_jetBMultd2, h_jetBMultd3)
                h_jetEtad = addThreeHists(h_jetEtad1, h_jetEtad2, h_jetEtad3)
                h_jetPhid = addThreeHists(h_jetPhid1, h_jetPhid2, h_jetPhid3)
                h_muonPtd = addThreeHists(h_muonPtd1, h_muonPtd2, h_muonPtd3)
                h_muonEtad = addThreeHists(h_muonEtad1, h_muonEtad2, h_muonEtad3)
                h_muonPhid = addThreeHists(h_muonPhid1, h_muonPhid2,h_muonPhid3)
                h_muonIsolationd = addThreeHists(h_muonIsolationd1, h_muonIsolationd2, h_muonIsolationd3)
                h_metPtd = addThreeHists(h_metPtd1, h_metPtd2, h_metPtd3)
                h_metPhid = addThreeHists(h_metPhid1, h_metPhid2, h_metPhid3)

    h_TriggerRatio = {}

    f_jetHt = {}
    f_muonPt = {}

    # - Create canvases
    triggerCanvas = ROOT.TCanvas('triggerCanvas', 'Triggers', 900, 500)#900,500  # 1100 600
    triggerCanvas.SetGrid()

    i = 2
    style = [1, 8, 9, 10]
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:

            f_jetHt[tg] = ROOT.TF1('jetHt' + tg, turnOnFit, 200, 2500, 4)
            f_jetHt[tg].SetLineColor(1)
            f_jetHt[tg].SetParNames("saturation_Y", "slope", "x_turnON", "initY")
            f_jetHt[tg].SetParLimits(0, 0, 1)
            f_jetHt[tg].SetParLimits(1, 2, 25)
            f_jetHt[tg].SetParLimits(2, -100, 500)
            f_jetHt[tg].SetParLimits(3, -0.1, 1)
            #f_jetHt[tg].SetLineStyle(style[i - 2])

            f_muonPt[tg] = ROOT.TF1('f_muonPt' + tg, turnOnFit, 0, 250, 4)
            f_muonPt[tg].SetLineColor(1)
            f_muonPt[tg].SetParNames("saturation_Y", "slope", "x_turnON", "initY")
            f_muonPt[tg].SetParLimits(0, 0.7, 0.9)
            f_muonPt[tg].SetParLimits(1, 0, 2000)
            f_muonPt[tg].SetParLimits(2, 10, 50)
            f_muonPt[tg].SetParLimits(3, -0.1, 1)
            #f_muonPt[tg].SetLineStyle(style[i - 2])

            i += 2


    ####################
    # - Draw on Canvas #
    ####################
    # - Canvas Details
    triggerCanvas.cd(1)
    ltx = TLatex()
    cutInfoPage(ltx, selCriteria, preSelCuts)
    pdfCreator(argms, 0, triggerCanvas, selCriteria)

    # - Create text for legend
    legString = cmsPlotString(argms.inputLFN)
    t2 = ROOT.TPaveText(0.08, 0.91, 0.92, 0.96, "nbNDC")
    t2.SetFillColorAlpha(0, 0.9)
    t2.SetTextSize(0.035)
    t2.AddText(legString)

    muonpT_rebin = numpy.array(
        (0., 10., 20., 22., 24., 26., 28., 30., 35., 40., 50., 75., 100., 125., 150., 200., 300.))
    #muonpT_rebin = numpy.array(
     #   (0., 10., 20., 30., 40., 50., 60., 70., 80., 100., 125., 150., 200., 300.))
    ht_rebin = numpy.array(
        (0., 100., 200., 220., 240., 260., 280., 300., 350., 400., 500., 750., 1000., 1250., 1500., 2000., 3000.))

    cv1 = triggerCanvas.cd(1)
    """ HT distribution for different triggers """
    #drawEventHists(h_jetHt, trigList, "H_{T} (GeV/c)", cv1, ht_rebin, True)
    #nDim = (ht_rebin.ndim) - 1
    #print(nDim)
    h_jetHtcp = {}
    h_jetHt["notrigger"] = h_jetHt["notrigger"].Rebin(16, "h_jetHT", ht_rebin)
    histEntries = h_jetHt["notrigger"].GetEntries()
    h_jetHt["notrigger"].SetTitle("No HLT selection (%d) ;H_{T} (GeV/c) ;Number of Events / GeVc^{-1}" % histEntries)
    h_jetHtcp["notrigger"] = h_jetHt["notrigger"].Clone()
    for i in range (0, 17):
        binWidth = h_jetHtcp["notrigger"].GetXaxis().GetBinWidth(i)
        binContent = h_jetHtcp["notrigger"].GetBinContent(i)
        newBinContent = round(binContent/binWidth)
        h_jetHtcp["notrigger"].SetBinContent(i, newBinContent)
    h_jetHtcp["notrigger"].Draw()
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            h_jetHt[tg] = h_jetHt[tg].Rebin(16, "h_jetHT_" + tg, ht_rebin)
            histEntries = h_jetHt[tg].GetEntries()
            h_jetHt[tg].SetTitle("%s (%d) ;H_{T} (GeV/c) ;Number of Events / GeVc^{-1}" % (tg,histEntries))
            h_jetHtcp[tg] = h_jetHt[tg].Clone()
            for i in range (0,17):
                binWidth = h_jetHtcp[tg].GetXaxis().GetBinWidth(i)
                binContent = h_jetHtcp[tg].GetBinContent(i)
                newBinContent = round(binContent/binWidth)
                h_jetHtcp[tg].SetBinContent(i, newBinContent)
            h_jetHtcp[tg].Draw('same')
    ROOT.gStyle.SetLegendTextSize(0.025)
    cv1.BuildLegend(0.42, 0.6, 0.95, 0.9)
    t2.Draw("same")
    pdfCreator(argms, 1, triggerCanvas, selCriteria)
    triggerCanvas.Print("TriggerPlots/images/event_jetPt.png", "png")

    cv2 = triggerCanvas.cd(1)
    """ Trigger efficiency vs total HT """
    i = 0
    j = 2
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            if ROOT.TEfficiency.CheckConsistency(h_jetHt[tg], h_jetHt["notrigger"]):
                h_TriggerRatio[tg] = ROOT.TEfficiency(h_jetHt[tg], h_jetHt["notrigger"])
                xTitle = h_jetHt["notrigger"].GetXaxis().GetTitle()
                xBinWidth = h_jetHt["notrigger"].GetXaxis().GetBinWidth(1)
                h_TriggerRatio[tg].SetTitle(";{0};Trigger Efficiency".format(xTitle))
                h_TriggerRatio[tg].SetName(tg)
                h_TriggerRatio[tg].SetTitle(tg)
                h_TriggerRatio[tg].SetLineColor(j)
                j += 2
                if i == 0:
                    # h_TriggerRatio[tg].GetListOfFunctions().AddFirst(f_jetHt[tg])
                    # f_jetHt[tg].SetParameters(0.8, 20, 135, 0)
                    # h_TriggerRatio[tg].Fit(f_jetHt[tg], 'LR')  # L= log likelihood, V=verbose, R=range in function
                    # fitInfo(fit=f_jetHt[tg], printEqn="t", fitName=("jetHt" + tg), args=argms)
                    h_TriggerRatio[tg].Draw('AP')
                    cv2.Update()
                    graph1 = h_TriggerRatio[tg].GetPaintedGraph()
                    graph1.SetMinimum(0)
                    graph1.SetMaximum(1.2)
                    cv2.Update()
                    tX1 = 0.15*(h_jetHt["notrigger"].GetXaxis().GetXmax())
                    tY1 = 1.1
                    # assymGraph = h_TriggerRatio[tg].CreateGraph()
                elif i > 0:
                    if i == 1: f_jetHt[tg].SetParameters(0.8, 5, 500, 0)
                    elif i == 2: f_jetHt[tg].SetParameters(0.8, 10, 330, 0)
                    elif i == 3: f_jetHt[tg].SetParameters(0.8, 5, 500, 0)
                    # h_TriggerRatio[tg].Fit(f_jetHt[tg], 'LR')
                    # fitInfo(fit=f_jetHt[tg], printEqn="n", fitName=("jetHt" + tg), args=argms)
                    h_TriggerRatio[tg].Draw('same')
                i += 1
    ROOT.gStyle.SetLegendTextSize(0.025)
    cv2.BuildLegend(0.3, 0.1, 0.9, 0.3)
    t2.Draw("same")
    pdfCreator(argms, 1, triggerCanvas, selCriteria)
    triggerCanvas.Print("TriggerPlots/images/teff_jetPt.png", "png")


    cv3 = triggerCanvas.cd(1)
    """ Trigger inclussive efficiency vs total HT """
    i = 0
    for key in trigList:
        if not key.find("El") == -1: continue
        numBins = h_jetHt["notrigger"].GetNbinsX()
        h_jetHt["notrigger"].RebinX(numBins, "")
        for tg in trigList[key]:
            numBins = h_jetHt[tg].GetNbinsX()
            h_jetHt[tg].RebinX(numBins, "")
            h_TriggerRatio[tg] = h_jetHt[tg].Clone("h_jetHtRatio" + tg)
            h_TriggerRatio[tg].Sumw2()
            h_TriggerRatio[tg].SetStats(0)
            h_TriggerRatio[tg].Divide(h_jetHt["notrigger"])
            # h_TriggerRatio[tg].Rebin(numBins)
            # print(h_TriggerRatio[tg].GetBinContent(1))
            inEff = h_TriggerRatio[tg].GetBinContent(1)  # / numBins
            # print(h_TriggerRatio[tg].GetBinError(1))
            inErEff = h_TriggerRatio[tg].GetBinError(1)  # / 300
            inclusiveEfficiency(" Jet HT Eff =,{0:.3f},+/- ,{1:.3f}, {2} \n".format(inEff, inErEff, tg), argms.inputLFN)
            xTitle = h_jetHt["notrigger"].GetXaxis().GetTitle()
            xBinWidth = h_jetHt["notrigger"].GetXaxis().GetBinWidth(1)
            h_TriggerRatio[tg].SetTitle(";{0};Trigger Efficiency".format(xTitle))
            h_TriggerRatio[tg].SetName(tg)
            # h_TriggerRatio[tg].SetBinContent(1, inEff)
            # h_TriggerRatio[tg].SetBinError(1, inErEff)
            if i == 0:
                # h_TriggerRatio[tg].SetMinimum(0.)
                # h_TriggerRatio[tg].SetMaximum(301.8)
                h_TriggerRatio[tg].Draw()
                tX1 = 0.15 * (h_jetHt["notrigger"].GetXaxis().GetXmax())
                tY1 = 0.1
            if i > 0:
                h_TriggerRatio[tg].Draw('same')
            i += 1
    ROOT.gStyle.SetLegendTextSize(0.025)
    cv3.BuildLegend(0.37, 0.6, 0.9, 0.9)
    t2.Draw("same")
    pdfCreator(argms, 1, triggerCanvas, selCriteria)

    # - Jet Multiplicity plots ---------------------------------
    cv4 = triggerCanvas.cd(1)
    h_jetMult["notrigger"].GetXaxis().SetTitle("Number of Jets")
    histEntries = h_jetMult["notrigger"].GetEntries()
    h_jetMult["notrigger"].SetTitle("No HLT selection (%d);Number of Jets ;Number of Events" % histEntries)
    h_jetMult["notrigger"].Draw()
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            histEntries= h_jetMult[tg].GetEntries()
            h_jetMult[tg].SetTitle("%s (%d);Number of Jets ;Number of Events" % (tg,histEntries))
            h_jetMult[tg].Draw('same')
    ROOT.gStyle.SetLegendTextSize(0.025)
    cv4.BuildLegend(0.42, 0.6, 0.95, 0.9)
    t2.Draw("same")
    pdfCreator(argms, 1, triggerCanvas, selCriteria)
    triggerCanvas.Print("TriggerPlots/images/event_mult.png", "png")


    cv5 = triggerCanvas.cd(1)
    i = 0
    j = 2
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            if ROOT.TEfficiency.CheckConsistency(h_jetMult[tg], h_jetMult["notrigger"]):
                h_TriggerRatio[tg] = ROOT.TEfficiency(h_jetMult[tg], h_jetMult["notrigger"])
                # xTitle = h_jetMult["notrigger"].GetXaxis().GetTitle()
                # xBinWidth = h_jetMult["notrigger"].GetXaxis().GetBinWidth(1)
                h_TriggerRatio[tg].SetTitle(";Number of Jets ;Trigger Efficiency")
                h_TriggerRatio[tg].SetName(tg)
                h_TriggerRatio[tg].SetTitle(tg)
                h_TriggerRatio[tg].SetLineColor(j)
                j += 2
                if i == 0:
                    h_TriggerRatio[tg].Draw('AP')
                    cv5.Update()
                    graph1 = h_TriggerRatio[tg].GetPaintedGraph()
                    graph1.SetMinimum(0)
                    graph1.SetMaximum(1.2)
                    cv5.Update()
                    tX1 = 0.05 * ((h_jetMult["notrigger"].GetXaxis().GetXmax())-5)+5
                    tY1 = 1.1
                if i > 0:
                    h_TriggerRatio[tg].Draw('same')
            i += 1
    ROOT.gStyle.SetLegendTextSize(0.025)
    cv5.BuildLegend(0.3, 0.1, 0.9, 0.3)
    t2.Draw("same")
    pdfCreator(argms, 1, triggerCanvas, selCriteria)
    triggerCanvas.Print("TriggerPlots/images/teff_mult.png", "png")


    # - B tagged Jet Multiplicity plots ---------------------------
    cv6 = triggerCanvas.cd(1)
    # h_jetBMult["notrigger"].SetTitle("")
    h_jetBMult["notrigger"].GetXaxis().SetRange(1, 10)
    histEntries = h_jetBMult["notrigger"].GetEntries()
    h_jetBMult["notrigger"].SetTitle(" No HLT selection (%d);Number of b-tagged Jets ;Number of Events" % histEntries)
    h_jetBMult["notrigger"].Draw()
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            histEntries = h_jetBMult[tg].GetEntries()
            h_jetBMult[tg].SetTitle("%s (%d);Number of b-tagged Jets ;Number of Events" % (tg, histEntries))
            h_jetBMult[tg].Draw('same')
    ROOT.gStyle.SetLegendTextSize(0.025)
    cv6.BuildLegend(0.42, 0.55, 0.95, 0.9)
    tX1 = 0.6 * (h_jetBMult["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95 * (h_jetBMult["notrigger"].GetMaximum())
    #ltx.SetTextSize(0.03)
    #ltx.DrawLatex(tX1, tY1, legString)
    t2.Draw("same")
    pdfCreator(argms, 1, triggerCanvas, selCriteria)
    triggerCanvas.Print("TriggerPlots/images/event_bmult.png", "png")


    cv7 = triggerCanvas.cd(1)
    i = 0
    j = 2
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            if ROOT.TEfficiency.CheckConsistency(h_jetBMult[tg], h_jetBMult["notrigger"]):
                h_TriggerRatio[tg] = ROOT.TEfficiency(h_jetBMult[tg], h_jetBMult["notrigger"])
                xTitle = h_jetBMult["notrigger"].GetXaxis().GetTitle()
                xBinWidth = h_jetBMult["notrigger"].GetXaxis().GetBinWidth(1)
                h_TriggerRatio[tg].SetTitle(";{0};Trigger Efficiency".format(xTitle))
                h_TriggerRatio[tg].SetName(tg)
                h_TriggerRatio[tg].SetTitle(tg)
                h_TriggerRatio[tg].SetLineColor(j)
                j += 2
                if i == 0:
                    h_TriggerRatio[tg].Draw('AP')
                    cv7.Update()
                    graph1 = h_TriggerRatio[tg].GetPaintedGraph()
                    graph1.SetMinimum(0)
                    graph1.SetMaximum(1.2)
                    cv7.Update()
                    tX1 = 0.05 * (h_jetBMult["notrigger"].GetXaxis().GetXmax())
                    tY1 = 1.1
                if i > 0:
                    h_TriggerRatio[tg].Draw('same')
            i += 1
    ROOT.gStyle.SetLegendTextSize(0.025)
    cv7.BuildLegend(0.3, 0.1, 0.9, 0.3)
    #ltx.SetTextSize(0.03)
    #ltx.DrawLatex(tX1, tY1, legString)
    t2.Draw("same")
    pdfCreator(argms, 1, triggerCanvas, selCriteria)
    triggerCanvas.Print("TriggerPlots/images/teff_bmult.png", "png")


    # - Muon test Plots-------------------------------
#    triggerCanvas.cd(1)
#    h_muonGenPartFlav.Draw()
#    pdfCreator(argms, 1, triggerCanvas, selCriteria)
    #
#    triggerCanvas.cd(1)
#    h_muonGenPartIdx.Draw()
#    pdfCreator(argms, 1, triggerCanvas, selCriteria)

#    triggerCanvas.cd(1)
#    h_muonPfRelIso04_all.Draw()
    #pdfCreator(argms, 1, triggerCanvas, selCriteria)

    # - Muon pT plots ---------------------------------
    cv8 = triggerCanvas.cd(1)
    # h_muonPt["notrigger"].SetTitle("")
    h_muonPtcp = {}
    h_muonPt["notrigger"] = h_muonPt["notrigger"].Rebin(16, "h_muonPt", muonpT_rebin)
    histEntries = h_muonPt["notrigger"].GetEntries()
    h_muonPt["notrigger"].SetTitle("No HLT selection (%d);Muon P_{T} (GeV/c) ;Number of Events / GeVc^{-1}" % histEntries)
    h_muonPt["notrigger"].SetMinimum(0.)
    h_muonPtcp["notrigger"] = h_muonPt["notrigger"].Clone()
    # h_muonPt["notrigger"].SetMaximum(3500)
    for i in range (0, 17):
        binWidth = h_muonPtcp["notrigger"].GetXaxis().GetBinWidth(i)
        binContent = h_muonPtcp["notrigger"].GetBinContent(i)
        newBinContent = round(binContent/binWidth)
        h_muonPtcp["notrigger"].SetBinContent(i, newBinContent)
    h_muonPtcp["notrigger"].Draw()
#    h_muonPt["nobaseline"] = h_muonPt["nobaseline"].Rebin(11, "h_muonPt_base", muonpT_rebin)
#    normPt = 10* (h_muonPt["notrigger"].GetEntries())/(h_muonPt["nobaseline"].GetEntries())
#    h_muonPt["nobaseline"].Scale(normPt)
#    h_muonPt["nobaseline"].Draw("same")
    tX1 = 0.60*(h_muonPt["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95*(h_muonPt["notrigger"].GetMaximum())
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            h_muonPt[tg] = h_muonPt[tg].Rebin(16, "h_muonPt_" + tg, muonpT_rebin)
            histEntries = h_muonPt[tg].GetEntries()
            h_muonPt[tg].SetTitle("%s (%d);Muon P_{T} (GeV/c);Number of Events / GeVc^{-1}" % (tg, histEntries))
            h_muonPtcp[tg] = h_muonPt[tg].Clone()
            for i in range (0, 17):
                binWidth = h_muonPtcp[tg].GetXaxis().GetBinWidth(i)
                binContent = h_muonPtcp[tg].GetBinContent(i)
                newBinContent = round(binContent/binWidth)
                h_muonPtcp[tg].SetBinContent(i, newBinContent)
            h_muonPtcp[tg].Draw('same')
    ROOT.gStyle.SetLegendTextSize(0.025)
    cv8.BuildLegend(0.42, 0.55, 0.95, 0.9)
    t2.Draw("same")
    #pdfCreator(argms, 1, triggerCanvas, selCriteria)
    triggerCanvas.Print("TriggerPlots/images/event_muonPt.png", "png")


#     cv72 = triggerCanvas.cd(1)
#     # h_muonPt["notrigger"].SetTitle("")
#     h_muonPt["nobaseline"].SetMinimum(0.)
# #    h_muonPt["nobaseline"].Scale(1/normPt)
#     # h_muonPt["notrigger"].SetMaximum(3500)
#     h_muonPt["nobaseline"] = h_muonPt["nobaseline"]#.Rebin(16, "h_muonPt_unmatched0", muonpT_rebin)
#     h_muonPt["prompt0"].SetTitle("prompt muons")
#     h_muonPt["prompt0"] = h_muonPt["prompt0"].Rebin(16, "h_muonPt_prompt0", muonpT_rebin)
#     h_muonPt["prompt0"].SetFillColorAlpha(4,0.3)
#     h_muonPt["from_b0"] = h_muonPt["from_b0"].Rebin(16, "h_muonPt_from_b0", muonpT_rebin)
#     h_muonPt["from_b0"].SetFillColorAlpha(2,0.3)
#     h_muonPt["from_c0"] = h_muonPt["from_c0"].Rebin(16, "h_muonPt_from_c0", muonpT_rebin)
#     h_muonPt["from_c0"].SetFillColorAlpha(3,0.3)
#     h_muonPt["from_light_or_unknown0"] = h_muonPt["from_light_or_unknown0"].Rebin(16, "h_muonPt_from_light_or_unknown0", muonpT_rebin)
#     h_muonPt["from_light_or_unknown0"].SetFillColorAlpha(6,0.3)
#     h_muonPt["unmatched0"] = h_muonPt["unmatched0"].Rebin(16, "h_muonPt_unmatched0", muonpT_rebin)
#     h_muonPt["unmatched0"].SetFillColorAlpha(8,0.3)
#     h_muonPt["from_prompt_tau0"] = h_muonPt["from_prompt_tau0"].Rebin(16, "h_muonPt_from_prompt_tau0", muonpT_rebin)
#     h_muonPt["from_prompt_tau0"].SetFillColorAlpha(9,0.3)
#
#     for i in range (0, 17):
#         binWidth = h_muonPt["nobaseline"].GetXaxis().GetBinWidth(i)
#         binContent = h_muonPt["nobaseline"].GetBinContent(i)
#         newBinContent = round(binContent/binWidth)
#         h_muonPt["nobaseline"].SetBinContent(i, newBinContent)
#         binContent = h_muonPt["prompt0"].GetBinContent(i)
#         newBinContent = round(binContent/binWidth)
#         h_muonPt["prompt0"].SetBinContent(i, newBinContent)
#         binContent = h_muonPt["from_b0"].GetBinContent(i)
#         newBinContent = round(binContent/binWidth)
#         h_muonPt["from_b0"].SetBinContent(i, newBinContent)
#         binContent = h_muonPt["from_c0"].GetBinContent(i)
#         newBinContent = round(binContent/binWidth)
#         h_muonPt["from_c0"].SetBinContent(i, newBinContent)
#         binContent = h_muonPt["from_light_or_unknown0"].GetBinContent(i)
#         newBinContent = round(binContent/binWidth)
#         h_muonPt["from_light_or_unknown0"].SetBinContent(i, newBinContent)
#         binContent = h_muonPt["unmatched0"].GetBinContent(i)
#         newBinContent = round(binContent/binWidth)
#         h_muonPt["unmatched0"].SetBinContent(i, newBinContent)
#         binContent = h_muonPt["from_prompt_tau0"].GetBinContent(i)
#         newBinContent = round(binContent/binWidth)
#         h_muonPt["from_prompt_tau0"].SetBinContent(i,  newBinContent)
#     h_muonPt["nobaseline"].Draw()
#     h_muonPt["prompt0"].Draw('same')
#     h_muonPt["from_b0"].Draw('same')
#     h_muonPt["from_c0"].Draw('same')
#     h_muonPt["from_light_or_unknown0"].Draw('same')
#     h_muonPt["unmatched0"].Draw('same')
#     h_muonPt["from_prompt_tau0"].Draw('same')
#     ROOT.gStyle.SetLegendTextSize(0.025)
#     cv72.BuildLegend(0.5, 0.2, 0.95, 0.9)
#     t2.Draw("same")
#     pdfCreator(argms, 1, triggerCanvas, selCriteria)
#     triggerCanvas.Print("TriggerPlots/images/event_muonGentest1.png", "png")

    cv11 = triggerCanvas.cd(1)
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            if tg.find("_PFHT380") == -1: continue
            print(tg)
            if ROOT.TEfficiency.CheckConsistency(h_muonPt[tg], h_muonPt["notrigger"]):
                h_muonPt[tg] = h_muonPt[tg].Rebin(16, "h_muonPt" +tg, muonpT_rebin)
                h_TriggerRatio[tg] = ROOT.TEfficiency(h_muonPt[tg], h_muonPt["notrigger"])
                xTitle = h_muonPt["notrigger"].GetXaxis().GetTitle()
                h_TriggerRatio[tg].SetTitle("All events;{0};Trigger Efficiency".format(xTitle))
#                h_TriggerRatio[tg].SetName(tg)
#                h_TriggerRatio[tg].SetTitle(tg)
                h_TriggerRatio[tg].SetLineColor(1)
                h_TriggerRatio[tg].Draw('AP')
                cv11.Update()
                graph1 = h_TriggerRatio[tg].GetPaintedGraph()
                graph1.SetMinimum(0.3)
                graph1.SetMaximum(1.2)
                cv11.Update()
                tX1 = 0.05 * (h_muonPt["notrigger"].GetXaxis().GetXmax())
                tY1 = 1.1
                muMother ="prompt"
                h_muonPt[muMother + tg] = h_muonPt[muMother + tg].Rebin(16, "h_muonPt_" + muMother, muonpT_rebin)
                h_muonPt[muMother] = h_muonPt[muMother].Rebin(16, "h_muonPttg_" + muMother, muonpT_rebin)
                h_TriggerRatio[tg + muMother] = ROOT.TEfficiency(h_muonPt[muMother + tg], h_muonPt[muMother])
                h_TriggerRatio[tg+ muMother].SetTitle(muMother)
                h_TriggerRatio[tg+ muMother].SetLineColor(2)
                h_TriggerRatio[tg+ muMother].Draw('same')
                muMother ="from_b"
                h_muonPt[muMother + tg] = h_muonPt[muMother + tg].Rebin(16, "h_muonPt_" + muMother, muonpT_rebin)
                h_muonPt[muMother] = h_muonPt[muMother].Rebin(16, "h_muonPttg_" + muMother, muonpT_rebin)
                h_TriggerRatio[tg + muMother] = ROOT.TEfficiency(h_muonPt[muMother + tg], h_muonPt[muMother])
                h_TriggerRatio[tg+ muMother].SetTitle(muMother)
                h_TriggerRatio[tg+ muMother].SetLineColor(6)
                h_TriggerRatio[tg+ muMother].Draw('same')
                muMother ="from_c"
                h_muonPt[muMother + tg] = h_muonPt[muMother + tg].Rebin(16, "h_muonPt_" + muMother, muonpT_rebin)
                h_muonPt[muMother] = h_muonPt[muMother].Rebin(16, "h_muonPttg_" + muMother, muonpT_rebin)
                h_TriggerRatio[tg + muMother] = ROOT.TEfficiency(h_muonPt[muMother + tg], h_muonPt[muMother])
                h_TriggerRatio[tg+ muMother].SetTitle(muMother)
                # h_TriggerRatio[tg+ muMother].Draw('same')
                muMother ="from_light_or_unknown"
                h_muonPt[muMother + tg] = h_muonPt[muMother + tg].Rebin(16, "h_muonPt_" + muMother, muonpT_rebin)
                h_muonPt[muMother] = h_muonPt[muMother].Rebin(16, "h_muonPttg_" + muMother, muonpT_rebin)
                h_TriggerRatio[tg + muMother] = ROOT.TEfficiency(h_muonPt[muMother + tg], h_muonPt[muMother])
                h_TriggerRatio[tg+ muMother].SetTitle(muMother)
                # h_TriggerRatio[tg+ muMother].Draw('same')
                muMother ="unmatched"
                h_muonPt[muMother + tg] = h_muonPt[muMother + tg].Rebin(16, "h_muonPt_" + muMother, muonpT_rebin)
                h_muonPt[muMother] = h_muonPt[muMother].Rebin(16, "h_muonPttg_" + muMother, muonpT_rebin)
                h_TriggerRatio[tg + muMother] = ROOT.TEfficiency(h_muonPt[muMother + tg], h_muonPt[muMother])
                h_TriggerRatio[tg+ muMother].SetTitle(muMother)
                # h_TriggerRatio[tg+ muMother].Draw('same')
                muMother ="from_prompt_tau"
                h_muonPt[muMother + tg] = h_muonPt[muMother + tg].Rebin(16, "h_muonPt_" + muMother, muonpT_rebin)
                h_muonPt[muMother] = h_muonPt[muMother].Rebin(16, "h_muonPttg_" + muMother, muonpT_rebin)
                h_TriggerRatio[tg + muMother] = ROOT.TEfficiency(h_muonPt[muMother + tg], h_muonPt[muMother])
                h_TriggerRatio[tg+ muMother].SetTitle(muMother)
                h_TriggerRatio[tg+ muMother].SetLineColor(4)
                h_TriggerRatio[tg+ muMother].Draw('same')
                # ROOT.gPad.SetLogy()
    ROOT.gStyle.SetLegendTextSize(0.04)
    cv11.BuildLegend(0.5, 0.1, 0.9, 0.5)
    t2.Draw("same")
    #pdfCreator(argms, 1, triggerCanvas, selCriteria)
    triggerCanvas.Print("TriggerPlots/images/teff_muonPtGen.png", "png")


    cv12 = triggerCanvas.cd(1)
    i = 0
    j = 2
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            if ROOT.TEfficiency.CheckConsistency(h_muonPt[tg], h_muonPt["notrigger"]):
                h_TriggerRatio[tg] = ROOT.TEfficiency(h_muonPt[tg], h_muonPt["notrigger"])
                xTitle = h_muonPt["notrigger"].GetXaxis().GetTitle()
                xBinWidth = h_muonPt["notrigger"].GetXaxis().GetBinWidth(1)
                h_TriggerRatio[tg].SetTitle(";{0};Trigger Efficiency".format(xTitle))
                h_TriggerRatio[tg].SetName(tg)
                h_TriggerRatio[tg].SetTitle(tg)
                h_TriggerRatio[tg].SetLineColor(j)
                j += 2
                if i == 0:
                    f_muonPt[tg].SetParameters(0.8, 0.95, 24, 0.05)
                    # f_muonPt[tg].SetParLimits(0, 0.7, 0.9)
                    # f_muonPt[tg].SetParLimits(1, 0, 5)
                    # f_muonPt[tg].SetParLimits(2, 20, 40)
                    # f_muonPt[tg].SetParLimits(3, 0.01, 0.05)
                    #h_TriggerRatio[tg].Fit(f_muonPt[tg], 'LR')  # L= log likelihood, V=verbose, R=range in function
                    #fitInfo(fit=f_muonPt[tg], printEqn="n", fitName=("muonPt" + tg), args=argms)
                    h_TriggerRatio[tg].Draw('AP')
                    cv12.Update()
                    graph1 = h_TriggerRatio[tg].GetPaintedGraph()
                    graph1.SetMinimum(0)
                    graph1.SetMaximum(1.2)
                    cv12.Update()
                    tX1 = 0.05 * (h_muonPt["notrigger"].GetXaxis().GetXmax())
                    tY1 = 1.1
                if i > 0:
                    if i == 1:
                        f_muonPt[tg].SetParameters(0.05, 1000, 24, 0.8)
                        # f_muonPt[tg].SetParLimits(0, 0, 0.1)
                        # f_muonPt[tg].SetParLimits(1, 100, 2000)
                        # f_muonPt[tg].SetParLimits(2, 20, 40)
                        # f_muonPt[tg].SetParLimits(3, 0.8, 0.9)
                    elif i == 2:
                        f_muonPt[tg].SetParameters(0.18, 0.95, 24, 0.8)
                        # f_muonPt[tg].SetParLimits(0, 0.1, 1)
                        # f_muonPt[tg].SetParLimits(1, 0, 10)
                        # f_muonPt[tg].SetParLimits(2, 20, 40)
                        # f_muonPt[tg].SetParLimits(3, 0, 0.9)
                    elif i == 3:
                        f_muonPt[tg].SetParameters(0.75, 0.95, 15, 0.15)
                        # f_muonPt[tg].SetParLimits(0, 0.5, 1)
                        # f_muonPt[tg].SetParLimits(1, 0, 10)
                        # f_muonPt[tg].SetParLimits(2, 0, 30)
                        # f_muonPt[tg].SetParLimits(3, 0, 0.3)
                    #h_TriggerRatio[tg].Fit(f_muonPt[tg], 'LR')
                    #fitInfo(fit=f_muonPt[tg], printEqn="n", fitName=("muonPt" + tg), args=argms)
                    h_TriggerRatio[tg].Draw('same')
            i += 1
    ROOT.gStyle.SetLegendTextSize(0.025)
    cv12.BuildLegend(0.3, 0.1, 0.9, 0.3)
    #ltx.SetTextSize(0.03)
    #ltx.DrawLatex(tX1, tY1, legString)
    t2.Draw("same")
    pdfCreator(argms, 1, triggerCanvas, selCriteria)
    triggerCanvas.Print("TriggerPlots/images/teff_muonPt.png", "png")


    cv13 = triggerCanvas.cd(1)
    i = 0
    for key in trigList:
        if not key.find("El") == -1: continue
#        numBins = h_muonPt["notrigger"].GetNbinsX()
#        h_muonPt["notrigger"].RebinX(numBins, "")
        for tg in trigList[key]:
            # numBins = h_muonPt[tg].GetNbinsX()
            # h_muonPt[tg].RebinX(numBins, "")
            h_TriggerRatio[tg] = h_muonPt[tg].Clone("h_muonPtRatio" + tg)
            h_TriggerRatio[tg].Sumw2()
            h_TriggerRatio[tg].SetStats(0)
            h_TriggerRatio[tg].Divide(h_muonPt["notrigger"])
            # h_TriggerRatio[tg].Rebin(300)
            # print(h_TriggerRatio[tg].GetBinContent(1))
            inEff = h_TriggerRatio[tg].GetBinContent(1)
            # print(h_TriggerRatio[tg].GetBinError(1))
            inErEff = h_TriggerRatio[tg].GetBinError(1)
            inclusiveEfficiency("Muon Pt Eff = ,{0:.3f},+/-,{1:.3f}, {2} \n".format(inEff, inErEff, tg), argms.inputLFN)
            xTitle = h_muonPt["notrigger"].GetXaxis().GetTitle()
            xBinWidth = h_muonPt["notrigger"].GetXaxis().GetBinWidth(1)
            h_TriggerRatio[tg].SetTitle(";{0};Trigger Efficiency per {1:.2f} GeV/c".format(xTitle, xBinWidth))
            h_TriggerRatio[tg].SetName(tg)
            if i == 0:
                # h_TriggerRatio[tg].SetMinimum(0.)
                # h_TriggerRatio[tg].SetMaximum(301.8)
                h_TriggerRatio[tg].Draw()
                tX1 = 0.05 * (h_muonPt["notrigger"].GetXaxis().GetXmax())
                tY1 = 0.1
            if i > 0:
                h_TriggerRatio[tg].Draw('same')
            i += 2
    cv13.BuildLegend(0.4, 0.1, 0.9, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    #ltx.SetTextSize(0.03)
    #ltx.DrawLatex(tX1, tY1, legString)
    t2.Draw("same")
    pdfCreator(argms, 1, triggerCanvas, selCriteria)

    # - MET pT plots ---------------------------------
    # cv9 = triggerCanvas.cd(1)
    # h_metPt["notrigger"].GetXaxis().SetTitle("E^{Miss}_{T}")
    # h_metPt["notrigger"].SetMinimum(0.)
    # # h_metPt["notrigger"].SetMaximum(1800)
    # h_metPt["notrigger"].Draw('E1')
    # tX1 = 0.6 * (h_metPt["notrigger"].GetXaxis().GetXmax())
    # tY1 = 0.95 * (h_metPt["notrigger"].GetMaximum())
    # for key in trigList:
    #     if not key.find("El") == -1: continue
    #     for tg in trigList[key]:
    #         h_metPt[tg].Draw('E1 same')
    # cv9.BuildLegend(0.47, 0.54, 0.97, 0.74)
    # ltx.SetTextSize(0.03)
    # ltx.DrawLatex(tX1, tY1, legString)
    # ROOT.gStyle.SetLegendTextSize(0.02)
    # pdfCreator(argms, 1, triggerCanvas, selCriteria)
    #
    # cv10 = triggerCanvas.cd(1)
    # i = 0
    # j = 2
    # for key in trigList:
    #     if not key.find("El") == -1: continue
    #     for tg in trigList[key]:
    #         if ROOT.TEfficiency.CheckConsistency(h_metPt[tg], h_metPt["notrigger"]):
    #             h_TriggerRatio[tg] = ROOT.TEfficiency(h_metPt[tg], h_metPt["notrigger"])
    #             # xTitle = h_metPt["notrigger"].GetXaxis().GetTitle()
    #             xBinWidth = h_metPt["notrigger"].GetXaxis().GetBinWidth(1)
    #             h_TriggerRatio[tg].SetTitle(";E^{Miss}_{T};Trigger Efficiency per %.2f GeV/c" % xBinWidth)
    #             h_TriggerRatio[tg].SetName(tg)
    #             h_TriggerRatio[tg].SetTitle(tg)
    #             h_TriggerRatio[tg].SetLineColor(j)
    #             j += 1
    #             if i == 0:
    #                 h_TriggerRatio[tg].Draw('AP')
    #                 cv10.Update()
    #                 graph1 = h_TriggerRatio[tg].GetPaintedGraph()
    #                 graph1.SetMinimum(0)
    #                 graph1.SetMaximum(1.2)
    #                 cv10.Update()
    #                 tX1 = 0.05 * (h_metPt["notrigger"].GetXaxis().GetXmax())
    #                 tY1 = 1.1
    #             if i > 0:
    #                 h_TriggerRatio[tg].Draw('same')
    #         i += 1
    # cv10.BuildLegend(0.4, 0.1, 0.9, 0.3)
    # ROOT.gStyle.SetLegendTextSize(0.02)
    # ltx.SetTextSize(0.03)
    # ltx.DrawLatex(tX1, tY1, legString)
    # pdfCreator(argms, 1, triggerCanvas, selCriteria)

    # - GenMET pT plots ---------------------------------
    # cv11 = triggerCanvas.cd(1)
    # h_genMetPt["notrigger"].GetXaxis().SetTitle("Gen E^{Miss}_{T}")
    # h_genMetPt["notrigger"].SetMinimum(0.)
    # # h_genMetPt["notrigger"].SetMaximum(2000)
    # h_genMetPt["notrigger"].Draw('E1')
    # tX1 = 0.6 * (h_genMetPt["notrigger"].GetXaxis().GetXmax())
    # tY1 = 0.95 * (h_genMetPt["notrigger"].GetMaximum())
    # for key in trigList:
    #     if not key.find("El") == -1: continue
    #     for tg in trigList[key]:
    #         h_genMetPt[tg].Draw('E1 same')
    # cv11.BuildLegend(0.47, 0.54, 0.97, 0.74)
    # ltx.SetTextSize(0.03)
    # ltx.DrawLatex(tX1, tY1, legString)
    # ROOT.gStyle.SetLegendTextSize(0.02)
    # pdfCreator(argms, 1, triggerCanvas, selCriteria)

    # cv12 = triggerCanvas.cd(1)
    # i = 0
    # j = 2
    # for key in trigList:
    #     if not key.find("El") == -1: continue
    #     for tg in trigList[key]:
    #         if ROOT.TEfficiency.CheckConsistency(h_genMetPt[tg], h_genMetPt["notrigger"]):
    #             h_TriggerRatio[tg] = ROOT.TEfficiency(h_genMetPt[tg], h_genMetPt["notrigger"])
    #             # xTitle = h_genMetPt["notrigger"].GetXaxis().GetTitle()
    #             xBinWidth = h_genMetPt["notrigger"].GetXaxis().GetBinWidth(1)
    #             h_TriggerRatio[tg].SetTitle("; Gen E^{Miss}_{T};Trigger Efficiency per %.2f GeV/c" % xBinWidth)
    #             h_TriggerRatio[tg].SetName(tg)
    #             h_TriggerRatio[tg].SetTitle(tg)
    #             h_TriggerRatio[tg].SetLineColor(j)
    #             j += 1
    #             if i == 0:
    #                 h_TriggerRatio[tg].Draw('AP')
    #                 cv12.Update()
    #                 graph1 = h_TriggerRatio[tg].GetPaintedGraph()
    #                 graph1.SetMinimum(0)
    #                 graph1.SetMaximum(1.2)
    #                 cv12.Update()
    #                 tX1 = 0.05 * (h_genMetPt["notrigger"].GetXaxis().GetXmax())
    #                 tY1 = 1.1
    #             if i > 0:
    #                 h_TriggerRatio[tg].Draw('same')
    #         i += 1
    # cv12.BuildLegend(0.4, 0.1, 0.9, 0.3)
    # ROOT.gStyle.SetLegendTextSize(0.02)
    # ltx.SetTextSize(0.03)
    # ltx.DrawLatex(tX1, tY1, legString)
    # pdfCreator(argms, 1, triggerCanvas, selCriteria)

    # - Eta plots ------------------------------------------
    # cv13 = triggerCanvas.cd(1)
    # # h_jetEta["notrigger"].GetYaxis().SetTitleOffset(1.1)
    # h_jetEta["notrigger"].Draw('E1')
    # tX1 = (0.6*14)-6
    # tY1 = 0.95*(h_jetEta["notrigger"].GetMaximum())
    # for key in trigList:
    #     if not key.find("El") == -1: continue
    #     for tg in trigList[key]:
    #         h_jetEta[tg].Draw('E1 same')
    # cv13.BuildLegend(0.47, 0.54, 0.97, 0.74)
    # ltx.SetTextSize(0.03)
    # ltx.DrawLatex(tX1, tY1, legString)
    # ROOT.gStyle.SetLegendTextSize(0.02)
    # pdfCreator(argms, 1, triggerCanvas, selCriteria)

    # cv14 = triggerCanvas.cd(1)
    # h_muonEta["notrigger"].Draw('E1')
    # tX1 = (0.6*14)-6
    # tY1 = 0.95*(h_muonEta["notrigger"].GetMaximum())
    # for key in trigList:
    #     if not key.find("El") == -1: continue
    #     for tg in trigList[key]:
    #         h_muonEta[tg].Draw('E1 same')
    # cv14.BuildLegend(0.47, 0.54, 0.97, 0.74)
    # ltx.SetTextSize(0.03)
    # ltx.DrawLatex(tX1, tY1, legString)
    # ROOT.gStyle.SetLegendTextSize(0.02)
    # pdfCreator(argms, 1, triggerCanvas, selCriteria)
    #
    # cv15 = triggerCanvas.cd(1)
    # i = 0
    # j = 2
    # for key in trigList:
    #     if not key.find("El") == -1: continue
    #     for tg in trigList[key]:
    #         if ROOT.TEfficiency.CheckConsistency(h_muonEta[tg], h_muonEta["notrigger"]):
    #             h_TriggerRatio[tg] = ROOT.TEfficiency(h_muonEta[tg], h_muonEta["notrigger"])
    #             xTitle = h_muonEta["notrigger"].GetXaxis().GetTitle()
    #             xBinWidth = h_muonEta["notrigger"].GetXaxis().GetBinWidth(1)
    #             h_TriggerRatio[tg].SetTitle(";{0};Trigger Efficiency per {1:.3f} GeV/c".format(xTitle, xBinWidth))
    #             h_TriggerRatio[tg].SetName(tg)
    #             h_TriggerRatio[tg].SetTitle(tg)
    #             h_TriggerRatio[tg].SetLineColor(j)
    #             j += 1
    #             if i == 0:
    #                 h_TriggerRatio[tg].Draw('AP')
    #                 cv15.Update()
    #                 graph1 = h_TriggerRatio[tg].GetPaintedGraph()
    #                 graph1.SetMinimum(0)
    #                 graph1.SetMaximum(1.2)
    #                 cv15.Update()
    #                 tX1 = 0.05 * (h_muonEta["notrigger"].GetXaxis().GetXmax())
    #                 tY1 = 1.1
    #             if i > 0:
    #                 h_TriggerRatio[tg].Draw('same')
    #         i += 1
    # cv15.BuildLegend(0.4, 0.1, 0.9, 0.3)
    # ROOT.gStyle.SetLegendTextSize(0.02)
    # ltx.SetTextSize(0.03)
    # ltx.DrawLatex(tX1, tY1, legString)
    # pdfCreator(argms, 1, triggerCanvas, selCriteria)

    # - Phi plots ------------------------------------------
    # cv16 = triggerCanvas.cd(1)
    # # h_jetPhi["notrigger"].GetYaxis().SetTitleOffset(1.3)
    # h_jetPhi["notrigger"].Draw('E1')
    # tX1 = 0.6*6
    # tY1 = 0.95*(h_jetPhi["notrigger"].GetMaximum())
    # for key in trigList:
    #     if not key.find("El") == -1: continue
    #     for tg in trigList[key]:
    #         h_jetPhi[tg].Draw('E1 same')
    # cv16.BuildLegend(0.4, 0.2, 0.4, 0.2)
    # ltx.SetTextSize(0.03)
    # ltx.DrawLatex(tX1, tY1, legString)
    # ROOT.gStyle.SetLegendTextSize(0.02)
    # pdfCreator(argms, 1, triggerCanvas, selCriteria)

    # cv17 = triggerCanvas.cd(1)
    # # h_muonPhi["notrigger"].GetYaxis().SetTitleOffset(1.4)
    # h_muonPhi["notrigger"].Draw('E1')
    # tX1 = 0.6*6
    # tY1 = 0.97*(h_muonPhi["notrigger"].GetMaximum())
    # for key in trigList:
    #     if not key.find("El") == -1: continue
    #     for tg in trigList[key]:
    #         h_muonPhi[tg].Draw('E1 same')
    # cv17.BuildLegend(0.4, 0.2, 0.4, 0.2)
    # ltx.SetTextSize(0.03)
    # ltx.DrawLatex(tX1, tY1, legString)
    # ROOT.gStyle.SetLegendTextSize(0.02)
    # pdfCreator(argms, 1, triggerCanvas, selCriteria)

    # - Eta-Phi Map plots ------------------------------------------
    # triggerCanvas.cd(1)
    # h_jetMap["notrigger"].Draw('COLZ')  # CONT4Z
    # # pdfCreator(argms, 1, triggerCanvas, selCriteria)
    # for key in trigList:
    #     if not key.find("El") == -1: continue
    #     for tg in trigList[key]:
    #         h_jetMap[tg].Draw('COLZ')
    #         # pdfCreator(argms, 1, triggerCanvas, selCriteria)
    #
    # h_muonMap["notrigger"].Draw('COLZ')
    # # pdfCreator(argms, 1, triggerCanvas, selCriteria)
    # for key in trigList:
    #     if not key.find("El") == -1: continue
    #     for tg in trigList[key]:
    #         h_muonMap[tg].Draw('COLZ')  # E
    #         # pdfCreator(argms, 1, triggerCanvas, selCriteria)

    # - plots for mu Triggers ---------------------------------
    #cv0 = triggerCanvas.cd(1)
 #   """ Isolation distribution for different triggers """
    # h_muonIsolation["notrigger"].RebinX(3, "")
    #h_muonIsolation["notrigger"].Draw('E1')
    #for key in trigList:
    #    if not key.find("El") == -1: continue
    #    for tg in trigList[key]:
    #        # h_muonIsolation[tg].RebinX(2, "")
    #        h_muonIsolation[tg].Draw('E1 same')
    #cv0.BuildLegend(0.47, 0.54, 0.97, 0.74)
    #ROOT.gStyle.SetLegendTextSize(0.02)
    #tX1 = 0.6 * (h_muonIsolation["notrigger"].GetXaxis().GetXmax())
    #tY1 = 1 * (h_muonIsolation["notrigger"].GetMaximum())
    #ltx.SetTextSize(0.03)
    #ltx.DrawLatex(tX1, tY1, legString)
    #pdfCreator(argms, 1, triggerCanvas, selCriteria)

    # cvEff = triggerCanvas.cd(1)
    # """ Trigger efficiency vs muon Isolation"""
    # i = 0
    # j = 2
    # for key in trigList:
    #     if not key.find("El") == -1: continue
    #     for tg in trigList[key]:
    #         if ROOT.TEfficiency.CheckConsistency(h_muonIsolation[tg], h_muonIsolation["notrigger"]):
    #             h_TriggerRatio[tg] = ROOT.TEfficiency(h_muonIsolation[tg], h_muonIsolation["notrigger"])
    #             xTitle = h_muonIsolation["notrigger"].GetXaxis().GetTitle()
    #             xBinWidth = h_muonIsolation["notrigger"].GetXaxis().GetBinWidth(1)
    #             h_TriggerRatio[tg].SetTitle(";{0};Trigger Efficiency per {1}a.u.".format(xTitle, round(xBinWidth)))
    #             h_TriggerRatio[tg].SetName(tg)
    #             h_TriggerRatio[tg].SetTitle(tg)
    #             h_TriggerRatio[tg].SetLineColor(j)
    #             j += 2
    #             if i == 0:
                    #h_TriggerRatio[tg].Draw()
                    #cvEff.Update()
                    #graph1 = h_TriggerRatio[tg].GetPaintedGraph()
                    #graph1.SetMinimum(0)
                    #graph1.SetMaximum(1.2)
                    #cvEff.Update()
                    # tX1 = 0.05 * (h_muonIsolation["notrigger"].GetXaxis().GetXmax())
                    # tY1 = 1.1
                    # i += 1
                #elif i > 0:
                    #h_TriggerRatio[tg].Draw('same')
                    #i += 1
    #cvEff.BuildLegend(0.4, 0.1, 0.9, 0.3)
    #ROOT.gStyle.SetLegendTextSize(0.02)
    #ltx.SetTextSize(0.03)
    #ltx.DrawLatex(0.08, 1.1, legString)
    #pdfCreator(argms, 1, triggerCanvas, selCriteria)

    # triggerCanvas.cd(1)
    # h_muonIsoPt["notrigger"].Draw('COLZ')  # CONT4Z
    # pdfCreator(argms, 1, triggerCanvas, selCriteria)
    # for key in trigList:
    #    if not key.find("El") == -1: continue
    #    for tg in trigList[key]:
    #        h_muonIsoPt[tg].Draw('COLZ')
    #        pdfCreator(argms, 1, triggerCanvas, selCriteria)

    # cvIso = {}
    # h_TEffOut = {}
    # for i in range(5, 80, 5):
    #     cvIso[i] = triggerCanvas.cd(1)
    #     colr = 2
    #     t = ROOT.TPaveText(0.2, 0.95, 0.5, 1.0, "nbNDC")
    #     t.AddText("Muon Pt = %d" % i)
    #     h_isoProjection = {"notrigger": h_muonIsoPt["notrigger"].ProjectionY("noTrigger", i, i, "o")}
    #     h_isoProjection["notrigger"].GetXaxis().SetTitleOffset(1.3)
    #     xTitle = h_isoProjection["notrigger"].GetXaxis().GetTitle()
    #     xBinWidth = h_isoProjection["notrigger"].GetXaxis().GetBinWidth(1)
    #     #h_isoProjection["notrigger"].Draw()
    #     for key in trigList:
    #         if not key.find("El") == -1: continue
    #         for tg in trigList[key]:
    #             h_isoProjection[tg] = h_muonIsoPt[tg].ProjectionY(tg, i, i, "o")
    #             h_isoProjection[tg].SetLineColor(colr)
    #             #h_isoProjection[tg].Draw("same")
    #             if not ROOT.TEfficiency.CheckConsistency(h_isoProjection[tg], h_isoProjection["notrigger"]): continue
    #             h_TEffOut[tg] = ROOT.TEfficiency(h_isoProjection[tg], h_isoProjection["notrigger"])
    #             h_TEffOut[tg].SetTitle(";{0};Trigger Efficiency per {1} a.u.".format(xTitle, round(xBinWidth)))
    #             h_TEffOut[tg].SetName(tg)
    #             h_TEffOut[tg].SetTitle(tg)
    #             h_TEffOut[tg].SetLineColor(colr)
    #             #h_TEffOut[tg].SetName(effName2)
    #             if colr == 2:
    #                 h_TEffOut[tg].Draw()
    #                 cvIso[i].Update()
    #                 graph1 = h_TEffOut[tg].GetPaintedGraph()
    #                 graph1.SetMinimum(0)
    #                 graph1.SetMaximum(1.2)
    #                 cvIso[i].Update()
    #             else: h_TEffOut[tg].Draw("same")
    #             colr += 2
    #     t.Draw("same")
    #     cvIso[i].BuildLegend(0.47, 0.74, 0.97, 0.94)
        # pdfCreator(argms, 1, triggerCanvas, selCriteria)

    #############################################################################
    # - Test Event numbers along steps ----------
    triggerCanvas.cd(1)
    #h_eventsPrg.SetFillColor(ROOT.kAzure-9)
    #h_eventsPrg.GetXaxis().SetLabelOffset(999)
    #h_eventsPrg.GetXaxis().SetLabelSize(0)
    #h_eventsPrg.Draw()
    #tY1 = 0.05*(h_eventsPrg.GetMaximum())
    #ltx.SetTextAngle(88)
    #ltx.DrawLatex(0.5, tY1, "Pre-selection")
    #ltx.DrawLatex(1.5, tY1, "Post-selection")
    #i = 0
    #for key in trigList:
    #    if not key.find("El") == -1: continue
    #    for tg in trigList[key]:
    #        ltx.DrawLatex((5.5 - i), tY1, tg)
    #        i += 1

    # h.GetXAxis().SetBinLabel(binnumber,string)
    t3 = ROOT.TPaveText(0., 0., 1., 1., "nbNDC")
    t3.SetFillColor(0)
    t3.SetTextSize(0.03)
    t3.AddText("That's all folks!")
    t3.Draw()
    pdfCreator(argms, 2, triggerCanvas, selCriteria)

    genCanvas = ROOT.TCanvas('genCanvas', 'muonMothers', 900, 500)  # 1100 600
    genCanvas.SetGrid()

    intLumiDEF = 27.052
    intLumiC = 9.664
    intLumiB = 4.823


    cv71 = genCanvas.cd(1)
    hstack = ROOT.THStack("hsgg","ggg")
    # h_muonPt["notrigger"].SetTitle("")
    h_muonPtcp2 = {}
    h_muonPtcp2["notrigger"] = h_muonPt["notrigger"]#.Rebin(13, "h_muonPt_notrigger_v2", muonpT_rebin)
    h_muonPtcp2["notrigger"].SetMinimum(0.)
    h_muonPtd["notrigger"] = h_muonPtd["notrigger"].Rebin(16, "h_muonPt_prompt", muonpT_rebin)
    h_muonPtd["notrigger"].SetTitle("Data")
    h_muonPtd["notrigger"].SetLineStyle(10)
    normVal = (4.823*831000 * 0.45)/43732445  # wjets = * 524200 ) /11103685  ttsemi=831000 * 0.45)/43732445  # (h_mcTTToSemiLeps[hName2].GetEntries())
    print(1/normVal)

    # h_muonPtd["notrigger"].Scale(1/normVal)
    # h_muonPt["notrigger"].SetMaximum(3500)
    h_muonPt["prompt"].SetTitle("prompt muons")
    h_muonPt["prompt"] = h_muonPt["prompt"].Rebin(16, "h_muonPt_prompt", muonpT_rebin)
    h_muonPtcp2["prompt"] = h_muonPt["prompt"]
    h_muonPtcp2["prompt"].SetFillColorAlpha(4,0.4)
    h_muonPt["from_b"] = h_muonPt["from_b"].Rebin(16, "h_muonPt_from_b", muonpT_rebin)
    h_muonPtcp2["from_b"] = h_muonPt["from_b"]
    h_muonPtcp2["from_b"].SetFillColorAlpha(2,0.4)
    h_muonPt["from_c"] = h_muonPt["from_c"].Rebin(16, "h_muonPt_from_c", muonpT_rebin)
    h_muonPtcp2["from_c"] = h_muonPt["from_c"]
    h_muonPtcp2["from_c"].SetFillColorAlpha(3,0.4)
    h_muonPt["from_light_or_unknown"] = h_muonPt["from_light_or_unknown"].Rebin(16, "h_muonPt_from_light_or_unknown", muonpT_rebin)
    h_muonPtcp2["from_light_or_unknown"] = h_muonPt["from_light_or_unknown"]
    h_muonPtcp2["from_light_or_unknown"].SetFillColorAlpha(6,0.4)
    h_muonPt["unmatched"] = h_muonPt["unmatched"].Rebin(16, "h_muonPt_unmatched", muonpT_rebin)
    h_muonPtcp2["unmatched"] = h_muonPt["unmatched"]
    h_muonPtcp2["unmatched"].SetFillColorAlpha(9,0.4)
    h_muonPt["from_prompt_tau"] = h_muonPt["from_prompt_tau"].Rebin(16, "h_muonPt_from_prompt_tau", muonpT_rebin)
    h_muonPtcp2["from_prompt_tau"] = h_muonPt["from_prompt_tau"]
    h_muonPtcp2["from_prompt_tau"].SetFillColorAlpha(8,0.5)

#    h_muonPt["prompt"].Scale(normVal)
#    h_muonPt["from_b"].Scale(normVal)
#    h_muonPt["from_c"].Scale(normVal)
#    h_muonPt["from_light_or_unknown"].Scale(#normVal)
#    h_muonPt["unmatched"].Scale(normVal)
#    h_muonPt["from_prompt_tau"].Scale(normVal)

    h_muonPt["prompt"].Draw('hist')
    h_muonPt["from_b"].Draw('hist')
    h_muonPt["from_c"].Draw('hist')
    h_muonPt["from_light_or_unknown"].Draw('hist')
    h_muonPt["unmatched"].Draw('hist')
    h_muonPt["from_prompt_tau"].Draw('hist')


    histListnew = [h_muonPtcp2["notrigger"], h_muonPtd["notrigger"],h_muonPtcp2["prompt"],h_muonPtcp2["from_b"],h_muonPtcp2["from_c"],h_muonPtcp2["from_light_or_unknown"],h_muonPtcp2["from_prompt_tau"]]
    maxYhistlist = getMaxY(histListnew)
    hstack.SetMaximum(maxYhistlist)
    print maxYhistlist
    hstack.SetTitle(";Muon pt GeV/c; Number of events per GeVc^{-1}")
    
    
    for i in range (0, 17):
        binWidth = h_muonPtcp2["notrigger"].GetXaxis().GetBinWidth(i)
        binContent = h_muonPtcp2["notrigger"].GetBinContent(i)
        newBinContent = round(binContent/binWidth)
        h_muonPtcp2["notrigger"].SetBinContent(i, newBinContent)
        binContent = h_muonPtd["notrigger"].GetBinContent(i)
        newBinContent = round(binContent/binWidth)
        h_muonPtd["notrigger"].SetBinContent(i, newBinContent)
        binContent = h_muonPtcp2["prompt"].GetBinContent(i)
        newBinContent = round(binContent/binWidth)
        h_muonPtcp2["prompt"].SetBinContent(i, newBinContent)
        binContent = h_muonPtcp2["from_b"].GetBinContent(i)
        newBinContent = round(binContent/binWidth)
        h_muonPtcp2["from_b"].SetBinContent(i, newBinContent)
        binContent = h_muonPtcp2["from_c"].GetBinContent(i)
        newBinContent = round(binContent/binWidth)
        h_muonPtcp2["from_c"].SetBinContent(i, newBinContent)
        binContent = h_muonPtcp2["from_light_or_unknown"].GetBinContent(i)
        newBinContent = round(binContent/binWidth)
        h_muonPtcp2["from_light_or_unknown"].SetBinContent(i, newBinContent)
        binContent = h_muonPtcp2["unmatched"].GetBinContent(i)
        newBinContent = round(binContent/binWidth)
        h_muonPtcp2["unmatched"].SetBinContent(i, newBinContent)
        binContent = h_muonPtcp2["from_prompt_tau"].GetBinContent(i)
        newBinContent = round(binContent/binWidth)
        h_muonPtcp2["from_prompt_tau"].SetBinContent(i,  newBinContent)
    #    h_muonPtcp2["notrigger"].Draw()
    h_muonPtd["notrigger"].SetMarkerStyle(8)
    h_muonPtd["notrigger"].SetMarkerSize(1)
    #    h_muonPtd["notrigger"].Draw('same')
    #    h_muonPtcp2["prompt"].Draw('same')
    #    h_muonPtcp2["from_b"].Draw('same')
    #    h_muonPtcp2["from_c"].Draw('same')
    #    h_muonPtcp2["from_light_or_unknown"].Draw('same')
    #    h_muonPtcp2["unmatched"].Draw('same')
    #    h_muonPtcp2["from_prompt_tau"].Draw('same')
    hstack.Add(h_muonPtcp2["from_c"])
    hstack.Add(h_muonPtcp2["from_light_or_unknown"])
    hstack.Add(h_muonPtcp2["unmatched"])
    hstack.Add(h_muonPtcp2["from_b"])
    hstack.Add(h_muonPtcp2["from_prompt_tau"])
    hstack.Add(h_muonPtcp2["prompt"])
    hstack.Draw()
    h_muonPtd["notrigger"].Draw('E1 same')
    h_muonPtcp2["notrigger"].Draw('same')

    ROOT.gStyle.SetLegendTextSize(0.035)
    cv71.BuildLegend(0.47, 0.3, 0.97, 0.9)
    t2.Draw("same")
    pdfCreator(argms, 1, genCanvas, selCriteria)
    genCanvas.Print("TriggerPlots/images/event_muonGentest2.png", "png")



#    histFile.Close()

main(process_arguments())
