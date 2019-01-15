
from __future__ import (division, print_function)

import ROOT
from ROOT import TLatex

# from importlib import import_module

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
        self.numTriggers = len(trigLst["t1"]) * len(trigLst["t2"]) + len(trigLst["stndlone"])
        print("Number of Combined Triggers: %d" % self.numTriggers)
        self.trigCombination = [0]*self.numTriggers

        self.nJet = {}
        self.nMuon = {}
        self.nEl = {}
        self.nMet = {}
        self.nGenMet = {}

        self.h_eventsPrg = ROOT.TH1D('h_eventsPrg', ';steps; Events per Trigger', 11, 0, 11)

        self.writeHistFile = writeHistFile
        self.eventLimit = eventLimit  # -1 for no limit of events fully processed
        if trigLst is None:
            self.trigLst = {}
        else:
            self.trigLst = trigLst
            for t1 in self.trigLst["t1"]:
                for t2 in self.trigLst["t2"]:
                    self.trigCombination[self.comboCounter] = [t1, t2]
                    self.comboCounter += 1
                    self.trigLst["combos"].append(t1 + '_' + t2)  # append new triggers to old list

    def beginJob(self, histFile=None, histDirName=None):
        """ Initialise histograms to be used and saved in output file. """

        # - Run beginJob() of Module
        Module.beginJob(self, histFile, histDirName)  # pass histFile and histDirName first passed to the PostProcessor

        # - Defining ntuples to be saved to file
        self.nJet['no_trigger'] = ROOT.TNtuple("njet_notrigger", "tuple of Jets", "HT : eta : phi ")
        self.addObject(self.nJet['no_trigger'])
        self.nMuon['no_trigger'] = ROOT.TNtuple("nmuon_notrigger", "tuple of Muons", "pt : eta : phi ")
        self.addObject(self.nMuon['no_trigger'])
        self.nEl['no_trigger'] = ROOT.TNtuple("nel_notrigger", "tuple of Electrons", "pt : eta : phi ")
        self.addObject(self.nEl['no_trigger'])
        self.nMet['no_trigger'] = ROOT.TNtuple("nmet_notrigger", "tuple of MET", "pt : phi ")
        self.addObject(self.nMet['no_trigger'])
        self.nGenMet['no_trigger'] = ROOT.TNtuple("ngenmet_notrigger", "tuple of GenMET", "pt : phi ")
        self.addObject(self.nGenMet['no_trigger'])

        for key in self.trigLst:
            for trgPath in self.trigLst[key]:
                self.nJet[trgPath] = ROOT.TNtuple("njet_" + trgPath, "tuple of Jets", "HT : eta : phi ")
                self.addObject(self.nJet[trgPath])
                self.nMuon[trgPath] = ROOT.TNtuple("nmuon_" + trgPath, "tuple of Muons", "pt : eta : phi ")
                self.addObject(self.nMuon[trgPath])
                self.nEl[trgPath] = ROOT.TNtuple("nel_" + trgPath, "tuple of Electrons", "pt : eta : phi ")
                self.addObject(self.nEl[trgPath])
                self.nMet[trgPath] = ROOT.TNtuple("nmet_" + trgPath, "tuple of MET", "pt : phi ")
                self.addObject(self.nMet[trgPath])
                self.nGenMet[trgPath] = ROOT.TNtuple("ngenmet_" + trgPath, "tuple of GenMET", "pt : phi ")
                self.addObject(self.nGenMet[trgPath])

        self.addObject(self.h_eventsPrg)

    def analyze(self, event):
        """ process event, return True (go to next module) or False (fail, go to next event) """

        self.eventCounter += 1
        self.h_eventsPrg.Fill(0)

        # - 'Halt' execution for events past the first N (20 when written) by returning False
        if self.eventCounter > self.eventLimit > -1:
            return False

        ##################################
        #  Event Collections and Objects #
        ##################################
        muons = Collection(event, "Muon")
        electrons = Collection(event, "Electron")
        jets = Collection(event, "Jet")
        hltObj = Object(event, "HLT")  # object with only the trigger branches in that event
        met = Object(event, "MET")
        genMet = Object(event, "GenMET")

        trigPath = {}

        for key in self.trigLst:
            for tg in self.trigLst[key]:
                if not self.trigLst[key] == self.trigLst["combos"]:
                    trigPath[tg] = getattr(hltObj, tg)
    
        for i in range(self.comboCounter):
            trigPath[self.trigCombination[i][0] + '_' + self.trigCombination[i][1]] = False
            for trig in self.trigCombination[i]:
                if trigPath[trig]:
                    trigPath[self.trigCombination[i][0] + '_' + self.trigCombination[i][1]] = True

        jetHt = {"notrig": 0}
        for key in self.trigLst:
            for tg in self.trigLst[key]:
                jetHt.update({tg: 0})

        nJetPass = 0
        nBtagPass = 0
        firstMuonPass = False
        firstElPass = False

        for nj, jet in enumerate(jets):
            # - Check jet passes 2017 Tight Jet ID https://twiki.cern.ch/twiki/bin/view/CMS/JetID13TeVRun2017
            # - Minimum 30GeV Pt on the jets
            # - Only look at jets within |eta| < 2.4
            if jet.jetId < 2 or jet.pt < 30 or abs(jet.eta) > 2.4:
                continue
            else:
                nJetPass += 1

            # Count b-tagged jets with DeepFlavourB algorithm at the medium working point
            # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation94X
            if jet.btagDeepFlavB > 0.7489:
                nBtagPass += 1

            # Calculate jetHt for different trigger paths and combinations of them
            for key in self.trigLst:
                for tg in self.trigLst[key]:
                    if trigPath[tg]:
                        jetHt[tg] += jet.pt
                        self.nJet[tg].Fill(None, jet.eta, jet.phi)
            jetHt["notrig"] += jet.pt
            self.nJet['no_trigger'].Fill(None, jet.eta, jet.phi)

        for nm, muon in enumerate(muons):
            if nm == 0:
                if (getattr(muon, "tightId") is False) or abs(muon.eta) > 2.4 or muon.miniPFRelIso_all > 0.15:
                    continue
                else:
                    firstMuonPass = True

            if nm == 0 and nJetPass > 5 and firstMuonPass is True and nBtagPass > 0:
                for key in self.trigLst:
                    for tg in self.trigLst[key]:
                        if trigPath[tg]:
                            self.nMuon[tg].Fill(muon.pt, muon.eta, muon.phi)
                self.nMuon['no_trigger'].Fill(muon.pt, muon.eta, muon.phi)

        for nl, el in enumerate(electrons):
            if nl == 0:
                if abs(el.eta) > 2.4 or el.miniPFRelIso_all > 0.15:
                    continue
                else:
                    firstElPass = True

            if nl == 0 and nJetPass > 5 and firstElPass is True and nBtagPass > 0:
                for key in self.trigLst:
                    for tg in self.trigLst[key]:
                        if trigPath[tg]:
                            self.nEl[tg].Fill(el.pt, el.eta, el.phi)
                self.nEl['no_trigger'].Fill(el.pt, el.eta, el.phi)

        metPt = getattr(met, "pt")
        metPhi = getattr(met, "phi")
        genMetPt = getattr(genMet, "pt")
        genMetPhi = getattr(genMet, "pt")
        for key in self.trigLst:
            for tg in self.trigLst[key]:
                if trigPath[tg]:
                    self.nMet[tg].Fill(metPt, metPhi)
                    self.nGenMet[tg].Fill(genMetPt, genMetPhi)
        self.nMet['no_trigger'].Fill(metPt)
        self.nGenMet['no_trigger'].Fill(genMetPt)

        if nJetPass > 5 and nBtagPass > 0:
            self.h_eventsPrg.Fill(1)
            i = 0
            for key in self.trigLst:
                for tg in self.trigLst[key]:
                    if trigPath[tg]:
                        self.h_eventsPrg.Fill(2+i)
                        i += 1

        if nJetPass > 5 and firstMuonPass is True and nBtagPass > 0:
            for key in self.trigLst:
                for tg in self.trigLst[key]:
                    if trigPath[tg]:
                        self.nJet[tg].Fill(jetHt[tg], None, None)

            self.nJet['no_trigger'].Fill(jetHt["notrig"], None, None)
        
        return True
