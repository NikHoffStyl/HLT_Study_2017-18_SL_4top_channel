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
from PfJetMultSkimmer import PfJetsSkimmer
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from multiprocessing import Process


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
    parser.add_argument("-o", "--outputName", default="_v", help="Set name of output file")
    args = parser.parse_args()
    return args


def skimmer(file, arg):
    """

    Args:
        file: input files of datasets
        arg: the string attached to the end of the file names

    Returns:

    """
    thePostFix = arg.inputLFN
    p99 = PostProcessor("SingleElectron/17F",
                        # "TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_102X",
                        # "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_102X",
                        [file],
                        cut="nJet > 5 && ( nMuon >0 || nElectron >0 ) ",
                        modules=[PfJetsSkimmer(eventLimit=arg.eventLimit)],
                        postfix=thePostFix,
                        branchsel="myInFiles/kd_branchsel.txt",
                        outputbranchsel="myInFiles/kd_branchsel.txt",
                        )
    #p99.inputFiles
    print(p99.inputFiles)
    t0 = time.time()
    p99.run()
    t1 = time.time()
    proc = os.getpid()
    print("Elapsed time {0:7.1f} s by process id: {1}".format((t1 - t0), proc))


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
        # outFile = "OutFiles/Skimmed{0}/dataHTMHT17B_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif arg.inputLFN == "dataSMu17B":
        inLFNList = open("myInFiles/data/SingleMuon_Run2017B-Nano14Dec2018-v1.txt", "r")
        # outFile = "OutFiles/Skimmed{0}/dataSMu17B_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif arg.inputLFN == "dataSEl17B":
        inLFNList = open("myInFiles/data/SingleElectron_Run2017B-Nano14Dec2018-v1.txt", "r")
        # outFile = "OutFiles/Skimmed{0}/dataSEl17B_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif arg.inputLFN == "dataHTMHT17C":
        inLFNList = open("myInFiles/data/HTMHT_Run2017C-Nano14Dec2018-v1.txt", "r")
        # outFile = "OutFiles/Skimmed{0}/dataHTMHT17C_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif arg.inputLFN == "dataSMu17C":
        inLFNList = open("myInFiles/data/SingleMuon_Run2017C-Nano14Dec2018-v1.txt", "r")
        # outFile = "OutFiles/Skimmed{0}/dataSMu17C_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif arg.inputLFN == "dataSEl17C":
        inLFNList = open("myInFiles/data/SingleElectron_Run2017C-Nano14Dec2018-v1.txt", "r")
        # outFile = "OutFiles/Skimmed{0}/dataSEl17C_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif arg.inputLFN == "dataHTMHT17D":
        inLFNList = open("myInFiles/data/HTMHT_Run2017D-Nano14Dec2018-v1.txt", "r")
        # outFile = "OutFiles/Skimmed{0}/dataHTMHT17D_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif arg.inputLFN == "dataSMu17D":
        inLFNList = open("myInFiles/data/SingleMuon_Run2017D-Nano14Dec2018-v1.txt", "r")
        # outFile = "OutFiles/Skimmed{0}/dataSMu17D_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif arg.inputLFN == "dataSEl17D":
        inLFNList = open("myInFiles/data/SingleElectron_Run2017D-Nano14Dec2018-v1.txt", "r")
        # outFile = "OutFiles/Skimmed{0}/dataSEl17D_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif arg.inputLFN == "dataHTMHT17E":
        inLFNList = open("myInFiles/data/HTMHT_Run2017E-Nano14Dec2018-v1.txt", "r")
        # outFile = "OutFiles/Skimmed{0}/dataHTMHT17E_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif arg.inputLFN == "dataSMu17E":
        inLFNList = open("myInFiles/data/SingleMuon_Run2017E-Nano14Dec2018-v1.txt", "r")
        # outFile = "OutFiles/Skimmed{0}/dataSMu17E_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif arg.inputLFN == "dataSEl17E":
        inLFNList = open("myInFiles/data/SingleElectron_Run2017E-Nano14Dec2018-v1.txt", "r")
        # outFile = "OutFiles/Skimmed{0}/dataSEl17E_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif arg.inputLFN == "dataHTMHT17F":
        inLFNList = open("myInFiles/data/HTMHT_Run2017F-Nano14Dec2018-v1.txt", "r")
        # outFile = "OutFiles/Skimmed{0}/dataHTMHT17F_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif arg.inputLFN == "dataSMu17F":
        inLFNList = open("myInFiles/data/SingleMuon_Run2017F-Nano14Dec2018-v1.txt", "r")
        # outFile = "OutFiles/Skimmed{0}/dataSMu17F_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif arg.inputLFN == "dataSEl17F":
        inLFNList = open("myInFiles/data/SingleElectron_Run2017F-Nano14Dec2018-v1.txt", "r")
        # outFile = "OutFiles/Skimmed{0}/dataSEl17F_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])

    elif not arg.inputLFN.find("tt_semilep102_17") == -1:
        inLFNList = open("myInFiles/mc/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_102X.txt", "r")
        # if arg.inputLFN == "tt_semilep102_17B":
        #     outFile = "OutFiles/Skimmed{0}/TTToSemiLep102X_17B_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
        # elif arg.inputLFN == "tt_semilep102_17C":
        #     outFile = "OutFiles/Skimmed{0}/TTToSemiLep102X_17C_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
        # elif arg.inputLFN == "tt_semilep102_17DEF":
        #     outFile = "OutFiles/Skimmed{0}/TTToSemiLep102X_17DEF_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])

    elif arg.inputLFN == "tt_semilep94":  # tt + jets MC
        inLFNList = open("myInFiles/mc/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_94X.txt", "r")
        # outFile = "OutFiles/Skimmed{0}/TTToSemiLep94X_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif arg.inputLFN == "ttjets94":
        if arg.redirector == "local":
            inLFNList = open(
                "../myInFiles/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8/fileNames.txt", "r")
        else:
            inLFNList = open("myInFiles/mc/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8_94X.txt", "r")
        # outFile = "OutFiles/Skimmed{0}/TT94_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif arg.inputLFN == "tttt_weights":
        if arg.redirector == "local":
            inLFNList = open("../myInFiles/TTTTweights/TTTTweights_files.txt", "r")
        else:
            inLFNList = open("myInFiles/mc/TTTTweights_files.txt", "r")
        # outFile = "OutFiles/Skimmed{0}/TTTTweights.root"
    elif arg.inputLFN == "wjets":  # W (to Lep + Nu) + jets
        if arg.redirector == "local":
            inLFNList = open("../myInFiles/Wjets/Wjets_files.txt", "r")
        else:
            inLFNList = open("myInFiles/mc/Wjets_files.txt", "r")
        outFile = "OutFiles/Skimmed{0}/Wjets.root"
    elif arg.inputLFN == "tttt94":  # tttt MC
        if arg.redirector == "local":
            inLFNList = open("../myInFiles/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/fileNames.txt", "r")
        else:
            inLFNList = open("myInFiles/mc/TTTT_TuneCP5_13TeV-amcatnlo-pythia8_94X.txt", "r")
        # outFile = "OutFiles/Skimmed{0}/TTTT94X_6Jets1Mu{1}jPt_test.root".format(descriptor, selCrit["minJetPt"])
    elif not arg.inputLFN.find("tttt102_17") == -1:  # tttt MC
        if arg.redirector == "local":
            inLFNList = open("../myInFiles/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/fileNames.txt", "r")
        else:
            inLFNList = open("myInFiles/mc/TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_102X.txt", "r")
        # if arg.inputLFN == "tttt102_17B":
        #     outFile = "OutFiles/Skimmed{0}/TTTT102X_17B_6Jets1Mu{1}jPt_test.root".format(descriptor, selCrit["minJetPt"])
        # elif arg.inputLFN == "tttt102_17C":
        #     outFile = "OutFiles/Skimmed{0}/TTTT102X_17C_6Jets1Mu{1}jPt_test.root".format(descriptor, selCrit["minJetPt"])
        # elif arg.inputLFN == "tttt102_17DEF":
        #     outFile = "OutFiles/Skimmed{0}/TTTT102X_17DEF_6Jets1Mu{1}jPt_test.root".format(descriptor, selCrit["minJetPt"])
    else:
        return None

    return inLFNList


def main(argms):
    """ This is where the input files are chosen and the PostProcessor runs """

    redirector = chooseRedirector(argms)

    inputLFNList = ioFiles(argms)
    if inputLFNList is None: return 0

    allFiles = []
    for counter, line in enumerate(inputLFNList):
        counter += 1
        if not argms.fileLimit == -1:
            if counter > argms.fileLimit: break
        allFiles.append(redirector + str(line).replace('\n', ''))

    procs = []
    for index, files in enumerate(allFiles):
        proc = Process(target=skimmer, args=(files, argms,))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

    print("End of job!")
    #skimmer(allFiles, argms)


if __name__ == '__main__':
    main(process_arguments())
