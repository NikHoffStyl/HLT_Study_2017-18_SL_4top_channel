#!/bin/bash                                                                                                                                                                                                      
fileOut="v3_HistFiles"
csvFile="eventIDsv2"
echo " "
counter=1
ERA_ARRAY=("17B" "17C" "17D" "17E" "17F")
ERA_ARRAY_MC=("17B" "17C" "17DEF")

for era in ${ERA_ARRAY[*]};do                                                                                                                                                                                
# SUBSTRING=$(echo $f| cut -d'/' -f 10);                                                                                                                                                                        
era2=$era
if [ $era = "17D" ] || [ $era = "17E" ] || [ $era = "17F" ];then
    era2="17DEF"
fi
prTpe=ht
echo " "
echo "qsub -q express -N ${prTpe}${era}_sfini -o logs/${prTpe}${era}_sfini.stdout -e logs/${prTpe}${era}_sfini.stderr -v FILE_IN=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/HTMHT_Run20${era}-Nano14Dec2018-v1/BaseSelectionv2_${era2}/,FILE_OUT=${fileOut}/${prTpe}${era}_sfini.root,ERA=${era2},CSV_FILE=${csvFile}${prTpe}${era}.csv run2017DataJob.sh"
qsub -q express -N ${prTpe}${era}_sfini -o logs/${prTpe}${era}_sfini.stdout -e logs/${prTpe}${era}_sfini.stderr -v FILE_IN=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/HTMHT_Run20${era}-Nano14Dec2018-v1/BaseSelectionv2_${era2}/,FILE_OUT=${fileOut}/${prTpe}${era}_sfini.root,ERA=${era2},CSV_FILE=${csvFile}${prTpe}${era}.csv run2017DataJob.sh

prTpe=smu
echo " "
echo "qsub -q express -N ${prTpe}${era}_sfini -o logs/${prTpe}${era}_sfini.stdout -e logs/${prTpe}${era}_sfini.stderr -v FILE_IN=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/SingleMuon_Run20${era}-Nano14Dec2018-v1/BaseSelectionv2_${era2}/,FILE_OUT=${fileOut}/${prTpe}${era}_sfini.root,ERA=${era2},CSV_FILE=${csvFile}${prTpe}${era}.csv run2017DataJob.sh"
qsub -q express -N ${prTpe}${era}_sfini -o logs/${prTpe}${era}_sfini.stdout -e logs/${prTpe}${era}_sfini.stderr -v FILE_IN=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/SingleMuon_Run20${era}-Nano14Dec2018-v1/BaseSelectionv2_${era2}/,FILE_OUT=${fileOut}/${prTpe}${era}_sfini.root,ERA=${era2},CSV_FILE=${csvFile}${prTpe}${era}.csv run2017DataJob.sh

prTpe=sel
echo " "
echo "qsub -q express -N ${prTpe}${era}_sfini -o logs/${prTpe}${era}_sfini.stdout -e logs/${prTpe}${era}_sfini.stderr -v FILE_IN=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/SingleElectron_Run20${era}-Nano14Dec2018-v1/BaseSelectionv2_${era2}/,FILE_OUT=${fileOut}/${prTpe}${era}_sfini.root,ERA=${era2},CSV_FILE=${csvFile}${prTpe}${era}.csv run2017DataJob.sh"
qsub -q express -N ${prTpe}${era}_sfini -o logs/${prTpe}${era}_sfini.stdout -e logs/${prTpe}${era}_sfini.stderr -v FILE_IN=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/SingleElectron_Run20${era}-Nano14Dec2018-v1/BaseSelectionv2_${era2}/,FILE_OUT=${fileOut}/${prTpe}${era}_sfini.root,ERA=${era2},CSV_FILE=${csvFile}${prTpe}${era}.csv run2017DataJob.sh

done                                                                                                                                                                                                            


for era in ${ERA_ARRAY_MC[*]};do                                                                                                                                                                                
# SUBSTRING=$(echo $f| cut -d'/' -f 10);                                                                                                                                                                        
era2=$era
prTpe=ttjets
echo " "
echo "qsub -q express -N ${prTpe}${era}_sfini -o logs/${prTpe}${era}_sfini.stdout -e logs/${prTpe}${era}_sfini.stderr -v FILE_IN=/pnfs/iihe/cms/store/user/nistylia/TrimmedSkimmed2017Data/TTJets_TuneCP5_13TeV-madgraphMLM-pythia8_102X/BaseSelectionv2_${era2}/,FILE_OUT=${fileOut}/${prTpe}${era}_sfini.root,ERA=${era2},CSV_FILE=${csvFile}${prTpe}${era}.csv run2017DataJob.sh"
qsub -q express -N ${prTpe}${era}_sfini -o logs/${prTpe}${era}_sfini.stdout -e logs/${prTpe}${era}_sfini.stderr -v FILE_IN=/pnfs/iihe/cms/store/user/nistylia/TrimmedSkimmed2017Data/TTJets_TuneCP5_13TeV-madgraphMLM-pythia8_102X/BaseSelectionv2_${era2}/,FILE_OUT=${fileOut}/${prTpe}${era}_sfini.root,ERA=${era2},CSV_FILE=${csvFile}${prTpe}${era}.csv run2017DataJob.sh

