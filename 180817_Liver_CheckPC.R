####################
##	17/07/08	##
##	By Sohyun   ##
####################

WD = "D:/C&KGenomics_ByFiled/RNASeq_분석/길동용_2년차_1차/4.DEG"
setwd(paste(WD,"0.Code",sep="/"))

setwd(paste(WD,"1.GeneCount",sep="/"))

Data <- read.table("Chicken_Liver.txt",header=T)
head(Data)
Header <- names(Data)
Tissue <- "Liver"

#Sorting_Table & Make Metadata
nCol <- ncol(Data)
CountData <- Data[,seq(from=7,to=nCol)]
head(CountData )

Condition <- c("Control","Control","Control","Control","Control"
,"Treatment","Treatment","Treatment","Treatment","Treatment")


GeneIDs <- Data[,1]
rownames(CountData) <- GeneIDs

head(CountData)
SampleID <- colnames(CountData)
SampleID <- gsub(".bam","",SampleID)
colnames(CountData) <- SampleID 
head(CountData)
dim(CountData)

#############################################################################
#########	MDS plot 		###############################################
#############################################################################

setwd(paste(WD,"2.DEG",sep="/"))

library(edgeR)
library(ggplot2)
library(limma)
library(edgeR)
library(ggplot2)
library(gridExtra)


MetaData <- data.frame(SampleID ,Condition)

str(MetaData)
targets <- MetaData ##Metadata
targets$Condition <- factor(targets$Condition)
str(targets)
levels(targets$Condition)
Condition <-factor(Condition,levels=c("Control","Treatment"))
targets$Condition <- factor(targets$Condition,levels=c("Control","Treatment"))

str(Condition)
head(CountData)
targets
design <- model.matrix(~Condition, data=targets)
y <- DGEList(counts=CountData, gene=GeneIDs)
y <- calcNormFactors(y)
y <- estimateGLMRobustDisp(y,design)
plotBCV(y)
fit <- glmFit(y, design)


TMM <- cpm(y, normalized.lib.sizes=TRUE,log=T)
head(TMM)

#########################################################################################

pdf(paste(Tissue,"_MDSplot.pdf",sep=""))
MDS_data <- plotMDS(y, top=20000)
dev.off()
?plotMDS
head(MDS_data)
cmdscale(MDS_data$distance.matrix, k = 9, eig = TRUE)



plot_data <- data.frame(Condition = targets$Condition, X=MDS_data$x, Y=MDS_data$y)

head(plot_data)

##########################################################################
theme0 <- function(...) theme( legend.position = "none",
                               panel.background = element_blank(),
                               panel.grid.major = element_blank(),
                               panel.grid.minor = element_blank(),
                               panel.margin = unit(0,"null"),
                               axis.ticks = element_blank(),
                               axis.text.x = element_blank(),
                               axis.text.y = element_blank(),
                               axis.title.x = element_blank(),
                               axis.title.y = element_blank(),
                               axis.ticks.length = unit(0,"null"),
                               axis.ticks.margin = unit(0,"null"),
                               panel.border=element_rect(color=NA),...)
##########################################################################


p1 <- ggplot(plot_data, aes(x=X, y=Y, color=Condition, label = colnames(TMM))) +
   geom_point(size=2) +
   xlab("Dimension 1") +
   ylab("Dimension 2") +
   scale_x_continuous(expand=c(0.02,0)) +
   scale_y_continuous(expand=c(0.02,0)) +
   #ylim(-0.6, 0.5)+
   #xlim(-0.6, 0.5)+
   theme_bw() +
   geom_text(size=3, vjust = 0, nudge_y = 0.02)
   #theme(legend.position="none",plot.margin=unit(c(0,0,0,0),"points"))
   

p2 <- ggplot(plot_data, aes(x=X, color=Condition, fill=Condition)) +  
   geom_density(alpha=0.5) +
   #scale_x_continuous(breaks=NULL,expand=c(0.02,0),limits=c(-0.6,0.5)) +
   #scale_y_continuous(breaks=NULL,expand=c(0.02,0)) +
   theme_bw() +
   theme0(plot.margin = unit(c(0,4,0,2),"lines"))



p3 <- ggplot(plot_data, aes(x=Y, colour=Condition,fill=Condition)) + 
   geom_density(alpha=0.5) +
   coord_flip()  +
   scale_x_continuous(labels = NULL,breaks=NULL,expand=c(0.02,0)) +
   scale_y_continuous(labels = NULL,breaks=NULL,expand=c(0.02,0)) +
   theme_bw() +
   theme0(plot.margin = unit(c(0,2,1.8,0),"lines"))

pdf(paste(Tissue,"_MDSplot_ggplot.pdf",sep=""))

grid.arrange(arrangeGrob(p2,ncol=2,widths=c(3,1)),
             arrangeGrob(p1,p3,ncol=2,widths=c(3,1)),
             heights=c(1,3))

