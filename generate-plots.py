'''
This is script is an adapted version of the scripts I had written 
for analyszing stanford talks w r t switchboard dictionary. Those
scripts were a mess. Here is me writing a cleaner version for their
analysis w r t tedlium ditionary instead. 
'''

import os
import glob
import re
import codecs
import num2words
import matplotlib.pyplot as plt
from decimal import *
import numpy as np
from tabulate import tabulate


'''
This function accepts a file and populates a list of the words
the expected form of the file:
each line:word pronunciation 
'''
def loadDictionary(dictionaryFile):
	
	content = open(dictionaryFile).readlines()
	dictionary = []
	
	for i in range(len(content)):
		line = content[i].split()
		word = line[0]
		dictionary.append(word)
	
	return dictionary






'''
This function returns all the files in the given directory
'''
def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))





'''
Accepts text and replaces all the instances of numbers with
their spellings
'''
def ConvertNum2Words(text):
	
	p = re.compile('\d+')
	List = p.findall(text)

	for i in range(0,len(List)):
		List[i] = int(float(List[i]))
	
	#sort in descending order.
	List.sort(reverse=True)
	
	for i in range(0,len(List)):
		List[i] = str(List[i])

	for item in List:
		replace = num2words.num2words(int(float(item)))		
		text = re.sub(item," "+replace+" ",text)

	return text


'''
strip all punctuations from the text
'''
def stripPunctuations(text):
	return "".join(c for c in text if c not in \
		('!','.',':',',','"','?'))




'''
This function normalizes the text:
1. strips all the punctuations
2. changes numbers to words -> done
3. symbols to their spellings -> done
4. 't to nots -> done
5. UTF charachters are cause problems while parsing -> done
6. convert unicode string to regular python strings

motivations: we do not want OOVs that are not actually OOVSs

NOTE: expects that the content is utf-8 compliant
'''
def normalizeText(text):

	# replacement patterns that will take care of ''t' and spell
	# out the special symbols	

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
		(r'\$',' dollars '),
		(r'\n',' '),
		('\xe2\x80\x99','\''),
		('\xe2\x80\x9c','\"'),
		('\xe2\x80\x9d','\"'),
		('\xe2\x80\x90','-'),
		('\xe2\x80\x91','-'),
		('\xe2\x80\x92','-'),
		('\xe2\x80\x93','-'),
		('\xe2\x80\x94','-'),
		('\xe2\x80\x95','-'),
		('ProgrammingParadigms','Programming Paradigm'),
		('\)', ' '),
		('\(', ' '),
		('-', ' '),
		('\[', ' '),
		('\]', ' '),
		(';', ' ')
	]

	# class for replacing regex patterns
	class RegexpReplacer(object):

		def __init__(self,patterns=replacement_patterns):
			self.patterns = [(re.compile(regex), repl) for (regex,repl) in patterns]

		def replace(self, text):
			s = text
			for (pattern,repl) in self.patterns:
				s = re.sub(pattern,repl,s)
			return s


    # instantiate the replacer
	replacer = RegexpReplacer()

	# strip punctuattions and convert all to upper case?
    # replace patterns and numbers
	return str(stripPunctuations(replacer.replace\
		(ConvertNum2Words(text)))).lower()
	

'''
accepts a path to a directory, where all the lectures are located 
It cleans (normalizes) them and returns a list of list, where each
sublist is an array from a lecture 
'''

def loadLectures(pathToLectures):

	lectures = []

	# get all the files on the path
	files = listdir_nohidden(pathToLectures)

	for f in files:
		f_open = codecs.open(f,"r","utf-8-sig")
		text = f_open.read().encode('ascii', 'ignore')

		lectures.append(normalizeText(text).split())
		f_open.close()

	return lectures




'''
Accepts a list of words, and prints the repitition in a convenient form
so that you can analyse it.
'''
def analyzeLecture(lecture, words_per_second, title):

	# Initializing all the important arrays
	uniqueOOV = []
	OOVArrayFrequency = []
	OOVTimeWhenFirstAppeared = []
	OOVArrayMinSpace = []
	OOVArrayMaxSpace = []
	OOVRepititionIndex = []

	
	#====== uniqueOOV and OOVTimeWhenFirstAppeared =========#

	for i in range(len(lecture)):
		word = lecture[i]
		if word not in dictionary and word not in uniqueOOV:
			uniqueOOV.append(word)
			OOVTimeWhenFirstAppeared.append(i)

	
	#====== OOVRepititionIndex and OOVArrayFrequency =========#	

	for i in range(len(uniqueOOV)):
		repitition = []
		for j in range(len(lecture)):
			if uniqueOOV[i] == lecture[j]:
				repitition.append(j)

		OOVRepititionIndex.append(repitition)
		OOVArrayFrequency.append(len(repitition))


	#====== OOVArrayMinSpace and OOVArrayMaxSpace =========#	

	for i in range(0,len(OOVRepititionIndex)):
		x = np.array(OOVRepititionIndex[i])
		if len(x) > 1:
			x_diff = np.diff(x)
			OOVArrayMinSpace.append(Decimal(np.amin(x_diff))/words_per_second)
			OOVArrayMaxSpace.append(Decimal(np.amax(x_diff))/words_per_second)
		else:
			OOVArrayMinSpace.append('NA')
			OOVArrayMaxSpace.append('NA')


	#====== print the graph ========#


	for i in range(0,len(OOVRepititionIndex)):
		x = OOVRepititionIndex[i]
		x = [Decimal(i)/words_per_second for i in x]
		ValueFory = x[0]
		y = [ValueFory]*len(x)
		plt.plot(x,y,linestyle="",marker="o")

	plt.xlabel('seconds')
	plt.ylabel('seconds')
	plt.suptitle(title)
	plt.savefig('graphs-and-tables/%d.png' % title)
	plt.clf()


	#======= save the table =======#


	f = open('graphs-and-tables/%d-table' % title,'w')
	table = []
	table.append(['OOV word','frequency','First Occurence (seconds)','Minimum Spacing (seconds)','Maximum Spacing(seconds)'])
	table.append(['','','','',''])
	for i in range(0,len(uniqueOOV)):
	        table.append([uniqueOOV[i],OOVArrayFrequency[i],Decimal(OOVTimeWhenFirstAppeared[i])/words_per_second,(OOVArrayMinSpace[i]),(OOVArrayMaxSpace[i])])

	print >> f,tabulate(table)
	totalOOV = sum(OOVArrayFrequency)
	print >> f, "Total number of OOV types",len(uniqueOOV),"\n","Total number of OOV tokens",totalOOV,"\n","OOV rate from the table:",(100*Decimal(totalOOV)/Decimal(len(lecture)))

	f.close()




'''
main
'''
if __name__ == '__main__':

	# config params
	dictionaryFile = 'TEDLIUM.150k.dic'
	pathToLectures = 'data/raw'
	words_per_second = 2

	# load dictionary
	dictionary = loadDictionary(dictionaryFile)

	# load the lectures 
	lectures = loadLectures(pathToLectures)

	for i in range(0,27):
		analyzeLecture(lectures[i], words_per_second, i+1)	