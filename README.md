# [Nikos - Four Top Production Repository](https://github.com/NikHoffStyl/RemoteWork)
Repository for Working in the Single Lepton tttt decay channel. 



## Combining High-Level-Trigger (HLT) :high_brightness:
This study is done using non-prescaled HLT triggers, which can be checked by searching the HLT menu at the [CMS-HLT 
configuration explorer](https://cmsweb.cern.ch/confdb/). The HLT Menu name/path can be found at:
* https://twiki.cern.ch/twiki/bin/view/CMS/TopTriggerYear2017 for 2017 and
* https://twiki.cern.ch/twiki/bin/view/CMS/TopTriggerYear2018 for 2018.

Currently the triggers which are being studied, in the hopes that a better event acceptance efficiency can be achieved, 
are:
* IsoMu24  ,
* PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2  and
* Mu15_IsoVVVL_PFHT450_CaloBTagCSV_4p5  ,

where if a combination is successful it will be called: IsoMu24_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2 .

### Event Acceptance Criteria for at least 6 Jets:
* Must satisfy what is called a JetID > 2 (https://twiki.cern.ch/twiki/bin/view/CMS/JetID13TeVRun2017),
* Momentum pT of at least 30 GeV
* Absolute value of pseudo-rapidity (eta) less than 2.4  
* At least one of these Jets that pass the above criteria are from b-quarks, checked by b-tagging algorithms, at the
moment it required that the value given by the DeepFlavourB algorithm is larger than 0.7489 
(https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation94X), which is recognised as a tight test.


### Event Acceptance Criteria for exactly one Muon:
* Absolute value of pseudo-rapidity (eta) less than 2.4 
* Relatively well isolated, in other words not very close to other particles that may inhibit the its 
correct identification or the measure of its properties. This is done using an algorithm that tests the total particle 
flow relative isolation, the particular one used is called miniPFRelIso_all and should give a value less than 0.15.
* Correctly identified, in other words not mistakenly identified another particle as a muon; this is done using special
algorithms. In this study, one such algorithm was used, which only accepts particles identified as muons with high
certainty (known as tightId).



### Instructions for Repeating Study:
 To produce a text file of [triggers](https://twiki.cern.ch/twiki/bin/view/CMS/TriggerStudies)
( and other unwanted stuff, which will be removed) do:
```
    $ HLTnames.py | tee LeafNames.txt
```
    
or 
```
    $ HLTnames.py > LeafNames.txt
```

To produce histograms run:
```
    $ python3 nsMain.py
```
which imports histoMaker and adds HistogramMaker() as an argument to the postProcessor. 
The choice of triggers is given here, along with the preselection criteria.

The help message given for [`histoMain.py`](histoMain.py) is:
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

To produce [`histoDraw.py`](histoDraw.py) plots run:
```
    $ python3 triggerPathEfficiency.py
```

The help nessage given for [`triggerPathEfficiency.py`](triggerPathEfficiency.py) is:
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
