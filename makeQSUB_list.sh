#!/usr/bin/env bash

export pathToFile=$1
export logDescriptor=$2


count=0
while read p; do
    qsub -q localgrid -N ${logDescriptor}_${count} -o logs/${logDescriptor}_${count}.stdout -e logs/${logDescriptor}_${count}.stderr -v FILE_TO_RUN_ON=$p  runJobSkimmer.sh
    (( count++ ));
    echo "Submitted >>> qsub -q localgrid -N ${logDescriptor}_${count} -o logs/${logDescriptor}_${count}.stdout -e logs/${logDescriptor}_${count}.stderr -v FILE_TO_RUN_ON=$p  runJobSkimmer.sh"
done < ${pathToFile}
echo "All Done! Submitted all files listed."