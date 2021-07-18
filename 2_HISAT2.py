import sys,re,os,string,glob
import Queue,threading,time

#################################
# main
#################################

my_path = "/RNA-seqProtocol/"
data_path = "2.Trimmomatic"
Program = "/hisat2-2.1.0/hisat2"
os.chdir(my_path + data_path)
file = glob.glob("*R1.paired.fq")

#os.mkdir(my_path + '3.HISAT')
os.chdir(my_path + '3.HISAT')
count = 1

for id_left in file: 	
	id_right = id_left.replace("R1", "R2")

	id_bam = id_log = id_left.split(".R1")[0]

	if not id_bam+".bam" in os.listdir(os.curdir):

		cmd = "%s -p 14 --rna-strandness RF -x %s0.Reference/galGal4 -1 ../2.Trimmomatic/%s -2 ../2.Trimmomatic/%s 2> %s.log| samtools view -@ 8 -Sbo %s.bam -"%(Program,my_path, id_left, id_right, id_log, id_bam)

		print(cmd)
		os.system(cmd)

