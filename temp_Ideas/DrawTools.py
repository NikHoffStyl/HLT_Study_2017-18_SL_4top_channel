import ROOT
from PdfCreator import pdfCreator


class DrawTools:
    """ Some additional drawing tools for plotting on same canvas, dividing and plotting contour plots"""

    def __init__(self, argms):
        self.argms = argms
        self.trigList = {"combos": ['IsoMu24_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2'],
                         "stndlone": ['Mu15_IsoVVVL_PFHT450_CaloBTagCSV_4p5'],
                         "t1": ['IsoMu24'],
                         "t2": ['PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2']}
        self.ltx = ROOT.TLatex()

        # - Create text for legend
        if argms.inputLFN == "ttjets":
            self.legString = "#splitline{CMS}{t#bar{t} #rightarrow l #nu_{l} #plus jets}"
        elif argms.inputLFN == "tttt":
            self.legString = "#splitline{CMS}{t#bar{t}t#bar{t} #rightarrow l #nu_{l} #plus jets}"
        elif argms.inputLFN == "tttt_weights":
            self.legString = "#splitline{CMS}{t#bar{t}t#bar{t} #rightarrow l #nu_{l} #plus jets}"
        else:
            self.legString = "#splitline{CMS}{W #rightarrow jets}"

        # - Create canvases
        self.triggerCanvas = ROOT.TCanvas('triggerCanvas', 'Triggers', 1100, 600)
        # self.triggerCanvas.Divide(2,1)
        self.cv = [] * 30

    def GetHistList(self, name=""):
        hist = {"notrigger": ROOT.gDirectory.Get("{0}_notrigger".format(name))}
        hist["notrigger"].SetLineColor(1)
        if not (hist["notrigger"]):
            print("No trigger jet Ht histogram is empty")
        for key in self.trigList:
            for tg in self.trigList[key]:
                hist.update({tg: ROOT.gDirectory.Get("{0}_{1}".format(name, tg))})
        return hist

    def stepHist(self):
        h_eventsPrg = ROOT.gDirectory.Get("h_eventsPrg")
        if not h_eventsPrg:
            print("h_eventsPrg histogram is empty")
            return
        self.triggerCanvas.cd(1)
        h_eventsPrg.SetFillColor(ROOT.kAzure - 9)
        h_eventsPrg.GetXaxis().SetLabelOffset(999)
        h_eventsPrg.GetXaxis().SetLabelSize(0)
        h_eventsPrg.Draw('E1')
        tY1 = 0.05 * (h_eventsPrg.GetMaximum())
        self.ltx.SetTextAngle(88)
        self.ltx.DrawLatex(0.5, tY1, "Pre-selection")
        self.ltx.DrawLatex(1.5, tY1, "Post-selection")
        i = 0
        for key in self.trigList:
            for tg in self.trigList[key]:
                self.ltx.DrawLatex((i + 2.5), tY1, tg)
                i += 1
        # h.GetXAxis().SetBinLabel(binnumber,string)
        pdfCreator(self.argms, 2, self.triggerCanvas)

    def drawSame(self, page, histIn, option="E1"):
        self.cv[page] = self.triggerCanvas.cd(1)
        histIn["notrigger"].Draw(option)
        for key in self.trigList:
            for tg in self.trigList[key]:

                histIn[tg].Draw(option + ' same')
        self.cv[page].BuildLegend(0.4, 0.3, 0.4, 0.3)
        ROOT.gStyle.SetLegendTextSize(0.02)
        tX1 = 0.04 * (histIn["notrigger"].GetXaxis().GetXmax())
        tY1 = 0.95 * (histIn["notrigger"].GetMaximum())
        self.ltx.SetTextSize(0.03)
        self.ltx.DrawLatex(tX1, tY1, self.legString)
        pdfCreator(self.argms, 1, self.triggerCanvas)

    def histDivision(self, page, histIn):
        histOut = {}
        # histIn = {}
        self.cv[page] = self.triggerCanvas.cd(1)
        i = 0
        j = 2
        tX1 = 0
        tY1 = 0
        # for tg in self.trigList["combos"]:
        #     histOut[tg] = (histIn[tg]).Clone("h_jetHtRatio" + tg)
        #     histOut[tg].Divide(histIn["notrigger"])
        #     if i == 0:
        #         histOut[tg].Draw('E1')
        #         tX1 = 0.04 * (histOut[tg].GetXaxis().GetXmax())
        #         tY1 = 0.95 * (histOut[tg].GetMaximum())
        #     if i == 1:
        #         histOut[tg].Draw('E1 same')
        #     i += 1
        # for tg in self.trigList["stndlone"]:
        #     histOut[tg] = (histIn[tg]).Clone("h_jetHtRatio" + tg)
        #     histOut[tg].Divide(histIn["notrigger"])
        #     if i == 0:
        #         histOut[tg].Draw('E1')
        #         tX1 = 0.04 * (histOut[tg].GetXaxis().GetXmax())
        #         tY1 = 0.95 * (histOut[tg].GetMaximum())
        #     if i == 1:
        #         histOut[tg].Draw('E1 same')
        #     i += 1
        for key in self.trigList:
            for tg in self.trigList[key]:
                if ROOT.TEfficiency.CheckConsistency(histIn[tg], histIn["notrigger"]):
                    histOut[tg] = ROOT.TEfficiency(histIn[tg], histIn["notrigger"])
                    xTitle = histIn["notrigger"].GetXaxis().GetTitle()
                    xBinWidth = histIn["notrigger"].GetXaxis().GetBinWidth(1)
                    histOut[tg].SetTitle(";{0};Trigger Efficiency per {1} GeV/c".format(xTitle, xBinWidth))
                    histOut[tg].SetName(tg)
                    histOut[tg].SetLineColor(j)
                    j += 1
                    if i == 0:
                        histOut[tg].Draw()
                        tX1 = 0.04 * (histIn[tg].GetXaxis().GetXmax())
                        tY1 = 0.99
                    if i == 1:
                        histOut[tg].Draw('same')
                    i += 1
        self.cv[page].BuildLegend(0.4, 0.3, 0.4, 0.3)
        ROOT.gStyle.SetLegendTextSize(0.02)
        self.ltx.SetTextSize(0.03)
        self.ltx.DrawLatex(tX1, tY1, self.legString)
        pdfCreator(self.argms, 1, self.triggerCanvas)
