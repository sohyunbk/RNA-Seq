import sys,re,os,string,glob
import Queue,threading,time


#################################
# main
#################################

#Step 4: Convert and sort sam filese
data_path = "3.HISAT"
os.chdir('/disk4/6.Sohyun_HanJaeYong_Chicken/' + data_path)

file = glob.glob("*.bam")

os.chdir('/disk4/6.Sohyun_HanJaeYong_Chicken/4.Sorted_BAM')
count = 1;

for left in file: 	
	id = left.split(".")[0]  

	cmd = '/home/Program/samtools-1.3.1/samtools sort -@ 18 ../%s/%s -o %s_Sorted.bam ' %(data_path, left, id)

	print(cmd)
	os.system(cmd)
