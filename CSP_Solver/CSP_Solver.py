import csv
import sys


###
### These are the present XML tags that can be used to write an XML tag
### to an XML file
###
def OpenTag(fileName):
    fileName.write('<CSPIF VERSION="0.01">\n')
    fileName.write('<CSP>\n')

def CloseTag(fileName):
    fileName.write('</CSP>\n')
    fileName.write('</CSPIF>\n')


def NameTag(fileName, Name):
    fileName.write('<NAME>'+Name+'</NAME>\n')


def CustomNameTag(fileName, Name):
    fileName.write('<CUSTOMNAME>'+Name+'</CUSTOMNAME>\n')

def ValueTag(fileName, Value):
    fileName.write('<VALUE>'+Value+'</VALUE>\n')

def VarOTag(fileName,Type):
    fileName.write('<VARIABLE TYPE ="'+Type+'">\n')

def VarCTag(fileName):
    fileName.write('</VARIABLE>\n\n')

def DescriptionTag(fileName):
    fileName.write("<DESCRIPTION>\n<SHORT></SHORT>\n<DETAILED></DETAILED>\n</DESCRIPTION>\n")

def ConstraintTag(fileName,names,truthTable,customName):
    fileName.write('<CONSTRAINT TYPE="Custom">\n<CUSTOMNAME>'+customName+'</CUSTOMNAME>\n')
    for x in range(0,len(names)):
        GivenTag(fileName,names[x])
    TableTag(fileName,truthTable)
    fileName.write("</CONSTRAINT>\n\n")


def GivenTag(fileName,Name):
    fileName.write("<GIVEN>"+Name+"</GIVEN>\n")

def TableTag(fileName,truthTable):
    fileName.write("<TABLE>\n"+truthTable+"\n</TABLE>\n")



#######
#######
#######Main
#######
#######




###
###
###CSV File Reader
###
###


allRows = []

inputCSVFile = open(sys.argv[1],"r")
reader = csv.reader(inputCSVFile)

for currentRow in reader:
    allRows.append(currentRow)

inputCSVFile.close()


###
###
### Store values into lists for manipulation.
###
###

#Makes a list of Variables with all its values
VARcount = int(allRows[0][0])
indexADC = VARcount+1;
varValPairs = []
for x in range(1,VARcount+1):
    Variable = allRows[x][0]
    Values = []
    for y in range(2, len(allRows[x])):
        if(allRows[x][y] != None):
            if(allRows[x][y]!=''):
                Values.append(allRows[x][y])
    varValPairs.append((Variable,Values))


#Makes a list of All Diff Constraints
ADCcount = int(allRows[indexADC][0])
indexCNF = indexADC+ADCcount+1
allDif = []
for x in range(indexADC+1,indexADC+ADCcount+1):
    difRow = []
    for y in range(0, len(allRows[x])):
        if(allRows[x][y] != ''):
            difRow.append(allRows[x][y])
    allDif.append(difRow)


#Makes a list of CNF Clauses
CNFclauses = []
CNFcount = int(allRows[indexCNF][0])
for x in range(indexCNF+1,indexCNF+CNFcount+1):
    CNFclause = []
    for y in range(0, len(allRows[x])):
        if(allRows[x][y] != ''):
            CNFclause.append(allRows[x][y])
    CNFclauses.append(CNFclause)





###
###
###HELPER METHOD FOR FILE WRITING
###
###


def getVals(var):
    for x in range(0,len(varValPairs)):
        if(varValPairs[x][0]==var):
            return varValPairs[x][1]

def getTruthTable(val1,val2):
    truthLine = ""
    for x in range(0,len(val1)):
        for y in range(0,len(val2)):
            if(val1[x]==val2[y]):
                truthLine = truthLine+"F "
            else:
                truthLine = truthLine+"T "
    return truthLine

def reformatLiterals(literals):
    varValBool = [];
    for index in range(0,len(literals)):
        temp = literals[index].split("/")
        if(len(temp)>1):
            varValBool.append([temp[0],temp[1],False])
        else:
            temp = literals[index].split("=")
            varValBool.append([temp[0],temp[1],True])
    return varValBool


def getTFSeq(literals):
    VarTFSeq = []
    for x in range(0,len(literals)):
        TFSeq = []
        literalValues = getVals(literals[x][0])
        testVal = literals[x][1]
        BOOL = literals[x][2]
        for y in range(0,len(literalValues)):
            if(literalValues[y]==testVal):
                if(BOOL==True):
                    TFSeq.append("T")
                else:
                    TFSeq.append("F")
            else:
                if(BOOL==True):
                    TFSeq.append("F")
                else:
                    TFSeq.append("T")
        VarTFSeq.append(TFSeq)
    return VarTFSeq

def getCNFTruthTable(TFSequences):
    numOfClauses = len(TFSequences)

    index=1

    currSeq = TFSequences[0]

    tempSeq = []
    for clause in range(1,numOfClauses):
        for x in range(0,len(currSeq)):
            if(index<numOfClauses):
                comparingSeq = TFSequences[index]
                for y in range(0,len(comparingSeq)):
                    if(currSeq[x]=="T" or comparingSeq[y]=="T"):
                        tempSeq.append('T')
                    else:
                        tempSeq.append('F')
        currSeq = tempSeq
        tempSeq = []
        index=index+1

    tableAsString = ""
    for x in range(0,len(currSeq)):
        tableAsString=tableAsString+currSeq[x]+' '
    return tableAsString












###
###
###WRITING TO OUTPUT FILE
###
###


writeFile = open(sys.argv[2],"w")

OpenTag(writeFile)
NameTag(writeFile,"Untitled")
DescriptionTag(writeFile)

#WRITES ALL VARIABLES AND THEIR VALUES INTO XML FILE
for x in range(0,len(varValPairs)):
    VarOTag(writeFile,"String")
    NameTag(writeFile,varValPairs[x][0])
    for y in range(0,len(varValPairs[x][1])):
        if(varValPairs[x][1][y] != ""):
            ValueTag(writeFile,varValPairs[x][1][y])
    VarCTag(writeFile)

#WRITES OUT ALLDIF CONSTRAINTS INTO XML FILE
allDifPairs = []
for x in range(0,len(allDif)):
    for y in range(0,len(allDif[x])):
        for z in range(y+1,len(allDif[x])):
            if((len(allDif[x])-y)>=2):
                allDifPairs.append([allDif[x][y],allDif[x][z]])

for x in range(0,len(allDifPairs)):
    valueSet1 = getVals(allDifPairs[x][0])
    valueSet2 = getVals(allDifPairs[x][1])
    truthTable = getTruthTable(valueSet1,valueSet2)
    ConstraintTag(writeFile,[allDifPairs[x][0],allDifPairs[x][1]],truthTable,"allDif")

#WRITES ON CNF CONSTRAINTS INTO XML FILES
for x in range(0,len(CNFclauses)):
    variableTruthVals = reformatLiterals(CNFclauses[x])
    varTFSeq = getTFSeq(variableTruthVals)
    truthTable = getCNFTruthTable(varTFSeq)
    names=[]
    for name in range(0,len(variableTruthVals)):
        names.append(variableTruthVals[name][0])
    ConstraintTag(writeFile,names,truthTable,'CNF Clause')



CloseTag(writeFile)
