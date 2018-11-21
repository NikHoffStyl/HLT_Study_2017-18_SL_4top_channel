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
        #beginJob is typically where histograms should be initialized
        #So we call the default Module's beginJob, passing it the histFile and histDirName first passed to the PostProcessor
        Module.beginJob(self,histFile,histDirName)

        #Create a 1-D histogram (TH1D) with histogram_name h_jets, and someTitle(title)/nJets(x-axis)/Events(y-axis), 20 bins, Domain 0 to 20
        #The histogram then has to be 'booked' with the service that will write everything to the output file via self.addObject()
        """self.h_jets = ROOT.TH1D('h_jets', 'someTitle;nJets;Events',   20, 0, 20)
        self.addObject(self.h_jets)
        self.h_jetsT = ROOT.TH1D('h_jetsT', 'someTitle;nJets;Events',   20, 0, 20)
        self.addObject(self.h_jetsT)
        self.h_fatjets = ROOT.TH1D('h_fatjets', ';nFatJets;Events', 8, 0, 8)
        self.addObject(self.h_fatjets)
        self.h_fatjetsT = ROOT.TH1D('h_fatjetsT', ';nFatJets;Events', 8, 0, 8)
        self.addObject(self.h_fatjetsT)
        self.h_subjets = ROOT.TH1D('h_subjets', ';nSubJets;Events', 16, 0, 16)
        self.addObject(self.h_subjets)
        self.h_subjetsT = ROOT.TH1D('h_subjetsT', ';nSubJets;Events', 16, 0, 16)
        self.addObject(self.h_subjetsT)
        self.h_jetEta = ROOT.TH1D('h_jetEta', ';valJetEta;Events', 40, -2.5, 2.5)
        self.addObject(self.h_jetEta)
        self.h_jetEtaT = ROOT.TH1D('h_jetEtaT', ';valJetEta;Events', 40, -2.5, 2.5)
        self.addObject(self.h_jetEtaT)"""
        self.h_jetPt = ROOT.TH1D('h_jetPt', ';JetPt;Events', 60, 0, 200)
        self.addObject(self.h_jetPt)
        self.h_jetPtT = ROOT.TH1D('h_jetPtT', ';JetPt;Events', 60, 0, 200)
        self.addObject(self.h_jetPtT)
        self.h_elPt = ROOT.TH1D('h_elPt', ';valElPt ;Events', 60, 0, 200)
        self.addObject(self.h_elPt)
        self.h_elPtT = ROOT.TH1D('h_elPtT', ';valElPt;Events', 60, 0, 200)
        self.addObject(self.h_elPtT)
        self.h_muonPt = ROOT.TH1D('h_muonPt', ';valMuonPt;Events', 60, 0, 200)
        self.addObject(self.h_muonPt)
        self.h_muonPtT = ROOT.TH1D('h_muonPtT', ';valMuonPt;Events', 60, 0, 200)
        self.addObject(self.h_muonPtT)
        """self.h_jetPhi = ROOT.TH1D('h_jetPhi', ';valJetPhi;Events', 20, -3.14, 3.14)
        self.addObject(self.h_jetPhi)
        self.h_jetPhiT = ROOT.TH1D('h_jetPhiT', ';valJetPhi;Events', 20, -3.14, 3.14)
        self.addObject(self.h_jetPhiT)
        self.h_jet_map = ROOT.TH2F('h_jet_map', ';Jet #eta;Jet #phi', 40, -2.5, 2.5, 20, -3.14, 3.14)
        self.addObject(self.h_jet_map)
        self.h_jetPtPhi = ROOT.TH2F('h_jetPtPhi', ';Jet #phi;Jet P_{T}', 20, -3.14, 3.14, 60, 30, 400)
        self.addObject(self.h_jetPtPhi)
        self.h_jetPtEta = ROOT.TH2F('h_jetPtEta', ';Jet #eta;Jet P_{T}', 40, -2.5, 2.5, 60, 30, 400)
        self.addObject(self.h_jetPtEta)
        self.h_jetPtId = ROOT.TH2F('h_jetPtId', ';Jet ID;Jet P_{T}', 11, 0,10, 60, 30, 400)
        self.addObject(self.h_jetPtId)
        self.h_jetPtnjet = ROOT.TH2F('h_jetPtnjet', ';Number of Jets;Jet P_{T}', 21, 0,20, 60, 30, 500)
        self.addObject(self.h_jetPtnjet)
        self.h_medCSVV2 = ROOT.TH1D('h_medCSVV2', ';Medium CSVV2 btags; Events', 5, 0, 5)
        self.addObject(self.h_medCSVV2)
        self.h_medDeepB = ROOT.TH1D('h_medDeepB', ';Medium DeepCSV btags; Events', 5, 0, 5)
        self.addObject(self.h_medDeepB)"""

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
        #Collections are for variable-length objects, easily identified by a nVARIABLE object in the NanoAOD file ("nJet")
        #Objects are for 1-deep variables, like HLT triggers, where there are many of them, but there is only one boolean value
        #for each HLT_SomeSpecificTrigger in the event. These are more than just wrappers, providing convenient methods
        #This will 'work' for anything that has some common name + '_' (like "SV_x" and "SV_y" and "SV_z")

        #Objects:
        #met = Object(event, "MET")
        #PV = Object(event, "PV")

        #Collections:
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        #fatjets = Collection(event, "FatJet")
        #subjets = Collection(event, "SubJet")
        hltAk4PfJet100 = getattr(event, "HLT_AK4PFJet100")
        hltIsoMu24 = getattr(event,"HLT_IsoMu24")
        hltIsoTkMu24 = getattr(event, "HLT_IsoTkMu24")

        """nEles = len(electrons)
        nMus = len(muons)
        nAK4Jets = len(jets)
        nAK8Jets = len(fatjets)
        nAK8SubJets = len(subjets)

        self.h_jets.Fill(nAK4Jets)
        self.h_fatjets.Fill(nAK8Jets)
        self.h_subjets.Fill(nAK8SubJets)

        nMedCSVV2 = 0
        nMedDeepB = 0
        #jetCounter =0"""

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

            if  hltIsoMu24 or hltIsoTkMu24:
                #self.h_jetPtT.Fill(jet.pt)
                jetHT_withT += jet.pt
            #jetCounter += 1
            jetHT_withoutT += jet.pt
            # Fill 2D histo
            """self.h_jet_map.Fill(jet.eta, jet.phi)
            self.h_jetPtPhi.Fill(jet.phi, jet.pt)
            self.h_jetPtEta.Fill(jet.eta, jet.pt)
            self.h_jetPtId.Fill(jet.jetId, jet.pt)"""
            #numJet = getattr(event, "nJet")
            #self.h_jetPtnjet.Fill(nAK4Jets,jet.pt)
            #self.h_jetPt.Fill(jet.pt)
            #Count b-tagged jets with two algos at the medium working point
            #https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation94X
            """if jet.btagCSVV2 > 0.8838:
                nMedCSVV2 += 1
            if jet.btagDeepB > 0.4941:
                nMedDeepB += 1"""

        #Use the enumerate() function to get both an index and the iterated item in the collection
        for ne, ele in enumerate(electrons) :
            if hltIsoTkMu24 or hltIsoMu24:
                self.h_elPtT.Fill(ele.pt)
            self.h_elPt.Fill(ele.pt)
        for nm, muon in enumerate(muons) :
            if hltIsoTkMu24 or hltIsoMu24:
                self.h_muonPtT.Fill(muon.pt)
            self.h_muonPt.Fill(muon.pt)

        # Fill 1D histo
	    #self.h_jetEta.Fill(jet.eta)
        #self.h_jetPhi.Fill(jet.phi)
        self.h_jetPt.Fill(jetHT_withT)
        self.h_jetPtT.Fill(jetHT_withoutT)
        #self.h_medCSVV2.Fill(nMedCSVV2)
        #self.h_medDeepB.Fill(nMedDeepB)

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
                  cut="nJet > 6 && nMuon >0",
                  modules=[HistogramMaker()],
                  jsonInput=None,
                  noOut=True,
                  justcount=False,
                  postfix=thePostFix,
                  histFileName="../OutHistoMaker2.root",
                  histDirName="plots",
                  )
t0 = time.clock()
p99.run()
t1 = time.clock()
print("Elapsed time %7.1fs" %(t1-t0))
