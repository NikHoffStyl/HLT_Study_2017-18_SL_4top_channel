
from __future__ import (division, print_function)

import ROOT
from ROOT import TLatex

# from importlib import import_module

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


class TriggerStudy(Module):
    """This class HistogramMaker() fills histograms of required variables of jets, muons, electrons and MET;
    for different combinations of trigger paths."""

    def __init__(self, writeHistFile=True, eventLimit=-1, trigLst=None):
        """ Initialise global variables

        Args:
            writeHistFile (bool): True to write file, False otherwise
            eventLimit (int): -1 for no event limit, value otherwise for limit
            trigLst (dict): dictionary of trigger names
        """

        self.eventCounter = 0
        self.comboCounter = 0
        # self.numTriggers = len(trigLst["Muon"]) * len(trigLst["Jet"])
        # print("Number of Combined Triggers: %d" % self.numTriggers)

        self.h_jetHt = {}
        self.h_jetMult = {}
        self.h_jetBMult = {}
        self.h_jetEta = {}
        self.h_jetPhi = {}
        self.h_jetMap = {}

        self.h_elPt = {}
        self.h_elEta = {}
        self.h_elPhi = {}
        self.h_elMap = {}

        self.h_metPt = {}
        self.h_metPhi = {}

        self.h_genMetPt = {}
        self.h_genMetPhi = {}

        self.nJet = None
        self.h_eventsPrg = ROOT.TH1D('h_eventsPrg', ';Cuts and Triggers;Total Number of Accepted Events', 16, 0, 16)
        self.h_elGenPartFlav = ROOT.TH1D('h_elGenPartFlav', 'genPartFlav_afterCriteria; GenPartFlav; '
                                                            'Number of events', 16, 0, 16)
        self.h_elGenPartIdx = ROOT.TH1D('h_elGenPartIdx', 'genPartIdx_afterCriteria; GenPartIdx; '
                                                          'Number of events', 182, -2, 180)
        self.h_elMiniPfRelIso_all = ROOT.TH1D('h_elMiniPfRelIso_all', 'elMiniPfRelIso_all;elMiniPfRelIso_all;'
                                                                      'Number of Events', 110, 0, 55)

        self.writeHistFile = writeHistFile
        self.eventLimit = eventLimit  # -1 for no limit of events fully processed
        self.trigLst = trigLst
        self.selCriteria = {}

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

    def beginJob(self, histFile=None, histDirName=None):
        """ Initialise histograms to be used and saved in output file. """

        # - Run beginJob() of Module
        Module.beginJob(self, histFile, histDirName)  # pass histFile and histDirName first passed to the PostProcessor

        # - Defining histograms to be saved to file
        self.h_jetHt['no_trigger'] = ROOT.TH1D('h_jetHt_notrigger',
                                               'no trigger ;H_{T} (GeV/c);Number of Events per 10 GeV/c', 300, 1, 3000)
        self.h_jetMult['no_trigger'] = ROOT.TH1D('h_jetMult_notrigger',
                                                 'no trigger ; Multiplicity ;Number of Events per Number of Jets',
                                                 20, 0, 20)
        self.h_jetBMult['no_trigger'] = ROOT.TH1D('h_jetBMult_notrigger',
                                                  'no trigger ;B tag Multiplicity ;Number of Events per Number of Jets',
                                                  20, 0, 20)

        # Histograms used for unit testing
        self.h_jetEta['no_trigger'] = ROOT.TH1D('h_jetEta_notrigger', 'no trigger ;Jet #eta;Number of Events per '
                                                                      '#delta#eta = 0.046', 300, -6, 8)
        self.h_jetPhi['no_trigger'] = ROOT.TH1D('h_jetPhi_notrigger', 'no trigger ;Jet #phi;Number of Events per '
                                                                      '#delta#phi = 0.046', 300, -6, 8)
        self.h_jetMap['no_trigger'] = ROOT.TH2F('h_jetMap_notrigger', 'no trigger ;Jet #eta;Jet #phi',
                                                150, -6, 6, 160, -3.2, 3.2)

        #######################
        # ELECTRON HISTOGRAMS #
        #######################
        self.h_elPt['no_trigger'] = ROOT.TH1D('h_elPt_notrigger', 'no trigger ;Electron P_{T} (GeV/c);Number of Events '
                                                                  'per 1 GeV/c', 300, 0, 300)
        self.h_elPt['prompt'] = ROOT.TH1D('h_elPt_prompt', 'prompt muons ;Electron P_{T} (GeV/c);Number of '
                                                           'Events per 1 GeV/c', 300, 0, 300)
        self.h_elPt['non-prompt'] = ROOT.TH1D('h_elPt_non-prompt',
                                              'bottom parent ;Electron P_{T} (GeV/c);Number of Events '
                                              'per 1 GeV/c', 300, 0, 300)
        self.h_elEta['no_trigger'] = ROOT.TH1D('h_elEta_notrigger', 'no trigger ;Electron #eta;Number of Events per '
                                                                    '#delta#eta = 0.046', 300, -6, 8)
        self.h_elPhi['no_trigger'] = ROOT.TH1D('h_elPhi_notrigger', 'no trigger ;Electron #phi;Number of Events per '
                                                                    '#delta#phi = 0.046', 300, -6, 8)
        self.h_elMap['no_trigger'] = ROOT.TH2F('h_elMap_notrigger', 'no trigger ;Electron #eta;Electron #phi',
                                               150, -6, 6, 160, -3.2, 3.2)
        ##################
        # MET HISTOGRAMS #
        ##################
        self.h_metPt['no_trigger'] = ROOT.TH1D('h_metPt_notrigger', 'no trigger ;MET P_{T} (GeV/c);Number of Events per'
                                                                    ' 1 GeV/c', 300, 0, 300)
        self.h_metPhi['no_trigger'] = ROOT.TH1D('h_metPhi_notrigger', 'no trigger ;MET #phi;Number of Events per '
                                                                      '#delta#phi = 0.046', 300, -6, 8)
        self.h_genMetPt['no_trigger'] = ROOT.TH1D('h_genMetPt_notrigger', 'no trigger ;GenMET P_{T} (GeV/c);Number of '
                                                                          'Events per 1GeV/c', 300, 0, 300)
        self.h_genMetPhi['no_trigger'] = ROOT.TH1D('h_genMetPhi_notrigger', 'no trigger ;GenMET #phi;Number of Events '
                                                                            'per #delta#phi = 0.046', 300, -6, 8)
        self.addObject(self.h_jetHt['no_trigger'])
        self.addObject(self.h_jetMult['no_trigger'])
        self.addObject(self.h_jetBMult['no_trigger'])
        self.addObject(self.h_jetEta['no_trigger'])
        self.addObject(self.h_jetPhi['no_trigger'])
        self.addObject(self.h_jetMap['no_trigger'])

        self.addObject(self.h_elGenPartFlav)
        self.addObject(self.h_elGenPartIdx)
        self.addObject(self.h_elMiniPfRelIso_all)
        self.addObject(self.h_elPt['no_trigger'])
        self.addObject(self.h_elPt['prompt'])
        self.addObject(self.h_elPt['non-prompt'])
        self.addObject(self.h_elEta['no_trigger'])
        self.addObject(self.h_elPhi['no_trigger'])
        self.addObject(self.h_elMap['no_trigger'])
        self.addObject(self.h_metPt['no_trigger'])
        self.addObject(self.h_metPhi['no_trigger'])
        self.addObject(self.h_genMetPt['no_trigger'])
        self.addObject(self.h_genMetPhi['no_trigger'])

        for key in self.trigLst:
            if not key.find("Mu") == -1: continue
            for trgPath in self.trigLst[key]:
                self.h_jetHt[trgPath] = ROOT.TH1D('h_jetHt_' + trgPath, trgPath + ';H_{T} (GeV/c);Number of Events'
                                                                                  ' per 10 GeV/c', 300, 1, 3000)
                self.addObject(self.h_jetHt[trgPath])
                self.h_jetMult[trgPath] = ROOT.TH1D('h_jetMult_' + trgPath, trgPath + ';Multiplicity;Number of Events'
                                                                                      ' per Number of Jets', 20, 0, 20)
                self.addObject(self.h_jetMult[trgPath])
                self.h_jetBMult[trgPath] = ROOT.TH1D('h_jetBMult_' + trgPath, trgPath + ';Multiplicity;Number of Events'
                                                                                        ' /Number of Jets', 20, 0, 20)
                self.addObject(self.h_jetBMult[trgPath])
                self.h_jetEta[trgPath] = ROOT.TH1D('h_jetEta_' + trgPath, trgPath + ';Jet #eta;Number of Events per'
                                                                                    ' #delta#eta = 0.046', 300, -6, 8)
                self.addObject(self.h_jetEta[trgPath])
                self.h_jetPhi[trgPath] = ROOT.TH1D('h_jetPhi_' + trgPath, trgPath + ';Jet #phi;Number of Events per'
                                                                                    ' #delta#phi = 0.046', 300, -6, 8)
                self.addObject(self.h_jetPhi[trgPath])
                self.h_jetMap[trgPath] = ROOT.TH2F('h_jetMap_' + trgPath,  trgPath + ';Jet #eta;Jet #phi',
                                                   150, -3, 3, 160, -3.2, 3.2)
                self.addObject(self.h_jetMap[trgPath])

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
                                                                                          'Events per #delta#phi=0.046',
                                                      300, -6, 8)
                self.addObject(self.h_genMetPhi[trgPath])

        self.addObject(self.h_eventsPrg)

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
        for nj, jet in enumerate(jets):
            # - Check jet passes 2017 Tight Jet ID https://twiki.cern.ch/twiki/bin/view/CMS/JetID13TeVRun2017
            # - Minimum 30GeV Pt on the jets
            # - Only look at jets within |eta| < 2.4
            if jet.jetId < self.selCriteria["minJetId"] or jet.pt < self.selCriteria["minJetPt"]: continue
            if abs(jet.eta) > self.selCriteria["maxObjEta"]: continue
            if self.selCriteria["jetCleanmask"] == "Y" and jet.cleanmask is False: continue
            nJetsPass += 1
            # Count b-tagged jets with DeepFlavourB algorithm at the medium working point
            # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation94X
            if jet.btagDeepFlavB > 0.7489:
                nBtagsPass += 1
        return nJetsPass, nBtagsPass

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
            if self.selCriteria["mvaWP"] == 90 and el.mvaFall17Iso_WP90 is False: continue
            if 1.4442 < abs(el.eta) < 1.566: continue

            #  el.convVeto or el.sieie<0.0106 or el.lostHits<=1
            #  or el.hoe <(0.046 + 1.16/(el.EtaSC)+ 0.0324*(rho)/(EtaSC))
            nElsPass += 1
            ElsPassIdx = ne

        return nElsPass, ElsPassIdx

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

        metPt = getattr(met, "pt")
        metPhi = getattr(met, "phi")
        genMetPt = getattr(genMet, "pt")
        genMetPhi = getattr(genMet, "pt")

        trigPath = {}
        for key in self.trigLst:
            if key.find("_OR_") == -1:
                for tg in self.trigLst[key]:
                    trigPath.update({tg: getattr(hltObj, tg)})
            else:
                for tg in self.trigLst[key]:
                    trigPath.update({tg: False})

        if trigPath['Ele32_WPTight_Gsf'] is True or trigPath['PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2'] is True:
            trigPath['Ele32_WPTight_Gsf_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2'] = True
        if trigPath['Ele35_WPTight_Gsf'] is True or trigPath['PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2'] is True:
            trigPath['Ele35_WPTight_Gsf_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2'] = True
        if trigPath['Ele38_WPTight_Gsf'] is True or trigPath['PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2'] is True:
            trigPath['Ele38_WPTight_Gsf_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2'] = True

        jetHt = {"notrig": 0}
        for key in self.trigLst:
            if not key.find("Mu") == -1: continue
            for tg in self.trigLst[key]:
                jetHt.update({tg: 0})

        # jetHt2 = {"notrig": 0}
        # for key in self.trigLst:
        #     if not key.find("Mu") == -1: continue
        #     for tg in self.trigLst[key]:
        #         jetHt2.update({tg: 0})

        nJetPass, nBtagPass = self.jetCriteria(jets)
        nMuonPass, MuonPassIdx = self.muonCriteria(muons)
        nElPass, ElPassIdx = self.electronCriteria(electrons)

        ###########################
        # Electron Trigger Checks #
        ###########################
        if nJetPass > self.selCriteria["minNJet"] and nElPass == self.selCriteria["minNElectron"] \
                and nMuonPass == self.selCriteria["minNMuon"] and nBtagPass > self.selCriteria["minNBJet"]:
            for ne, electron in enumerate(electrons):
                if ElPassIdx == ne:
                    self.h_elMiniPfRelIso_all.Fill(electron.miniPFRelIso_all)
                    self.h_elGenPartFlav.Fill(electron.genPartFlav)
                    self.h_elGenPartIdx.Fill(electron.genPartIdx)
                    self.h_elEta['no_trigger'].Fill(electron.eta)
                    self.h_elPhi['no_trigger'].Fill(electron.phi)
                    self.h_elMap['no_trigger'].Fill(electron.eta, electron.phi)

                    self.h_elPt['no_trigger'].Fill(electron.pt)
                    for key in self.trigLst:
                        if not key.find("Mu") == -1: continue
                        for tg in self.trigLst[key]:
                            if trigPath[tg]:
                                self.h_elPt[tg].Fill(electron.pt)
                                self.h_elEta[tg].Fill(electron.eta)
                                self.h_elPhi[tg].Fill(electron.phi)
                                self.h_elMap[tg].Fill(electron.eta, electron.phi)
                    if electron.genPartFlav == 1:
                        self.h_elPt['prompt'].Fill(electron.pt)
                    else:
                        self.h_elPt['non-prompt'].Fill(electron.pt)

            for nj, jet in enumerate(jets):
                for key in self.trigLst:
                    if not key.find("Mu") == -1: continue
                    for tg in self.trigLst[key]:
                        if trigPath[tg]:
                            jetHt[tg] += jet.pt
                            self.h_jetEta[tg].Fill(jet.eta)
                            self.h_jetPhi[tg].Fill(jet.phi)
                            self.h_jetMap[tg].Fill(jet.eta, jet.phi)
                jetHt["notrig"] += jet.pt
                self.h_jetEta['no_trigger'].Fill(jet.eta)
                self.h_jetPhi['no_trigger'].Fill(jet.phi)
                self.h_jetMap['no_trigger'].Fill(jet.eta, jet.phi)

            self.h_jetHt['no_trigger'].Fill(jetHt["notrig"])
            self.h_metPt['no_trigger'].Fill(metPt)
            self.h_metPhi['no_trigger'].Fill(metPhi)
            self.h_genMetPt['no_trigger'].Fill(genMetPt)
            self.h_genMetPhi['no_trigger'].Fill(genMetPhi)
            self.h_jetMult['no_trigger'].Fill(nJetPass)
            self.h_jetBMult['no_trigger'].Fill(nBtagPass)
            self.h_eventsPrg.Fill(1)
            i = 0
            for key in self.trigLst:
                if not key.find("Mu") == -1: continue
                for tg in self.trigLst[key]:
                    if trigPath[tg]:
                        self.h_jetHt[tg].Fill(jetHt[tg])
                        self.h_metPt[tg].Fill(metPt)
                        self.h_metPhi[tg].Fill(metPhi)
                        self.h_genMetPt[tg].Fill(genMetPt)
                        self.h_genMetPhi[tg].Fill(genMetPhi)
                        self.h_jetMult[tg].Fill(nJetPass)
                        self.h_jetBMult[tg].Fill(nBtagPass)
                        self.h_eventsPrg.Fill(2 + i)
                        i += 1

            # for nj, jet in enumerate(jets):
            #     for key in self.trigLst:
            #         if not key.find("Mu") == -1: continue
            #         for tg in self.trigLst[key]:
            #             if trigPath[tg]:
            #                 jetHt2[tg] += jet.pt
            #                 self.h_jetEta[tg].Fill(jet.eta)
            #                 self.h_jetPhi[tg].Fill(jet.phi)
            #                 self.h_jetMap[tg].Fill(jet.eta, jet.phi)
            #     jetHt2["notrig"] += jet.pt
            #     self.h_jetEta['no_trigger'].Fill(jet.eta)
            #     self.h_jetPhi['no_trigger'].Fill(jet.phi)
            #     self.h_jetMap['no_trigger'].Fill(jet.eta, jet.phi)
            # for ne, el in enumerate(electrons):
            #     if ElPassIdx == ne:
            #         for key in self.trigLst:
            #             if not key.find("Mu") == -1: continue
            #             for tg in self.trigLst[key]:
            #                 if trigPath[tg]:
            #                     self.h_elPt[tg].Fill(el.pt)
            #                     self.h_elEta[tg].Fill(el.eta)
            #                     self.h_elPhi[tg].Fill(el.phi)
            #                     self.h_elMap[tg].Fill(el.eta, el.phi)
            #         self.h_elPt['no_trigger'].Fill(el.pt)
            #         self.h_elEta['no_trigger'].Fill(el.eta)
            #         self.h_elPhi['no_trigger'].Fill(el.phi)
            #         self.h_elMap['no_trigger'].Fill(el.eta, el.phi)
            #
            # self.h_jetHt['no_trigger'].Fill(jetHt2["notrig"])
            # self.h_metPt['no_trigger'].Fill(metPt)
            # self.h_metPhi['no_trigger'].Fill(metPhi)
            # self.h_genMetPt['no_trigger'].Fill(genMetPt)
            # self.h_genMetPhi['no_trigger'].Fill(genMetPhi)
            # self.h_jetMult['no_trigger'].Fill(nJetPass)
            # self.h_jetBMult['no_trigger'].Fill(nBtagPass)
            # for key in self.trigLst:
            #     if not key.find("Mu") == -1: continue
            #     for tg in self.trigLst[key]:
            #         if trigPath[tg]:
            #             self.h_jetHt[tg].Fill(jetHt[tg])
            #             self.h_metPt[tg].Fill(metPt)
            #             self.h_metPhi[tg].Fill(metPhi)
            #             self.h_genMetPt[tg].Fill(genMetPt)
            #             self.h_genMetPhi[tg].Fill(genMetPhi)
            #             self.h_jetMult[tg].Fill(nJetPass)
            #             self.h_jetBMult[tg].Fill(nBtagPass)
            #             self.h_eventsPrg.Fill(2 + i)
            #             i += 1
        
        return True
