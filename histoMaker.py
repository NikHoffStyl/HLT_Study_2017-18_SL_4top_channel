
from __future__ import (division, print_function)

import ROOT
from ROOT import TLatex

# from importlib import import_module

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


class HistogramMaker(Module):
    """
    This class HistogramMaker() fills histograms of required variables of jets, muons, electrons and MET;
    for different combinations of trigger paths.
    """

    def __init__(self, writeHistFile=True, eventLimit=-1, trigLst=None):
        """ Initialise global variables """

        self.eventCounter = 0
        self.comboCounter = 0
        self.numTriggers = len(trigLst["t1"]) * len(trigLst["t2"]) + len(trigLst["stndlone"])
        print("Number of Combined Triggers: %d" % self.numTriggers)
        self.trigCombination = [0]*self.numTriggers

        self.h_jetHt = {}
        self.h_jetEta = {}
        self.h_jetPhi = {}
        self.h_jetMap = {}

        self.h_muonPt = {}
        self.h_muonEta = {}
        self.h_muonPhi = {}
        self.h_muonMap = {}

        self.h_elPt = {}
        self.h_elEta = {}
        self.h_elPhi = {}
        self.h_elMap = {}

        self.h_metPt = {}
        self.h_metPhi = {}

        self.h_genMetPt = {}
        self.h_genMetPhi = {}

        self.nJet = None
        self.h_eventsPrg = ROOT.TH1D('h_eventsPrg', ';steps;entries', 11, 0, 11)

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

        # - Defining histograms to be saved to file
        self.h_jetHt['no_trigger'] = ROOT.TH1D('h_jetHt_notrigger',
                                               'no trigger ;H_{T} (GeV/c);Number of Events per 10 GeV/c', 300, 1, 3000)
        self.addObject(self.h_jetHt['no_trigger'])
        self.h_jetEta['no_trigger'] = ROOT.TH1D('h_jetEta_notrigger', 'no trigger ;Jet #eta;Number of Events per '
                                                                      '#delta#eta = 0.046', 300, -6, 8)
        self.addObject(self.h_jetEta['no_trigger'])
        self.h_jetPhi['no_trigger'] = ROOT.TH1D('h_jetPhi_notrigger', 'no trigger ;Jet #phi;Number of Events per '
                                                                      '#delta#phi = 0.046', 300, -6, 8)
        self.addObject(self.h_jetPhi['no_trigger'])
        self.h_jetMap['no_trigger'] = ROOT.TH2F('h_jetMap_notrigger', 'no trigger ;Jet #eta;Jet #phi',
                                                150, -6, 6, 160, -3.2, 3.2)
        self.addObject(self.h_jetMap['no_trigger'])

        self.h_muonPt['no_trigger'] = ROOT.TH1D('h_muonPt_notrigger', 'no trigger ;Muon P_{T} (GeV/c);Number of Events '
                                                                      'per 1 GeV/c', 300, 0, 300)
        self.addObject(self.h_muonPt['no_trigger'])
        self.h_muonEta['no_trigger'] = ROOT.TH1D('h_muonEta_notrigger', 'no trigger ;Muon #eta;Number of Events per '
                                                                        '#delta#eta = 0.046', 300, -6, 8)
        self.addObject(self.h_muonEta['no_trigger'])
        self.h_muonPhi['no_trigger'] = ROOT.TH1D('h_muonPhi_notrigger', 'no trigger ;Muon #phi;Number of Events per '
                                                                        '#delta#phi = 0.046', 300, -6, 8)
        self.addObject(self.h_muonPhi['no_trigger'])
        self.h_muonMap['no_trigger'] = ROOT.TH2F('h_muonMap_notrigger', 'no trigger;Muon #eta;Muon #phi;Number of '
                                                                        'Events per #delta#eta#times#delta#phi = 0.0016',
                                                 150, -6, 6, 160, -3.2, 3.2)
        self.addObject(self.h_muonMap['no_trigger'])

        self.h_elPt['no_trigger'] = ROOT.TH1D('h_elPt_notrigger', 'no trigger ;Electron P_{T} (GeV/c);Number of Events '
                                                                  'per 1 GeV/c', 300, 0, 300)
        self.addObject(self.h_elPt['no_trigger'])
        self.h_elEta['no_trigger'] = ROOT.TH1D('h_elEta_notrigger', 'no trigger ;Electron #eta;Number of Events per '
                                                                    '#delta#eta = 0.046', 300, -6, 8)
        self.addObject(self.h_elEta['no_trigger'])
        self.h_elPhi['no_trigger'] = ROOT.TH1D('h_elPhi_notrigger', 'no trigger ;Electron #phi;Number of Events per '
                                                                    '#delta#phi = 0.046', 300, -6, 8)
        self.addObject(self.h_elPhi['no_trigger'])
        self.h_elMap['no_trigger'] = ROOT.TH2F('h_elMap_notrigger', 'no trigger ;Electron #eta;Electron #phi',
                                               150, -6, 6, 160, -3.2, 3.2)
        self.addObject(self.h_elMap['no_trigger'])

        self.h_metPt['no_trigger'] = ROOT.TH1D('h_metPt_notrigger', 'no trigger ;MET P_{T} (GeV/c);Number of Events per'
                                                                    ' 1 GeV/c', 300, 0, 300)
        self.addObject(self.h_metPt['no_trigger'])
        self.h_metPhi['no_trigger'] = ROOT.TH1D('h_metPhi_notrigger', 'no trigger ;MET #phi;Number of Events per '
                                                                      '#delta#phi = 0.046', 300, -6, 8)
        self.addObject(self.h_metPhi['no_trigger'])

        self.h_genMetPt['no_trigger'] = ROOT.TH1D('h_genMetPt_notrigger', 'no trigger ;GenMET P_{T} (GeV/c);Number of '
                                                                          'Events per 1GeV/c', 300, 0, 300)
        self.addObject(self.h_genMetPt['no_trigger'])
        self.h_genMetPhi['no_trigger'] = ROOT.TH1D('h_genMetPhi_notrigger', 'no trigger ;GenMET #phi;Number of Events '
                                                                            'per #delta#phi = 0.046', 300, -6, 8)
        self.addObject(self.h_genMetPhi['no_trigger'])

        for key in self.trigLst:
            for trgPath in self.trigLst[key]:
                self.h_jetHt[trgPath] = ROOT.TH1D('h_jetHt_' + trgPath, trgPath + ';H_{T} (GeV/c);Number of Events'
                                                                                  ' per 10 GeV/c', 300, 1, 3000)
                self.addObject(self.h_jetHt[trgPath])
                self.h_jetEta[trgPath] = ROOT.TH1D('h_jetEta_' + trgPath, trgPath + ';Jet #eta;Number of Events per'
                                                                                    ' #delta#eta = 0.046', 300, -6, 8)
                self.addObject(self.h_jetEta[trgPath])
                self.h_jetPhi[trgPath] = ROOT.TH1D('h_jetPhi_' + trgPath, trgPath + ';Jet #phi;Number of Events per'
                                                                                    ' #delta#phi = 0.046', 300, -6, 8)
                self.addObject(self.h_jetPhi[trgPath])
                self.h_jetMap[trgPath] = ROOT.TH2F('h_jetMap_' + trgPath,  trgPath + ';Jet #eta;Jet #phi',
                                                   150, -3, 3, 160, -3.2, 3.2)
                self.addObject(self.h_jetMap[trgPath])

                self.h_muonPt[trgPath] = ROOT.TH1D('h_muonPt_' + trgPath, trgPath + ';Muon P_{T} (GeV/c);Number of '
                                                                                    'Events per 1 GeV/c', 300, 0, 300)
                self.addObject(self.h_muonPt[trgPath])
                self.h_muonEta[trgPath] = ROOT.TH1D('h_muonEta_' + trgPath, trgPath + ';Muon #eta;Number of Events per'
                                                                                      ' #delta#eta = 0.046', 300, -6, 8)
                self.addObject(self.h_muonEta[trgPath])
                self.h_muonPhi[trgPath] = ROOT.TH1D('h_muonPhi_' + trgPath, trgPath + ';Muon #phi;Number of Events per'
                                                                                      ' #delta#phi = 0.046', 300, -6, 8)
                self.addObject(self.h_muonPhi[trgPath])
                self.h_muonMap[trgPath] = ROOT.TH2F('h_muonMap_' + trgPath,  trgPath + ';Muon #eta;Muon #phi',
                                                    150, -3, 3, 160, -3.2, 3.2)
                self.addObject(self.h_muonMap[trgPath])  # - Draw ith CONTZ COLZPOL COLZ1 ARR E

                self.h_elPt[trgPath] = ROOT.TH1D('h_elPt_' + trgPath, trgPath + ';Electron P_{T} (GeV/c);Number of '
                                                                                'Events per 1 GeV/c', 300, 0, 300)
                self.addObject(self.h_elPt[trgPath])
                self.h_elEta[trgPath] = ROOT.TH1D('h_elEta_' + trgPath, trgPath + ';Electron #eta;Number of Events per '
                                                                                  '#delta#eta = 0.046', 300, -6, 8)
                self.addObject(self.h_elEta[trgPath])
                self.h_elPhi[trgPath] = ROOT.TH1D('h_elPhi_' + trgPath, trgPath + ';Electron #phi;Number of Events per '
                                                                                  '#delta#phi = 0.046', 300, -6, 8)
                self.addObject(self.h_elPhi[trgPath])
                self.h_elMap[trgPath] = ROOT.TH2F('h_elMap_' + trgPath, trgPath + ';Electron #eta;Electron #phi',
                                                  150, -3, 3, 160, -3.2, 3.2)
                self.addObject(self.h_elMap[trgPath])

                self.h_metPt[trgPath] = ROOT.TH1D('h_metPt_' + trgPath, trgPath + ';MET P_{T} (GeV/c);Number of Events '
                                                                                  'per 1 GeV/c', 300, 0, 300)
                self.addObject(self.h_metPt[trgPath])
                self.h_metPhi[trgPath] = ROOT.TH1D('h_metPhi_' + trgPath, trgPath + ';MET #phi;Number of Events per '
                                                                                    '#delta#phi = 0.046', 300, -6, 8)
                self.addObject(self.h_metPhi[trgPath])

                self.h_genMetPt[trgPath] = ROOT.TH1D('h_genMetPt_' + trgPath, trgPath + ';GenMET P_{T} (GeV/c);Number '
                                                                                        'of Events per 1 GeV/c',
                                                     300, 0, 300)
                self.addObject(self.h_genMetPt[trgPath])
                self.h_genMetPhi[trgPath] = ROOT.TH1D('h_genMetPhi_' + trgPath, trgPath + ';GenMET #phi;Number of '
                                                                                          'Events per #delta#phi = 0.046',
                                                      300, -6, 8)
                self.addObject(self.h_genMetPhi[trgPath])

        # - TODO: Test creation of ntuple
        self.nJet = ROOT.TNtuple("njet", "tuple of Jets", "HT : eta : phi ")

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
                        self.h_jetEta[tg].Fill(jet.eta)
                        self.h_jetPhi[tg].Fill(jet.phi)
                        self.h_jetMap[tg].Fill(jet.eta, jet.phi)
                        # self.nJet.Fill(jetHt[tg],jet.eta, jet.phi)
            jetHt["notrig"] += jet.pt
            self.h_jetEta['no_trigger'].Fill(jet.eta)
            self.h_jetPhi['no_trigger'].Fill(jet.phi)
            self.h_jetMap['no_trigger'].Fill(jet.eta, jet.phi)

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
                            self.h_muonPt[tg].Fill(muon.pt)
                            self.h_muonEta[tg].Fill(muon.eta)
                            self.h_muonPhi[tg].Fill(muon.phi)
                            self.h_muonMap[tg].Fill(muon.eta, muon.phi)
                self.h_muonPt['no_trigger'].Fill(muon.pt)
                self.h_muonEta['no_trigger'].Fill(muon.eta)
                self.h_muonPhi['no_trigger'].Fill(muon.phi)
                self.h_muonMap['no_trigger'].Fill(muon.eta, muon.phi)

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
                            self.h_elPt[tg].Fill(el.pt)
                            self.h_elEta[tg].Fill(el.eta)
                            self.h_elPhi[tg].Fill(el.phi)
                            self.h_elMap[tg].Fill(el.eta, el.phi)
                self.h_elPt['no_trigger'].Fill(el.pt)
                self.h_elEta['no_trigger'].Fill(el.eta)
                self.h_elPhi['no_trigger'].Fill(el.phi)
                self.h_elMap['no_trigger'].Fill(el.eta, el.phi)

        metPt = getattr(met, "pt")
        metPhi = getattr(met, "phi")
        genMetPt = getattr(genMet, "pt")
        genMetPhi = getattr(genMet, "pt")
        for key in self.trigLst:
            for tg in self.trigLst[key]:
                if trigPath[tg]:
                    self.h_metPt[tg].Fill(metPt)
                    self.h_metPhi[tg].Fill(metPhi)
                    self.h_genMetPt[tg].Fill(genMetPt)
                    self.h_genMetPhi[tg].Fill(genMetPhi)
        self.h_metPt['no_trigger'].Fill(metPt)
        self.h_metPhi['no_trigger'].Fill(metPhi)
        self.h_genMetPt['no_trigger'].Fill(genMetPt)
        self.h_genMetPhi['no_trigger'].Fill(genMetPhi)

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
                        self.h_jetHt[tg].Fill(jetHt[tg])

            self.h_jetHt['no_trigger'].Fill(jetHt["notrig"])
        
        return True
