import os
import errno
import ROOT
from ROOT import TLatex
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


def main(argms):
    """ This code merges histograms, only for specific root file """

    if argms.inputLFN == "ttjets":
        inputFile = "OutFiles/Histograms/TT6jets.root"
    elif argms.inputLFN == "tttt_weights":
        inputFile = "OutFiles/Histograms/TTTTweights.root"
    elif argms.inputLFN == "wjets":
        inputFile = "OutFiles/Histograms/Wjets.root"
    elif argms.inputLFN == "tttt":
        inputFile = "OutFiles/Histograms/TTTT_6jets.root"
    else:
        return 0
    
    # - Initialise variables
    trigList = {"combos": ['IsoMu24_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2'],
                "stndlone": ['Mu15_IsoVVVL_PFHT450_CaloBTagCSV_4p5'],
                "t1": ['IsoMu24'],
                "t2": ['PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2']}

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
    h_elPt = {}
    h_elEta = {}
    h_elPhi = {}
    h_elMap = {}
    h_metPt = {}
    h_metPhi = {}
    h_genMetPt = {}
    h_genMetPhi = {}
    h_jetHtTriggerRatio = {}
    h_jetMultTriggerRatio = {}
    h_jetBMultTriggerRatio = {}
    h_muonPtTriggerRatio = {}
    h_elPtTriggerRatio = {}
    h_metPtTriggerRatio = {}
    h_genMetPtTriggerRatio = {}

    # - Create canvases
    triggerCanvas = ROOT.TCanvas('triggerCanvas', 'Triggers', 1100, 600)
    # triggerCanvas.Divide(2,1)

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

    h_muonPt["notrigger"] = ROOT.gDirectory.Get("h_muonPt_notrigger")
    h_muonPt["notrigger"].SetLineColor(1)
    if not (h_muonPt["notrigger"]):
        print("No trigger muon Pt histogram is empty")
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

    h_elPt["notrigger"] = ROOT.gDirectory.Get("h_elPt_notrigger")
    h_elPt["notrigger"].SetLineColor(1)
    if not (h_elPt["notrigger"]):
        print("No trigger el Pt histogram is empty")
    h_elEta["notrigger"] = ROOT.gDirectory.Get("h_elEta_notrigger")
    h_elEta["notrigger"].SetLineColor(1)
    if not (h_elEta["notrigger"]):
        print("No trigger el eta histogram is empty")
    h_elPhi["notrigger"] = ROOT.gDirectory.Get("h_elPhi_notrigger")
    h_elPhi["notrigger"].SetLineColor(1)
    if not (h_elPhi["notrigger"]):
        print("No trigger el Phi histogram is empty")
    h_elMap["notrigger"] = ROOT.gDirectory.Get("h_elMap_notrigger")
    h_elMap["notrigger"].SetLineColor(1)
    if not (h_elMap["notrigger"]):
        print("No trigger el map histogram is empty")

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
    for key in trigList:
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

            h_elPt[tg] = ROOT.gDirectory.Get("h_elPt_" + tg)
            h_elEta[tg] = ROOT.gDirectory.Get("h_elEta_" + tg)
            h_elPhi[tg] = ROOT.gDirectory.Get("h_elPhi_" + tg)
            h_elMap[tg] = ROOT.gDirectory.Get("h_elMap_" + tg)

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
            h_elPt[tg].SetLineColor(i)
            h_elEta[tg].SetLineColor(i)
            h_elPhi[tg].SetLineColor(i)
            h_metPt[tg].SetLineColor(i)
            h_metPhi[tg].SetLineColor(i)
            h_genMetPt[tg].SetLineColor(i)
            h_genMetPhi[tg].SetLineColor(i)

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
    ltx.DrawLatex(0.16, 0.65, "#bullet Jets: #bf{number > 5 , jetId > 2 and |#eta| < 2.4 }")
    ltx.DrawLatex(0.16, 0.60, "#bullet Muons: #bf{number >0 and has softId}")
    ltx.DrawLatex(0.10, 0.50, "Event Limit: #bf{None (see last page)}")
    ltx.DrawLatex(0.10, 0.40, "Off-line (post-)selection Requisites for:")
    ltx.DrawLatex(0.16, 0.35, "#bullet Jets: #bf{jetId > 2 , p_{T} > 30 and |#eta|<2.4 (for at least 6)}")
    ltx.DrawLatex(0.16, 0.30, "      #bf{btagDeepFlavB > 0.7489 (for at least one jet)}")
    ltx.DrawLatex(0.16, 0.25, "#bullet Muons: #bf{has tightId, |#eta|<2.4 and miniPFRelIso_all<0.15 (for at least 1)}")
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

    # - HT plots ---------------------------------
    cv1 = triggerCanvas.cd(1)
    # h_jetHt["notrigger"].GetYaxis().SetTitleOffset(1.5)
    h_jetHt["notrigger"].Draw('E1')
    for key in trigList:
        for tg in trigList[key]:
            h_jetHt[tg].Draw('E1 same')
    cv1.BuildLegend(0.4, 0.3, 0.4, 0.3)
    # leg1.SetNColumns(2)
    ROOT.gStyle.SetLegendTextSize(0.02)
    tX1 = 0.04*(h_jetHt["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95*(h_jetHt["notrigger"].GetMaximum())
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    cv2 = triggerCanvas.cd(1)
    i = 0
    for tg in trigList["combos"]:
        h_jetHtTriggerRatio[tg] = (h_jetHt[tg]).Clone("h_jetHtRatio" + tg)
        h_jetHtTriggerRatio[tg].Divide(h_jetHt["notrigger"])
        if i == 0:
            h_jetHtTriggerRatio[tg].Draw('E1')
            tX1 = 0.04*(h_jetHtTriggerRatio[tg].GetXaxis().GetXmax())
            tY1 = 0.95*(h_jetHtTriggerRatio[tg].GetMaximum())
        if i == 1:
            h_jetHtTriggerRatio[tg].Draw('E1 same')
        i += 1
    for tg in trigList["stndlone"]:
        h_jetHtTriggerRatio[tg] = (h_jetHt[tg]).Clone("h_jetHtRatio" + tg)
        h_jetHtTriggerRatio[tg].Divide(h_jetHt["notrigger"])
        if i == 0:
            h_jetHtTriggerRatio[tg].Draw('E1')
            tX1 = 0.04*(h_jetHtTriggerRatio[tg].GetXaxis().GetXmax())
            tY1 = 0.95*(h_jetHtTriggerRatio[tg].GetMaximum())
        if i == 1:
            h_jetHtTriggerRatio[tg].Draw('E1 same')
        i += 1

    cv2.BuildLegend(0.4, 0.3, 0.4, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    # - Jet Multiplicity plots ---------------------------------
    cv17 = triggerCanvas.cd(1)
    # h_jetMult["notrigger"].GetYaxis().SetTitleOffset(1.5)
    h_jetMult["notrigger"].Draw('E1')
    for key in trigList:
        for tg in trigList[key]:
            h_jetMult[tg].Draw('E1 same')
    cv17.BuildLegend(0.4, 0.3, 0.4, 0.3)
    # leg1.SetNColumns(2)
    ROOT.gStyle.SetLegendTextSize(0.02)
    tX1 = 0.04 * (h_jetMult["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95 * (h_jetMult["notrigger"].GetMaximum())
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    cv18 = triggerCanvas.cd(1)
    i = 0
    for tg in trigList["combos"]:
        h_jetMultTriggerRatio[tg] = (h_jetMult[tg]).Clone("h_jetMultRatio" + tg)
        h_jetMultTriggerRatio[tg].Divide(h_jetMult["notrigger"])
        if i == 0:
            h_jetMultTriggerRatio[tg].Draw('E1')
            tX1 = 0.04 * (h_jetMultTriggerRatio[tg].GetXaxis().GetXmax())
            tY1 = 0.95 * (h_jetMultTriggerRatio[tg].GetMaximum())
        if i == 1:
            h_jetMultTriggerRatio[tg].Draw('E1 same')
        i += 1
    for tg in trigList["stndlone"]:
        h_jetMultTriggerRatio[tg] = (h_jetMult[tg]).Clone("h_jetMultRatio" + tg)
        h_jetMultTriggerRatio[tg].Divide(h_jetMult["notrigger"])
        if i == 0:
            h_jetMultTriggerRatio[tg].Draw('E1')
            tX1 = 0.04 * (h_jetMultTriggerRatio[tg].GetXaxis().GetXmax())
            tY1 = 0.95 * (h_jetMultTriggerRatio[tg].GetMaximum())
        if i == 1:
            h_jetMultTriggerRatio[tg].Draw('E1 same')
        i += 1

    cv18.BuildLegend(0.4, 0.3, 0.4, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    # - B tagged Jet Multiplicity plots ---------------------------
    cv19 = triggerCanvas.cd(1)
    # h_jetBMult["notrigger"].GetYaxis().SetTitleOffset(1.5)
    h_jetBMult["notrigger"].Draw('E1')
    for key in trigList:
        for tg in trigList[key]:
            h_jetBMult[tg].Draw('E1 same')
    cv19.BuildLegend(0.4, 0.3, 0.4, 0.3)
    # leg1.SetNColumns(2)
    ROOT.gStyle.SetLegendTextSize(0.02)
    tX1 = 0.04 * (h_jetBMult["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95 * (h_jetBMult["notrigger"].GetMaximum())
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    cv20 = triggerCanvas.cd(1)
    i = 0
    for tg in trigList["combos"]:
        h_jetBMultTriggerRatio[tg] = (h_jetBMult[tg]).Clone("h_jetBMultRatio" + tg)
        h_jetBMultTriggerRatio[tg].Divide(h_jetBMult["notrigger"])
        if i == 0:
            h_jetBMultTriggerRatio[tg].Draw('E1')
            tX1 = 0.04 * (h_jetBMultTriggerRatio[tg].GetXaxis().GetXmax())
            tY1 = 0.95 * (h_jetBMultTriggerRatio[tg].GetMaximum())
        if i == 1:
            h_jetBMultTriggerRatio[tg].Draw('E1 same')
        i += 1
    for tg in trigList["stndlone"]:
        h_jetBMultTriggerRatio[tg] = (h_jetBMult[tg]).Clone("h_jetBMultRatio" + tg)
        h_jetBMultTriggerRatio[tg].Divide(h_jetBMult["notrigger"])
        if i == 0:
            h_jetBMultTriggerRatio[tg].Draw('E1')
            tX1 = 0.04 * (h_jetBMultTriggerRatio[tg].GetXaxis().GetXmax())
            tY1 = 0.95 * (h_jetBMultTriggerRatio[tg].GetMaximum())
        if i == 1:
            h_jetBMultTriggerRatio[tg].Draw('E1 same')
        i += 1

    cv20.BuildLegend(0.4, 0.3, 0.4, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    # - Muon pT plots ---------------------------------
    cv3 = triggerCanvas.cd(1)
    # h_muonPt["notrigger"].GetYaxis().SetTitleOffset(1.5)
    h_muonPt["notrigger"].Draw('E1')
    tX1 = 0.04*(h_muonPt["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95*(h_muonPt["notrigger"].GetMaximum())
    for key in trigList:
        for tg in trigList[key]:
            h_muonPt[tg].Draw('E1 same')
    cv3.BuildLegend(0.4, 0.3, 0.4, 0.3)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas)

    cv4 = triggerCanvas.cd(1)
    i = 0
    for tg in trigList["combos"]:
        h_muonPtTriggerRatio[tg] = (h_muonPt[tg]).Clone("h_muonPtRatio" + tg)
        h_muonPtTriggerRatio[tg].Divide(h_muonPt["notrigger"])
        if i == 0:
            h_muonPtTriggerRatio[tg].Draw('E1')
            tX1 = 0.04*(h_muonPtTriggerRatio[tg].GetXaxis().GetXmax())
            tY1 = 0.95*(h_muonPtTriggerRatio[tg].GetMaximum())
        if i == 1:
            h_muonPtTriggerRatio[tg].Draw('E1 same')
        i += 1
    for tg in trigList["stndlone"]:
        h_muonPtTriggerRatio[tg] = (h_muonPt[tg]).Clone("h_muonPtRatio" + tg)
        h_muonPtTriggerRatio[tg].Divide(h_muonPt["notrigger"])
        if i == 0:
            h_muonPtTriggerRatio[tg].Draw('E1')
            tX1 = 0.04*(h_muonPtTriggerRatio[tg].GetXaxis().GetXmax())
            tY1 = 0.95*(h_muonPtTriggerRatio[tg].GetMaximum())
        if i == 1:
            h_muonPtTriggerRatio[tg].Draw('E1 same')
        i += 1
    cv4.BuildLegend(0.4, 0.3, 0.4, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    # - Electron pT plots ---------------------------------
    cv5 = triggerCanvas.cd(1)
    # h_elPt["notrigger"].GetYaxis().SetTitleOffset(1.5)
    h_elPt["notrigger"].Draw('E1')
    tX1 = 0.04 * (h_elPt["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95 * (h_elPt["notrigger"].GetMaximum())
    for key in trigList:
        for tg in trigList[key]:
            h_elPt[tg].Draw('E1 same')
    cv5.BuildLegend(0.4, 0.3, 0.4, 0.3)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas)

    cv6 = triggerCanvas.cd(1)
    i = 0
    for tg in trigList["combos"]:
        h_elPtTriggerRatio[tg] = (h_elPt[tg]).Clone("h_elPtRatio" + tg)
        h_elPtTriggerRatio[tg].Divide(h_elPt["notrigger"])
        if i == 0:
            h_elPtTriggerRatio[tg].Draw('E1')
            tX1 = 0.04 * (h_elPtTriggerRatio[tg].GetXaxis().GetXmax())
            tY1 = 0.95 * (h_elPtTriggerRatio[tg].GetMaximum())
        if i == 1:
            h_elPtTriggerRatio[tg].Draw('E1 same')
        i += 1
    for tg in trigList["stndlone"]:
        h_elPtTriggerRatio[tg] = (h_elPt[tg]).Clone("h_elPtRatio" + tg)
        h_elPtTriggerRatio[tg].Divide(h_elPt["notrigger"])
        if i == 0:
            h_elPtTriggerRatio[tg].Draw('E1')
            tX1 = 0.04 * (h_elPtTriggerRatio[tg].GetXaxis().GetXmax())
            tY1 = 0.95 * (h_elPtTriggerRatio[tg].GetMaximum())
        if i == 1:
            h_elPtTriggerRatio[tg].Draw('E1 same')
        i += 1
    cv6.BuildLegend(0.4, 0.3, 0.4, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    # - MET pT plots ---------------------------------
    cv13 = triggerCanvas.cd(1)
    # h_metPt["notrigger"].GetYaxis().SetTitleOffset(1.5)
    h_metPt["notrigger"].Draw('E1')
    tX1 = 0.04 * (h_metPt["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95 * (h_metPt["notrigger"].GetMaximum())
    for key in trigList:
        for tg in trigList[key]:
            h_metPt[tg].Draw('E1 same')
    cv13.BuildLegend(0.4, 0.3, 0.4, 0.3)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas)

    cv14 = triggerCanvas.cd(1)
    i = 0
    for tg in trigList["combos"]:
        h_metPtTriggerRatio[tg] = (h_metPt[tg]).Clone("h_metPtRatio" + tg)
        h_metPtTriggerRatio[tg].Divide(h_metPt["notrigger"])
        if i == 0:
            h_metPtTriggerRatio[tg].Draw('E1')
            tX1 = 0.04 * (h_metPtTriggerRatio[tg].GetXaxis().GetXmax())
            tY1 = 0.95 * (h_metPtTriggerRatio[tg].GetMaximum())
        if i == 1:
            h_metPtTriggerRatio[tg].Draw('E1 same')
        i += 1
    for tg in trigList["stndlone"]:
        h_metPtTriggerRatio[tg] = (h_metPt[tg]).Clone("h_metPtRatio" + tg)
        h_metPtTriggerRatio[tg].Divide(h_metPt["notrigger"])
        if i == 0:
            h_metPtTriggerRatio[tg].Draw('E1')
            tX1 = 0.04 * (h_metPtTriggerRatio[tg].GetXaxis().GetXmax())
            tY1 = 0.95 * (h_metPtTriggerRatio[tg].GetMaximum())
        if i == 1:
            h_elPtTriggerRatio[tg].Draw('E1 same')
        i += 1
    cv14.BuildLegend(0.4, 0.3, 0.4, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    # - GenMET pT plots ---------------------------------
    cv15 = triggerCanvas.cd(1)
    # h_genMetPt["notrigger"].GetYaxis().SetTitleOffset(1.5)
    h_genMetPt["notrigger"].Draw('E1')
    tX1 = 0.04 * (h_genMetPt["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95 * (h_genMetPt["notrigger"].GetMaximum())
    for key in trigList:
        for tg in trigList[key]:
            h_genMetPt[tg].Draw('E1 same')
    cv15.BuildLegend(0.4, 0.3, 0.4, 0.3)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas)

    cv16 = triggerCanvas.cd(1)
    i = 0
    for tg in trigList["combos"]:
        h_genMetPtTriggerRatio[tg] = (h_genMetPt[tg]).Clone("h_genMetPtRatio" + tg)
        h_genMetPtTriggerRatio[tg].Divide(h_genMetPt["notrigger"])
        if i == 0:
            h_genMetPtTriggerRatio[tg].Draw('E1')
            tX1 = 0.04 * (h_genMetPtTriggerRatio[tg].GetXaxis().GetXmax())
            tY1 = 0.95 * (h_genMetPtTriggerRatio[tg].GetMaximum())
        if i == 1:
            h_genMetPtTriggerRatio[tg].Draw('E1 same')
        i += 1
    for tg in trigList["stndlone"]:
        h_genMetPtTriggerRatio[tg] = (h_genMetPt[tg]).Clone("h_genMetPtRatio" + tg)
        h_genMetPtTriggerRatio[tg].Divide(h_genMetPt["notrigger"])
        if i == 0:
            h_genMetPtTriggerRatio[tg].Draw('E1')
            tX1 = 0.04 * (h_genMetPtTriggerRatio[tg].GetXaxis().GetXmax())
            tY1 = 0.95 * (h_genMetPtTriggerRatio[tg].GetMaximum())
        if i == 1:
            h_elPtTriggerRatio[tg].Draw('E1 same')
        i += 1
    cv16.BuildLegend(0.4, 0.3, 0.4, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    # - Eta plots ------------------------------------------
    cv7 = triggerCanvas.cd(1)
    # h_jetEta["notrigger"].GetYaxis().SetTitleOffset(1.1)
    h_jetEta["notrigger"].Draw('E1')
    tX1 = 0.94*(-6)
    tY1 = 0.95*(h_jetEta["notrigger"].GetMaximum())
    for key in trigList:
        for tg in trigList[key]:
            h_jetEta[tg].Draw('E1 same')
    cv7.BuildLegend(0.4, 0.3, 0.4, 0.3)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas)

    cv8 = triggerCanvas.cd(1)
    # h_muonEta["notrigger"].GetYaxis().SetTitleOffset(1.2)
    h_muonEta["notrigger"].Draw('E1')
    tX1 = 0.94*(-6)
    tY1 = 0.95*(h_muonEta["notrigger"].GetMaximum())
    for key in trigList:
        for tg in trigList[key]:
            h_muonEta[tg].Draw('E1 same')
    cv8.BuildLegend(0.4, 0.3, 0.4, 0.3)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas)

    cv9 = triggerCanvas.cd(1)
    # h_elEta["notrigger"].GetYaxis().SetTitleOffset(1.2)
    h_elEta["notrigger"].Draw('E1')
    tX1 = 0.94 * (-6)
    tY1 = 0.95 * (h_elEta["notrigger"].GetMaximum())
    for key in trigList:
        for tg in trigList[key]:
            h_elEta[tg].Draw('E1 same')
    cv9.BuildLegend(0.4, 0.3, 0.4, 0.3)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas)

    # - Phi plots ------------------------------------------
    cv10 = triggerCanvas.cd(1)
    # h_jetPhi["notrigger"].GetYaxis().SetTitleOffset(1.3)
    h_jetPhi["notrigger"].Draw('E1')
    tX1 = 0.94*(-6)
    tY1 = 0.95*(h_jetPhi["notrigger"].GetMaximum())
    for key in trigList:
        for tg in trigList[key]:
            h_jetPhi[tg].Draw('E1 same')
    cv10.BuildLegend(0.4, 0.3, 0.4, 0.3)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas)

    cv11 = triggerCanvas.cd(1)
    # h_muonPhi["notrigger"].GetYaxis().SetTitleOffset(1.4)
    h_muonPhi["notrigger"].Draw('E1')
    tX1 = 0.94*(-6)
    tY1 = 0.97*(h_muonPhi["notrigger"].GetMaximum())
    for key in trigList:
        for tg in trigList[key]:
            h_muonPhi[tg].Draw('E1 same')
    cv11.BuildLegend(0.4, 0.3, 0.4, 0.3)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas)

    cv12 = triggerCanvas.cd(1)
    # h_elPhi["notrigger"].GetYaxis().SetTitleOffset(1.4)
    h_elPhi["notrigger"].Draw('E1')
    tX1 = 0.94 * (-6)
    tY1 = 0.97 * (h_elPhi["notrigger"].GetMaximum())
    for key in trigList:
        for tg in trigList[key]:
            h_elPhi[tg].Draw('E1 same')
    cv12.BuildLegend(0.4, 0.3, 0.4, 0.3)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas)

    # - Eta-Phi Map plots ------------------------------------------
    triggerCanvas.cd(1)
    h_jetMap["notrigger"].Draw('COLZ')  # CONT4Z
    pdfCreator(argms, 1, triggerCanvas)
    for key in trigList:
        for tg in trigList[key]:
            h_jetMap[tg].Draw('COLZ')
            pdfCreator(argms, 1, triggerCanvas)

    h_muonMap["notrigger"].Draw('COLZ')
    pdfCreator(argms, 1, triggerCanvas)
    for key in trigList:
        for tg in trigList[key]:
            h_muonMap[tg].Draw('COLZ')  # E
            pdfCreator(argms, 1, triggerCanvas)

    h_elMap["notrigger"].Draw('COLZ')
    pdfCreator(argms, 1, triggerCanvas)
    for key in trigList:
        for tg in trigList[key]:
            h_elMap[tg].Draw('COLZ')  # E
            pdfCreator(argms, 1, triggerCanvas)

    # - Test Event numbers along steps ----------
    triggerCanvas.cd(1)
    h_eventsPrg.SetFillColor(ROOT.kAzure-9)
    h_eventsPrg.GetXaxis().SetLabelOffset(999)
    h_eventsPrg.GetXaxis().SetLabelSize(0)
    h_eventsPrg.Draw('E1')
    tY1 = 0.05*(h_eventsPrg.GetMaximum())
    ltx.SetTextAngle(88)
    ltx.DrawLatex(0.5, tY1, "Pre-selection")
    ltx.DrawLatex(1.5, tY1, "Post-selection")
    i = 0
    for key in trigList:
        for tg in trigList[key]:
            ltx.DrawLatex((i + 2.5), tY1, tg)
            i += 1

    # h.GetXAxis().SetBinLabel(binnumber,string)
    pdfCreator(argms, 2, triggerCanvas)

    histFile.Close()


main(process_arguments())
