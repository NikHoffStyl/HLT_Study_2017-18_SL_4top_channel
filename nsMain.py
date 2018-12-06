from __future__ import (division, print_function)
from importlib import import_module
import time
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from histoMaker import HistogramMaker
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

def process_arguments():
    """ Process command-line arguments """

    parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("--ttjets", action = "store_true", help="Set input files to tt + jets MC")
    parser.add_argument("--tttt", action = "store_true", help="Set input files to tttt MC")
    parser.add_argument("--tttt_weights", action = "store_true", help="Set input files to tttt MC with PSWeights")
    parser.add_argument("--wjets", action = "store_true", help="Set input files to W (to lep + Nu) +jets MC")
    args = parser.parse_args()

    return args

def main(argms):
    """ This is where the input files are chosen and the PostProcessor runs """

    filePrefix = "root://cms-xrd-global.cern.ch/"
    #filePrefix = "root://cmseos.fnal.gov/"
    files=[]

    # Open the text list of files as read-only ("r" option), use as pairs to add proper postfix to output file
    # you may want to change path to suit your file ordering
    if argms.ttjets:
        inputList =  open("../NanoAODTools/StandaloneExamples/Infiles/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8.txt", "r") # tt + jets MC
        thePostFix = "TTJets_SL"
    elif argms.tttt_weights:
        inputList =  open("../NanoAODTools/StandaloneExamples/Infiles/TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8.txt", "r") # tttt MC PSWeights
        thePostFix = "TTTT_PSWeights"
    elif argms.wjets:
        inputList =  open("../NanoAODTools/StandaloneExamples/Infiles/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8.txt", "r") # W (to Lep + Nu) + jets
        thePostFix = "WJetsToLNu"
    else:
        inputList =  open("../NanoAODTools/StandaloneExamples/Infiles/TTTT_TuneCP5_13TeV-amcatnlo-pythia8.txt", "r") # tttt MC
        thePostFix = "TTTT"


    for line in inputList:
        #.replace('\n','') protects against new line characters at end of filenames, use just str(line) if problem appears
        files.append(filePrefix + str(line).replace('\n','') )

    """for file in files:
          print(file)"""
    onefile=[files[0]]

    p99=PostProcessor(".",
                      files,
                      #onefile,
                      cut="nJet > 5 && ( nMuon >0 || nElectron >0 )",
                      modules=[HistogramMaker()],
                      jsonInput=None,
                      noOut=True,
                      justcount=False,
                      postfix=thePostFix,
                      histFileName="../RWOutput/OutHistoMaker2.root",
                      histDirName="plots",
                      )
    t0 = time.clock()
    p99.run()
    t1 = time.clock()
    print("Elapsed time %7.1fs" %(t1-t0))

main(process_arguments())
