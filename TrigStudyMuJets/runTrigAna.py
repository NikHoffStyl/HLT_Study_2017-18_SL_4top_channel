# -*- coding: utf-8 -*-
"""
Created on Jan 2019

@author: NikHoffStyl
"""
from __future__ import (division, print_function)
import time
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
# from anaTrigsMuJets import *


def process_arguments():
    """ Process command-line arguments """

    parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--inputLFN", choices=["tt_semilep94", "ttjets94", "tttt94", "tttt_weights", "wjets",
                                                     "tt_semilep102_17B", "tttt102_17B",
                                                     "tt_semilep102_17C", "tttt102_17C",
                                                     "tt_semilep102_17DEF", "tttt102_17DEF",
                                                     "dataHTMHT17B", "dataSMu17B", "dataSEl17B",
                                                     "dataHTMHT17C", "dataSMu17C", "dataSEl17C",
                                                     "dataHTMHT17D", "dataSMu17D", "dataSEl17D",
                                                     "dataHTMHT17E", "dataSMu17E", "dataSEl17E",
                                                     "dataHTMHT17F", "dataSMu17F", "dataSEl17F",
                                                     "tt_semilep102_18", "tttt102_18",
                                                     "dataHTMHT18A", "dataSMu18A", "dataSEl18A",
                                                     "dataHTMHT18B", "dataSMu18B", "dataSEl18B",
                                                     "dataHTMHT18C", "dataSMu18C", "dataSEl18C",
                                                     "dataHTMHT18D", "dataSMu18D", "dataSEl18D",
                                                     "oneFile"
                                                     ],
                        default="_v", help="Set list of input files")
    parser.add_argument("-fnp", "--fileName", help="path/to/fileName")
    parser.add_argument("-r", "--redirector", choices=["xrd-global", "xrdUS", "xrdEU_Asia", "eos", "iihe", "local"],
                        default="xrd-global", help="Sets redirector to query locations for LFN")
    parser.add_argument("-nw", "--noWriteFile", action="store_true",
                        help="Does not output a ROOT file, which contains the histograms.")
    parser.add_argument("-e", "--eventLimit", type=int, default=-1,
                        help="Set a limit to the number of events.")
    parser.add_argument("-lf", "--fileLimit", type=int, default=-1,
                        help="Set a limit to the number of files to run through.")
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


