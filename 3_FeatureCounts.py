import sys,re,os,string,glob

import Queue,threading,time

#Final step: Convert and sort sam filese
GTF_file = 'Gallus_gallus.Galgal4.82_mRNA.gtf'
Program = "/disk11/1.Sohyun_ChickenRNAseq_ChungangUniv/subread-1.5.2-Linux-x86_64/bin/featureCounts"

os.system("mkdir 4.FeatureCounts_mRNA")

my_path = "/disk10/1.SH_chicken_mRNA_ChungangUniv_2nd/"
outputdir="4.FeatureCounts_mRNA"
dir = '3.HISAT'

#####################################
os.chdir(my_path+dir)


Jej_Color = ["BR-Jej-75.bam","BR-JeJ-102.bam","BR-JeJ-179.bam","BR-Jej-190-new.bam","DK-JeJ-31.bam","DK-Jej-33.bam","DK-Jej-154-new.bam","DK-Jej-187-new.bam"]
uT_Color = ["BR-uT-75.bam","BR-uT-102.bam","BR-uT-161.bam","BR-uT-179.bam","BR-uT-190-new.bam","DK-uT-31.bam","DK-uT-33.bam","DK-uT-49.bam","DK-uT-89.bam","DK-uT-154.bam"]
Jej_Strength = ["ST-JeJ-63.bam","ST-Jej-118-new.bam","ST-JeJ-138.bam","ST-Jej-143-new.bam","WK-Jej-49.bam","WK-Jej-119-new.bam","WK-Jej-127.bam","WK-Jej-171-new.bam"]
uT_Strength=["ST-uT-63.bam","ST-uT-118.bam","ST-uT-138.bam","ST-uT-143.bam","ST-uT-148.bam","WK-uT-49.bam","WK-uT-117.bam","WK-uT-119.bam","WK-uT-127.bam","WK-uT-171.bam"]


count = 1;

cmd = "%s -T 6 -p -s 2 -t exon -g gene_id -a ../0.Reference/%s -o %s%s/Chicken_Jej_Color.txt %s" %(Program,GTF_file,my_path,outputdir," ".join(Jej_Color))
print(cmd)
os.system(cmd)

cmd = "%s -T 6 -p -s 2 -t exon -g gene_id -a ../0.Reference/%s -o %s%s/Chicken_uT_Color.txt %s" %(Program,GTF_file,my_path,outputdir," ".join(uT_Color))
print(cmd)
os.system(cmd)

cmd = "%s -T 6 -p -s 2 -t exon -g gene_id -a ../0.Reference/%s -o %s%s/Chicken_Jej_Strength.txt %s" %(Program,GTF_file,my_path,outputdir," ".join(Jej_Strength))
print(cmd)
os.system(cmd)

cmd = "%s -T 6 -p -s 2 -t exon -g gene_id -a ../0.Reference/%s -o %s%s/Chicken_uT_Strength.txt %s" %(Program,GTF_file,my_path,outputdir," ".join(uT_Strength))
print(cmd)
os.system(cmd)
