#################################
## 2017/07/11 
## Programmed by Sohyun
#################################

import glob, os
def Add_scoreinfo(nScore_dic):

	nTotalNumb = 0
	nOver30 = 0
	nOver20 = 0
	
	for nScores in nScore_dic:
		nTotalNumb+=nScore_dic[nScores]
		#print nTotalNumb
		if nScores >= 20 :
			nOver20 +=nScore_dic[nScores]
		if nScores >= 30 :
			nOver30 +=nScore_dic[nScores]


	return nTotalNumb, nOver30, nOver20
def Make_writinglist():
	sDic = {}
	sSample_list = []
	for filenames in glob.glob("./1.Raw_data/*.gz"):


		Filename = os.path.split(filenames)[1]
		
		sReadName = Filename.split(".fq")[0]
		sSampleName = sReadName.split(".R")[0]
		sSample_list.append(sSampleName)

		sDic.setdefault(sReadName,{})

		fastqfile = "./1.Raw_data/"+sReadName+"_fastqc/fastqc_data.txt"
		infile = open(fastqfile,"r")
		
		Switch_forQ = 0

		nScore_dic = {}
		for sLine in infile:
			if sLine.startswith("Sequence length"):
				RaadLength = sLine.strip().replace("Sequence length","").replace("\t","").replace(" ","")
				sDic[sReadName]["ReadLength"] = RaadLength
			
			elif sLine.startswith("Total Sequences"):
				sCount_read = sLine.strip().replace("Total Sequences","").replace("\t","").replace(" ","")
				sDic[sReadName]["ReadCount"] = sCount_read
			

			elif sLine.startswith("%GC"):
				GCratio = sLine.replace("%GC","").strip().replace("\t","").replace(" ","")
				sDic[sReadName]["GCratio"] = GCratio 

			elif sLine.startswith("#Quality"):
				Switch_forQ = 1
			elif sLine.startswith(">>Per base sequence content"):
				Switch_forQ = 0

			if Switch_forQ == 1 :
				if not "#" in sLine:
					if not ">>" in sLine:
						sScoreList = sLine.strip().split("\t")
						nScore = float(sScoreList[0])
						nNumb = float(sScoreList[1])
						nScore_dic[nScore] = nNumb
		
		#print nScore_dic
		nTotalNumb, nOver30, nOver20 = Add_scoreinfo(nScore_dic)
		
		sDic[sReadName]["Q20ratio"] = nOver20/nTotalNumb
		sDic[sReadName]["Q30ratio"] = nOver30/nTotalNumb
		
		
		sTrimmomaticFile = "./2.Trimmomatic/"+sSampleName+"_.log"

		#nReads = Load_Trimmomatic(sTrimmomaticFile)
		'''
		CountLine_read_cmd = "zgrep -Ec '$'  "+filenames
		Count =os.popen(CountLine_read_cmd)
		nCount_read = Count.read()/2'''

		sDic[sReadName]["TotalSequences"] = str(int(sCount_read)*int(RaadLength))

				
	sSample_list = list(set(sSample_list))
	return sDic, sSample_list

def Load_Trimmomatic(sTrimmomaticFile):
	infile = open(sTrimmomaticFile,"r")
	for sLine in infile:
		#print sLine
		if sLine.startswith("Input Read Pairs: "):
			sList = sLine.split(" Both Surviving")
			
			sReads = sList[0].replace("Input Read Pairs: ","")
			nReads = int(sReads)

	return nReads 

					
def Writing_bySample(sReadsDic,sSample_list) :
	outfile = open("./6.Statistic/RawDatainfo.txt","w")
	outfile.write("SampleName\tReadLength\tTotalBase\tReadCount\tGC\tQ20Ratio\tQ30Ratio\n")
	for Samnpleid in sSample_list:
		SampleR1 = Samnpleid+".R1"
		SampleR2 = Samnpleid+".R2"


		outfile.write(Samnpleid)
		outfile.write("\t")
		outfile.write(sReadsDic[SampleR1]["ReadLength"])
		outfile.write("\t")
		outfile.write(sReadsDic[SampleR1]["TotalSequences"])
		outfile.write("\t")
		outfile.write(str(sReadsDic[SampleR1]["ReadCount"]))
		outfile.write("\t")

		#####################
		nTotalGCRatio = (float(sReadsDic[SampleR1]["GCratio"])+float(sReadsDic[SampleR1]["GCratio"]))/2
		
		outfile.write(str(nTotalGCRatio))
		outfile.write("\t")

		nQ20 = round((float(sReadsDic[SampleR1]["Q20ratio"])+float(sReadsDic[SampleR1]["Q20ratio"]))/2,5)
		outfile.write(str(nQ20))
		outfile.write("\t")
		nQ30 = round((float(sReadsDic[SampleR1]["Q30ratio"])+float(sReadsDic[SampleR1]["Q30ratio"]))/2,3)
		outfile.write(str(nQ30))
		outfile.write("\n")

if __name__ == "__main__":
	sReadsDic,sSample_list = Make_writinglist()
	Writing_bySample(sReadsDic,sSample_list)
