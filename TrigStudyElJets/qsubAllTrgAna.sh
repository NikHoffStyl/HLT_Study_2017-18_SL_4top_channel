#!/usr/bin/env bash

outputDIR=OutFiles/Histograms_LooseMuInfo_vetoing/
mkdir -p ${outputDIR}

era=17B
logDESCRIPTOR=ttsemi${era}_v
inputFILE=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_102X/
outputFILE=${outputDIR}TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_102X
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh
echo "Submitted >>> qsub -N SEl18D -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh"

era=17C
logDESCRIPTOR=ttsemi${era}_v
inputFILE=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_102X/
outputFILE=${outputDIR}TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_102X
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh
echo "Submitted >>> qsub -N SEl18D -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh"

era=17DEF
logDESCRIPTOR=ttsemi${era}_v
inputFILE=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_102X/
outputFILE=${outputDIR}TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_102X
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh
echo "Submitted >>> qsub -N SEl18D -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh"

era=17B
logDESCRIPTOR=ht${era}_v
inputFILE=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/HTMHT_Run2017B-Nano14Dec2018-v1/
outputFILE=${outputDIR}HTMHT_Run2017B-Nano14Dec2018-v1
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh
echo "Submitted >>> qsub -N SEl18D -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh"

era=17C
logDESCRIPTOR=ht${era}_v
inputFILE=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/HTMHT_Run2017C-Nano14Dec2018-v1/
outputFILE=${outputDIR}HTMHT_Run2017C-Nano14Dec2018-v1
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh
echo "Submitted >>> qsub -N SEl18D -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh"

era=17DEF
logDESCRIPTOR=ht${era}_v
inputFILE=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/HTMHT_Run2017D-Nano14Dec2018-v1/
outputFILE=${outputDIR}HTMHT_Run2017D-Nano14Dec2018-v1
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh
echo "Submitted >>> qsub -N SEl18D -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh"

era=17DEF
logDESCRIPTOR=ht${era}_v
inputFILE=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/HTMHT_Run2017E-Nano14Dec2018-v1/
outputFILE=${outputDIR}HTMHT_Run2017E-Nano14Dec2018-v1
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh
echo "Submitted >>> qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh"

era=17DEF
logDESCRIPTOR=ht${era}_v
inputFILE=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/HTMHT_Run2017F-Nano14Dec2018-v1/
outputFILE=${outputDIR}HTMHT_Run2017F-Nano14Dec2018-v1
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh
echo "Submitted >>> qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh"

era=17B
logDESCRIPTOR=smu${era}_v
inputFILE=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/SingleMuon_Run2017B-Nano14Dec2018-v1/
outputFILE=${outputDIR}SingleMuon_Run2017B-Nano14Dec2018-v1
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh
echo "Submitted >>> qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh"

era=17C
logDESCRIPTOR=smu${era}_v
inputFILE=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/SingleMuon_Run2017C-Nano14Dec2018-v1/
outputFILE=${outputDIR}SingleMuon_Run2017C-Nano14Dec2018-v1
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh
echo "Submitted >>> qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh"

era=17DEF
logDESCRIPTOR=smu${era}_v
inputFILE=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/SingleMuon_Run2017D-Nano14Dec2018-v1/
outputFILE=${outputDIR}SingleMuon_Run2017D-Nano14Dec2018-v1
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh
echo "Submitted >>> qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh"

era=17DEF
logDESCRIPTOR=smu${era}_v
inputFILE=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/SingleMuon_Run2017E-Nano14Dec2018-v1/
outputFILE=${outputDIR}SingleMuon_Run2017E-Nano14Dec2018-v1
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh
echo "Submitted >>> qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh"

era=17DEF
logDESCRIPTOR=smu${era}_v
inputFILE=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/SingleMuon_Run2017F-Nano14Dec2018-v1/
outputFILE=${outputDIR}SingleMuon_Run2017F-Nano14Dec2018-v1
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh
echo "Submitted >>> qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh"

era=17B
logDESCRIPTOR=sel${era}_v
inputFILE=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/SingleElectron_Run2017B-Nano14Dec2018-v1/
outputFILE=${outputDIR}SingleElectron_Run2017B-Nano14Dec2018-v1
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh
echo "Submitted >>> qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh"

era=17C
logDESCRIPTOR=sel${era}_v
inputFILE=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/SingleElectron_Run2017C-Nano14Dec2018-v1/
outputFILE=${outputDIR}SingleElectron_Run2017C-Nano14Dec2018-v1
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh
echo "Submitted >>> qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh"

era=17DEF
logDESCRIPTOR=sel${era}_v
inputFILE=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/SingleElectron_Run2017D-Nano14Dec2018-v1/
outputFILE=${outputDIR}SingleElectron_Run2017D-Nano14Dec2018-v1
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh
echo "Submitted >>> qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh"

era=17DEF
logDESCRIPTOR=sel${era}_v
inputFILE=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/SingleElectron_Run2017E-Nano14Dec2018-v1/
outputFILE=${outputDIR}SingleElectron_Run2017E-Nano14Dec2018-v1
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh
echo "Submitted >>> qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh"

era=17DEF
logDESCRIPTOR=sel${era}_v
inputFILE=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/SingleElectron_Run2017F-Nano14Dec2018-v1/
outputFILE=${outputDIR}SingleElectron_Run2017F-Nano14Dec2018-v1
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh
echo "Submitted >>> qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh"