class TriggerStudy(Module):
    """This class is to be used by the postprocessor to skimm a file down
    using the requirement of number of jets and a single lepton."""

    def __init__(self, writeHistFile=True, eventLimit=-1, trigLst=None, era=None):
        """ Initialise global variables
        Args:
            writeHistFile (bool): True to write file, False otherwise
        """

        self.era = era
        self.eventCounter = 0
        self.writeHistFile = writeHistFile
        self.eventLimit = eventLimit
        self.trigLst = trigLst

    def beginJob(self, histFile=None, histDirName=None):
        """begin job"""
        Module.beginJob(self, histFile, histDirName)

    def endJob(self):
        """end Job"""
        Module.endJob(self)

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        """add branches to file"""
        self.out = wrappedOutputTree

        self.out.branch("Jet2_HT", "F")
        self.out.branch("Jet2_n", "I")
        self.out.branch("Jet2_nbtag", "I")
        self.out.branch("Jet2_jetId", "I")
        self.out.branch("Jet2_btagDeepFlavB", "F")
        self.out.branch("Jet2_eta", "F")
        self.out.branch("Jet2_phi", "F")

        self.out.branch("Muon2_pt", "F")
        self.out.branch("Muon2_phi", "F")
        self.out.branch("Muon2_eta", "F")
        self.out.branch("Muon2_pfRelIso04_all", "F")

        self.out.branch("Electron2_pt", "F")
        self.out.branch("Electron2_phi", "F")
        self.out.branch("Electron2_eta", "F")
        self.out.branch("Electron2_mvaFall17V2Iso_WP90", "F")
        self.out.branch("Electron2_miniPFRelIso_all", "F")

        self.out.branch("Met2_pt", "F")
        self.out.branch("Met2_phi", "F")
        self.out.branch("Met2_eta", "F")

        self.out.branch("HLT_SingleLep", "I")
        self.out.branch("HLT_FullyHadronic", "I")
        self.out.branch("HLT_OfflineOR", "I")
        self.out.branch("HLT_OnlineAND", "I")  # 0= Fail, 1= Pass , -1=Non Existent

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
        """process event, return True (go to next module) or False (fail, go to next event)"""
        self.eventCounter += 1

        if self.eventCounter > self.eventLimit > -1:
            return False

        jets = Collection(event, "Jet")
        jetHt = 0
        for nj, jet in enumerate(jets):
            jetHt += jet.pt
        self.out.fillBranch("Jet2_HT", jetHt)

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
                self.out.fillBranch("HLT_OfflineOR", 1)
        elif self.era == "17ABmc":
            if trigPath['IsoMu24_eta2p1'] is True or trigPath['PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2'] is True:
                trigPath['IsoMu24_eta2p1_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2'] = True
                self.out.fillBranch("HLT_OfflineOR", 1)
        elif self.era == "17C":
            if trigPath['IsoMu27'] is True or trigPath['PFHT380_SixPFJet32_DoublePFBTagCSV_2p2'] is True:
                trigPath['IsoMu27_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2'] = True
                self.out.fillBranch("HLT_OfflineOR", 1)
        elif self.era == "17DEF":
            if trigPath['IsoMu27'] is True or trigPath['PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2'] is True:
                trigPath['IsoMu27_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2'] = True
                self.out.fillBranch("HLT_OfflineOR", 1)
        else:
            print("No era specified. Stopped Analysis.")
            return False

        jetHt = {"notrig": 0}
        for key in self.trigLst:
            if not key.find("El") == -1: continue
            for tg in self.trigLst[key]:
                jetHt.update({tg: 0})

        nJetPass, JetPassIdx, nBtagPass = self.jetCriteria(jets)
        nMuonPass, MuonPassIdx = self.muonCriteria(muons)
        nElPass, ElPassIdx = self.electronCriteria(electrons)

        ##############################
        #    Muon Trigger checks     #
        ##############################
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
                for nm, muon in enumerate(muons):
                    if not MuonPassIdx == nm: continue
                    self.h_muonRelIso04_all.Fill(muon.pfRelIso04_all)
                    # self.h_muonGenPartFlav.Fill(muon.genPartFlav)
                    # self.h_muonGenPartIdx.Fill(muon.genPartIdx)
                    self.h_muonEta['no_trigger'].Fill(muon.eta)
                    self.h_muonPhi['no_trigger'].Fill(muon.phi)
                    self.h_muonMap['no_trigger'].Fill(muon.eta, muon.phi)
                    self.h_muonIsolation['no_trigger'].Fill(muon.miniPFRelIso_all)
                    self.h_muonIsoPt['no_trigger'].Fill(muon.pt, muon.miniPFRelIso_all)
                    self.h_muonPt['no_trigger'].Fill(muon.pt)
                    for key in self.trigLst:
                        if not key.find("El") == -1: continue
                        for tg in self.trigLst[key]:
                            if trigPath[tg]:
                                self.h_muonPt[tg].Fill(muon.pt)
                                self.h_muonEta[tg].Fill(muon.eta)
                                self.h_muonPhi[tg].Fill(muon.phi)
                                self.h_muonMap[tg].Fill(muon.eta, muon.phi)
                                self.h_muonIsolation[tg].Fill(muon.miniPFRelIso_all)
                                self.h_muonIsoPt[tg].Fill(muon.pt, muon.miniPFRelIso_all)
                    # if muon.genPartFlav == 1:
                    #    self.h_muonPt['prompt'].Fill(muon.pt)
                    # if muon.genPartFlav == 5:
                    #    self.h_muonPt['non-prompt'].Fill(muon.pt)
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
                self.h_eventsPrg.Fill(1)
                # self.out.fillBranch("aTestBranch", self.eventCounter)
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
                            self.h_eventsPrg.Fill(2 + i)
                            i += 1

        return True


