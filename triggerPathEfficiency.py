import os, errno
import ROOT
from ROOT import TLatex
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from datetime import datetime

def process_arguments():
    """ Process command-line arguments """

    parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--inputLFN", choices= ["ttjets","tttt", "tttt_weights", "wjets"],
                        default = "tttt", help= "Set list of input files")
    args = parser.parse_args()
    return args

def main(argms):
    """ This code merges histograms, only for specific root file """

    if argms.inputLFN == "ttjets":
        inputFile = "OutHistosTT6jets.root"
    elif argms.inputLFN == "tttt_weights":
        inputFile = "OutHistosTTTTweights.root"
    elif argms.inputLFN == "wjets":
        inputFile = "OutHistosWjets.root"
    elif argms.inputLFN == "tttt":
        inputFile = "TestOutHistosTTTT_6jets.root"
    else:
        return 0
    
    # - Initialise variables
    time_ = datetime.now()

    trigList = {"combos":['IsoMu24_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2'],
                "stndlone":['Mu15_IsoVVVL_PFHT450_CaloBTagCSV_4p5'],
                "t1" :['IsoMu24'],
                "t2":['PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2']}

    h_jetHt = {}
    h_jetEta = {}
    h_jetPhi ={}
    h_jetMap = {}
    h_muonPt = {}
    h_muonEta = {}
    h_muonPhi = {}
    h_muonMap = {}
    h_jetHtTriggerRatio ={}
    h_muoPtTriggerRatio = {}

    # - Create canvases
    triggerCanvas = ROOT.TCanvas('triggerCanvas', 'Triggers: PFHT380or430_min6jets_min1btag and' + triggerPath2 , 1100,600)
    triggerCanvas.Divide(2,1)
    #eventPrgCanvas = ROOT.TCanvas('eventPrgCanvas', 'Canvas of events in each selection step', 500,500)

    # - Open file and sub folder
    histFile = ROOT.TFile.Open(inputFile)
    histFile.cd("plots")

    # - Jet HT histograms
    h_jetHt["notrigger"] = ROOT.gDirectory.Get("h_jetHt_notrigger")
    h_jetHt["notrigger"].SetLineColor(1)
    h_jetHt["notrigger"].SetTitle("no trigger")
    if not (h_jetHt["notrigger"]):
        print("No trigger jet Ht histogram is empty")
    h_muonPt["notrigger"] = ROOT.gDirectory.Get("h_muonPt_notrigger")
    h_muonPt["notrigger"].SetLineColor(1)
    h_muonPt["notrigger"].SetTitle("no trigger")
    if not (h_muonPt["notrigger"]):
        print("No trigger muon Pt histogram is empty")

    for key in trigList:
        for tg in trigList[key]:
            h_jetHt[tg] = ROOT.gDirectory.Get("h_jetHt_" + tg)
            h_jetEta[tg] = ROOT.gDirectory.Get("h_jetEta_" + tg)
            h_jetPhi[tg] = ROOT.gDirectory.Get("h_jetPhi_" + tg)
            h_jetMap[tg] = ROOT.gDirectory.Get("h_jetMap_" + tg)
            h_muonPt[tg] = ROOT.gDirectory.Get("h_muonPt_" + tg)
            h_muonEta[tg] = ROOT.gDirectory.Get("h_muonEta_" + tg)
            h_muonPhi[tg] = ROOT.gDirectory.Get("h_muonPhi_" + tg)
            h_muonMap[tg] = ROOT.gDirectory.Get("h_muonMap_" + tg)

    # - Events histogram
    h_eventsPrg = ROOT.gDirectory.Get("h_eventsPrg")
    if not (h_eventsPrg):
        print("h_eventsPrg histogram is empty")
        return 

    ##############################
    # - Draw HT Histos on Canvas #
    ##############################
    cv1=triggerCanvas.cd(1)
    h_jetHt["notrigger"].GetYaxis().SetTitleOffset(1.5)
    h_jetHt["notrigger"].Draw()
    for key in trigList:
        for tg in trigList[key]:
            h_jetHt[tg].Draw('same')
    leg1=cv1.BuildLegend()
    leg1.SetNColumns(2)
    ROOT.gStyle.SetLegendTextSize(0.03)

    cv2=triggerCanvas.cd(2)
    for tg in trigList["combos"]:
        h_jetHtTriggerRatio[tg] = (h_jetHt[tg]).Clone("h_jetPtRatio" + tg)
        h_jetHtTriggerRatio[tg].Divide(h_jetHt["notrigger"])
        h_jetHtTriggerRatio[tg].Draw('same')

    # h_jetHtTriggerRatio1 = (h_jetHtT1_1).Clone("h_jetPtTriggerRatio1")
    # h_jetHtTriggerRatio1.SetTitle("PFHT380;H_{T} (GeV);Trigger Efficiency")
    # h_jetHtTriggerRatio1.GetYaxis().SetRangeUser(0,1.1)
    # h_jetHtTriggerRatio1.SetStats(False)
    # h_jetHtTriggerRatio1.Divide(h_jetHt)
    # h_jetHtTriggerRatio1.SetLineStyle(2)
    # h_jetHtTriggerRatio1.Draw()
    # h_jetHtTriggerRatio1_2 = (h_jetHtT1_2).Clone("h_jetPtTriggerRatio1_2")
    # h_jetHtTriggerRatio1_2.Divide(h_jetHt)
    # h_jetHtTriggerRatio1_2.SetLineStyle(2)
    # h_jetHtTriggerRatio1_2.Draw('same')
    # h_jetHtTriggerRatio1_3 = (h_jetHtT1_3).Clone("h_jetPtTriggerRatio1_3")
    # h_jetHtTriggerRatio1_3.Divide(h_jetHt)
    # h_jetHtTriggerRatio1_3.SetLineStyle(2)
    # h_jetHtTriggerRatio1_3.Draw('same')
    # h_jetHtTriggerRatio1_4 = (h_jetHtT1_4).Clone("h_jetPtTriggerRatio1_4")
    # h_jetHtTriggerRatio1_4.Divide(h_jetHt)
    # h_jetHtTriggerRatio1_4.SetLineStyle(2)
    # h_jetHtTriggerRatio1_4.Draw('same')
    # h_jetHtTriggerRatio2 = (h_jetHtT2).Clone("h_jetPtTriggerRatio2")
    # h_jetHtTriggerRatio2.SetTitle("IsoMu24")
    # h_jetHtTriggerRatio2.Divide(h_jetHt)
    # h_jetHtTriggerRatio2.SetLineStyle(7)
    # h_jetHtTriggerRatio2.Draw('same')
    # h_jetHtTriggerRatio3_1 = (h_jetHtT3_1).Clone("h_jetPtTriggerRatio3_1")
    # h_jetHtTriggerRatio3_1.SetTitle("combined")
    # h_jetHtTriggerRatio3_1.Divide(h_jetHt)
    # h_jetHtTriggerRatio3_1.SetLineStyle(1)
    # h_jetHtTriggerRatio3_1.Draw('same')
    # h_jetHtTriggerRatio3_2 = (h_jetHtT3_2).Clone("h_jetPtTriggerRatio3_2")
    # h_jetHtTriggerRatio3_2.Divide(h_jetHt)
    # h_jetHtTriggerRatio3_2.SetLineStyle(1)
    # h_jetHtTriggerRatio3_2.Draw('same')
    # h_jetHtTriggerRatio3_3 = (h_jetHtT3_3).Clone("h_jetPtTriggerRatio3_3")
    # h_jetHtTriggerRatio3_3.Divide(h_jetHt)
    # h_jetHtTriggerRatio3_3.SetLineStyle(1)
    # h_jetHtTriggerRatio3_3.Draw('same')
    # h_jetHtTriggerRatio3_4 = (h_jetHtT3_4).Clone("h_jetPtTriggerRatio3_4")
    # h_jetHtTriggerRatio3_4.Divide(h_jetHt)
    # h_jetHtTriggerRatio3_4.SetLineStyle(1)
    # h_jetHtTriggerRatio3_4.Draw('same')
    cv2.BuildLegend()
    ROOT.gStyle.SetLegendTextSize(0.04)

    #######################
    # Save Canvas to File #
    #######################
    filename = time_.strftime("TriggerPlots/W%V_%y/%w%a.pdf")
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    triggerCanvas.Print(time_.strftime("TriggerPlots/W%V_%y/%w%a.pdf("),"pdf")


    ##############################
    # - Draw pT Histos on Canvas #
    ##############################
    cv3=triggerCanvas.cd(1)
    h_muonPt["notrigger"].GetYaxis().SetTitleOffset(1.5)
    h_muonPt["notrigger"].Draw()
    for key in trigList:
        for tg in trigList[key]:
            h_muonPt[tg].Draw('same')
    cv3.BuildLegend()
    ROOT.gStyle.SetLegendTextSize(0.04)

    cv4=triggerCanvas.cd(2)
    for tg in trigList["combos"]:
        h_muoPtTriggerRatio[tg] = (h_jetHt[tg]).Clone("h_muonPtRatio" + tg)
        h_muoPtTriggerRatio[tg].Divide(h_muonPt["notrigger"])
        h_muoPtTriggerRatio[tg].Draw('same')

    # h_muonPtTriggerRatio1 = (h_muonPtT1_1).Clone("h_muonPtTriggerRatio1")
    # h_muonPtTriggerRatio1.SetTitle("PFHT380;muon p_{T} (GeV);Trigger Efficiency")
    # h_muonPtTriggerRatio1.GetYaxis().SetRangeUser(0,1.1)
    # h_muonPtTriggerRatio1.SetStats(False)
    # h_muonPtTriggerRatio1.Divide(h_muonPt)
    # h_muonPtTriggerRatio1.SetLineStyle(2)
    # h_muonPtTriggerRatio1.Draw()
    # h_muonPtTriggerRatio1_2 = (h_muonPtT1_2).Clone("h_muonPtTriggerRatio1_2")
    # h_muonPtTriggerRatio1_2.Divide(h_muonPt)
    # h_muonPtTriggerRatio1_2.SetLineStyle(2)
    # h_muonPtTriggerRatio1_2.Draw('same')
    # h_muonPtTriggerRatio1_3 = (h_muonPtT1_3).Clone("h_muonPtTriggerRatio1_3")
    # h_muonPtTriggerRatio1_3.Divide(h_muonPt)
    # h_muonPtTriggerRatio1_3.SetLineStyle(2)
    # h_muonPtTriggerRatio1_3.Draw('same')
    # h_muonPtTriggerRatio1_4 = (h_muonPtT1_4).Clone("h_muonPtTriggerRatio1_4")
    # h_muonPtTriggerRatio1_4.Divide(h_muonPt)
    # h_muonPtTriggerRatio1_4.SetLineStyle(2)
    # h_muonPtTriggerRatio1_4.Draw('same')
    # h_muonPtTriggerRatio2 = (h_muonPtT2).Clone("h_muonPtTriggerRatio2")
    # h_muonPtTriggerRatio2.SetTitle("IsoMu24")
    # h_muonPtTriggerRatio2.Divide(h_muonPt)
    # h_muonPtTriggerRatio2.SetLineStyle(7)
    # h_muonPtTriggerRatio2.Draw('same')
    # h_muonPtTriggerRatio3_1 = (h_muonPtT3_1).Clone("h_muonPtTriggerRatio3_1")
    # h_muonPtTriggerRatio3_1.SetTitle("combined")
    # h_muonPtTriggerRatio3_1.Divide(h_muonPt)
    # h_muonPtTriggerRatio3_1.SetLineStyle(1)
    # h_muonPtTriggerRatio3_1.Draw('same')
    # h_muonPtTriggerRatio3_2 = (h_muonPtT3_2).Clone("h_muonPtTriggerRatio3_2")
    # h_muonPtTriggerRatio3_2.Divide(h_muonPt)
    # h_muonPtTriggerRatio3_2.SetLineStyle(1)
    # h_muonPtTriggerRatio3_2.Draw('same')
    # h_muonPtTriggerRatio3_3 = (h_muonPtT3_3).Clone("h_muonPtTriggerRatio3_3")
    # h_muonPtTriggerRatio3_3.Divide(h_muonPt)
    # h_muonPtTriggerRatio3_3.SetLineStyle(1)
    # h_muonPtTriggerRatio3_3.Draw('same')
    # h_muonPtTriggerRatio3_4 = (h_muonPtT3_4).Clone("h_muonPtTriggerRatio3_4")
    # h_muonPtTriggerRatio3_4.Divide(h_muonPt)
    # h_muonPtTriggerRatio3_4.SetLineStyle(1)
    # h_muonPtTriggerRatio3_4.Draw('same')
    cv4.BuildLegend()
    ROOT.gStyle.SetLegendTextSize(0.04)

    filename = time_.strftime("TriggerPlots/W%V_%y/%w%a.pdf")
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    triggerCanvas.Print(time_.strftime("TriggerPlots/W%V_%y/%w%a.pdf)"),"pdf")

    #######################
    # Save Canvas to File #
    #######################
    # filename = time_.strftime("TriggerPlots/W%V_%y/%w%a.pdf")
    # if not os.path.exists(os.path.dirname(filename)):
    #     try:
    #         os.makedirs(os.path.dirname(filename))
    #     except OSError as exc:
    #         if exc.errno != errno.EEXIST:
    #             raise
    # triggerCanvas.Print(time_.strftime("TriggerPlots/W%V_%y/%w%a.png"))
    #
    # -Test Event numbers along steps
    #eventPrgCanvas.cd(1)
    #h_eventsPrg.Draw()
    #eventPrgCanvas.Print("eventProgress.png")
    histFile.Close()

main(process_arguments())
