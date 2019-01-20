import ROOT
from DrawTools import DrawTools
from ROOT import TLatex
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from PdfCreator import pdfCreator


def process_arguments():
    """ Process command-line arguments """

    parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--inputLFN", choices=["ttjets", "tttt", "tttt_weights", "wjets"],
                        default="tttt", help="Set list of input files")
    args = parser.parse_args()
    return args


def main(argms):
    """ This code merges histograms, only for specific root file """

    if argms.inputLFN == "ttjets":
        inputFile = "../OutFiles/Histograms/TT6jets2.root"
    elif argms.inputLFN == "tttt_weights":
        inputFile = "../OutFiles/Histograms/TTTTweights.root"
    elif argms.inputLFN == "wjets":
        inputFile = "../OutFiles/Histograms/Wjets.root"
    elif argms.inputLFN == "tttt":
        inputFile = "../OutFiles/Histograms/TTTT_6jets2.root"
    else:
        return 0

    # - Create canvases
    triggerCanvas = ROOT.TCanvas('triggerCanvas', 'Triggers', 1100, 600)
    # triggerCanvas.Divide(2,1)

    # - Open file and sub folder
    histFile = ROOT.TFile.Open(inputFile)
    histFile.cd("plots")

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

    # - HT plots ---------------------------------
    h_jetHT = DrawTools.GetHistList("h_jetHT")
    DrawTools.drawSame(1, h_jetHT)
    DrawTools.histDivision(2, h_jetHT)

    # - Jet Multiplicity plots ---------------------------------
    h_jetMult = DrawTools.GetHistList("h_jetMult")
    DrawTools.drawSame(3, h_jetMult)
    DrawTools.histDivision(4, h_jetMult)

    # - B tagged Jet Multiplicity plots ---------------------------
    h_jetBMult = DrawTools.GetHistList("h_jetBMult")
    DrawTools.drawSame(5, h_jetBMult)
    DrawTools.histDivision(6, h_jetBMult)

    # - Muon pT plots ---------------------------------
    h_muonPt = DrawTools.GetHistList("h_muonPt")
    DrawTools.drawSame(7, h_muonPt)
    DrawTools.histDivision(7, h_muonPt)

    # - Electron pT plots ---------------------------------
    h_elPt = DrawTools.GetHistList("h_elPt")
    DrawTools.drawSame(8, h_elPt)
    DrawTools.histDivision(9, h_elPt)

    # - MET pT plots ---------------------------------
    h_metPt = DrawTools.GetHistList("h_metPt")
    DrawTools.drawSame(10, h_metPt)
    DrawTools.histDivision(11, h_metPt)

    # - GenMET pT plots ---------------------------------
    h_genMetPt = DrawTools.GetHistList("h_genMetPt")
    DrawTools.drawSame(12, h_genMetPt)
    DrawTools.histDivision(13, h_genMetPt)

    # - Eta plots ------------------------------------------
    h_jetEta = DrawTools.GetHistList("h_jetEta")
    DrawTools.drawSame(14, h_jetEta)

    h_muonEta = DrawTools.GetHistList("h_muonEta")
    DrawTools.drawSame(15, h_muonEta)

    h_elEta = DrawTools.GetHistList("h_elEta")
    DrawTools.drawSame(16, h_elEta)

    # - Phi plots ------------------------------------------
    h_jetPhi = DrawTools.GetHistList("h_jetPhi")
    DrawTools.drawSame(17, h_jetPhi)

    h_muonPhi = DrawTools.GetHistList("h_muonPhi")
    DrawTools.drawSame(18, h_muonPhi)

    h_elPhi = DrawTools.GetHistList("h_elPhi")
    DrawTools.drawSame(19, h_elPhi)

    # - Eta-Phi Map plots ------------------------------------------
    h_jetMap = DrawTools.GetHistList("h_jetMap")
    DrawTools.drawSame(18, h_jetMap, option="COLZ")

    h_muonMap = DrawTools.GetHistList("h_muonMap")
    DrawTools.drawSame(20, h_muonMap, option="COLZ")

    h_elMap = DrawTools.GetHistList("h_elMap")
    DrawTools.drawSame(21, h_elMap, option="COLZ")

    # - Test Event numbers along steps ----------
    DrawTools.stepHist()
    histFile.Close()


main(process_arguments())
