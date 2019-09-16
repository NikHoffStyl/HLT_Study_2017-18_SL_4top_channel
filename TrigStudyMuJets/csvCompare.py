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

csv_file1 = open(file1, "r")
csv_file2 = open(file2, "r")

csv_outfile = open(file3, "w")
csv_writer = csv.writer(csv_outfile, delimiter=',')


csv_reader1 = csv.reader(csv_file1, delimiter=',')
csv_reader2 = csv.reader(csv_file2, delimiter=',')

# csv_reader1 = csv.DictReader(csv_file1)
# csv_reader2 = csv.DictReader(csv_file2)


line1 = 0
line2 = 0
for row in csv_reader1:
    line1 += 1
    print(line1)
    print("%d , %d, %d" %(row[0],row[1],row[2]))
#    for roww in csv_reader2:
#    	line2 += 1
#    	print("%d , %d" % (line1 , line2))
    	#if row[0] != roww[0]: continue
	#if row[1] != roww[1]: continue
	#if row[2] != roww[2]: continue
#	if row[0] == roww[0] and row[1] == roww[1] and row[2] == roww[2]:
#		csv_writer.writerow([row[0], row[1], row[2]])

# csv_file1.close()
# csv_file2.close()
# csv_outfile.close()