# -*- coding: utf-8 -*-
"""
Created on 1 Jan 2019

@author: NikHoffStyl
"""

from __future__ import (division, print_function)
# from importlib import import_module
import time
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
# from PfJetMultSkimmer import PfJetsSkimmer
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
# from multiprocessing import Process
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


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
                                                     "tt_semilep102_18", "tttt102_18", "ttjets102_18", "ttjetHad"
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


def getFileName(pathToFile):
    """
        Find Root files in a given directory/path.
        Args:
        path (string): directory
        
        Returns: fileName (string): name of file given as input
        
        """
    foldersList = []
    foldersList = pathToFile.split("/")
    numberOfSteps = pathToFile.count("/")
    fileDir = "/".join(foldersList[:numberOfSteps]) + "/"
    fileName, fileExt = foldersList[-1].split(".")
    if foldersList[2] == "mc": channelType = foldersList[4]
    elif foldersList[2] == "data": channelType = foldersList[4] + "_" + foldersList[3] + "_" + foldersList[6]
    
    return channelType, fileName


class PfJetsSkimmer(Module):
    """This class is to be used by the postprocessor to skimm a file down
    using the requirement of number of jets and a single lepton."""

    def __init__(self, writeHistFile=True, eventLimit=-1):
        """ Initialise global variables
        Args:
            writeHistFile (bool): True to write file, False otherwise
        """

        self.eventCounter = 0
        self.writeHistFile = writeHistFile
        self.eventLimit = eventLimit

        self.selCriteria = {}
        with open("/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/myInFiles/selectionCriteria.txt") as f:
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
        """begin job"""
        Module.beginJob(self, histFile, histDirName)

    def endJob(self):
        """end Job"""
        Module.endJob(self)

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        """add branches to file"""
        self.out = wrappedOutputTree

        self.out.branch("Jet2_" + "HT", "F")

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
            #if jet.btagDeepFlavB > 0.7264:
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
        nSoftMuonsPass = 0
        MuonsSoftPassIdx = 0
        for nm, muon in enumerate(muons):
            # - Check muon criteria 2017 https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideMuonIdRun2
            if (getattr(muon, "softId") is True) and muon.pt < 20:
                nSoftMuonsPass += 1
                MuonsSoftPassIdx = nm
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

        nJetPass, JetPassIdx, nBtagPass = self.jetCriteria(jets)
        nMuonPass, MuonPassIdx = self.muonCriteria(muons)
        nElPass, ElPassIdx = self.electronCriteria(electrons)

        if nJetPass > 5 and nBtagPass > 1:
            if nMuonPass == 1 and nElPass == 0:
                jetHt = 0
                for nj, jet in enumerate(jets):
                    jetHt += jet.pt
                self.out.fillBranch("Jet2_HT", jetHt)
                return True
            elif nMuonPass == 0 and nElPass == 1:
                jetHt = 0
                for nj, jet in enumerate(jets):
                    jetHt += jet.pt
                self.out.fillBranch("Jet2_HT", jetHt)
                return True
            else:
                return False
        else:
            return False
        return True


