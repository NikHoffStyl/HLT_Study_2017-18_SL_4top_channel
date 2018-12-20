# [Nikos - Four Top Production Repository](https://github.com/NikHoffStyl/RemoteWork)
Repository for Working in the Single Lepton tttt decay channel. 

## Combining High-Level-Trigger (HLT) :high_brightness:

  * To produce a text file of [triggers](https://twiki.cern.ch/twiki/bin/view/CMS/TriggerStudies)
( and other unwanted stuff, which will be removed) do:
```bash
     $ HLTnames.py | tee LeafNames.txt
```
    
or 
```bash
     $ HLTnames.py > LeafNames.txt
```

To produce histograms run:
```bash
     $ python nsMain.py
```
which imports histoMaker and adds HistogramMaker() as an argument to the postProcessor. 
The choice of triggers is given here, along with the preselection criteria.

The help message given for [`nsMain.py`](nsMain.py) is:
```
usage: nsMain.py [-h] [-f {ttjets,tttt,tttt_weights,wjets}]
                 [-r {xrd-global,xrdUS,xrdEU_Asia,eos,iihe,local}] [-nw]
                 [-e EVENTLIMIT]

optional arguments:
  -h, --help            show this help message and exit
  -f {ttjets,tttt,tttt_weights,wjets}, --inputLFN {ttjets,tttt,tttt_weights,wjets}
                        Set list of input files (default: tttt)
  -r {xrd-global,xrdUS,xrdEU_Asia,eos,iihe,local}, --redirector {xrd-global,xrdUS,xrdEU_Asia,eos,iihe,local}
                        Sets redirector to query locations for LFN (default:
                        local)
  -nw, --noWriteFile    Does not output a ROOT file, which contains the
                        histograms. (default: False)
  -e EVENTLIMIT, --eventLimit EVENTLIMIT
                        Set a limit to the number of events. (default: -1)
```
___

To produce [trigger efficiency](triggerPathEfficiency.py) plots run:
```
$ python triggerPathEfficiency.py
```

The help nessage given for [`triggerPathEfficiency.py](triggerPathEfficiency.py)
```
usage: triggerPathEfficiency.py [-h] [-f {ttjets,tttt,tttt_weights,wjets}]

optional arguments:
  -h, --help            show this help message and exit
  -f {ttjets,tttt,tttt_weights,wjets}, --inputLFN {ttjets,tttt,tttt_weights,wjets}
                        Set list of input files (default: tttt)
```

I will try to introduce the option to input a trigger as an argument to some of these 
and if argument is not given it will revert to search for a default trigger 
and exit if trigger does not exist.
At the moment it makes more sense not to introduce command line args for triggers as 
this code is only ~~used~~ by me!

When this is done and saved :floppy_disk:, sit back relax and have many :beers:.
