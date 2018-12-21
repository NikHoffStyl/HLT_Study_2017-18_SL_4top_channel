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

def pdfCreator(arg, canvas):
    time_ = datetime.now()
    filename = time_.strftime("TriggerPlots/W%V_%y/%w%a.pdf")
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    if arg == 0: canvas.Print(time_.strftime("TriggerPlots/W%V_%y/%w%a.pdf("),"pdf")
    if arg == 1: canvas.Print(time_.strftime("TriggerPlots/W%V_%y/%w%a.pdf"),"pdf")
    if arg == 2: canvas.Print(time_.strftime("TriggerPlots/W%V_%y/%w%a.pdf)"),"pdf")

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
    triggerCanvas = ROOT.TCanvas('triggerCanvas', 'Triggers', 1100,600)
    #triggerCanvas.Divide(2,1)

    # - Open file and sub folder
    histFile = ROOT.TFile.Open(inputFile)
    histFile.cd("plots")

    # - Jet HT histograms
    h_jetHt["notrigger"] = ROOT.gDirectory.Get("h_jetHt_notrigger")
    h_jetHt["notrigger"].SetLineColor(1)
    if not (h_jetHt["notrigger"]):
        print("No trigger jet Ht histogram is empty")
    h_muonPt["notrigger"] = ROOT.gDirectory.Get("h_muonPt_notrigger")
    h_muonPt["notrigger"].SetLineColor(1)
    if not (h_muonPt["notrigger"]):
        print("No trigger muon Pt histogram is empty")

    i=2
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

            h_jetHt[tg].SetLineColor(i)
            h_jetEta[tg].SetLineColor(i)
            h_jetPhi[tg].SetLineColor(i)
            h_muonPt[tg].SetLineColor(i)
            h_muonEta[tg].SetLineColor(i)
            h_muonPhi[tg].SetLineColor(i)

            i+=1

    # - Events histogram
    h_eventsPrg = ROOT.gDirectory.Get("h_eventsPrg")
    if not (h_eventsPrg):
        print("h_eventsPrg histogram is empty")
        return 

    ####################
    # - Draw on Canvas #
    ####################
    # - Canvas Details
    triggerCanvas.cd(2)
    l = TLatex(0.1,0.4,"""On-line (pre-)selection Requisites: \n
                          nJet > 5 && Jet_jetId>2 && abs(Jet_eta) <2.4 && \n
                          ( nMuon >0 || nElectron >0 ) && Muon_softId == 1  \n \n
                        Event Limit : None \n \n
                        Off-line (post-)selection Requisites: \n
                          jet.jetId>2 or jet.pt>30 or jet|#eta|<2.4 for at least 6 jets \n
                          jet.btagDeepFlavB > 0.7489 for at least one jet \n
                          muon_tightId=True and muon_|#eta|<2.4 
                          and muon.miniPFRelIso_all<0.15 for at least one muon
                        """
               )
    l.SetTextSize(0.15)
    l.Draw()
    pdfCreator(0,triggerCanvas)

    # - HT or pT plots ---------------------------------
    cv1=triggerCanvas.cd(1)
    h_jetHt["notrigger"].GetYaxis().SetTitleOffset(1.5)
    h_jetHt["notrigger"].Draw()
    for key in trigList:
        for tg in trigList[key]:
            h_jetHt[tg].Draw('same')
    cv1.BuildLegend(0.4,0.9,0.4,0.9)
    #leg1.SetNColumns(2)
    ROOT.gStyle.SetLegendTextSize(0.03)
    pdfCreator(1,triggerCanvas)

    cv2=triggerCanvas.cd(1)
    i=0
    for tg in (trigList["combos"] and trigList["stndlone"]):
        h_jetHtTriggerRatio[tg] = (h_jetHt[tg]).Clone("h_jetHtRatio" + tg)
        h_jetHtTriggerRatio[tg].Divide(h_jetHt["notrigger"])
        if  i==0: h_jetHtTriggerRatio[tg].Draw()
        if  i==1: h_jetHtTriggerRatio[tg].Draw('same')
        i += 1

    cv2.BuildLegend(0.2,0.9,0.2,0.9)
    ROOT.gStyle.SetLegendTextSize(0.03)
    pdfCreator(1,triggerCanvas)

    cv3=triggerCanvas.cd(1)
    h_muonPt["notrigger"].GetYaxis().SetTitleOffset(1.5)
    h_muonPt["notrigger"].Draw()
    for key in trigList:
        for tg in trigList[key]:
            h_muonPt[tg].Draw('same')
    cv3.BuildLegend(0.4,0.9,0.4,0.9)
    ROOT.gStyle.SetLegendTextSize(0.03)
    pdfCreator(1,triggerCanvas)

    cv4=triggerCanvas.cd(1)
    i=0
    for tg in (trigList["combos"] and trigList["stndlone"]):
        h_muoPtTriggerRatio[tg] = (h_muonPt[tg]).Clone("h_muonPtRatio" + tg)
        h_muoPtTriggerRatio[tg].Divide(h_muonPt["notrigger"])
        if i == 0 :h_muoPtTriggerRatio[tg].Draw()
        if i == 1 :h_muoPtTriggerRatio[tg].Draw('same')
        i += 1
    cv4.BuildLegend(0.2,0.9,0.2,0.9)
    ROOT.gStyle.SetLegendTextSize(0.03)
    pdfCreator(1,triggerCanvas)

    # - Eta plots ------------------------------------------
    cv5=triggerCanvas.cd(1)
    h_jetEta["notrigger"].GetYaxis().SetTitleOffset(1.5)
    h_jetEta["notrigger"].Draw()
    for key in trigList:
        for tg in trigList[key]:
            h_jetEta[tg].Draw('same')
    cv5.BuildLegend(0.4,0.9,0.4,0.9)
    ROOT.gStyle.SetLegendTextSize(0.03)
    pdfCreator(1,triggerCanvas)

    cv6=triggerCanvas.cd(1)
    h_muonEta["notrigger"].GetYaxis().SetTitleOffset(1.5)
    h_muonEta["notrigger"].Draw()
    for key in trigList:
        for tg in trigList[key]:
            h_muonEta[tg].Draw('same')
    cv6.BuildLegend(0.4,0.9,0.4,0.9)
    ROOT.gStyle.SetLegendTextSize(0.03)
    pdfCreator(1,triggerCanvas)


    # - Phi plots ------------------------------------------
    cv7=triggerCanvas.cd(1)
    h_jetPhi["notrigger"].GetYaxis().SetTitleOffset(1.5)
    h_jetPhi["notrigger"].Draw()
    for key in trigList:
        for tg in trigList[key]:
            h_jetPhi[tg].Draw('same')
    cv7.BuildLegend(0.4,0.9,0.4,0.9)
    ROOT.gStyle.SetLegendTextSize(0.03)
    pdfCreator(1,triggerCanvas)

    cv8=triggerCanvas.cd(1)
    h_muonPhi["notrigger"].GetYaxis().SetTitleOffset(1.5)
    h_muonPhi["notrigger"].Draw()
    for key in trigList:
        for tg in trigList[key]:
            h_muonPhi[tg].Draw('same')
    cv8.BuildLegend(0.4,0.9,0.4,0.9)
    ROOT.gStyle.SetLegendTextSize(0.03)
    pdfCreator(1,triggerCanvas)

    # - Eta-Phi Map plots ------------------------------------------
    triggerCanvas.cd(1)
    h_jetMap["notrigger"].GetYaxis().SetTitleOffset(1.5)
    h_jetMap["notrigger"].Draw('CONTZ')
    pdfCreator(1,triggerCanvas)
    for key in trigList:
        for tg in trigList[key]:
            h_jetMap[tg].Draw('CONTZ')
            pdfCreator(1,triggerCanvas)

    h_muonMap["notrigger"].GetYaxis().SetTitleOffset(1.5)
    h_muonMap["notrigger"].Draw('CONTZ')
    pdfCreator(1,triggerCanvas)
    for key in trigList:
        for tg in trigList[key]:
            h_muonMap[tg].Draw('CONTZ')
            pdfCreator(1,triggerCanvas)

    # - Test Event numbers along steps ----------
    triggerCanvas.cd(1)
    h_eventsPrg.Draw()
    pdfCreator(2,triggerCanvas)

    histFile.Close()

main(process_arguments())
