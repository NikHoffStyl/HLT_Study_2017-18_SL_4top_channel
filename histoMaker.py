from __future__ import (division, print_function)

import ROOT
from ROOT import TLatex
from importlib import import_module

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
#from argProcessor import process_arguments as args

class HistogramMaker(Module):
    """ This class HistogramMaker() does as the name suggests. """

    def __init__(self):
        """ Initialise global variables """

        self.writeHistFile=True #Necessary for an output file to be created?
        self.counter = 0 #Define this global variable to count events
        self.EventLimit = -1 # 100000 -1 for no limit of events fully processed
        self.trigList={"HT": ['PFHT180', 'PFHT250', 'PFHT370', 'PFHT430','PFHT510',
                       'PFHT590', 'PFHT680', 'PFHT780', 'PFHT890', 'PFHT1050',
                       'PFHT380_SixPFJet32', 'PFHT430_SixPFJet40',
                       'PFHT380_SixPFJet32_DoublePFBTagCSV_2p2',
                       'PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2',
                       'PFHT430_SixPFJet40_PFBTagCSV_1p5'],
                       "Mu":['Mu17_TrkIsoVVL', 'Mu19_TrkIsoVVL', 'IsoMu24']
                       }
        self.triggerPath1 ='PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2'#args().triggerpath1
        self.triggerPath1_1='PFHT380_SixPFJet32_DoublePFBTagCSV_2p2'
        self.triggerPath1_2='PFHT430_SixPFJet40_PFBTagCSV_1p5'
        self.triggerPath2 = 'IsoMu24'#args().triggerpath2
        self.trigCombination1 = [self.triggerPath1, self.triggerPath2]
        self.trigCombination2 = [self.triggerPath1_1, self.triggerPath2]
        self.trigCombination3 = [self.triggerPath1_2, self.triggerPath2]

    def beginJob(self,histFile=None,histDirName=None):
        """ Initialise histograms to be used and saved in output file. """

        # - Run beginJob() of Module
        Module.beginJob(self,histFile,histDirName) #pass histFile and histDirName first passed to the PostProcessor

        # - Defining Jet HT histograms to be saved to file
        self.h_jetHt = {}
        self.h_jetHt['no_trigger'] = ROOT.TH1D('h_jetHt_notrigger', ';H_{T};Events', 200, 0, 2300)
        self.addObject(self.h_jetHt['no_trigger'])
        self.h_jetHt[self.triggerPath1] = ROOT.TH1D('h_jetHt_' + self.triggerPath1,
                                                    self.triggerPath1 + ';H_{T};Events', 200, 0, 2300)
        self.addObject(self.h_jetHt[self.triggerPath1])
        self.h_jetHt[self.triggerPath1_1] = ROOT.TH1D('h_jetHt_' + self.triggerPath1_1,
                                                    self.triggerPath1_1 + ';H_{T};Events', 200, 0, 2300)
        self.addObject(self.h_jetHt[self.triggerPath1_1])
        self.h_jetHt[self.triggerPath1_2] = ROOT.TH1D('h_jetHt_' + self.triggerPath1_2,
                                                    self.triggerPath1_2 + ';H_{T};Events', 200, 0, 2300)
        self.addObject(self.h_jetHt[self.triggerPath1_2])
        self.h_jetHt[self.triggerPath2] = ROOT.TH1D('h_jetHt_' + self.triggerPath2,
                                                     self.triggerPath2 + ';H_{T};Events', 200, 0, 2300)
        self.addObject(self.h_jetHt[self.triggerPath2])
        self.h_jetHt['combination1'] = ROOT.TH1D('h_jetHt_combination1', self.triggerPath1 + 'and' + self.triggerPath2 +
                                             ';H_{T};Events', 200, 0, 2300)
        self.addObject(self.h_jetHt['combination1'])
        self.h_jetHt['combination2'] = ROOT.TH1D('h_jetHt_combination2', self.triggerPath1_1 + 'and' + self.triggerPath2 +
                                             ';H_{T};Events', 200, 0, 2300)
        self.addObject(self.h_jetHt['combination2'])
        self.h_jetHt['combination3'] = ROOT.TH1D('h_jetHt_combination3', self.triggerPath1_2 + 'and' + self.triggerPath2 +
                                             ';H_{T};Events', 200, 0, 2300)
        self.addObject(self.h_jetHt['combination3'])

        # - Defining Muon pT histograms to be saved to file
        self.h_muonPt = {}
        self.h_muonPt['no_trigger'] = ROOT.TH1D('h_muonPt_notrigger', ';Muon P_{T};Events', 200, 0, 170)
        self.addObject(self.h_muonPt['no_trigger'])
        self.h_muonPt[self.triggerPath1] = ROOT.TH1D('h_muonPt_' + self.triggerPath1,
                                                     self.triggerPath1 + ';Muon P_{T};Events', 200, 0, 170)
        self.addObject(self.h_muonPt[self.triggerPath1])
        self.h_muonPt[self.triggerPath1_1] = ROOT.TH1D('h_muonPt_' + self.triggerPath1_1,
                                                     self.triggerPath1_1 + ';Muon P_{T};Events', 200, 0, 170)
        self.addObject(self.h_muonPt[self.triggerPath1_1])
        self.h_muonPt[self.triggerPath1_2] = ROOT.TH1D('h_muonPt_' + self.triggerPath1_2,
                                                     self.triggerPath1_2 + ';Muon P_{T};Events', 200, 0, 170)
        self.addObject(self.h_muonPt[self.triggerPath1_2])
        self.h_muonPt[self.triggerPath2] = ROOT.TH1D('h_muonPt_' + self.triggerPath2,
                                                      self.triggerPath2 + ';Muon P_{T};Events', 200, 0, 170)
        self.addObject(self.h_muonPt[self.triggerPath2])
        self.h_muonPt['combination1'] = ROOT.TH1D('h_muonPt_combination1', self.triggerPath1 + 'and' + self.triggerPath2 +
                                              ';Muon P_{T};Events', 200, 0, 170)
        self.addObject(self.h_muonPt['combination1'])
        self.h_muonPt['combination2'] = ROOT.TH1D('h_muonPt_combination2', self.triggerPath1_1 + 'and' + self.triggerPath2 +
                                              ';Muon P_{T};Events', 200, 0, 170)
        self.addObject(self.h_muonPt['combination2'])
        self.h_muonPt['combination3'] = ROOT.TH1D('h_muonPt_combination3', self.triggerPath1_2 + 'and' + self.triggerPath2 +
                                              ';Muon P_{T};Events', 200, 0, 170)
        self.addObject(self.h_muonPt['combination3'])

        # - FIXME: May be a better way.
        self.h_eventsPrg = ROOT.TH1D('h_eventsPrg', ';steps;entries', 10,0,10)
        self.addObject(self.h_eventsPrg)

    def analyze(self, event):
        """ process event, return True (go to next module) or False (fail, go to next event) """

        self.counter += 1
        self.h_eventsPrg.Fill(0)

        # - 'Halt' execution for events past the first N (20 when written) by returning False
        if self.counter > self.EventLimit > -1:
            return False

        ###########################################
        ###### Basic Attributes of the Event ######
        ###########################################
        #Use basic python getattr() method to grab this info, no need for Object or Collection here
        #run = getattr(event, "run")
        #lumi = getattr(event, "luminosityBlock")
        #evt = getattr(event, "event")
        
        #print("\n\nRun: {0:>8d} \tLuminosityBlock: {1:>8d} \tEvent: {2:>8d}".format(run,lumi,evt))
        #eventSum = ROOT.TLorentzVector()

        ###########################################
        ###### Event Collections and Objects ######
        ###########################################
        # - Collections:
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        HLTObj = Object(event, "HLT") #object with only the trigger branches in that event
        trigPath={}
        for key in self.trigList:
            for tg in self.trigList[key]:
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

        jetHT={"t1":0, "t1_1":0, "t1_2":0, "t2":0, "comb1":0, "comb2":0, "comb3":0, "notrig":0}
        nJetPass =0
        nBtagPass = 0
        firstMuonPass = False

        #if self.counter<5:print("\n{0:>5s} {1:>5s} {2:>10s} {3:>10s} {4:>10s}"
         #                       .format("Jet", "jetId","Pt", "Eta", "Phi"))
        for nj, jet in enumerate(jets):
            # # - Check jet passes 2017 Tight Jet ID https://twiki.cern.ch/twiki/bin/view/CMS/JetID13TeVRun2017
            # # - Minimum 30GeV Pt on the jets
            # # - Only look at jets within |eta| < 2.4
            if jet.jetId<2 or jet.pt<30 or jet.eta>2.4 :continue
            else:nJetPass +=1

            if jet.btagDeepFlavB > 0.7489: nBtagPass +=1
            #Count b-tagged jets with two algos at the medium working point
            #https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation94X
            #if jet.btagCSVV2 < 0.8838: continue # tight = 0.9693
            #if jet.btagDeepB < 0.4941: continue # no tight
            #if jet.btagDeepC < 0.4941: continue # tight = 0.8001
            #if jet.btagDeepFlavB < 0.7489: continue # no tight
            if trigPath[self.triggerPath1]: jetHT["t1"] += jet.pt
            if trigPath[self.triggerPath1]: jetHT["t1_1"] += jet.pt
            if trigPath[self.triggerPath1]: jetHT["t1_2"] += jet.pt
            if trigPath[self.triggerPath2]: jetHT["t2"] += jet.pt
            if passComb1:
                jetHT["comb1"] += jet.pt
            if passComb2:
                jetHT["comb2"] += jet.pt
            if passComb3:
                jetHT["comb3"] += jet.pt
                #if self.counter<5:print("{0:*<5d} {1:*<5d} {2:>10.4f} {3:>+10.3f} {4:>+10.3f} (No triggers)"
                 #                       .format(nj+1, jet.jetId, jet.pt, jet.eta, jet.phi))
            jetHT["notrig"] += jet.pt
            #if self.counter<5:print("{0:*<5d} {1:*<5d} {2:>10.4f} {3:>+10.3f} {4:>+10.3f}"
            #                        .format(nj+1, jet.jetId, jet.pt, jet.eta, jet.phi))

        if nJetPass >4 and nBtagPass >0:
            self.h_eventsPrg.Fill(1)
            if trigPath[self.triggerPath1]:self.h_eventsPrg.Fill(2)
            if trigPath[self.triggerPath1_1]:self.h_eventsPrg.Fill(3)
            if trigPath[self.triggerPath1_2]:self.h_eventsPrg.Fill(4)
            if trigPath[self.triggerPath2]:self.h_eventsPrg.Fill(5)
            if passComb1: self.h_eventsPrg.Fill(6)
            if passComb2: self.h_eventsPrg.Fill(7)
            if passComb3: self.h_eventsPrg.Fill(8)

        #if self.counter<5:print("\n{0:>5s} {1:>5s} {2:>6s} {3:>7s} {4:>6s} {5:>10s} {6:>10s} {7:>10s}"
         #                       .format("Muon", "pdgId","softId","tightId","jetIdx", "Pt", "Eta", "Phi"))
        for nm, muon in enumerate(muons) :
            # - TODO: Add correct identification cuts for muons(or electrons).
            if nm == 0:
                if (getattr(muon, "tightId") == False) or abs(muon.eta) > 2.4 or muon.miniPFRelIso_all > 0.15:
                    continue
                else:firstMuonPass=True

            if nm ==0 and nJetPass >4 and firstMuonPass == True and nBtagPass >0:
                if trigPath[self.triggerPath1]:
                    self.h_muonPt[self.triggerPath1].Fill(muon.pt)
                if trigPath[self.triggerPath1_1]:
                    self.h_muonPt[self.triggerPath1_1].Fill(muon.pt)
                if trigPath[self.triggerPath1_2]:
                    self.h_muonPt[self.triggerPath1_2].Fill(muon.pt)
                if trigPath[self.triggerPath2]:
                    self.h_muonPt[self.triggerPath2].Fill(muon.pt)
                if passComb1:
                    self.h_muonPt['combination1'].Fill(muon.pt)
                if passComb2:
                    self.h_muonPt['combination2'].Fill(muon.pt)
                if passComb3:
                    self.h_muonPt['combination3'].Fill(muon.pt)
                self.h_muonPt['no_trigger'].Fill(muon.pt)
            #if self.counter<5 and passComb1:print("{0:*<5d} {1:*<5d} {2:*<6d} {3:*<7d} {4:*<6d} {5:>10.4f} "
             #                                    "{6:>+10.3f} {7:>+10.3f}"
              #                                   .format(nm+1, muon.pdgId, muon.softId, muon.tightId, muon.jetIdx,
               #                                          muon.pt, muon.eta, muon.phi))
            #if self.counter<5:print("{0:*<5d} {1:*<5d} {2:*<6d} {3:*<7d} {4:*<6d} {5:>10.4f} {6:>+10.3f} "
             #                      "{7:>+10.3f} (No triggers)"
              #                     .format(nm+1, muon.pdgId, muon.softId, muon.tightId, muon.jetIdx, muon.pt,
               #                           muon.pdgId, muon.eta, muon.phi))
        if nJetPass >4 and firstMuonPass==True and nBtagPass >0:
            self.h_eventsPrg.Fill(1)
            if trigPath[self.triggerPath1]:
                self.h_jetHt[self.triggerPath1].Fill(jetHT["t1"])
            if trigPath[self.triggerPath1_1]:
                self.h_jetHt[self.triggerPath1_1].Fill(jetHT["t1_1"])
            if trigPath[self.triggerPath1_2]:
                self.h_jetHt[self.triggerPath1_2].Fill(jetHT["t1_2"])
            if trigPath[self.triggerPath2]:
                self.h_jetHt[self.triggerPath2].Fill(jetHT["t2"])
            if passComb1:
                self.h_jetHt['combination1'].Fill(jetHT["comb1"])
            if passComb2:
                self.h_jetHt['combination2'].Fill(jetHT["comb2"])
            if passComb3:
                self.h_jetHt['combination3'].Fill(jetHT["comb3"])
            self.h_jetHt['no_trigger'].Fill(jetHT["notrig"])
        
        return True