def skimmer(arg):
    """

    Args:
        file: input files of datasets
        arg: the string attached to the end of the file names

    Returns:

    """
    #if "HT" in fileN:
     #   if "Run2017B" in fileN: OutDir="TrimmedSkimmed2017Data/HTMHT_Run2017B-Nano14Dec2018-v1"
      #  elif "Run2017C" in fileN: OutDir="TrimmedSkimmed2017Data/HTMHT_Run2017C-Nano14Dec2018-v1"
       # elif "Run2017D" in fileN: OutDir="TrimmedSkimmed2017Data/HTMHT_Run2017D-Nano14Dec2018-v1"
        #elif "Run2017E" in fileN: OutDir="TrimmedSkimmed2017Data/HTMHT_Run2017E-Nano14Dec2018-v1"
        #elif "Run2017F" in fileN: OutDir="TrimmedSkimmed2017Data/HTMHT_Run2017F-Nano14Dec2018-v1"
     #   elif "Run2018A" in fileN: OutDir="TrimmedSkimmed2018Data/JetHT_Run2018A-Nano14Dec2018-v1"
      #  elif "Run2018B" in fileN: OutDir="TrimmedSkimmed2018Data/JetHT_Run2018B-Nano14Dec2018-v1"
       # elif "Run2018C" in fileN: OutDir="TrimmedSkimmed2018Data/JetHT_Run2018C-Nano14Dec2018-v1"
        #elif "Run2018D" in fileN: OutDir="TrimmedSkimmed2018Data/JetHT_Run2018D-Nano14Dec2018_ver2-v1"
        #else: OutDir="Unknown/HT"
  #  elif "SingleMuon" in fileN:
   #     if "Run2017B" in fileN: OutDir="TrimmedSkimmed2017Data/SingleMuon_Run2017B-Nano14Dec2018-v1"
    #    elif "Run2017C" in fileN: OutDir="TrimmedSkimmed2017Data/SingleMuon_Run2017C-Nano14Dec2018-v1"
     #   elif "Run2017D" in fileN: OutDir="TrimmedSkimmed2017Data/SingleMuon_Run2017D-Nano14Dec2018-v1"
      #  elif "Run2017E" in fileN: OutDir="TrimmedSkimmed2017Data/SingleMuon_Run2017E-Nano14Dec2018-v1"
       # elif "Run2017F" in fileN: OutDir="TrimmedSkimmed2017Data/SingleMuon_Run2017F-Nano14Dec2018-v1"
        #elif "Run2018A" in fileN: OutDir="TrimmedSkimmed2018Data/SingleMuon_Run2018A-Nano14Dec2018-v1"
   #     elif "Run2018B" in fileN: OutDir="TrimmedSkimmed2018Data/SingleMuon_Run2018B-Nano14Dec2018-v1"
    #    elif "Run2018C" in fileN: OutDir="TrimmedSkimmed2018Data/SingleMuon_Run2018C-Nano14Dec2018-v1"
     #   elif "Run2018D" in fileN: OutDir="TrimmedSkimmed2018Data/SingleMuon_Run2018D-Nano14Dec2018_ver2-v1"
      #  else: OutDir="Unknown/SingleMuon"
   # elif "SingleElectron" in fileN:
    #    if "Run2017B" in fileN: OutDir="TrimmedSkimmed2017Data/SingleElectron_Run2017B-Nano14Dec2018-v1"
     #   elif "Run2017C" in fileN: OutDir="TrimmedSkimmed2017Data/SingleElectron_Run2017C-Nano14Dec2018-v1"
      #  elif "Run2017D" in fileN: OutDir="TrimmedSkimmed2017Data/SingleElectron_Run2017D-Nano14Dec2018-v1"
       # elif "Run2017E" in fileN: OutDir="TrimmedSkimmed2017Data/SingleElectron_Run2017E-Nano14Dec2018-v1"
        #elif "Run2017F" in fileN: OutDir="TrimmedSkimmed2017Data/SingleElectron_Run2017F-Nano14Dec2018-v1"
       # else: OutDir="Unknown/SingleElectron"
   # elif "EGamma" in fileN:
    #    if "Run2018A" in fileN: OutDir="TrimmedSkimmed2018Data/EGamma_Run2018A-Nano14Dec2018-v1"
     #   elif "Run2018B" in fileN: OutDir="TrimmedSkimmed2018Data/EGamma_Run2018B-Nano14Dec2018-v1"
      #  elif "Run2018C" in fileN: OutDir="TrimmedSkimmed2018Data/EGamma_Run2018C-Nano14Dec2018-v1"
      #  elif "Run2018D" in fileN: OutDir="TrimmedSkimmed2018Data/EGamma_Run2018D-Nano14Dec2018_ver2-v1"
       # else: OutDir="Unknown/EGamma"
   # elif "TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8" in fileN:
    #    if "_102X_mc2017" in fileN: OutDir="TrimmedSkimmed2017Data/TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_102X"
     #   if "_102_upgrade2018" in fileN: OutDir="TrimmedSkimmed2018Data/TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_102X_18"
   # elif "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8" in fileN:
    #    if "_102X_mc2017" in fileN: OutDir="TrimmedSkimmed2017Data/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_102X"
     #   if "_102_upgrade2018" in fileN:OutDir="TrimmedSkimmed2018Data/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_102X_18"
    #elif "W4JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8" in fileN:
     #   if "_102X_mc2017" in fileN: OutDir="TrimmedSkimmed2017Data/W4JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8_102X"
    #elif "bbbarToMuMu_MuonPt2_TuneCP5_13TeV-pythia8-evtgen" in fileN:
     #   if "_102X_mc2017" in fileN: OutDir="TrimmedSkimmed2017Data/bbbarToMuMu_MuonPt2_TuneCP5_13TeV-pythia8-evtgen"
    #else: OutDir="Unknown" 
    redirector = chooseRedirector(arg)
    pathToFile = redirector + arg.fileName
    print (pathToFile)
    sampleName, inFile = getFileName(arg.fileName)
    if  "_102X_mc2017" in pathToFile: OutDir = "TrimmedSkimmed2017Data/" + sampleName + "_102X"
    else: OutDir = "Trimmed2017Data/" + sampleName
    thePostFix = arg.inputLFN
    p99 = PostProcessor(".",
                        [pathToFile],
                        cut="nJet > 5 && ( nMuon >0 || nElectron >0 ) ",
                        modules=[PfJetsSkimmer(eventLimit=arg.eventLimit)],
                        postfix=thePostFix,
                        branchsel="/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/myInFiles/kd_branchsel.txt",
                        outputbranchsel="/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/myInFiles/kd_branchsel.txt",
                        )
    print(p99.inputFiles)
    t0 = time.time()
    p99.run()
    outFileName = pathToFile[-41:-5]
    cmdString = "gfal-copy -r file://$TMPDIR/{0}{1}.root srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/{2}/{0}.root/".format(inFile, thePostFix, OutDir)
    os.system(cmdString)
    t1 = time.time()
    proc = os.getpid()
    print(">>> Elapsed time {0:7.1f} s by process id: {1}".format((t1 - t0), proc))


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



def main(argms):
    """ This is where the input files are chosen and the PostProcessor runs """
    # allFiles = []
    # for counter, line in enumerate(inputLFNList):
    #     counter += 1
    #     if not argms.fileLimit == -1:
    #         if counter > argms.fileLimit: break
    #     allFiles.append(redirector + str(line).replace('\n', ''))
    #
    # procs = []
    # for index, files in enumerate(allFiles):
    #     proc = Process(target=skimmer, args=(files, argms,))
    #     procs.append(proc)
    #     proc.start()
    #
    # for proc in procs:
    #     proc.join()

    # print("End of job!")
    #skimmer(pathToFile, argms)
    skimmer(argms)


if __name__ == '__main__':
    t2 = time.time()
    main(process_arguments())
    t3 = time.time()
    print(">>>>> Total Elapsed time {0:7.1f} s ".format((t3 - t2)))
