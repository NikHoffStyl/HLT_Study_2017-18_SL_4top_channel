import ROOT
from ROOT import TLatex
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

def main():
    #Create canvas
    triggerCanvas = ROOT.TCanvas('triggerCanvas', 'Canvas of Pt with and without triggers', 1100,660)
    triggerCanvas.Divide(2,2)

    #Get histos from file
    h_PtTriggerStack = ROOT.THStack('h_PtTriggerStack', ';P_{T} (GeV); Events ')
    histFile = ROOT.TFile.Open("../RWOutput/OutHistoMaker2.root")
    plotDirectory = histFile.cd("plots")
    h_jetPt = ROOT.gDirectory.Get("h_jetPt")
    h_jetPt.SetLineColor(28)
    if not (h_jetPt):
        print("jetPt histogram is empty")
    h_jetPtT = ROOT.gDirectory.Get("h_jetPtT")
    h_jetPtT.SetLineColor(1)
    if not (h_jetPtT):
        print("jetPt_t histogram is empty")
    h_elPt = ROOT.gDirectory.Get("h_elPt")
    h_elPt.SetLineColor(2)
    if not (h_elPt):
        print("elPt histogram is empty")
    h_elPtT = ROOT.gDirectory.Get("h_elPtT")
    h_elPtT.SetLineColor(3)
    if not (h_elPtT):
        print("elPt_t histogram is empty")
    h_muonPt = ROOT.gDirectory.Get("h_muonPt")
    h_muonPt.SetLineColor(4)
    if not (h_muonPt):
        print("muonPt histogram is empty")
    h_muonPtT = ROOT.gDirectory.Get("h_muonPtT")
    h_muonPtT.SetLineColor(6)
    if not (h_muonPtT):
        print("jetPt_t histogram is empty")

    cv = triggerCanvas.cd(1)
    h_jetPt.GetXaxis().SetTitle("H_{T} (GeV)")
    h_jetPt.GetYaxis().SetTitleOffset(1.5)
    h_jetPt.Draw()
    h_jetPt.SetStats(False)
    h_jetPtT.SetLineColor(2)
    h_jetPtT.Draw('same')
    legg = ROOT.TLegend(0.12, 0.7,0.3, 0.87)
    legg.AddEntry(h_jetPt, "without trigger", "l")
    legg.AddEntry(h_jetPtT, "with trigger", "l")
    ROOT.gStyle.SetLegendTextSize(0.04)
    legg.SetBorderSize(0)
    legg.Draw()

    cv = triggerCanvas.cd(2)
    h_jetPtTriggerRatio = (h_jetPtT).Clone("h_jetPtTriggerRatio")
    h_jetPtTriggerRatio.Divide(h_jetPt)
    h_jetPtTriggerRatio.SetLineColor(1)
    h_jetPtTriggerRatio.Draw()
    h_jetPtTriggerRatio.GetXaxis().SetTitle("H_{T} (GeV)")
    h_jetPtTriggerRatio.GetYaxis().SetTitle("Trigger Efficiency")
    h_jetPtTriggerRatio.GetYaxis().SetRangeUser(0,1)
    h_jetPtTriggerRatio.SetStats(False)
    legg2 = ROOT.TLegend(0.12, 0.7,0.3, 0.87)
    legg2.AddEntry(h_jetPtTriggerRatio, "jet", "l")
    ROOT.gStyle.SetLegendTextSize(0.04)
    legg2.SetBorderSize(0)
    legg2.Draw()

    cv = triggerCanvas.cd(4)
    h_elPtTriggerRatio = (h_elPtT).Clone("h_elPtTriggerRatio")
    h_elPtTriggerRatio.Divide(h_elPt)
    h_elPtTriggerRatio.SetLineColor(2)
    h_elPtTriggerRatio.Draw()
    h_muonPtTriggerRatio = (h_muonPtT).Clone("h_muonPtTriggerRatio")
    h_muonPtTriggerRatio.Divide(h_muonPt)
    h_muonPtTriggerRatio.SetLineColor(4)
    h_muonPtTriggerRatio.Draw('same')
    h_elPtTriggerRatio.GetXaxis().SetTitle("P_{T} (GeV)")
    h_elPtTriggerRatio.GetYaxis().SetTitle("Trigger Efficiency")
    h_elPtTriggerRatio.GetYaxis().SetRangeUser(0,1)
    h_elPtTriggerRatio.SetStats(False)
    legg3 = ROOT.TLegend(0.12, 0.7,0.3, 0.87)
    legg3.AddEntry(h_elPtTriggerRatio, "electron", "l")
    legg3.AddEntry(h_muonPtTriggerRatio, "muon", "l")
    ROOT.gStyle.SetLegendTextSize(0.04)
    legg3.SetBorderSize(0)
    legg3.Draw()

    cv = triggerCanvas.cd(3)
    h_PtTriggerStack.Add(h_elPt)
    h_elPt.GetYaxis().SetTitleOffset(1.7)
    h_PtTriggerStack.Add(h_muonPt)
    h_PtTriggerStack.Add(h_elPtT)
    h_muonPtT.GetYaxis().SetTitleOffset(1.7)
    h_PtTriggerStack.Add(h_muonPtT)
    h_PtTriggerStack.Draw('nostack')
    h_elPt.SetStats(False)
    h_elPtT.SetStats(False)
    h_muonPt.SetStats(False)
    h_muonPtT.SetStats(False)
    legend = ROOT.TLegend(0.47, 0.4,0.88, 0.86)
    legend.SetNColumns(2)
    ROOT.gStyle.SetLegendTextSize(0.04)
    legend.SetBorderSize(0)
    legend.SetHeader("with(without) trigger on left(right)", "C")
    en3=legend.AddEntry(h_elPtT, "electron", "l")
    en4=legend.AddEntry(h_elPt, "electron", "l")
    en5=legend.AddEntry(h_muonPtT, "muon ", "l")
    en6=legend.AddEntry(h_muonPt, "muon ", "l")
    legend.Draw()
    triggerCanvas.Print("../RWOutput/histCanvas.png")
    histFile.Close()

main()

"""if __name__ == "__main__":
    args = process_arguments()
    if args:
        main(args)"""
