#!/usr/bin/env bash

# PYTHONPATH=$PYTHONPATH:/user/nistylia/CMSSW_9_4_10/src/PhysicsTools/NanoAODTools/build/lib/python
# export PYTHONPATH 

pwd=$PWD
source $VO_CMS_SW_DIR/cmsset_default.sh                          # make scram available                              
cd /user/$USER/CMSSW_9_4_10/src/                                 # your local CMSSW release
eval `scram runtime -sh`                                         # don't use cmsenv, won't work on batch                             
cd $pwd


#  make proxy with long validity voms-proxy-init --voms MYEXPERIMENT --valid 192:0
#  copy proxy to user directory cp $X509_USER_PROXY /user/$USER/
export X509_USER_PROXY=/user/$USER/x509up_u23075 # $(#id -u $USER)

echo "this is a test"
cd /user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/TrigStudyMuJets
python /user/$USER/CMSSW_9_4_10/src/TopBrussels/RemoteWork/TrigStudyMuJets/runAnaTrigsMuJets.py -f tttt102 -lf 2 -e 1000

# gfal-copy file://$TMPDIR/../OutFiles/Histograms/TT102X_6Jets1Mu20jPt.root srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/CMSSW_9_4_10/src/TopBrussels/RemoteWork/OutFiles/Histograms/TT102X_6Jets1Mu20jPt.root