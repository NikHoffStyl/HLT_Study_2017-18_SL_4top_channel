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


def pdfCreator(parg, arg, canvas):
    """
        Create a pdf of histograms
        Args:
            parg (class): commandline arguments
            arg (int): print argument
            canvas (TCanvas): canvas which includes plot
    """
    time_ = datetime.now()
    filename = time_.strftime("TriggerPlots/W%V_%y/%w%a_" + parg.inputLFN + ".pdf")
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    if arg == 0:
        canvas.Print(time_.strftime("TriggerPlots/W%V_%y/%w%a_" + parg.inputLFN + ".pdf("), "pdf")
    if arg == 1:
        canvas.Print(time_.strftime("TriggerPlots/W%V_%y/%w%a_" + parg.inputLFN + ".pdf"), "pdf")
    if arg == 2:
        canvas.Print(time_.strftime("TriggerPlots/W%V_%y/%w%a_" + parg.inputLFN + ".pdf)"), "pdf")


def fitf(x, par):
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


def fitInfo(fileName="fitInfo", fit=ROOT.TF1()):
    """
        Print fit parameter values and their errors along with the statistics

    :param fileName: where info will be printed
    :param fit: function fitted to histogram
    :return:
    """
    try:
        file = open(fileName + ".csv", "a+")
        with file:
            file.write(
                "{0}, {1}, {2}, {3}, {4} \r ".format(fit.GetChisquare(), fit.GetParameter(0), fit.GetParameter(1),
                                                     fit.GetParameter(2), fit.GetParameter(3)))
    except OSError:
        print("Could not open file! Please close Excel!")


