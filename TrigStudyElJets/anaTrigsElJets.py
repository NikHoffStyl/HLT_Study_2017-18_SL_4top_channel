#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Jan 2019

@author: NikHoffStyl
"""
from __future__ import (division, print_function)

import ROOT
from ROOT import TLatex

# from importlib import import_module

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


class TriggerStudy(Module):
    """This class HistogramMaker() fills histograms of required variables of jets, muons, electrons and MET;
    for different combinations of trigger paths."""

    def __init__(self, writeHistFile=True, eventLimit=-1, trigLst=None, era=None):
        """
        Initialise global variables

        Args:
            writeHistFile (bool): True to write file, False otherwise
            eventLimit (int): -1 for no event limit, value otherwise for limit
            trigLst (dict): dictionary of trigger names
        """

        self.era = era
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
        #
        # self.h_genMetPt = {}
        # self.h_genMetPhi = {}

        self.nJet = None
        self.h_eventsPrg = ROOT.TH1D('h_eventsPrg', ';Cuts and Triggers;Total Number of Accepted Events', 16, 0, 16)
        # self.h_elGenPartFlav = ROOT.TH1D('h_elGenPartFlav', 'genPartFlav_afterCriteria; GenPartFlav; '
        #                                                     'Number of events', 16, 0, 16)
        # self.h_elGenPartIdx = ROOT.TH1D('h_elGenPartIdx', 'genPartIdx_afterCriteria; GenPartIdx; '
        #                                                   'Number of events', 182, -2, 180)
        self.h_elMiniPfRelIso_all = ROOT.TH1D('h_elMiniPfRelIso_all', 'elMiniPfRelIso_all;elMiniPfRelIso_all;'
                                                                      'Number of Events', 110, 0, 55)

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

    def beginJob(self, histFile=None, histDirName=None):
        """ Initialise histograms to be used and saved in output file. """

        # - Run beginJob() of Module
        Module.beginJob(self, histFile, histDirName)  # pass histFile and histDirName first passed to the PostProcessor

        ##################
        # JET HISTOGRAMS #
        ##################
        self.h_jetHt['no_trigger'] = ROOT.TH1D('h_jetHt_notrigger',
                                               'no trigger ;H_{T} (GeV/c);Number of Events per 10 GeV/c', 300, 1, 3000)
        self.h_jetMult['no_trigger'] = ROOT.TH1D('h_jetMult_notrigger',
                                                 'no trigger ; Multiplicity ;Number of Events per Number of Jets',
                                                 20, 0, 20)
        self.h_jetBMult['no_trigger'] = ROOT.TH1D('h_jetBMult_notrigger',
                                                  'no trigger ;B tag Multiplicity ;Number of Events per Number of Jets',
                                                  20, 0, 20)
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
        self.h_elPt['prompt'] = ROOT.TH1D('h_elPt_prompt', 'prompt electrons ;Electron P_{T} (GeV/c);Number of '
                                                           'Events per 1 GeV/c', 300, 0, 300)
        self.h_elPt['non-prompt'] = ROOT.TH1D('h_elPt_non-prompt',
                                              'non-prompt electrons ;Electron P_{T} (GeV/c);Number of Events '
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
        # self.h_genMetPt['no_trigger'] = ROOT.TH1D('h_genMetPt_notrigger', 'no trigger ;GenMET P_{T} (GeV/c);Number of '
        #                                                                   'Events per 1GeV/c', 300, 0, 300)
        # self.h_genMetPhi['no_trigger'] = ROOT.TH1D('h_genMetPhi_notrigger', 'no trigger ;GenMET #phi;Number of Events '
        #                                                                     'per #delta#phi = 0.046', 300, -6, 8)

        self.addObject(self.h_jetHt['no_trigger'])
        self.addObject(self.h_jetMult['no_trigger'])
        self.addObject(self.h_jetBMult['no_trigger'])
        self.addObject(self.h_jetEta['no_trigger'])
        self.addObject(self.h_jetPhi['no_trigger'])
        self.addObject(self.h_jetMap['no_trigger'])

        # self.addObject(self.h_elGenPartFlav)
        # self.addObject(self.h_elGenPartIdx)
        self.addObject(self.h_elMiniPfRelIso_all)
        self.addObject(self.h_elPt['no_trigger'])
        self.addObject(self.h_elPt['prompt'])
        self.addObject(self.h_elPt['non-prompt'])
        self.addObject(self.h_elEta['no_trigger'])
        self.addObject(self.h_elPhi['no_trigger'])
        self.addObject(self.h_elMap['no_trigger'])

        self.addObject(self.h_metPt['no_trigger'])
        self.addObject(self.h_metPhi['no_trigger'])
        # self.addObject(self.h_genMetPt['no_trigger'])
        # self.addObject(self.h_genMetPhi['no_trigger'])

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
                #
                # self.h_genMetPt[trgPath] = ROOT.TH1D('h_genMetPt_' + trgPath, trgPath + ';GenMET P_{T} (GeV/c);Number '
                #                                                                         'of Events per 1 GeV/c',
                #                                      300, 0, 300)
                # self.addObject(self.h_genMetPt[trgPath])
                # self.h_genMetPhi[trgPath] = ROOT.TH1D('h_genMetPhi_' + trgPath, trgPath + ';GenMET #phi;Number of '
                #                                                                           'Events per #delta#phi=0.046',
                #                                       300, -6, 8)
                # self.addObject(self.h_genMetPhi[trgPath])

        self.addObject(self.h_eventsPrg)

    def jetCriteria(self, jets):
        """
            Return the number of accepted jets and the number of accepted b-tagged jets

            Args:
                jets (Collection): Information of jets
            Returns:
                (tuple): tuple containing:
                    nJetsPass (int): number of jets
                    JetPassIdx (list): list of jet indices that passed cuts
                    nBtagsPass (int): number of b-tagged jets
        """
        nJetsPass = 0
        nBtagsPass = 0
        JetsPassIdx = []
        for nj, jet in enumerate(jets):
            # - Check jet passes 2017 Tight Jet ID https://twiki.cern.ch/twiki/bin/view/CMS/JetID13TeVRun2017
            # - Minimum 30GeV Pt on the jets
            # - Only look at jets within |eta| < 2.4
            if jet.jetId < self.selCriteria["minJetId"] or jet.pt < self.selCriteria["minJetPt"]: continue
            if abs(jet.eta) > self.selCriteria["maxObjEta"]: continue
            if self.selCriteria["jetCleanmask"] == "Y" and jet.cleanmask is False: continue
            nJetsPass += 1
            JetsPassIdx.append(nj)
            # Count b-tagged jets with DeepFlavourB algorithm at the medium working point
            # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation94X
            if jet.btagDeepFlavB > 0.7489:
                nBtagsPass += 1
        return nJetsPass, JetsPassIdx, nBtagsPass

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
        # genMet = Object(event, "GenMET")

        metPt = getattr(met, "pt")
        metPhi = getattr(met, "phi")
        # genMetPt = getattr(genMet, "pt")
        # genMetPhi = getattr(genMet, "pt")

        trigPath = {}
        for key in self.trigLst:
            if key.find("_OR_") == -1:
                for tg in self.trigLst[key]:
                    trigPath.update({tg: getattr(hltObj, tg)})
            else:
                for tg in self.trigLst[key]:
                    trigPath.update({tg: False})

        if self.era == "17AB":
            if trigPath['Ele35_WPTight_Gsf'] is True or trigPath['PFHT380_SixJet32_DoubleBTagCSV_p075'] is True:
                trigPath['Ele35_WPTight_Gsf_PFHT380_SixPFJet32_DoublePFBTagCSV_p075'] = True
        elif self.era == "17C":
            if trigPath['Ele35_WPTight_Gsf'] is True or trigPath['PFHT380_SixPFJet32_DoublePFBTagCSV_2p2'] is True:
                trigPath['Ele35_WPTight_Gsf_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2'] = True
        elif self.era == "17DEF":
            if trigPath['Ele32_WPTight_Gsf'] is True or trigPath['PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2'] is True:
                trigPath['Ele32_WPTight_Gsf_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2'] = True
        else:
            print("No era specified. Stopped Analysis.")
            return False

        jetHt = {"notrig": 0}
        for key in self.trigLst:
            if not key.find("Mu") == -1: continue
            for tg in self.trigLst[key]:
                jetHt.update({tg: 0})

        nJetPass, JetPassIdx, nBtagPass = self.jetCriteria(jets)
        nMuonPass, MuonPassIdx = self.muonCriteria(muons)
        nElPass, ElPassIdx = self.electronCriteria(electrons)

        ###########################
        # Electron Trigger Checks #
        ###########################
        if nJetPass > self.selCriteria["minNJet"] and nElPass == self.selCriteria["minNElectron"] \
                and nMuonPass == self.selCriteria["minNMuon"] and nBtagPass > self.selCriteria["minNBJet"]:
            for ne, electron in enumerate(electrons):
                if not ElPassIdx == ne: continue
                self.h_elMiniPfRelIso_all.Fill(electron.miniPFRelIso_all)
                # self.h_elGenPartFlav.Fill(electron.genPartFlav)
                # self.h_elGenPartIdx.Fill(electron.genPartIdx)
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
                # if electron.genPartFlav == 1:
                #     self.h_elPt['prompt'].Fill(electron.pt)
                # else:
                #     self.h_elPt['non-prompt'].Fill(electron.pt)

            for nj, jet in enumerate(jets):
                if nj not in JetPassIdx: continue
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
            # self.h_genMetPt['no_trigger'].Fill(genMetPt)
            # self.h_genMetPhi['no_trigger'].Fill(genMetPhi)
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
                        # self.h_genMetPt[tg].Fill(genMetPt)
                        # self.h_genMetPhi[tg].Fill(genMetPhi)
                        self.h_jetMult[tg].Fill(nJetPass)
                        self.h_jetBMult[tg].Fill(nBtagPass)
                        self.h_eventsPrg.Fill(2 + i)
                        i += 1
        
        return True


def process_arguments():
    """
    Processes command line arguments
    Returns:
        args: list of commandline arguments

    """

    parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--inputLFN", choices=["tt_semilep94", "ttjets94", "tttt94", "tttt_weights", "wjets",
                                                     "tt_semilep102_17B", "tttt102_17B",
                                                     "tt_semilep102_17C", "tttt102_17C",
                                                     "tt_semilep102_17DEF", "tttt102_17DEF",
                                                     "dataHTMHT17B", "dataSMu17B", "dataSEl17B",
                                                     "dataHTMHT17C", "dataSMu17C", "dataSEl17C",
                                                     "dataHTMHT17D", "dataSMu17D", "dataSEl17D",
                                                     "dataHTMHT17E", "dataSMu17E", "dataSEl17E",
                                                     "dataHTMHT17F", "dataSMu17F", "dataSEl17F"],
                        default="tttt102", help="Set list of input files")
    parser.add_argument("-r", "--redirector", choices=["xrd-global", "xrdUS", "xrdEU_Asia", "eos", "iihe", "local"],
                        default="xrd-global", help="Sets redirector to query locations for LFN")
    parser.add_argument("-nw", "--noWriteFile", action="store_true",
                        help="Does not output a ROOT file, which contains the histograms.")
    parser.add_argument("-e", "--eventLimit", type=int, default=-1,
                        help="Set a limit to the number of events.")
    parser.add_argument("-lf", "--fileLimit", type=int, default=-1,
                        help="Set a limit to the number of files to run through.")
    args = parser.parse_args()
    return args


def chooseRedirector(arg):
    """
    Sets redirector using keyword given in commandline arguments
    Args:
        arg: command line argument list

    Returns:
        redir: redirector, where redirector + LFN = PFN

    """
    if arg.redirector == "xrd-global":
        redir = "root://cms-xrd-global.cern.ch/"
    elif arg.redirector == "xrdUS":
        redir = "root://cmsxrootd.fnal.gov/"
    elif arg.redirector == "xrdEU_Asia":
        redir = "root://xrootd-cms.infn.it/"
    elif arg.redirector == "eos":
        redir = "root://cmseos.fnal.gov/"
    elif arg.redirector == "iihe":
        redir = "dcap://maite.iihe.ac.be/pnfs/iihe/cms/ph/sc4/"
    elif arg.redirector == "local":
        if arg.inputLFN == "ttjets":
            redir = "../../myInFiles/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8/"
        elif arg.inputLFN == "tttt_weights":
            redir = "../../myInFiles/TTTTweights/"
        elif arg.inputLFN == "wjets":
            redir = "../../myInFiles/Wjets/"
        elif arg.inputLFN == "tttt":
            redir = "../../myInFiles/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/"
        else:
            return ""
    else:
        return ""
    return redir


def getFileContents(fileName, elmList):
    """

    Args:
        fileName (string): path/to/file
        elmList (bool): if true then dictionary elements are lists else strings

    Returns:
        fileContents (dictionary): file contents given as a dictionary

    """
    fileContents = {}
    with open(fileName) as f:
        for line in f:
            if line.find(":") == -1: continue
            (key1, val) = line.split(": ")
            c = len(val) - 1
            val = val[0:c]
            if elmList is False:
                fileContents[key1] = val
            else:
                fileContents[key1] = val.split(", ")
    return fileContents


def ioFiles(arg, selCrit):
    """
    Input and Output file

    Args:
        arg : command line arguments
        selCrit (dictionary): selection criteria

    Returns:
        inLFNList (string): list of file datasets
        postFix (string): string added to output file
        outFile (string): output file name

    Open the text list of files as read-only ("r" option), use as pairs to add proper postfix to output file
    you may want to change path to suit your file ordering

    """
    if arg.inputLFN == "dataHTMHT17B":
        inLFNList = open("../myInFiles/data/HTMHT_Run2017B-Nano14Dec2018-v1.txt", "r")
        postFix = "dataHTMHT17B"
        outFile = "OutFiles/Histograms/dataHTMHT17B_6Jets1El{0}jPt.root".format(selCrit["minJetPt"])
    elif arg.inputLFN == "dataSMu17B":
        inLFNList = open("../myInFiles/data/SingleMuon_Run2017B-Nano14Dec2018-v1.txt", "r")
        postFix = "dataSMu17B"
        outFile = "OutFiles/Histograms/dataSMu17B_6Jets1El{0}jPt.root".format(selCrit["minJetPt"])
    elif arg.inputLFN == "dataSEl17B":
        inLFNList = open("../myInFiles/data/SingleElectron_Run2017B-Nano14Dec2018-v1.txt", "r")
        postFix = "dataSEl17B"
        outFile = "OutFiles/Histograms/dataSEl17B_6Jets1El{0}jPt.root".format(selCrit["minJetPt"])
    elif arg.inputLFN == "dataHTMHT17C":
        inLFNList = open("../myInFiles/data/HTMHT_Run2017C-Nano14Dec2018-v1.txt", "r")
        postFix = "dataHTMHT17C"
        outFile = "OutFiles/Histograms/dataHTMHT17C_6Jets1El{0}jPt.root".format(selCrit["minJetPt"])
    elif arg.inputLFN == "dataSMu17C":
        inLFNList = open("../myInFiles/data/SingleMuon_Run2017C-Nano14Dec2018-v1.txt", "r")
        postFix = "dataSMu17C"
        outFile = "OutFiles/Histograms/dataSMu17C_6Jets1El{0}jPt.root".format(selCrit["minJetPt"])
    elif arg.inputLFN == "dataSEl17C":
        inLFNList = open("../myInFiles/data/SingleElectron_Run2017C-Nano14Dec2018-v1.txt", "r")
        postFix = "dataSEl17C"
        outFile = "OutFiles/Histograms/dataSEl17C_6Jets1El{0}jPt.root".format(selCrit["minJetPt"])
    elif arg.inputLFN == "dataHTMHT17D":
        inLFNList = open("../myInFiles/data/HTMHT_Run2017D-Nano14Dec2018-v1.txt", "r")
        postFix = "dataHTMHT17D"
        outFile = "OutFiles/Histograms/dataHTMHT17D_6Jets1El{0}jPt.root".format(selCrit["minJetPt"])
    elif arg.inputLFN == "dataSMu17D":
        inLFNList = open("../myInFiles/data/SingleMuon_Run2017D-Nano14Dec2018-v1.txt", "r")
        postFix = "dataSMu17D"
        outFile = "OutFiles/Histograms/dataSMu17D_6Jets1El{0}jPt.root".format(selCrit["minJetPt"])
    elif arg.inputLFN == "dataSEl17D":
        inLFNList = open("../myInFiles/data/SingleElectron_Run2017D-Nano14Dec2018-v1.txt", "r")
        postFix = "dataSEl17D"
        outFile = "OutFiles/Histograms/dataSEl17D_6Jets1El{0}jPt.root".format(selCrit["minJetPt"])
    elif arg.inputLFN == "dataHTMHT17E":
        inLFNList = open("../myInFiles/data/HTMHT_Run2017E-Nano14Dec2018-v1.txt", "r")
        postFix = "dataHTMHT17E"
        outFile = "OutFiles/Histograms/dataHTMHT17E_6Jets1El{0}jPt.root".format(selCrit["minJetPt"])
    elif arg.inputLFN == "dataSMu17E":
        inLFNList = open("../myInFiles/data/SingleMuon_Run2017E-Nano14Dec2018-v1.txt", "r")
        postFix = "dataSMu17E"
        outFile = "OutFiles/Histograms/dataSMu17E_6Jets1El{0}jPt.root".format(selCrit["minJetPt"])
    elif arg.inputLFN == "dataSEl17E":
        inLFNList = open("../myInFiles/data/SingleElectron_Run2017E-Nano14Dec2018-v1.txt", "r")
        postFix = "dataSEl17E"
        outFile = "OutFiles/Histograms/dataSEl17E_6Jets1El{0}jPt.root".format(selCrit["minJetPt"])
    elif arg.inputLFN == "dataHTMHT17F":
        inLFNList = open("../myInFiles/data/HTMHT_Run2017F-Nano14Dec2018-v1.txt", "r")
        postFix = "dataHTMHT17F"
        outFile = "OutFiles/Histograms/dataHTMHT17F_6Jets1El{0}jPt.root".format(selCrit["minJetPt"])
    elif arg.inputLFN == "dataSMu17F":
        inLFNList = open("../myInFiles/data/SingleMuon_Run2017F-Nano14Dec2018-v1.txt", "r")
        postFix = "dataSMu17F"
        outFile = "OutFiles/Histograms/dataSMu17F_6Jets1El{0}jPt.root".format(selCrit["minJetPt"])
    elif arg.inputLFN == "dataSEl17F":
        inLFNList = open("../myInFiles/data/SingleElectron_Run2017F-Nano14Dec2018-v1.txt", "r")
        postFix = "dataSEl17F"
        outFile = "OutFiles/Histograms/dataSEl17F_6Jets1El{0}jPt.root".format(selCrit["minJetPt"])

    elif not arg.inputLFN.find("tt_semilep102_17") == -1:
        inLFNList = open("../myInFiles/mc/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_102X.txt", "r")
        postFix = "TTToSemiLep102X"
        if arg.inputLFN == "tt_semilep102_17B":
            outFile = "OutFiles/Histograms/TTToSemiLep102X_17B_6Jets1El{0}jPt.root".format(selCrit["minJetPt"])
        elif arg.inputLFN == "tt_semilep102_17C":
            outFile = "OutFiles/Histograms/TTToSemiLep102X_17C_6Jets1El{0}jPt.root".format(selCrit["minJetPt"])
        elif arg.inputLFN == "tt_semilep102_17DEF":
            outFile = "OutFiles/Histograms/TTToSemiLep102X_17DEF_6Jets1El{0}jPt.root".format(selCrit["minJetPt"])

    elif arg.inputLFN == "tt_semilep94":  # tt + jets MC
        inLFNList = open("../myInFiles/mc/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_94X.txt", "r")
        # inLFNList = open("../NanoAODTools/StandaloneExamples/Infiles/TTJets_"
        #                     "SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8.txt", "r")
        postFix = "TTToSemiLep94X"
        outFile = "OutFiles/Histograms/TTToSemiLep94X_6Jets1El{0}jPt.root".format(selCrit["minJetPt"])
    elif arg.inputLFN == "ttjets94":
        if arg.redirector == "local":
            inLFNList = open(
                "../../myInFiles/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8/fileNames.txt", "r")
        else:
            inLFNList = open("../myInFiles/mc/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8_94X.txt", "r")
        postFix = "TTJets_SL_94"
        outFile = "OutFiles/Histograms/TT94_6Jets1El{0}jPt.root".format(selCrit["minJetPt"])
    elif arg.inputLFN == "tttt_weights":
        if arg.redirector == "local":
            inLFNList = open("../../myInFiles/TTTTweights/TTTTweights_files.txt", "r")
        else:
            inLFNList = open("../myInFiles/mc/TTTTweights_files.txt", "r")
        postFix = "TTTT_PSWeights"
        outFile = "OutFiles/Histograms/TTTTweights.root"
    elif arg.inputLFN == "wjets":  # W (to Lep + Nu) + jets
        if arg.redirector == "local":
            inLFNList = open("../../myInFiles/Wjets/Wjets_files.txt", "r")
        else:
            inLFNList = open("../myInFiles/mc/Wjets_files.txt", "r")
        postFix = "WJetsToLNu"
        outFile = "OutFiles/Histograms/Wjets.root"
    elif arg.inputLFN == "tttt94":  # tttt MC
        if arg.redirector == "local":
            inLFNList = open("../../myInFiles/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/fileNames.txt", "r")
        else:
            inLFNList = open("../myInFiles/mc/TTTT_TuneCP5_13TeV-amcatnlo-pythia8_94X.txt", "r")
        postFix = "TTTT94"
        outFile = "OutFiles/Histograms/TTTT94X_6Jets1El{0}jPt_test.root".format(selCrit["minJetPt"])
    elif not arg.inputLFN.find("tttt102_17") == -1:  # tttt MC
        if arg.redirector == "local":
            inLFNList = open("../../myInFiles/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/fileNames.txt", "r")
        else:
            inLFNList = open("../myInFiles/mc/TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_102X.txt", "r")
        postFix = "TTTT102"
        if arg.inputLFN == "tttt102_17B":
            outFile = "OutFiles/Histograms/TTTT102X_17B_6Jets1El{0}jPt.root".format(selCrit["minJetPt"])
        elif arg.inputLFN == "tttt102_17C":
            outFile = "OutFiles/Histograms/TTTT102X_17C_6Jets1El{0}jPt.root".format(selCrit["minJetPt"])
        elif arg.inputLFN == "tttt102_17DEF":
            outFile = "OutFiles/Histograms/TTTT102X_17DEF_6Jets1El{0}jPt.root".format(selCrit["minJetPt"])

    else:
        inLFNList = None
        postFix = None
        outFile = None

    return inLFNList, postFix, outFile
