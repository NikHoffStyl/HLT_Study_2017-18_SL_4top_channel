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
        inputFile = "OutFiles/Histograms/TT6jets2.root"
    elif argms.inputLFN == "tttt_weights":
        inputFile = "OutFiles/Histograms/TTTTweights.root"
    elif argms.inputLFN == "wjets":
        inputFile = "OutFiles/Histograms/Wjets.root"
    elif argms.inputLFN == "tttt":
        inputFile = "OutFiles/Histograms/TTTT_6jets2.root"
    else:
        return 0
    
    # - Initialise variables
    # trigList = {"combos": ['IsoMu24_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2'],
    #             "stndlone": ['Mu15_IsoVVVL_PFHT450_CaloBTagCSV_4p5'],
    #             "t1": ['IsoMu24'],
    #             "t2": ['PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2']}

    trigList = {"MuPJets": ['IsoMu24_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2'],
                "ElPJets": [],
                "stndlone": ['Mu15_IsoVVVL_PFHT450_CaloBTagCSV_4p5'],
                "Muon": ['IsoMu24'],
                "Electron": ['Ele32_WPTight_Gsf', 'Ele35_WPTight_Gsf', 'Ele38_WPTight_Gsf'],
                "Jet": ['PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2']}

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

    h_jetHt2 = {}
    h_jetMult2 = {}
    h_jetBMult2 = {}
    h_jetEta2 = {}
    h_jetPhi2 = {}
    h_jetMap2 = {}
    h_metPt2 = {}
    h_metPhi2 = {}
    h_genMetPt2 = {}
    h_genMetPhi2 = {}

    h_TriggerRatio = {}

    # - Create canvases
    triggerCanvas = ROOT.TCanvas('triggerCanvas', 'Triggers', 1100, 600)

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

    h_jetHt2["notrigger"] = ROOT.gDirectory.Get("h_jetHt2_notrigger")
    h_jetHt2["notrigger"].SetLineColor(1)
    if not (h_jetHt2["notrigger"]):
        print("No trigger jet Ht histogram is empty")
    h_jetMult2["notrigger"] = ROOT.gDirectory.Get("h_jetMult2_notrigger")
    h_jetMult2["notrigger"].SetLineColor(1)
    if not (h_jetMult2["notrigger"]):
        print("No trigger jet Mult histogram is empty")
    h_jetBMult2["notrigger"] = ROOT.gDirectory.Get("h_jetBMult2_notrigger")
    h_jetBMult2["notrigger"].SetLineColor(1)
    if not (h_jetBMult2["notrigger"]):
        print("No trigger jet BMult histogram is empty")
    h_jetEta2["notrigger"] = ROOT.gDirectory.Get("h_jetEta2_notrigger")
    h_jetEta2["notrigger"].SetLineColor(1)
    if not (h_jetEta2["notrigger"]):
        print("No trigger jet Eta histogram is empty")
    h_jetPhi2["notrigger"] = ROOT.gDirectory.Get("h_jetPhi2_notrigger")
    h_jetPhi2["notrigger"].SetLineColor(1)
    if not (h_jetPhi2["notrigger"]):
        print("No trigger jet Phi histogram is empty")
    h_jetMap2["notrigger"] = ROOT.gDirectory.Get("h_jetMap2_notrigger")
    h_jetMap2["notrigger"].SetLineColor(1)
    if not (h_jetMap2["notrigger"]):
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

    h_metPt2["notrigger"] = ROOT.gDirectory.Get("h_metPt2_notrigger")
    h_metPt2["notrigger"].SetLineColor(1)
    if not (h_metPt2["notrigger"]):
        print("No trigger met Pt histogram is empty")
    h_metPhi2["notrigger"] = ROOT.gDirectory.Get("h_metPhi2_notrigger")
    h_metPhi2["notrigger"].SetLineColor(1)
    if not (h_metPhi2["notrigger"]):
        print("No trigger met Phi histogram is empty")

    h_genMetPt2["notrigger"] = ROOT.gDirectory.Get("h_genMetPt2_notrigger")
    h_genMetPt2["notrigger"].SetLineColor(1)
    if not (h_genMetPt2["notrigger"]):
        print("No trigger genMet Pt histogram is empty")
    h_genMetPhi2["notrigger"] = ROOT.gDirectory.Get("h_genMetPhi2_notrigger")
    h_genMetPhi2["notrigger"].SetLineColor(1)
    if not (h_genMetPhi2["notrigger"]):
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

            h_jetHt2[tg] = ROOT.gDirectory.Get("h_jetHt2_" + tg)
            h_jetMult2[tg] = ROOT.gDirectory.Get("h_jetMult2_" + tg)
            h_jetBMult2[tg] = ROOT.gDirectory.Get("h_jetBMult2_" + tg)
            h_jetEta2[tg] = ROOT.gDirectory.Get("h_jetEta2_" + tg)
            h_jetPhi2[tg] = ROOT.gDirectory.Get("h_jetPhi2_" + tg)
            h_jetMap2[tg] = ROOT.gDirectory.Get("h_jetMap2_" + tg)

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

            h_metPt2[tg] = ROOT.gDirectory.Get("h_metPt2_" + tg)
            h_metPhi2[tg] = ROOT.gDirectory.Get("h_metPhi2_" + tg)
            h_genMetPt2[tg] = ROOT.gDirectory.Get("h_genMetPt2_" + tg)
            h_genMetPhi2[tg] = ROOT.gDirectory.Get("h_genMetPhi2_" + tg)

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

            h_jetHt2[tg].SetLineColor(i)
            h_jetMult2[tg].SetLineColor(i)
            h_jetBMult2[tg].SetLineColor(i)
            h_jetEta2[tg].SetLineColor(i)
            h_jetPhi2[tg].SetLineColor(i)
            h_metPt2[tg].SetLineColor(i)
            h_metPhi2[tg].SetLineColor(i)
            h_genMetPt2[tg].SetLineColor(i)
            h_genMetPhi2[tg].SetLineColor(i)
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
    ltx.DrawLatex(0.16, 0.65, "#bullet Jets: #bf{number > 5}")
    ltx.DrawLatex(0.16, 0.60, "#bullet Muons: #bf{number >0}")
    ltx.DrawLatex(0.16, 0.55, "#bullet Electrons: #bf{number >0}")
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

    ROOT.gStyle.SetOptTitle(0)

    # - HT plots for mu Triggers ---------------------------------
    cv1 = triggerCanvas.cd(1)
    h_jetHt["notrigger"].Draw('E1')
    for key in trigList:
        if not (key == "Electron" or key == "ElPJets"):
            for tg in trigList[key]:
                h_jetHt[tg].Draw('E1 same')
    cv1.BuildLegend(0.4, 0.25, 0.4, 0.25)
    ROOT.gStyle.SetLegendTextSize(0.02)
    tX1 = 0.05*(h_jetHt["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95*(h_jetHt["notrigger"].GetMaximum())
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    cv2 = triggerCanvas.cd(1)
    i = 0
    j = 2
    for key in trigList:
        if not (key == "Electron" or key == "ElPJets"):
            for tg in trigList[key]:
                if ROOT.TEfficiency.CheckConsistency(h_jetHt[tg], h_jetHt["notrigger"]):
                    h_TriggerRatio[tg] = ROOT.TEfficiency(h_jetHt[tg], h_jetHt["notrigger"])
                    xTitle = h_jetHt["notrigger"].GetXaxis().GetTitle()
                    xBinWidth = h_jetHt["notrigger"].GetXaxis().GetBinWidth(1)
                    h_TriggerRatio[tg].SetTitle(";{0};Trigger Efficiency per {1} GeV/c".format(xTitle, round(xBinWidth)))
                    h_TriggerRatio[tg].SetName(tg)
                    h_TriggerRatio[tg].SetTitle(tg)
                    h_TriggerRatio[tg].SetLineColor(j)
                    j += 1
                    if i == 0:
                        h_TriggerRatio[tg].Draw('AP')
                        cv2.Update()
                        graph1 = h_TriggerRatio[tg].GetPaintedGraph()
                        graph1.SetMinimum(0)
                        graph1.SetMaximum(1.2)
                        cv2.Update()
                        tX1 = 0.06*(h_jetHt["notrigger"].GetXaxis().GetXmax())
                        tY1 = 1.1
                    if i > 0:
                        h_TriggerRatio[tg].Draw('same')
                i += 1
    cv2.BuildLegend(0.4, 0.2, 0.4, 0.2)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    # - Jet Multiplicity plots ---------------------------------
    cv3 = triggerCanvas.cd(1)
    h_jetMult["notrigger"].Draw('E1')
    for key in trigList:
        if not (key == "Electron" or key == "ElPJets"):
            for tg in trigList[key]:
                h_jetMult[tg].Draw('E1 same')
    cv3.BuildLegend(0.4, 0.25, 0.4, 0.25)
    ROOT.gStyle.SetLegendTextSize(0.02)
    tX1 = 0.05 * (h_jetMult["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95 * (h_jetMult["notrigger"].GetMaximum())
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    cv4 = triggerCanvas.cd(1)
    i = 0
    j = 2
    for key in trigList:
        if not (key == "Electron" or key == "ElPJets"):
            for tg in trigList[key]:
                if ROOT.TEfficiency.CheckConsistency(h_jetMult[tg], h_jetMult["notrigger"]):
                    h_TriggerRatio[tg] = ROOT.TEfficiency(h_jetMult[tg], h_jetMult["notrigger"])
                    xTitle = h_jetMult["notrigger"].GetXaxis().GetTitle()
                    xBinWidth = h_jetMult["notrigger"].GetXaxis().GetBinWidth(1)
                    h_TriggerRatio[tg].SetTitle(";{0};Trigger Efficiency per {1} GeV/c".format(xTitle, xBinWidth))
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
                        tY1 = 1.15
                    if i > 0:
                        h_TriggerRatio[tg].Draw('same')
                i += 1
    cv4.BuildLegend(0.4, 0.2, 0.4, 0.2)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    # - B tagged Jet Multiplicity plots ---------------------------
    cv5 = triggerCanvas.cd(1)
    # h_jetBMult["notrigger"].SetTitle("")
    h_jetBMult["notrigger"].GetXaxis().SetRange(1, 10)
    h_jetBMult["notrigger"].Draw('E1')
    for key in trigList:
        if not (key == "Electron" or key == "ElPJets"):
            for tg in trigList[key]:
                h_jetBMult[tg].Draw('E1 same')
    cv5.BuildLegend(0.4, 0.25, 0.4, 0.25)
    ROOT.gStyle.SetLegendTextSize(0.02)
    tX1 = 0.05 * (h_jetBMult["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95 * (h_jetBMult["notrigger"].GetMaximum())
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    cv6 = triggerCanvas.cd(1)
    i = 0
    j = 2
    for key in trigList:
        if not (key == "Electron" or key == "ElPJets"):
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
                        tY1 = 1.15
                    if i > 0:
                        h_TriggerRatio[tg].Draw('same')
                i += 1
    cv6.BuildLegend(0.4, 0.2, 0.4, 0.2)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    # - Muon pT plots ---------------------------------
    cv7 = triggerCanvas.cd(1)
    # h_muonPt["notrigger"].SetTitle("")
    h_muonPt["notrigger"].SetMinimum(0.)
    h_muonPt["notrigger"].SetMaximum(3500)
    h_muonPt["notrigger"].Draw('E1')
    tX1 = 0.05*(h_muonPt["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95*(h_muonPt["notrigger"].GetMaximum())
    for key in trigList:
        if not (key == "Electron" or key == "ElPJets"):
            for tg in trigList[key]:
                h_muonPt[tg].Draw('E1 same')
    cv7.BuildLegend(0.4, 0.25, 0.4, 0.25)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas)

    cv8 = triggerCanvas.cd(1)
    i = 0
    j = 2
    for key in trigList:
        if not (key == "Electron" or key == "ElPJets"):
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
                        h_TriggerRatio[tg].Draw('AP')
                        cv8.Update()
                        graph1 = h_TriggerRatio[tg].GetPaintedGraph()
                        graph1.SetMinimum(0)
                        graph1.SetMaximum(1.2)
                        cv8.Update()
                        tX1 = 0.05 * (h_muonPt["notrigger"].GetXaxis().GetXmax())
                        tY1 = 1.15
                    if i > 0:
                        h_TriggerRatio[tg].Draw('same')
                i += 1
    cv8.BuildLegend(0.4, 0.2, 0.4, 0.2)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    # - MET pT plots ---------------------------------
    cv9 = triggerCanvas.cd(1)
    # h_metPt["notrigger"].SetTitle("")
    h_metPt["notrigger"].SetMinimum(0.)
    h_metPt["notrigger"].SetMaximum(1800)
    h_metPt["notrigger"].Draw('E1')
    tX1 = 0.05 * (h_metPt["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95 * (h_metPt["notrigger"].GetMaximum())
    for key in trigList:
        if not (key == "Electron" or key == "ElPJets"):
            for tg in trigList[key]:
                h_metPt[tg].Draw('E1 same')
    cv9.BuildLegend(0.4, 0.25, 0.4, 0.25)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas)

    cv10 = triggerCanvas.cd(1)
    i = 0
    j = 2
    for key in trigList:
        if not (key == "Electron" or key == "ElPJets"):
            for tg in trigList[key]:
                if ROOT.TEfficiency.CheckConsistency(h_metPt[tg], h_metPt["notrigger"]):
                    h_TriggerRatio[tg] = ROOT.TEfficiency(h_metPt[tg], h_metPt["notrigger"])
                    xTitle = h_metPt["notrigger"].GetXaxis().GetTitle()
                    xBinWidth = h_metPt["notrigger"].GetXaxis().GetBinWidth(1)
                    h_TriggerRatio[tg].SetTitle(";{0};Trigger Efficiency per {1} GeV/c".format(xTitle, xBinWidth))
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
                        tY1 = 1.15
                    if i > 0:
                        h_TriggerRatio[tg].Draw('same')
                i += 1
    cv10.BuildLegend(0.4, 0.2, 0.4, 0.2)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    # - GenMET pT plots ---------------------------------
    cv11 = triggerCanvas.cd(1)
    # h_genMetPt["notrigger"].SetTitle("")
    h_genMetPt["notrigger"].SetMinimum(0.)
    h_genMetPt["notrigger"].SetMaximum(2000)
    h_genMetPt["notrigger"].Draw('E1')
    tX1 = 0.05 * (h_genMetPt["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95 * (h_genMetPt["notrigger"].GetMaximum())
    for key in trigList:
        if not (key == "Electron" or key == "ElPJets"):
            for tg in trigList[key]:
                h_genMetPt[tg].Draw('E1 same')
    cv11.BuildLegend(0.4, 0.25, 0.4, 0.25)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas)

    cv12 = triggerCanvas.cd(1)
    i = 0
    j = 2
    for key in trigList:
        if not (key == "Electron" or key == "ElPJets"):
            for tg in trigList[key]:
                if ROOT.TEfficiency.CheckConsistency(h_genMetPt[tg], h_genMetPt["notrigger"]):
                    h_TriggerRatio[tg] = ROOT.TEfficiency(h_genMetPt[tg], h_genMetPt["notrigger"])
                    xTitle = h_genMetPt["notrigger"].GetXaxis().GetTitle()
                    xBinWidth = h_genMetPt["notrigger"].GetXaxis().GetBinWidth(1)
                    h_TriggerRatio[tg].SetTitle(";{0};Trigger Efficiency per {1} GeV/c".format(xTitle, xBinWidth))
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
                        tY1 = 1.15
                    if i > 0:
                        h_TriggerRatio[tg].Draw('same')
                i += 1
    cv12.BuildLegend(0.4, 0.2, 0.4, 0.2)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    # - Eta plots ------------------------------------------
    cv13 = triggerCanvas.cd(1)
    # h_jetEta["notrigger"].GetYaxis().SetTitleOffset(1.1)
    h_jetEta["notrigger"].Draw('E1')
    tX1 = 0.94*(-6)
    tY1 = 0.95*(h_jetEta["notrigger"].GetMaximum())
    for key in trigList:
        if not (key == "Electron" or key == "ElPJets"):
            for tg in trigList[key]:
                h_jetEta[tg].Draw('E1 same')
    cv13.BuildLegend(0.4, 0.25, 0.4, 0.25)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    # pdfCreator(argms, 1, triggerCanvas)

    cv14 = triggerCanvas.cd(1)
    # h_muonEta["notrigger"].GetYaxis().SetTitleOffset(1.2)
    h_muonEta["notrigger"].Draw('E1')
    tX1 = 0.94*(-6)
    tY1 = 0.95*(h_muonEta["notrigger"].GetMaximum())
    for key in trigList:
        if not (key == "Electron" or key == "ElPJets"):
            for tg in trigList[key]:
                h_muonEta[tg].Draw('E1 same')
    cv14.BuildLegend(0.4, 0.25, 0.4, 0.25)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    # pdfCreator(argms, 1, triggerCanvas)

    cv15 = triggerCanvas.cd(1)
    i = 0
    j = 2
    for key in trigList:
        if not (key == "Electron" or key == "ElPJets"):
            for tg in trigList[key]:
                if ROOT.TEfficiency.CheckConsistency(h_muonEta[tg], h_muonEta["notrigger"]):
                    h_TriggerRatio[tg] = ROOT.TEfficiency(h_muonEta[tg], h_muonEta["notrigger"])
                    xTitle = h_muonEta["notrigger"].GetXaxis().GetTitle()
                    xBinWidth = h_muonEta["notrigger"].GetXaxis().GetBinWidth(1)
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
                        tX1 = 0.05 * (h_muonEta["notrigger"].GetXaxis().GetXmax())
                        tY1 = 1.15
                    if i > 0:
                        h_TriggerRatio[tg].Draw('same')
                i += 1
    cv15.BuildLegend(0.4, 0.2, 0.4, 0.2)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    # - Phi plots ------------------------------------------
    cv16 = triggerCanvas.cd(1)
    # h_jetPhi["notrigger"].GetYaxis().SetTitleOffset(1.3)
    h_jetPhi["notrigger"].Draw('E1')
    tX1 = 0.94*(-6)
    tY1 = 0.95*(h_jetPhi["notrigger"].GetMaximum())
    for key in trigList:
        if not (key == "Electron" or key == "ElPJets"):
            for tg in trigList[key]:
                h_jetPhi[tg].Draw('E1 same')
    cv16.BuildLegend(0.4, 0.2, 0.4, 0.2)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    # pdfCreator(argms, 1, triggerCanvas)

    cv17 = triggerCanvas.cd(1)
    # h_muonPhi["notrigger"].GetYaxis().SetTitleOffset(1.4)
    h_muonPhi["notrigger"].Draw('E1')
    tX1 = 0.94*(-6)
    tY1 = 0.97*(h_muonPhi["notrigger"].GetMaximum())
    for key in trigList:
        if not (key == "Electron" or key == "ElPJets"):
            for tg in trigList[key]:
                h_muonPhi[tg].Draw('E1 same')
    cv17.BuildLegend(0.4, 0.2, 0.4, 0.2)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    # pdfCreator(argms, 1, triggerCanvas)

    # - Eta-Phi Map plots ------------------------------------------
    triggerCanvas.cd(1)
    h_jetMap["notrigger"].Draw('COLZ')  # CONT4Z
    # pdfCreator(argms, 1, triggerCanvas)
    for key in trigList:
        if not (key == "Electron" or key == "ElPJets"):
            for tg in trigList[key]:
                h_jetMap[tg].Draw('COLZ')
                # pdfCreator(argms, 1, triggerCanvas)

    h_muonMap["notrigger"].Draw('COLZ')
    # pdfCreator(argms, 1, triggerCanvas)
    for key in trigList:
        if not (key == "Electron" or key == "ElPJets"):
            for tg in trigList[key]:
                h_muonMap[tg].Draw('COLZ')  # E
                # pdfCreator(argms, 1, triggerCanvas)

    ######################################################################
    # - HT plots for electron Triggers ---------------------------------
    cv31 = triggerCanvas.cd(1)
    h_jetHt2["notrigger"].SetTitle("")
    h_jetHt2["notrigger"].Draw('E1')
    for key in trigList:
        if not (key == "Muon" or key == "MuPJets" or key == "stndlone"):
            for tg in trigList[key]:
                h_jetHt2[tg].Draw('E1 same')
    cv31.BuildLegend(0.4, 0.3, 0.4, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    tX1 = 0.05 * (h_jetHt2["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95 * (h_jetHt2["notrigger"].GetMaximum())
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    cv32 = triggerCanvas.cd(1)
    i = 0
    for key in trigList:
        if not (key == "Muon" or key == "MuPJets" or key == "stndlone"):
            for tg in trigList[key]:
                h_TriggerRatio[tg] = h_jetHt2[tg].Clone("h_jetHt2Ratio" + tg)
                h_TriggerRatio[tg].Sumw2()
                h_TriggerRatio[tg].SetStats(0)
                h_TriggerRatio[tg].Divide(h_jetHt2["notrigger"])
                xTitle = h_jetHt2["notrigger"].GetXaxis().GetTitle()
                xBinWidth = h_jetHt2["notrigger"].GetXaxis().GetBinWidth(1)
                h_TriggerRatio[tg].SetTitle(";{0};Trigger Efficiency per {1} GeV/c".format(xTitle, round(xBinWidth)))
                h_TriggerRatio[tg].SetName(tg)
                if i == 0:
                    h_TriggerRatio[tg].SetMinimum(0.)
                    h_TriggerRatio[tg].SetMaximum(1.8)
                    h_TriggerRatio[tg].Draw('E1')
                    tX1 = 0.04 * (h_jetHt2["notrigger"].GetXaxis().GetXmax())
                    tY1 = 0.95 * (h_TriggerRatio[tg].GetMaximum())
                if i > 0:
                    h_TriggerRatio[tg].Draw('E1 same')
                i += 1
    cv32.BuildLegend(0.4, 0.3, 0.4, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    triggerCanvas.Print("test.png")
    pdfCreator(argms, 1, triggerCanvas)

    # - Jet Multiplicity plots ---------------------------------
    cv33 = triggerCanvas.cd(1)
    h_jetMult2["notrigger"].SetTitle("")
    h_jetMult2["notrigger"].Draw('E1')
    for key in trigList:
        if not (key == "Muon" or key == "MuPJets" or key == "stndlone"):
            for tg in trigList[key]:
                h_jetMult2[tg].Draw('E1 same')
    cv33.BuildLegend(0.4, 0.3, 0.4, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    tX1 = 0.04 * (h_jetMult2["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95 * (h_jetMult2["notrigger"].GetMaximum())
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    cv34 = triggerCanvas.cd(1)
    i = 0
    for key in trigList:
        if not (key == "Muon" or key == "MuPJets" or key == "stndlone"):
            for tg in trigList[key]:
                h_TriggerRatio[tg] = h_jetMult2[tg].Clone("h_jetMult2Ratio" + tg)
                h_TriggerRatio[tg].Sumw2()
                h_TriggerRatio[tg].SetStats(0)
                h_TriggerRatio[tg].Divide(h_jetMult2["notrigger"])
                xTitle = h_jetMult2["notrigger"].GetXaxis().GetTitle()
                xBinWidth = h_jetMult2["notrigger"].GetXaxis().GetBinWidth(1)
                h_TriggerRatio[tg].SetTitle(";{0};Trigger Efficiency per {1} GeV/c".format(xTitle, round(xBinWidth)))
                h_TriggerRatio[tg].SetName(tg)
                if i == 0:
                    h_TriggerRatio[tg].SetMinimum(0.)
                    h_TriggerRatio[tg].SetMaximum(1.8)
                    h_TriggerRatio[tg].Draw('E1')
                    tX1 = 0.04 * (h_jetMult2["notrigger"].GetXaxis().GetXmax())
                    tY1 = 0.95 * (h_TriggerRatio[tg].GetMaximum())
                if i > 0:
                    h_TriggerRatio[tg].Draw('E1 same')
                i += 1
    cv34.BuildLegend(0.4, 0.3, 0.4, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    # - B tagged Jet Multiplicity plots ---------------------------
    cv35 = triggerCanvas.cd(1)
    h_jetBMult2["notrigger"].SetTitle("")
    h_jetBMult2["notrigger"].GetXaxis().SetRange(1, 10)
    h_jetBMult2["notrigger"].Draw('E1')
    for key in trigList:
        if not (key == "Muon" or key == "MuPJets" or key == "stndlone"):
            for tg in trigList[key]:
                h_jetBMult2[tg].Draw('E1 same')
    cv35.BuildLegend(0.4, 0.3, 0.4, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    tX1 = 0.04 * (h_jetBMult2["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95 * (h_jetBMult2["notrigger"].GetMaximum())
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    cv36 = triggerCanvas.cd(1)
    i = 0
    for key in trigList:
        if not (key == "Muon" or key == "MuPJets" or key == "stndlone"):
            for tg in trigList[key]:
                h_TriggerRatio[tg] = h_jetBMult2[tg].Clone("h_jetBMult2Ratio" + tg)
                h_TriggerRatio[tg].Sumw2()
                h_TriggerRatio[tg].SetStats(0)
                h_TriggerRatio[tg].Divide(h_jetBMult2["notrigger"])
                xTitle = h_jetBMult2["notrigger"].GetXaxis().GetTitle()
                xBinWidth = h_jetBMult2["notrigger"].GetXaxis().GetBinWidth(1)
                h_TriggerRatio[tg].SetTitle(";{0};Trigger Efficiency per {1} GeV/c".format(xTitle, round(xBinWidth)))
                h_TriggerRatio[tg].SetName(tg)
                if i == 0:
                    h_TriggerRatio[tg].SetMinimum(0.)
                    h_TriggerRatio[tg].SetMaximum(1.8)
                    h_TriggerRatio[tg].GetXaxis().SetRange(1, 10)
                    h_TriggerRatio[tg].Draw('E1')
                    tX1 = 0.04 * (h_jetBMult2["notrigger"].GetXaxis().GetXmax())
                    tY1 = 0.95 * (h_TriggerRatio[tg].GetMaximum())
                if i > 0:
                    h_TriggerRatio[tg].Draw('E1 same')
                i += 1
    cv36.BuildLegend(0.4, 0.3, 0.4, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    # - Electron pT plots ---------------------------------
    cv37 = triggerCanvas.cd(1)
    h_elPt["notrigger"].Draw('E1')
    tX1 = 0.04 * (h_elPt["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95 * (h_elPt["notrigger"].GetMaximum())
    for key in trigList:
        if not (key == "Muon" or key == "MuPJets" or key == "stndlone"):
            for tg in trigList[key]:
                h_elPt[tg].Draw('E1 same')
    cv37.BuildLegend(0.4, 0.3, 0.4, 0.3)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas)

    cv38 = triggerCanvas.cd(1)
    i = 0
    for key in trigList:
        if not (key == "Muon" or key == "MuPJets")or key == "stndlone":
            for tg in trigList[key]:
                h_TriggerRatio[tg] = h_elPt[tg].Clone("h_elPtRatio" + tg)
                h_TriggerRatio[tg].Sumw2()
                h_TriggerRatio[tg].SetStats(0)
                h_TriggerRatio[tg].Divide(h_elPt["notrigger"])
                xTitle = h_elPt["notrigger"].GetXaxis().GetTitle()
                xBinWidth = h_elPt["notrigger"].GetXaxis().GetBinWidth(1)
                h_TriggerRatio[tg].SetTitle(";{0};Trigger Efficiency per {1} GeV/c".format(xTitle, round(xBinWidth)))
                h_TriggerRatio[tg].SetName(tg)
                if i == 0:
                    h_TriggerRatio[tg].SetMinimum(0.)
                    h_TriggerRatio[tg].SetMaximum(1.8)
                    h_TriggerRatio[tg].Draw('E1')
                    tX1 = 0.04 * (h_elPt["notrigger"].GetXaxis().GetXmax())
                    tY1 = 0.95 * (h_elPt["notrigger"].GetMaximum())
                if i > 0:
                    h_TriggerRatio[tg].Draw('E1 same')
                i += 1
    cv38.BuildLegend(0.4, 0.3, 0.4, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    # - MET pT plots ---------------------------------
    cv39 = triggerCanvas.cd(1)
    h_metPt2["notrigger"].SetTitle("")
    h_metPt2["notrigger"].SetMinimum(0.)
    h_metPt2["notrigger"].SetMaximum(1800)
    h_metPt2["notrigger"].Draw('E1')
    tX1 = 0.04 * (h_metPt2["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95 * (h_metPt2["notrigger"].GetMaximum())
    for key in trigList:
        if not (key == "Muon" or key == "MuPJets" or key == "stndlone"):
            for tg in trigList[key]:
                h_metPt2[tg].Draw('E1 same')
    cv39.BuildLegend(0.4, 0.3, 0.4, 0.3)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas)

    cv40 = triggerCanvas.cd(1)
    i = 0
    for key in trigList:
        if not (key == "Muon" or key == "MuPJets" or key == "stndlone"):
            for tg in trigList[key]:
                h_TriggerRatio[tg] = h_metPt2[tg].Clone("h_metPt2Ratio" + tg)
                h_TriggerRatio[tg].Sumw2()
                h_TriggerRatio[tg].SetStats(0)
                h_TriggerRatio[tg].Divide(h_metPt2["notrigger"])
                xTitle = h_metPt2["notrigger"].GetXaxis().GetTitle()
                xBinWidth = h_metPt2["notrigger"].GetXaxis().GetBinWidth(1)
                h_TriggerRatio[tg].SetTitle(";{0};Trigger Efficiency per {1} GeV/c".format(xTitle, round(xBinWidth)))
                h_TriggerRatio[tg].SetName(tg)
                if i == 0:
                    h_TriggerRatio[tg].SetMinimum(0.)
                    h_TriggerRatio[tg].SetMaximum(1.2)
                    h_TriggerRatio[tg].Draw('E1')
                    tX1 = 0.04 * (h_metPt2["notrigger"].GetXaxis().GetXmax())
                    tY1 = 0.95 * (h_TriggerRatio[tg].GetMaximum())
                if i > 0:
                    h_TriggerRatio[tg].Draw('E1 same')
            i += 1
    cv40.BuildLegend(0.4, 0.3, 0.4, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    # - GenMET pT plots ---------------------------------
    cv41 = triggerCanvas.cd(1)
    h_genMetPt2["notrigger"].SetTitle("")
    h_genMetPt2["notrigger"].SetMinimum(0.)
    h_genMetPt2["notrigger"].SetMaximum(2000)
    h_genMetPt2["notrigger"].Draw('E1')
    tX1 = 0.04 * (h_genMetPt2["notrigger"].GetXaxis().GetXmax())
    tY1 = 0.95 * (h_genMetPt2["notrigger"].GetMaximum())
    for key in trigList:
        if not (key == "Muon" or key == "MuPJets" or key == "stndlone"):
            for tg in trigList[key]:
                h_genMetPt2[tg].Draw('E1 same')
    cv41.BuildLegend(0.4, 0.3, 0.4, 0.3)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas)

    cv42 = triggerCanvas.cd(1)
    i = 0
    for key in trigList:
        if not (key == "Muon" or key == "MuPJets" or key == "stndlone"):
            for tg in trigList[key]:
                h_TriggerRatio[tg] = h_genMetPt2[tg].Clone("h_genMetPt2Ratio" + tg)
                h_TriggerRatio[tg].Sumw2()
                h_TriggerRatio[tg].SetStats(0)
                h_TriggerRatio[tg].Divide(h_genMetPt2["notrigger"])
                xTitle = h_genMetPt2["notrigger"].GetXaxis().GetTitle()
                xBinWidth = h_genMetPt2["notrigger"].GetXaxis().GetBinWidth(1)
                h_TriggerRatio[tg].SetTitle(";{0};Trigger Efficiency per {1} GeV/c".format(xTitle, round(xBinWidth)))
                h_TriggerRatio[tg].SetName(tg)
                if i == 0:
                    h_TriggerRatio[tg].SetMinimum(0.)
                    h_TriggerRatio[tg].SetMaximum(1.2)
                    h_TriggerRatio[tg].Draw('E1')
                    tX1 = 0.04 * (h_genMetPt2["notrigger"].GetXaxis().GetXmax())
                    tY1 = 0.95 * (h_TriggerRatio[tg].GetMaximum())
                if i > 0:
                    h_TriggerRatio[tg].Draw('E1 same')
                i += 1
    cv42.BuildLegend(0.4, 0.3, 0.4, 0.3)
    ROOT.gStyle.SetLegendTextSize(0.02)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    pdfCreator(argms, 1, triggerCanvas)

    # - Eta plots ------------------------------------------
    cv43 = triggerCanvas.cd(1)
    # h_jetEta2["notrigger"].GetYaxis().SetTitleOffset(1.1)
    h_jetEta2["notrigger"].Draw('E1')
    tX1 = 0.94 * (-6)
    tY1 = 0.95 * (h_jetEta2["notrigger"].GetMaximum())
    for key in trigList:
        if not (key == "Muon" or key == "MuPJets" or key == "stndlone"):
            for tg in trigList[key]:
                h_jetEta2[tg].Draw('E1 same')
    cv43.BuildLegend(0.4, 0.3, 0.4, 0.3)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas)

    cv44 = triggerCanvas.cd(1)
    # h_elEta["notrigger"].GetYaxis().SetTitleOffset(1.2)
    h_elEta["notrigger"].Draw('E1')
    tX1 = 0.94 * (-6)
    tY1 = 0.95 * (h_elEta["notrigger"].GetMaximum())
    for key in trigList:
        if not (key == "Muon" or key == "MuPJets" or key == "stndlone"):
            for tg in trigList[key]:
                h_elEta[tg].Draw('E1 same')
    cv44.BuildLegend(0.4, 0.3, 0.4, 0.3)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas)

    # - Phi plots ------------------------------------------
    cv45 = triggerCanvas.cd(1)
    # h_jetPhi2["notrigger"].GetYaxis().SetTitleOffset(1.3)
    h_jetPhi2["notrigger"].Draw('E1')
    tX1 = 0.94 * (-6)
    tY1 = 0.95 * (h_jetPhi2["notrigger"].GetMaximum())
    for key in trigList:
        if not (key == "Muon" or key == "MuPJets" or key == "stndlone"):
            for tg in trigList[key]:
                h_jetPhi2[tg].Draw('E1 same')
    cv45.BuildLegend(0.4, 0.3, 0.4, 0.3)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas)

    cv46 = triggerCanvas.cd(1)
    # h_elPhi["notrigger"].GetYaxis().SetTitleOffset(1.4)
    h_elPhi["notrigger"].Draw('E1')
    tX1 = 0.94 * (-6)
    tY1 = 0.97 * (h_elPhi["notrigger"].GetMaximum())
    for key in trigList:
        if not (key == "Muon" or key == "MuPJets" or key == "stndlone"):
            for tg in trigList[key]:
                h_elPhi[tg].Draw('E1 same')
    cv46.BuildLegend(0.4, 0.3, 0.4, 0.3)
    ltx.SetTextSize(0.03)
    ltx.DrawLatex(tX1, tY1, legString)
    ROOT.gStyle.SetLegendTextSize(0.02)
    pdfCreator(argms, 1, triggerCanvas)

    # - Eta-Phi Map plots ------------------------------------------
    triggerCanvas.cd(1)
    h_jetMap2["notrigger"].Draw('COLZ')  # CONT4Z
    # pdfCreator(argms, 1, triggerCanvas)
    for key in trigList:
        if not (key == "Muon" or key == "MuPJets" or key == "stndlone"):
            for tg in trigList[key]:
                h_jetMap2[tg].Draw('COLZ')
                # pdfCreator(argms, 1, triggerCanvas)

    h_elMap["notrigger"].Draw('COLZ')
    # pdfCreator(argms, 1, triggerCanvas)
    for key in trigList:
        if not (key == "Muon" or key == "MuPJets" or key == "stndlone"):
            for tg in trigList[key]:
                h_elMap[tg].Draw('COLZ')  # E
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
        for tg in trigList[key]:
            ltx.DrawLatex((i + 2.5), tY1, tg)
            i += 1

    # h.GetXAxis().SetBinLabel(binnumber,string)
    pdfCreator(argms, 2, triggerCanvas)

    histFile.Close()


main(process_arguments())
