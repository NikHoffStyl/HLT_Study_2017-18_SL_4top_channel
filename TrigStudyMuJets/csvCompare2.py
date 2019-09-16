#!/usr/bin/env python3
# -*- coding: utf-8 -*-  

import csv
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("-i1", "--input1", help="Set name of input file1")
parser.add_argument("-i2", "--input2", help="Set name of input file2")
parser.add_argument("-o", "--output", help="Set name of output file")
args = parser.parse_args()

file1 = args.input1
file2 = args.input2
file3 = args.output

with open(file1, 'r') as t1, open(file2, 'r') as t2:
    fileone = t1.readlines()
    filetwo = t2.readlines()

counter_f2 = 0
counter_common = 0 
with open(file3, 'w') as outFile:
     for line in filetwo:
         counter_f2 += 1
     	 if line in fileone:
	    outFile.write(line)
            counter_common += 1

counter_f1 = 0
for line in fileone:
    counter_f1 += 1

print("f1: %d , f2: %d , Common: %d" %(counter_f1, counter_f2, counter_common))


#fileone.close()
#filetwo.close()
#outFile.close()
