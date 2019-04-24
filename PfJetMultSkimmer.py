# -*- coding: utf-8 -*-
"""
Created on Jan 2019

@author: NikHoffStyl
"""
from __future__ import (division, print_function)
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


class PfJetsSkimmer(Module):
    """This class is to be used by the postprocessor to skimm a file down
    using the requirement of number of jets and a single lepton."""

    def __init__(self, writeHistFile=True):
        """ Initialise global variables
        Args:
            writeHistFile (bool): True to write file, False otherwise
        """

        self.writeHistFile = writeHistFile

    def beginJob(self, histFile=None, histDirName=None):
        """begin job"""
        Module.beginJob(self, histFile, histDirName)

    def endJob(self):
        """end Job"""
        Module.endJob(self)

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        """add branches to file"""
        self.out = wrappedOutputTree

        # Jets
        self.out.branch("nJets2", "I")
        # self.out.branch("Jet2_" + "btagDeepB", "F")
        # self.out.branch("Jet2_" + "btagDeepFlavB", "F")
        # self.out.branch("Jet2_" + "eta", "F")
        # self.out.branch("Jet2_" + "phi", "F")
        # self.out.branch("Jet2_" + "pt", "F")
        # self.out.branch("Jet2_" + "jetId", "I")
        # self.out.branch("Jet2_" + "cleanmask", "F")
        self.out.branch("Jet2_" + "HT", "F")

        # Muons
        self.out.branch("nMuon2", "I")
        self.out.branch("Muon2_" + "eta", "F")
        self.out.branch("Muon2_" + "phi", "F")
        self.out.branch("Muon2_" + "pt", "F")
        self.out.branch("Muon2_" + "pfRelIso04_all", "F")
        self.out.branch("Muon2_" + "tightId", "F")

        # Electrons
        self.out.branch("nElectron2", "I")
        self.out.branch("Electron2_" + "eta", "F")
        self.out.branch("Electron2_" + "phi", "F")
        self.out.branch("Electron2_" + "pt", "F")
        self.out.branch("Electron2_" + "pfRelIso04_all", "F")
        self.out.branch("Electron2_" + "tightId", "F")

        pass

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        """end file"""
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        # Collections
        muons = Collection(event, "Muon")
        electrons = Collection(event, "Electron")
        jets = Collection(event, "Jet")
        # hltObj = Object(event, "HLT")  # object with only the trigger branches in that event
        # met = Object(event, "MET")

        jetHt = 0
        for nj, jet in enumerate(jets):
            jetHt += jet.pt

        # Select from reco :
        # muons = [x for nx, x in enumerate(allmuons) if
        #          (x.mediumId and abs(x.p4().Eta()) <self.maxObjEta)]
        # electrons = [x for x in allelectrons if (abs(x.p4().Eta()) < self.maxObjEta)]
        # self.out.fillBranch("nElectron", len(electrons))
        # recojets = [x for x in allrecojets if
        #             x.p4().Perp() > self.minJetPt and abs(x.eta) < self.maxObjEta and x.p4().DeltaR(lep0) > 0.8]
        # recojets.sort(key=lambda x: x.p4().Perp(), reverse=True)

        self.out.fillBranch("nMuon2", len(muons))
        self.out.fillBranch("nElectron2", len(electrons))
        self.out.fillBranch("nJets2", len(jets))
        self.out.fillBranch("Jet2_HT", jetHt)
        #for muon in allmuons:
            #self.out.fillBranch("Muon_eta", muon.p4().Eta())
            #self.out.fillBranch("Muon_phi", muon.phi)
            #self.out.fillBranch("Muon_pt", muon.pt)

        #for electron in allelectrons:
            #self.out.fillBranch("Electron_eta", electron.p4().Eta)
            #self.out.fillBranch("Electron_phi", electron.phi)
            #self.out.fillBranch("Electron_pt", electron.pt)

        #for jet in allrecojets:
            #self.out.fillBranch("Jet_eta", jet.eta)
            #self.out.fillBranch("Jet_phi", jet.phi)
            #self.out.fillBranch("Jet_pt", jet.pt)

        return True