def skimmer(fileN, arg):
    """

    Args:
        file: input files of datasets
        arg: the string attached to the end of the file names

    Returns:

    """
    if "HT" in fileN:
        if "Run2017B" in fileN: OutDir="Trimmed2017Data/HTMHT_Run2017B-Nano14Dec2018-v1"
        elif "Run2017C" in fileN: OutDir="Trimmed2017Data/HTMHT_Run2017C-Nano14Dec2018-v1"
        elif "Run2017D" in fileN: OutDir="Trimmed2017Data/HTMHT_Run2017D-Nano14Dec2018-v1"
        elif "Run2017E" in fileN: OutDir="Trimmed2017Data/HTMHT_Run2017E-Nano14Dec2018-v1"
        elif "Run2017F" in fileN: OutDir="Trimmed2017Data/HTMHT_Run2017F-Nano14Dec2018-v1"
        elif "Run2018A" in fileN: OutDir="Trimmed2018Data/JetHT_Run2018A-Nano14Dec2018-v1"
        elif "Run2018B" in fileN: OutDir="Trimmed2018Data/JetHT_Run2018B-Nano14Dec2018-v1"
        elif "Run2018C" in fileN: OutDir="Trimmed2018Data/JetHT_Run2018C-Nano14Dec2018-v1"
        elif "Run2018D" in fileN: OutDir="Trimmed2018Data/JetHT_Run2018D-Nano14Dec2018_ver2-v1"
        else: OutDir="Unknown/HT"
    elif "SingleMuon" in fileN:
        if "Run2017B" in fileN: OutDir="Trimmed2017Data/SingleMuon_Run2017B-Nano14Dec2018-v1"
        elif "Run2017C" in fileN: OutDir="Trimmed2017Data/SingleMuon_Run2017C-Nano14Dec2018-v1"
        elif "Run2017D" in fileN: OutDir="Trimmed2017Data/SingleMuon_Run2017D-Nano14Dec2018-v1"
        elif "Run2017E" in fileN: OutDir="Trimmed2017Data/SingleMuon_Run2017E-Nano14Dec2018-v1"
        elif "Run2017F" in fileN: OutDir="Trimmed2017Data/SingleMuon_Run2017F-Nano14Dec2018-v1"
        elif "Run2018A" in fileN: OutDir="Trimmed2018Data/SingleMuon_Run2018A-Nano14Dec2018-v1"
        elif "Run2018B" in fileN: OutDir="Trimmed2018Data/SingleMuon_Run2018B-Nano14Dec2018-v1"
        elif "Run2018C" in fileN: OutDir="Trimmed2018Data/SingleMuon_Run2018C-Nano14Dec2018-v1"
        elif "Run2018D" in fileN: OutDir="Trimmed2018Data/SingleMuon_Run2018D-Nano14Dec2018_ver2-v1"
        else: OutDir="Unknown/SingleMuon"
    elif "SingleElectron" in fileN:
        if "Run2017B" in fileN: OutDir="Trimmed2017Data/SingleElectron_Run2017B-Nano14Dec2018-v1"
        elif "Run2017C" in fileN: OutDir="Trimmed2017Data/SingleElectron_Run2017C-Nano14Dec2018-v1"
        elif "Run2017D" in fileN: OutDir="Trimmed2017Data/SingleElectron_Run2017D-Nano14Dec2018-v1"
        elif "Run2017E" in fileN: OutDir="Trimmed2017Data/SingleElectron_Run2017E-Nano14Dec2018-v1"
        elif "Run2017F" in fileN: OutDir="Trimmed2017Data/SingleElectron_Run2017F-Nano14Dec2018-v1"
        else: OutDir="Unknown/SingleElectron"
    elif "EGamma" in fileN:
        if "Run2018A" in fileN: OutDir="Trimmed2018Data/EGamma_Run2018A-Nano14Dec2018-v1"
        elif "Run2018B" in fileN: OutDir="Trimmed2018Data/EGamma_Run2018B-Nano14Dec2018-v1"
        elif "Run2018C" in fileN: OutDir="Trimmed2018Data/EGamma_Run2018C-Nano14Dec2018-v1"
        elif "Run2018D" in fileN: OutDir="Trimmed2018Data/EGamma_Run2018D-Nano14Dec2018_ver2-v1"
        else: OutDir="Unknown/EGamma"
    elif "TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8" in fileN:
        if "_102X_mc2017" in fileN: OutDir="Trimmed2017Data/TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_102X"
        if "_102_upgrade2018" in fileN: OutDir="Trimmed2018Data/TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_102X_18"
    elif "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8" in fileN:
        if "_102X_mc2017" in fileN: OutDir="Trimmed2017Data/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_102X"
        if "_102_upgrade2018" in fileN:OutDir="Trimmed2018Data/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_102X_18"
    else: OutDir="Unknown"
    thePostFix = arg.inputLFN

    p99 = PostProcessor(".",
                        [fileN],
                        modules=[TriggerStudy(writeHistFile=writeFile,
                                              eventLimit=argms.eventLimit,
                                              trigLst=trigList,
                                              era=era2017)],
                        postfix=thePostFix,
                        branchsel="/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/TrigStudyMuJets/kd_branchsel.txt",
                        outputbranchsel="/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/TrigStudyMuJets/kd_branchsel.txt",
                        )

    print(p99.inputFiles)
    t0 = time.time()
    p99.run()
    outFileName = fileN[-41:-5]
    cmdString = "gfal-copy -r file://$TMPDIR/{0}{1}.root srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/{2}/{0}.root/".format(outFileName, thePostFix, OutDir)
    os.system(cmdString)
    t1 = time.time()
    proc = os.getpid()
    print(">>> Elapsed time {0:7.1f} s by process id: {1}".format((t1 - t0), proc))


