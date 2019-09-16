import ROOT
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import numpy
from plotStyle import *
from tools import *

SetPlotStyle()

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)


def rebinHist(hIn):
    """                                                                                                                                                                              
    Args:                                                                                                                                                                            
       hIn: Input histogram
                                                                                                                                   
    Returns:                                                                                                                                                                         
       hOut: Output histogram List                                                                                                                                                   
    """
    muonpT_rebin = numpy.array((0., 20., 30., 35., 40., 50., 75., 300.))
    ht_rebin = numpy.array((0., 500., 750., 1000., 2000., 3000.))

    hName = hIn.GetName()
    if "_HT_" in hName:
        entryBefore = hIn.GetEntries()
        hOut = hIn.Rebin(5, hName, ht_rebin)
        if entryBefore != hOut.GetEntries() : print("ERROR!!!!! Entries not the same after rebining")
        print("HT plot")
        hOut2 = hOut.Clone("hOut2")
        for i in range(0, 6):
            binWidth = hOut2.GetXaxis().GetBinWidth(i)
            binContent = hOut2.GetBinContent(i)
            newBinContent = round(binContent / binWidth)
            hOut2.SetBinContent(i, newBinContent)
    elif "_pt_" in hName:
        hOut = hIn.Rebin(7, hName, muonpT_rebin)
        hOut2 = hOut.Clone("hOut2")
        for i in range(0, 8):
            binWidth = hOut2.GetXaxis().GetBinWidth(i)
            binContent = hOut2.GetBinContent(i)
            newBinContent = round(binContent / binWidth)
            hOut2.SetBinContent(i, newBinContent)
    else:
        hOut = hIn

    return hOut, hOut2

