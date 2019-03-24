#!/usr/bin/env bash

pwd=$PWD
source $VO_CMS_SW_DIR/cmsset_default.sh                          # make scram available
cd /user/$USER/CMSSW_9_4_10/src/                                 # your local CMSSW release
eval `scram runtime -sh`                                         # don't use cmsenv, won't work on batch
cd $pwd

#  make proxy with long validity voms-proxy-init --voms MYEXPERIMENT --valid 192:0
#  copy proxy to user directory cp $X509_USER_PROXY /user/$USER/
export X509_USER_PROXY=/user/$USER/x509up_u23075 # $(#id -u $USER)

cd /user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/TrigStudyLepJets
#python runAnaTrigsLepJets.py -f dataHTMHT17B
#python runAnaTrigsLepJets.py -f dataHTMHT17C
#python runAnaTrigsLepJets.py -f dataHTMHT17D
#python runAnaTrigsLepJets.py -f dataHTMHT17E
python runAnaTrigsLepJets.py -f dataHTMHT17F
#
#python runAnaTrigsLepJets.py -f dataSMu17B
#python runAnaTrigsLepJets.py -f dataSMu17C
#python runAnaTrigsLepJets.py -f dataSMu17D
#python runAnaTrigsLepJets.py -f dataSMu17E
#python runAnaTrigsLepJets.py -f dataSMu17F
#
#python runAnaTrigsLepJets.py -f dataSEl17B
#python runAnaTrigsLepJets.py -f dataSEl17C
#python runAnaTrigsLepJets.py -f dataSEl17D
#python runAnaTrigsLepJets.py -f dataSEl17E
#python runAnaTrigsLepJets.py -f dataSEl17F