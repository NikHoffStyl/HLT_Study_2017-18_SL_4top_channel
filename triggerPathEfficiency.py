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

    # - TODO: Add Command line arguments
    if argms.inputLFN == "ttjets":
        inputFile = "OutHistosTT6jets.root"
    elif argms.inputLFN == "tttt_weights":
        inputFile = "OutHistosTTTTweights.root"
    elif argms.inputLFN == "wjets":
        inputFile = "OutHistosWjets.root"
    elif argms.inputLFN == "tttt":
        inputFile = "OutHistosTTTT_6jets.root"
    else:
        inputFile = "OutHistosTTTT_6jets.root"
    
    # - Initialise variables
    time_ = datetime.now()
    triggerPath1_1 = 'PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2'
    triggerPath1_2='PFHT380_SixPFJet32_DoublePFBTagCSV_2p2'
    triggerPath1_3='PFHT430_SixPFJet40_PFBTagCSV_1p5'
    triggerPath1_4='PFHT430_SixPFJet40'
    triggerPath2 = 'IsoMu24'

    # - Create canvases
    triggerCanvas = ROOT.TCanvas('triggerCanvas', 'Triggers: PFHT380or430_min6jets_min1btag and' + triggerPath2 , 1100,700)
    triggerCanvas.Divide(2,2)
    #eventPrgCanvas = ROOT.TCanvas('eventPrgCanvas', 'Canvas of events in each selection step', 500,500)

    # - Open file and sub folder
    histFile = ROOT.TFile.Open(inputFile)
    histFile.cd("plots")

    # - Jet HT histograms
    h_jetHt = ROOT.gDirectory.Get("h_jetHt_notrigger")
    h_jetHt.SetLineColor(1)
    if not (h_jetHt):
        print("jetHt histogram is empty")
    h_jetHtT1_1 = ROOT.gDirectory.Get("h_jetHt_" + triggerPath1_1)
    h_jetHtT1_1.SetLineStyle(2)
    h_jetHtT1_1.SetLineColor(2)
    if not (h_jetHtT1_1):
        print("jetPtT1 histogram is empty")
    # h_jetHtT1_2 = ROOT.gDirectory.Get("h_jetHt_" + triggerPath1_2)
    # h_jetHtT1_2.SetLineStyle(2)
    # h_jetHtT1_2.SetLineColor(4)
    # if not (h_jetHtT1_2):
    #     print("jetPtT1_2 histogram is empty")
    # h_jetHtT1_3 = ROOT.gDirectory.Get("h_jetHt_" + triggerPath1_3)
    # h_jetHtT1_3.SetLineStyle(2)
    # h_jetHtT1_3.SetLineColor(8)
    # if not (h_jetHtT1_3):
    #     print("jetPtT1_3 histogram is empty")
    # h_jetHtT1_4 = ROOT.gDirectory.Get("h_jetHt_" + triggerPath1_4)
    # h_jetHtT1_4.SetLineStyle(2)
    # h_jetHtT1_4.SetLineColor(9)
    # if not (h_jetHtT1_4):
    #     print("jetPtT1_4 histogram is empty")
    h_jetHtT2 = ROOT.gDirectory.Get("h_jetHt_" + triggerPath2)
    h_jetHtT2.SetLineStyle(2)
    if not (h_jetHtT2):
        print("jetPtT2 histogram is empty")
    h_jetHtT3_1 = ROOT.gDirectory.Get("h_jetHt_combination1")
    h_jetHtT3_1.SetLineStyle(1)
    h_jetHtT3_1.SetLineColor(2)
    if not (h_jetHtT3_1):
        print("jetPtT3_1 histogram is empty")
    # h_jetHtT3_2 = ROOT.gDirectory.Get("h_jetHt_combination2")
    # h_jetHtT3_2.SetLineStyle(1)
    # h_jetHtT3_2.SetLineColor(4)
    # if not (h_jetHtT3_2):
    #     print("jetPtT3_2 histogram is empty")
    # h_jetHtT3_3 = ROOT.gDirectory.Get("h_jetHt_combination3")
    # h_jetHtT3_3.SetLineStyle(1)
    # h_jetHtT3_3.SetLineColor(8)
    # if not (h_jetHtT3_3):
    #     print("jetPtT3_3 histogram is empty")
    # h_jetHtT3_4 = ROOT.gDirectory.Get("h_jetHt_combination4")
    # h_jetHtT3_4.SetLineStyle(1)
    # h_jetHtT3_4.SetLineColor(9)
    # if not (h_jetHtT3_4):
    #     print("jetPtT3_4 histogram is empty")


    # - Muon histograms
    h_muonPt = ROOT.gDirectory.Get("h_muonPt_notrigger")
    h_muonPt.SetLineColor(1)
    if not (h_muonPt):
        print("muonPt histogram is empty")
    h_muonPtT1_1 = ROOT.gDirectory.Get("h_muonPt_" + triggerPath1_1)
    h_muonPtT1_1.SetLineStyle(2)
    h_muonPtT1_1.SetLineColor(2)
    if not (h_muonPtT1_1):
        print("muonPtT1 histogram is empty")
    # h_muonPtT1_2 = ROOT.gDirectory.Get("h_muonPt_" + triggerPath1_2)
    # h_muonPtT1_2.SetLineStyle(2)
    # h_muonPtT1_2.SetLineColor(4)
    # if not (h_muonPtT1_2):
    #     print("muonPtT1_2 histogram is empty")
    # h_muonPtT1_3 = ROOT.gDirectory.Get("h_muonPt_" + triggerPath1_3)
    # h_muonPtT1_3.SetLineStyle(2)
    # h_muonPtT1_3.SetLineColor(8)
    # if not (h_muonPtT1_3):
    #     print("muonPtT1_3 histogram is empty")
    # h_muonPtT1_4 = ROOT.gDirectory.Get("h_muonPt_" + triggerPath1_4)
    # h_muonPtT1_4.SetLineStyle(2)
    # h_muonPtT1_4.SetLineColor(9)
    # if not (h_muonPtT1_4):
    #     print("muonPtT1_4 histogram is empty")
    h_muonPtT2 = ROOT.gDirectory.Get("h_muonPt_" + triggerPath2)
    h_muonPtT2.SetLineStyle(2)
    if not (h_muonPtT2):
        print("muonPtT2 histogram is empty")
    h_muonPtT3_1 = ROOT.gDirectory.Get("h_muonPt_combination1")
    h_muonPtT3_1.SetLineStyle(1)
    h_muonPtT3_1.SetLineColor(2)
    if not (h_muonPtT3_1):
        print("muonPtT3_1 histogram is empty")
    # h_muonPtT3_2 = ROOT.gDirectory.Get("h_muonPt_combination2")
    # h_muonPtT3_2.SetLineStyle(1)
    # h_muonPtT3_2.SetLineColor(4)
    # if not (h_muonPtT3_2):
    #     print("muonPtT3_2 histogram is empty")
    # h_muonPtT3_3 = ROOT.gDirectory.Get("h_muonPt_combination3")
    # h_muonPtT3_3.SetLineStyle(1)
    # h_muonPtT3_3.SetLineColor(8)
    # if not (h_muonPtT3_3):
    #     print("muonPtT3_3 histogram is empty")
    # h_muonPtT3_4 = ROOT.gDirectory.Get("h_muonPt_combination4")
    # h_muonPtT3_4.SetLineStyle(1)
    # h_muonPtT3_4.SetLineColor(9)
    # if not (h_muonPtT3_4):
    #     print("muonPtT3_4 histogram is empty")

    # - Events histogram
    h_eventsPrg = ROOT.gDirectory.Get("h_eventsPrg")
    if not (h_eventsPrg):
        print("h_eventsPrg histogram is empty")
        return 

    ###########################
    # - Draw Histos on Canvas #
    ###########################
    cv1=triggerCanvas.cd(1)
    h_jetHt.GetYaxis().SetTitleOffset(1.5)
    h_jetHt.Draw()
    h_jetHtT1_1.Draw('same')
    # h_jetHtT1_2.Draw('same')
    # h_jetHtT1_3.Draw('same')
    # h_jetHtT1_4.Draw('same')
    h_jetHtT2.Draw('same')
    h_jetHtT3_1.Draw('same')
    # h_jetHtT3_2.Draw('same')
    # h_jetHtT3_3.Draw('same')
    # h_jetHtT3_4.Draw('same')
    cv1.BuildLegend(0.5,0.4, 0.5, 0.4)


    cv3=triggerCanvas.cd(3)
    h_muonPt.GetYaxis().SetTitleOffset(1.5)
    h_muonPt.Draw()
    h_muonPtT1_1.Draw('same')
    # h_muonPtT1_2.Draw('same')
    # h_muonPtT1_3.Draw('same')
    # h_muonPtT1_4.Draw('same')
    h_muonPtT2.Draw('same')
    h_muonPtT3_1.Draw('same')
    # h_muonPtT3_2.Draw('same')
    # h_muonPtT3_3.Draw('same')
    # h_muonPtT3_4.Draw('same')
    cv3.BuildLegend(0.5,0.4, 0.5, 0.4)

    cv2=triggerCanvas.cd(2)
    h_jetHtTriggerRatio1 = (h_jetHtT1_1).Clone("h_jetPtTriggerRatio1")
    h_jetHtTriggerRatio1.SetTitle(";H_{T} (GeV);Trigger Efficiency")
    h_jetHtTriggerRatio1.GetYaxis().SetRangeUser(0,1.1)
    h_jetHtTriggerRatio1.SetStats(False)
    h_jetHtTriggerRatio1.Divide(h_jetHt)
    h_jetHtTriggerRatio1.SetLineStyle(2)
    h_jetHtTriggerRatio1.Draw()
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
    h_jetHtTriggerRatio2 = (h_jetHtT2).Clone("h_jetPtTriggerRatio2")
    h_jetHtTriggerRatio2.Divide(h_jetHt)
    h_jetHtTriggerRatio2.SetLineStyle(7)
    h_jetHtTriggerRatio2.Draw('same')
    h_jetHtTriggerRatio3_1 = (h_jetHtT3_1).Clone("h_jetPtTriggerRatio3_1")
    h_jetHtTriggerRatio3_1.Divide(h_jetHt)
    h_jetHtTriggerRatio3_1.SetLineStyle(1)
    h_jetHtTriggerRatio3_1.Draw('same')
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
    cv2.BuildLegend(0.5,0.4, 0.5, 0.4)

    cv4=triggerCanvas.cd(4)
    h_muonPtTriggerRatio1 = (h_muonPtT1_1).Clone("h_muonPtTriggerRatio1")
    h_muonPtTriggerRatio1.Divide(h_muonPt)
    h_muonPtTriggerRatio1.SetLineStyle(2)
    h_muonPtTriggerRatio1.Draw()
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
    h_muonPtTriggerRatio2 = (h_muonPtT2).Clone("h_muonPtTriggerRatio2")
    h_muonPtTriggerRatio2.Divide(h_muonPt)
    h_muonPtTriggerRatio2.SetLineStyle(7)
    h_muonPtTriggerRatio2.Draw('same')
    h_muonPtTriggerRatio3_1 = (h_muonPtT3_1).Clone("h_muonPtTriggerRatio3_1")
    h_muonPtTriggerRatio3_1.Divide(h_muonPt)
    h_muonPtTriggerRatio3_1.SetLineStyle(1)
    h_muonPtTriggerRatio3_1.Draw('same')
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
    h_muonPtTriggerRatio1.SetTitle(";muon p_{T} (GeV);Trigger Efficiency")
    h_muonPtTriggerRatio1.GetYaxis().SetRangeUser(0,1.1)
    h_muonPtTriggerRatio1.SetStats(False)
    cv4.BuildLegend(0.5,0.4, 0.5, 0.4)

    #######################
    # Save Canvas to File #
    #######################
    filename = time_.strftime("TriggerPlots/W%V_%y/Canvas%d_%m_%y_%H%M.png")
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    triggerCanvas.Print(time_.strftime("TriggerPlots/W%V_%y/Canvas%d_%m_%y_%H%M.png"))
    
    # -Test Event numbers along steps
    #eventPrgCanvas.cd(1)
    #h_eventsPrg.Draw()
    #eventPrgCanvas.Print("eventProgress.png")
    histFile.Close()

main(process_arguments())
