# -*- coding: utf-8 -*-
"""
Created on Jan 2019

@author: NikHoffStyl
"""

from __future__ import (division, print_function)
import time
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from anaTrigsData import *


def main(argms):
    """
    This is where the input files are chosen and their contents are translated to variables.
    The PostProcessor runs to output a root file containing histograms of pt, eta and phi properties
    of jets, muons, electrons and MET.

    Args:
        argms: command line arguments

    """
    redirector = chooseRedirector(argms)
    trigList = getFileContents("../myInFiles/trigList.txt", True)
    preSelCuts = getFileContents("../myInFiles/preSelectionCuts.txt", False)
    selCriteria = getFileContents("selectionCriteria.txt", False)
    inputLFNList, thePostFix, outputFile = ioFiles(argms, selCriteria)

    if argms.noWriteFile: writeFile = False
    else: writeFile = True

    files = []
    for counter, line in enumerate(inputLFNList):
        counter += 1
        if not argms.fileLimit == -1:
            if counter > argms.fileLimit: break
        files.append(redirector + str(line).replace('\n', ''))

    cutsString = "nJet > {0} && ( nMuon >{1} || nElectron >{2} ) && (HLT_PFHT250 == 1 || HLT_Mu20 == 1)"\
        .format(preSelCuts["nJet"], preSelCuts["nMuon"], preSelCuts["nElectron"])

    p99 = PostProcessor(".",
                        files,
                        # files[0],
                        cut=cutsString,
                        # cut="nJet > 5 && ( nMuon >0 || nElectron >0 ) && (HLT_PFHT250 == 1 || HLT_Mu20 == 1)",
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
