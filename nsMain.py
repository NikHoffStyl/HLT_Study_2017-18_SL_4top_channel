from __future__ import (division, print_function)

import ROOT
from ROOT import TLatex
from importlib import import_module
import time

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from histoMaker import HistogramMaker
from argProcessor import process_arguments as args
#from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

"""def process_arguments():
    parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-e", "--events-per-job", type=int, default=1000,
                        help="Set the number of events per job")
    parser.add_argument("-t1", "--triggerpath1", default="PFHT380_SixPFJet32_DoublePFBTagCSV_2p2",
                        help="Set the first trigger path")
    parser.add_argument("-t2", "--triggerpath2", default="IsoMu24",
                        help="Set the second trigger path")
    args = parser.parse_args()
    return args

argms = process_arguments()"""

filePrefix = "root://cms-xrd-global.cern.ch/"
#filePrefix = "root://cmseos.fnal.gov/"
files=[]
#Open the text list of files as read-only ("r" option), use as pairs to add proper postfix to output file
inputList =  open("../NanoAODTools/StandaloneExamples/Infiles/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8.txt", "r") # tt + jets MC
thePostFix = "TTJets_SL"
#inputList =  open("../NanoAODTools/StandaloneExamples/Infiles/TTTT_TuneCP5_13TeV-amcatnlo-pythia8.txt", "r") # tttt MC
#thePostFix = "TTTT"
#inputList =  open("../Infiles/TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8.txt", "r") # tttt MC PSWeights
#thePostFix = "TTTT_PSWeights"
#inputList =  open("../Infiles/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8.txt", "r") # W (to Lep + Nu) + jets
#thePostFix = "WJetsToLNu"

for line in inputList:
    #.replace('\n','') protects against new line characters at end of filenames, use just str(line) if problem appears
    files.append(filePrefix + str(line).replace('\n','') )

"""for file in files:
    print(file)"""
onefile=[files[0]]

p99=PostProcessor(".",
                  #files,
                  onefile,
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