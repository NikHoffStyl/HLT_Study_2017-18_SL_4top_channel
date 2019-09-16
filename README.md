
# [Nikos - Four Top Production Repository](https://github.com/NikHoffStyl/RemoteWork)
Repository for New High-Level-Trigger combinations for a 2017 four-top production analysis with single-lepton final state. 


## Introduction

The study described is:
* a HLT study,
* carried out using the new smaller data sample files format, called NanoAOD.
* performed on the four top and top anti-top MC data-sets and
* HTMHT, Single-Muon and SingleElectron primary data-sets of Run II 2017 collected by CMS and 
* JetHt, SingleMuon and EGamma primary data-sets of Run II 2018 collected by CMS

### Motivation
In a previous search for four tops in the final state with one lepton plus  jets  at  13  TeV  using  2016  data,  there
was  reduced  sensitivity  caused  by  the  use  of  a  single  muon  HLT,  specifically the HLT_Iso(Tk)Mu24. 
Therefore, a study on HLTs for 2017 data  was  performed,  to  assess  how  to  improve  sensitivity  to the four top process.

Four tops production process has a cross section of $9.2\ fb^{-1}$, thus it is very rare and any possible improvements on the acceptance of four top events in the final selection should be studied.

In a previous search for four-tops in the final state with one lepton plus jets at 13 TeV using 2016 data, many four top events were being lost at low lepton $p_{T}$, caused by the use of a single muon HLT, specifically the HLT\_Iso(Tk)Mu24. 

Therefore, a study on s for 2017-18 data was performed, to assess how to improve sensitivity to the four-top production process. Initial guess: by includding events from a hadronic trigger , these lost events will be taken back by the hadronic trigger.HLT

## Data and MC Samples
The  latest  AOD  format  files,  the  NanoAOD,  were  used  for this  study. The  run  period  looked  at  was  2017  RunII,
where the  MonteCarlo  (MC)  samples  used  were  the  four  top  and top  anti-top  with  a  single  lepton  plus  jets
final  states;  and where the primary data samples used were the HTMHT, the SingleMuon and the SingleElectron. 

The MC used for four top, found in `myInFiles/mc/`
* /TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8/
and for backgrounds:
* /TTToSemiLeptonic\_TuneCP5\_13TeV-powheg-pythia8/
* /TTJets\_DiLept\_TuneCP5\_13TeV-madgraphMLM-pythia8/
* /TTToHadronic\_TuneCP5\_13TeV-powheg-pythia8/
* /TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/
* plus some more for QCD and EW background
where  the 94X versions of these files were also looked at initially, but had some outputs results from new algorithms missing.

The summary of the datasets from SingleMuon,
SingleElectron and HTMHT streams is given below:

| Datasets | Run Ranges | Integrated Luminosity /fb |
|---------|-----------|----------------|
|Run2017B-Nano14Dec2018-v1|297020-299368| 4.823 |
|Run2017C-Nano14Dec2018-v1|299368-302029| 9.664 |
|Run2017D-Nano14Dec2018-v1|302030-303434| 4.252 |
|Run2017E-Nano14Dec2018-v1|303569-304826| 9.278 |
|Run2017F-Nano14Dec2018-v1|305033-306154| 13.522 |
|Run2018A-Nano14Dec2018-v1| 315252-316995 | 14.00 |
|Run2018B-Nano14Dec2018-v1| 317080-319310 | 7.10 |
|Run2018C-Nano14Dec2018-v1| 319337-320065 | 6.94 |
|Run2018D-Nano14Dec2018_ver2-v1| 320673-325175 | 31.93 |

The study on all 2017 data and MC samples was done using the 9_4_10 version of the CMSSW software and the sample files
chosen according to the  [Particle Performance Dataset (PPD) RunII Analysis
Guideline](https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVAnalysisSummaryTable). Good data was chosen using the Golden-JSON files for each era, more details on these can be found [here](https://twiki.cern.ch/twiki/bin/view/CMS/PdmV2017Analysis#Data). 

## Objects and Event Selection
 Selected 6 or more good jets and only one good lepton per event (look at AN-19-091 for details).
 
## Environment SetUp
For bash users:
```
source $VO_CMS_SW_DIR/cmsset_default.sh

```
 
## Instructions for skimming and pruning NanoAOD files
You may like to use a class such as the one given in [PfJetMultSkimmer.py](`PfJetMultSkimmer.py`) as an argument to the `PostProcessor()`
module. This can be used to remove branches (Objetcs and/or Collections) and remove events for certain cuts provided to the `PostProcessor()`.

You may also like to take 



## TODO:
* Add a shell script to set up environment for users.
* 
