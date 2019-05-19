#!/usr/bin/env bash

count=0
PRIMARY_DATASET="SEl"
ERA="A"
while read p; do
    echo "qsub -q localgrid -N ${count}_${PRIMARY_DATASET}18${ERA} -o logs/${count}_${PRIMARY_DATASET}18${ERA}.stdout -e logs/${count}_${PRIMARY_DATASET}18${ERA}.stderr -v FILE_TO_RUN_ON=$p  runJobSkimmer.sh" >> joblist.txt
    (( count++ ));
done <myInFiles/data2018/EGamma_Run2018A-Nano14Dec2018-v1.txt
echo " " >> joblist.txt

count=0
ERA="D"
while read p; do
    echo "qsub -q localgrid -N ${count}_${PRIMARY_DATASET}18${ERA} -o logs/${count}_${PRIMARY_DATASET}18${ERA}.stdout -e logs/${count}_${PRIMARY_DATASET}18${ERA}.stderr -v FILE_TO_RUN_ON=$p  runJobSkimmer.sh" >> joblist.txt
    (( count++ ));
done <myInFiles/data2018/EGamma_Run2018D-Nano14Dec2018-v1.txt
echo " " >> joblist.txt


count=0
PRIMARY_DATASET="TTTT"
while read p; do
    echo "qsub -q localgrid -N ${count}_${PRIMARY_DATASET}17 -o logs/${count}_${PRIMARY_DATASET}17.stdout -e logs/${count}_${PRIMARY_DATASET}17.stderr-v FILE_TO_RUN_ON=$p  runJobSkimmer.sh" >> joblist.txt
    (( count++ ));
done <myInFiles/data2018/mc/TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_102X.txt
echo " " >> joblist.txt

count=0
PRIMARY_DATASET="TTToSLep"
while read p; do
    echo "qsub -q localgrid -N ${count}_${PRIMARY_DATASET}17 -o logs/${count}_${PRIMARY_DATASET}17.stdout -e logs/${count}_${PRIMARY_DATASET}17.stderr runJobSkimmer.sh" >> joblist.txt
    (( count++ ));
done <myInFiles/data2018/mc/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_102X.txt
echo " " >> joblist.txt

for f in myInFiles/data/*
do

    if [[ $f == *"HTMHT"* ]]; then PRIMARY_DATASET="HT";
    elif [[ $f == *"SingleMuon"* ]]; then PRIMARY_DATASET="SMu";
    elif [[ $f == *"SingleElectron"* ]]; then PRIMARY_DATASET="SEl";
    fi

    if [[ $f == *"A"* ]]; then ERA="A";
    elif [[ $f == *"B"* ]]; then ERA="B";
    elif [[ $f == *"C"* ]]; then ERA="C";
    elif [[ $f == *"D"* ]]; then ERA="D";
    elif [[ $f == *"E"* ]]; then ERA="E";
    elif [[ $f == *"F"* ]]; then ERA="F";
    fi

    count=0
    while read p; do
        echo "qsub -q localgrid -N ${count}_${PRIMARY_DATASET}17${ERA} -o logs/${count}_${PRIMARY_DATASET}17${ERA}.stdout -e logs/${count}_${PRIMARY_DATASET}17${ERA}.stderr -v FILE_TO_RUN_ON=$p  runJobSkimmer.sh" >> joblist.txt
        (( count++ ));
    done <${f}

    echo " " >> joblist.txt
done