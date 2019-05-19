# -*- coding: utf-8 -*-
"""
Created on Jan 2019

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
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection  # , Object
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

        return True


def skimmer(file, arg):
    """

    Args:
        file: input files of datasets
        arg: the string attached to the end of the file names

    Returns:

    """
    thePostFix = arg.inputLFN
    p99 = PostProcessor("OutDirectory",
                        [file],
                        cut="nJet > 5 && ( nMuon >0 || nElectron >0 ) ",
                        modules=[PfJetsSkimmer(eventLimit=arg.eventLimit)],
                        postfix=thePostFix,
                        branchsel="/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/myInFiles/kd_branchsel.txt",
                        outputbranchsel="/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/myInFiles/kd_branchsel.txt",
                        )
    # p99.inputFiles
    print(p99.inputFiles)
    t0 = time.time()
    p99.run()
    outFileName = file[-41:-5]
    cmdString = "gfal-copy -r file://$TMPDIR/OutDirectory/{0}{1}.root srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Trimmed2018Data/{0}/".format(outFileName, thePostFix)
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


def ioFiles(arg):
    """
        Input and Output file

        Args:
            arg : command line arguments

        Returns:
            inLFNList (string): list of file datasets

        Open the text list of files as read-only ("r" option), use as pairs to add proper postfix to output file
        you may want to change path to suit your file ordering

        """
    # Open the text list of files as read-only ("r" option), use as pairs to add proper postfix to output file
    # you may want to change path to suit your file ordering
    if arg.inputLFN == "dataHTMHT17B":
        inLFNList = open("myInFiles/data/HTMHT_Run2017B-Nano14Dec2018-v1.txt", "r")
    elif arg.inputLFN == "dataSMu17B":
        inLFNList = open("myInFiles/data/SingleMuon_Run2017B-Nano14Dec2018-v1.txt", "r")
    elif arg.inputLFN == "dataSEl17B":
        inLFNList = open("myInFiles/data/SingleElectron_Run2017B-Nano14Dec2018-v1.txt", "r")
    elif arg.inputLFN == "dataHTMHT17C":
        inLFNList = open("myInFiles/data/HTMHT_Run2017C-Nano14Dec2018-v1.txt", "r")
    elif arg.inputLFN == "dataSMu17C":
        inLFNList = open("myInFiles/data/SingleMuon_Run2017C-Nano14Dec2018-v1.txt", "r")
    elif arg.inputLFN == "dataSEl17C":
        inLFNList = open("myInFiles/data/SingleElectron_Run2017C-Nano14Dec2018-v1.txt", "r")
    elif arg.inputLFN == "dataHTMHT17D":
        inLFNList = open("myInFiles/data/HTMHT_Run2017D-Nano14Dec2018-v1.txt", "r")
    elif arg.inputLFN == "dataSMu17D":
        inLFNList = open("myInFiles/data/SingleMuon_Run2017D-Nano14Dec2018-v1.txt", "r")
    elif arg.inputLFN == "dataSEl17D":
        inLFNList = open("myInFiles/data/SingleElectron_Run2017D-Nano14Dec2018-v1.txt", "r")
    elif arg.inputLFN == "dataHTMHT17E":
        inLFNList = open("myInFiles/data/HTMHT_Run2017E-Nano14Dec2018-v1.txt", "r")
    elif arg.inputLFN == "dataSMu17E":
        inLFNList = open("myInFiles/data/SingleMuon_Run2017E-Nano14Dec2018-v1.txt", "r")
    elif arg.inputLFN == "dataSEl17E":
        inLFNList = open("myInFiles/data/SingleElectron_Run2017E-Nano14Dec2018-v1.txt", "r")
    elif arg.inputLFN == "dataHTMHT17F":
        inLFNList = open("myInFiles/data/HTMHT_Run2017F-Nano14Dec2018-v1.txt", "r")
    elif arg.inputLFN == "dataSMu17F":
        inLFNList = open("myInFiles/data/SingleMuon_Run2017F-Nano14Dec2018-v1.txt", "r")
    elif arg.inputLFN == "dataSEl17F":
        inLFNList = open("myInFiles/data/SingleElectron_Run2017F-Nano14Dec2018-v1.txt", "r")
    elif not arg.inputLFN.find("tt_semilep102_17") == -1:
        inLFNList = open("myInFiles/mc/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_102X.txt", "r")
    elif arg.inputLFN == "tt_semilep94":  # tt + jets MC
        inLFNList = open("myInFiles/mc/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_94X.txt", "r")
    elif arg.inputLFN == "ttjets94":
        if arg.redirector == "local":
            inLFNList = open(
                "../myInFiles/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8/fileNames.txt", "r")
        else:
            inLFNList = open("myInFiles/mc/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8_94X.txt", "r")
    elif arg.inputLFN == "tttt_weights":
        if arg.redirector == "local":
            inLFNList = open("../myInFiles/TTTTweights/TTTTweights_files.txt", "r")
        else:
            inLFNList = open("myInFiles/mc/TTTTweights_files.txt", "r")
    elif arg.inputLFN == "wjets":  # W (to Lep + Nu) + jets
        if arg.redirector == "local":
            inLFNList = open("../myInFiles/Wjets/Wjets_files.txt", "r")
        else:
            inLFNList = open("myInFiles/mc/Wjets_files.txt", "r")
    elif arg.inputLFN == "tttt94":  # tttt MC
        if arg.redirector == "local":
            inLFNList = open("../myInFiles/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/fileNames.txt", "r")
        else:
            inLFNList = open("myInFiles/mc/TTTT_TuneCP5_13TeV-amcatnlo-pythia8_94X.txt", "r")
    elif not arg.inputLFN.find("tttt102_17") == -1:  # tttt MC
        inLFNList = open("myInFiles/mc/TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_102X.txt", "r")

    elif arg.inputLFN == "dataHTMHT18A":
        inLFNList = open("/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/myInFiles/data2018/JetHT_Run2018A-Nano14Dec2018-v1.txt", "r")
    elif arg.inputLFN == "dataSMu18A":
        inLFNList = open("/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/myInFiles/data2018/SingleMuon_Run2018A-Nano14Dec2018-v1.txt", "r")
    elif arg.inputLFN == "dataSEl18A":
        inLFNList = open("/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/myInFiles/data2018/EGamma_Run2018A-Nano14Dec2018-v1.txt", "r")
    elif arg.inputLFN == "dataHTMHT18B":
        inLFNList = open("/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/myInFiles/data2018/JetHT_Run2018B-Nano14Dec2018-v1.txt", "r")
    elif arg.inputLFN == "dataSMu18B":
        inLFNList = open("/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/myInFiles/data2018/SingleMuon_Run2018B-Nano14Dec2018-v1.txt", "r")
    elif arg.inputLFN == "dataSEl18B":
        inLFNList = open("/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/myInFiles/data2018/EGamma_Run2018B-Nano14Dec2018-v1.txt", "r")
    elif arg.inputLFN == "dataHTMHT18C":
        inLFNList = open("/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/myInFiles/data2018/JetHT_Run2018C-Nano14Dec2018-v1.txt", "r")
    elif arg.inputLFN == "dataSMu18C":
        inLFNList = open("/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/myInFiles/data2018/SingleMuon_Run2018C-Nano14Dec2018-v1.txt", "r")
    elif arg.inputLFN == "dataSEl18C":
        inLFNList = open("/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/myInFiles/data2018/EGamma_Run2018C-Nano14Dec2018-v1.txt", "r")
    elif arg.inputLFN == "dataHTMHT18D":
        inLFNList = open("/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/myInFiles/data2018/JetHT_Run2018D-Nano14Dec2018_ver2-v1.txt", "r")
    elif arg.inputLFN == "dataSMu18D":
        inLFNList = open("/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/myInFiles/data2018/SingleMuon_Run2018D-Nano14Dec2018_ver2-v1.txt", "r")
    elif arg.inputLFN == "dataSEl18D":
        inLFNList = open("/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/myInFiles/data2018/EGamma_Run2018D-Nano14Dec2018_ver2-v1.txt", "r")
    elif not arg.inputLFN.find("tt_semilep102_18") == -1:
        inLFNList = open("/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/myInFiles/mc/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_102X_18.txt", "r")
    elif not arg.inputLFN.find("tttt102_18") == -1:
        inLFNList = open("/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/myInFiles/mc/TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_102X_18.txt", "r")
    else:
        return None

    return inLFNList


def main(argms):
    """ This is where the input files are chosen and the PostProcessor runs """

    redirector = chooseRedirector(argms)

    # inputLFNList = ioFiles(argms)
    # if inputLFNList is None: return 0

    pathToFile = redirector + argms.fileName

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
    skimmer(pathToFile, argms)


if __name__ == '__main__':
    t2 = time.time()
    main(process_arguments())
    t3 = time.time()
    print(">>>>> Total Elapsed time {0:7.1f} s ".format((t3 - t2)))
