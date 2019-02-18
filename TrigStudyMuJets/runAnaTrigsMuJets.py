from __future__ import (division, print_function)
# from importlib import import_module
import time
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from anaTrigsMuJets import TriggerStudy
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


def process_arguments():
    """ Process command-line arguments """

    parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--inputLFN", choices=["ttjets", "tttt", "tttt_weights", "wjets"],
                        default="tttt", help="Set list of input files")
    parser.add_argument("-r", "--redirector", choices=["xrd-global", "xrdUS", "xrdEU_Asia", "eos", "iihe", "local"],
                        default="local", help="Sets redirector to query locations for LFN")
    parser.add_argument("-nw", "--noWriteFile", action="store_true",
                        help="Does not output a ROOT file, which contains the histograms.")
    parser.add_argument("-e", "--eventLimit", type=int, default=1000000,
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
            redirector = "../../myInFiles/TTjets/"
        elif argms.inputLFN == "tttt_weights":
            redirector = "../../myInFiles/TTTTweights/"
        elif argms.inputLFN == "wjets":
            redirector = "../../myInFiles/Wjets/"
        elif argms.inputLFN == "tttt":
            redirector = "../../myInFiles/TTTT/"
        else:
            return 0
    else:
        return 0
    files = []

    # Open the text list of files as read-only ("r" option), use as pairs to add proper postfix to output file
    # you may want to change path to suit your file ordering
    if argms.inputLFN == "ttjets":  # tt + jets MC
        if argms.redirector == "local":
            inputLFNList = open("../../myInFiles/TTjets/TTjets_files.txt", "r")
        else:
            inputLFNList = open("../myInFiles/TTjets_files.txt", "r")
            # inputLFNList = open("../NanoAODTools/StandaloneExamples/Infiles/TTJets_"
            #                     "SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8.txt", "r")
        thePostFix = "TTJets_SL"
        outputFile = "../OutFiles/Histograms/TT6jets2.root"
    elif argms.inputLFN == "tttt_weights":  # tttt MC PSWeights
        if argms.redirector == "local":
            inputLFNList = open("../../myInFiles/TTTTweights/TTTTweights_files.txt", "r")
        else:
            inputLFNList = open("../myInFiles/TTTTweights_files.txt", "r")
        thePostFix = "TTTT_PSWeights"
        outputFile = "../OutFiles/Histograms/TTTTweights.root"
    elif argms.inputLFN == "wjets":  # W (to Lep + Nu) + jets
        if argms.redirector == "local":
            inputLFNList = open("../../myInFiles/Wjets/Wjets_files.txt", "r")
        else:
            inputLFNList = open("../myInFiles/Wjets_files.txt", "r")
        thePostFix = "WJetsToLNu"
        outputFile = "../OutFiles/Histograms/Wjets.root"
    elif argms.inputLFN == "tttt":  # tttt MC
        if argms.redirector == "local":
            inputLFNList = open("../../myInFiles/TTTT/TTTT_files.txt", "r")
        else:
            inputLFNList = open("../myInFiles/TTTT_files.txt", "r")
        thePostFix = "TTTT"
        outputFile = "../OutFiles/Histograms/TTTT_6jets2.root"
    else:
        return 0

    if argms.noWriteFile:
        writeFile = False
    else:
        writeFile = True

    iterat = 0
    for line in inputLFNList:
        iterat += 1
        if iterat > 5:
            break
        # .replace('\n','') protects against new line characters at end of filenames,
        # use just str(line) if problem appears
        files.append(redirector + str(line).replace('\n', ''))

    trigList = {}
    with open("trigList.txt") as f:
        for line in f:
            if line.find(":") == -1: continue
            (key, val) = line.split(": ")
            c = len(val) - 1
            val = val[0:c]
            trigList[key] = val.split(", ")

    # trigList = {"MuPJets": [],
    #             "ElPJets": [],
    #             "MuLone": ['Mu15_IsoVVVL_PFHT450_CaloBTagCSV_4p5'],
    #             "ElLone": ['Ele28_eta2p1_WPTight_Gsf_HT150'],
    #             "Muon": ['IsoMu24'],
    #             "Electron": ["Ele32_WPTight_Gsf", "Ele35_WPTight_Gsf", "Ele38_WPTight_Gsf"],
    #             "Jet": ['PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2']}

    p99 = PostProcessor(".",
                        files,
                        # files[0],
                        cut="nJet > 5 && ( nMuon >0 || nElectron >0 ) " 
                            "&& Muon_softId == 1",
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
