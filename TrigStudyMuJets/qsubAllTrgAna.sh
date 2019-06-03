#!/usr/bin/env bash

era=17B
logDESCRIPTOR=ht${era}
inputFILE=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/HTMHT_Run2017B-Nano14Dec2018-v1/
outputFILE=OutFiles/Histograms_LooseMuInfo/HTMHT_Run2017B-Nano14Dec2018-v1
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh
echo "Submitted >>> qsub -N SEl18D -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh"

era=17C
logDESCRIPTOR=ht${era}
inputFILE=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/HTMHT_Run2017C-Nano14Dec2018-v1/
outputFILE=OutFiles/Histograms_LooseMuInfo/HTMHT_Run2017C-Nano14Dec2018-v1
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh
echo "Submitted >>> qsub -N SEl18D -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh"

era=17DEF
logDESCRIPTOR=ht${era}
inputFILE=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/HTMHT_Run2017D-Nano14Dec2018-v1/
outputFILE=OutFiles/Histograms_LooseMuInfo/HTMHT_Run2017D-Nano14Dec2018-v1
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh
echo "Submitted >>> qsub -N SEl18D -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh"

era=17DEF
logDESCRIPTOR=ht${era}
inputFILE=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/HTMHT_Run2017E-Nano14Dec2018-v1/
outputFILE=OutFiles/Histograms_LooseMuInfo/HTMHT_Run2017E-Nano14Dec2018-v1
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh
echo "Submitted >>> qsub -N SEl18D -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh"

era=17F
logDESCRIPTOR=ht${era}
inputFILE=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/HTMHT_Run2017F-Nano14Dec2018-v1/
outputFILE=OutFiles/Histograms_LooseMuInfo/HTMHT_Run2017F-Nano14Dec2018-v1
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh
echo "Submitted >>> qsub -N SEl18D -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh"

era=17B
logDESCRIPTOR=smu${era}
inputFILE=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/SingleMuon_Run2017B-Nano14Dec2018-v1/
outputFILE=OutFiles/Histograms_LooseMuInfo/SingleMuon_Run2017B-Nano14Dec2018-v1
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh
echo "Submitted >>> qsub -N SEl18D -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh"

era=17C
logDESCRIPTOR=smu${era}
inputFILE=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/SingleMuon_Run2017C-Nano14Dec2018-v1/
outputFILE=OutFiles/Histograms_LooseMuInfo/SingleMuon_Run2017C-Nano14Dec2018-v1
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh
echo "Submitted >>> qsub -N SEl18D -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh"

era=17DEF
logDESCRIPTOR=smu${era}
inputFILE=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/SingleMuon_Run2017D-Nano14Dec2018-v1/
outputFILE=OutFiles/Histograms_LooseMuInfo/SingleMuon_Run2017D-Nano14Dec2018-v1
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh
echo "Submitted >>> qsub -N SEl18D -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh"

era=17DEF
logDESCRIPTOR=smu${era}
inputFILE=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/SingleMuon_Run2017E-Nano14Dec2018-v1/
outputFILE=OutFiles/Histograms_LooseMuInfo/SingleMuon_Run2017E-Nano14Dec2018-v1
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh
echo "Submitted >>> qsub -N SEl18D -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh"

era=17DEF
logDESCRIPTOR=smu${era}
inputFILE=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/SingleMuon_Run2017F-Nano14Dec2018-v1/
outputFILE=OutFiles/Histograms_LooseMuInfo/SingleMuon_Run2017F-Nano14Dec2018-v1
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh
echo "Submitted >>> qsub -N SEl18D -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh"

era=17B
logDESCRIPTOR=sel${era}
inputFILE=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/SingleElectron_Run2017B-Nano14Dec2018-v1/
outputFILE=OutFiles/Histograms_LooseMuInfo/SingleElectron_Run2017B-Nano14Dec2018-v1
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh
echo "Submitted >>> qsub -N SEl18D -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh"

era=17C
logDESCRIPTOR=sel${era}
inputFILE=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/SingleElectron_Run2017C-Nano14Dec2018-v1/
outputFILE=OutFiles/Histograms_LooseMuInfo/SingleElectron_Run2017C-Nano14Dec2018-v1
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh
echo "Submitted >>> qsub -N SEl18D -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh"

era=17DEF
logDESCRIPTOR=sel${era}
inputFILE=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/SingleElectron_Run2017D-Nano14Dec2018-v1/
outputFILE=OutFiles/Histograms_LooseMuInfo/SingleElectron_Run2017D-Nano14Dec2018-v1
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh
echo "Submitted >>> qsub -N SEl18D -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh"

era=17DEF
logDESCRIPTOR=sel${era}
inputFILE=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/SingleElectron_Run2017E-Nano14Dec2018-v1/
outputFILE=OutFiles/Histograms_LooseMuInfo/SingleElectron_Run2017E-Nano14Dec2018-v1
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh
echo "Submitted >>> qsub -N SEl18D -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh"

era=17DEF
logDESCRIPTOR=sel${era}
inputFILE=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/SingleElectron_Run2017F-Nano14Dec2018-v1/
outputFILE=OutFiles/Histograms_LooseMuInfo/SingleElectron_Run2017F-Nano14Dec2018-v1
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh
echo "Submitted >>> qsub -N SEl18D -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh"

