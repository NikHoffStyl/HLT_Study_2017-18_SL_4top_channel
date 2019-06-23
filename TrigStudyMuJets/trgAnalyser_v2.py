#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Created on May 2019

    @author: NikHoffStyl
    """
from __future__ import (division, print_function)
import ROOT
import time
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

##
#  Change global variables as needed
##
pathToTrigLists = "/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/myInFiles/"
pathToSelectionCriteria = "/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/TrigStudyMuJets"


###


def process_arguments():
    """
    Processes command line arguments
    Returns:
        args: list of commandline arguments

    """

    parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-fnp", "--fileName", help="path/to/fileName")
    parser.add_argument("-era", "--era", choices=["17B", "17C", "17DEF", "18"], help="era")
    parser.add_argument("-nw", "--noWriteFile", action="store_true",
                        help="Does not output a ROOT file, which contains the histograms.")
    parser.add_argument("-e", "--eventLimit", type=int, default=-1,
                        help="Set a limit to the number of events.")
    parser.add_argument("-o", "--outputName", default="_v", help="Set name of output file")
    args = parser.parse_args()
    return args


def findEraRootFiles(path, verbose=False, FullPaths=True):
    """
    Find Root files in a given directory/path.
    Args:
        path (string): directory
        verbose (bool): print to stdout if true
        FullPaths (bool): return path plus file name in list elements

    Returns: files (list): list of names of root files in the directory given as argument

    """
    files = []
    if not path[-1] == '/': path += '/'
    if verbose: print(' >> Looking for files in path: ' + path)
    for f in os.listdir(path):
        if not f[-5:] == '.root': continue
        # if era != "all" and era not in f[:-5]: continue
        if verbose: print(' >> Adding file: ', f)
        files.append(f)
    if FullPaths: files = [path + x for x in files]
    if len(files) == 0: print('[ERROR]: No root files found in: ' + path)
    return files


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
            if line.find(":") == -1:
                continue
            (key1, val) = line.split(": ")
            c = len(val) - 1
            val = val[0:c]
            if elmList is False:
                fileContents[key1] = val
            else:
                fileContents[key1] = val.split(", ")

    return fileContents


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
        self.eventId = {}
        self.runId = {}
        self.lumi = {}
        self.h_jetHt = {}
        self.h_jetMult = {}
        self.h_jetBMult = {}
        self.h_jetEta = {}
        self.h_jetPhi = {}
        self.h_jetMap = {}
        self.h_muonPtMap = {}
        self.h_muonPt = {}
        self.h_muonPtnomedium = {}
        self.h_mediumMuonPt = {}
        self.h_mediumMuonMult = {}
        self.h_mediumMuonTightPt = {}
        self.h_muonEta = {}
        self.h_muonPhi = {}
        self.h_muonMap = {}
        self.h_muonIsolation = {}
        self.h_muonIsoPt = {}
        self.h_muonEtaNomedium = {}
        self.h_muonPhiNomedium = {}
        self.h_muonMapNomedium = {}
        self.h_muonIsolationNomedium = {}
        self.h_muonIsoPtNomedium = {}
        self.h_metPt = {}
        self.h_metPhi = {}

        self.h_genMetPt = {}
        self.h_genMetPhi = {}

        self.nJet = None
        self.h_eventsPrg = ROOT.TH1D('h_eventsPrg', ';Selection Steps;Total Number of Accepted Events', 16, 0, 16)
        if not self.era.find('mc') == -1:
            self.h_muonGenPartFlav = ROOT.TH1D('h_muonGenPartFlav', 'genPartFlav_afterCriteria; GenPartFlav; '
                                                                    'Number of events', 16, 0, 16)
            self.h_muonGenPartIdx = ROOT.TH1D('h_muonGenPartIdx', 'genPartIdx_afterCriteria; GenPartIdx; '
                                                                  'Number of events', 182, -2, 180)
        self.h_muonRelIso04_all = ROOT.TH1D('h_muonRelIso04_all', 'muonRelIso04_all;muonRelIso04_all;Number of Events',
                                            50, 0, 0.2)

        self.writeHistFile = writeHistFile
        self.eventLimit = eventLimit  # -1 for no limit of events fully processed
        self.trigLst = trigLst

        self.selCriteria = {}
        with open(pathToSelectionCriteria + "/selectionCriteria.txt") as f:
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
        Module.beginJob(self, histFile, histDirName)

        # self.runId['no_trigger'] = ROOT.TH1D('h_runId_notrigger', 'no trigger ; run; Number of Events', 1000000, 0, 1000000)
        # self.eventId['no_trigger'] = ROOT.TH1D('h_runId_notrigger', 'no trigger ;event; Number of Events', 1000000, 0, 1000000)
        # self.lumi['no_trigger'] = ROOT.TH1D('h_runId_notrigger', 'no trigger ;luminosityBlock; Number of Events', 1000000, 0, 1000000)
        #
        # self.runId['no_baseline'] = ROOT.TH1D('h_runId_nobaseline', 'no baseline ; run; Number of Events', 1000000, 0, 1000000)
        # self.eventId['no_baseline'] = ROOT.TH1D('h_runId_nobaseline', 'no baseline ;event; Number of Events', 1000000, 0, 1000000)
        # self.lumi['no_baseline'] = ROOT.TH1D('h_runId_nobaseline', 'no baseline ;luminosityBlock; Number of Events', 1000000, 0, 1000000)

        ##################
        # JET HISTOGRAMS #
        ##################
        self.h_jetHt['no_baseline'] = ROOT.TH1D('h_jetHt_nobaseline',
                                                'no baseline ;H_{T} (GeV/c);Number of Events per 10 GeV/c', 300, 1,
                                                3000)
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

        ###################
        # MUON HISTOGRAMS #
        ##################
        self.h_muonPtMap['no_trigger'] = ROOT.TH2F('h_muonPtMap_notrigger', 'no trigger ;Tight muon Pt; Medium muon Pt',
                                                   300, 0, 300, 300, 0, 300)
        self.h_muonPt['no_trigger'] = ROOT.TH1D('h_muonPt_notrigger', 'no trigger ;Muon P_{T} (GeV/c);Number of Events'
                                                                      ' per 1 GeV/c', 300, 0, 300)
        self.h_muonPt['no_baseline'] = ROOT.TH1D('h_muonPt_nobaseline',
                                                 'no baseline ;Muon P_{T} (GeV/c);Number of Events'
                                                 ' per 1 GeV/c', 300, 0, 300)
        self.h_muonPtnomedium['no_trigger'] = ROOT.TH1D('h_muonPtnomedium_notrigger',
                                                        'no trigger ;Muon P_{T} (GeV/c);Number of Events'
                                                        ' per 1 GeV/c', 300, 0, 300)
        self.h_muonPtnomedium['no_baseline'] = ROOT.TH1D('h_muonPtnomedium_nobaseline',
                                                         'no baseline ;Muon P_{T} (GeV/c);Number of Events'
                                                         ' per 1 GeV/c', 300, 0, 300)
        if not self.era.find('mc') == -1:
            self.h_muonPt['prompt0'] = ROOT.TH1D('h_muonPt_prompt0', 'prompt0 muons ;Muon P_{T} (GeV/c);Number of '
                                                                     'Events per 1 GeV/c', 300, 0, 300)
            self.h_muonPt['from_prompt_tau0'] = ROOT.TH1D('h_muonPt_from_prompt_tau0',
                                                          'muons from_prompt_tau0 ;Muon P_{T} (GeV/c);Number of Events '
                                                          'per 1 GeV/c', 300, 0, 300)
            self.h_muonPt['from_b0'] = ROOT.TH1D('h_muonPt_from_b0',
                                                 'muons from_b0;Muon P_{T} (GeV/c);Number of Events '
                                                 'per 1 GeV/c', 300, 0, 300)
            self.h_muonPt['from_c0'] = ROOT.TH1D('h_muonPt_from_c0',
                                                 'muons from_c0 ;Muon P_{T} (GeV/c);Number of Events '
                                                 'per 1 GeV/c', 300, 0, 300)
            self.h_muonPt['from_light_or_unknown0'] = ROOT.TH1D('h_muonPt_from_light_or_unknown0',
                                                                'muons from_light_or_unknown0;Muon P_{T} (GeV/c);Number of Events '
                                                                'per 1 GeV/c', 300, 0, 300)
            self.h_muonPt['unmatched0'] = ROOT.TH1D('h_muonPt_unmatched0',
                                                    'unmatched0 muons ;Muon P_{T} (GeV/c);Number of Events '
                                                    'per 1 GeV/c', 300, 0, 300)
            self.h_muonPt['prompt'] = ROOT.TH1D('h_muonPt_prompt', 'prompt muons ;Muon P_{T} (GeV/c);Number of '
                                                                   'Events per 1 GeV/c', 300, 0, 300)
            self.h_muonPt['from_prompt_tau'] = ROOT.TH1D('h_muonPt_from_prompt_tau',
                                                         'muons from_prompt_tau ;Muon P_{T} (GeV/c);Number of Events '
                                                         'per 1 GeV/c', 300, 0, 300)
            self.h_muonPt['from_b'] = ROOT.TH1D('h_muonPt_from_b',
                                                'muons from_b;Muon P_{T} (GeV/c);Number of Events '
                                                'per 1 GeV/c', 300, 0, 300)
            self.h_muonPt['from_c'] = ROOT.TH1D('h_muonPt_from_c',
                                                'muons from_c ;Muon P_{T} (GeV/c);Number of Events '
                                                'per 1 GeV/c', 300, 0, 300)
            self.h_muonPt['from_light_or_unknown'] = ROOT.TH1D('h_muonPt_from_light_or_unknown',
                                                               'muons from_light_or_unknown;Muon P_{T} (GeV/c);Number of Events '
                                                               'per 1 GeV/c', 300, 0, 300)
            self.h_muonPt['unmatched'] = ROOT.TH1D('h_muonPt_unmatched',
                                                   'unmatched muons ;Muon P_{T} (GeV/c);Number of Events '
                                                   'per 1 GeV/c', 300, 0, 300)

            self.h_muonPtnomedium['prompt0'] = ROOT.TH1D('h_muonPtnomedium_prompt0',
                                                         'prompt0 muons ;Muon P_{T} (GeV/c);Number of '
                                                         'Events per 1 GeV/c', 300, 0, 300)
            self.h_muonPtnomedium['from_prompt_tau0'] = ROOT.TH1D('h_muonPtnomedium_from_prompt_tau0',
                                                                  'muons from_prompt_tau0 ;Muon P_{T} (GeV/c);Number of Events '
                                                                  'per 1 GeV/c', 300, 0, 300)
            self.h_muonPtnomedium['from_b0'] = ROOT.TH1D('h_muonPtnomedium_from_b0',
                                                         'muons from_b0;Muon P_{T} (GeV/c);Number of Events '
                                                         'per 1 GeV/c', 300, 0, 300)
            self.h_muonPtnomedium['from_c0'] = ROOT.TH1D('h_muonPtnomedium_from_c0',
                                                         'muons from_c0 ;Muon P_{T} (GeV/c);Number of Events '
                                                         'per 1 GeV/c', 300, 0, 300)
            self.h_muonPtnomedium['from_light_or_unknown0'] = ROOT.TH1D('h_muonPtnomedium_from_light_or_unknown0',
                                                                        'muons from_light_or_unknown0;Muon P_{T} (GeV/c);Number of Events '
                                                                        'per 1 GeV/c', 300, 0, 300)
            self.h_muonPtnomedium['unmatched0'] = ROOT.TH1D('h_muonPtnomedium_unmatched0',
                                                            'unmatched0 muons ;Muon P_{T} (GeV/c);Number of Events '
                                                            'per 1 GeV/c', 300, 0, 300)
            self.h_muonPtnomedium['prompt'] = ROOT.TH1D('h_muonPtnomedium_prompt',
                                                        'prompt muons ;Muon P_{T} (GeV/c);Number of '
                                                        'Events per 1 GeV/c', 300, 0, 300)
            self.h_muonPtnomedium['from_prompt_tau'] = ROOT.TH1D('h_muonPtnomedium_from_prompt_tau',
                                                                 'muons from_prompt_tau ;Muon P_{T} (GeV/c);Number of Events '
                                                                 'per 1 GeV/c', 300, 0, 300)
            self.h_muonPtnomedium['from_b'] = ROOT.TH1D('h_muonPtnomedium_from_b',
                                                        'muons from_b;Muon P_{T} (GeV/c);Number of Events '
                                                        'per 1 GeV/c', 300, 0, 300)
            self.h_muonPtnomedium['from_c'] = ROOT.TH1D('h_muonPtnomedium_from_c',
                                                        'muons from_c ;Muon P_{T} (GeV/c);Number of Events '
                                                        'per 1 GeV/c', 300, 0, 300)
            self.h_muonPtnomedium['from_light_or_unknown'] = ROOT.TH1D('h_muonPtnomedium_from_light_or_unknown',
                                                                       'muons from_light_or_unknown;Muon P_{T} (GeV/c);Number of Events '
                                                                       'per 1 GeV/c', 300, 0, 300)
            self.h_muonPtnomedium['unmatched'] = ROOT.TH1D('h_muonPtnomedium_unmatched',
                                                           'unmatched muons ;Muon P_{T} (GeV/c);Number of Events '
                                                           'per 1 GeV/c', 300, 0, 300)

            self.h_genMetPt['no_trigger'] = ROOT.TH1D('h_genMetPt_notrigger',
                                                      'no trigger ;GenMET P_{T} (GeV/c);Number of '
                                                      'Events per 1GeV/c', 300, 0, 300)
            self.h_genMetPhi['no_trigger'] = ROOT.TH1D('h_genMetPhi_notrigger',
                                                       'no trigger ;GenMET #phi;Number of Events '
                                                       'per #delta#phi = 0.046', 300, -6, 8)
            self.addObject(self.h_genMetPt['no_trigger'])
            self.addObject(self.h_genMetPhi['no_trigger'])
            self.addObject(self.h_muonPt['prompt0'])
            self.addObject(self.h_muonPt['from_prompt_tau0'])
            self.addObject(self.h_muonPt['from_b0'])
            self.addObject(self.h_muonPt['from_c0'])
            self.addObject(self.h_muonPt['from_light_or_unknown0'])
            self.addObject(self.h_muonPt['unmatched0'])
            self.addObject(self.h_muonPt['prompt'])
            self.addObject(self.h_muonPt['from_prompt_tau'])
            self.addObject(self.h_muonPt['from_b'])
            self.addObject(self.h_muonPt['from_c'])
            self.addObject(self.h_muonPt['from_light_or_unknown'])
            self.addObject(self.h_muonPt['unmatched'])

            self.addObject(self.h_muonPtnomedium['prompt0'])
            self.addObject(self.h_muonPtnomedium['from_prompt_tau0'])
            self.addObject(self.h_muonPtnomedium['from_b0'])
            self.addObject(self.h_muonPtnomedium['from_c0'])
            self.addObject(self.h_muonPtnomedium['from_light_or_unknown0'])
            self.addObject(self.h_muonPtnomedium['unmatched0'])
            self.addObject(self.h_muonPtnomedium['prompt'])
            self.addObject(self.h_muonPtnomedium['from_prompt_tau'])
            self.addObject(self.h_muonPtnomedium['from_b'])
            self.addObject(self.h_muonPtnomedium['from_c'])
            self.addObject(self.h_muonPtnomedium['from_light_or_unknown'])
            self.addObject(self.h_muonPtnomedium['unmatched'])

            self.addObject(self.h_muonGenPartFlav)
            self.addObject(self.h_muonGenPartIdx)

        self.h_muonEtaNomedium['no_trigger'] = ROOT.TH1D('h_muonEtaNomedium_notrigger',
                                                         'no trigger ;Muon #eta;Number of Events per '
                                                         '#delta#eta = 0.046', 300, -6, 8)
        self.h_muonPhiNomedium['no_trigger'] = ROOT.TH1D('h_muonPhiNomedium_notrigger',
                                                         'no trigger ;Muon #phi;Number of Events per '
                                                         '#delta#phi = 0.046', 300, -6, 8)
        self.h_muonIsolationNomedium['no_trigger'] = ROOT.TH1D('h_muonIsolationNomedium_notrigger',
                                                               'no trigger ;Muon miniPFRelIso_all;'
                                                               'Number of Events', 30, 0, 0.17)
        self.h_muonIsoPtNomedium['no_trigger'] = ROOT.TH2F('h_muonIsoPtNomedium_notrigger',
                                                           'no trigger ;Muon P_{T} (GeV/c);'
                                                           'Muon miniPFRelIso_all',
                                                           300, 0, 300, 30, 0, 0.17)
        self.h_muonMapNomedium['no_trigger'] = ROOT.TH2F('h_muonMapNomedium_notrigger',
                                                         'no trigger;Muon #eta;Muon #phi;',
                                                         150, -6, 6, 160, -3.2, 3.2)

        self.h_muonEta['no_trigger'] = ROOT.TH1D('h_muonEta_notrigger', 'no trigger ;Muon #eta;Number of Events per '
                                                                        '#delta#eta = 0.046', 300, -6, 8)
        self.h_muonPhi['no_trigger'] = ROOT.TH1D('h_muonPhi_notrigger', 'no trigger ;Muon #phi;Number of Events per '
                                                                        '#delta#phi = 0.046', 300, -6, 8)
        self.h_muonIsolation['no_trigger'] = ROOT.TH1D('h_muonIsolation_notrigger', 'no trigger ;Muon miniPFRelIso_all;'
                                                                                    'Number of Events', 30, 0, 0.17)
        self.h_muonIsoPt['no_trigger'] = ROOT.TH2F('h_muonIsoPt_notrigger', 'no trigger ;Muon P_{T} (GeV/c);'
                                                                            'Muon miniPFRelIso_all',
                                                   300, 0, 300, 30, 0, 0.17)
        self.h_muonMap['no_trigger'] = ROOT.TH2F('h_muonMap_notrigger', 'no trigger;Muon #eta;Muon #phi;',
                                                 150, -6, 6, 160, -3.2, 3.2)

        ##################
        # SOFT MUONS     #
        ##################
        self.h_mediumMuonMult['no_trigger'] = ROOT.TH1D('h_mediumMuonMult_notrigger',
                                                        'no trigger ;Number of Soft Muons;Number of Events',
                                                        10, 0, 10)
        self.addObject(self.h_mediumMuonMult['no_trigger'])
        self.h_mediumMuonPt['no_trigger'] = ROOT.TH1D('h_mediumMuonPt_notrigger',
                                                      'no trigger ;soft Muon P_{T} (GeV/c);Number of Events'
                                                      ' per 1 GeV/c', 300, 0, 300)
        self.addObject(self.h_mediumMuonPt['no_trigger'])
        self.h_mediumMuonTightPt['no_trigger'] = ROOT.TH1D('h_mediumMuonTightPt_notrigger',
                                                           'no trigger ; tight Muon P_{T} (GeV/c);Number of Events'
                                                           ' per 1 GeV/c', 300, 0, 300)
        self.addObject(self.h_mediumMuonTightPt['no_trigger'])
        if not self.era.find('mc') == -1:
            self.h_mediumMuonPt['prompt'] = ROOT.TH1D('h_mediumMuonPt_prompt',
                                                      'prompt muons ;Muon P_{T} (GeV/c);Number of '
                                                      'Events per 1 GeV/c', 300, 0, 300)
            self.h_mediumMuonPt['from_prompt_tau'] = ROOT.TH1D('h_mediumMuonPt_from_prompt_tau',
                                                               'muons from_prompt_tau ;Muon P_{T} (GeV/c);Number of Events '
                                                               'per 1 GeV/c', 300, 0, 300)
            self.h_mediumMuonPt['from_b'] = ROOT.TH1D('h_mediumMuonPt_from_b',
                                                      'muons from_b;Muon P_{T} (GeV/c);Number of Events '
                                                      'per 1 GeV/c', 300, 0, 300)
            self.h_mediumMuonPt['from_c'] = ROOT.TH1D('h_mediumMuonPt_from_c',
                                                      'muons from_c ;Muon P_{T} (GeV/c);Number of Events '
                                                      'per 1 GeV/c', 300, 0, 300)
            self.h_mediumMuonPt['from_light_or_unknown'] = ROOT.TH1D('h_mediumMuonPt_from_light_or_unknown',
                                                                     'muons from_light_or_unknown;Muon P_{T} (GeV/c);Number of Events '
                                                                     'per 1 GeV/c', 300, 0, 300)
            self.h_mediumMuonPt['unmatched'] = ROOT.TH1D('h_mediumMuonPt_unmatched',
                                                         'unmatched muons ;Muon P_{T} (GeV/c);Number of Events '
                                                         'per 1 GeV/c', 300, 0, 300)
            self.addObject(self.h_mediumMuonPt['prompt'])
            self.addObject(self.h_mediumMuonPt['from_prompt_tau'])
            self.addObject(self.h_mediumMuonPt['from_b'])
            self.addObject(self.h_mediumMuonPt['from_c'])
            self.addObject(self.h_mediumMuonPt['from_light_or_unknown'])
            self.addObject(self.h_mediumMuonPt['unmatched'])

            self.h_mediumMuonTightPt['prompt'] = ROOT.TH1D('h_mediumMuonTightPt_prompt',
                                                           'prompt muons ;Muon P_{T} (GeV/c);Number of '
                                                           'Events per 1 GeV/c', 300, 0, 300)
            self.h_mediumMuonTightPt['from_prompt_tau'] = ROOT.TH1D('h_mediumMuonTightPt_from_prompt_tau',
                                                                    'muons from_prompt_tau ;Muon P_{T} (GeV/c);Number of Events '
                                                                    'per 1 GeV/c', 300, 0, 300)
            self.h_mediumMuonTightPt['from_b'] = ROOT.TH1D('h_mediumMuonTightPt_from_b',
                                                           'muons from_b;Muon P_{T} (GeV/c);Number of Events '
                                                           'per 1 GeV/c', 300, 0, 300)
            self.h_mediumMuonTightPt['from_c'] = ROOT.TH1D('h_mediumMuonTightPt_from_c',
                                                           'muons from_c ;Muon P_{T} (GeV/c);Number of Events '
                                                           'per 1 GeV/c', 300, 0, 300)
            self.h_mediumMuonTightPt['from_light_or_unknown'] = ROOT.TH1D('h_mediumMuonTightPt_from_light_or_unknown',
                                                                          'muons from_light_or_unknown;Muon P_{T} (GeV/c);Number of Events '
                                                                          'per 1 GeV/c', 300, 0, 300)
            self.h_mediumMuonTightPt['unmatched'] = ROOT.TH1D('h_mediumMuonTightPt_unmatched',
                                                              'unmatched muons ;Muon P_{T} (GeV/c);Number of Events '
                                                              'per 1 GeV/c', 300, 0, 300)
            self.addObject(self.h_mediumMuonTightPt['prompt'])
            self.addObject(self.h_mediumMuonTightPt['from_prompt_tau'])
            self.addObject(self.h_mediumMuonTightPt['from_b'])
            self.addObject(self.h_mediumMuonTightPt['from_c'])
            self.addObject(self.h_mediumMuonTightPt['from_light_or_unknown'])
            self.addObject(self.h_mediumMuonTightPt['unmatched'])

            self.h_mediumMuonMult['prompt'] = ROOT.TH1D('h_mediumMuonMult_prompt',
                                                        'prompt muons ;tight Muon P_{T} (GeV/c);Number of '
                                                        'Events per 1 GeV/c', 10, 0, 10)
            self.h_mediumMuonMult['from_prompt_tau'] = ROOT.TH1D('h_mediumMuonMult_from_prompt_tau',
                                                                 'muons from_prompt_tau ;tight Muon P_{T} (GeV/c);Number of Events '
                                                                 'per 1 GeV/c', 10, 0, 10)
            self.h_mediumMuonMult['from_b'] = ROOT.TH1D('h_mediumMuonMult_from_b',
                                                        'muons from_b;tight Muon P_{T} (GeV/c);Number of Events '
                                                        'per 1 GeV/c', 10, 0, 10)
            self.h_mediumMuonMult['from_c'] = ROOT.TH1D('h_mediumMuonMult_from_c',
                                                        'muons from_c ;tight Muon P_{T} (GeV/c);Number of Events '
                                                        'per 1 GeV/c', 10, 0, 10)
            self.h_mediumMuonMult['from_light_or_unknown'] = ROOT.TH1D('h_mediumMuonMult_from_light_or_unknown',
                                                                       'muons from_light_or_unknown;tight Muon P_{T} (GeV/c);Number of Events '
                                                                       'per 1 GeV/c', 10, 0, 10)
            self.h_mediumMuonMult['unmatched'] = ROOT.TH1D('h_mediumMuonMult_unmatched',
                                                           'unmatched muons ;tight Muon P_{T} (GeV/c);Number of Events '
                                                           'per 1 GeV/c', 10, 0, 10)
            self.addObject(self.h_mediumMuonMult['prompt'])
            self.addObject(self.h_mediumMuonMult['from_prompt_tau'])
            self.addObject(self.h_mediumMuonMult['from_b'])
            self.addObject(self.h_mediumMuonMult['from_c'])
            self.addObject(self.h_mediumMuonMult['from_light_or_unknown'])
            self.addObject(self.h_mediumMuonMult['unmatched'])

        ##################
        # MET HISTOGRAMS #
        ##################
        self.h_metPt['no_trigger'] = ROOT.TH1D('h_metPt_notrigger', 'no trigger ;MET P_{T} (GeV/c);Number of Events per'
                                                                    ' 1 GeV/c', 300, 0, 300)
        self.h_metPhi['no_trigger'] = ROOT.TH1D('h_metPhi_notrigger', 'no trigger ;MET #phi;Number of Events per '
                                                                      '#delta#phi = 0.046', 300, -6, 8)
        self.addObject(self.h_jetHt['no_baseline'])
        self.addObject(self.h_jetHt['no_trigger'])
        self.addObject(self.h_jetMult['no_trigger'])
        self.addObject(self.h_jetBMult['no_trigger'])
        self.addObject(self.h_jetEta['no_trigger'])
        self.addObject(self.h_jetPhi['no_trigger'])
        self.addObject(self.h_jetMap['no_trigger'])

        self.addObject(self.h_muonPt['no_baseline'])
        self.addObject(self.h_muonPt['no_trigger'])
        self.addObject(self.h_muonPtMap['no_trigger'])

        self.addObject(self.h_muonPtnomedium['no_baseline'])
        self.addObject(self.h_muonPtnomedium['no_trigger'])

        self.addObject(self.h_muonRelIso04_all)
        self.addObject(self.h_muonEta['no_trigger'])
        self.addObject(self.h_muonPhi['no_trigger'])
        self.addObject(self.h_muonIsolation['no_trigger'])
        self.addObject(self.h_muonIsoPt['no_trigger'])
        self.addObject(self.h_muonMap['no_trigger'])

        self.addObject(self.h_muonEtaNomedium['no_trigger'])
        self.addObject(self.h_muonPhiNomedium['no_trigger'])
        self.addObject(self.h_muonIsolationNomedium['no_trigger'])
        self.addObject(self.h_muonIsoPtNomedium['no_trigger'])
        self.addObject(self.h_muonMapNomedium['no_trigger'])

        self.addObject(self.h_metPt['no_trigger'])
        self.addObject(self.h_metPhi['no_trigger'])

        for key in self.trigLst:
            if not key.find("El") == -1: continue
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
                self.h_jetMap[trgPath] = ROOT.TH2F('h_jetMap_' + trgPath, trgPath + ';Jet #eta;Jet #phi',
                                                   150, -3, 3, 160, -3.2, 3.2)
                self.addObject(self.h_jetMap[trgPath])

                self.h_muonPtMap[trgPath] = ROOT.TH2F('h_muonPtMap_' + trgPath,
                                                      trgPath + ';Tight muon Pt; Medium muon Pt',
                                                      300, 0, 300, 300, 0, 300)
                self.addObject(self.h_muonPtMap[trgPath])
                self.h_muonPt[trgPath] = ROOT.TH1D('h_muonPt_' + trgPath, trgPath + ';Muon P_{T} (GeV/c);Number of '
                                                                                    'Events per 1 GeV/c', 300, 0, 300)
                self.addObject(self.h_muonPt[trgPath])

                self.h_muonPtnomedium[trgPath] = ROOT.TH1D('h_muonPtnomedium_' + trgPath,
                                                           trgPath + ';Muon P_{T} (GeV/c);Number of '
                                                                     'Events per 1 GeV/c', 300, 0, 300)
                self.addObject(self.h_muonPtnomedium[trgPath])

                self.h_mediumMuonTightPt[trgPath] = ROOT.TH1D('h_mediumMuonTightPt_' + trgPath,
                                                              trgPath + ';tight Muon P_{T} (GeV/c);Number of '
                                                                        'Events per 1 GeV/c', 300, 0, 300)
                self.addObject(self.h_mediumMuonTightPt[trgPath])
                self.h_mediumMuonPt[trgPath] = ROOT.TH1D('h_mediumMuonPt_' + trgPath,
                                                         trgPath + ';Muon P_{T} (GeV/c);Number of '
                                                                   'Events per 1 GeV/c', 300, 0, 300)
                self.addObject(self.h_mediumMuonPt[trgPath])
                self.h_mediumMuonMult[trgPath] = ROOT.TH1D('h_mediumMuonMult' + trgPath,
                                                           trgPath + ';Number of Soft Muons;Number of Events',
                                                           10, 0, 10)
                self.addObject(self.h_mediumMuonMult[trgPath])
                if not self.era.find('mc') == -1:
                    self.h_muonPt['prompt' + trgPath] = ROOT.TH1D('h_muonPt_prompt' + trgPath,
                                                                  'prompt muons ;Muon P_{T} (GeV/c);Number of '
                                                                  'Events per 1 GeV/c', 300, 0, 300)
                    self.addObject(self.h_muonPt['prompt' + trgPath])
                    self.h_muonPt['from_prompt_tau' + trgPath] = ROOT.TH1D('h_muonPt_from_prompt_tau' + trgPath,
                                                                           'muons from_prompt_tau ;Muon P_{T} (GeV/c);Number of Events '
                                                                           'per 1 GeV/c', 300, 0, 300)
                    self.addObject(self.h_muonPt['from_prompt_tau' + trgPath])
                    self.h_muonPt['from_b' + trgPath] = ROOT.TH1D('h_muonPt_from_b' + trgPath,
                                                                  'muons from_b;Muon P_{T} (GeV/c);Number of Events '
                                                                  'per 1 GeV/c', 300, 0, 300)
                    self.addObject(self.h_muonPt['from_b' + trgPath])
                    self.h_muonPt['from_c' + trgPath] = ROOT.TH1D('h_muonPt_from_c' + trgPath,
                                                                  'muons from_c ;Muon P_{T} (GeV/c);Number of Events '
                                                                  'per 1 GeV/c', 300, 0, 300)
                    self.addObject(self.h_muonPt['from_c' + trgPath])
                    self.h_muonPt['from_light_or_unknown' + trgPath] = ROOT.TH1D(
                        'h_muonPt_from_light_or_unknown' + trgPath,
                        'muons from_light_or_unknown;Muon P_{T} (GeV/c);Number of Events '
                        'per 1 GeV/c', 300, 0, 300)
                    self.addObject(self.h_muonPt['from_light_or_unknown' + trgPath])
                    self.h_muonPt['unmatched' + trgPath] = ROOT.TH1D('h_muonPt_unmatched' + trgPath,
                                                                     'unmatched muons ;Muon P_{T} (GeV/c);Number of Events '
                                                                     'per 1 GeV/c', 300, 0, 300)
                    self.addObject(self.h_muonPt['unmatched' + trgPath])
                    self.h_genMetPt[trgPath] = ROOT.TH1D('h_genMetPt_' + trgPath,
                                                         trgPath + ';GenMET P_{T} (GeV/c);Number '
                                                                   'of Events per 1 GeV/c', 300, 0, 300)

                    self.h_muonPtnomedium['prompt' + trgPath] = ROOT.TH1D('h_muonPtnomedium_prompt' + trgPath,
                                                                          'prompt muons ;Muon P_{T} (GeV/c);Number of '
                                                                          'Events per 1 GeV/c', 300, 0, 300)
                    self.addObject(self.h_muonPtnomedium['prompt' + trgPath])
                    self.h_muonPtnomedium['from_prompt_tau' + trgPath] = ROOT.TH1D(
                        'h_muonPtnomedium_from_prompt_tau' + trgPath,
                        'muons from_prompt_tau ;Muon P_{T} (GeV/c);Number of Events '
                        'per 1 GeV/c', 300, 0, 300)
                    self.addObject(self.h_muonPtnomedium['from_prompt_tau' + trgPath])
                    self.h_muonPtnomedium['from_b' + trgPath] = ROOT.TH1D('h_muonPtnomedium_from_b' + trgPath,
                                                                          'muons from_b;Muon P_{T} (GeV/c);Number of Events '
                                                                          'per 1 GeV/c', 300, 0, 300)
                    self.addObject(self.h_muonPtnomedium['from_b' + trgPath])
                    self.h_muonPtnomedium['from_c' + trgPath] = ROOT.TH1D('h_muonPtnomedium_from_c' + trgPath,
                                                                          'muons from_c ;Muon P_{T} (GeV/c);Number of Events '
                                                                          'per 1 GeV/c', 300, 0, 300)
                    self.addObject(self.h_muonPtnomedium['from_c' + trgPath])
                    self.h_muonPtnomedium['from_light_or_unknown' + trgPath] = ROOT.TH1D(
                        'h_muonPtnomedium_from_light_or_unknown' + trgPath,
                        'muons from_light_or_unknown;Muon P_{T} (GeV/c);Number of Events '
                        'per 1 GeV/c', 300, 0, 300)
                    self.addObject(self.h_muonPtnomedium['from_light_or_unknown' + trgPath])
                    self.h_muonPtnomedium['unmatched' + trgPath] = ROOT.TH1D('h_muonPtnomedium_unmatched' + trgPath,
                                                                             'unmatched muons ;Muon P_{T} (GeV/c);Number of Events '
                                                                             'per 1 GeV/c', 300, 0, 300)
                    self.addObject(self.h_muonPtnomedium['unmatched' + trgPath])
                    self.h_genMetPt[trgPath] = ROOT.TH1D('h_genMetPt_' + trgPath,
                                                         trgPath + ';GenMET P_{T} (GeV/c);Number '
                                                                   'of Events per 1 GeV/c', 300, 0, 300)

                    self.addObject(self.h_genMetPt[trgPath])
                    self.h_genMetPhi[trgPath] = ROOT.TH1D('h_genMetPhi_' + trgPath, trgPath + ';GenMET #phi;Number of '
                                                                                              'Events per #delta#phi=0.046',
                                                          300, -6, 8)
                    self.addObject(self.h_genMetPhi[trgPath])

                    self.h_mediumMuonPt['prompt' + trgPath] = ROOT.TH1D('h_mediumMuonPt_prompt' + trgPath,
                                                                        'prompt muons ;Muon P_{T} (GeV/c);Number of '
                                                                        'Events per 1 GeV/c', 300, 0, 300)
                    self.addObject(self.h_mediumMuonPt['prompt' + trgPath])
                    self.h_mediumMuonPt['from_prompt_tau' + trgPath] = ROOT.TH1D(
                        'h_mediumMuonPt_from_prompt_tau' + trgPath,
                        'muons from_prompt_tau ;Muon P_{T} (GeV/c);Number of Events '
                        'per 1 GeV/c', 300, 0, 300)
                    self.addObject(self.h_mediumMuonPt['from_prompt_tau' + trgPath])
                    self.h_mediumMuonPt['from_b' + trgPath] = ROOT.TH1D('h_mediumMuonPt_from_b' + trgPath,
                                                                        'muons from_b;Muon P_{T} (GeV/c);Number of Events '
                                                                        'per 1 GeV/c', 300, 0, 300)
                    self.addObject(self.h_mediumMuonPt['from_b' + trgPath])
                    self.h_mediumMuonPt['from_c' + trgPath] = ROOT.TH1D('h_mediumMuonPt_from_c' + trgPath,
                                                                        'muons from_c ;Muon P_{T} (GeV/c);Number of Events '
                                                                        'per 1 GeV/c', 300, 0, 300)
                    self.addObject(self.h_mediumMuonPt['from_c' + trgPath])
                    self.h_mediumMuonPt['from_light_or_unknown' + trgPath] = ROOT.TH1D(
                        'h_mediumMuonPt_from_light_or_unknown' + trgPath,
                        'muons from_light_or_unknown;Muon P_{T} (GeV/c);Number of Events '
                        'per 1 GeV/c', 300, 0, 300)
                    self.addObject(self.h_mediumMuonPt['from_light_or_unknown' + trgPath])
                    self.h_mediumMuonPt['unmatched' + trgPath] = ROOT.TH1D('h_mediumMuonPt_unmatched' + trgPath,
                                                                           'unmatched muons ;Muon P_{T} (GeV/c);Number of Events '
                                                                           'per 1 GeV/c', 300, 0, 300)
                    self.addObject(self.h_mediumMuonPt['unmatched' + trgPath])

                    self.h_mediumMuonTightPt['prompt' + trgPath] = ROOT.TH1D('h_mediumMuonTightPt_prompt' + trgPath,
                                                                             'prompt muons ;tight Muon P_{T} (GeV/c);Number of '
                                                                             'Events per 1 GeV/c', 300, 0, 300)
                    self.addObject(self.h_mediumMuonTightPt['prompt' + trgPath])
                    self.h_mediumMuonTightPt['from_prompt_tau' + trgPath] = ROOT.TH1D(
                        'h_mediumMuonTightPt_from_prompt_tau' + trgPath,
                        'muons from_prompt_tau ;tight Muon P_{T} (GeV/c);Number of Events '
                        'per 1 GeV/c', 300, 0, 300)
                    self.addObject(self.h_mediumMuonTightPt['from_prompt_tau' + trgPath])
                    self.h_mediumMuonTightPt['from_b' + trgPath] = ROOT.TH1D('h_mediumMuonTightPt_from_b' + trgPath,
                                                                             'muons from_b;tight Muon P_{T} (GeV/c);Number of Events '
                                                                             'per 1 GeV/c', 300, 0, 300)
                    self.addObject(self.h_mediumMuonTightPt['from_b' + trgPath])
                    self.h_mediumMuonTightPt['from_c' + trgPath] = ROOT.TH1D('h_mediumMuonTightPt_from_c' + trgPath,
                                                                             'muons from_c ;tight Muon P_{T} (GeV/c);Number of Events '
                                                                             'per 1 GeV/c', 300, 0, 300)
                    self.addObject(self.h_mediumMuonTightPt['from_c' + trgPath])
                    self.h_mediumMuonTightPt['from_light_or_unknown' + trgPath] = ROOT.TH1D(
                        'h_mediumMuonTightPt_from_light_or_unknown' + trgPath,
                        'muons from_light_or_unknown;tight Muon P_{T} (GeV/c);Number of Events '
                        'per 1 GeV/c', 300, 0, 300)
                    self.addObject(self.h_mediumMuonTightPt['from_light_or_unknown' + trgPath])
                    self.h_mediumMuonTightPt['unmatched' + trgPath] = ROOT.TH1D(
                        'h_mediumMuonTightPt_unmatched' + trgPath,
                        'unmatched muons ;tight Muon P_{T} (GeV/c);Number of Events '
                        'per 1 GeV/c', 300, 0, 300)
                    self.addObject(self.h_mediumMuonTightPt['unmatched' + trgPath])

                    self.h_mediumMuonMult['prompt' + trgPath] = ROOT.TH1D('h_mediumMuonMult_prompt' + trgPath,
                                                                          'prompt muons ;Muon P_{T} (GeV/c);Number of '
                                                                          'Events per 1 GeV/c', 10, 0, 10)
                    self.addObject(self.h_mediumMuonMult['prompt' + trgPath])
                    self.h_mediumMuonMult['from_prompt_tau' + trgPath] = ROOT.TH1D(
                        'h_mediumMuonMult_from_prompt_tau' + trgPath,
                        'muons from_prompt_tau ;Muon P_{T} (GeV/c);Number of Events '
                        'per 1 GeV/c', 10, 0, 10)
                    self.addObject(self.h_mediumMuonMult['from_prompt_tau' + trgPath])
                    self.h_mediumMuonMult['from_b' + trgPath] = ROOT.TH1D('h_mediumMuonMult_from_b' + trgPath,
                                                                          'muons from_b;Muon P_{T} (GeV/c);Number of Events '
                                                                          'per 1 GeV/c', 10, 0, 10)
                    self.addObject(self.h_mediumMuonMult['from_b' + trgPath])
                    self.h_mediumMuonMult['from_c' + trgPath] = ROOT.TH1D('h_mediumMuonMult_from_c' + trgPath,
                                                                          'muons from_c ;Muon P_{T} (GeV/c);Number of Events '
                                                                          'per 1 GeV/c', 10, 0, 10)
                    self.addObject(self.h_mediumMuonMult['from_c' + trgPath])
                    self.h_mediumMuonMult['from_light_or_unknown' + trgPath] = ROOT.TH1D(
                        'h_mediumMuonMult_from_light_or_unknown' + trgPath,
                        'muons from_light_or_unknown;Muon P_{T} (GeV/c);Number of Events '
                        'per 1 GeV/c', 10, 0, 10)
                    self.addObject(self.h_mediumMuonMult['from_light_or_unknown' + trgPath])
                    self.h_mediumMuonMult['unmatched' + trgPath] = ROOT.TH1D('h_mediumMuonMult_unmatched' + trgPath,
                                                                             'unmatched muons ;Muon P_{T} (GeV/c);Number of Events '
                                                                             'per 1 GeV/c', 10, 0, 10)
                    self.addObject(self.h_mediumMuonMult['unmatched' + trgPath])

                #                    self.h_genMetPt[trgPath] = ROOT.TH1D('h_genMetPt_' + trgPath, trgPath + ';GenMET P_{T} (GeV/c);Number '
                #                                                        'of Events per 1 GeV/c', 300, 0, 300)
                #                  self.addObject(self.h_genMetPt[trgPath])
                #                 self.h_genMetPhi[trgPath] = ROOT.TH1D('h_genMetPhi_' + trgPath, trgPath + ';GenMET #phi;Number of '
                #                                                                                        'Events per #delta#phi=0.046',
                #                                                     300, -6, 8)
                #              self.addObject(self.h_genMetPhi[trgPath])

                self.h_muonEta[trgPath] = ROOT.TH1D('h_muonEta_' + trgPath, trgPath + ';Muon #eta;Number of Events per'
                                                                                      ' #delta#eta = 0.046', 300, -6, 8)
                self.addObject(self.h_muonEta[trgPath])
                self.h_muonPhi[trgPath] = ROOT.TH1D('h_muonPhi_' + trgPath, trgPath + ';Muon #phi;Number of Events per'
                                                                                      ' #delta#phi = 0.046', 300, -6, 8)
                self.addObject(self.h_muonPhi[trgPath])
                self.h_muonIsolation[trgPath] = ROOT.TH1D('h_muonIsolation_' + trgPath,
                                                          trgPath + ';Muon miniPFRelIso_all;Number of Events', 30, 0,
                                                          0.17)
                self.addObject(self.h_muonIsolation[trgPath])
                self.h_muonIsoPt[trgPath] = ROOT.TH2F('h_muonIsoPt_' + trgPath, trgPath + ';Muon P_{T} (GeV/c);'
                                                                                          'Muon miniPFRelIso_all',
                                                      300, 0, 300, 30, 0, 0.17)
                self.addObject(self.h_muonIsoPt[trgPath])
                self.h_muonMap[trgPath] = ROOT.TH2F('h_muonMap_' + trgPath, trgPath + ';Muon #eta;Muon #phi',
                                                    150, -3, 3, 160, -3.2, 3.2)
                self.addObject(self.h_muonMap[trgPath])  # - Draw ith CONTZ COLZPOL COLZ1 ARR E

                self.h_muonEtaNomedium[trgPath] = ROOT.TH1D('h_muonEtaNomedium_' + trgPath,
                                                            trgPath + ';Muon #eta;Number of Events per'
                                                                      ' #delta#eta = 0.046', 300, -6, 8)
                self.addObject(self.h_muonEtaNomedium[trgPath])
                self.h_muonPhiNomedium[trgPath] = ROOT.TH1D('h_muonPhiNomedium_' + trgPath,
                                                            trgPath + ';Muon #phi;Number of Events per'
                                                                      ' #delta#phi = 0.046', 300, -6, 8)
                self.addObject(self.h_muonPhiNomedium[trgPath])
                self.h_muonIsolationNomedium[trgPath] = ROOT.TH1D('h_muonIsolationNomedium_' + trgPath,
                                                                  trgPath + ';Muon miniPFRelIso_all;Number of Events',
                                                                  30, 0, 0.17)
                self.addObject(self.h_muonIsolationNomedium[trgPath])
                self.h_muonIsoPtNomedium[trgPath] = ROOT.TH2F('h_muonIsoPtNomedium_' + trgPath,
                                                              trgPath + ';Muon P_{T} (GeV/c);'
                                                                        'Muon miniPFRelIso_all',
                                                              300, 0, 300, 30, 0, 0.17)
                self.addObject(self.h_muonIsoPtNomedium[trgPath])
                self.h_muonMapNomedium[trgPath] = ROOT.TH2F('h_muonMapNomedium_' + trgPath,
                                                            trgPath + ';Muon #eta;Muon #phi',
                                                            150, -3, 3, 160, -3.2, 3.2)
                self.addObject(self.h_muonMapNomedium[trgPath])  # - Draw ith CONTZ COLZPOL COLZ1 ARR E

                self.h_metPt[trgPath] = ROOT.TH1D('h_metPt_' + trgPath, trgPath + ';MET P_{T} (GeV/c);Number of Events '
                                                                                  'per 1 GeV/c', 300, 0, 300)
                self.addObject(self.h_metPt[trgPath])
                self.h_metPhi[trgPath] = ROOT.TH1D('h_metPhi_' + trgPath, trgPath + ';MET #phi;Number of Events per '
                                                                                    '#delta#phi = 0.046', 300, -6, 8)
                self.addObject(self.h_metPhi[trgPath])

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
        nTightMuonsPass = 0
        tightMuonsPassIdx = 0
        nSoftMuonsPass = 0
        softMuonsPassIdx = 0
        for nm, muon in enumerate(muons):
            if (getattr(muon, "mediumId") is True) and (getattr(muon, "tightId") is False):
                nSoftMuonsPass += 1
                softMuonsPassIdx = nm
            # - Check muon criteria 2017 https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideMuonIdRun2
            if (getattr(muon, "tightId") is False) or abs(muon.eta) > self.selCriteria["maxObjEta"]: continue
            if muon.pfRelIso04_all > self.selCriteria["maxPfRelIso04"]: continue
            nTightMuonsPass += 1
            tightMuonsPassIdx = nm

        return nTightMuonsPass, tightMuonsPassIdx, nSoftMuonsPass, softMuonsPassIdx

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
        # runObj = Object(event, "run")
        # eventObj = Object(event, "event")
        # lumiObj = Object(event, "luminosityBlock")
        met = Object(event, "MET")
        # genMet = Object(event, "GenMET")

        metPt = getattr(met, "pt")
        metPhi = getattr(met, "phi")
        # genMetPt = getattr(genMet, "pt")
        # genMetPhi = getattr(genMet, "phi")

        trigPath = {}
        for key in self.trigLst:
            if key.find("_OR_") == -1:
                for tg in self.trigLst[key]:
                    trigPath.update({tg: getattr(hltObj, tg)})
            else:
                for tg in self.trigLst[key]:
                    trigPath.update({tg: False})

        if self.era == "17ABdata":
            if trigPath['IsoMu24_eta2p1'] is True or trigPath['PFHT380_SixJet32_DoubleBTagCSV_p075'] is True:
                trigPath['IsoMu24_eta2p1_PFHT380_SixJet32_DoubleBTagCSV_p075'] = True
        elif self.era == "17ABmc":
            if trigPath['IsoMu24_eta2p1'] is True or trigPath['PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2'] is True:
                trigPath['IsoMu24_eta2p1_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2'] = True
        elif not self.era.find("17C") == -1:
            if trigPath['IsoMu27'] is True or trigPath['PFHT380_SixPFJet32_DoublePFBTagCSV_2p2'] is True:
                trigPath['IsoMu27_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2'] = True
        elif not self.era.find("17DEF") == -1:
            if trigPath['IsoMu27'] is True or trigPath['PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2'] is True:
                trigPath['IsoMu27_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2'] = True
        elif self.era == '18data':
            if trigPath['IsoMu24'] is True or trigPath['PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2'] is True:
                trigPath['IsoMu24_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2'] = True
        else:
            print("No era specified. Stopped Analysis.")
            return False

        jetHt = {"notrig": 0}
        for key in self.trigLst:
            if not key.find("El") == -1: continue
            for tg in self.trigLst[key]:
                jetHt.update({tg: 0})

        nJetPass, JetPassIdx, nBtagPass = self.jetCriteria(jets)
        nMuonPass, MuonPassIdx, nSoftMuonPass, softMuonPassIdx = self.muonCriteria(muons)
        nElPass, ElPassIdx = self.electronCriteria(electrons)

        ##############################
        #    Muon Trigger checks     #
        ##############################
        HT = 0
        for jet in jets:
            HT += jet.pt
        self.h_jetHt['no_baseline'].Fill(HT)
        for muon in muons:
            if not self.era.find('mc') == -1:
                self.h_muonPt['no_baseline'].Fill(muon.pt)
                if muon.genPartFlav == 1:
                    self.h_muonPt['prompt0'].Fill(muon.pt)
                elif muon.genPartFlav == 5:
                    self.h_muonPt['from_b0'].Fill(muon.pt)
                elif muon.genPartFlav == 4:
                    self.h_muonPt['from_c0'].Fill(muon.pt)
                elif muon.genPartFlav == 3:
                    self.h_muonPt['from_light_or_unknown0'].Fill(muon.pt)
                elif muon.genPartFlav == 0:
                    self.h_muonPt['unmatched0'].Fill(muon.pt)
                elif muon.genPartFlav == 15:
                    self.h_muonPt['from_prompt_tau0'].Fill(muon.pt)

        if nJetPass > 5 and nMuonPass == 1 and nBtagPass > 1 and nElPass == 0:
            for nj, jet in enumerate(jets):
                if nj not in JetPassIdx: continue
                for key in self.trigLst:
                    if not key.find("El") == -1: continue
                    for tg in self.trigLst[key]:
                        if trigPath[tg]:
                            jetHt[tg] += jet.pt
                jetHt["notrig"] += jet.pt
            if jetHt["notrig"] > 500:
                self.h_eventsPrg.Fill(1)
                for nm, muon in enumerate(muons):
                    if MuonPassIdx == nm: tightMuonPt = muon.pt
                for nm, muon in enumerate(muons):
                    if nSoftMuonPass > 0 and nm != MuonPassIdx:
                        self.h_mediumMuonMult['no_trigger'].Fill(nSoftMuonPass)
                        self.h_mediumMuonPt['no_trigger'].Fill(muon.pt)
                        self.h_muonPtMap['no_trigger'].Fill(tightMuonPt, muon.pt)

                        self.h_muonEtaNomedium['no_trigger'].Fill(muon.eta)
                        self.h_muonPhiNomedium['no_trigger'].Fill(muon.phi)
                        self.h_muonMapNomedium['no_trigger'].Fill(muon.eta, muon.phi)
                        self.h_muonIsolationNomedium['no_trigger'].Fill(muon.miniPFRelIso_all)
                        self.h_muonIsoPtNomedium['no_trigger'].Fill(muon.pt, muon.miniPFRelIso_all)

                        for key in self.trigLst:
                            if not key.find("El") == -1: continue
                            for tg in self.trigLst[key]:
                                if trigPath[tg]:
                                    self.h_muonPtMap[tg].Fill(tightMuonPt, muon.pt)
                                    self.h_mediumMuonPt[tg].Fill(muon.pt)
                                    self.h_muonEtaNomedium[tg].Fill(muon.eta)
                                    self.h_muonPhiNomedium[tg].Fill(muon.phi)
                                    self.h_muonMapNomedium[tg].Fill(muon.eta, muon.phi)
                                    self.h_muonIsolationNomedium[tg].Fill(muon.miniPFRelIso_all)
                                    self.h_muonIsoPtNomedium[tg].Fill(muon.pt, muon.miniPFRelIso_all)
                                    self.h_mediumMuonMult[tg].Fill(nSoftMuonPass)
                                    if not self.era.find('mc') == -1:
                                        if muon.genPartFlav == 1:
                                            self.h_mediumMuonPt['prompt' + tg].Fill(muon.pt)
                                            self.h_mediumMuonMult['prompt' + tg].Fill(nSoftMuonPass)
                                        elif muon.genPartFlav == 5:
                                            self.h_mediumMuonPt['from_b' + tg].Fill(muon.pt)
                                            self.h_mediumMuonMult['from_b' + tg].Fill(nSoftMuonPass)
                                        elif muon.genPartFlav == 4:
                                            self.h_mediumMuonPt['from_c' + tg].Fill(muon.pt)
                                            self.h_mediumMuonMult['from_c' + tg].Fill(nSoftMuonPass)
                                        elif muon.genPartFlav == 3:
                                            self.h_mediumMuonPt['from_light_or_unknown' + tg].Fill(muon.pt)
                                            self.h_mediumMuonMult['from_light_or_unknown' + tg].Fill(nSoftMuonPass)
                                        elif muon.genPartFlav == 0:
                                            self.h_mediumMuonPt['unmatched' + tg].Fill(muon.pt)
                                            self.h_mediumMuonMult['unmatched' + tg].Fill(nSoftMuonPass)
                                        elif muon.genPartFlav == 15:
                                            self.h_mediumMuonPt['from_prompt_tau' + tg].Fill(muon.pt)
                                            self.h_mediumMuonMult['from_prompt_tau' + tg].Fill(nSoftMuonPass)
                        if not self.era.find('mc') == -1:
                            if muon.genPartFlav == 1:
                                self.h_mediumMuonPt['prompt'].Fill(muon.pt)
                                self.h_mediumMuonMult['prompt'].Fill(nSoftMuonPass)
                            elif muon.genPartFlav == 5:
                                self.h_mediumMuonPt['from_b'].Fill(muon.pt)
                                self.h_mediumMuonMult['from_b'].Fill(nSoftMuonPass)
                            elif muon.genPartFlav == 4:
                                self.h_mediumMuonPt['from_c'].Fill(muon.pt)
                                self.h_mediumMuonMult['from_c'].Fill(nSoftMuonPass)
                            elif muon.genPartFlav == 3:
                                self.h_mediumMuonPt['from_light_or_unknown'].Fill(muon.pt)
                                self.h_mediumMuonMult['from_light_or_unknown'].Fill(nSoftMuonPass)
                            elif muon.genPartFlav == 0:
                                self.h_mediumMuonPt['unmatched'].Fill(muon.pt)
                                self.h_mediumMuonMult['unmatched'].Fill(nSoftMuonPass)
                            elif muon.genPartFlav == 15:
                                self.h_mediumMuonPt['from_prompt_tau'].Fill(muon.pt)
                                self.h_mediumMuonMult['from_prompt_tau'].Fill(nSoftMuonPass)
                    if nSoftMuonPass > 0 and nm == MuonPassIdx:
                        self.h_mediumMuonTightPt['no_trigger'].Fill(muon.pt)
                        for key in self.trigLst:
                            if not key.find("El") == -1: continue
                            for tg in self.trigLst[key]:
                                if trigPath[tg]:
                                    self.h_mediumMuonTightPt[tg].Fill(muon.pt)
                                    if not self.era.find('mc') == -1:
                                        if muon.genPartFlav == 1:
                                            self.h_mediumMuonTightPt['prompt' + tg].Fill(muon.pt)
                                        elif muon.genPartFlav == 5:
                                            self.h_mediumMuonTightPt['from_b' + tg].Fill(muon.pt)
                                        elif muon.genPartFlav == 4:
                                            self.h_mediumMuonTightPt['from_c' + tg].Fill(muon.pt)
                                        elif muon.genPartFlav == 3:
                                            self.h_mediumMuonTightPt['from_light_or_unknown' + tg].Fill(muon.pt)
                                        elif muon.genPartFlav == 0:
                                            self.h_mediumMuonTightPt['unmatched' + tg].Fill(muon.pt)
                                        elif muon.genPartFlav == 15:
                                            self.h_mediumMuonTightPt['from_prompt_tau' + tg].Fill(muon.pt)
                        if not self.era.find('mc') == -1:
                            if muon.genPartFlav == 1:
                                self.h_mediumMuonTightPt['prompt'].Fill(muon.pt)
                            elif muon.genPartFlav == 5:
                                self.h_mediumMuonTightPt['from_b'].Fill(muon.pt)
                            elif muon.genPartFlav == 4:
                                self.h_mediumMuonTightPt['from_c'].Fill(muon.pt)
                            elif muon.genPartFlav == 3:
                                self.h_mediumMuonTightPt['from_light_or_unknown'].Fill(muon.pt)
                            elif muon.genPartFlav == 0:
                                self.h_mediumMuonTightPt['unmatched'].Fill(muon.pt)
                            elif muon.genPartFlav == 15:
                                self.h_mediumMuonTightPt['from_prompt_tau'].Fill(muon.pt)
                    if not MuonPassIdx == nm: continue
                    if nSoftMuonPass > 0: continue
                    self.h_muonRelIso04_all.Fill(muon.pfRelIso04_all)
                    if not self.era.find('mc') == -1:
                        self.h_muonGenPartFlav.Fill(muon.genPartFlav)
                        self.h_muonGenPartIdx.Fill(muon.genPartIdx)
                    self.h_muonEta['no_trigger'].Fill(muon.eta)
                    self.h_muonPhi['no_trigger'].Fill(muon.phi)
                    self.h_muonMap['no_trigger'].Fill(muon.eta, muon.phi)
                    self.h_muonIsolation['no_trigger'].Fill(muon.miniPFRelIso_all)
                    self.h_muonIsoPt['no_trigger'].Fill(muon.pt, muon.miniPFRelIso_all)

                    self.h_muonPt['no_trigger'].Fill(muon.pt)
                    # self.h_muonPtnomedium['no_trigger'].Fill(muon.pt)
                    self.h_eventsPrg.Fill(2)
                    for key in self.trigLst:
                        if not key.find("El") == -1: continue
                        for tg in self.trigLst[key]:
                            if trigPath[tg]:
                                self.h_muonPt[tg].Fill(muon.pt)
                                # if nSoftMuonPass == 0: self.h_muonPtnomedium[tg].Fill(muon.pt)
                                if not self.era.find('mc') == -1:
                                    if muon.genPartFlav == 1:
                                        self.h_muonPt['prompt' + tg].Fill(muon.pt)
                                    elif muon.genPartFlav == 5:
                                        self.h_muonPt['from_b' + tg].Fill(muon.pt)
                                    elif muon.genPartFlav == 4:
                                        self.h_muonPt['from_c' + tg].Fill(muon.pt)
                                    elif muon.genPartFlav == 3:
                                        self.h_muonPt['from_light_or_unknown' + tg].Fill(muon.pt)
                                    elif muon.genPartFlav == 0:
                                        self.h_muonPt['unmatched' + tg].Fill(muon.pt)
                                    elif muon.genPartFlav == 15:
                                        self.h_muonPt['from_prompt_tau' + tg].Fill(muon.pt)
                                self.h_muonEta[tg].Fill(muon.eta)
                                self.h_muonPhi[tg].Fill(muon.phi)
                                self.h_muonMap[tg].Fill(muon.eta, muon.phi)
                                self.h_muonIsolation[tg].Fill(muon.miniPFRelIso_all)
                                self.h_muonIsoPt[tg].Fill(muon.pt, muon.miniPFRelIso_all)
                    if not self.era.find('mc') == -1:
                        if muon.genPartFlav == 1:
                            self.h_muonPt['prompt'].Fill(muon.pt)
                        elif muon.genPartFlav == 5:
                            self.h_muonPt['from_b'].Fill(muon.pt)
                        elif muon.genPartFlav == 4:
                            self.h_muonPt['from_c'].Fill(muon.pt)
                        elif muon.genPartFlav == 3:
                            self.h_muonPt['from_light_or_unknown'].Fill(muon.pt)
                        elif muon.genPartFlav == 0:
                            self.h_muonPt['unmatched'].Fill(muon.pt)
                        elif muon.genPartFlav == 15:
                            self.h_muonPt['from_prompt_tau'].Fill(muon.pt)
                for nj, jet in enumerate(jets):
                    if nj not in JetPassIdx: continue
                    for key in self.trigLst:
                        if not key.find("El") == -1: continue
                        for tg in self.trigLst[key]:
                            if trigPath[tg]:
                                # jetHt[tg] += jet.pt
                                self.h_jetEta[tg].Fill(jet.eta)
                                self.h_jetPhi[tg].Fill(jet.phi)
                                self.h_jetMap[tg].Fill(jet.eta, jet.phi)
                    # jetHt["notrig"] += jet.pt
                    self.h_jetEta['no_trigger'].Fill(jet.eta)
                    self.h_jetPhi['no_trigger'].Fill(jet.phi)
                    self.h_jetMap['no_trigger'].Fill(jet.eta, jet.phi)
                self.h_jetHt['no_trigger'].Fill(jetHt["notrig"])
                self.h_jetMult['no_trigger'].Fill(nJetPass)
                self.h_jetBMult['no_trigger'].Fill(nBtagPass)
                self.h_metPt['no_trigger'].Fill(metPt)
                self.h_metPhi['no_trigger'].Fill(metPhi)
                # self.h_genMetPt['no_trigger'].Fill(genMetPt)
                # self.h_genMetPhi['no_trigger'].Fill(genMetPhi)
                # self.h_eventsPrg.Fill(1)
                i = 0
                for key in self.trigLst:
                    if not key.find("El") == -1: continue
                    for tg in self.trigLst[key]:
                        if trigPath[tg]:
                            self.h_jetHt[tg].Fill(jetHt[tg])
                            self.h_metPt[tg].Fill(metPt)
                            self.h_metPhi[tg].Fill(metPhi)
                            # self.h_genMetPt[tg].Fill(genMetPt)
                            # self.h_genMetPhi[tg].Fill(genMetPhi)
                            self.h_jetMult[tg].Fill(nJetPass)
                            self.h_jetBMult[tg].Fill(nBtagPass)
                            if tg.find("_PFHT380") != -1: self.h_eventsPrg.Fill(3)
                            i += 1

        return True


def main(argms):
    """
    This is where the input files are chosen and the PostProcessor runs
    Args:
        argms: command line arguments

    Returns:

    """
    if argms.fileName.find("Run2017B") != -1 or argms.era == "17B":
        if not argms.fileName.find("pythia") == -1:
            trigList = getFileContents(pathToTrigLists + "trigList.txt", True)
            era2017 = "17ABmc"
        else:
            trigList = getFileContents(pathToTrigLists + "2017ABtrigList.txt", True)
            era2017 = "17ABdata"
    elif argms.fileName.find("Run2017C") != -1 or argms.era == "17C":
        trigList = getFileContents(pathToTrigLists + "2017CtrigList.txt", True)
        era2017 = "17C"
        if argms.fileName.find("pythia") != -1 and argms.era == "17C": era2017 = "17Cmc"
    elif argms.fileName.find("Run2017D") != -1 or argms.fileName.find("Run2017E") != -1 or argms.fileName.find(
            "Run2017F") != -1 or argms.era == "17DEF":
        trigList = getFileContents(pathToTrigLists + "2017DEFtrigList.txt", True)
        era2017 = "17DEF"
        if argms.fileName.find("pythia") != -1 and argms.era == "17DEF": era2017 = "17DEFmc"
    elif not argms.fileName.find("Run2018") == -1:
        trigList = getFileContents(pathToTrigLists + "2018trigList.txt", True)
        era2017 = "18data"
        if not argms.fileName.find("pythia") == -1: era2017 = "18mc"
    else:
        trigList = getFileContents(pathToTrigLists + "trigList.txt", True)
        era2017 = "original"

    print(era2017)

    preSelCuts = getFileContents(pathToTrigLists + "preSelectionCuts.txt", False)
    selCriteria = getFileContents("selectionCriteria.txt", False)

    if argms.noWriteFile:
        writeFile = False
    else:
        writeFile = True

    files = findEraRootFiles(argms.fileName)

    p99 = PostProcessor(".",
                        files,
                        # argms.fileName,
                        cut="nJet > 5 && ( nMuon >0 || nElectron >0 )",
                        modules=[TriggerStudy(writeHistFile=writeFile,
                                              eventLimit=argms.eventLimit,
                                              trigLst=trigList,
                                              era=era2017)],
                        # jsonInput=None,
                        noOut=True,
                        histFileName=argms.outputName,
                        histDirName="plots",
                        # branchsel="../myInFiles/kd_branchsel.txt",
                        # outputbranchsel="../myInFiles/kd_branchsel.txt",
                        )
    t0 = time.time()
    p99.run()
    t1 = time.time()
    print("Elapsed time %7.1fs" % (t1 - t0))


if __name__ == '__main__':
    t2 = time.time()
    main(process_arguments())
    t3 = time.time()
    print(">>>>> Total Elapsed time {0:7.1f} s ".format((t3 - t2)))
