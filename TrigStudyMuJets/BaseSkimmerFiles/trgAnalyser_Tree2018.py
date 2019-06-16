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
# pathToSelectionCriteria = "/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/TrigStudyMuJets"
###


def process_arguments():
    """
    Processes command line arguments
    Returns:
        args: list of commandline arguments

    """

    parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-fnp", "--fileName", help="path/to/fileName")
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


def getFileName(pathToFile):
    """
        Find Root files in a given directory/path.
        Args:
        path (string): directory

        Returns: fileName (string): name of file given as input

    """
    foldersList = pathToFile.split("/")
    numberOfSteps = pathToFile.count("/")
    fileDir = "/".join(foldersList[:numberOfSteps]) + "/"
    fileName, fileExt = foldersList[-1].split(".")
    # channelType = foldersList[4]

    return fileDir, fileName


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

    def __init__(self, writeHistFile=True, eventLimit=-1, trigLst=None):
        """
        Initialise global variables

        Args:
            writeHistFile (bool): True to write file, False otherwise
            eventLimit (int): -1 for no event limit, value otherwise for limit
            trigLst (dict): dictionary of trigger names
        """
        self.eventCounter = 0
        self.writeHistFile = writeHistFile
        self.eventLimit = eventLimit
        self.trigLst = trigLst

        pathToSelectionCriteria = "/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/TrigStudyMuJets"

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

    def endJob(self):
        """end Job"""
        Module.endJob(self)

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        """add branches to file"""
        self.out = wrappedOutputTree

        self.out.branch("nVetoMuons", "I")
        self.out.branch("VetoMuons_" + "pt", "F")
        self.out.branch("VetoMuons_" + "phi", "F")
        self.out.branch("VetoMuons_" + "eta", "F")

        self.out.branch("nVetoElectrons", "I")
        self.out.branch("VetoElectrons_" + "pt", "F")
        self.out.branch("VetoElectrons_" + "phi", "F")
        self.out.branch("VetoElectrons_" + "eta", "F")
        self.out.branch("HLT_IsoMu24_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2", "I")
        self.out.branch("HLT_Ele32_WPTight_Gsf_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2", "I")
        self.out.branch("HLT_IsoMu24_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94", "I")
        self.out.branch("HLT_Ele32_WPTight_Gsf_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94", "I")

        self.out.branch("nBtagJets", "I")
        self.out.branch("Jet_HT", "F")

        pass

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        """end file"""
        pass

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
            if jet.btagDeepFlavB > 0.7264:
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
        nMediumMuonsPass = 0
        mediumMuonsPassIdx = 0
        for nm, muon in enumerate(muons):
            if (getattr(muon, "mediumId") is True) and (getattr(muon, "tightId") is False):
                nMediumMuonsPass += 1
                mediumMuonsPassIdx = nm
            # - Check muon criteria 2017 https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideMuonIdRun2
            if (getattr(muon, "tightId") is False) or abs(muon.eta) > self.selCriteria["maxObjEta"]: continue
            if muon.pfRelIso04_all > self.selCriteria["maxPfRelIso04"]: continue
            nTightMuonsPass += 1
            tightMuonsPassIdx = nm

        return nTightMuonsPass, tightMuonsPassIdx, nMediumMuonsPass, mediumMuonsPassIdx

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
        nLooseElectronsPass = 0
        looseElectronsPassIdx = 0
        for ne, el in enumerate(electrons):
            if  el.mvaFall17V2Iso_WPL is True and el.mvaFall17V2Iso_WP90 is False:
                nLooseElectronsPass += 1
                looseElectronsPassIdx = ne

            if abs(el.eta) > self.selCriteria["maxObjEta"]: continue
            if el.miniPFRelIso_all > self.selCriteria["maxMiniPfRelIso"]: continue
            if self.selCriteria["mvaWP"] == 90 and el.mvaFall17V2Iso_WP90 is False: continue
            if 1.4442 < abs(el.eta) < 1.566: continue

            nElsPass += 1
            ElsPassIdx = ne

        return nElsPass, ElsPassIdx, nLooseElectronsPass, looseElectronsPassIdx

    def analyze(self, event):
        """ process event, return True (go to next module) or False (fail, go to next event) """

        self.eventCounter += 1

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

        ########################################
        #  Set Object attributes to variables  #
        ########################################
        trigPath = {}
        for key in self.trigLst:
            if key.find("_OR_") == -1:
                for tg in self.trigLst[key]:
                    if hasattr(hltObj, tg):
                        trigPath.update({tg: getattr(hltObj, tg)})
                    else:
                        trigPath.update({tg: None})
            else:
                for tg in self.trigLst[key]:
                    trigPath.update({tg: False})

        ############################
        #  Fill new HLT_OR Branch  #
        ############################
        if trigPath['PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2'] != None: 
            hadronicHLT = 'PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2'
            if trigPath['IsoMu24'] is True or trigPath[hadronicHLT] is True:
                self.out.fillBranch("HLT_IsoMu24_" + hadronicHLT, 1)
            else:
                self.out.fillBranch("HLT_IsoMu24_" + hadronicHLT, 0)
            if trigPath['Ele32_WPTight_Gsf'] is True or trigPath[hadronicHLT] is True:
                self.out.fillBranch("HLT_Ele32_WPTight_Gsf_" + hadronicHLT, 1)
            else:
                self.out.fillBranch("HLT_Ele32_WPTight_Gsf_" + hadronicHLT, 0)
        elif trigPath['PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94'] != None: 
            hadronicHLT = 'PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94'
            if trigPath['IsoMu24'] is True or trigPath[hadronicHLT] is True:
                self.out.fillBranch("HLT_IsoMu24_" + hadronicHLT, 1)
            else:
                self.out.fillBranch("HLT_IsoMu24_" + hadronicHLT, 0)
            if trigPath['Ele32_WPTight_Gsf'] is True or trigPath[hadronicHLT] is True:
                self.out.fillBranch("HLT_Ele32_WPTight_Gsf_" + hadronicHLT, 1)
            else:
                self.out.fillBranch("HLT_Ele32_WPTight_Gsf_" + hadronicHLT, 0)
        else: return False

        # Object Criteria
        nJetPass, JetPassIdx, nBtagPass = self.jetCriteria(jets)
        nMuonPass, MuonPassIdx, nMediumMuonPass, mediumMuonPassIdx = self.muonCriteria(muons)
        nElPass, ElPassIdx, nLooseElectronPass, looseElectronPassIdx = self.electronCriteria(electrons)

        HT = 0
        for jet in jets:
            HT += jet.pt
        if nJetPass > 5 and nBtagPass > 1 and ( nMuonPass == 1 or nElPass == 1):
            if HT > 500:
                self.out.fillBranch("Jet_HT", HT)
                self.out.fillBranch("nBtagJets", nBtagPass)
                for nm, muon in enumerate(muons):
                    self.out.fillBranch("nVetoMuons", nMediumMuonPass)
                    if nMediumMuonPass > 0 and nm != MuonPassIdx:
                        self.out.fillBranch("VetoMuons_" + "pt", muon.pt)
                        self.out.fillBranch("VetoMuons_" + "phi", muon.phi)
                        self.out.fillBranch("VetoMuons_" + "eta", muon.eta)
                    # if not MuonPassIdx == nm: continue
                for ne, el in enumerate(electrons):
                    self.out.fillBranch("nVetoElectrons", nLooseElectronPass)
                    if nLooseElectronPass > 0 and ne != ElPassIdx:
                        self.out.fillBranch("VetoElectrons_" + "pt", el.pt)
                        self.out.fillBranch("VetoElectrons_" + "phi", el.phi)
                        self.out.fillBranch("VetoElectrons_" + "eta", el.eta)                    
            else:
                return False
        else:
            return False
        return True


