from __future__ import (division, print_function)

import ROOT
from ROOT import TLatex
from importlib import import_module

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
#from argProcessor import process_arguments as args

class HistogramMaker(Module):
    """ This class HistogramMaker() does as the name suggests. """

    def __init__(self, writeHistFile=True,EventLimit = 100000,trigDict=None,trigLst = None):
        """ Initialise global variables """

        self.writeHistFile=writeHistFile #Necessary for an output file to be created?
        self.counter = 0 #Define this global variable to count events
        self.EventLimit = EventLimit # 100000 -1 for no limit of events fully processed
        if trigDict is None: self.trigDict = {}
        else: self.trigDict=trigDict
        if trigLst is None: self.trigLst=[]
        else:
            self.trigLst = trigLst
            self.trigCombination1 = [self.trigLst[1], self.trigLst[0]]
            self.trigCombination2 = [self.trigLst[2], self.trigLst[0]]
            self.trigCombination3 = [self.trigLst[3], self.trigLst[0]]
            self.trigCombination4 = [self.trigLst[4], self.trigLst[0]]
        self.h_jetHt = {}
        self.h_muonPt = {}

    def beginJob(self,histFile=None,histDirName=None):
        """ Initialise histograms to be used and saved in output file. """

        # - Run beginJob() of Module
        Module.beginJob(self,histFile,histDirName) #pass histFile and histDirName first passed to the PostProcessor

        # - Defining Jet HT histograms to be saved to file
        self.h_jetHt['no_trigger'] = ROOT.TH1D('h_jetHt_notrigger', ';H_{T};Events', 200, 0, 2300)
        self.addObject(self.h_jetHt['no_trigger'])
        for trgPath in self.trigLst:
            self.h_jetHt[trgPath] = ROOT.TH1D('h_jetHt_' + trgPath,
                                                          trgPath + ';H_{T};Events', 200, 0, 2300)
            self.addObject(self.h_jetHt[trgPath])
        self.h_jetHt['combination1'] = ROOT.TH1D('h_jetHt_combination1', self.trigLst[1] + 'and' + self.trigLst[0] +
                                             ';H_{T};Events', 200, 0, 2300)
        self.addObject(self.h_jetHt['combination1'])
        self.h_jetHt['combination2'] = ROOT.TH1D('h_jetHt_combination2', self.trigLst[2] + 'and' + self.trigLst[0] +
                                             ';H_{T};Events', 200, 0, 2300)
        self.addObject(self.h_jetHt['combination2'])
        self.h_jetHt['combination3'] = ROOT.TH1D('h_jetHt_combination3', self.trigLst[3] + 'and' + self.trigLst[0] +
                                             ';H_{T};Events', 200, 0, 2300)
        self.addObject(self.h_jetHt['combination3'])
        self.h_jetHt['combination4'] = ROOT.TH1D('h_jetHt_combination4', self.trigLst[4] + 'and' + self.trigLst[0] +
                                                 ';H_{T};Events', 200, 0, 2300)
        self.addObject(self.h_jetHt['combination4'])

        ##
        # - Defining Muon pT histograms to be saved to file
        ##
        self.h_muonPt['no_trigger'] = ROOT.TH1D('h_muonPt_notrigger', ';Muon P_{T};Events', 200, 0, 170)
        self.addObject(self.h_muonPt['no_trigger'])

        for trgPath in self.trigLst:
            self.h_muonPt[trgPath] = ROOT.TH1D('h_muonPt_' + trgPath,
                                                           trgPath + ';Muon P_{T};Events', 200, 0, 170)
            self.addObject(self.h_muonPt[trgPath])
        self.h_muonPt['combination1'] = ROOT.TH1D('h_muonPt_combination1', self.trigLst[1] + 'and' + self.trigLst[0] +
                                              ';Muon P_{T};Events', 200, 0, 170)
        self.addObject(self.h_muonPt['combination1'])
        self.h_muonPt['combination2'] = ROOT.TH1D('h_muonPt_combination2', self.trigLst[2] + 'and' + self.trigLst[0] +
                                              ';Muon P_{T};Events', 200, 0, 170)
        self.addObject(self.h_muonPt['combination2'])
        self.h_muonPt['combination3'] = ROOT.TH1D('h_muonPt_combination3', self.trigLst[3] + 'and' + self.trigLst[0] +
                                              ';Muon P_{T};Events', 200, 0, 170)
        self.addObject(self.h_muonPt['combination3'])
        self.h_muonPt['combination4'] = ROOT.TH1D('h_muonPt_combination4', self.trigLst[4] + 'and' + self.trigLst[0] +
                                                  ';Muon P_{T};Events', 200, 0, 170)
        self.addObject(self.h_muonPt['combination4'])

        # - FIXME: May be a better way.
        self.h_eventsPrg = ROOT.TH1D('h_eventsPrg', ';steps;entries', 11,0,11)
        self.addObject(self.h_eventsPrg)

    def analyze(self, event):
        """ process event, return True (go to next module) or False (fail, go to next event) """

        self.counter += 1
        self.h_eventsPrg.Fill(0)

        # - 'Halt' execution for events past the first N (20 when written) by returning False
        if self.counter > self.EventLimit > -1:
            return False

        ###########################################
        ###### Event Collections and Objects ######
        ###########################################
        # - Collections:
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        HLTObj = Object(event, "HLT") #object with only the trigger branches in that event
        trigPath={}
        for key in self.trigDict:
            for tg in self.trigDict[key]:
                trigPath[tg] = getattr(HLTObj,tg)
    
        passComb1 = False
        for trig in self.trigCombination1:
            if trigPath[trig]:
                passComb1 = True

        passComb2 = False
        for trig in self.trigCombination2:
            if trigPath[trig]:
                passComb2 = True

        passComb3 = False
        for trig in self.trigCombination3:
            if trigPath[trig]:
                passComb3 = True

        passComb4 = False
        for trig in self.trigCombination4:
            if trigPath[trig]:
                passComb4 = True

        jetHT={"t1_1":0, "t1_2":0, "t1_3":0, "t1_4":0, "t2":0, "comb1":0, "comb2":0, "comb3":0, "comb4":0, "notrig":0}
        #for key in self.trigDict: jetHT.update({key:0})
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
            if trigPath[self.trigLst[1]]: jetHT["t1_1"] += jet.pt
            if trigPath[self.trigLst[2]]: jetHT["t1_2"] += jet.pt
            if trigPath[self.trigLst[3]]: jetHT["t1_3"] += jet.pt
            if trigPath[self.trigLst[4]]: jetHT["t1_4"] += jet.pt
            if trigPath[self.trigLst[0]]: jetHT["t2"] += jet.pt
            if passComb1: jetHT["comb1"] += jet.pt
            if passComb2: jetHT["comb2"] += jet.pt
            if passComb3: jetHT["comb3"] += jet.pt
            if passComb4: jetHT["comb4"] += jet.pt
            jetHT["notrig"] += jet.pt

        for nm, muon in enumerate(muons) :
            # - FIXME: Correct identification cuts for muons.
            if nm == 0:
                if (getattr(muon, "tightId") == False) or abs(muon.eta) > 2.4 or muon.miniPFRelIso_all > 0.15:
                    continue
                else:firstMuonPass=True

            if nm ==0 and nJetPass >5 and firstMuonPass == True and nBtagPass >0:
                if trigPath[self.trigLst[1]]: self.h_muonPt[self.trigLst[1]].Fill(muon.pt)
                if trigPath[self.trigLst[2]]: self.h_muonPt[self.trigLst[2]].Fill(muon.pt)
                if trigPath[self.trigLst[3]]: self.h_muonPt[self.trigLst[3]].Fill(muon.pt)
                if trigPath[self.trigLst[4]]: self.h_muonPt[self.trigLst[4]].Fill(muon.pt)
                if trigPath[self.trigLst[0]]: self.h_muonPt[self.trigLst[0]].Fill(muon.pt)
                if passComb1: self.h_muonPt['combination1'].Fill(muon.pt)
                if passComb2: self.h_muonPt['combination2'].Fill(muon.pt)
                if passComb3: self.h_muonPt['combination3'].Fill(muon.pt)
                if passComb4: self.h_muonPt['combination4'].Fill(muon.pt)
                self.h_muonPt['no_trigger'].Fill(muon.pt)

        if nJetPass >5 and nBtagPass >0:
            self.h_eventsPrg.Fill(1)
            if trigPath[self.trigLst[1]]:self.h_eventsPrg.Fill(2)
            if trigPath[self.trigLst[2]]:self.h_eventsPrg.Fill(3)
            if trigPath[self.trigLst[3]]:self.h_eventsPrg.Fill(4)
            if trigPath[self.trigLst[4]]:self.h_eventsPrg.Fill(5)
            if trigPath[self.trigLst[0]]:self.h_eventsPrg.Fill(6)
            if passComb1: self.h_eventsPrg.Fill(7)
            if passComb2: self.h_eventsPrg.Fill(8)
            if passComb3: self.h_eventsPrg.Fill(9)
            if passComb4: self.h_eventsPrg.Fill(10)

        if nJetPass >5 and firstMuonPass==True and nBtagPass >0:
            if trigPath[self.trigLst[1]]: self.h_jetHt[self.trigLst[1]].Fill(jetHT["t1_1"])
            if trigPath[self.trigLst[2]]: self.h_jetHt[self.trigLst[2]].Fill(jetHT["t1_2"])
            if trigPath[self.trigLst[3]]: self.h_jetHt[self.trigLst[3]].Fill(jetHT["t1_3"])
            if trigPath[self.trigLst[4]]: self.h_jetHt[self.trigLst[4]].Fill(jetHT["t1_4"])
            if trigPath[self.trigLst[0]]: self.h_jetHt[self.trigLst[0]].Fill(jetHT["t2"])
            if passComb1: self.h_jetHt['combination1'].Fill(jetHT["comb1"])
            if passComb2: self.h_jetHt['combination2'].Fill(jetHT["comb2"])
            if passComb3: self.h_jetHt['combination3'].Fill(jetHT["comb3"])
            if passComb4: self.h_jetHt['combination4'].Fill(jetHT["comb4"])
            self.h_jetHt['no_trigger'].Fill(jetHT["notrig"])
        
        return True
