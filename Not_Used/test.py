
from __future__ import (division, print_function)

import ROOT
from ROOT import TLatex

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


class NTupleMaker(Module):
    """
    This class NTupleMaker() fills ntuples with values of required variables of jets, muons, electrons and MET;
    for different combinations of trigger paths.
    """

    def __init__(self, writeHistFile=True, eventLimit=-1, trigLst=None):
        """ Initialise global variables """

        self.eventCounter = 0
        self.comboCounter = 0

        self.writeHistFile = writeHistFile
        self.eventLimit = eventLimit  # -1 for no limit of events fully processed
        self.trigLst = trigLst
        self.selCriteria = {}
        with open("selectionCriteria.txt") as f:
            for line in f:
                if line.find(":") == -1: continue
                (key, val) = line.split(": ")
                c = len(val) - 1
                val = val[0:c]
                if val.replace('.', '', 1).isdigit():
                    self.selCriteria[key] = float(val)
                else:
                    self.selCriteria[key] = val

        self.nJet = ROOT.TNtuple("njet_notrigger", "tuple of Jets", "HT:eta:phi")

    def beginJob(self, histFile=None, histDirName=None):
        """ Initialise histograms to be used and saved in output file. """

        # - Run beginJob() of Module
        Module.beginJob(self, histFile, histDirName)  # pass histFile and histDirName first passed to the PostProcessor

        # - Defining ntuples to be saved to file

        self.addObject(self.nJet)

    def jetCriteria(self, jets):
        """
        Return the number of accepted jets and the number of accepted b-tagged jets

        Args:
            jets (Collection): Information of jets
        Returns:
            (tuple): tuple containing:
                nJetsPass (int): number of jets
                nBtagsPass (int): number of b-tagged jets
        """
        nJetsPass = 0
        nBtagsPass = 0
        JetPassIdx = []
        for nj, jet in enumerate(jets):
            # - Check jet passes 2017 Tight Jet ID https://twiki.cern.ch/twiki/bin/view/CMS/JetID13TeVRun2017
            # - Minimum 30GeV Pt on the jets
            # - Only look at jets within |eta| < 2.4
            if jet.jetId < self.selCriteria["minJetId"] or jet.pt < self.selCriteria["minJetPt"]: continue
            if abs(jet.eta) > self.selCriteria["maxObjEta"]: continue
            if self.selCriteria["jetCleanmask"] == "Y" and jet.cleanmask is False: continue
            nJetsPass += 1
            JetPassIdx.append(nj)
            # Count b-tagged jets with DeepFlavourB algorithm at the medium working point
            # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation94X
            if jet.btagDeepFlavB > 0.7489:
                nBtagsPass += 1
        return nJetsPass, JetPassIdx, nBtagsPass

    def muonCriteria(self, muons):
        """
        Return the number of accepted jets and the number of accepted b-tagged jets

        Args:
            muons (Collection): Information of jets
        Returns:
            tuple: tuple containing
                nMuonsPass (int): number of muons
                MuonsPassIdx (int): index of muon that passed
        """
        nMuonsPass = 0
        MuonsPassIdx = 0
        for nm, muon in enumerate(muons):
            # - Check muon criteria 2017 https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideMuonIdRun2
            if (getattr(muon, "tightId") is False) or abs(muon.eta) > self.selCriteria["maxObjEta"]: continue
            if muon.pfRelIso04_all > self.selCriteria["maxPfRelIso04"]: continue
            nMuonsPass += 1
            MuonsPassIdx = nm

        return nMuonsPass, MuonsPassIdx

    def electronCriteria(self, electrons):
        """
        Return the number of accepted jets and the number of accepted b-tagged jets

        Args:
            electrons (Collection): Information of jets
        Returns:
            tuple: tuple containing
                nElsPass (int): number of muons
                ElsPassIdx (int): index of muon that passed
        """
        nElsPass = 0
        ElsPassIdx = 0
        for ne, el in enumerate(electrons):
            if abs(el.eta) > self.selCriteria["maxObjEta"]: continue
            if el.miniPFRelIso_all > self.selCriteria["maxMiniPfRelIso"]: continue
            if self.selCriteria["mvaWP"] == 90 and el.mvaFall17V2Iso_WP90 is False: continue
            if 1.4442 < abs(el.eta) < 1.566: continue

            #  el.convVeto or el.sieie<0.0106 or el.lostHits<=1
            #  or el.hoe <(0.046 + 1.16/(el.EtaSC)+ 0.0324*(rho)/(EtaSC))
            nElsPass += 1
            ElsPassIdx = ne

        return nElsPass, ElsPassIdx

    def analyze(self, event):
        """ process event, return True (go to next module) or False (fail, go to next event) """

        self.eventCounter += 1
        if self.eventCounter > self.eventLimit > -1:
            return False

        muons = Collection(event, "Muon")
        electrons = Collection(event, "Electron")
        jets = Collection(event, "Jet")
        hltObj = Object(event, "HLT")  # object with only the trigger branches in that event
        met = Object(event, "MET")

        jetHt = {"notrig": 0}
        for key in self.trigLst:
            if not key.find("El") == -1: continue
            for tg in self.trigLst[key]:
                jetHt.update({tg: 0})

        nJetPass, JetPassIdx, nBtagPass = self.jetCriteria(jets)
        nMuonPass, MuonPassIdx = self.muonCriteria(muons)
        nElPass, ElPassIdx = self.electronCriteria(electrons)
        if nJetPass > 5 and nMuonPass == 1 and nBtagPass > 0 and nElPass == 0:
            for nj, jet in enumerate(jets):
                if nj not in JetPassIdx: continue
                self.nJet.Fill(jet.pt, jet.eta, jet.phi)
        
        return True
