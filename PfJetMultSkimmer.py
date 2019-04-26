# -*- coding: utf-8 -*-
"""
Created on Jan 2019

@author: NikHoffStyl
"""
from __future__ import (division, print_function)
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


class PfJetsSkimmer(Module):
    """This class is to be used by the postprocessor to skimm a file down
    using the requirement of number of jets and a single lepton."""

    def __init__(self, writeHistFile=True):
        """ Initialise global variables
        Args:
            writeHistFile (bool): True to write file, False otherwise
        """

        self.writeHistFile = writeHistFile

    def beginJob(self, histFile=None, histDirName=None):
        """begin job"""
        Module.beginJob(self, histFile, histDirName)

    def endJob(self):
        """end Job"""
        Module.endJob(self)

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        """add branches to file"""
        self.out = wrappedOutputTree

        self.out.branch("Jet2_" + "HT", "F")

        pass

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        """end file"""
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        jets = Collection(event, "Jet")
        jetHt = 0
        for nj, jet in enumerate(jets):
            jetHt += jet.pt
        self.out.fillBranch("Jet2_HT", jetHt)

        return True

