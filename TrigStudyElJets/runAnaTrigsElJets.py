# -*- coding: utf-8 -*-
"""
Created on Jan 2019

@author: NikHoffStyl
"""
from __future__ import (division, print_function)
# from importlib import import_module
import time
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from anaTrigsElJets import TriggerStudy
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


def process_arguments():
    """ Process command-line arguments """

    parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--inputLFN", choices=["tt_semilep94", "ttjets94", "tttt94", "tttt_weights", "wjets",
                                                     "tt_semilep102", "ttjets102", "tttt102",
                                                     "dataHTMHT17F", "dataSMu17F", "dataSEl17F"],
                        default="tttt", help="Set list of input files")
    parser.add_argument("-r", "--redirector", choices=["xrd-global", "xrdUS", "xrdEU_Asia", "eos", "iihe", "local"],
                        default="xrd-global", help="Sets redirector to query locations for LFN")
    parser.add_argument("-nw", "--noWriteFile", action="store_true",
                        help="Does not output a ROOT file, which contains the histograms.")
    parser.add_argument("-e", "--eventLimit", type=int, default=-1,
                        help="Set a limit to the number of events.")
    args = parser.parse_args()
    return args


def main(argms):
    """ This is where the input files are chosen and the PostProcessor runs """

    if argms.redirector == "xrd-global":
        redirector = "root://cms-xrd-global.cern.ch/"
    elif argms.redirector == "xrdUS":
        redirector = "root://cmsxrootd.fnal.gov/"
    elif argms.redirector == "xrdEU_Asia":
        redirector = "root://xrootd-cms.infn.it/"
    elif argms.redirector == "eos":
        redirector = "root://cmseos.fnal.gov/"
    elif argms.redirector == "iihe":
        redirector = "dcap://maite.iihe.ac.be/pnfs/iihe/cms/ph/sc4/"
    elif argms.redirector == "local":
        if argms.inputLFN == "ttjets":
            redirector = "../../myInFiles/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8/"
        elif argms.inputLFN == "tttt_weights":
            redirector = "../../myInFiles/TTTTweights/"
        elif argms.inputLFN == "wjets":
            redirector = "../../myInFiles/Wjets/"
        elif argms.inputLFN == "tttt":
            redirector = "../../myInFiles/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/"
        else:
            return 0
    else:
        return 0
    files = []

    preSelCuts = {}
    with open("../myInFiles/preSelectionCuts.txt") as f:
        for line in f:
            if line.find(":") == -1: continue
            (key1, val) = line.split(": ")
            c = len(val) - 1
            val = val[0:c]
            preSelCuts[key1] = val

    selCriteria = {}
    with open("selectionCriteria.txt") as f:
        for line in f:
            if line.find(":") == -1: continue
            (key1, val) = line.split(": ")
            c = len(val) - 1
            val = val[0:c]
            selCriteria[key1] = val

    # Open the text list of files as read-only ("r" option), use as pairs to add proper postfix to output file
    # you may want to change path to suit your file ordering
    if argms.inputLFN == "dataHTMHT17F":
        inputLFNList = open("../myInFiles/data/HTMHT_Run2017F-Nano14Dec2018-v1.txt", "r")
        thePostFix = "dataHTMHT17F"
        outputFile = "../OutFiles/Histograms/dataHTMHT17F_6Jets1Mu{0}jPt.root".format(selCriteria["minJetPt"])
    elif argms.inputLFN == "dataSMu17F":
        inputLFNList = open("../myInFiles/data/SingleMuon_Run2017F-Nano14Dec2018-v1.txt", "r")
        thePostFix = "dataSMu17F"
        outputFile = "../OutFiles/Histograms/dataSMu17F_6Jets1Mu{0}jPt.root".format(selCriteria["minJetPt"])
    elif argms.inputLFN == "dataSEl17F":
        inputLFNList = open("../myInFiles/data/SingleElectron_Run2017F-Nano14Dec2018-v1.txt", "r")
        thePostFix = "dataSEl17F"
        outputFile = "../OutFiles/Histograms/dataSEl17F_6Jets1Mu{0}jPt.root".format(selCriteria["minJetPt"])
    elif argms.inputLFN == "tt_semilep94":
        inputLFNList = open("../myInFiles/mc/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_94X.txt", "r")
        # inputLFNList = open("../NanoAODTools/StandaloneExamples/Infiles/TTJets_"
        #                     "SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8.txt", "r")
        thePostFix = "TTToSemiLep94X"
        outputFile = "../OutFiles/Histograms/TTToSemiLep94X_6Jets1Mu{0}jPt.root".format(selCriteria["minJetPt"])
    elif argms.inputLFN == "tt_semilep102":
        inputLFNList = open("../myInFiles/mc/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_102X.txt", "r")
        thePostFix = "TTToSemiLep102X"
        outputFile = "../OutFiles/Histograms/TTToSemiLep102X_6Jets1Mu{0}jPt.root".format(selCriteria["minJetPt"])
    elif argms.inputLFN == "ttjets94":
        if argms.redirector == "local":
            inputLFNList = open("../../myInFiles/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8/fileNames.txt", "r")
        else:
            inputLFNList = open("../myInFiles/mc/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8_94X.txt", "r")
        thePostFix = "TTJets_SL_94"
        outputFile = "../OutFiles/Histograms/TT94_6Jets1Mu{0}jPt.root" .format(selCriteria["minJetPt"])
    elif argms.inputLFN == "tttt_weights":
        if argms.redirector == "local":
            inputLFNList = open("../../myInFiles/TTTTweights/TTTTweights_files.txt", "r")
        else:
            inputLFNList = open("../myInFiles/mc/TTTTweights_files.txt", "r")
        thePostFix = "TTTT_PSWeights"
        outputFile = "../OutFiles/Histograms/TTTTweights.root"
    elif argms.inputLFN == "wjets":  # W (to Lep + Nu) + jets
        if argms.redirector == "local":
            inputLFNList = open("../../myInFiles/Wjets/Wjets_files.txt", "r")
        else:
            inputLFNList = open("../myInFiles/mc/Wjets_files.txt", "r")
        thePostFix = "WJetsToLNu"
        outputFile = "../OutFiles/Histograms/Wjets.root"
    elif argms.inputLFN == "tttt94":
        if argms.redirector == "local":
            inputLFNList = open("../../myInFiles/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/fileNames.txt", "r")
        else:
            inputLFNList = open("../myInFiles/mc/TTTT_TuneCP5_13TeV-amcatnlo-pythia8_94X.txt", "r")
        thePostFix = "TTTT94"
        outputFile = "../OutFiles/Histograms/TTTT94X_6Jets1Mu{0}jPt_test.root" .format(selCriteria["minJetPt"])
    elif argms.inputLFN == "tttt102":
        if argms.redirector == "local":
            inputLFNList = open("../../myInFiles/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/fileNames.txt", "r")
        else:
            inputLFNList = open("../myInFiles/mc/TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_102X.txt", "r")
        thePostFix = "TTTT102"
        outputFile = "../OutFiles/Histograms/TTTT102X_6Jets1Mu{0}jPt_test.root" .format(selCriteria["minJetPt"])
    else:
        return 0

    if argms.noWriteFile:
        writeFile = False
    else:
        writeFile = True

    for iterat, line in enumerate(inputLFNList):
        iterat += 1
        if iterat > 5: break
        files.append(redirector + str(line).replace('\n', ''))

    trigList = {}
    with open("trigList.txt") as f:
        for line in f:
            if line.find(":") == -1: continue
            (key, val) = line.split(": ")
            c = len(val) - 1
            val = val[0:c]
            trigList[key] = val.split(", ")

    p99 = PostProcessor(".",
                        files,
                        # files[0],
                        cut="nJet > 5 && ( nMuon >0 || nElectron >0 ) ",
                        modules=[TriggerStudy(writeHistFile=writeFile,
                                              eventLimit=argms.eventLimit,
                                              trigLst=trigList)],
                        # jsonInput=None,
                        noOut=True,
                        # justcount=False,
                        postfix=thePostFix,
                        histFileName=outputFile,
                        histDirName="plots",
                        branchsel="../myInFiles/kd_branchsel.txt",
                        outputbranchsel="../myInFiles/kd_branchsel.txt",
                        )
    t0 = time.clock()
    p99.run()
    t1 = time.clock()
    print("Elapsed time %7.1fs" % (t1-t0))

main(process_arguments())
