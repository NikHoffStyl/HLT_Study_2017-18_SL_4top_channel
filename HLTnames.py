import uproot
tree = uproot.open('root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAOD/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/70000/C6AABB0E-33AC-E811-8B63-0CC47A7C3404.root')
print(tree['Events'].keys())
