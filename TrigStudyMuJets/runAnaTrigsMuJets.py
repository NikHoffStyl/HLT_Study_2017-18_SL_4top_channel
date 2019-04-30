# -*- coding: utf-8 -*-
"""
Created on Jan 2019

@author: NikHoffStyl
"""
from __future__ import (division, print_function)
import time
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from anaTrigsMuJets import *


def findEraRootFiles(path, verbose=False, FullPaths=True):
    """
    Find Root files in a given directory/path.
    Args:
        path (string): directory
        verbose (bool): print to stdout if true
        FullPaths (bool): return path plus file name in list elements

    Returns: files (list): list of names of root files in the directory given as argument

    """
    files = []
    if not path[-1] == '/': path += '/'
    if verbose: print(' >> Looking for files in path: ' + path)
    for f in os.listdir(path):
        if not f[-5:] == '.root': continue
        # if era != "all" and era not in f[:-5]: continue
        if verbose: print(' >> Adding file: ', f)
        files.append(f)
    if FullPaths: files = [path + x for x in files]
    if len(files) == 0: print('[ERROR]: No root files found in: ' + path)
    return files


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

    # files = []
    # for counter, line in enumerate(inputLFNList):
    #     counter += 1
    #     if not argms.fileLimit == -1:
    #         if counter > argms.fileLimit: break
    #     files.append(redirector + str(line).replace('\n', ''))

    keyWord = argms.inputLFN
    runPeriod = keyWord[-3:]
    if not keyWord.find("HTMHT") == -1: dirPath = "../HTMHT/"
    elif not keyWord.find("SMu") == -1: dirPath = "../SingleMuon/"
    elif not keyWord.find("SEl") == -1: dirPath = "../SingleElectron/"
    elif not keyWord.find("tt_semilep102") == -1: dirPath = "../TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_102X/"
    elif not keyWord.find("tttt102") == -1: dirPath = "../TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_102X/"
    else: return 0
    files = findEraRootFiles(dirPath + runPeriod)

    p99 = PostProcessor(".",
                        files,
                        # files[0],
                        cut="nJet > 5 && ( nMuon >0 || nElectron >0 )",
                        modules=[TriggerStudy(writeHistFile=writeFile,
                                              eventLimit=argms.eventLimit,
                                              trigLst=trigList,
                                              era=era2017)],
                        # jsonInput=None,
                        noOut=True,
                        # haddFileName="TestBranch.root",
                        # justcount=False,
                        # postfix=thePostFix,
                        histFileName=outputFile,
                        histDirName="plots",
                        branchsel="../myInFiles/kd_branchsel.txt",
                        outputbranchsel="../myInFiles/kd_branchsel.txt",
                        )
    t0 = time.time()
    p99.run()
    t1 = time.time()
    print("Elapsed time %7.1fs" % (t1-t0))


main(process_arguments())
