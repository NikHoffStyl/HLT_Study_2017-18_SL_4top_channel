from __future__ import (division, print_function)

import ROOT
from ROOT import TLatex
from importlib import import_module

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
#from argProcessor import process_arguments as args

class HistogramMaker(Module):
    """ This class HistogramMaker() does as the name suggests. """

    def __init__(self, WriteHistFile=True,EventLimit = 100000,TrigDict=None,TrigLst = None):
        """ Initialise global variables """

        self.writeHistFile=WriteHistFile
        self.eventCounter = 0
        self.eventLimit = EventLimit # 100000 -1 for no limit of events fully processed
        self.numTriggers = len(TrigLst)

        # - Define Lists
        self.trigCombination = []
        if TrigLst is None: self.trigLst=[]
        else:
            self.trigLst = TrigLst
            for i in range(self.numTriggers -1):
                self.trigCombination[i] = [self.trigLst[i+1], self.trigLst[0]]

        # - Define Dictionaries
        if TrigDict is None: self.trigDict = {}
        else: self.trigDict=TrigDict
        self.h_jetHt = {}
        self.h_muonPt = {}

    def beginJob(self,histFile=None,histDirName=None):
        """ Initialise histograms to be used and saved in output file. """

        # - Run beginJob() of Module
        Module.beginJob(self,histFile,histDirName) #pass histFile and histDirName first passed to the PostProcessor

        # - Defining histograms to be saved to file
        self.h_jetHt['no_trigger'] = ROOT.TH1D('h_jetHt_notrigger', ';H_{T};Events', 200, 1, 2300)
        self.addObject(self.h_jetHt['no_trigger'])
        self.h_muonPt['no_trigger'] = ROOT.TH1D('h_muonPt_notrigger', ';Muon P_{T};Events', 200, 0, 170)
        self.addObject(self.h_muonPt['no_trigger'])
        for trgPath in self.trigLst:
            self.h_jetHt[trgPath] = ROOT.TH1D('h_jetHt_' + trgPath, trgPath + ';H_{T};Events', 200, 1, 2300)
            self.addObject(self.h_jetHt[trgPath])
            self.h_muonPt[trgPath] = ROOT.TH1D('h_muonPt_' + trgPath, trgPath + ';Muon P_{T};Events', 200, 0, 170)
            self.addObject(self.h_muonPt[trgPath])
        for i in range(self.numTriggers -1):
            self.h_jetHt['combination' + str(i+1)] = ROOT.TH1D('h_jetHt_combination' + str(i+1), self.trigLst[i+1] + 'and' + self.trigLst[0] +
                                                     ';H_{T};Events', 200, 1, 2300)
            self.addObject(self.h_jetHt['combination' + str(i+1)])
            self.h_muonPt['combination' + str(i+1)] = ROOT.TH1D('h_muonPt_combination' + str(i+1), self.trigLst[i+1] + 'and' + self.trigLst[0] +
                                                  ';Muon P_{T};Events', 200, 0, 170)
            self.addObject(self.h_muonPt['combination' + str(i+1)])

        # - FIXME: May be a better way.
        self.h_eventsPrg = ROOT.TH1D('h_eventsPrg', ';steps;entries', 11,0,11)
        self.addObject(self.h_eventsPrg)

    def analyze(self, event):
        """ process event, return True (go to next module) or False (fail, go to next event) """

        self.eventCounter += 1
        self.h_eventsPrg.Fill(0)

        # - 'Halt' execution for events past the first N (20 when written) by returning False
        if self.eventCounter > self.eventLimit > -1:
            return False

        ###########################################
        ###### Event Collections and Objects ######
        ###########################################
        # - Collections:
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        HLTObj = Object(event, "HLT") #object with only the trigger branches in that event
        trigPath = {}
        passComb = []
        for key in self.trigDict:
            for tg in self.trigDict[key]:
                trigPath[tg] = getattr(HLTObj,tg)
    
        for i in range(self.numTriggers -1):
            passComb[i] = False
            for trig in self.trigCombination[i]:
                if trigPath[trig]:
                    passComb[i] = True

        jetHT={"notrig":0}
        for i in range(self.numTriggers):
            jetHT.update({("t"+str(i)):0})
            jetHT.update({("comb"+str(i+1)):0})
        nJetPass =0
        nBtagPass = 0
        firstMuonPass = False

        for nj, jet in enumerate(jets):
            # # - Check jet passes 2017 Tight Jet ID https://twiki.cern.ch/twiki/bin/view/CMS/JetID13TeVRun2017
            # # - Minimum 30GeV Pt on the jets
            # # - Only look at jets within |eta| < 2.4
            # - FIXME: Correct identification cuts for jets.
            if jet.jetId<2 or jet.pt<30 or abs(jet.eta)>2.4 :continue
            else:nJetPass +=1

            #Count b-tagged jets with two algos at the medium working point
            #https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation94X
            if jet.btagDeepFlavB > 0.7489: nBtagPass +=1

            # Calculate jetHT for different trigger paths and combinations of them
            if trigPath[self.trigLst[0]]: jetHT["t0"] += jet.pt
            for i in range(self.numTriggers -1):
                if trigPath[self.trigLst[i+1]]: jetHT["t" + str(i+1)] += jet.pt
                if passComb[i]: jetHT["comb" + str(i+1)] += jet.pt
            jetHT["notrig"] += jet.pt

        for nm, muon in enumerate(muons) :
            # - FIXME: Correct identification cuts for muons.
            if nm == 0:
                if (getattr(muon, "tightId") == False) or abs(muon.eta) > 2.4 or muon.miniPFRelIso_all > 0.15:
                    continue
                else:firstMuonPass=True

            if nm ==0 and nJetPass >5 and firstMuonPass == True and nBtagPass >0:
                for i in range(self.numTriggers):
                    if trigPath[self.trigLst[i]]: self.h_muonPt[self.trigLst[i]].Fill(muon.pt)
                    if passComb[i]: self.h_muonPt['combination' + str(i+1)].Fill(muon.pt)
                self.h_muonPt['no_trigger'].Fill(muon.pt)

        if nJetPass >5 and nBtagPass >0:
            self.h_eventsPrg.Fill(1)
            for i in range(self.numTriggers):
                if trigPath[self.trigLst[i]]:self.h_eventsPrg.Fill(2+i)
                if passComb[i]: self.h_eventsPrg.Fill(7+i)

        if nJetPass >5 and firstMuonPass==True and nBtagPass >0:
            for i in range(self.numTriggers):
                if trigPath[self.trigLst[i]]: self.h_jetHt[self.trigLst[i]].Fill(jetHT["t" +str(i)])
                if passComb[i]: self.h_jetHt['combination' + str(i+1)].Fill(jetHT["comb" + str(i+1)])
            self.h_jetHt['no_trigger'].Fill(jetHT["notrig"])
        
        return True
