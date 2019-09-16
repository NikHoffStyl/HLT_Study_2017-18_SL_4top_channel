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
import numpy
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
    parser.add_argument("-o", "--outputName", default="v8_HistFiles", help="Set name of output file")
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
        self.trigLst['no-HLT2'] = "HLT_none2"
        self.h = {}  # dictionary for histograms

        # self.evelurun = open(pathToTrigLists + csvFile, 'w')
        # self.csv_writer = csv.writer(self.evelurun, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        self.csvFile = csvFile

        self.evelurun = open(pathToTrigLists + csvFile, 'r')
        self.csv_reader = csv.reader(self.evelurun, delimiter=',')
        csvFile2 = csvFile.replace("smu", "sel")
        self.evelurun2 = open(pathToTrigLists + csvFile2, 'r')
        self.csv_reader2 = csv.reader(self.evelurun2, delimiter=',')
        os.system("echo $PWD")
        # self.sffile = open(pathToScriptDir + "SF_17DEF_file.csv", 'r')
        # self.sf_reader = csv.reader(self.sffile, delimiter=',')

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

                muonpT_rebin = numpy.array((0., 20., 40., 50., 300.))
                ht_rebin = numpy.array((0., 100., 500., 750., 2000., 3000.))
                self.h[lep + key + "_HTpt"] =  ROOT.TH2F( "h_" + lep + "_HTpt_" + key, tg + " in " + lepton + "channel; H_{T} / GeV ; Lepton p_{T} / GeV;Number of Events per GeV", 5, ht_rebin, 4, muonpT_rebin)
                self.addObject(self.h[lep + key + "_HTpt"])



    def endJob(self):
        """end Job"""
        self.evelurun.close()
        self.evelurun2.close()
        # self.sffile.close()
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
            # if jet.btagDeepFlavB > 0.7489:
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
            if hasattr(hltObj, tg) and "no-HLT" not in key:
                trigPath.update({tg: getattr(hltObj, tg)})
                if key == "Jet":
                    trig2 = False
                if key == "Jet2":
                    trig2 = True
            else:
                trigPath.update({tg: False})
        if trig2 == False:
            trigPath.update({"HLT_none2": False})
            trigPath.update({"HLT_none": True})
        else:
            trigPath.update({"HLT_none": False})
            trigPath.update({"HLT_none2": True})            

        # Object Criteria
        nJetPass, JetPassIdx, nBtagPass = self.jetCriteria(jets)
        nMuonPass, MuonPassIdx, nMediumMuonPass, mediumMuonPassIdx = self.muonCriteria(muons)
        nElPass, ElPassIdx, nLooseElectronPass, looseElectronPassIdx = self.electronCriteria(electrons)

        HT = 0
        for jet in jets:
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
                        if "Compare" in self.csvFile:
                            self.evelurun.seek(0)
                            keepEvent = True
                            for row in self.csv_reader:
                                if int(row[0]) == event.event and int(row[1]) == event.luminosityBlock and int(row[2]) == event.run:
                                    keepEvent = False
                                    break
                            if keepEvent == False: 
                                print("Deleting Event %d , lumi %d , run %d" %(event.event, event.luminosityBlock, event.run))
                                continue
                        self.h["Mu" + key + "_HTpt"].Fill(HT, muon.pt)

            if nMuonPass == 0 and nElPass == 1:
                for ne, el in enumerate(electrons):
                    # Save Histograms for Electron Properties
                    if not ElPassIdx == ne: continue
                    for key , tg in self.trigLst.iteritems():
                        if "Mu" in key: continue
                        if trigPath[tg] == 0: continue
                        if "ht" in self.csvFile:
                            keepEvent = True
                            self.evelurun2.seek(0)
                            for row in self.csv_reader2:
                                if int(row[0]) == event.event and int(row[1]) == event.luminosityBlock and int(row[2]) == event.run:
                                    keepEvent = False
                                    break
                            if keepEvent == False: 
                                print("Deleting Event %d , lumi %d , run %d" %(event.event, event.luminosityBlock, event.run))
                                continue
                        self.h["El" + key + "_HTpt"].Fill(HT, el.pt)
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
    # "/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/TrigStudyMuJets/E2B1106E-2614-3443-8516-A651A11C0DB2.root",
    # && nVetoMuons == 0 && nVetoElectrons == 0

    p99 = PostProcessor(".",
                        files,
                        cut="nJet > 5 && ( nMuon >0 || nElectron >0 ) && Jet_HT > 500",
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
