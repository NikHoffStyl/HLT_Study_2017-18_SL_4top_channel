from __future__ import (division, print_function)

import ROOT
from ROOT import TLatex
from importlib import import_module
import time

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class HistogramMaker(Module):
    """ This class HistogramMaker() does as the name suggests. """

    def __init__(self):
        """ Initialise global variables """

        self.writeHistFile=True #Necessary for an output file to be created?
        self.counter = 0 #Define this global variable to count events
        self.EventLimit = -1 # 100000 -1 for no limit of events fully processed
        self.trigList={"HT": ['PFHT180', 'PFHT250', 'PFHT370', 'PFHT430','PFHT510',
                       'PFHT590', 'PFHT680', 'PFHT780', 'PFHT890', 'PFHT1050',
                       'HLT_PFHT380_SixPFJet32', 'HLT_PFHT430_SixPFJet40',
                       'HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2',
                       'HLT_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2',
                       'HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5']
                       "Mu":['Mu17_TrkIsoVVL', 'Mu19_TrkIsoVVL', 'IsoMu24',]
                       }
        self.triggerPath1 = 'PFHT380_SixPFJet32_DoublePFBTagCSV_2p2'
        self.triggerParth2 = 'IsoMu24'
        self.trigCombination1 = [triggerPath1, triggerParth2]

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
        self.h_jetHt[self.triggerParth2] = ROOT.TH1D('h_jetHt_' + self.triggerParth2,
                                                     self.triggerParth2 + ';H_{T};Events', 200, 0, 2300)
        self.addObject(self.h_jetHt[self.triggerParth2])
        self.h_jetHt['combined'] = ROOT.TH1D('h_jetHt_combined', self.triggerPath1 + 'and' + self.triggerParth2 +
                                             ';H_{T};Events', 200, 0, 2300)
        self.addObject(self.h_jetHt['combined'])

        # - Defining Muon pT histograms to be saved to file
        self.h_muonPt = {}
        self.h_muonPt['no_trigger'] = ROOT.TH1D('h_muonPt_notrigger', ';Muon P_{T};Events', 200, 0, 170)
        self.addObject(self.h_muonPt['no_trigger'])
        self.h_muonPt[self.triggerPath1] = ROOT.TH1D('h_muonPt_' + self.triggerPath1,
                                                     self.triggerPath1 + ';Muon P_{T};Events', 200, 0, 170)
        self.addObject(self.h_muonPt[self.triggerPath1])
        self.h_muonPt[self.triggerParth2] = ROOT.TH1D('h_muonPt_' + self.triggerParth2,
                                                      self.triggerParth2 + ';Muon P_{T};Events', 200, 0, 170)
        self.addObject(self.h_muonPt[self.triggerParth2])
        self.h_muonPt['combined'] = ROOT.TH1D('h_muonPt_combined', self.triggerPath1 + 'and' + self.triggerParth2 +
                                              ';Muon P_{T};Events', 200, 0, 170)
        self.addObject(self.h_muonPt['combined'])

        # - FIXME: May be a better way.
        self.h_eventsPrg = ROOT.TH1D('h_eventsPrg', ';steps;entries', 5,0,5)
        self.addObject(self.h_eventsPrg)

    def analyze(self, event):
        """ process event, return True (go to next module) or False (fail, go to next event) """

        self.counter += 1
        self.h_eventsPrg.Fill(1)

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
        for key, tg in self.trigList.items():
            if getattr(HLTObj,tg):
                trigPath[tg] = getattr(HLTObj,tg)
            else: print(" ERROR: There is no such attribute. ")

        passAny = False
        for trig in self.trigCombination1:
            if trigPath[trig]:
                passAny = True

        jetHT_withT1=0
        jetHT_withT2=0
        jetHT_withT3=0
        jetHT_withoutT=0

        # - TODO: Add correct identification cuts for muons(or electrons).
        
        if self.counter<5:print("\n{0:>5s} {1:>5s} {2:>10s} {3:>10s} {4:>10s}"
                                .format("Jet", "jetId","Pt", "Eta", "Phi"))
        for nj, jet in enumerate(jets):
            # - Check jet passes 2017 Tight Jet ID https://twiki.cern.ch/twiki/bin/view/CMS/JetID13TeVRun2017
            if jet.jetId < 2:
                continue
            # - Minimum 30GeV Pt on the jets
            if jet.pt < 30:
                continue
            # - Only look at jets within |eta| < 2.4
            if abs(jet.eta) > 2.4:
                continue
                       
            if trigPath[self.triggerPath1]:
                jetHT_withT1 += jet.pt
            if trigPath[self.triggerParth2]:
                jetHT_withT2 += jet.pt
            if passAny:
                jetHT_withT3 += jet.pt
                if self.counter<5:print("{0:*<5d} {1:*<5d} {2:>10.4f} {3:>+10.3f} {4:>+10.3f} (No triggers)"
                                        .format(nj+1, jet.jetId, jet.pt, jet.eta, jet.phi))
            jetHT_withoutT += jet.pt
            if self.counter<5:print("{0:*<5d} {1:*<5d} {2:>10.4f} {3:>+10.3f} {4:>+10.3f}"
                                    .format(nj+1, jet.jetId, jet.pt, jet.eta, jet.phi))
            
        self.h_eventsPrg.Fill(2)
        if passAny: self.h_eventsPrg.Fill(3)

        if self.counter<5:print("\n{0:>5s} {1:>5s} {2:>6s} {3:>7s} {4:>6s} {5:>10s} {6:>10s} {7:>10s}"
                                .format("Muon", "pdgId","softId","tightId","jetIdx", "Pt", "Eta", "Phi"))
        for nm, muon in enumerate(muons) :
            if nm < 1:
                if trigPath[self.triggerPath1]:
                    self.h_muonPtT1.Fill(muon.pt)
                if trigPath[self.triggerParth2]:
                    self.h_muonPtT2.Fill(muon.pt)
                if passAny:
                    self.h_muonPtT3.Fill(muon.pt)
                self.h_muonPt.Fill(muon.pt)
            if (self.counter<5 and passAny):print("{0:*<5d} {1:*<5d} {2:*<6d} {3:*<7d} {4:*<6d} {5:>10.4f} "
                                                  "{6:>+10.3f} {7:>+10.3f}"
                                                  .format(nm+1, muon.pdgId, muon.softId, muon.tightId, muon.jetIdx,
                                                          muon.pt, muon.eta, muon.phi))
            if self.counter<5:print("{0:*<5d} {1:*<5d} {2:*<6d} {3:*<7d} {4:*<6d} {5:>10.4f} {6:>+10.3f} "
                                    "{7:>+10.3f} (No triggers)"
                                    .format(nm+1, muon.pdgId, muon.softId, muon.tightId, muon.jetIdx, muon.pt,
                                            muon.pdgId, muon.eta, muon.phi))

        if trigPath[self.triggerPath1]:
            self.h_jetHtT1.Fill(jetHT_withT1)
        if trigPath[self.triggerParth2]:
            self.h_jetHtT2.Fill(jetHT_withT2)
        if passAny:
            self.h_jetHtT3.Fill(jetHT_withT3)
        self.h_jetHt.Fill(jetHT_withoutT)
        
        return True

