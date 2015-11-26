from nltk.tokenize import RegexpTokenizer
import re
from bs4 import BeautifulSoup
from urllib2 import urlopen
import num2words
from decimal import *
import matplotlib.pyplot as plt
from math import *
import numpy as np
#pdb.set_trace()

# The commented code is incase you want to download the text from the web

#url = "http://see.stanford.edu/materials/icsppcs107/transcripts/ProgrammingParadigms-Lecture01.html"
#request = urllib.request.Request(url)
#html = urlopen(url).read().decode('cp1252').encode('utf-8')
#raw = BeautifulSoup(html).get_text()
#print("===========================================================================================================")
#print(raw)
#print(html)

def ConvertNum2Words(text):
	
	p = re.compile('\d+')
	List = p.findall(text)
	#convert integers
	for i in range(0,len(List)):
		List[i] = int(float(List[i]))
	#sort in descending order
	List.sort(reverse=True)
	#convert it back to String :p
	for i in range(0,len(List)):
		List[i] = str(List[i])	
	for item in List:
		print item
		replace = num2words.num2words(int(float(item)))
		print replace
		text = re.sub(item,replace,text)
#		text = re.sub(item,num2words.num2words(int(float(item))),text)
#		print num2words.num2words(int(float(item)))	
	return text


replacement_patterns = [
        (r'won\'t', 'will not'),
        (r'can\'t', 'cannot'),
        (r'I\'m', 'I am'),
        (r'ain\'t', 'is not'),
        (r'(\w+)\'ll', '\g<1> will'),
        (r'(\w+)n\'t', '\g<1> not'),
        (r'(\w+)\'ve', '\g<1> have'),
        (r'(\w+)\'s', '\g<1> is'),
        (r'(\w+)\'re', '\g<1> are'),
        (r'(\w+)\'d', '\g<1> would'),
	(r'\+',' plus '),
	 (r'=',' equals '),
        (r'\*',' star '),
        (r'&',' ampersand '),
	(r'\$',' dollars ')

#	(r'[0-9]+', num2words.num2words(int(float('\g<1>')))),
]


class RegexpReplacer(object):

        def __init__(self,patterns=replacement_patterns):
                self.patterns = [(re.compile(regex), repl) for (regex,repl) in patterns]

        def replace(self, text):
                s = text
                for (pattern,repl) in self.patterns:
                        s = re.sub(pattern,repl,s)
                return s

replacer = RegexpReplacer()

raw = open('lecture1').read()

raw = re.sub('\xe2\x80\x99','\'',raw)
raw = re.sub('\xe2\x80\x9c','\"',raw)
raw = re.sub('\xe2\x80\x9d','\"',raw)
raw = re.sub('\xe2\x80\x90','-',raw)
raw = re.sub('\xe2\x80\x91','-',raw)
raw = re.sub('\xe2\x80\x92','-',raw)
raw = re.sub('\xe2\x80\x93','-',raw)
raw = re.sub('\xe2\x80\x94','-',raw)
raw = re.sub('\xe2\x80\x95','-',raw)
raw = re.sub('ProgrammingParadigms','Programming Paradigm',raw)

#print(raw)

raw = replacer.replace(raw)
raw = ConvertNum2Words(raw)

#print(raw)

#f = open('lecture1-clean','w')
#print >>f,raw
#f.close() 

#tokenizer = RegexpTokenizer(r'\b[w+]+\b')
tokenizer = RegexpTokenizer(r'\d+|[a-zA-Z]+|\$')
lecture = (tokenizer.tokenize(raw))

for i in range(0,len(lecture)):
	lecture[i] = lecture[i].upper()	


WordSet = (set(lecture))


vocab = open('switchboard_extracted').readlines()
for i in range(0,len(vocab)-1):
	vocab[i] = vocab[i].rstrip('\n')