def main(argms):
    """ This code merges histograms, only for specific root file """

    if argms.inputLFN == "ttjets":
        inputFile = "../OutFiles/Histograms/TT6Jets1Mu.root"
    elif argms.inputLFN == "tttt_weights":
        inputFile = "../OutFiles/Histograms/TTTTweights.root"
    elif argms.inputLFN == "wjets":
        inputFile = "../OutFiles/Histograms/Wjets.root"
    elif argms.inputLFN == "tttt":
        inputFile = "../OutFiles/Histograms/TTTT6Jets1Mu.root"
    else:
        return 0

    trigList = {}
    with open("trigList.txt") as f:
        for line in f:
            if line.find(":") == -1: continue
            (key1, val) = line.split(": ")
            c = len(val) - 1
            val = val[0:c]
            trigList[key1] = val.split(", ")

    preSelCuts = {}
    with open("../myInFiles/preSelectionCuts.txt") as f:
        for line in f:
            if line.find(":") == -1: continue
            (key1, val) = line.split(": ")
            c = len(val) - 1
            val = val[0:c]
            preSelCuts[key1] = val

    selCriteria = {}
    with open("selectionCriteria.txt") as f:
        for line in f:
            if line.find(":") == -1: continue
            (key1, val) = line.split(": ")
            c = len(val) - 1
            val = val[0:c]
            selCriteria[key1] = val
            
    h = {}  # TH1D class
    h_TriggerRatio = {}  # TEfficiency class
    f = {}  # TF1 class

    # - Create canvases
    triggerCanvas = ROOT.TCanvas('triggerCanvas', 'Triggers', 700, 500)  # 1100 600
    triggerCanvas.SetFillColor(33)
    triggerCanvas.SetFrameFillColor(41)
    triggerCanvas.SetGrid()

    # - Open file and sub folder
    histFile = ROOT.TFile.Open(inputFile)
    histFile.cd("plots")

    # - Histograms
    h_muonPfRelIso04_all = ROOT.gDirectory.Get("h_muonRelIso04_all")
    h_muonGenPartFlav = ROOT.gDirectory.Get("h_muonGenPartFlav")
    h_muonGenPartIdx = ROOT.gDirectory.Get("h_muonGenPartIdx")
    h["muonPt_prompt"].SetLineColor(4)
    if not (h["muonPt_prompt"]):
        print("top Mother muon Pt histogram is empty")
    h["muonPt_non-prompt"].SetLineColor(2)
    if not (h["muonPt_non-prompt"]):
        print("Bottom mother muon Pt histogram is empty")
     
    h["jetHt_notrigger"] = ROOT.gDirectory.Get("h_jetHt_notrigger") 
    h["jetMult_notrigger"] = ROOT.gDirectory.Get("h_jetMult_notrigger")
    h["jetBMult_notrigger"] = ROOT.gDirectory.Get("h_jetBMult_notrigger")
    h["jetEta_notrigger"] = ROOT.gDirectory.Get("h_jetEta_notrigger")
    h["jetPhi_notrigger"] = ROOT.gDirectory.Get("h_jetPhi_notrigger")
    h["jetMap_notrigger"] = ROOT.gDirectory.Get("h_jetMap_notrigger")
    h["muonPt_notrigger"] = ROOT.gDirectory.Get("h_muonPt_notrigger")
    h["muonPt_prompt"] = ROOT.gDirectory.Get("h_muonPt_prompt")
    h["muonPt_non-prompt"] = ROOT.gDirectory.Get("h_muonPt_non-prompt")
    h["muonEta_notrigger"] = ROOT.gDirectory.Get("h_muonEta_notrigger")
    h["muonPhi_notrigger"] = ROOT.gDirectory.Get("h_muonPhi_notrigger")
    h["muonMap_notrigger"] = ROOT.gDirectory.Get("h_muonMap_notrigger")
    h["metPt_notrigger"] = ROOT.gDirectory.Get("h_metPt_notrigger")
    h["metPhi_notrigger"] = ROOT.gDirectory.Get("h_metPhi_notrigger")
    h["genMetPt_notrigger"] = ROOT.gDirectory.Get("h_genMetPt_notrigger")
    h["genMetPhi_notrigger"] = ROOT.gDirectory.Get("h_genMetPhi_notrigger")
    
    for hName in h:
        if not hName.find("notrigger") == -1: continue
        for histo in h[hName]:
            histo.SetLineColor(1)
            if not histo:
                print("Histogram %s is empty" % hName)
    
    i = 2
    style = [1, 8, 9, 10]
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            h["jetHt_" + tg] = ROOT.gDirectory.Get("h_jetHt_" + tg)
            h["jetMult_" + tg] = ROOT.gDirectory.Get("h_jetMult_" + tg)
            h["jetBMult_" + tg] = ROOT.gDirectory.Get("h_jetBMult_" + tg)
            h["jetEta_" + tg] = ROOT.gDirectory.Get("h_jetEta_" + tg)
            h["jetPhi_" + tg] = ROOT.gDirectory.Get("h_jetPhi_" + tg)
            h["jetMap_" + tg] = ROOT.gDirectory.Get("h_jetMap_" + tg)

            h["muonPt_" + tg] = ROOT.gDirectory.Get("h_muonPt_" + tg)
            h["muonEta_" + tg] = ROOT.gDirectory.Get("h_muonEta_" + tg)
            h["muonPhi_" + tg] = ROOT.gDirectory.Get("h_muonPhi_" + tg)
            h["muonMap_" + tg] = ROOT.gDirectory.Get("h_muonMap_" + tg)

            h["metPt_" + tg] = ROOT.gDirectory.Get("h_metPt_" + tg)
            h["metPhi_" + tg] = ROOT.gDirectory.Get("h_metPhi_" + tg)
            h["genMetPt_" + tg] = ROOT.gDirectory.Get("h_genMetPt_" + tg)
            h["genMetPhi_" + tg] = ROOT.gDirectory.Get("h_genMetPhi_" + tg)

            for hName in h:
                if not hName.find(tg) == -1: continue
                for histo in h[hName]:
                    histo.SetLineColor(i)
                    if not histo:
                        print("Histogram %s is empty" % hName)

            f["jetHt_" + tg] = ROOT.TF1('f_jetHt' + tg, fitf, 200, 1500, 4)
            f["jetHt_" + tg].SetParameters(0.7, 0.0045, 100, 0.14)
            f["jetHt_" + tg].SetParLimits(0, 0.4, 0.8)
            f["jetHt_" + tg].SetParLimits(1, 0, 0.99)
            f["jetHt_" + tg].SetParLimits(2, -100, 500)
            f["jetHt_" + tg].SetParLimits(3, -0.1, 0.2)
            f["jetMult_" + tg] = ROOT.TF1('f_jetMult' + tg, fitf, 20, 0, 20)
            f["jetBMult_" + tg] = ROOT.TF1('f_jetBMult' + tg, fitf, 20, 0, 20)
            f["jetEta_" + tg] = ROOT.TF1('f_jetEta' + tg, fitf, 300, -6, 8)
            f["jetPhi_" + tg] = ROOT.TF1('f_jetPhi' + tg, fitf, 300, -6, 8)
            f["muonPt_" + tg] = ROOT.TF1('f_muonPt' + tg, fitf, 300, 0, 300)
            f["muonEta_" + tg] = ROOT.TF1('f_muonEta' + tg, fitf, 300, -6, 8)
            f["muonPhi_" + tg] = ROOT.TF1('f_muonPhi' + tg, fitf, 300, -6, 8)
            f["metPt_" + tg] = ROOT.TF1('f_metPt' + tg, fitf, 300, 0, 300)
            f["metPhi_" + tg] = ROOT.TF1('f_metPhi' + tg, fitf, 300, -6, 8)
            f["genMetPt_" + tg] = ROOT.TF1('f_genMetPt' + tg, fitf, 300, 0, 300)
            f["genMetPhi_" + tg] = ROOT.TF1('f_genMetPhi' + tg, fitf, 300, -6, 8)

            for fName in f:
                if not fName.find(tg) == -1: continue
                for function in f[fName]:
                    function.SetLineColor(1)
                    function.SetParNames("saturation_Y", "slope", "x_turnON", "initY")
                    function.SetLineStyle(style[i - 2])

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
    ltx.DrawLatex(0.10, 0.70, "On-line (pre-)selection Requisites for:")
    ltx.DrawLatex(0.16, 0.65, "#bullet Jets: #bf{number > %s}" % preSelCuts["nJet"])
    ltx.DrawLatex(0.16, 0.60, "#bullet Muons plus Electrons: #bf{number > %s }" % preSelCuts["nLepton"])
    ltx.DrawLatex(0.10, 0.50, "Event Limit: #bf{None (see last page)}")
    ltx.DrawLatex(0.10, 0.40, "Off-line (post-)selection Requisites for:")
    ltx.DrawLatex(0.16, 0.35, "#bullet Jets: #bf{jetId > %s , p_{T} > %s and |#eta|<%s (for at least 6 jets)}"
                  % (selCriteria["minJetId"], selCriteria["minJetPt"], selCriteria["maxObjEta"]))
    ltx.DrawLatex(0.16, 0.30, "      #bf{btagDeepFlavB > 0.7489 (for at least one jet)}")
    ltx.DrawLatex(0.16, 0.25, "#bullet Muons: #bf{has tightId, |#eta|<%s and miniPFRelIso_all<%s (for at least 1)}"
                  % (selCriteria["maxObjEta"], selCriteria["maxPfRelIso04"]))
    ltx.SetTextSize(0.015)
    pdfCreator(argms, 0, triggerCanvas)

    # - Create text for legend
    if argms.inputLFN == "ttjets":
        legString = "#splitline{CMS}{t#bar{t} #rightarrow l #nu_{l} #plus jets}"
    elif argms.inputLFN == "tttt":
        legString = "#splitline{CMS}{t#bar{t}t#bar{t} #rightarrow l #nu_{l} #plus jets}"
    elif argms.inputLFN == "tttt_weights":
        legString = "#splitline{CMS}{t#bar{t}t#bar{t} #rightarrow l #nu_{l} #plus jets}"
    else:
        legString = "#splitline{CMS}{W #rightarrow jets}"

    ROOT.gStyle.SetOptTitle(0)

    # - HT plots for mu Triggers ---------------------------------
    cv1 = triggerCanvas.cd(1)
    h["jetHt_notrigger"].Draw('E1')
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            h["jetHt_" + tg].Draw('E1 same')
    cv1.BuildLegend(0.57, 0.54, 0.97, 0.74)
    ROOT.gStyle.SetLegendTextSize(0.02)
    tX1 = 0.6*(h["jetHt_notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95*(h["jetHt_notrigger"].GetMaximum())
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    cv2 = triggerCanvas.cd(1)
    i = 0
    j = 2
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            if ROOT.TEfficiency.CheckConsistency(h["jetHt_" + tg], h["jetHt_notrigger"]):
                h_TriggerRatio[tg] = ROOT.TEfficiency(h["jetHt_" + tg], h["jetHt_notrigger"])
                xTitle = h["jetHt_notrigger"].GetXaxis().GetTitle()
                xBinWidth = h["jetHt_notrigger"].GetXaxis().GetBinWidth(1)
                h_TriggerRatio[tg].SetTitle(";{0};Trigger Efficiency per {1}GeV/c".format(xTitle, round(xBinWidth)))
                h_TriggerRatio[tg].SetName(tg)
                h_TriggerRatio[tg].SetTitle(tg)
                h_TriggerRatio[tg].SetLineColor(j)
                j += 1
                if i == 0:
                    h_TriggerRatio[tg].GetListOfFunctions().AddFirst(f["jetHt_" + tg])
                    h_TriggerRatio[tg].Fit(f["jetHt_" + tg], 'LVR')  # L= log likelihood, V=verbose, R=range in function
                    h_TriggerRatio[tg].Draw('AP')
                    cv2.Update()
                    graph1 = h_TriggerRatio[tg].GetPaintedGraph()
                    graph1.SetMinimum(0)
                    graph1.SetMaximum(1.2)
                    cv2.Update()
                    tX1 = 0.05*(h["jetHt_notrigger"].GetXaxis().GetXmax())
                    tY1 = 1.1
                elif i > 0:
                    h_TriggerRatio[tg].Fit(f["jetHt_" + tg], 'LVR')
                    h_TriggerRatio[tg].Draw('same')
                i += 1
    cv2.BuildLegend(0.5, 0.1, 0.9, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    # - Jet Multiplicity plots ---------------------------------
    cv3 = triggerCanvas.cd(1)
    h["jetMult_notrigger"].GetXaxis().SetTitle("Number of Jets")
    h["jetMult_notrigger"].Draw('E1')
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            h["jetMult_" + tg].Draw('E1 same')
    cv3.BuildLegend(0.57, 0.54, 0.97, 0.74)
    ROOT.gStyle.SetLegendTextSize(0.02)
    tX1 = 0.6 * (h["jetMult_notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95 * (h["jetMult_notrigger"].GetMaximum())
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    cv4 = triggerCanvas.cd(1)
    i = 0
    j = 2
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            if ROOT.TEfficiency.CheckConsistency(h["jetMult_" + tg], h["jetMult_notrigger"]):
                h_TriggerRatio[tg] = ROOT.TEfficiency(h["jetMult_" + tg], h["jetMult_notrigger"])
                # xTitle = h["jetMult_notrigger"].GetXaxis().GetTitle()
                xBinWidth = h["jetMult_notrigger"].GetXaxis().GetBinWidth(1)
                h_TriggerRatio[tg].SetTitle(";Number of Jets ;Trigger Efficiency per {0} GeV/c".format(xBinWidth))
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
                    tX1 = 0.05 * ((h["jetMult_notrigger"].GetXaxis().GetXmax())-5)+5
                    tY1 = 1.1
                if i > 0:
                    h_TriggerRatio[tg].Draw('same')
            i += 1
    cv4.BuildLegend(0.5, 0.1, 0.9, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    # - B tagged Jet Multiplicity plots ---------------------------
    cv5 = triggerCanvas.cd(1)
    # h["jetBMult_notrigger"].SetTitle("")
    h["jetBMult_notrigger"].GetXaxis().SetRange(1, 10)
    h["jetBMult_notrigger"].Draw('E1')
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            h["jetBMult_" + tg].Draw('E1 same')
    cv5.BuildLegend(0.57, 0.54, 0.97, 0.74)
    ROOT.gStyle.SetLegendTextSize(0.02)
    tX1 = 0.6 * (h["jetBMult_notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95 * (h["jetBMult_notrigger"].GetMaximum())
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    cv6 = triggerCanvas.cd(1)
    i = 0
    j = 2
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            if ROOT.TEfficiency.CheckConsistency(h["jetBMult_" + tg], h["jetBMult_notrigger"]):
                h_TriggerRatio[tg] = ROOT.TEfficiency(h["jetBMult_" + tg], h["jetBMult_notrigger"])
                xTitle = h["jetBMult_notrigger"].GetXaxis().GetTitle()
                xBinWidth = h["jetBMult_notrigger"].GetXaxis().GetBinWidth(1)
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
                    tX1 = 0.05 * (h["jetBMult_notrigger"].GetXaxis().GetXmax())
                    tY1 = 1.1
                if i > 0:
                    h_TriggerRatio[tg].Draw('same')
            i += 1
    cv6.BuildLegend(0.5, 0.1, 0.9, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    # - Muon test Plots-------------------------------
    triggerCanvas.cd(1)
    h_muonGenPartFlav.Draw()
    pdfCreator(argms, 1, triggerCanvas)

    triggerCanvas.cd(1)
    h_muonGenPartIdx.Draw()
    pdfCreator(argms, 1, triggerCanvas)

    triggerCanvas.cd(1)
    h_muonPfRelIso04_all.Draw()
    pdfCreator(argms, 1, triggerCanvas)

    # - Muon pT plots ---------------------------------
    cv7 = triggerCanvas.cd(1)
    # h["muonPt_notrigger"].SetTitle("")
    h["muonPt_notrigger"].SetMinimum(0.)
    # h["muonPt_notrigger"].SetMaximum(3500)
    h["muonPt_notrigger"].Draw('E1')
    tX1 = 0.60*(h["muonPt_notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95*(h["muonPt_notrigger"].GetMaximum())
    for key in trigList:
        if not key.find("El") == -1: continue
        # if not (key == "Electron" or key == "ElPJets" or key == "ElLone"):
        for tg in trigList[key]:
            h["muonPt_" + tg].Draw('E1 same')
    cv7.BuildLegend(0.57, 0.54, 0.97, 0.74)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas)

    cv71 = triggerCanvas.cd(1)
    # h["muonPt_notrigger"].SetTitle("")
    h["muonPt_notrigger"].SetMinimum(0.)
    # h["muonPt_notrigger"].SetMaximum(3500)
    h["muonPt_notrigger"].Draw('E1')
    tX1 = 0.6*(h["muonPt_notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95*(h["muonPt_notrigger"].GetMaximum())
    h["muonPt_prompt"].SetTitle("prompt muons")
    h["muonPt_prompt"].Draw('E1 same')
    h["muonPt_non-prompt"].Draw('E1 same')
    cv71.BuildLegend(0.57, 0.54, 0.97, 0.74)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas)

    cv8 = triggerCanvas.cd(1)
    i = 0
    j = 2
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            if ROOT.TEfficiency.CheckConsistency(h["muonPt_" + tg], h["muonPt_notrigger"]):
                h_TriggerRatio[tg] = ROOT.TEfficiency(h["muonPt_" + tg], h["muonPt_notrigger"])
                xTitle = h["muonPt_notrigger"].GetXaxis().GetTitle()
                xBinWidth = h["muonPt_notrigger"].GetXaxis().GetBinWidth(1)
                h_TriggerRatio[tg].SetTitle(";{0};Trigger Efficiency per {1} GeV/c".format(xTitle, xBinWidth))
                h_TriggerRatio[tg].SetName(tg)
                h_TriggerRatio[tg].SetTitle(tg)
                h_TriggerRatio[tg].SetLineColor(j)
                j += 1
                if i == 0:
                    h_TriggerRatio[tg].Draw('AP')
                    cv8.Update()
                    graph1 = h_TriggerRatio[tg].GetPaintedGraph()
                    graph1.SetMinimum(0)
                    graph1.SetMaximum(1.2)
                    cv8.Update()
                    tX1 = 0.05 * (h["muonPt_notrigger"].GetXaxis().GetXmax())
                    tY1 = 1.1
                if i > 0:
                    h_TriggerRatio[tg].Draw('same')
            i += 1
    cv8.BuildLegend(0.5, 0.1, 0.9, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    # - MET pT plots ---------------------------------
    cv9 = triggerCanvas.cd(1)
    h["metPt_notrigger"].GetXaxis().SetTitle("E^{Miss}_{T}")
    h["metPt_notrigger"].SetMinimum(0.)
    # h["metPt_notrigger"].SetMaximum(1800)
    h["metPt_notrigger"].Draw('E1')
    tX1 = 0.6 * (h["metPt_notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95 * (h["metPt_notrigger"].GetMaximum())
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            h["metPt_" + tg].Draw('E1 same')
    cv9.BuildLegend(0.57, 0.54, 0.97, 0.74)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas)

    cv10 = triggerCanvas.cd(1)
    i = 0
    j = 2
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            if ROOT.TEfficiency.CheckConsistency(h["metPt_" + tg], h["metPt_notrigger"]):
                h_TriggerRatio[tg] = ROOT.TEfficiency(h["metPt_" + tg], h["metPt_notrigger"])
                # xTitle = h["metPt_notrigger"].GetXaxis().GetTitle()
                xBinWidth = h["metPt_notrigger"].GetXaxis().GetBinWidth(1)
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
                    tX1 = 0.05 * (h["metPt_notrigger"].GetXaxis().GetXmax())
                    tY1 = 1.1
                if i > 0:
                    h_TriggerRatio[tg].Draw('same')
            i += 1
    cv10.BuildLegend(0.5, 0.1, 0.9, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    # - GenMET pT plots ---------------------------------
    cv11 = triggerCanvas.cd(1)
    h["genMetPt_notrigger"].GetXaxis().SetTitle("Gen E^{Miss}_{T}")
    h["genMetPt_notrigger"].SetMinimum(0.)
    # h["genMetPt_notrigger"].SetMaximum(2000)
    h["genMetPt_notrigger"].Draw('E1')
    tX1 = 0.6 * (h["genMetPt_notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95 * (h["genMetPt_notrigger"].GetMaximum())
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            h["genMetPt_" + tg].Draw('E1 same')
    cv11.BuildLegend(0.57, 0.54, 0.97, 0.74)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas)

    cv12 = triggerCanvas.cd(1)
    i = 0
    j = 2
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            if ROOT.TEfficiency.CheckConsistency(h["genMetPt_" + tg], h["genMetPt_notrigger"]):
                h_TriggerRatio[tg] = ROOT.TEfficiency(h["genMetPt_" + tg], h["genMetPt_notrigger"])
                # xTitle = h["genMetPt_notrigger"].GetXaxis().GetTitle()
                xBinWidth = h["genMetPt_notrigger"].GetXaxis().GetBinWidth(1)
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
                    tX1 = 0.05 * (h["genMetPt_notrigger"].GetXaxis().GetXmax())
                    tY1 = 1.1
                if i > 0:
                    h_TriggerRatio[tg].Draw('same')
            i += 1
    cv12.BuildLegend(0.5, 0.1, 0.9, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    # - Eta plots ------------------------------------------
    cv13 = triggerCanvas.cd(1)
    # h["jetEta_notrigger"].GetYaxis().SetTitleOffset(1.1)
    h["jetEta_notrigger"].Draw('E1')
    tX1 = 0.6*6
    tY1 = 0.95*(h["jetEta_notrigger"].GetMaximum())
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            h["jetEta_" + tg].Draw('E1 same')
    cv13.BuildLegend(0.4, 0.25, 0.4, 0.25)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    # pdfCreator(argms, 1, triggerCanvas)

    cv14 = triggerCanvas.cd(1)
    # h["muonEta_notrigger"].GetYaxis().SetTitleOffset(1.2)
    h["muonEta_notrigger"].Draw('E1')
    tX1 = 0.6*6
    tY1 = 0.95*(h["muonEta_notrigger"].GetMaximum())
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            h["muonEta_" + tg].Draw('E1 same')
    cv14.BuildLegend(0.4, 0.25, 0.4, 0.25)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas)

    cv15 = triggerCanvas.cd(1)
    i = 0
    j = 2
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            if ROOT.TEfficiency.CheckConsistency(h["muonEta_" + tg], h["muonEta_notrigger"]):
                h_TriggerRatio[tg] = ROOT.TEfficiency(h["muonEta_" + tg], h["muonEta_notrigger"])
                xTitle = h["muonEta_notrigger"].GetXaxis().GetTitle()
                xBinWidth = h["muonEta_notrigger"].GetXaxis().GetBinWidth(1)
                h_TriggerRatio[tg].SetTitle(";{0};Trigger Efficiency per {1} GeV/c".format(xTitle, xBinWidth))
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
                    tX1 = 0.05 * (h["muonEta_notrigger"].GetXaxis().GetXmax())
                    tY1 = 1.1
                if i > 0:
                    h_TriggerRatio[tg].Draw('same')
            i += 1
    cv15.BuildLegend(0.5, 0.1, 0.9, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    # - Phi plots ------------------------------------------
    cv16 = triggerCanvas.cd(1)
    # h["jetPhi_notrigger"].GetYaxis().SetTitleOffset(1.3)
    h["jetPhi_notrigger"].Draw('E1')
    tX1 = 0.6*6
    tY1 = 0.95*(h["jetPhi_notrigger"].GetMaximum())
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            h["jetPhi_" + tg].Draw('E1 same')
    cv16.BuildLegend(0.4, 0.2, 0.4, 0.2)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    # pdfCreator(argms, 1, triggerCanvas)

    cv17 = triggerCanvas.cd(1)
    # h["muonPhi_notrigger"].GetYaxis().SetTitleOffset(1.4)
    h["muonPhi_notrigger"].Draw('E1')
    tX1 = 0.6*6
    tY1 = 0.97*(h["muonPhi_notrigger"].GetMaximum())
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            h["muonPhi_" + tg].Draw('E1 same')
    cv17.BuildLegend(0.4, 0.2, 0.4, 0.2)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    # pdfCreator(argms, 1, triggerCanvas)

    # - Eta-Phi Map plots ------------------------------------------
    triggerCanvas.cd(1)
    h["jetMap_notrigger"].Draw('COLZ')  # CONT4Z
    # pdfCreator(argms, 1, triggerCanvas)
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            h["jetMap_" + tg].Draw('COLZ')
            # pdfCreator(argms, 1, triggerCanvas)

    h["muonMap_notrigger"].Draw('COLZ')
    # pdfCreator(argms, 1, triggerCanvas)
    for key in trigList:
        if not key.find("El") == -1: continue
        for tg in trigList[key]:
            h["muonMap_" + tg].Draw('COLZ')  # E
            # pdfCreator(argms, 1, triggerCanvas)

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
    pdfCreator(argms, 2, triggerCanvas)

    histFile.Close()


main(process_arguments())
