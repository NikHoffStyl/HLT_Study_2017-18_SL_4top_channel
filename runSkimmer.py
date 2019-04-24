# -*- coding: utf-8 -*-
"""
Created on Jan 2019

@author: NikHoffStyl
"""

from __future__ import (division, print_function)
# from importlib import import_module
import time
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PfJetMultSkimmer import PfJetsSkimmer
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


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
    descriptor = arg.outputName
    if arg.inputLFN == "dataHTMHT17B":
        inLFNList = open("../myInFiles/data/HTMHT_Run2017B-Nano14Dec2018-v1.txt", "r")
        postFix = "dataHTMHT17B"
        outFile = "OutFiles/Skimmed{0}/dataHTMHT17B_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif arg.inputLFN == "dataSMu17B":
        inLFNList = open("../myInFiles/data/SingleMuon_Run2017B-Nano14Dec2018-v1.txt", "r")
        postFix = "dataSMu17B"
        outFile = "OutFiles/Skimmed{0}/dataSMu17B_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif arg.inputLFN == "dataSEl17B":
        inLFNList = open("../myInFiles/data/SingleElectron_Run2017B-Nano14Dec2018-v1.txt", "r")
        postFix = "dataSEl17B"
        outFile = "OutFiles/Skimmed{0}/dataSEl17B_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif arg.inputLFN == "dataHTMHT17C":
        inLFNList = open("../myInFiles/data/HTMHT_Run2017C-Nano14Dec2018-v1.txt", "r")
        postFix = "dataHTMHT17C"
        outFile = "OutFiles/Skimmed{0}/dataHTMHT17C_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif arg.inputLFN == "dataSMu17C":
        inLFNList = open("../myInFiles/data/SingleMuon_Run2017C-Nano14Dec2018-v1.txt", "r")
        postFix = "dataSMu17C"
        outFile = "OutFiles/Skimmed{0}/dataSMu17C_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif arg.inputLFN == "dataSEl17C":
        inLFNList = open("../myInFiles/data/SingleElectron_Run2017C-Nano14Dec2018-v1.txt", "r")
        postFix = "dataSEl17C"
        outFile = "OutFiles/Skimmed{0}/dataSEl17C_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif arg.inputLFN == "dataHTMHT17D":
        inLFNList = open("../myInFiles/data/HTMHT_Run2017D-Nano14Dec2018-v1.txt", "r")
        postFix = "dataHTMHT17D"
        outFile = "OutFiles/Skimmed{0}/dataHTMHT17D_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif arg.inputLFN == "dataSMu17D":
        inLFNList = open("../myInFiles/data/SingleMuon_Run2017D-Nano14Dec2018-v1.txt", "r")
        postFix = "dataSMu17D"
        outFile = "OutFiles/Skimmed{0}/dataSMu17D_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif arg.inputLFN == "dataSEl17D":
        inLFNList = open("../myInFiles/data/SingleElectron_Run2017D-Nano14Dec2018-v1.txt", "r")
        postFix = "dataSEl17D"
        outFile = "OutFiles/Skimmed{0}/dataSEl17D_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif arg.inputLFN == "dataHTMHT17E":
        inLFNList = open("../myInFiles/data/HTMHT_Run2017E-Nano14Dec2018-v1.txt", "r")
        postFix = "dataHTMHT17E"
        outFile = "OutFiles/Skimmed{0}/dataHTMHT17E_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif arg.inputLFN == "dataSMu17E":
        inLFNList = open("../myInFiles/data/SingleMuon_Run2017E-Nano14Dec2018-v1.txt", "r")
        postFix = "dataSMu17E"
        outFile = "OutFiles/Skimmed{0}/dataSMu17E_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif arg.inputLFN == "dataSEl17E":
        inLFNList = open("../myInFiles/data/SingleElectron_Run2017E-Nano14Dec2018-v1.txt", "r")
        postFix = "dataSEl17E"
        outFile = "OutFiles/Skimmed{0}/dataSEl17E_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif arg.inputLFN == "dataHTMHT17F":
        inLFNList = open("../myInFiles/data/HTMHT_Run2017F-Nano14Dec2018-v1.txt", "r")
        postFix = "dataHTMHT17F"
        outFile = "OutFiles/Skimmed{0}/dataHTMHT17F_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif arg.inputLFN == "dataSMu17F":
        inLFNList = open("../myInFiles/data/SingleMuon_Run2017F-Nano14Dec2018-v1.txt", "r")
        postFix = "dataSMu17F"
        outFile = "OutFiles/Skimmed{0}/dataSMu17F_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif arg.inputLFN == "dataSEl17F":
        inLFNList = open("../myInFiles/data/SingleElectron_Run2017F-Nano14Dec2018-v1.txt", "r")
        postFix = "dataSEl17F"
        outFile = "OutFiles/Skimmed{0}/dataSEl17F_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])

    elif not arg.inputLFN.find("tt_semilep102_17") == -1:
        inLFNList = open("../myInFiles/mc/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_102X.txt", "r")
        postFix = "TTToSemiLep102X"
        if arg.inputLFN == "tt_semilep102_17B":
            outFile = "OutFiles/Skimmed{0}/TTToSemiLep102X_17B_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
        elif arg.inputLFN == "tt_semilep102_17C":
            outFile = "OutFiles/Skimmed{0}/TTToSemiLep102X_17C_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
        elif arg.inputLFN == "tt_semilep102_17DEF":
            outFile = "OutFiles/Skimmed{0}/TTToSemiLep102X_17DEF_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])

    elif arg.inputLFN == "tt_semilep94":  # tt + jets MC
        inLFNList = open("../myInFiles/mc/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_94X.txt", "r")
        # inLFNList = open("../NanoAODTools/StandaloneExamples/Infiles/TTJets_"
        #                     "SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8.txt", "r")
        postFix = "TTToSemiLep94X"
        outFile = "OutFiles/Skimmed{0}/TTToSemiLep94X_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif arg.inputLFN == "ttjets94":
        if arg.redirector == "local":
            inLFNList = open(
                "../../myInFiles/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8/fileNames.txt", "r")
        else:
            inLFNList = open("../myInFiles/mc/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8_94X.txt", "r")
        postFix = "TTJets_SL_94"
        outFile = "OutFiles/Skimmed{0}/TT94_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif arg.inputLFN == "tttt_weights":
        if arg.redirector == "local":
            inLFNList = open("../../myInFiles/TTTTweights/TTTTweights_files.txt", "r")
        else:
            inLFNList = open("../myInFiles/mc/TTTTweights_files.txt", "r")
        postFix = "TTTT_PSWeights"
        outFile = "OutFiles/Skimmed{0}/TTTTweights.root"
    elif arg.inputLFN == "wjets":  # W (to Lep + Nu) + jets
        if arg.redirector == "local":
            inLFNList = open("../../myInFiles/Wjets/Wjets_files.txt", "r")
        else:
            inLFNList = open("../myInFiles/mc/Wjets_files.txt", "r")
        postFix = "WJetsToLNu"
        outFile = "OutFiles/Skimmed{0}/Wjets.root"
    elif arg.inputLFN == "tttt94":  # tttt MC
        if arg.redirector == "local":
            inLFNList = open("../../myInFiles/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/fileNames.txt", "r")
        else:
            inLFNList = open("../myInFiles/mc/TTTT_TuneCP5_13TeV-amcatnlo-pythia8_94X.txt", "r")
        postFix = "TTTT94"
        outFile = "OutFiles/Skimmed{0}/TTTT94X_6Jets1Mu{1}jPt_test.root".format(descriptor, selCrit["minJetPt"])
    elif not arg.inputLFN.find("tttt102_17") == -1:  # tttt MC
        if arg.redirector == "local":
            inLFNList = open("../../myInFiles/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/fileNames.txt", "r")
        else:
            inLFNList = open("../myInFiles/mc/TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_102X.txt", "r")
        postFix = "TTTT102"
        if arg.inputLFN == "tttt102_17B":
            outFile = "OutFiles/Skimmed{0}/TTTT102X_17B_6Jets1Mu{1}jPt_test.root".format(descriptor, selCrit["minJetPt"])
        elif arg.inputLFN == "tttt102_17C":
            outFile = "OutFiles/Skimmed{0}/TTTT102X_17C_6Jets1Mu{1}jPt_test.root".format(descriptor, selCrit["minJetPt"])
        elif arg.inputLFN == "tttt102_17DEF":
            outFile = "OutFiles/Skimmed{0}/TTTT102X_17DEF_6Jets1Mu{1}jPt_test.root".format(descriptor, selCrit["minJetPt"])

    else:
        inLFNList = None
        postFix = None
        outFile = None

    return inLFNList, postFix, outFile


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
            redirector = "myInFiles/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8/"
        elif argms.inputLFN == "tttt_weights":
            redirector = "myInFiles/TTTTweights/"
        elif argms.inputLFN == "wjets":
            redirector = "myInFiles/Wjets/"
        elif argms.inputLFN == "tttt":
            redirector = "myInFiles/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/"
        else:
            return 0
    else:
        return 0

    # Open the text list of files as read-only ("r" option), use as pairs to add proper postfix to output file
    # you may want to change path to suit your file ordering
    if argms.inputLFN == "dataHTMHT17B":
        inLFNList = open("myInFiles/data/HTMHT_Run2017B-Nano14Dec2018-v1.txt", "r")
        # postFix = "dataHTMHT17B"
        # outFile = "OutFiles/Skimmed{0}/dataHTMHT17B_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif argms.inputLFN == "dataSMu17B":
        inLFNList = open("myInFiles/data/SingleMuon_Run2017B-Nano14Dec2018-v1.txt", "r")
        # postFix = "dataSMu17B"
        # outFile = "OutFiles/Skimmed{0}/dataSMu17B_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif argms.inputLFN == "dataSEl17B":
        inLFNList = open("myInFiles/data/SingleElectron_Run2017B-Nano14Dec2018-v1.txt", "r")
        # postFix = "dataSEl17B"
        # outFile = "OutFiles/Skimmed{0}/dataSEl17B_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif argms.inputLFN == "dataHTMHT17C":
        inLFNList = open("myInFiles/data/HTMHT_Run2017C-Nano14Dec2018-v1.txt", "r")
        # postFix = "dataHTMHT17C"
        # outFile = "OutFiles/Skimmed{0}/dataHTMHT17C_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif argms.inputLFN == "dataSMu17C":
        inLFNList = open("myInFiles/data/SingleMuon_Run2017C-Nano14Dec2018-v1.txt", "r")
        # postFix = "dataSMu17C"
        # outFile = "OutFiles/Skimmed{0}/dataSMu17C_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif argms.inputLFN == "dataSEl17C":
        inLFNList = open("myInFiles/data/SingleElectron_Run2017C-Nano14Dec2018-v1.txt", "r")
        # postFix = "dataSEl17C"
        # outFile = "OutFiles/Skimmed{0}/dataSEl17C_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif argms.inputLFN == "dataHTMHT17D":
        inLFNList = open("myInFiles/data/HTMHT_Run2017D-Nano14Dec2018-v1.txt", "r")
        # postFix = "dataHTMHT17D"
        # outFile = "OutFiles/Skimmed{0}/dataHTMHT17D_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif argms.inputLFN == "dataSMu17D":
        inLFNList = open("myInFiles/data/SingleMuon_Run2017D-Nano14Dec2018-v1.txt", "r")
        # postFix = "dataSMu17D"
        # outFile = "OutFiles/Skimmed{0}/dataSMu17D_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif argms.inputLFN == "dataSEl17D":
        inLFNList = open("myInFiles/data/SingleElectron_Run2017D-Nano14Dec2018-v1.txt", "r")
        # postFix = "dataSEl17D"
        # outFile = "OutFiles/Skimmed{0}/dataSEl17D_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif argms.inputLFN == "dataHTMHT17E":
        inLFNList = open("myInFiles/data/HTMHT_Run2017E-Nano14Dec2018-v1.txt", "r")
        # postFix = "dataHTMHT17E"
        # outFile = "OutFiles/Skimmed{0}/dataHTMHT17E_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif argms.inputLFN == "dataSMu17E":
        inLFNList = open("myInFiles/data/SingleMuon_Run2017E-Nano14Dec2018-v1.txt", "r")
        # postFix = "dataSMu17E"
        # outFile = "OutFiles/Skimmed{0}/dataSMu17E_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif argms.inputLFN == "dataSEl17E":
        inLFNList = open("myInFiles/data/SingleElectron_Run2017E-Nano14Dec2018-v1.txt", "r")
        # postFix = "dataSEl17E"
        # outFile = "OutFiles/Skimmed{0}/dataSEl17E_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif argms.inputLFN == "dataHTMHT17F":
        inLFNList = open("myInFiles/data/HTMHT_Run2017F-Nano14Dec2018-v1.txt", "r")
        # postFix = "dataHTMHT17F"
        # outFile = "OutFiles/Skimmed{0}/dataHTMHT17F_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif argms.inputLFN == "dataSMu17F":
        inLFNList = open("myInFiles/data/SingleMuon_Run2017F-Nano14Dec2018-v1.txt", "r")
        # postFix = "dataSMu17F"
        # outFile = "OutFiles/Skimmed{0}/dataSMu17F_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif argms.inputLFN == "dataSEl17F":
        inLFNList = open("myInFiles/data/SingleElectron_Run2017F-Nano14Dec2018-v1.txt", "r")
        # postFix = "dataSEl17F"
        # outFile = "OutFiles/Skimmed{0}/dataSEl17F_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])

    elif not argms.inputLFN.find("tt_semilep102_17") == -1:
        inLFNList = open("myInFiles/mc/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_102X.txt", "r")
        # postFix = "TTToSemiLep102X"
        # if argms.inputLFN == "tt_semilep102_17B":
        #     outFile = "OutFiles/Skimmed{0}/TTToSemiLep102X_17B_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
        # elif argms.inputLFN == "tt_semilep102_17C":
        #     outFile = "OutFiles/Skimmed{0}/TTToSemiLep102X_17C_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
        # elif argms.inputLFN == "tt_semilep102_17DEF":
        #     outFile = "OutFiles/Skimmed{0}/TTToSemiLep102X_17DEF_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])

    elif argms.inputLFN == "tt_semilep94":  # tt + jets MC
        inLFNList = open("myInFiles/mc/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_94X.txt", "r")
        # inLFNList = open("../NanoAODTools/StandaloneExamples/Infiles/TTJets_"
        #                     "SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8.txt", "r")
        # postFix = "TTToSemiLep94X"
        # outFile = "OutFiles/Skimmed{0}/TTToSemiLep94X_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif argms.inputLFN == "ttjets94":
        if argms.redirector == "local":
            inLFNList = open(
                "../myInFiles/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8/fileNames.txt", "r")
        else:
            inLFNList = open("myInFiles/mc/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8_94X.txt", "r")
        # postFix = "TTJets_SL_94"
        # outFile = "OutFiles/Skimmed{0}/TT94_6Jets1Mu{1}jPt.root".format(descriptor, selCrit["minJetPt"])
    elif argms.inputLFN == "tttt_weights":
        if argms.redirector == "local":
            inLFNList = open("../myInFiles/TTTTweights/TTTTweights_files.txt", "r")
        else:
            inLFNList = open("myInFiles/mc/TTTTweights_files.txt", "r")
        # postFix = "TTTT_PSWeights"
        # outFile = "OutFiles/Skimmed{0}/TTTTweights.root"
    elif argms.inputLFN == "wjets":  # W (to Lep + Nu) + jets
        if argms.redirector == "local":
            inLFNList = open("../myInFiles/Wjets/Wjets_files.txt", "r")
        else:
            inLFNList = open("myInFiles/mc/Wjets_files.txt", "r")
        # postFix = "WJetsToLNu"
        outFile = "OutFiles/Skimmed{0}/Wjets.root"
    elif argms.inputLFN == "tttt94":  # tttt MC
        if argms.redirector == "local":
            inLFNList = open("../myInFiles/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/fileNames.txt", "r")
        else:
            inLFNList = open("myInFiles/mc/TTTT_TuneCP5_13TeV-amcatnlo-pythia8_94X.txt", "r")
        # postFix = "TTTT94"
        # outFile = "OutFiles/Skimmed{0}/TTTT94X_6Jets1Mu{1}jPt_test.root".format(descriptor, selCrit["minJetPt"])
    elif not argms.inputLFN.find("tttt102_17") == -1:  # tttt MC
        if argms.redirector == "local":
            inLFNList = open("../myInFiles/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/fileNames.txt", "r")
        else:
            inLFNList = open("myInFiles/mc/TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_102X.txt", "r")
        postFix = "TTTT102"
        # if argms.inputLFN == "tttt102_17B":
        #     outFile = "OutFiles/Skimmed{0}/TTTT102X_17B_6Jets1Mu{1}jPt_test.root".format(descriptor, selCrit["minJetPt"])
        # elif argms.inputLFN == "tttt102_17C":
        #     outFile = "OutFiles/Skimmed{0}/TTTT102X_17C_6Jets1Mu{1}jPt_test.root".format(descriptor, selCrit["minJetPt"])
        # elif argms.inputLFN == "tttt102_17DEF":
        #     outFile = "OutFiles/Skimmed{0}/TTTT102X_17DEF_6Jets1Mu{1}jPt_test.root".format(descriptor, selCrit["minJetPt"])
    else:
        return 0

    files = []
    for counter, line in enumerate(inLFNList):
        counter += 1
        if counter > 3: break
        files.append(redirector + str(line).replace('\n', ''))

    thePostFix = argms.inputLFN

    p99 = PostProcessor(".",
                        files,
                        # files[0],
                        cut="nJet > 5 && ( nMuon >0 || nElectron >0 ) ",
                        modules=[PfJetsSkimmer()],
                        postfix=thePostFix,
                        # histFileName=outputFile,
                        # histDirName="plots",
                        branchsel="myInFiles/kd_branchsel.txt",
                        outputbranchsel="myInFiles/kd_branchsel.txt",
                        )
    t0 = time.clock()
    p99.run()
    t1 = time.clock()
    print("Elapsed time %7.1fs" % (t1-t0))


main(process_arguments())

