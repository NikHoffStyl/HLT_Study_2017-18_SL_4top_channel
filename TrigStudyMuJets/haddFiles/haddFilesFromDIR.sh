#!/bin/bash

echo " "

#setERA=17B
ERA_ARRAY=("17B" "17C" "17DEF")

counter=1
for f in ${1}*; do

if [[ $counter -eq 1 ]]; then 
    firstFile=${f}
elif [[ $counter -gt 1 ]];then
    echo "hadd ${2}${counter}.root  ${firstFile} ${f}"
    hadd ${2}${counter}.root  ${firstFile} ${f}
    firstFile=${2}${counter}.root
fi
if [[ $counter -gt 2 ]];then
    ((counter--))
    echo " "
    echo "rm ${2}${counter}.root"
    rm ${2}${counter}.root
    ((counter++))
fi
((counter++))
done

echo " "