#Start with the standard vocab, when OOV encountered, increase OOV count and add in the vocab. Give OOV rate after every word=OOV count/total words seen till now or will be seen (the total number of words in array). 
#i/p=lecture array, vocab, timetaken to add OOV in lecture
def CalculateOOVRateJeff1(array,vocab,TimeTakenToAddOOV,FileToWriteOOVRates):
        print "entered function"
        NumberOfTokensSeen = 0
        NumberOfOOVSeen = 0
        OOVRateArray = {}
        OOVArray = {}
	OOVRateArray[0] = FindOOVRateOffset(array,vocab,0,len(array))
	OOVArray[0] = 'NA'
        for i in range(1,len(array)):
                NumberOfTokensSeen = NumberOfTokensSeen + 1
		flag1 = 0
		flag2 = 0

                print "Processing token", array[i]

                if array[i] not in vocab:
                        OOVArray[i] = array[i]
                        print "OOV encountered", array[i]
                        NumberOfOOVSeen = NumberOfOOVSeen + 1
			flag1 = 1
                else:
                        OOVArray[i] = 'NA'
                        print "We are good, OOV not encountered"

                if (((i-TimeTakenToAddOOV) > 0) and (OOVArray[i-TimeTakenToAddOOV] is not 'NA')):
                        vocab.append(OOVArray[i-TimeTakenToAddOOV])
                        print "OOV added:", OOVArray[i-TimeTakenToAddOOV]
			flag2 = 1

#                OOVRateArray[i] = Decimal(NumberOfOOVSeen)/Decimal(NumberOfTokensSeen)
		if (flag1 == 1 or flag2 == 1):
			OOVRateArray[i] = FindOOVRateOffset(array[i+1:len(array)],vocab,NumberOfOOVSeen,len(array))
		else:
			OOVRateArray[i] = OOVRateArray[i-1]


        f = open(FileToWriteOOVRates,'w')

        for item in OOVRateArray:
                print>>f,OOVRateArray[item]*100

        f.close()
        for item in OOVArray:
                print(OOVArray[item])



def FindOOVRateOffset(array,vocab,Offset,LengthOfTheWholeThing):

        NumberOfMatches = 0
        NumberOfOOV = 0

        for x in array:
                if x in vocab:
                        NumberOfMatches = NumberOfMatches + 1
                else:
                        NumberOfOOV = NumberOfOOV + 1

        print('OOV rate:')
        print(Decimal(NumberOfOOV+Offset)/LengthOfTheWholeThing)
        return(Decimal(NumberOfOOV+Offset)/LengthOfTheWholeThing)




#Start with the standard vocab, when OOV encountered, increase OOV count and add in the vocab. Give OOV after every word=OOV count/total words seen till now.
#i/p=lecture array, vocab, timetaken to add OOV in lecture
def CalculateOOVRateJeff(array,vocab,TimeTakenToAddOOV,FileToWriteOOVRates):
	print "entered function"
	NumberOfTokensSeen = 0
	NumberOfOOVSeen = 0
	OOVRateArray = {}
	OOVArray = {}

	for i in range(0,len(array)):
		NumberOfTokensSeen = NumberOfTokensSeen + 1
		
		print "Processing token", array[i]		
		
		if array[i] not in vocab:
			OOVArray[i] = array[i]
			print "OOV encountered", array[i]
			NumberOfOOVSeen = NumberOfOOVSeen + 1
		else:
			OOVArray[i] = 'NA'
			print "We are good, OOV not encountered"
		
		if (((i-TimeTakenToAddOOV) >= 0) and (OOVArray[i-TimeTakenToAddOOV] is not 'NA')):
                	vocab.append(OOVArray[i-TimeTakenToAddOOV])
                        print "OOV added:", array[i-TimeTakenToAddOOV]
		
		OOVRateArray[i] = Decimal(NumberOfOOVSeen)/Decimal(NumberOfTokensSeen)
	
	f = open(FileToWriteOOVRates,'w')

	for item in OOVRateArray:
                print>>f,OOVRateArray[item]*100

        f.close()
	for item in OOVArray:
		print(OOVArray[item])

	

def FindOOVRate(array,vocab):
	
	NumberOfMatches = 0
	NumberOfOOV = 0

	for x in array:
		if x in vocab:
			NumberOfMatches = NumberOfMatches + 1
		else:
			NumberOfOOV = NumberOfOOV + 1
	
	print('OOV rate:')
	print(Decimal(NumberOfOOV)/Decimal(len(array)))
	return(Decimal(NumberOfOOV)/Decimal(len(array)))


#Function: Processes tokens linearly, adds OOV to the vocab and calculates the new OOV rate as and when the OOV token is encountered.
#i/p = token array, File to write instantaneous OOV rate array to.
#o/p = No return
def CrunchInstantaneous(FileToWriteOOVRates,array):

	OOVRateArray = {}
	OOVRateArray[0] = (FindOOVRate(array,vocab))

	for i in range(1,len(array)):
	
		print("processing token")	
		print(array[i])	

		if array[i] in vocab:
			OOVRateArray[i] = OOVRateArray[i-1]
		else:
		#add OOV to vocab then caculate OOV rate for the remaning words in the array
			vocab.append(array[i])
			print("New Vocab added:")
			print(vocab[-1])
			OOVRateArray[i] = (FindOOVRate(array,vocab))

	f = open(FileToWriteOOVRates,'w')

	for item in OOVRateArray:
		print>>f,(OOVRateArray[item]*100)
	f.close()



