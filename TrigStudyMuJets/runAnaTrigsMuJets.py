# -*- coding: utf-8 -*-
"""
Created on Jan 2019

@author: NikHoffStyl
"""
from __future__ import (division, print_function)
import time
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from anaTrigsMuJets import *


def main(argms):
    """
    This is where the input files are chosen and the PostProcessor runs
    Args:
        argms: command line arguments

    Returns:

    """
    redirector = chooseRedirector(argms)
    if not argms.inputLFN.find("17B") == -1:
        trigList = getFileContents("../myInFiles/2017ABtrigList.txt", True)
        era2017 = "17AB"
    elif not argms.inputLFN.find("17C") == -1:
        trigList = getFileContents("../myInFiles/2017CtrigList.txt", True)
        era2017 = "17C"
    elif not argms.inputLFN.find("17D") or argms.inputLFN.find("17E") or argms.inputLFN.find("17F") == -1:
        trigList = getFileContents("../myInFiles/2017DEFtrigList.txt", True)
        era2017 = "17DEF"
    else:
        trigList = getFileContents("../myInFiles/trigList.txt", True)
        era2017 = "original"

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

    p99 = PostProcessor(".",
                        files,
                        # files[0],
                        cut="nJet > 5 && ( nMuon >0 || nElectron >0 )",
                        modules=[TriggerStudy(writeHistFile=writeFile,
                                              eventLimit=argms.eventLimit,
                                              trigLst=trigList,
                                              era=era2017)],
                        # jsonInput=None,
                        # noOut=True,
                        haddFileName="TestBranch.root",
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
