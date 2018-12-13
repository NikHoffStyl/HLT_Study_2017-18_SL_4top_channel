from __future__ import (division, print_function)
from importlib import import_module
import time
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from histoMaker import HistogramMaker
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

def process_arguments():
    """ Process command-line arguments """

    parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--inputLFN", choices= ["ttjets","tttt", "tttt_weights", "wjets"],
                        default = "tttt", help= "Set list of input files")
    parser.add_argument("-r", "--redirector", choices= ["xrd-global","xrdUS","xrdEU_Asia", "eos", "iihe", "local"],
                        default = "local", help= "Sets redirector to query locations for LFN")
    parser.add_argument("-nw", "--noWriteFile", action = "store_true",
                        help="Does not output a ROOT file, which contains the histograms.")
    parser.add_argument("-e", "--eventLimit", type=int, default=-1,
                        help="Set a limit to the number of events.")
    #parser.add_argument("-t", "--triggerList", type=[], default = ['PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2','IsoMu24'])
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
        if argms.inputLFN == "ttjets": redirector="../myInFiles/TTjets/"
        elif argms.inputLFN == "tttt_weights": redirector = "../myInFiles/TTTTweights/"
        elif argms.inputLFN == "wjets": redirector = "../myInFiles/Wjets/"
        elif argms.inputLFN == "tttt": redirector = "../myInFiles/TTTT/"
        else: return 0
    else: return 0
    files=[]

    # Open the text list of files as read-only ("r" option), use as pairs to add proper postfix to output file
    # you may want to change path to suit your file ordering
    if argms.inputLFN == "ttjets": # tt + jets MC
        if argms.redirector == "local": inputLFNList =  open("../myInFiles/TTjets/TTjets_files.txt", "r")
        else: inputLFNList =  open("../NanoAODTools/StandaloneExamples/Infiles/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8.txt", "r")
        thePostFix = "TTJets_SL"
        outtputFile = "OutHistosTT6jets.root"
    elif argms.inputLFN == "tttt_weights": # tttt MC PSWeights
        if argms.redirector == "local": inputLFNList =  open("../myInFiles/TTTTweights/TTTTweights_files.txt", "r")
        else: inputLFNList =  open("../NanoAODTools/StandaloneExamples/Infiles/TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8.txt", "r")
        thePostFix = "TTTT_PSWeights"
        outtputFile = "OutHistosTTTTweights.root"
    elif argms.inputLFN == "wjets": # W (to Lep + Nu) + jets
        if  argms.redirector == "local": inputLFNList =  open("../myInFiles/Wjets/Wjets_files.txt", "r")
        else: inputLFNList =  open("../NanoAODTools/StandaloneExamples/Infiles/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8.txt", "r")
        thePostFix = "WJetsToLNu"
        outtputFile = "OutHistosWjets.root"
    elif argms.inputLFN == "tttt": # tttt MC
        if argms.redirector == "local": inputLFNList =  open("../myInFiles/TTTT/TTTT_files.txt", "r")
        else: inputLFNList =  open("../NanoAODTools/StandaloneExamples/Infiles/TTTT_TuneCP5_13TeV-amcatnlo-pythia8.txt", "r")
        thePostFix = "TTTT"
        outtputFile = "OutHistosTTTT_6jets.root"
    else: return 0

    if argms.noWriteFile: writeFile=False
    else: writeFile = True

    iterat = 0
    for line in inputLFNList:
        iterat += 1
        if iterat > 5: break
        #.replace('\n','') protects against new line characters at end of filenames, use just str(line) if problem appears
        files.append(redirector + str(line).replace('\n','') )

    trigDictionary={"HT": ['PFHT180', 'PFHT250', 'PFHT370', 'PFHT430','PFHT510',
                     'PFHT590', 'PFHT680', 'PFHT780', 'PFHT890', 'PFHT1050',
                     'PFHT380_SixPFJet32', 'PFHT430_SixPFJet40',
                     'PFHT380_SixPFJet32_DoublePFBTagCSV_2p2',
                     'PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2',
                     'PFHT430_SixPFJet40_PFBTagCSV_1p5'],
                    "Mu":['Mu17_TrkIsoVVL', 'Mu19_TrkIsoVVL', 'IsoMu24']
                    }

    p99=PostProcessor(".",
                      files,
                      #files[0],
                      cut="nJet > 5 && Jet_jetId>2 && abs(Jet_eta) <2.4 &&( nMuon >0 || nElectron >0 ) && Muon_softId == 1",
                      modules=[HistogramMaker(WriteHistFile=writeFile,
                                              EventLimit = argms.eventLimit,
                                              TrigDict=trigDictionary,
                                              TrigLst = ['IsoMu24','PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2','PFHT380_SixPFJet32_DoublePFBTagCSV_2p2','PFHT430_SixPFJet40_PFBTagCSV_1p5','PFHT430_SixPFJet40'])],
                      jsonInput=None,
                      noOut=True,
                      justcount=False,
                      postfix=thePostFix,
                      histFileName=outtputFile,
                      histDirName="plots",
                      #branchsel="../NanoAODTools/StandaloneExamples/Infiles/kd_branchsel.txt",
                      outputbranchsel="../NanoAODTools/StandaloneExamples/Infiles/kd_branchsel.txt",
                      )
    t0 = time.clock()
    p99.run()
    t1 = time.clock()
    print("Elapsed time %7.1fs" %(t1-t0))

main(process_arguments())