prTpe=ttdilep
echo " "
echo "qsub -q express -N ${prTpe}${era}_sfini -o logs/${prTpe}${era}_sfini.stdout -e logs/${prTpe}${era}_sfini.stderr -v FILE_IN=/pnfs/iihe/cms/store/user/nistylia/TrimmedSkimmed2017Data/TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8_102X/BaseSelectionv2_${era2}/,FILE_OUT=${fileOut}/${prTpe}${era}_sfini.root,ERA=${era2},CSV_FILE=${csvFile}${prTpe}${era}.csv run2017DataJob.sh"
qsub -q express -N ${prTpe}${era}_sfini -o logs/${prTpe}${era}_sfini.stdout -e logs/${prTpe}${era}_sfini.stderr -v FILE_IN=/pnfs/iihe/cms/store/user/nistylia/TrimmedSkimmed2017Data/TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8_102X/BaseSelectionv2_${era2}/,FILE_OUT=${fileOut}/${prTpe}${era}_sfini.root,ERA=${era2},CSV_FILE=${csvFile}${prTpe}${era}.csv run2017DataJob.sh

prTpe=tthad
echo " "
echo "qsub -q express -N ${prTpe}${era}_sfini -o logs/${prTpe}${era}_sfini.stdout -e logs/${prTpe}${era}_sfini.stderr -v FILE_IN=/pnfs/iihe/cms/store/user/nistylia/TrimmedSkimmed2017Data/TTToHadronic_TuneCP5_13TeV-powheg-pythia8_102X/BaseSelectionv2_${era2}/,FILE_OUT=${fileOut}/${prTpe}${era}_sfini.root,ERA=${era2},CSV_FILE=${csvFile}${prTpe}${era}.csv run2017DataJob.sh"
qsub -q express -N ${prTpe}${era}_sfini -o logs/${prTpe}${era}_sfini.stdout -e logs/${prTpe}${era}_sfini.stderr -v FILE_IN=/pnfs/iihe/cms/store/user/nistylia/TrimmedSkimmed2017Data/TTToHadronic_TuneCP5_13TeV-powheg-pythia8_102X/BaseSelectionv2_${era2}/,FILE_OUT=${fileOut}/${prTpe}${era}_sfini.root,ERA=${era2},CSV_FILE=${csvFile}${prTpe}${era}.csv run2017DataJob.sh

prTpe=ttsemi
echo " "
echo "qsub -q express -N ${prTpe}${era}_sfini -o logs/${prTpe}${era}_sfini.stdout -e logs/${prTpe}${era}_sfini.stderr -v FILE_IN=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_102X/BaseSelectionv2_${era2}/,FILE_OUT=${fileOut}/${prTpe}${era}_sfini.root,ERA=${era2},CSV_FILE=${csvFile}${prTpe}${era}.csv run2017DataJob.sh"
qsub -q express -N ${prTpe}${era}_sfini -o logs/${prTpe}${era}_sfini.stdout -e logs/${prTpe}${era}_sfini.stderr -v FILE_IN=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_102X/BaseSelectionv2_${era2}/,FILE_OUT=${fileOut}/${prTpe}${era}_sfini.root,ERA=${era2},CSV_FILE=${csvFile}${prTpe}${era}.csv run2017DataJob.sh

prTpe=tttt
echo " "
echo "qsub -q express -N ${prTpe}${era}_sfini -o logs/${prTpe}${era}_sfini.stdout -e logs/${prTpe}${era}_sfini.stderr -v FILE_IN=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_102X/BaseSelectionv2_${era2}/,FILE_OUT=${fileOut}/${prTpe}${era}_sfini.root,ERA=${era2},CSV_FILE=${csvFile}${prTpe}${era}.csv run2017DataJob.sh"
qsub -q express -N ${prTpe}${era}_sfini -o logs/${prTpe}${era}_sfini.stdout -e logs/${prTpe}${era}_sfini.stderr -v FILE_IN=/pnfs/iihe/cms/store/user/nistylia/Trimmed2017Data/TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_102X/BaseSelectionv2_${era2}/,FILE_OUT=${fileOut}/${prTpe}${era}_sfini.root,ERA=${era2},CSV_FILE=${csvFile}${prTpe}${era}.csv run2017DataJob.sh

done                                                                                                                                                                                                            

