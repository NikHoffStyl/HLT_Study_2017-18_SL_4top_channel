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
    parser.add_argument("-f", "--inputLFN", choices=["ttjets", "tttt", "tttt_weights", "wjets"],
                        default="tttt", help="Set list of input files")
    args = parser.parse_args()
    return args


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
    filename = time_.strftime("TriggerPlots/W%V_%y/" + parg.inputLFN + "_" + minPt + "jetPt.pdf")
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    if arg == 0:
        canvas.Print(time_.strftime("TriggerPlots/W%V_%y/" + parg.inputLFN + "_" + minPt +
                                    "jetPt.pdf("), "pdf")
    if arg == 1:
        canvas.Print(time_.strftime("TriggerPlots/W%V_%y/" + parg.inputLFN + "_" + minPt +
                                    "jetPt.pdf"), "pdf")
    if arg == 2:
        canvas.Print(time_.strftime("TriggerPlots/W%V_%y/" + parg.inputLFN + "_" + minPt +
                                    "jetPt.pdf)"), "pdf")


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
    fitFile = open("fitInfo.txt", "a+")
    try:
        with fitFile:
            if printEqn == "s":
                fitFile.write("\n Equation given by: \n \t "
                              "y = (par[0] / (1 + math.exp(-par[1] * (x[0]-par[2])))) + par[3] \n\n")
                fitFile.write("Chi2, NDF, prob, par1, par2, par3, par4 \n")
            if printEqn == "t":
                fitFile.write("\n Equation given by: \n \t subFunc = (x[0] - par[1]) / (par[2] * math.sqrt(x[0])) \n \t"
                              "y = (0.5 * par[0] * (1 + ROOT.TMath.Erf(subFunc))) + par[3] \n\n")
                fitFile.write("fitName, Chi2, NDF, prob, par1, par2, par3, par4 \n ")
            fitFile.write("{0:.3f}, {1:.3f}, {2:.3f}, {3:.3f}, {4:.3f}, {5:.3f} +/- {6:.3f}, {7:.3f} +/- {8:.3f}, "
                          "{9:.3f} +/- {10:.3f}, {11:.3f} +/- {12:.3f}\n " .format
                          (args.inputLFN, fitName, fit.GetChisquare(), fit.GetNDF(), fit.GetProb(), fit.GetParameter(0),
                           fit.GetParError(0), fit.GetParameter(1), fit.GetParError(1), fit.GetParameter(2),
                           fit.GetParError(2), fit.GetParameter(3), fit.GetParError(3)))

    except OSError:
        print("Could not open file!")


def inclusiveEfficiency(info):
    """
    Args:
        info (string): information to be written to file

    Returns:

    """
    fitFile = open("fitInfo.txt", "a+")
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
    if args == "ttjets":
        legStr = "#splitline{CMS}{t#bar{t} #rightarrow l #nu_{l} #plus jets}"
    elif args == "tttt":
        legStr = "#splitline{CMS}{t#bar{t}t#bar{t} #rightarrow l #nu_{l} #plus jets}"
    elif args == "tttt_weights":
        legStr = "#splitline{CMS}{t#bar{t}t#bar{t} #rightarrow l #nu_{l} #plus jets}"
    else:
        legStr = "#splitline{CMS}{W #rightarrow jets}"

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


def inputFileName(arg, selCrit):
    """

    Args:
        arg (string): string that specifies decay and decay channel
        selCrit (dictionary): dictionary of content selectionCriteria.txt

    Returns:
        inFile (string): input file name

    """

    if arg == "ttjets":
        inFile = "../OutFiles/Histograms/TT6Jets1Mu{0}jPt.root" .format(selCrit["minJetPt"])
    elif arg == "tttt_weights":
        inFile = "../OutFiles/Histograms/TTTTweights{0}jPt.root" .format(selCrit["minJetPt"])
    elif arg == "wjets":
        inFile = "../OutFiles/Histograms/Wjets{0}jPt.root" .format(selCrit["minJetPt"])
    elif arg == "tttt":
        inFile = "../OutFiles/Histograms/TTTT6Jets1Mu{0}jPt.root" .format(selCrit["minJetPt"])
    else:
        inFile = None

    return inFile


