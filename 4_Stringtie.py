import sys,re,os,string,glob
import Queue,threading,time

#################################
# main
#################################


data_path = "4.Sorted_BAM"
os.chdir('/disk4/6.Sohyun_HanJaeYong_Chicken/' + data_path)

file = glob.glob("*.bam")

os.chdir('/disk4/6.Sohyun_HanJaeYong_Chicken/5.Stringtie')
count = 1;

for left in file: 	
	id = left.split("_Sorted")[0] 
	
	
	cmd = "stringtie -p 18 -G ../0.Reference/Galgal4_Ensembl.gtf -o %s.gtf -l %s ../4.Sorted_BAM/%s"%(id,id,left)

	print(cmd)
	os.system(cmd)
