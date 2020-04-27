#################################
## 2017/07/11 
## Programmed by Sohyun
#################################
import glob, os

def Make_writinglist():
	outfile = open("./6.Statistic/Trimmomatic_statistic.txt","w")
	outfile.write("SampleName\tTotal reads\tBoth Surviving\tForward Only Surviving\tReverse Only Surviving\tDrop\n")
	sSample_list = []
	for filenames in glob.glob("./2.Trimmomatic/*.log"):


		Filename = os.path.split(filenames)[1]
		
		sSampleName = Filename.replace(".log","")
		print(sSampleName)
		
		infile = open(filenames,"r")
		for sLine in infile:
			if sLine.startswith("Input Read Pairs"):
				sList = sLine.split(":")
				sTotalReads = sList[1][1:].split(" ")[0]
				sBothSurviving = sList[2][1:].split(")")[0]+")"
				sForwardSurviving = sList[3][1:].split(")")[0]+")"
				sReverseSurviving = sList[4][1:].split(")")[0]+")"
				sDrop = sList[5][1:].split(")")[0]+")"
				
		sOutputline = sSampleName+"\t"+sTotalReads+"\t"+sBothSurviving+"\t"+sForwardSurviving+"\t"+sReverseSurviving+"\t"+sDrop+"\n"
		outfile.write(sOutputline)
	
	outfile.close()



					
if __name__ == "__main__":
	Make_writinglist()
	
