import glob, os

def Alignment_info_dic():
	sDic = {}
	for sFiles in glob.glob("./3.HISAT/*.log") :
		sSamples = os.path.split(sFiles)[1].split(".log")[0]

		infile = open(sFiles,"r")

		sDic.setdefault(sSamples,{})
		for sLine in infile:
			#print sLine
			if ") aligned concordantly 0 times" in sLine:
				print(sLine)	
				sConcordantly = sLine.split("(")[1].split(")")[0]
				sDic[sSamples]["Zero"] = sConcordantly
				
			elif "aligned concordantly exactly 1 time" in sLine:
				
				sConcordantly1Time = sLine.split("(")[1].split(")")[0]	
				#print sConcordantly1Time
				sDic[sSamples]["1Time"] = sConcordantly1Time
			elif "aligned concordantly >1 times" in sLine:
				sConcordantlyMore = sLine.split("(")[1].split(")")[0]	
				sDic[sSamples]["Multiple"] =sConcordantlyMore
			elif "overall alignment rate" in sLine:
				sOverall = sLine.split(" ")[0]		
				sDic[sSamples]["All"] = sOverall

	return sDic
					
def Writing_bySample(sAlignmentDic) :
	outfile = open("./6.Statistic/Alignmentinfo.txt","w")
	outfile.write("SampleName\tOverallAlignmentRate\tConcordantZero\tConcordantPairAlignment\tMultipleAlignment\n")
	for Samnpleid in sAlignmentDic.keys():
		
		outfile.write(Samnpleid)
		outfile.write("\t")
		
		outfile.write(sAlignmentDic[Samnpleid]["All"])
		outfile.write("\t")

		outfile.write(sAlignmentDic[Samnpleid]["Zero"])
		outfile.write("\t")


		outfile.write(sAlignmentDic[Samnpleid]["1Time"])
		outfile.write("\t")


		outfile.write(sAlignmentDic[Samnpleid]["Multiple"])
		outfile.write("\n")

		#####################


if __name__ == "__main__":
	
	sAlignmentDic = Alignment_info_dic()
	Writing_bySample(sAlignmentDic)
