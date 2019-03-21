
![cms_higgsto4muons](https://user-images.githubusercontent.com/32751356/51404641-f1847e00-1b4b-11e9-88d4-eb94f7c02036.png)
# [Nikos - Four Top Production Repository](https://github.com/NikHoffStyl/RemoteWork)
Repository for Working in the Single Lepton tttt decay channel. 



## The Standard Model

The Standard Model of fundamental particle physics is our current best attempt at model that broadens the field of 
knowledge of what our Universe consists of on the smallest scale. At first sight it seems to be a very successful and 
thoroughly tested model, as it describes the existence, properties and possible interactions of most of the observed 
fundamental particles of our visible Universe. However, it must be incomplete as it fails to explain all of the observed
phenomena in astrophysics, cosmology and particle physics. The main indications being:

* Baryon asymmetry of the Universe: Why is there an abundance of matter over antimatter?
* Neutrino masses and oscillations: Why do they have mass? What makes neutrinos change from
one form to another?
* Dark Matter: What can account for the rotational speeds of galaxies and stellar objects and a few other observations 
in astrophysics? What is the matter content of the Universe?
* Inflation of the Universe: What causes the acceleration of its expansion in the early stages of the evolution of the 
Universe?
* Dark Energy: What form of energy is required to explain inflation of the Universe at its present stage of evolution?
* Gravity: What causes the most familiar force of everyday life?
In addition to these, there are some aspects which remain far from desirable; these are: the Higgs mass tuning,
not predicting a unification of all forces, not predicting the masses or couplings of all the particles and some strong 
CP problems. More particles and interactions would be required to explain these enigmas, hence some unknown
particles are assumed to have not yet been observed.

## Combining High-Level-Trigger (HLT) :high_brightness:
### Datasets
Monte Carlo Datasets Studied in CMSSW_9_4_X, chosen according to the  [Particle Performance Dataset (PPD) RunII Analysis
Guideline](https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVAnalysisSummaryTable) :
* Four Top Decay: 
    * Primary Dataset: /store/mc/RunIIFall17NanoAOD/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/
    * NANOAODSIM/
    * Campaign: RunIIFall17NanoAOD/
    * Process String: PU2017_12Apr2018_94X_mc2017_realistic_v14-v1
        * Processing Version: v1
* TTBar Decay: 
    * /store/mc/RunIIFall17NanoAOD/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/
    PU2017_12Apr2018_94X_mc2017_realistic_v14-v1

### HLTriggers
This study is done using non-prescaled HLT triggers, which can be checked by searching the HLT menu at the [CMS-HLT 
configuration explorer](https://cmsweb.cern.ch/confdb/). The HLT Menu names/paths for 2017-18 can be found at:
* [TopTrigger2018](https://twiki.cern.ch/twiki/bin/view/CMS/TopTriggerYear2017) (last updated 2018-09-27) and
* [TopTrigger2017](https://twiki.cern.ch/twiki/bin/view/CMS/TopTriggerYear2018) (last updated 2018-09-12) .

Currently the triggers which are being studied, in the hopes that a better event acceptance efficiency can be achieved, 
are:
* IsoMu24  ,
* PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2  and
* Mu15_IsoVVVL_PFHT450_CaloBTagCSV_4p5  ,

where if a combination is successful it will be called: IsoMu24_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2 .

 
### Jet Acceptance Criteria

Jets are counted if the following criteria are satisfied:
* Must satisfy what is called a JetID > 2 (https://twiki.cern.ch/twiki/bin/view/CMS/JetID13TeVRun2017),
* Momentum pT of at least 30 GeV
* Absolute value of pseudo-rapidity (eta) less than 2.4  
* Implement jet cleaning (”cleanmask”) , with priority given to leptons

If Jet passes above criteria it is counted as a b-tagged jet if:
* At least one of these Jets that pass the above criteria are from b-quarks, checked by b-tagging algorithms, at the
moment it required that the value given by the DeepFlavourB algorithm is larger than 0.7489 
(https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation94X), which is recognised as a tight test.

### Muon Acceptance Criteria

Muons are counted if the following criteria are satisfied:
* Absolute value of pseudo-rapidity (eta) less than 2.4 
* Relatively well isolated, in other words not very close to other particles that may inhibit the its 
correct identification or the measure of its properties. This is done using an algorithm that tests the total particle 
flow relative isolation, the particular one used is called miniPFRelIso_all and should give a value less than 0.15.
* Correctly identified, in other words not mistakenly identified another particle as a muon; this is done using special
algorithms. In this study, one such algorithm was used, which only accepts particles identified as muons with high
certainty [(known as tightId)](https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMuonIdRun2).
 
### Electron Acceptance Criteria 

Electrons are counted if the following criteria are satisfied:
* Absolute value of pseudo-rapidity (eta) less than 2.4, but with a vetoed section from 1.4442 to 1.566;
* i.e. Electrons are counted if in the regions : |eta|<1.4442 and 1.566<|eta|<2.4

### Denominator of “Trigger Efficiencies” 

Accepted Events:
* Six or more jets pass the jet criteria,
* Two of which are b-tagged,
* One muon passes the muon criteria and 
* Zero electrons pass the electron criteria

### Numerator of “Trigger Efficiencies”
Accepted Events:

+ If the Denominator criteria are satisfied and 
+ the given Trigger studied is “True”.

Un-Prescaled Triggers studied for μ + jets:

* 'IsoMu24’
* 'PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2’
* Combined Version: ' 'IsoMu24 _PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2’ 
* ‘Mu15_IsoVVVL_PFHT450_CaloBTagCSV_4p5’

### Instructions for Repeating Study 
 
 To produce a text file of [triggers](https://twiki.cern.ch/twiki/bin/view/CMS/TriggerStudies)
( and other unwanted stuff, which will be removed) do:

```
    $ HLTnames.py | tee LeafNames.txt
```


or 
```
    $ HLTnames.py > LeafNames.txt
```
This Repository is still being worked on so this documentation will be updated when I have 
finished fixing major problems etc...
N.B. If you come across this repo by accident, do not believe what you read here as its probably outdated. 
