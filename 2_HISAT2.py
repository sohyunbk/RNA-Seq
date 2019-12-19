import sys,re,os,string,glob
import Queue,threading,time

#################################
# main
#################################

#Step 1: Align the read on the bovine reference genome
my_path = "/disk4/6.Sohyun_HanJaeYong_Chicken/"
data_path = "2.Trimmomatic"
os.chdir(my_path + data_path)
file = glob.glob("*R1.paired.fastq.gz")

#os.mkdir(my_path + '3.HISAT')
os.chdir(my_path + '3.HISAT')
count = 1

for id_left in file: 	
	id_right = id_left.replace("R1", "R2")

	id_bam = id_log = id_left.split("_R1")[0]

	cmd = "/home/Program/hisat2-2.0.0-beta/hisat2 -p 16 --rna-strandness RF -x %s0.Reference/Galgal4_tran -1 ../2.Trimmomatic/%s -2 ../2.Trimmomatic/%s 2> %s.log| samtools view -@ 8 -Sbo %s.bam -"%(my_path, id_left, id_right, id_log, id_bam)

	print(cmd)
	os.system(cmd)

	count = count + 1