def main(argms):
    """
    This is where the input files are chosen and the PostProcessor runs
    Args:
        argms: command line arguments

    Returns:

    """
    if not argms.fileName.find("Run2018") == -1:
        trigList = getFileContents(pathToTrigLists + "2018trigList.txt", True)
        if not argms.fileName.find("Run2018A") == -1: jsonINPUT = pathToTrigLists + "Json_files/Cert_315252-316995_13TeV_PromptReco_Collisions18_JSON_eraA.txt"
        if not argms.fileName.find("Run2018B") == -1: jsonINPUT = pathToTrigLists + "Json_files/Cert_316998-319312_13TeV_PromptReco_Collisions18_JSON_eraB.txt"
        if not argms.fileName.find("Run2018C") == -1: jsonINPUT = pathToTrigLists + "Json_files/Cert_319313-320393_13TeV_PromptReco_Collisions18_JSON_eraC.txt"
        if not argms.fileName.find("Run2018D") == -1: jsonINPUT = pathToTrigLists + "Json_files/Cert_320394-325273_13TeV_PromptReco_Collisions18_JSON_eraD.txt"
        #if not argms.fileName.find("pythia") == -1: 
            #jsonINPUT = None
    else:
        trigList = getFileContents(pathToTrigLists + "2018trigList.txt", True)
        jsonINPUT = None
    print("jsonInput: %s" % jsonINPUT)

    # preSelCuts = getFileContents(pathToTrigLists + "preSelectionCuts.txt", False)
    # selCriteria = getFileContents("selectionCriteria.txt", False)

    if argms.noWriteFile: writeFile = False
    else: writeFile = True

    # files = findEraRootFiles(argms.fileName)
    pathToFile = argms.fileName
    OutDir, inFile = getFileName(argms.fileName)
    thePostFix = "_v"

    p99 = PostProcessor(".",
                        [pathToFile],
                        cut="nJet > 5 && ( nMuon >0 || nElectron >0 )",
                        modules=[TriggerStudy(writeHistFile=writeFile,
                                              eventLimit=argms.eventLimit,
                                              trigLst=trigList)],
                        jsonInput=jsonINPUT,
                        postfix=thePostFix,
                        branchsel="/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/TrigStudyMuJets/kd_branchsel.txt",
                        outputbranchsel="/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/TrigStudyMuJets/kd_branchsel.txt",
                        )

    print(p99.inputFiles)
    t0 = time.time()
    p99.run()
    cmdString = "gfal-copy -r file://$TMPDIR/{0}{1}.root srm://maite.iihe.ac.be:8443{2}BaseSelectionv2_18/{0}.root/".format(inFile, thePostFix, OutDir)
    os.system(cmdString)
    t1 = time.time()
    proc = os.getpid()
    print(">>> Elapsed time {0:7.1f} s by process id: {1}".format((t1 - t0), proc))

if __name__ == '__main__':
    t2 = time.time()
    main(process_arguments())
    t3 = time.time()
    print(">>>>> Total Elapsed time {0:7.1f} s ".format((t3 - t2)))