def main(argms):
    """ This code merges histograms, only for specific root file """

    trigList = getFileContents("trigList.txt", True)
    preSelCuts = getFileContents("../myInFiles/preSelectionCuts.txt", False)
    selCriteria = getFileContents("selectionCriteria.txt", False)
    
    inputFile = inputFileName(argms.inputLFN, selCriteria)

    # h = {}  # TH1D class
    # h_TriggerRatio = {}  # TEfficiency class
    # f = {}  # TF1 class

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
    h_metPt = {}
    h_metPhi = {}
    h_genMetPt = {}
    h_genMetPhi = {}

    h_TriggerRatio = {}

    f_jetHt = {}
    f_muonPt = {}

    # - Create canvases
    triggerCanvas = ROOT.TCanvas('triggerCanvas', 'Triggers', 750, 500)  # 1100 600
    triggerCanvas.SetFillColor(17)
    triggerCanvas.SetFrameFillColor(18)
    triggerCanvas.SetGrid()

    # - Open file and sub folder
    histFile = ROOT.TFile.Open(inputFile)
    histFile.cd("plots")

    # - Histograms
    h_jetHt["notrigger"] = ROOT.gDirectory.Get("h_jetHt_notrigger")
    h_jetHt["notrigger"].SetLineColor(1)
    if not (h_jetHt["notrigger"]):
        print("No trigger jet Ht histogram is empty")
    h_jetMult["notrigger"] = ROOT.gDirectory.Get("h_jetMult_notrigger")
    h_jetMult["notrigger"].SetLineColor(1)
    if not (h_jetMult["notrigger"]):
        print("No trigger jet Mult histogram is empty")
    h_jetBMult["notrigger"] = ROOT.gDirectory.Get("h_jetBMult_notrigger")
    h_jetBMult["notrigger"].SetLineColor(1)
    if not (h_jetBMult["notrigger"]):
        print("No trigger jet BMult histogram is empty")
    h_jetEta["notrigger"] = ROOT.gDirectory.Get("h_jetEta_notrigger")
    h_jetEta["notrigger"].SetLineColor(1)
    if not (h_jetEta["notrigger"]):
        print("No trigger jet Eta histogram is empty")
    h_jetPhi["notrigger"] = ROOT.gDirectory.Get("h_jetPhi_notrigger")
    h_jetPhi["notrigger"].SetLineColor(1)
    if not (h_jetPhi["notrigger"]):
        print("No trigger jet Phi histogram is empty")
    h_jetMap["notrigger"] = ROOT.gDirectory.Get("h_jetMap_notrigger")
    h_jetMap["notrigger"].SetLineColor(1)
    if not (h_jetMap["notrigger"]):
        print("No trigger jet map histogram is empty")

    h_muonPfRelIso04_all = ROOT.gDirectory.Get("h_muonRelIso04_all")
    h_muonGenPartFlav = ROOT.gDirectory.Get("h_muonGenPartFlav")
    h_muonGenPartIdx = ROOT.gDirectory.Get("h_muonGenPartIdx")

    h_muonPt["notrigger"] = ROOT.gDirectory.Get("h_muonPt_notrigger")
    h_muonPt["notrigger"].SetLineColor(1)
    if not (h_muonPt["notrigger"]):
        print("No trigger muon Pt histogram is empty")
    h_muonPt["prompt"] = ROOT.gDirectory.Get("h_muonPt_prompt")
    h_muonPt["prompt"].SetLineColor(4)
    if not (h_muonPt["prompt"]):
        print("top Mother muon Pt histogram is empty")
    h_muonPt["non-prompt"] = ROOT.gDirectory.Get("h_muonPt_non-prompt")
    h_muonPt["non-prompt"].SetLineColor(2)
    if not (h_muonPt["non-prompt"]):
        print("Bottom mother muon Pt histogram is empty")
    h_muonEta["notrigger"] = ROOT.gDirectory.Get("h_muonEta_notrigger")
    h_muonEta["notrigger"].SetLineColor(1)
    if not (h_muonEta["notrigger"]):
        print("No trigger muon eta histogram is empty")
    h_muonPhi["notrigger"] = ROOT.gDirectory.Get("h_muonPhi_notrigger")
    h_muonPhi["notrigger"].SetLineColor(1)
    if not (h_muonPhi["notrigger"]):
        print("No trigger muon Phi histogram is empty")
    h_muonMap["notrigger"] = ROOT.gDirectory.Get("h_muonMap_notrigger")
    h_muonMap["notrigger"].SetLineColor(1)
    if not (h_muonMap["notrigger"]):
        print("No trigger muon map histogram is empty")

    h_metPt["notrigger"] = ROOT.gDirectory.Get("h_metPt_notrigger")
    h_metPt["notrigger"].SetLineColor(1)
    if not (h_metPt["notrigger"]):
        print("No trigger met Pt histogram is empty")
    h_metPhi["notrigger"] = ROOT.gDirectory.Get("h_metPhi_notrigger")
    h_metPhi["notrigger"].SetLineColor(1)
    if not (h_metPhi["notrigger"]):
        print("No trigger met Phi histogram is empty")

    h_genMetPt["notrigger"] = ROOT.gDirectory.Get("h_genMetPt_notrigger")
    h_genMetPt["notrigger"].SetLineColor(1)
    if not (h_genMetPt["notrigger"]):
        print("No trigger genMet Pt histogram is empty")
    h_genMetPhi["notrigger"] = ROOT.gDirectory.Get("h_genMetPhi_notrigger")
    h_genMetPhi["notrigger"].SetLineColor(1)
    if not (h_genMetPhi["notrigger"]):
        print("No trigger genMet Phi histogram is empty")

    i = 2
    style = [1, 8, 9, 10]
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            h_jetHt[tg] = ROOT.gDirectory.Get("h_jetHt_" + tg)
            h_jetMult[tg] = ROOT.gDirectory.Get("h_jetMult_" + tg)
            h_jetBMult[tg] = ROOT.gDirectory.Get("h_jetBMult_" + tg)
            h_jetEta[tg] = ROOT.gDirectory.Get("h_jetEta_" + tg)
            h_jetPhi[tg] = ROOT.gDirectory.Get("h_jetPhi_" + tg)
            h_jetMap[tg] = ROOT.gDirectory.Get("h_jetMap_" + tg)

            h_muonPt[tg] = ROOT.gDirectory.Get("h_muonPt_" + tg)
            h_muonEta[tg] = ROOT.gDirectory.Get("h_muonEta_" + tg)
            h_muonPhi[tg] = ROOT.gDirectory.Get("h_muonPhi_" + tg)
            h_muonMap[tg] = ROOT.gDirectory.Get("h_muonMap_" + tg)

            h_metPt[tg] = ROOT.gDirectory.Get("h_metPt_" + tg)
            h_metPhi[tg] = ROOT.gDirectory.Get("h_metPhi_" + tg)
            h_genMetPt[tg] = ROOT.gDirectory.Get("h_genMetPt_" + tg)
            h_genMetPhi[tg] = ROOT.gDirectory.Get("h_genMetPhi_" + tg)

            h_jetHt[tg].SetLineColor(i)
            h_jetMult[tg].SetLineColor(i)
            h_jetBMult[tg].SetLineColor(i)
            h_jetEta[tg].SetLineColor(i)
            h_jetPhi[tg].SetLineColor(i)
            h_muonPt[tg].SetLineColor(i)
            h_muonEta[tg].SetLineColor(i)
            h_muonPhi[tg].SetLineColor(i)
            h_metPt[tg].SetLineColor(i)
            h_metPhi[tg].SetLineColor(i)
            h_genMetPt[tg].SetLineColor(i)
            h_genMetPhi[tg].SetLineColor(i)

            f_jetHt[tg] = ROOT.TF1('jetHt' + tg, turnOnFit, 200, 2500, 4)
            f_jetHt[tg].SetLineColor(1)
            f_jetHt[tg].SetParNames("saturation_Y", "slope", "x_turnON", "initY")
            f_jetHt[tg].SetParLimits(0, 0.4, 1)
            f_jetHt[tg].SetParLimits(1, 2, 25)
            f_jetHt[tg].SetParLimits(2, -100, 500)
            f_jetHt[tg].SetParLimits(3, -0.1, 0.1)
            f_jetHt[tg].SetLineStyle(style[i - 2])

            f_muonPt[tg] = ROOT.TF1('f_muonPt' + tg, turnOnFit, 0, 250, 4)
            f_muonPt[tg].SetLineColor(1)
            f_muonPt[tg].SetParNames("saturation_Y", "slope", "x_turnON", "initY")
            f_muonPt[tg].SetLineStyle(style[i - 2])

            i += 1

    # - Events histogram
    h_eventsPrg = ROOT.gDirectory.Get("h_eventsPrg")
    if not h_eventsPrg:
        print("h_eventsPrg histogram is empty")
        return

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

    ROOT.gStyle.SetOptTitle(0)

    # - HT plots for mu Triggers ---------------------------------
    cv1 = triggerCanvas.cd(1)
    h_jetHt["notrigger"].Draw('E1')
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            h_jetHt[tg].Draw('E1 same')
    cv1.BuildLegend(0.47, 0.54, 0.97, 0.74)
    ROOT.gStyle.SetLegendTextSize(0.02)
    tX1 = 0.6*(h_jetHt["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95*(h_jetHt["notrigger"].GetMaximum())
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas, selCriteria)

    cv2 = triggerCanvas.cd(1)
    i = 0
    j = 2
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            if ROOT.TEfficiency.CheckConsistency(h_jetHt[tg], h_jetHt["notrigger"]):
                h_TriggerRatio[tg] = ROOT.TEfficiency(h_jetHt[tg], h_jetHt["notrigger"])
                xTitle = h_jetHt["notrigger"].GetXaxis().GetTitle()
                xBinWidth = h_jetHt["notrigger"].GetXaxis().GetBinWidth(1)
                h_TriggerRatio[tg].SetTitle(";{0};Trigger Efficiency per {1}GeV/c".format(xTitle, round(xBinWidth)))
                h_TriggerRatio[tg].SetName(tg)
                h_TriggerRatio[tg].SetTitle(tg)
                h_TriggerRatio[tg].SetLineColor(j)
                j += 1
                if i == 0:
                    # h_TriggerRatio[tg].GetListOfFunctions().AddFirst(f_jetHt[tg])
                    f_jetHt[tg].SetParameters(0.8, 20, 135, 0)
                    h_TriggerRatio[tg].Fit(f_jetHt[tg], 'LVR')  # L= log likelihood, V=verbose, R=range in function
                    fitInfo(fit=f_jetHt[tg], printEqn="t", fitName=("jetHt" + tg), args=argms)
                    h_TriggerRatio[tg].Draw('AP')
                    cv2.Update()
                    graph1 = h_TriggerRatio[tg].GetPaintedGraph()
                    graph1.SetMinimum(0)
                    graph1.SetMaximum(1.2)
                    cv2.Update()
                    tX1 = 0.05*(h_jetHt["notrigger"].GetXaxis().GetXmax())
                    tY1 = 1.1
                    # assymGraph = h_TriggerRatio[tg].CreateGraph()
                elif i > 0:
                    if i == 1: f_jetHt[tg].SetParameters(0.8, 5, 500, 0)
                    elif i == 2: f_jetHt[tg].SetParameters(0.8, 10, 330, 0)
                    elif i == 3: f_jetHt[tg].SetParameters(0.8, 5, 500, 0)
                    h_TriggerRatio[tg].Fit(f_jetHt[tg], 'LVR')
                    fitInfo(fit=f_jetHt[tg], printEqn="n", fitName=("jetHt" + tg), args=argms)
                    h_TriggerRatio[tg].Draw('same')
                i += 1
    cv2.BuildLegend(0.4, 0.1, 0.9, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas, selCriteria)

    cv82 = triggerCanvas.cd(1)
    i = 0
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            h_TriggerRatio[tg] = h_jetHt[tg].Clone("h_jetHtRatio" + tg)
            h_TriggerRatio[tg].Sumw2()
            h_TriggerRatio[tg].SetStats(0)
            h_TriggerRatio[tg].Divide(h_jetHt["notrigger"])
            h_TriggerRatio[tg].Rebin(300)
            print(h_TriggerRatio[tg].GetBinContent(1))
            inEff = h_TriggerRatio[tg].GetBinContent(1) / 300
            print(h_TriggerRatio[tg].GetBinError(1))
            inErEff = h_TriggerRatio[tg].GetBinError(1) / 300
            inclusiveEfficiency(" Jet HT Eff = {0:.3f} +/- {1:.3f} , {2} \n".format(inEff, inErEff, tg))
            xTitle = h_jetHt["notrigger"].GetXaxis().GetTitle()
            xBinWidth = h_jetHt["notrigger"].GetXaxis().GetBinWidth(1)
            h_TriggerRatio[tg].SetTitle(";{0};Trigger Efficiency per {1} GeV/c".format(xTitle, round(xBinWidth)))
            h_TriggerRatio[tg].SetName(tg)
            if i == 0:
                h_TriggerRatio[tg].SetMinimum(0.)
                h_TriggerRatio[tg].SetMaximum(301.8)
                h_TriggerRatio[tg].Draw()
                tX1 = 0.05 * (h_jetHt["notrigger"].GetXaxis().GetXmax())
                tY1 = 1.1
            if i > 0:
                h_TriggerRatio[tg].Draw('same')
            i += 1
    cv82.BuildLegend(0.4, 0.1, 0.9, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas, selCriteria)

    # - Jet Multiplicity plots ---------------------------------
    cv3 = triggerCanvas.cd(1)
    h_jetMult["notrigger"].GetXaxis().SetTitle("Number of Jets")
    h_jetMult["notrigger"].Draw('E1')
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            h_jetMult[tg].Draw('E1 same')
    cv3.BuildLegend(0.47, 0.54, 0.97, 0.74)
    ROOT.gStyle.SetLegendTextSize(0.02)
    tX1 = 0.6 * (h_jetMult["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95 * (h_jetMult["notrigger"].GetMaximum())
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas, selCriteria)

    cv4 = triggerCanvas.cd(1)
    i = 0
    j = 2
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            if ROOT.TEfficiency.CheckConsistency(h_jetMult[tg], h_jetMult["notrigger"]):
                h_TriggerRatio[tg] = ROOT.TEfficiency(h_jetMult[tg], h_jetMult["notrigger"])
                # xTitle = h_jetMult["notrigger"].GetXaxis().GetTitle()
                # xBinWidth = h_jetMult["notrigger"].GetXaxis().GetBinWidth(1)
                h_TriggerRatio[tg].SetTitle(";Number of Jets ;Trigger Efficiency per Number of Jets")
                h_TriggerRatio[tg].SetName(tg)
                h_TriggerRatio[tg].SetTitle(tg)
                h_TriggerRatio[tg].SetLineColor(j)
                j += 1
                if i == 0:
                    h_TriggerRatio[tg].Draw('AP')
                    cv4.Update()
                    graph1 = h_TriggerRatio[tg].GetPaintedGraph()
                    graph1.SetMinimum(0)
                    graph1.SetMaximum(1.2)
                    cv4.Update()
                    tX1 = 0.05 * ((h_jetMult["notrigger"].GetXaxis().GetXmax())-5)+5
                    tY1 = 1.1
                if i > 0:
                    h_TriggerRatio[tg].Draw('same')
            i += 1
    cv4.BuildLegend(0.4, 0.1, 0.9, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas, selCriteria)

    # - B tagged Jet Multiplicity plots ---------------------------
    cv5 = triggerCanvas.cd(1)
    # h_jetBMult["notrigger"].SetTitle("")
    h_jetBMult["notrigger"].GetXaxis().SetRange(1, 10)
    h_jetBMult["notrigger"].Draw('E1')
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            h_jetBMult[tg].Draw('E1 same')
    cv5.BuildLegend(0.47, 0.54, 0.97, 0.74)
    ROOT.gStyle.SetLegendTextSize(0.02)
    tX1 = 0.6 * (h_jetBMult["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95 * (h_jetBMult["notrigger"].GetMaximum())
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas, selCriteria)

    cv6 = triggerCanvas.cd(1)
    i = 0
    j = 2
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            if ROOT.TEfficiency.CheckConsistency(h_jetBMult[tg], h_jetBMult["notrigger"]):
                h_TriggerRatio[tg] = ROOT.TEfficiency(h_jetBMult[tg], h_jetBMult["notrigger"])
                xTitle = h_jetBMult["notrigger"].GetXaxis().GetTitle()
                xBinWidth = h_jetBMult["notrigger"].GetXaxis().GetBinWidth(1)
                h_TriggerRatio[tg].SetTitle(";{0};Trigger Efficiency per {1} GeV/c".format(xTitle, xBinWidth))
                h_TriggerRatio[tg].SetName(tg)
                h_TriggerRatio[tg].SetTitle(tg)
                h_TriggerRatio[tg].SetLineColor(j)
                j += 1
                if i == 0:
                    h_TriggerRatio[tg].Draw('AP')
                    cv6.Update()
                    graph1 = h_TriggerRatio[tg].GetPaintedGraph()
                    graph1.SetMinimum(0)
                    graph1.SetMaximum(1.2)
                    cv6.Update()
                    tX1 = 0.05 * (h_jetBMult["notrigger"].GetXaxis().GetXmax())
                    tY1 = 1.1
                if i > 0:
                    h_TriggerRatio[tg].Draw('same')
            i += 1
    cv6.BuildLegend(0.4, 0.1, 0.9, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas, selCriteria)

    # - Muon test Plots-------------------------------
    triggerCanvas.cd(1)
    h_muonGenPartFlav.Draw()
    pdfCreator(argms, 1, triggerCanvas, selCriteria)

    triggerCanvas.cd(1)
    h_muonGenPartIdx.Draw()
    pdfCreator(argms, 1, triggerCanvas, selCriteria)

    triggerCanvas.cd(1)
    h_muonPfRelIso04_all.Draw()
    pdfCreator(argms, 1, triggerCanvas, selCriteria)

    # - Muon pT plots ---------------------------------
    cv7 = triggerCanvas.cd(1)
    # h_muonPt["notrigger"].SetTitle("")
    h_muonPt["notrigger"].SetMinimum(0.)
    # h_muonPt["notrigger"].SetMaximum(3500)
    h_muonPt["notrigger"].Draw('E1')
    tX1 = 0.60*(h_muonPt["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95*(h_muonPt["notrigger"].GetMaximum())
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            h_muonPt[tg].Draw('E1 same')
    cv7.BuildLegend(0.47, 0.54, 0.97, 0.74)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas, selCriteria)

    cv71 = triggerCanvas.cd(1)
    # h_muonPt["notrigger"].SetTitle("")
    h_muonPt["notrigger"].SetMinimum(0.)
    # h_muonPt["notrigger"].SetMaximum(3500)
    h_muonPt["notrigger"].Draw('E1')
    tX1 = 0.6*(h_muonPt["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95*(h_muonPt["notrigger"].GetMaximum())
    h_muonPt["prompt"].SetTitle("prompt muons")
    h_muonPt["prompt"].Draw('E1 same')
    h_muonPt["non-prompt"].Draw('E1 same')
    cv71.BuildLegend(0.47, 0.54, 0.97, 0.74)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas, selCriteria)

    cv8 = triggerCanvas.cd(1)
    i = 0
    j = 2
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            if ROOT.TEfficiency.CheckConsistency(h_muonPt[tg], h_muonPt["notrigger"]):
                h_TriggerRatio[tg] = ROOT.TEfficiency(h_muonPt[tg], h_muonPt["notrigger"])
                xTitle = h_muonPt["notrigger"].GetXaxis().GetTitle()
                xBinWidth = h_muonPt["notrigger"].GetXaxis().GetBinWidth(1)
                h_TriggerRatio[tg].SetTitle(";{0};Trigger Efficiency per {1} GeV/c".format(xTitle, xBinWidth))
                h_TriggerRatio[tg].SetName(tg)
                h_TriggerRatio[tg].SetTitle(tg)
                h_TriggerRatio[tg].SetLineColor(j)
                j += 1
                if i == 0:
                    f_muonPt[tg].SetParameters(0.8, 0.95, 24, 0.05)
                    f_muonPt[tg].SetParLimits(0, 0.7, 0.9)
                    f_muonPt[tg].SetParLimits(1, 0, 5)
                    f_muonPt[tg].SetParLimits(2, 20, 40)
                    f_muonPt[tg].SetParLimits(3, 0.01, 0.05)
                    h_TriggerRatio[tg].Fit(f_muonPt[tg], 'LR')  # L= log likelihood, V=verbose, R=range in function
                    fitInfo(fit=f_muonPt[tg], printEqn="t", fitName=("muonPt" + tg), args=argms)
                    h_TriggerRatio[tg].Draw('AP')
                    cv8.Update()
                    graph1 = h_TriggerRatio[tg].GetPaintedGraph()
                    graph1.SetMinimum(0)
                    graph1.SetMaximum(1.2)
                    cv8.Update()
                    tX1 = 0.05 * (h_muonPt["notrigger"].GetXaxis().GetXmax())
                    tY1 = 1.1
                if i > 0:
                    if i == 1:
                        f_muonPt[tg].SetParameters(0.05, 1000, 24, 0.8)
                        f_muonPt[tg].SetParLimits(0, 0, 0.1)
                        f_muonPt[tg].SetParLimits(1, 100, 2000)
                        f_muonPt[tg].SetParLimits(2, 20, 40)
                        f_muonPt[tg].SetParLimits(3, 0.8, 0.9)
                    elif i == 2:
                        f_muonPt[tg].SetParameters(0.18, 0.95, 24, 0.8)
                        f_muonPt[tg].SetParLimits(0, 0.1, 0.2)
                        f_muonPt[tg].SetParLimits(1, 0, 10)
                        f_muonPt[tg].SetParLimits(2, 20, 40)
                        f_muonPt[tg].SetParLimits(3, 0.8, 0.9)
                    elif i == 3:
                        f_muonPt[tg].SetParameters(0.75, 0.95, 15, 0.15)
                        f_muonPt[tg].SetParLimits(0, 0.5, 0.9)
                        f_muonPt[tg].SetParLimits(1, 0, 10)
                        f_muonPt[tg].SetParLimits(2, 0, 30)
                        f_muonPt[tg].SetParLimits(3, 0.1, 0.3)
                    h_TriggerRatio[tg].Fit(f_muonPt[tg], 'LR')
                    fitInfo(fit=f_muonPt[tg], printEqn="n", fitName=("muonPt" + tg), args=argms)
                    h_TriggerRatio[tg].Draw('same')
            i += 1
    cv8.BuildLegend(0.4, 0.1, 0.9, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas, selCriteria)

    cv81 = triggerCanvas.cd(1)
    i = 0
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            h_TriggerRatio[tg] = h_muonPt[tg].Clone("h_muonPtRatio" + tg)
            h_TriggerRatio[tg].Sumw2()
            h_TriggerRatio[tg].SetStats(0)
            h_TriggerRatio[tg].Divide(h_muonPt["notrigger"])
            h_TriggerRatio[tg].Rebin(300)
            print(h_TriggerRatio[tg].GetBinContent(1))
            inEff = h_TriggerRatio[tg].GetBinContent(1)/300
            print(h_TriggerRatio[tg].GetBinError(1))
            inErEff = h_TriggerRatio[tg].GetBinError(1)/300
            inclusiveEfficiency("Muon Pt Eff = {0:.3f} +/- {1:.3f} , {2} \n" .format(inEff, inErEff, tg))
            xTitle = h_muonPt["notrigger"].GetXaxis().GetTitle()
            xBinWidth = h_muonPt["notrigger"].GetXaxis().GetBinWidth(1)
            h_TriggerRatio[tg].SetTitle(";{0};Trigger Efficiency per {1:.2f} GeV/c".format(xTitle, xBinWidth))
            h_TriggerRatio[tg].SetName(tg)
            if i == 0:
                h_TriggerRatio[tg].SetMinimum(0.)
                h_TriggerRatio[tg].SetMaximum(301.8)
                h_TriggerRatio[tg].Draw()
                tX1 = 0.05 * (h_muonPt["notrigger"].GetXaxis().GetXmax())
                tY1 = 1.1
            if i > 0:
                h_TriggerRatio[tg].Draw('same')
            i += 1
    cv81.BuildLegend(0.4, 0.1, 0.9, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas, selCriteria)

    # - MET pT plots ---------------------------------
    cv9 = triggerCanvas.cd(1)
    h_metPt["notrigger"].GetXaxis().SetTitle("E^{Miss}_{T}")
    h_metPt["notrigger"].SetMinimum(0.)
    # h_metPt["notrigger"].SetMaximum(1800)
    h_metPt["notrigger"].Draw('E1')
    tX1 = 0.6 * (h_metPt["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95 * (h_metPt["notrigger"].GetMaximum())
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            h_metPt[tg].Draw('E1 same')
    cv9.BuildLegend(0.47, 0.54, 0.97, 0.74)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas, selCriteria)

    cv10 = triggerCanvas.cd(1)
    i = 0
    j = 2
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            if ROOT.TEfficiency.CheckConsistency(h_metPt[tg], h_metPt["notrigger"]):
                h_TriggerRatio[tg] = ROOT.TEfficiency(h_metPt[tg], h_metPt["notrigger"])
                # xTitle = h_metPt["notrigger"].GetXaxis().GetTitle()
                xBinWidth = h_metPt["notrigger"].GetXaxis().GetBinWidth(1)
                h_TriggerRatio[tg].SetTitle(";E^{Miss}_{T};Trigger Efficiency per %.2f GeV/c" % xBinWidth)
                h_TriggerRatio[tg].SetName(tg)
                h_TriggerRatio[tg].SetTitle(tg)
                h_TriggerRatio[tg].SetLineColor(j)
                j += 1
                if i == 0:
                    h_TriggerRatio[tg].Draw('AP')
                    cv10.Update()
                    graph1 = h_TriggerRatio[tg].GetPaintedGraph()
                    graph1.SetMinimum(0)
                    graph1.SetMaximum(1.2)
                    cv10.Update()
                    tX1 = 0.05 * (h_metPt["notrigger"].GetXaxis().GetXmax())
                    tY1 = 1.1
                if i > 0:
                    h_TriggerRatio[tg].Draw('same')
            i += 1
    cv10.BuildLegend(0.4, 0.1, 0.9, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas, selCriteria)

    # - GenMET pT plots ---------------------------------
    cv11 = triggerCanvas.cd(1)
    h_genMetPt["notrigger"].GetXaxis().SetTitle("Gen E^{Miss}_{T}")
    h_genMetPt["notrigger"].SetMinimum(0.)
    # h_genMetPt["notrigger"].SetMaximum(2000)
    h_genMetPt["notrigger"].Draw('E1')
    tX1 = 0.6 * (h_genMetPt["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95 * (h_genMetPt["notrigger"].GetMaximum())
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            h_genMetPt[tg].Draw('E1 same')
    cv11.BuildLegend(0.47, 0.54, 0.97, 0.74)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas, selCriteria)

    cv12 = triggerCanvas.cd(1)
    i = 0
    j = 2
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            if ROOT.TEfficiency.CheckConsistency(h_genMetPt[tg], h_genMetPt["notrigger"]):
                h_TriggerRatio[tg] = ROOT.TEfficiency(h_genMetPt[tg], h_genMetPt["notrigger"])
                # xTitle = h_genMetPt["notrigger"].GetXaxis().GetTitle()
                xBinWidth = h_genMetPt["notrigger"].GetXaxis().GetBinWidth(1)
                h_TriggerRatio[tg].SetTitle("; Gen E^{Miss}_{T};Trigger Efficiency per %.2f GeV/c" % xBinWidth)
                h_TriggerRatio[tg].SetName(tg)
                h_TriggerRatio[tg].SetTitle(tg)
                h_TriggerRatio[tg].SetLineColor(j)
                j += 1
                if i == 0:
                    h_TriggerRatio[tg].Draw('AP')
                    cv12.Update()
                    graph1 = h_TriggerRatio[tg].GetPaintedGraph()
                    graph1.SetMinimum(0)
                    graph1.SetMaximum(1.2)
                    cv12.Update()
                    tX1 = 0.05 * (h_genMetPt["notrigger"].GetXaxis().GetXmax())
                    tY1 = 1.1
                if i > 0:
                    h_TriggerRatio[tg].Draw('same')
            i += 1
    cv12.BuildLegend(0.4, 0.1, 0.9, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas, selCriteria)

    # - Eta plots ------------------------------------------
    cv13 = triggerCanvas.cd(1)
    # h_jetEta["notrigger"].GetYaxis().SetTitleOffset(1.1)
    h_jetEta["notrigger"].Draw('E1')
    tX1 = 0.6*14
    tY1 = 0.95*(h_jetEta["notrigger"].GetMaximum())
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            h_jetEta[tg].Draw('E1 same')
    cv13.BuildLegend(0.4, 0.25, 0.4, 0.25)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas, selCriteria)

    cv14 = triggerCanvas.cd(1)
    h_muonEta["notrigger"].Draw('E1')
    tX1 = (0.6*14)-6
    tY1 = 0.95*(h_muonEta["notrigger"].GetMaximum())
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            h_muonEta[tg].Draw('E1 same')
    cv14.BuildLegend(0.4, 0.25, 0.4, 0.25)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas, selCriteria)

    cv15 = triggerCanvas.cd(1)
    i = 0
    j = 2
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            if ROOT.TEfficiency.CheckConsistency(h_muonEta[tg], h_muonEta["notrigger"]):
                h_TriggerRatio[tg] = ROOT.TEfficiency(h_muonEta[tg], h_muonEta["notrigger"])
                xTitle = h_muonEta["notrigger"].GetXaxis().GetTitle()
                xBinWidth = h_muonEta["notrigger"].GetXaxis().GetBinWidth(1)
                h_TriggerRatio[tg].SetTitle(";{0};Trigger Efficiency per {1:.3f} GeV/c".format(xTitle, xBinWidth))
                h_TriggerRatio[tg].SetName(tg)
                h_TriggerRatio[tg].SetTitle(tg)
                h_TriggerRatio[tg].SetLineColor(j)
                j += 1
                if i == 0:
                    h_TriggerRatio[tg].Draw('AP')
                    cv15.Update()
                    graph1 = h_TriggerRatio[tg].GetPaintedGraph()
                    graph1.SetMinimum(0)
                    graph1.SetMaximum(1.2)
                    cv15.Update()
                    tX1 = 0.05 * (h_muonEta["notrigger"].GetXaxis().GetXmax())
                    tY1 = 1.1
                if i > 0:
                    h_TriggerRatio[tg].Draw('same')
            i += 1
    cv15.BuildLegend(0.4, 0.1, 0.9, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas, selCriteria)

    # - Phi plots ------------------------------------------
    cv16 = triggerCanvas.cd(1)
    # h_jetPhi["notrigger"].GetYaxis().SetTitleOffset(1.3)
    h_jetPhi["notrigger"].Draw('E1')
    tX1 = 0.6*6
    tY1 = 0.95*(h_jetPhi["notrigger"].GetMaximum())
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            h_jetPhi[tg].Draw('E1 same')
    cv16.BuildLegend(0.4, 0.2, 0.4, 0.2)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    # pdfCreator(argms, 1, triggerCanvas, selCriteria)

    cv17 = triggerCanvas.cd(1)
    # h_muonPhi["notrigger"].GetYaxis().SetTitleOffset(1.4)
    h_muonPhi["notrigger"].Draw('E1')
    tX1 = 0.6*6
    tY1 = 0.97*(h_muonPhi["notrigger"].GetMaximum())
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            h_muonPhi[tg].Draw('E1 same')
    cv17.BuildLegend(0.4, 0.2, 0.4, 0.2)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    # pdfCreator(argms, 1, triggerCanvas, selCriteria)

    # - Eta-Phi Map plots ------------------------------------------
    triggerCanvas.cd(1)
    h_jetMap["notrigger"].Draw('COLZ')  # CONT4Z
    # pdfCreator(argms, 1, triggerCanvas, selCriteria)
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            h_jetMap[tg].Draw('COLZ')
            # pdfCreator(argms, 1, triggerCanvas, selCriteria)

    h_muonMap["notrigger"].Draw('COLZ')
    # pdfCreator(argms, 1, triggerCanvas, selCriteria)
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            h_muonMap[tg].Draw('COLZ')  # E
            # pdfCreator(argms, 1, triggerCanvas, selCriteria)

    #############################################################################
    # - Test Event numbers along steps ----------
    triggerCanvas.cd(1)
    h_eventsPrg.SetFillColor(ROOT.kAzure-9)
    h_eventsPrg.GetXaxis().SetLabelOffset(999)
    h_eventsPrg.GetXaxis().SetLabelSize(0)
    h_eventsPrg.Draw()
    tY1 = 0.05*(h_eventsPrg.GetMaximum())
    ltx.SetTextAngle(88)
    ltx.DrawLatex(0.5, tY1, "Pre-selection")
    ltx.DrawLatex(1.5, tY1, "Post-selection")
    i = 0
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            ltx.DrawLatex((5.5 - i), tY1, tg)
            i += 1

    # h.GetXAxis().SetBinLabel(binnumber,string)
    pdfCreator(argms, 2, triggerCanvas, selCriteria)

    histFile.Close()


main(process_arguments())
