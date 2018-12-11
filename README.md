# Nikos - Four Top Production Repository
Repository for Working in the Single Lepton tttt decay channel

## Combining High-Level-Trigger (HLT)

To produce a text file of [triggers](https://twiki.cern.ch/twiki/bin/view/CMS/TriggerStudies)( and other unwanted stuff, which will be removed) do:
```
$ HLTnames.py | tee LeafNames.txt
```
or
```
$ HLTnames.py > LeafNames.txt
```

To produce histograms run:
```
$ nsMain.py
```
which imports histoMaker and adds HistogramMaker() as an argument to the postProcessor. 
The choice of triggers is given here, along with the preselection criteria.

The help message given for nsMain.py is:
```
usage: nsMain.py [-h] [-f {ttjets,tttt,tttt_weights,wjets}]
                 [-r {xrd-global,xrdUS,xrdEU_Asia,eos,iihe}]

optional arguments:
  -h, --help            show this help message and exit
  -f {ttjets,tttt,tttt_weights,wjets}, --inputLFN {ttjets,tttt,tttt_weights,wjets}
                        Set list of input files (default: None)
  -r {xrd-global,xrdUS,xrdEU_Asia,eos,iihe}, --redirector {xrd-global,xrdUS,xrdEU_Asia,eos,iihe}
                        Sets redirector to query locations for LFN (default:
                        None)
```

To produce trigger efficiency plots run:
```
$ python triggerPathEfficiency.py
```

I will try to introduce the option to input a trigger as an argument to some of these 
and if argument is not given it will revert to search for a default trigger 
and exit if trigger does not exist.
At the moment it makes more sense not to introduce command line args for triggers as 
this code is only used by me!

