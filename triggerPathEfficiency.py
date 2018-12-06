import os, errno
import ROOT
from ROOT import TLatex
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from datetime import datetime 

def main():
    """ This code merges histograms, only for specific root file """

    # - TODO: Add Command line arguments
    
    # - Initialise variables
    time_ = datetime.now()
    triggerPath1 = 'PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2'
    triggerPath2 = 'IsoMu24'

    # - Create canvases
    triggerCanvas = ROOT.TCanvas('triggerCanvas', 'Triggers: ' + triggerPath1 + 'and' + triggerPath2 , 1100,700)
    triggerCanvas.Divide(2,2)
    eventPrgCanvas = ROOT.TCanvas('eventPrgCanvas', 'Canvas of events in each selection step', 500,500)

    # - Jet HT histograms
    h_PtTriggerStack = ROOT.THStack('h_PtTriggerStack', ';muon p_{T} (GeV); Events ')
    histFile = ROOT.TFile.Open("../RWOutput/OutHistoMaker2.root")
    histFile.cd("plots")
    h_jetHt = ROOT.gDirectory.Get("h_jetHt_notrigger")
    h_jetHt.SetLineColor(28)
    if not (h_jetHt):
        print("jetHt histogram is empty")
    h_jetHtT1 = ROOT.gDirectory.Get("h_jetHt_" + triggerPath1)
    h_jetHtT1.SetLineStyle(2)
    if not (h_jetHtT1):
        print("jetPtT1 histogram is empty")
    h_jetHtT2 = ROOT.gDirectory.Get("h_jetHt_" + triggerPath2)
    h_jetHtT2.SetLineStyle(7)
    if not (h_jetHtT2):
        print("jetPtT2 histogram is empty")
    h_jetHtT3 = ROOT.gDirectory.Get("h_jetHt_combined")
    h_jetHtT3.SetLineStyle(1)
    if not (h_jetHtT3):
        print("jetPtT3 histogram is empty")

    # - Muon histograms
    h_muonPt = ROOT.gDirectory.Get("h_muonPt_notrigger")
    h_muonPt.SetLineColor(28)
    if not (h_muonPt):
        print("muonPt histogram is empty")
    h_muonPtT1 = ROOT.gDirectory.Get("h_muonPt_" + triggerPath1)
    h_muonPtT1.SetLineStyle(2)
    if not (h_muonPtT1):
        print("muonPtT1 histogram is empty")
    h_muonPtT2 = ROOT.gDirectory.Get("h_muonPt_" + triggerPath2)
    h_muonPtT2.SetLineStyle(7)
    if not (h_muonPtT2):
        print("muonPtT2 histogram is empty")
    h_muonPtT3 = ROOT.gDirectory.Get("h_muonPt_combined")
    h_muonPtT3.SetLineStyle(1)
    if not (h_muonPtT3):
        print("muonPtT3 histogram is empty")
    h_eventsPrg = ROOT.gDirectory.Get("h_eventsPrg")
    if not (h_eventsPrg):
        print("h_eventsPrg histogram is empty")
        return 

    ###########################
    # - Draw Histos on Canvas #
    ###########################
    triggerCanvas.cd(1)
    h_jetHt.GetXaxis().SetTitle("H_{T} (GeV)")
    h_jetHt.GetYaxis().SetTitleOffset(1.5)
    h_jetHt.Draw()
    #h_jetHtT1.Draw('same')
    #h_jetHtT2.Draw('same')
    h_jetHtT3.Draw('same')
    legg = ROOT.TLegend(0.12, 0.7,0.3, 0.87)
    legg.AddEntry(h_jetHt, "no trigger", "l")
    #legg.AddEntry(h_jetHtT1, triggerPath1, "l")
    #legg.AddEntry(h_jetHtT2, triggerPath2, "l")
    legg.AddEntry(h_jetHtT3, " combined ", "l")
    ROOT.gStyle.SetLegendTextSize(0.04)
    legg.SetBorderSize(0)
    legg.Draw()
    
    triggerCanvas.cd(2)
    h_jetHtTriggerRatio1 = (h_jetHtT1).Clone("h_jetPtTriggerRatio1")
    h_jetHtTriggerRatio1.Divide(h_jetHt)
    h_jetHtTriggerRatio1.SetLineStyle(2)
    #h_jetHtTriggerRatio1.Draw()
    h_jetHtTriggerRatio1.SetTitle("Trigger Efficiency vs H_{T};H_{T} (GeV);Trigger Efficiency")
    h_jetHtTriggerRatio1.GetYaxis().SetRangeUser(0,1.1)
    h_jetHtTriggerRatio1.SetStats(False)
    h_jetHtTriggerRatio2 = (h_jetHtT2).Clone("h_jetPtTriggerRatio2")
    h_jetHtTriggerRatio2.Divide(h_jetHt)
    h_jetHtTriggerRatio2.SetLineStyle(7)
    #h_jetHtTriggerRatio2.Draw('same')
    h_jetHtTriggerRatio3 = (h_jetHtT3).Clone("h_jetPtTriggerRatio3")
    h_jetHtTriggerRatio3.Divide(h_jetHt)
    h_jetHtTriggerRatio3.SetLineStyle(1)
    h_jetHtTriggerRatio3.Draw('same')
    legg2 = ROOT.TLegend(0.12, 0.7,0.3, 0.87)
    #legg2.AddEntry(h_jetHtTriggerRatio1, triggerPath1, "l")
    legg2.AddEntry(h_jetHtTriggerRatio2, triggerPath2, "l")
    legg2.AddEntry(h_jetHtTriggerRatio3, " combined " , "l")
    ROOT.gStyle.SetLegendTextSize(0.04)
    legg2.SetBorderSize(0)
    legg2.Draw()

    triggerCanvas.cd(4)
    h_muonPtTriggerRatio1 = (h_muonPtT1).Clone("h_muonPtTriggerRatio1")
    h_muonPtTriggerRatio1.Divide(h_muonPt)
    h_muonPtTriggerRatio1.SetLineStyle(2)
    #h_muonPtTriggerRatio1.Draw()
    h_muonPtTriggerRatio2 = (h_muonPtT2).Clone("h_muonPtTriggerRatio2")
    h_muonPtTriggerRatio2.Divide(h_muonPt)
    h_muonPtTriggerRatio2.SetLineStyle(7)
    #h_muonPtTriggerRatio2.Draw('same')
    h_muonPtTriggerRatio3 = (h_muonPtT3).Clone("h_muonPtTriggerRatio3")
    h_muonPtTriggerRatio3.Divide(h_muonPt)
    h_muonPtTriggerRatio3.SetLineStyle(1)
    h_muonPtTriggerRatio3.Draw('same')
    h_muonPtTriggerRatio1.SetTitle("Trigger Efficiency vs muon p_{T};muon p_{T} (GeV);Trigger Efficiency")
    h_muonPtTriggerRatio1.GetYaxis().SetRangeUser(0,1.1)
    h_muonPtTriggerRatio1.SetStats(False)
    legg3 = ROOT.TLegend(0.5, 0.1,0.88, 0.33)
    #legg3.AddEntry(h_muonPtTriggerRatio1, triggerPath1, "l")
    #legg3.AddEntry(h_muonPtTriggerRatio2, triggerPath2, "l")
    legg3.AddEntry(h_muonPtTriggerRatio3, " combined ", "l")
    ROOT.gStyle.SetLegendTextSize(0.04)
    legg3.SetBorderSize(0)
    legg3.Draw()

    triggerCanvas.cd(3)
    h_muonPt.GetYaxis().SetTitleOffset(1.7)
    h_PtTriggerStack.Add(h_muonPt)
    h_muonPtT1.GetYaxis().SetTitleOffset(1.7)
    #h_PtTriggerStack.Add(h_muonPtT1)
    #h_PtTriggerStack.Add(h_muonPtT2)
    h_PtTriggerStack.Add(h_muonPtT3)
    h_PtTriggerStack.Draw('nostack')
    h_muonPt.SetStats(False)
    h_muonPtT1.SetStats(False)
    h_muonPtT2.SetStats(False)
    #h_muonPtT3.SetStats(False)
    legend = ROOT.TLegend(0.6, 0.7,0.88, 0.87)
    ROOT.gStyle.SetLegendTextSize(0.04)
    legend.SetBorderSize(0)
    legend.AddEntry(h_muonPt, "no trigger", "l")
    #legend.AddEntry(h_muonPtT1, triggerPath1, "l")
    #legend.AddEntry(h_muonPtT2, triggerPath2, "l")
    legend.AddEntry(h_muonPtT3," combined ", "l")
    legend.Draw()

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

main()