dev.off()





###########################################################################
###########################################################################









##############################################
######## DEG : Weak vs Strong or Bright vs Dark
##############################################
DataName <- "Normal_vs_Drop"

lrt <- glmLRT(fit,coef = 2)
Result_table <- topTags(lrt, n=dim(CountData)[1], sort.by="none")$table
head(Result_table)
nrow(CountData)[1]
print(sum(Result_table$PValue < 0.01))
print(sum(Result_table$FDR < 0.01))
print(sum(Result_table$FDR < 0.05))

head(TMM)
TMM_ColName <- paste("TMMValue_",gsub(".bam", "",colnames(TMM)),sep="")
colnames(TMM) <- TMM_ColName

head(CountData)
RawCount_ColName <- paste("RawCount_",gsub(".bam", "",colnames(CountData)),sep="")
colnames(CountData) <- RawCount_ColName

Result <- cbind(Result_table,TMM,CountData)
head(Result)
tail(Result)

write.table(Result, paste("Result_",DataName,".txt",sep=""), sep="\t", quote=F, row.names=F)

Index <- as.numeric(order(Result$FDR)[10:20])

plot_data <- data.frame(Gene_expression = TMM[Index[1],],
	Condition,
	Gene_ID = rep(GeneIDs[Index[1]], length(Condition)))

for(i in 2:10){
	temp <- data.frame(Gene_expression = TMM[Index[i],],
	Condition,
	Gene_ID =rep(GeneIDs[Index[i]], length(Condition)))
	
	plot_data <- rbind(plot_data, temp)
}


ggplot(data=plot_data, aes(x=Condition, y=Gene_expression)) +
geom_boxplot() +
geom_boxplot(aes(fill = Condition)) +
facet_wrap(~ Gene_ID, nrow=3, ncol=4, scale = "free") +
guides(fill=FALSE) +
ylab("log2 TMM normalized values") +
xlab("") +
theme_bw() +
theme(axis.text.x = element_text(angle = 90, hjust = 1))


ggsave(paste("TopPvalue_BoxPlot",DataName,".tiff",sep=""), width=8, height=6)

##############################################
#################### VolcanoPlot #############
##############################################

FileName <- "Volcanoplot.tiff"

tiff(filename=FileName, width=2000, height=2400, res=300)

head(Result)
with(Result, plot(logFC, -log10(FDR), pch=20, main="Volcano plot"))
with(subset(Result,  FDR <.05 & logFC > 2), points(logFC, -log10(FDR), pch=20, col="brown3"))
with(subset(Result, FDR <.05 & logFC < -2), points(logFC, -log10(FDR), pch=20, col="#93dfb8" ))
dev.off()


#####################################################
#####################################################
##	7 hour vs 9 hour ##############################
#####################################################
#####################################################

WD = "D:/C&K_genomics/92.사과_RNAseq/4.DEG/"
setwd(paste(WD,"0.Code",sep="/"))

setwd(paste(WD,"1.GeneCount",sep="/"))

Data <- read.table("Result_withoutNC.txt",header=T)
head(Data)
Header <- names(Data)

#Sorting_Table & Make Metadata
nCol <- ncol(Data)
CountData <- Data[,seq(from=7,to=8)]
head(CountData )

Condition <- c("1h","7h")

MetaData <- data.frame()

GeneIDs <- Data[,1]
rownames(CountData) <- GeneIDs

head(CountData)
dim(CountData)

#############################################################################
#########	MDS plot 		###############################################
#############################################################################

setwd(paste(WD,"2.DEG",sep="/"))

library(edgeR)
library(ggplot2)
library(limma)
library(edgeR)
library(ggplot2)
library(gridExtra)

SampleID <- colnames(CountData)
MetaData <- data.frame(SampleID ,Condition)

str(MetaData)
targets <- MetaData ##Metadata
targets$Condition <- factor(targets$Condition)
str(targets)
levels(targets$Condition)
Condition <-factor(Condition,levels=c("1h","7h"))
targets$Condition <- factor(targets$Condition,levels=c("1h","7h"))

str(Condition)
head(CountData)
targets
design <- model.matrix(~Condition, data=targets)
y <- DGEList(counts=CountData, gene=GeneIDs)
y <- calcNormFactors(y)

TMM <- cpm(y, normalized.lib.sizes=TRUE,log=T)
head(TMM)
colnames(TMM) <- paste("TMMValue_",colnames(TMM),sep="")
colnames(CountData) <- paste("RawCount_",colnames(CountData),sep="")


Result <- data.frame(GeneName=GeneIDs,TMM,CountData)
head(Result)
DataName <- "1h_vs_7h"
write.table(Result, paste("Result_",DataName,".txt",sep=""), sep="\t", quote=F, row.names=F)


?cpm






