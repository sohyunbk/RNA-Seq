import sys,re,os,string,glob
import Queue,threading,time

#################################
# main
#################################

#Step 5: Merge GTFs 
# 1) Make mergelist.txt 
# 2) Stringtie --merge

############################################
data_path = "5.Stringtie"
Path='/disk4/6.Sohyun_HanJaeYong_Chicken/'
Annotation='Galgal4_Ensembl.gtf'
############################################

outfile=open(Path+data_path+"/mergelist.txt","w")

for sFilenames in glob.glob("./5.Stringtie/*.gtf"):
	
	sGTF= sFilenames.strip().split("/")[2]
	outfile.write(sGTF+"\n")

outfile.close()
  

os.chdir(Path + data_path)

cmd = "stringtie --merge -p 18 -G %s0.Reference/%s -o stringtie_merged.gtf mergelist.txt"%(Path,Annotation)
#cmd = "stringtie --merge -p 18 -G %s0.Reference/%s -o stringtie_merged.gtf"%(Path,Annotation)
#cmd = "stringtie --merge -p 18 -G %s0.Reference/%s -o stringtie_merged.gtf %s%s/mergelist.txt"%(Path,Annotation,Path,data_path)

print cmd
os.system(cmd)
