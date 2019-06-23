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
import csv
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

##
#  Change global variables as needed
##
pathToTrigLists = "/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/myInFiles/"
pathToScriptDir = "/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/TrigStudyMuJets/"
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
    parser.add_argument("-o", "--outputName", default="v5_HistFiles", help="Set name of output file")
    parser.add_argument("-csv_", "--commaDelFile", default="eventIDs.csv", help="Set csv output file for event, lumi and run numbers")
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
        if f == 'A22A95CF-A110-B145-92FD-C121E5F9F84DdataHTMHT18C.root': continue
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

    def __init__(self, writeHistFile=True, eventLimit=-1, trigLst=None, era=None, csvFile="temp.csv"):
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
        self.era = era
        self.trigLst = trigLst
        self.trigLst['no-HLT'] = "HLT_none"
        
        self.h = {}  # dictionary for histograms

        #self.evelurun = open(pathToTrigLists + csvFile, 'w')
        #self.csv_writer = csv.writer(self.evelurun, delimiter=',')
        #self.evelurun = open(pathToTrigLists + csvFile, 'r')
        #self.csv_writer = csv.writer(self.evelurun, delimiter=',')
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
        for key , tg in self.trigLst.iteritems():
            for lep, lepton  in {"Mu":"Muon", "El":"Electron"}.iteritems():
                if lep == "El" and "Mu" in key : continue
                if lep == "Mu" and "El" in key : continue
                self.h[lep + key + "_HT"] =  ROOT.TH1D( "h_" + lep + "_HT_" + key, tg + " in " + lepton + "channel; H_{T} / GeVc^{-1} ;Number of Events per GeVc^{-1}", 300, 0, 3000)
                self.h[lep + key + "_pt"] = ROOT.TH1D( "h_" + lep + "_pt_" + key, tg + " in " + lepton + "channel; Lepton p_{T} / GeVc^{-1};Number of Events per GeVc^{-1}", 300, 0, 300)
                self.h[lep + key + "_lepEta"] = ROOT.TH1D( "h_" + lep + "_lepEta_" + key, tg + " in " + lepton + "channel; Lepton #eta ;Number of Events", 100, -6, 8)
                self.h[lep + key + "_lepPhi"] = ROOT.TH1D( "h_" + lep + "_lepPhi_" + key, tg + " in " + lepton + "channel; Lepton #phi;Number of Events", 100, -6, 8)
                self.h[lep + key + "_jetEta"] = ROOT.TH1D( "h_" + lep + "_jetEta_" + key, tg + " in " + lepton + "channel; Jet #eta;Number of Events", 100, -6, 8)
                self.h[lep + key + "_jetPhi"] = ROOT.TH1D( "h_" + lep + "_jetPhi_" + key, tg + " in " + lepton + "channel; Jet #phi;Number of Events", 100, -6, 8)
                self.h[lep + key + "_nJet"] = ROOT.TH1D( "h_" + lep + "_nJet_" + key, tg + " in " + lepton + "channel; Number of Jets;Number of Events", 20, 0, 20)
                self.h[lep + key + "_nBJet"] = ROOT.TH1D( "h_" + lep + "_nBJet_" + key, tg + " in " + lepton + "channel; Number of b-tagged Jets;Number of Events", 20, 0, 20)
                self.addObject(self.h[lep + key + "_HT"])
                self.addObject(self.h[lep + key + "_pt"])
                self.addObject(self.h[lep + key + "_lepEta"])
                self.addObject(self.h[lep + key + "_lepPhi"])
                self.addObject(self.h[lep + key + "_jetEta"])
                self.addObject(self.h[lep + key + "_jetPhi"])
                self.addObject(self.h[lep + key + "_nJet"])
                self.addObject(self.h[lep + key + "_nBJet"])




    def endJob(self):
        """end Job"""
        #self.evelurun.close()
        Module.endJob(self)


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
            #if jet.btagDeepFlavB > 0.7489:
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
                if muon.pt < 10: continue
                if muon.pfRelIso04_all > 0.25: continue
                nMediumMuonsPass += 1
                mediumMuonsPassIdx = nm
            # - Check muon criteria 2017 https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideMuonIdRun2
            if (getattr(muon, "tightId") is False) or abs(muon.eta) > self.selCriteria["maxObjEta"]: continue
            if muon.pfRelIso04_all > self.selCriteria["maxPfRelIso04"]: continue
            # if muon.pt < 21: continue
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
                if  el.pt < 10: continue
                nLooseElectronsPass += 1
                looseElectronsPassIdx = ne

            if abs(el.eta) > self.selCriteria["maxObjEta"]: continue
            if el.miniPFRelIso_all > self.selCriteria["maxMiniPfRelIso"]: continue
            if self.selCriteria["mvaWP"] == 90 and el.mvaFall17V2Iso_WP90 is False: continue
            if 1.4442 < abs(el.eta) < 1.566: continue
            # if  el.pt < 5: continue
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
        # met = Object(event, "MET")
        # genMet = Object(event, "GenMET")
        jet2 = Object(event,"Jet2")

        ########################################
        #  Set Object attributes to variables  #
        ########################################
        # metPt = getattr(met, "pt")
        # metPhi = getattr(met, "phi")
        # genMetPt = getattr(genMet, "pt")
        # genMetPhi = getattr(genMet, "phi")
        HT = getattr(jet2, "HT")

        trigPath = {}
        for key , tg in self.trigLst.iteritems():
            if key == "no-HLT": trigPath.update({tg: True})
            else: 
                if hasattr(hltObj, tg):trigPath.update({tg: getattr(hltObj, tg)})
                else: trigPath.update({tg: False})

        #eventLumibRun = [event.event, event.luminosityBlock, event.run]
        #self.csv_writer.writerow(eventLumibRun)

        # Object Criteria
        nJetPass, JetPassIdx, nBtagPass = self.jetCriteria(jets)
        nMuonPass, MuonPassIdx, nMediumMuonPass, mediumMuonPassIdx = self.muonCriteria(muons)
        nElPass, ElPassIdx, nLooseElectronPass, looseElectronPassIdx = self.electronCriteria(electrons)

        HT = 0
        for jet in jets:
            #HT = jet.HT
            HT += jet.pt 
            jetPhi = jet.phi
            jetEta = jet.eta
        if nJetPass > 5 and nBtagPass > 1 and HT > 500 and nMediumMuonPass == 0 and nLooseElectronPass == 0:
            if nMuonPass == 1 and nElPass == 0: 
                for nm, muon in enumerate(muons):
                    # Save Histograms for Muon Properties
                    if not MuonPassIdx == nm: continue
                    for key , tg in self.trigLst.iteritems():
                        if "El" in key: continue
                        if trigPath[tg] == 0: continue
                        self.h["Mu" + key + "_HT"].Fill(HT)
                        self.h["Mu" + key + "_pt"].Fill(muon.pt)
                        self.h["Mu" + key + "_lepEta"].Fill(muon.eta)
                        self.h["Mu" + key + "_lepPhi"].Fill(muon.phi)
                        self.h["Mu" + key + "_nJet"].Fill(nJetPass)
                        self.h["Mu" + key + "_nBJet"].Fill(nBtagPass)
                        for jet in jets:
                            self.h["Mu" + key + "_jetEta"].Fill(jet.eta)
                            self.h["Mu" + key + "_jetPhi"].Fill(jet.phi)

            if nMuonPass == 0 and nElPass == 1:
                for ne, el in enumerate(electrons):
                    # Save Histograms for Electron Properties
                    if not ElPassIdx == ne: continue
                    for key , tg in self.trigLst.iteritems():
                        if "Mu" in key: continue
                        if trigPath[tg] == 0: continue
                        self.h["El" + key + "_HT"].Fill(HT)
                        self.h["El" + key + "_pt"].Fill(el.pt)
                        self.h["El" + key + "_lepEta"].Fill(el.eta)
                        self.h["El" + key + "_lepPhi"].Fill(el.phi)
                        self.h["El" + key + "_nJet"].Fill(nJetPass)
                        self.h["El" + key + "_nBJet"].Fill(nBtagPass)
                        for jet in jets:
                            self.h["El" + key + "_jetEta"].Fill(jetEta)
                            self.h["El" + key + "_jetPhi"].Fill(jetPhi)
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
    if argms.fileName.find("Run2017B") != -1 or argms.era == "17B":
        if not argms.fileName.find("pythia") == -1:
            trigList = getFileContents(pathToTrigLists + "trigList.txt", False)
            era2017 = "17ABmc"
        else:
            trigList = getFileContents(pathToTrigLists + "2017ABtrigList.txt", False)
            era2017 = "17ABdata"
    elif argms.fileName.find("Run2017C") != -1 or argms.era == "17C":
        trigList = getFileContents(pathToTrigLists + "2017CtrigList.txt", False)
        era2017 = "17C"
        if argms.fileName.find("pythia") != -1 and argms.era == "17C":
            era2017 = "17Cmc"
    elif argms.fileName.find("Run2017D") != -1 or argms.fileName.find("Run2017E") != -1 or argms.fileName.find("Run2017F") != -1 or argms.era == "17DEF":
        trigList = getFileContents(pathToTrigLists + "2017DEFtrigList.txt", False)
        era2017 = "17DEF"
        if argms.fileName.find("pythia") != -1 and argms.era == "17DEF": 
            era2017 = "17DEFmc"
    elif not argms.fileName.find("Run2018") == -1 or argms.era == "18":
        trigList = getFileContents(pathToTrigLists + "2018trigList.txt", False)
        era2017 = "18data"
        if not argms.fileName.find("pythia") == -1: 
            era2017 = "18mc"
    else:
        trigList = getFileContents(pathToTrigLists + "trigList.txt", False)
        era2017 = "original"

    print(era2017)

    if argms.noWriteFile: writeFile = False
    else: writeFile = True

    files = findEraRootFiles(argms.fileName)
    # pathToFile = argms.fileName
    # OutDir, inFile = getFileName(argms.fileName)
    # thePostFix = "_v"
    #"/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/TrigStudyMuJets/E2B1106E-2614-3443-8516-A651A11C0DB2.root",

    p99 = PostProcessor(".",
                        files,
                        cut="nJet > 5 && ( nMuon >0 || nElectron >0 ) && nVetoMuons == 0 && nVetoElectrons == 0 && Jet_HT > 500",
                        modules=[TriggerStudy(writeHistFile=writeFile,
                                              eventLimit=argms.eventLimit,
                                              trigLst=trigList,
                                              era=era2017,
                                              csvFile=argms.commaDelFile)],
                        # postfix=thePostFix,
                        noOut=True,
                        histFileName=pathToScriptDir + argms.outputName,
                        histDirName="plots",
                        )

    print(p99.inputFiles)
    t0 = time.time()
    p99.run()
    # cmdString = "gfal-copy -r file://$TMPDIR/{0}{1}.root srm://maite.iihe.ac.be:8443{2}HistFiles{3}/{0}.root/".format(inFile, thePostFix, OutDir, argms.era)
    # os.system(cmdString)
    t1 = time.time()
    proc = os.getpid()
    print(">>> Elapsed time {0:7.1f} s by process id: {1}".format((t1 - t0), proc))

if __name__ == '__main__':
    t2 = time.time()
    main(process_arguments())
    t3 = time.time()
    print(">>>>> Total Elapsed time {0:7.1f} s ".format((t3 - t2)))
