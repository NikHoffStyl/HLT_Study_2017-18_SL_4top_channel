#!/usr/bin/env bash

count=0
PRIMARY_DATASET="TTTT"
while read p; do
    echo "qsub -q localgrid -N ${count}_${PRIMARY_DATASET}17 -o logs_v2/${count}_${PRIMARY_DATASET}17.stdout -e logs_v2/${count}_${PRIMARY_DATASET}17.stderr -v FILE_TO_RUN_ON=$p  runJobSkimmer.sh" >> joblist_v2.txt
    (( count++ ));
done <myInFiles/mc/TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_102X.txt
echo " " >> joblist_v2.txt

count=0
PRIMARY_DATASET="TTTT"
while read p; do
    echo "qsub -q localgrid -N ${count}_${PRIMARY_DATASET}18 -o logs_v2/${count}_${PRIMARY_DATASET}18.stdout -e logs_v2/${count}_${PRIMARY_DATASET}18.stderr -v FILE_TO_RUN_ON=$p  runJobSkimmer.sh" >> joblist_v2.txt
    (( count++ ));
done <myInFiles/mc/TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_102X_18.txt
echo " " >> joblist_v2.txt

count=0
PRIMARY_DATASET="TTToSLep"
while read p; do
    echo "qsub -q localgrid -N ${count}_${PRIMARY_DATASET}17 -o logs_v2/${count}_${PRIMARY_DATASET}17.stdout -e logs_v2/${count}_${PRIMARY_DATASET}17.stderr -v FILE_TO_RUN_ON=$p runJobSkimmer.sh" >> joblist_v2.txt
    (( count++ ));
done <myInFiles/mc/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_102X.txt
echo " " >> joblist_v2.txt

count=0
PRIMARY_DATASET="TTToSLep"
while read p; do
    echo "qsub -q localgrid -N ${count}_${PRIMARY_DATASET}18 -o logs_v2/${count}_${PRIMARY_DATASET}18.stdout -e logs_v2/${count}_${PRIMARY_DATASET}18.stderr -v FILE_TO_RUN_ON=$p runJobSkimmer.sh" >> joblist_v2.txt
    (( count++ ));
done <myInFiles/mc/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_102X_18.txt
echo " " >> joblist_v2.txt

for f in myInFiles/data/*
do

    if [[ $f == *"HTMHT"* ]]; then PRIMARY_DATASET="HT";
    elif [[ $f == *"SingleMuon"* ]]; then PRIMARY_DATASET="SMu";
    elif [[ $f == *"SingleElectron"* ]]; then PRIMARY_DATASET="SEl";
    fi

    if [[ $f == *"Run2017B"* ]]; then ERA="17B";
    elif [[ $f == *"Run2017C"* ]]; then ERA="17C";
    elif [[ $f == *"Run2017D"* ]]; then ERA="17D";
    elif [[ $f == *"Run2017E"* ]]; then ERA="17E";
    elif [[ $f == *"Run2017F"* ]]; then ERA="17F";
    fi

    count=0
    while read p; do
        echo "qsub -q localgrid -N ${count}_${PRIMARY_DATASET}${ERA} -o logs_v2/${count}_${PRIMARY_DATASET}${ERA}.stdout -e logs_v2/${count}_${PRIMARY_DATASET}${ERA}.stderr -v FILE_TO_RUN_ON=$p  runJobSkimmer.sh" >> joblist_v2.txt
        (( count++ ));
    done <${f}

    echo " " >> joblist_v2.txt
done

for f in myInFiles/data2018/*
do

    if [[ $f == *"JetHT"* ]]; then PRIMARY_DATASET="HT";
    elif [[ $f == *"SingleMuon"* ]]; then PRIMARY_DATASET="SMu";
    elif [[ $f == *"EGamma"* ]]; then PRIMARY_DATASET="SEl";
    fi

    if [[ $f == *"Run2018A"* ]]; then ERA="18A";
    elif [[ $f == *"Run2018B"* ]]; then ERA="18B";
    elif [[ $f == *"Run2018C"* ]]; then ERA="18C";
    elif [[ $f == *"Run2018D"* ]]; then ERA="18D";
    fi

    count=0
    while read p; do
        echo "qsub -q localgrid -N ${count}_${PRIMARY_DATASET}${ERA} -o logs_v2/${count}_${PRIMARY_DATASET}${ERA}.stdout -e logs_v2/${count}_${PRIMARY_DATASET}${ERA}.stderr -v FILE_TO_RUN_ON=$p  runJobSkimmer.sh" >> joblist_v2.txt
        (( count++ ));
    done <${f}

    echo " " >> joblist_v2.txt
done