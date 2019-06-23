#!/usr/bin/env bash                                                                                                                                                                  
era=$1
logDESCRIPTOR=$2${era}_v
inputFILE=$3
outputFILE=$4
qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh
echo "Submitted >>> qsub -q localgrid -N ${logDESCRIPTOR} -o logs/${logDESCRIPTOR}.stdout -e logs/${logDESCRIPTOR}.stderr -v FILE_IN=${inputFILE},FILE_OUT=${outputFILE},ERA=${era} run2017DataJob.sh"

