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
        self.EventLimit = 100000 #-1 for no limit, anything larger chosen here will be the limit of events fully processed

    def beginJob(self,histFile=None,histDirName=None):
        #typically where histograms should be initialized
        #So we call the default Module's beginJob, passing it the histFile and histDirName first passed to the PostProcessor
        Module.beginJob(self,histFile,histDirName)

        #The histogram is 'booked' with the service that will write everything to the output file via self.addObject()
        self.h_jetPt = ROOT.TH1D('h_jetPt', ';H_{T};Events', 200, 0, 2300)
        self.addObject(self.h_jetPt)
        self.h_jetPtT = ROOT.TH1D('h_jetPtT', ';H_{T};Events', 200, 0, 2300)
        self.addObject(self.h_jetPtT)
        self.h_elPt = ROOT.TH1D('h_elPt', ';P_{T} ;Events', 200, 0, 300)
        self.addObject(self.h_elPt)
        self.h_elPtT = ROOT.TH1D('h_elPtT', ';P_{T};Events', 200, 0, 300)
        self.addObject(self.h_elPtT)
        self.h_muonPt = ROOT.TH1D('h_muonPt', ';P_{T};Events', 200, 0, 300)
        self.addObject(self.h_muonPt)
        self.h_muonPtT = ROOT.TH1D('h_muonPtT', ';P_{T};Events', 200, 0, 300)
        self.addObject(self.h_muonPtT)

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        self.counter += 1

        #Below we 'halt' execution for events past the first N (20 when written) by returning False now
        if self.counter > self.EventLimit > -1:
            return False

        ###########################################
        ###### Basic Attributes of the Event ######
        ###########################################
        #Use basic python getattr() method to grab this info, no need for Object or Collection here
        run = getattr(event, "run")
        lumi = getattr(event, "luminosityBlock")
        evt = getattr(event, "event")
        #print("\n\nRun: {0:>8d} \tLuminosityBlock: {1:>8d} \tEvent: {2:>8d}".format(run,lumi,evt))
        eventSum = ROOT.TLorentzVector()

        ###########################################
        ###### Event Collections and Objects ######
        ###########################################
        #Collections:
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        hltAk4PfJet100 = getattr(event, "HLT_AK4PFJet100")
        hltIsoMu24 = getattr(event,"HLT_IsoMu24")
        hltIsoTkMu24 = getattr(event, "HLT_IsoMu24_eta2p1")

        jetHT_withT=0
        jetHT_withoutT=0

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

            if hltIsoMu24:
                jetHT_withT += jet.pt
            jetHT_withoutT += jet.pt

        #Use the enumerate() function to get both an index and the iterated item in the collection
        for ne, ele in enumerate(electrons) :
            if hltIsoMu24:
                self.h_elPtT.Fill(ele.pt)
            self.h_elPt.Fill(ele.pt)
        for nm, muon in enumerate(muons) :
            if hltIsoMu24:
                self.h_muonPtT.Fill(muon.pt)
            self.h_muonPt.Fill(muon.pt)

        if hltIsoMu24:
            self.h_jetPtT.Fill(jetHT_withT)
        self.h_jetPt.Fill(jetHT_withoutT)

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

for file in files:
    print(file)


p99=PostProcessor(".",
                  files,
                  #onefile,
                  cut="nJet > 5 && nMuon > 0 ",
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
