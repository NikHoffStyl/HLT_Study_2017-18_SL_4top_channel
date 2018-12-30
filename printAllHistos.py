import ROOT
import uproot


class PrintAllHistos():
    """ This Module prints all histograms """

    def __init__(self, FileName):
        """ Initialise Global Variables """

        self.fileName = FileName
        self.canvas1 = ROOT.TCanvas('triggerCanvas', 'All Histograms are here', 1100, 700)
        self.canvas1.Divide(2, 2)
        self.h = {}

    def h_print(self):
        """ Save Histograms to pdf file. """

        # histFile = ROOT.TFile.Open(self.fileName)
        histFile = uproot.open(self.fileName)
        branchC = histFile['Events'].keys()
        histFile.cd("Events")
        h = {}
        i = 0
        for leafName in branchC:
            h[leafName] = ROOT.gDirectory.Get(leafName)
            if i == 0:
                self.canvas1.Print("histograms.pdf(", "pdf")
            elif i == len(branchC):
                self.canvas1.Print("histograms.pdf)", "pdf")
            else:
                self.canvas1.Print("histograms.pdf", "pdf")
            i += 1
        print("Histogram file created")
        return True
