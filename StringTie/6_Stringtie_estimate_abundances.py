import sys,re,os,string,glob
import Queue,threading,time

###########################################################
# main
# Step 6
# Stringtie --> estimate abundances using BAM & merged GTF
###########################################################

Path="/disk4/6.Sohyun_HanJaeYong_Chicken/"
data_path = "4.Sorted_BAM"

os.chdir(Path+data_path)

file = glob.glob("*.bam")

os.chdir(Path+'6.Transcript_abundance')

count = 1;

for left in file: 	
	id = left.split(".")[0] 
	
	cmd = "stringtie -e -B -p 18 -G %s5.Stringtie/stringtie_merged.gtf -o %s.gtf %s%s/%s 2> %s.log"%(Path,id,Path,data_path,left,id)
	

	print(cmd)
	os.system(cmd)
