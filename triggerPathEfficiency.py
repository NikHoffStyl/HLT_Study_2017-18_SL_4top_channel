import ROOT
from ROOT import TLatex
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

def main():
    #Create canvas
    triggerCanvas = ROOT.TCanvas('triggerCanvas', 'Canvas of Pt with and without triggers', 950,650)
    triggerCanvas.Divide(2,2)

    #Get histos from file
    h_PtTriggerStack = ROOT.THStack('h_PtTriggerStack', ';jetPt (GeV); Events (a.u.)')
    histFile = ROOT.TFile.Open("OutHistoMaker2.root")
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
    h_jetPt.GetYaxis().SetTitleOffset(1.5)
    h_jetPt.Draw()

    cv = triggerCanvas.cd(2)
    h_jetPtT.GetYaxis().SetTitleOffset(1.5)
    h_jetPtT.Draw()

    cv = triggerCanvas.cd(4)
    cv.SetLogy()
    cv.SetLogx()
    h_jetPtTriggerRatio = (h_jetPt).Clone("h_jetPtTriggerRatio")
    h_jetPtTriggerRatio.Divide(h_jetPtT)
    h_jetPtTriggerRatio.SetLineColor(1)
    h_jetPtTriggerRatio.Draw()
    #h_jetPtTriggerRatio.GetYaxis().SetTitleOffset(1.3)
    h_elPtTriggerRatio = (h_elPt).Clone("h_elPtTriggerRatio")
    h_elPtTriggerRatio.Divide(h_elPtT)
    h_elPtTriggerRatio.SetLineColor(2)
    h_elPtTriggerRatio.Draw('same')
    h_muonPtTriggerRatio = (h_muonPt).Clone("h_muonPtTriggerRatio")
    h_muonPtTriggerRatio.Divide(h_muonPtT)
    h_muonPtTriggerRatio.SetLineColor(4)
    h_muonPtTriggerRatio.Draw('same')
    legg = ROOT.TLegend(0.1, 0.7,0.3, 0.9)
    legg.AddEntry(h_jetPtTriggerRatio, "jet", "l")
    legg.AddEntry(h_elPtTriggerRatio, "electron", "l")
    legg.AddEntry(h_muonPtTriggerRatio, "muon", "l")
    legg.Draw()

    cv = triggerCanvas.cd(3)
    #h_jetPtTrigger.Draw()
    #h_jetPt.Draw('same')
    h_PtTriggerStack.Add(h_jetPt)
    h_jetPt.GetYaxis().SetTitleOffset(1.7)
    h_PtTriggerStack.Add(h_elPt)
    h_PtTriggerStack.Add(h_muonPt)
    h_PtTriggerStack.Add(h_jetPtT)
    h_PtTriggerStack.Add(h_elPtT)
    h_muonPtT.GetYaxis().SetTitleOffset(1.7)
    h_PtTriggerStack.Add(h_muonPtT)
    #h_PtTriggerStack.GetYaxis().SetTitleOffset(1.5)
    h_PtTriggerStack.Draw('nostack')
    h_jetPt.SetStats(False)
    h_jetPtT.SetStats(False)
    h_elPt.SetStats(False)
    h_elPtT.SetStats(False)
    h_muonPt.SetStats(False)
    h_muonPtT.SetStats(False)
    legend = ROOT.TLegend(0.5, 0.5,0.9, 0.9)
    legend.SetNColumns(2)
    #SetLegendFont(50)
    legend.SetHeader("Histograms of P_{T}, with (without) trigger on left (right)", "C")
    en1=legend.AddEntry(h_jetPtT, "jet", "l")
    en1.SetTextFont(50)
    en2=legend.AddEntry(h_jetPt, "jet", "l")
    en1.SetTextFont(50)
    en3=legend.AddEntry(h_elPtT, "electron", "l")
    en1.SetTextFont(50)
    en4=legend.AddEntry(h_elPt, "electron", "l")
    en1.SetTextFont(50)
    en5=legend.AddEntry(h_muonPtT, "muon ", "l")
    en1.SetTextFont(50)
    en6=legend.AddEntry(h_muonPt, "muon ", "l")
    en1.SetTextFont(50)
    legend.Draw()
    triggerCanvas.Print("histCanvas.png")
    histFile.Close()

main()

"""if __name__ == "__main__":
    args = process_arguments()
    if args:
        main(args)"""