def main(argms):
    """
    This is where the input files are chosen and the PostProcessor runs
    Args:
        argms: command line arguments

    Returns:

    """
    redirector = chooseRedirector(argms)
    if not argms.inputLFN.find("17B") == -1:
        if argms.inputLFN == "tt_semilep102_17B" or argms.inputLFN == "tttt102_17B":
            trigList = getFileContents("/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/myInFiles/trigList.txt", True)
            era2017 = "17ABmc"
        else:
            trigList = getFileContents("/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/myInFiles/2017ABtrigList.txt", True)
            era2017 = "17ABdata"
    elif not argms.inputLFN.find("17C") == -1:
        trigList = getFileContents("./user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/myInFiles/2017CtrigList.txt", True)
        era2017 = "17C"
    elif not argms.inputLFN.find("17D") or argms.inputLFN.find("17E") or argms.inputLFN.find("17F") == -1:
        trigList = getFileContents("/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/myInFiles/2017DEFtrigList.txt", True)
        era2017 = "17DEF"
    else:
        trigList = getFileContents("/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/myInFiles/trigList.txt", True)
        era2017 = "original"

    preSelCuts = getFileContents("/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/myInFiles/preSelectionCuts.txt", False)
    selCriteria = getFileContents("/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/TrigStudyMuJets/selectionCriteria.txt", False)
    inputLFNList, thePostFix, outputFile = ioFiles(argms, selCriteria)

    if argms.noWriteFile: writeFile = False
    else: writeFile = True

    # files = []
    # for counter, line in enumerate(inputLFNList):
    #     counter += 1
    #     if not argms.fileLimit == -1:
    #         if counter > argms.fileLimit: break
    #     files.append(redirector + str(line).replace('\n', ''))

    keyWord = argms.inputLFN
    runPeriod = keyWord[-3:]
    if not keyWord.find("HTMHT") == -1: dirPath = "../HTMHT/" + runPeriod
    elif not keyWord.find("SMu") == -1: dirPath = "../SingleMuon/" + runPeriod
    elif not keyWord.find("SEl") == -1: dirPath = "../SingleElectron/" + runPeriod
    elif not keyWord.find("tt_semilep102") == -1: dirPath = "../TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_102X/"
    elif not keyWord.find("tttt102") == -1: dirPath = "../TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_102X/"
    else: return 0
    files = findEraRootFiles(dirPath)

    p99 = PostProcessor(".",
                        files,
                        modules=[TriggerStudy(writeHistFile=writeFile,
                                              eventLimit=argms.eventLimit,
                                              trigLst=trigList,
                                              era=era2017)],
                        # jsonInput=None,
                        noOut=True,
                        # haddFileName="TestBranch.root",
                        # justcount=False,
                        # postfix=thePostFix,
                        histFileName=outputFile,
                        histDirName="plots",
                        )
    t0 = time.time()
    p99.run()
    t1 = time.time()
    print("Elapsed time %7.1fs" % (t1-t0))


if __name__ == '__main__':
    t2 = time.time()
    main(process_arguments())
    t3 = time.time()
    print(">>>>> Total Elapsed time {0:7.1f} s ".format((t3 - t2)))
