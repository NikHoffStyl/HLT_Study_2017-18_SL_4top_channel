import ROOT
import os


path = "/pnfs/iihe/cms/store/user/nistylia/Trimmed2018Data/EGamma_Run2018A-Nano14Dec2018-v1/BaseSelectionv2_18/"
for f in os.listdir(path):
    if not f[-5:] == '.root': continue
    fileN = ROOT.TFile.Open(path + f)
    n = fileN.Events.GetEntries()
    if n == 0: print(f)
    print("1")

    fileN.Close()
    print("2")