# CrucnhInterval will take an array (which usually a part of the token array) collect OOVs, add them to vocab 
def CrunchInterval(array):

        for i in range(1,len(array)):

                print("processing token")
                print(array[i])

                if array[i] not in vocab:
			
                	#add OOV to vocab 
                        vocab.append(array[i])
                        print("New Vocab added:")
                        print(vocab[-1])


#Take the token array, divide it into parts, do CrunchInterval for each part, return the OOVRate array which will look like a staircase wil be written to a file of your choice
def CrunchStepWise(array,StepWidth,FileToWriteOOVRates):

	OOVRateArray = {}
	ChunkOOV = FindOOVRate(array,vocab)
	NoOfSteps = len(array)/StepWidth
	LastStepWidth = len(array) % StepWidth
	
	for i in range(0,(NoOfSteps)):

		print("===============================")
		print(StepWidth*i)
		print(StepWidth*(i+1))
		print("===============================")
		for j in range(StepWidth*i,StepWidth*(i+1)):
			OOVRateArray[j] =  ChunkOOV

		CrunchInterval(array[StepWidth*i:StepWidth*(i+1)])
		ChunkOOV = FindOOVRate(array,vocab)
	

	print("======================================")
	print(StepWidth*(NoOfSteps))
	print(len(array))
	print(ChunkOOV)
	print("======================================")
	for k in range(StepWidth*(NoOfSteps),len(array)):
		
		print "I am adding ",ChunkOOV," to ",k,"index"
		OOVRateArray[k] = ChunkOOV
		print "length of OOV array is",len(OOVRateArray)

	f = open(FileToWriteOOVRates,'w')
	
	print("length of OOVRate array is ", len(OOVRateArray))
	for item in OOVRateArray:
		print "the followong item indexs are being written to file ",item
		print>>f,OOVRateArray[item]*100

	f.close()

#CrunchInstantaneous('RateDenoisedData',lecture)

#CrunchStepWise(lecture,500,'rate_500_only_words')
#print(lecture)
#print(vocab)
#CalculateOOVRateJeff(lecture,vocab,600,'rate_jeff_600')
#CalculateOOVRateJeff1(lecture,vocab,6000,'rate_jeff1_6000')

#get a list of OOV with in the order that they appear
f = open('OOVList','w')


OOVArray = []
for i in range(0,len(lecture)):
	if lecture[i] not in vocab:
		if lecture[i] not in OOVArray:
			OOVArray.append(lecture[i])
			print >> f, lecture[i]
			print >> f, i	
f.close()


UniqueOOV = OOVArray
OOVRepititionIndex = []
#once that is done, get the array indices of when an OOV occurs in lecture/raw
for i in range(0,len(UniqueOOV)):
	LocalIndexes = []
	for j in range(0,len(lecture)):
		if UniqueOOV[i] == lecture[j]:
			LocalIndexes.append(j)
	OOVRepititionIndex.append(LocalIndexes)

f = open('OOVMinimumDistance','w')
#show bursty nature of each OOV by printing  the minimum and maximum spacing between these OOVs
for i in range(0,len(OOVRepititionIndex)):
	x = np.array(OOVRepititionIndex[i])
	if len(x) > 1:
		print len(x)
		x_diff = np.diff(x)
		print >> f,lecture[x[0]]
		print >> f,np.amin(x_diff)
	 

f.close()

print "printing OOV array :D "
print OOVArray
print "to cross validate, I am printing the lecture index value of the first index stored in every nested list"
for i in range(0,len(OOVRepititionIndex)):
	print lecture[OOVRepititionIndex[i][0]]
print "another cross validation test, all the words that follow this should be the same"
for i in range(0,len(OOVRepititionIndex[0])):
	print lecture[OOVRepititionIndex[0][i]]
print "another cross validation test, all the words that follow this should be the same"
for i in range(0,len(OOVRepititionIndex[40])):
        print lecture[OOVRepititionIndex[40][i]]

for i in range(0,len(OOVRepititionIndex)):
	x = OOVRepititionIndex[i]
	ValueFory = x[0]
	y = [ValueFory]*len(x)
	plt.plot(x,y,linestyle="",marker="o")

plt.show()






	

	

	

	

	