def main():

    parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--inputFile", help="Set name of input file")
    parser.add_argument("-p0", "--histOne", help="Set name of hist one")
    parser.add_argument("-p1", "--histTwo", help="Set name of hist two")
    args = parser.parse_args()

    # Create Canvas                                                                                                                                                                  
    c1 = ROOT.TCanvas('triggerCanvas', 'Triggers', 800, 800)
    c1.SetGrid()

    # Open File                                                                                                                                                                      
    fname = args.inputFile
    f0 = ROOT.TFile.Open(fname)
    # if (not f0) or (f0.IsZombie()):
    #  print("Cannot open " + fname)
    f0.cd("plots")

   # Get Histograms                                                                                                                                                                 
    h1 = ROOT.gDirectory.Get(args.histOne)
    if not h1: 
        print('[ERROR]: No histogram h1 found in ' + fname)
        return -1
    h1, h1p = rebinHist(h1)
    h2 = ROOT.gDirectory.Get(args.histTwo)
    if not h2: 
        print('[ERROR]: No histogram h2 found in ' + fname)
        return -1
    h2, h2p = rebinHist(h2)
    h2p.SetLineColor(2)
    # h1.Sumw2()

    #rp = ROOT.TRatioPlot(h1,h2)

    #c1.SetTicks(0,1)
    # rp.GetLowYaxis().SetNdivisions(505)                                                                                                                                            
    #c1.Update()
    #c1.Draw()
    #rp.Draw()
    

    c1.cd()
    t2 = ROOT.TPaveText(0.16, 0.95, 0.97, 1, "nbNDC")
    t2.SetFillColorAlpha(0, 0.9)
    t2.SetTextSize(0.04)
    if  "El" in args.histOne: channel = "Electron Channel"
    elif "Mu" in args.histOne: channel = "    Muon Channel"
    if "tttt" in fname: t2.AddText("#bf{CMS Internal}          " + channel + "    #sigma(t#bar{t}t#bar{t}) = 9.2 fb (13TeV)")
    elif "ttjets" in fname: t2.AddText("#bf{CMS Internal}           " + channel + "    #sigma(t#bar{t}) = 831 fb (13TeV)")
    ROOT.gStyle.SetLegendTextSize(0.035)

    # Upper plot will be in pad1
    pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
    pad1.SetBottomMargin(0) # Upper and lower plot are joined
    pad1.SetGridx()         # Vertical grid
    pad1.Draw()             # Draw the upper pad: pad1
    pad1.cd()               # pad1 becomes the current pad
    newyTitle = h1p.GetYaxis().GetTitle()
    newyTitle = newyTitle.replace("per GeVc^{-1}", "per GeV")
    newxTitle = h1p.GetYaxis().GetTitle()
    newxTitle = newxTitle.replace("/ GeVc^{-1}", " [GeV]")
    h1p.SetTitle(";{0};{1}".format(newxTitle, newyTitle))
    # h1.SetTitle(";{0};{1}".format(newxTitle, newyTitle))
    maxYs = getMaxY([h1p, h2p])
    h1p.Draw("hist")               # Draw h1
    h2p.Draw("hist same")         # Draw h2 on top of h1
    legd = ROOT.TLegend(0.7, 0.7, 0.95, 0.95)
    legd.AddEntry(h1p, "HLT SF(HT)" , "l")
    legd.AddEntry(h2p, "HLT SF(pt)" , "l")
    legd.SetHeader("#bf{Weighted by:}", "C")
    t2.Draw("same")
    legd.Draw("same")

    # Do not draw the Y axis label on the upper plot and redraw a small
    # axis instead, in order to avoid the first label (0) to be clipped
    h1p.GetYaxis().SetLabelSize(22)
    h1p.GetYaxis().SetLabelFont(43)
    h1p.SetMinimum(0.1)
    h1p.SetMaximum(1.1 * maxYs)
    #axis = ROOT.TGaxis( 0, 0, 0, 260, 1,253,510,"")
    #axis = ROOT.TGaxis( 0, 0, 0, 3000, 1,2700,510,"")
    #axis = ROOT.TGaxis( 0, 0, 0, 600, 1,570,510,"")
    #axis = ROOT.TGaxis( 0, 0, 0, 120, 1,120,510,"")
    #axis.SetLabelFont(43) # Absolute font size in pixel (precision 3)
    #axis.SetLabelSize(15)
    #axis.Draw()

    # lower plot will be in pad
    c1.cd()          # Go back to the main canvas before defining pad2
    pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
    pad2.SetTopMargin(0)
    pad2.SetBottomMargin(0.3)
    pad2.SetGridx() # vertical grid
    pad2.Draw()
    pad2.cd()       # pad2 becomes the current pad

    SetPlotStyle()

    # Define the ratio plot
    h3 = h1.Clone("h3")
    h3.SetLineColor(ROOT.kBlack)
    h3.SetMinimum(0.65)  # Define Y ..
    h3.SetMaximum(1.35) # .. range
    h3.Sumw2()
    h3.Divide(h2)
    h3.SetMarkerStyle(21)
    h3.Draw("ep")       # Draw the ratio plot

    # h1 settings
    h1p.SetLineColor(ROOT.kBlue+1)
    h1p.SetLineWidth(2)

    # Y axis h1 plot settings
    h1p.GetYaxis().SetTitleSize(24)
    #newyTitle = h1p.GetYaxis().GetTitle()
    #newyTitle.replace("Vc^{-1}", "V")
    #h1p.GetYaxis().SetTitle(newyTitle)
    h1p.GetYaxis().SetTitleFont(43)
    h1p.GetYaxis().SetTitleOffset(1.7)

    # h2 settings
    h2p.SetLineColor(ROOT.kRed)
    h2p.SetLineWidth(2)

    # Ratio plot (h3) settings
    h3.SetTitle("") # Remove the ratio title

    # Y axis ratio plot settings
    newxTitle = h3.GetXaxis().GetTitle()
    newxTitle = newxTitle.replace("/ GeVc^{-1}", " [GeV]")
    if  "El" in args.histOne: newxTitle = newxTitle.replace("Lepton", "Electron")
    elif  "Mu" in args.histOne: newxTitle = newxTitle.replace("Lepton", "Muon")
    h3.GetXaxis().SetTitle(newxTitle)
    h3.GetYaxis().SetTitle("ratio")
    h3.GetYaxis().SetNdivisions(505)
    h3.GetYaxis().SetTitleSize(24)
    h3.GetYaxis().SetTitleFont(43)
    h3.GetYaxis().SetTitleOffset(1.7)
    h3.GetYaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
    h3.GetYaxis().SetLabelSize(22)

    # X axis ratio plot settings
    h3.GetXaxis().SetTitleSize(24)
    h3.GetXaxis().SetTitleFont(43)
    h3.GetXaxis().SetTitleOffset(4.2)
    h3.GetXaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
    h3.GetXaxis().SetLabelSize(22)

    c1.Print("mcWeightedPlots.png", "png")


if __name__ == '__main__':
    main()
