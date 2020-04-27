import sys,re,os,string,glob
import Queue,threading,time

#################################
# main
#################################
os.system("mkdir 2.Trimmomatic") 
#Step 1: Trimmomatic to remove adapter sequences (in order to generate clean read)
my_path = "/disk10/1.SH_chicken_mRNA_ChungangUniv_2nd/"

data_path = "1.Raw_data"


os.chdir(my_path + data_path)
file = glob.glob("*R1.fq.gz")

os.chdir(my_path + '2.Trimmomatic')
count = 1;

outfile = open("Trimmomatic_cmd.log","w")
for id_left in file:
	id_right = id_left.replace(".R1.", ".R2.")
	id_log = id_left.replace("R1.fq.gz", "log")

	id_left_output_paired = id_left.replace("R1.fq.gz", "R1.paired.fq")
	id_right_output_paired = id_right.replace("R2.fq.gz", "R2.paired.fq")

	id_left_output_unpaired = id_left.replace("R1.fq.gz", "R1.unpaired.fq")
	id_right_output_unpaired = id_right.replace("R2.fq.gz", "R2.unpaired.fq")

	#print(os.listdir(os.curdir))
	if not id_log in os.listdir(os.curdir):

		cmd = 'java -jar /home/Program/Trimmomatic-0.36/trimmomatic-0.36.jar PE -threads 14  -phred33 ../%s/%s ../%s/%s %s %s %s %s ILLUMINACLIP:/home/Program/Trimmomatic-0.36/adapters/TruSeq3-PE-2.fa:2:30:10 TRAILING:20 SLIDINGWINDOW:4:15 MINLEN:75 2> %s'%(data_path, id_left, data_path, id_right, id_left_output_paired, id_left_output_unpaired, id_right_output_paired, id_right_output_unpaired, id_log)
		
		print(cmd)
		outfile.write(cmd+"\n")
		os.system(cmd)
		
	count = count +1
		
