#!/usr/bin/env bash

pwd=$PWD
source $VO_CMS_SW_DIR/cmsset_default.sh                          # make scram available
# cd /user/$USER/CMSSW_9_4_10/src/                                 # your local CMSSW release
cd /user/$USER/CMSSW_10_2_6/src/                                 # your local CMSSW release
eval `scram runtime -sh`                                         # don't use cmsenv, won't work on batch
cd $pwd

#  make proxy with long validity voms-proxy-init --voms MYEXPERIMENT --valid 192:0
#  copy proxy to user directory cp $X509_USER_PROXY /user/$USER/
export X509_USER_PROXY=/user/$USER/x509up_u23075 # $(#id -u $USER)

cd $TMPDIR
export SKIMJOBDIR=/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/TrigStudyMuJets

echo "inputFile:" ${FILE_IN}
echo "outputDIR:" ${FILE_OUT}
echo "fileERA:" ${ERA}
outputFILE=${FILE_OUT}${ERA}.root 
#mkdir -p $outputFILE

python ${SKIMJOBDIR}/trgAnalyser_2D_Hists.py -fnp ${FILE_IN} -o ${FILE_OUT} -era ${ERA} -csv_  ${CSV_FILE}