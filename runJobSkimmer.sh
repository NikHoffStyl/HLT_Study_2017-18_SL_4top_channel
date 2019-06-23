#!/usr/bin/env bash

pwd=$PWD
source $VO_CMS_SW_DIR/cmsset_default.sh                          # make scram available
cd /user/$USER/CMSSW_9_4_10/src/                                # your local CMSSW release use for RunII2017
#cd /user/$USER/CMSSW_10_2_6/src/                                 # your local CMSSW release use for RunII2018
eval `scram runtime -sh`                                         # don't use cmsenv, won't work on batch
# cd $pwd

#  make proxy with long validity voms-proxy-init --voms MYEXPERIMENT --valid 192:0
#  copy proxy to user directory cp $X509_USER_PROXY /user/$USER/
export X509_USER_PROXY=/user/$USER/x509up_u23075 # $(#id -u $USER)

# cd /user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork
cd $TMPDIR
export SKIMJOBDIR=/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork

python $SKIMJOBDIR/runSkimmerv2.py -fnp $FILE_TO_RUN_ON -r xrdEU_Asia
#python runAnaTrigsMuJets.py -o _HTcut -f tt_semilep102_17B
#python runSkimmer.py -f tt_semilep102_17C
#python runSkimmer.py -f tt_semilep102_17DEF
#python runSkimmer.py -f tt_semilep102_17DEF

#python runSkimmer.py -f tttt102_17B
#python runSkimmer.py -f tttt102_17C
#python runSkimmer.py -f tttt102_17DEF

#python runSkimmer.py -f dataHTMHT17B
#python runSkimmer.py -f dataHTMHT17C
#python runSkimmer.py -f dataHTMHT17D
#python runSkimmer.py -f dataHTMHT17E
#python runSkimmer.py -f dataHTMHT17F
#
#python runSkimmer.py -f dataSMu17B
#python runSkimmer.py -f dataSMu17C
#python runSkimmer.py -f dataSMu17D
#python runSkimmer.py -f dataSMu17E
#python runSkimmer.py -f dataSMu17F
#
#python runSkimmer.py -f dataSEl17B
#python runSkimmer.py -f dataSEl17C
#python runSkimmer.py -f dataSEl17D
#python runSkimmer.py -f dataSEl17E
#python runSkimmer.py -f dataSEl17F

#python $SKIMJOBDIR/runSkimmer.py -f tt_semilep102_18
#gfal-copy -r file://$TMPDIR/OutDirectory srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Trimmed2018Data/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_102X_18/
#python $SKIMJOBDIR/runSkimmer.py -f tttt102_18
#gfal-copy -r file://$TMPDIR/OutDirectory srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Trimmed2018Data/TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_102X_18/

#python $SKIMJOBDIR/runSkimmer.py -f dataHTMHT18B
#gfal-copy -r file://$TMPDIR/OutDirectory srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Trimmed2018Data/JetHT_Run2018B-Nano14Dec2018-v1/
#python $SKIMJOBDIR/runSkimmer.py -f dataHTMHT18C
#gfal-copy -r file://$TMPDIR/OutDirectory srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Trimmed2018Data/JetHT_Run2018C-Nano14Dec2018-v1/
#python $SKIMJOBDIR/runSkimmer.py -f dataHTMHT18D
#gfal-copy -r file://$TMPDIR/OutDirectory srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Trimmed2018Data/JetHT_Run2018D-Nano14Dec2018_ver2-v1/
#python $SKIMJOBDIR/runSkimmer.py -f dataHTMHT18A
#gfal-copy -r file://$TMPDIR/OutDirectory srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Trimmed2018Data/JetHT_Run2018A-Nano14Dec2018-v1/
#
#python $SKIMJOBDIR/runSkimmer.py -f dataSMu18B
#gfal-copy -r file://$TMPDIR/OutDirectory srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Trimmed2018Data/SingleMuon_Run2018B-Nano14Dec2018-v1/
#python $SKIMJOBDIR/runSkimmer.py -f dataSMu18C
#gfal-copy -r file://$TMPDIR/OutDirectory srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Trimmed2018Data/SingleMuon_Run2018C-Nano14Dec2018-v1/
#python $SKIMJOBDIR/runSkimmer.py -f dataSMu18D
#gfal-copy -r file://$TMPDIR/OutDirectory srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Trimmed2018Data/SingleMuon_Run2018D-Nano14Dec2018_ver2-v1/
#python $SKIMJOBDIR/runSkimmer.py -f dataSMu18A
#gfal-copy -r file://$TMPDIR/OutDirectory srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Trimmed2018Data/SingleMuon_Run2018A-Nano14Dec2018-v1/
#
#python $SKIMJOBDIR/runSkimmer.py -f dataSEl18B
#gfal-copy -r file://$TMPDIR/OutDirectory srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Trimmed2018Data/EGamma_Run2018B-Nano14Dec2018-v1/
#python $SKIMJOBDIR/runSkimmer.py -f dataSEl18C
#gfal-copy -r file://$TMPDIR/OutDirectory srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Trimmed2018Data/EGamma_Run2018C-Nano14Dec2018-v1/
#python $SKIMJOBDIR/runSkimmer.py -f dataSEl18D
#gfal-copy -r file://$TMPDIR/OutDirectory srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Trimmed2018Data/EGamma_Run2018D-Nano14Dec2018_ver2-v1/
#python $SKIMJOBDIR/runSkimmer.py -f dataSEl18A
#gfal-copy -r file://$TMPDIR/OutDirectory srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Trimmed2018Data/EGamma_Run2018A-Nano14Dec2018-v1/ 
