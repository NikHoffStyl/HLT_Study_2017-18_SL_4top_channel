# -*- coding: utf-8 -*-
"""
Created on Jan 2019

@author: NikHoffStyl
"""
from __future__ import (division, print_function)
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
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
        self.out.branch("nJets", "I")
        self.out.branch("Jet_" + "btagDeepB", "F")
        self.out.branch("Jet_" + "btagDeepFlavB", "F")
        self.out.branch("Jet_" + "eta", "F")
        self.out.branch("Jet_" + "phi", "F")
        self.out.branch("Jet_" + "pt", "F")
        self.out.branch("Jet_" + "jetId", "I")
        self.out.branch("Jet_" + "cleanmask", "F")

        # Muons
        self.out.branch("nMuon", "I")
        self.out.branch("Muon_" + "eta", "F")
        self.out.branch("Muon_" + "phi", "F")
        self.out.branch("Muon_" + "pt", "F")
        self.out.branch("Muon_" + "pfRelIso04_all", "F")
        self.out.branch("Muon_" + "tightId", "F")

        # Electrons
        self.out.branch("nElectron", "I")
        self.out.branch("Electron_" + "eta", "F")
        self.out.branch("Electron_" + "phi", "F")
        self.out.branch("Electron_" + "pt", "F")
        self.out.branch("Electron_" + "pfRelIso04_all", "F")
        self.out.branch("Electron_" + "tightId", "F")

        pass

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        """end file"""
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        # Collections
        allmuons = Collection(event, "Muon")
        allelectrons = Collection(event, "Electron")
        allrecojets = Collection(event, "Jet")

        # Select from reco :
        # muons = [x for nx, x in enumerate(allmuons) if
        #          (x.mediumId and abs(x.p4().Eta()) <self.maxObjEta)]
        # electrons = [x for x in allelectrons if (abs(x.p4().Eta()) < self.maxObjEta)]
        # self.out.fillBranch("nElectron", len(electrons))
        # recojets = [x for x in allrecojets if
        #             x.p4().Perp() > self.minJetPt and abs(x.eta) < self.maxObjEta and x.p4().DeltaR(lep0) > 0.8]
        # recojets.sort(key=lambda x: x.p4().Perp(), reverse=True)

        self.out.fillBranch("nMuon", len(allmuons))
        self.out.fillBranch("nElectron", len(allelectrons))
        self.out.fillBranch("nJet", len(allrecojets))
        for muon in allmuons:
            self.out.fillBranch("Muon_eta", muon.p4().Eta)
            self.out.fillBranch("Muon_phi", muon.p4().Phi)
            self.out.fillBranch("Muon_phi", muon.p4().Pt)

        for electron in allelectrons:
            self.out.fillBranch("Electron_eta", electron.p4().Eta)
            self.out.fillBranch("Electron_phi", electron.p4().Phi)
            self.out.fillBranch("Electron_phi", electron.p4().Pt)

        for jet in allrecojets:
            self.out.fillBranch("Electron_eta", jet.p4().Eta)
            self.out.fillBranch("Electron_phi", jet.p4().Phi)
            self.out.fillBranch("Electron_phi", jet.p4().Pt)

        return True

