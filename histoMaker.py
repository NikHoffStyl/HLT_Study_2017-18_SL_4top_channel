from __future__ import (division, print_function)

import ROOT
from ROOT import TLatex
from importlib import import_module

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
#from argProcessor import process_arguments as args

class HistogramMaker(Module):
    """ This class HistogramMaker() does as the name suggests. """

    def __init__(self, WriteHistFile=True,EventLimit = -1,TrigLst = None):
        """ Initialise global variables """

        self.eventCounter = 0
        self.comboCounter=0
        self.numTriggers = len(TrigLst["t1"])* len(TrigLst["t2"])+len(TrigLst["stndlone"])
        print("Number of Combined Triggers: %d" %(self.numTriggers))
        self.trigCombination = [""]*self.numTriggers
        self.h_jetHt = {}
        self.h_jetEta = {}
        self.h_jetPhi = {}
        self.h_muonPt = {}
        self.h_muonEta = {}
        self.h_muonPhi = {}


        self.writeHistFile=WriteHistFile
        self.eventLimit = EventLimit # -1 for no limit of events fully processed
        if TrigLst is None: self.trigLst={}
        else:
            self.trigLst = TrigLst
            for t1 in self.trigLst["t1"]:
                for t2 in self.trigLst["t2"]:
                    self.trigCombination[self.comboCounter] = [t1, t2]
                    self.comboCounter+=1



    def beginJob(self,histFile=None,histDirName=None):
        """ Initialise histograms to be used and saved in output file. """

        # - Run beginJob() of Module
        Module.beginJob(self,histFile,histDirName) #pass histFile and histDirName first passed to the PostProcessor

        # - Defining histograms to be saved to file
        self.h_jetHt['no_trigger'] = ROOT.TH1D('h_jetHt_notrigger', ';H_{T};Events', 200, 1, 2300)
        self.addObject(self.h_jetHt['no_trigger'])
        self.h_muonPt['no_trigger'] = ROOT.TH1D('h_muonPt_notrigger', ';Muon P_{T};Events', 200, 0, 170)
        self.addObject(self.h_muonPt['no_trigger'])
        for key in self.trigLst:
            for trgPath in self.trigLst[key]:
                self.h_jetHt[trgPath] = ROOT.TH1D('h_jetHt_' + trgPath, trgPath + ';H_{T};Events', 200, 1, 2300)
                self.addObject(self.h_jetHt[trgPath])
                self.h_jetEta[trgPath] = ROOT.TH1D('h_jetEta_' + trgPath, trgPath + ';Jet #eta;Events', 200, -6, 6)
                self.addObject(self.h_jetEta[trgPath])
                self.h_jetPhi[trgPath] = ROOT.TH1D('h_jetPhi_' + trgPath, trgPath + ';Jet #phi;Events', 200, -6, 6)
                self.addObject(self.h_jetPhi[trgPath])
                self.h_muonPt[trgPath] = ROOT.TH1D('h_muonPt_' + trgPath, trgPath + ';Muon P_{T};Events', 200, 0, 170)
                self.addObject(self.h_muonPt[trgPath])
                self.h_muonEta[trgPath] = ROOT.TH1D('h_muonEta_' + trgPath, trgPath + ';Muon #eta;Events', 200, -6, 6)
                self.addObject(self.h_muonEta[trgPath])
                self.h_muonPhi[trgPath] = ROOT.TH1D('h_muonPhi_' + trgPath, trgPath + ';Muon #phi;Events', 200, -6, 6)
                self.addObject(self.h_muonPhi[trgPath])
        for t1 in self.trigLst["t1"]:
            for t2 in self.trigLst["t2"]:
                self.h_jetHt[t1 +'_'+ t2] = ROOT.TH1D('h_jetHt_combination' + str(self.comboCounter), t1 + 'and' + t2 +
                                                                 ';H_{T};Events', 200, 1, 2300)
                self.addObject(self.h_jetHt[t1 +'_'+ t2])
                self.h_jetEta[t1 +'_'+ t2] = ROOT.TH1D('h_jetEta_combination' + str(self.comboCounter), t1 + 'and' + t2 +
                                                      ';Jet #eta;Events', 200, -6, 6)
                self.addObject(self.h_jetEta[t1 +'_'+ t2])
                self.h_jetPhi[t1 +'_'+ t2] = ROOT.TH1D('h_jetPhi_combination' + str(self.comboCounter), t1 + 'and' + t2 +
                                                      ';Jet #phi;Events', 200, -6, 6)
                self.addObject(self.h_jetPhi[t1 +'_'+ t2])
                self.h_muonPt[t1 +'_'+ t2] = ROOT.TH1D('h_muonPt_combination' + str(self.comboCounter), t1 + 'and' + t2 +
                                                                  ';Muon P_{T};Events', 200, 0, 170)
                self.addObject(self.h_muonPt[t1 +'_'+ t2])
                self.h_muonEta[t1 +'_'+ t2] = ROOT.TH1D('h_muonEta_combination' + str(self.comboCounter), t1 + 'and' + t2 +
                                                       ';Muon #eta;Events', 200, -6, 6)
                self.addObject(self.h_muonEta[t1 +'_'+ t2])
                self.h_muonPhi[t1 +'_'+ t2] = ROOT.TH1D('h_muonPhi_combination' + str(self.comboCounter), t1 + 'and' + t2 +
                                                       ';Muon #phi;Events', 200, -6, 6)
                self.addObject(self.h_muonPhi[t1 +'_'+ t2])

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
        passComb = [0]*self.numTriggers

        for key in self.trigLst:
            for tg in self.trigLst[key]:
                trigPath[tg] = getattr(HLTObj,tg)
    
        for i in range(self.comboCounter):
            passComb[i] = False
            trigPath[self.trigCombination[i][0] + '_' + self.trigCombination[i][1]]=False
            for trig in self.trigCombination[i]:
                if trigPath[trig]:
                    passComb[i] = True
                    trigPath[self.trigCombination[i][0] + '_' + self.trigCombination[i][1]]=True

        #for t1 in self.trigLst["t1"]:
         #   for t2 in self.trigLst["t2"]:
          #      self.trigLst["stndlone"].append(t1 +'_'+ t2) # append new triggers to old list

        jetHT={"notrig":0}
        for key in self.trigLst:
            for tg in self.trigLst[key]:
                jetHT.update({tg:0})

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
            #i=0
            for key in self.trigLst:
                for tg in self.trigLst[key]:
                    if trigPath[tg]:
                        jetHT[tg] += jet.pt
                        self.h_jetEta[tg].Fill(jet.eta)
                        self.h_jetPhi[tg].Fill(jet.phi)
            jetHT["notrig"] += jet.pt

        for nm, muon in enumerate(muons) :
            # - FIXME: Correct identification cuts for muons.
            if nm == 0:
                if (getattr(muon, "tightId") == False) or abs(muon.eta) > 2.4 or muon.miniPFRelIso_all > 0.15:
                    continue
                else:firstMuonPass=True

            if nm ==0 and nJetPass >5 and firstMuonPass == True and nBtagPass >0:
                for key in self.trigLst:
                    for tg in self.trigLst[key]:
                        if trigPath[tg]:
                            self.h_muonPt[tg].Fill(muon.pt)
                            self.h_muonEta[tg].Fill(muon.eta)
                            self.h_muonPhi[tg].Fill(muon.phi)
                self.h_muonPt['no_trigger'].Fill(muon.pt)

        if nJetPass >5 and nBtagPass >0:
            self.h_eventsPrg.Fill(1)
            for key in self.trigLst:
                for tg in self.trigLst[key]:
                    if trigPath[tg]:self.h_eventsPrg.Fill(2+i)
                    #if i>0 and passComb[i-1]: self.h_eventsPrg.Fill(6+i)

        if nJetPass >5 and firstMuonPass==True and nBtagPass >0:
            for key in self.trigLst:
                for tg in self.trigLst[key]:
                    if trigPath[tg]:
                        self.h_jetHt[tg].Fill(jetHT[tg])
                    #if i>0 and passComb[i-1]: self.h_jetHt['combination' + str(i)].Fill(jetHT[tg])
            self.h_jetHt['no_trigger'].Fill(jetHT["notrig"])
        
        return True
