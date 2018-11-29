from __future__ import (division, print_function)

import ROOT
from ROOT import TLatex
from importlib import import_module
import time

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class HistogramMaker(Module):
    def __init__(self):
        self.writeHistFile=True #Necessary for an output file to be created?
        self.counter = 0 #Define this global variable to count events
        self.EventLimit = -1 # 100000 -1 for no limit, anything larger chosen here will be the limit of events fully processed
        self.trigList=['PFHT180', 'PFHT250', 'PFHT370', 'PFHT430', 'PFHT510', 'PFHT590', 'PFHT680', 'PFHT780', 'PFHT890', 'PFHT1050','Mu17_TrkIsoVVL', 'Mu19_TrkIsoVVL','IsoMu24']
        """
        file=open("HLTNmaes.txt")
        for line in file:
            fields = line.split(",")
            trigerName = fields[0]
        """

    def beginJob(self,histFile=None,histDirName=None):
        #typically where histograms should be initialized
        #So we call the default Module's beginJob, passing it the histFile and histDirName first passed to the PostProcessor
        Module.beginJob(self,histFile,histDirName)

        #The histogram is 'booked' with the service that will write everything to the output file via self.addObject()
        self.h_jetHt = ROOT.TH1D('h_jetHt', ';H_{T};Events', 200, 0, 2300)
        self.addObject(self.h_jetHt)
        self.h_jetHtT1 = ROOT.TH1D('h_jetHtT1', 'IsoMu24;H_{T};Events', 200, 0, 2300)
        self.addObject(self.h_jetHtT1)
        self.h_jetHtT2 = ROOT.TH1D('h_jetHtT2', 'Mu50;H_{T};Events', 200, 0, 2300)
        self.addObject(self.h_jetHtT2)
        self.h_jetHtT3 = ROOT.TH1D('h_jetHtT3', 'IsoMu24 and Mu50;H_{T};Events', 200, 0, 2300)
        self.addObject(self.h_jetHtT3)

        self.h_eventsPrg = ROOT.TH1D('h_eventsPrg', ';steps;entries', 5,0,5)
        self.addObject(self.h_eventsPrg)

        """self.h_elPt = ROOT.TH1D('h_elPt', ';Electron P_{T} ;Events', 200, 0, 300)
        self.addObject(self.h_elPt)
        self.h_elPtT1 = ROOT.TH1D('h_elPtT1', 'IsoMu24;Electron P_{T};Events', 200, 0, 300)
        self.addObject(self.h_elPtT1)
        self.h_elPtT2 = ROOT.TH1D('h_elPtT2', 'Mu50;Electron P_{T};Events', 200, 0, 300)
        self.addObject(self.h_elPtT2)
        self.h_elPtT3 = ROOT.TH1D('h_elPtT3', 'IsoMu24 and Mu50;Electron P_{T};Events', 200, 0, 300)
        self.addObject(self.h_elPtT3)"""

        self.h_muonPt = ROOT.TH1D('h_muonPt', ';Muon P_{T};Events', 200, 0, 170)
        self.addObject(self.h_muonPt)
        self.h_muonPtT1 = ROOT.TH1D('h_muonPtT1', 'IsoMu24;Muon P_{T};Events', 200, 0, 170)
        self.addObject(self.h_muonPtT1)
        self.h_muonPtT2 = ROOT.TH1D('h_muonPtT2', 'Mu50;Muon P_{T};Events', 200, 0, 170)
        self.addObject(self.h_muonPtT2)
        self.h_muonPtT3 = ROOT.TH1D('h_muonPtT3', 'IsoMu24 and Mu50;Muon P_{T};Events', 200, 0, 170)
        self.addObject(self.h_muonPtT3)


    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        self.counter += 1
        self.h_eventsPrg.Fill(1)

        #Below we 'halt' execution for events past the first N (20 when written) by returning False now
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
        #Collections:
        #electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        HLTObj = Object(event, "HLT") #object with only the trigger branches in that event
        #IsoMu24 = getattr(HLTObj,'IsoMu24')
        #Mu50 = getattr(HLTObj, 'PFHT590')
        trigPath={}
        for tg in self.trigList:
            #if getattr(HLTObj,tg):
            trigPath[tg] = getattr(HLTObj,tg)

        trigCombination1 = ['IsoMu24', 'PFHT370'] #without "HLT_" prefix
        passAny = False
        for trig in trigCombination1:
            if trigPath[trig]:
                passAny = True

        jetHT_withT1=0
        jetHT_withT2=0
        jetHT_withT3=0
        jetHT_withoutT=0
        numberm=0
        
        if self.counter<5:print("\n{0:>5s} {1:>5s} {2:>10s} {3:>10s} {4:>10s}".format("Jet", "jetId","Pt", "Eta", "Phi"))
        for nj, jet in enumerate(jets):
            #Check jet passes 2017 Tight Jet ID https://twiki.cern.ch/twiki/bin/view/CMS/JetID13TeVRun2017
            if jet.jetId < 2:
                continue
            # Minimum 30GeV Pt on the jets
            if jet.pt < 30:
                continue
            # Only look at jets within |eta| < 2.4
            if abs(jet.eta) > 2.4:
                continue
                       
            if trigPath['IsoMu24']:
                jetHT_withT1 += jet.pt
            if trigPath['PFHT370']:
                jetHT_withT2 += jet.pt
            if passAny:
                jetHT_withT3 += jet.pt
                if self.counter<5:print("{0:*<5d} {1:*<5d} {2:>10.4f} {3:>+10.3f} {4:>+10.3f} (No triggers)".format(nj+1, jet.jetId, jet.pt, jet.eta, jet.phi))
            jetHT_withoutT += jet.pt
            if self.counter<5:print("{0:*<5d} {1:*<5d} {2:>10.4f} {3:>+10.3f} {4:>+10.3f}".format(nj+1, jet.jetId, jet.pt, jet.eta, jet.phi))
            
        self.h_eventsPrg.Fill(2)
        if passAny: self.h_eventsPrg.Fill(3)
        #Use the enumerate() function to get both an index and the iterated item in the collection
        """for ne, ele in enumerate(electrons) :
            if ne < 1:
                if IsoMu24:
                    self.h_elPtT1.Fill(ele.pt)
                if Mu50:
                    self.h_elPtT2.Fill(ele.pt)
                if passAny:
                    self.h_elPtT3.Fill(ele.pt)
                self.h_elPt.Fill(ele.pt)"""
        #self.preTriggerEvents+=1
        #if self.preTriggerEvents>70000: print(self.preTriggerEvents)
        if self.counter<5:print("\n{0:>5s} {1:>5s} {2:>6s} {3:>7s} {4:>6s} {5:>10s} {6:>10s} {7:>10s}".format("Muon", "pdgId","softId","tightId","jetIdx", "Pt", "Eta", "Phi"))
        for nm, muon in enumerate(muons) :
            if nm < 1:
                if trigPath['IsoMu24']:
                    self.h_muonPtT1.Fill(muon.pt)
                if trigPath['PFHT370']:
                    self.h_muonPtT2.Fill(muon.pt)
                if passAny:
                    self.h_muonPtT3.Fill(muon.pt)
                self.h_muonPt.Fill(muon.pt)
            if (self.counter<5 and passAny):print("{0:*<5d} {1:*<5d} {2:*<6d} {3:*<7d} {4:*<6d} {5:>10.4f} {6:>+10.3f} {7:>+10.3f}".format(nm+1, muon.pdgId, muon.softId, muon.tightId, muon.jetIdx, muon.pt, muon.eta, muon.phi))
            if self.counter<5:print("{0:*<5d} {1:*<5d} {2:*<6d} {3:*<7d} {4:*<6d} {5:>10.4f} {6:>+10.3f} {7:>+10.3f} (No triggers)".format(nm+1, muon.pdgId, muon.softId, muon.tightId, muon.jetIdx, muon.pt, muon.pdgId, muon.eta, muon.phi))

        if trigPath['IsoMu24']:
            self.h_jetHtT1.Fill(jetHT_withT1)
        if trigPath['PFHT370']:
            self.h_jetHtT2.Fill(jetHT_withT2)
        if passAny:
            self.h_jetHtT3.Fill(jetHT_withT3)
        self.h_jetHt.Fill(jetHT_withoutT)
        
        return True

#files=["06CC0D9B-4244-E811-8B62-485B39897212_CH01-Skim.root"]
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
                  #cut="nJet > 5 && ( nIsoTrack==1 ||(nMuon == 1 && nElectron==0 && nTau==0) || (nElectron == 1 && nMuon==0 && nTau==0) || (nElectron ==0 && nMuon==0 && nTau==1))",
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
