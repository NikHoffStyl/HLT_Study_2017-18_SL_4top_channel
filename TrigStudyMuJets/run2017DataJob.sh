#!/usr/bin/env bash

pwd=$PWD
source $VO_CMS_SW_DIR/cmsset_default.sh                          # make scram available
cd /user/$USER/CMSSW_9_4_10/src/                                 # your local CMSSW release
eval `scram runtime -sh`                                         # don't use cmsenv, won't work on batch
cd $pwd

#  make proxy with long validity voms-proxy-init --voms MYEXPERIMENT --valid 192:0
#  copy proxy to user directory cp $X509_USER_PROXY /user/$USER/
export X509_USER_PROXY=/user/$USER/x509up_u23075 # $(#id -u $USER)

cd /user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/TrigStudyMuJets

#inputFILE=/pnfs/iihe/cms/store/user/nistylia/TrimmedSkimmed2017Data/W4JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8_102X/
#outputDIR=/user/nistylia/CMSSW_9_4_10/src/TopBrussels/RemoteWork/TrigStudyMuJets/OutFiles/WjetsGenTest/
#fileERA=17B
echo "inputFile:" ${FILE_IN}
echo "outputDIR:" ${FILE_OUT}
echo "fileERA:" ${ERA}
outputFILE=${FILE_OUT}${ERA}.root 
#mkdir -p $outputFILE

python trgAnalyser.py -fnp ${FILE_IN} -o ${outputFILE} -era ${ERA}

#python runAnaTrigsMuJets.py -o _HTcutGenInfo -f tt_semilep102_17B
#python runAnaTrigsMuJets.py -o _HTcutGenInfo -f tt_semilep102_17C
#python runAnaTrigsMuJets.py -o _GenInfoV2 -f tt_semilep102_17DEF

#python runAnaTrigsMuJets.py -o _HTcut -f tttt102_17B
#python runAnaTrigsMuJets.py -o _HTcut -f tttt102_17C
#python runAnaTrigsMuJets.py -o _HTcut -f tttt102_17DEF

#python runAnaTrigsMuJets.py -o _HTcut -f dataHTMHT17B
#python runAnaTrigsMuJets.py -o _HTcut -f dataHTMHT17C
#python runAnaTrigsMuJets.py -o _HTcut -f dataHTMHT17D
#python runAnaTrigsMuJets.py -o _HTcut -f dataHTMHT17E
#python runAnaTrigsMuJets.py -o _HTcut -f dataHTMHT17F
#
#python runAnaTrigsMuJets.py -o _HTcut -f dataSMu17B
#python runAnaTrigsMuJets.py -o _HTcut -f dataSMu17C
#python runAnaTrigsMuJets.py -o _HTcut -f dataSMu17D
#python runAnaTrigsMuJets.py -o _HTcut -f dataSMu17E
#python runAnaTrigsMuJets.py -o _HTcut -f dataSMu17F
#
#python runAnaTrigsMuJets.py -o _HTcut -f dataSEl17B
#python runAnaTrigsMuJets.py -o _HTcut -f datasel17C
#python runAnaTrigsMuJets.py -o _HTcut -f dataSEl17D
#python runAnaTrigsMuJets.py -o _HTcut -f dataSEl17E
#python runAnaTrigsMuJets.py -o _HTcut -f dataSEl17F