filePrefix = "root://cms-xrd-global.cern.ch/"
files=[]
#Open the text list of files as read-only ("r" option), use as pairs to add proper postfix to output file
#inputList =  open("../Infiles/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8.txt", "r") # tt + jets MC
#thePostFix = "TTJets_SL"
inputList =  open("../NanoAODTools/StandaloneExamples/Infiles/TTTT_TuneCP5_13TeV-amcatnlo-pythia8.txt", "r") # tttt MC
thePostFix = "TTTT"
#inputList =  open("../Infiles/TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8.txt", "r") # tttt MC PSWeights
#thePostFix = "TTTT_PSWeights"
#inputList =  open("../Infiles/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8.txt", "r") # W (to Lep + Nu) + jets
#thePostFix = "WJetsToLNu"

for line in inputList:
    #.replace('\n','') protects against new line characters at end of filenames, use just str(line) if problem appears
    files.append(filePrefix + str(line).replace('\n','') )

"""for file in files:
    print(file)"""
onefile=[files[0]]

p99=PostProcessor(".",
                  #files,
                  onefile,
                  cut="nJet > 5 && ( nMuon >0 || nElectron >0 )",
                  modules=[HistogramMaker()],
                  jsonInput=None,
                  noOut=True,
                  justcount=False,
                  postfix=thePostFix,
                  histFileName="../RWOutput/OutHistoMaker2.root",
                  histDirName="plots",
                  )
t0 = time.clock()
p99.run()
t1 = time.clock()
print("Elapsed time %7.1fs" %(t1-t0))
