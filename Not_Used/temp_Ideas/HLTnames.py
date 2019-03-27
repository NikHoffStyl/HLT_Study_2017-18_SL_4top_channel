import uproot

tree = uproot.open('root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAOD/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/70000/C6AABB0E-33AC-E811-8B63-0CC47A7C3404.root')
# if tree['Events'].keys().find("PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2") != -1:
print(tree['Events'].keys().find("PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2"))

# tree = uproot.open('root://cms-xrd-global.cern.ch//store/data/Run2017C/HTMHT/NANOAOD/Nano14Dec2018-v1/80000/A6A7DF24-1C78-FB4D-930D-4165EECC45A3.root')
# print(tree['Events'].keys())
#
# tree = uproot.open('root://cms-xrd-global.cern.ch//store/data/Run2017C/HTMHT/NANOAOD/Nano14Dec2018-v1/80000/A62E19E6-841B-1E48-BB46-338F8DB37FE2.root')
# print(tree['Events'].keys())
#
# tree = uproot.open('root://cms-xrd-global.cern.ch//store/data/Run2017C/HTMHT/NANOAOD/Nano14Dec2018-v1/80000/A62E19E6-841B-1E48-BB46-338F8DB37FE2.root')
# print(tree['Events'].keys())
#
# tree = uproot.open('root://cms-xrd-global.cern.ch//store/data/Run2017C/HTMHT/NANOAOD/Nano14Dec2018-v1/80000/97DA481E-BB89-CA4A-AA94-90878473D991.root')
# print(tree['Events'].keys())
#
# tree = uproot.open('root://cms-xrd-global.cern.ch//store/data/Run2017C/HTMHT/NANOAOD/Nano14Dec2018-v1/80000/29CE5E03-A67E-8040-9377-1070B0BB503C.root')
# print(tree['Events'].keys())
#
# tree = uproot.open('root://cms-xrd-global.cern.ch//store/data/Run2017C/HTMHT/NANOAOD/Nano14Dec2018-v1/80000/1BA6BB8B-DD88-4344-8725-5BB7F8E94ABE.root')
# print(tree['Events'].keys())
#
# tree = uproot.open('root://cms-xrd-global.cern.ch//store/data/Run2017C/HTMHT/NANOAOD/Nano14Dec2018-v1/80000/FDE7F720-98DB-B944-887C-A6BE211E45DD.root')
# print(tree['Events'].keys())