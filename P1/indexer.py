import sys
import json
import nltk
import collections
import pickle
import argparse

from collections import Counter
from nltk.tokenize import RegexpTokenizer
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
# nltk.download('stopwords')
stop = stopwords.words('english') + list(string.punctuation)
tknzr = RegexpTokenizer(r'\w+')

moocs='.\corpora\moocs\json\moocs.json'
cf=[".\corpora\cf\json\cf74.json", ".\corpora\cf\json\cf75.json", ".\corpora\cf\json\cf76.json", ".\corpora\cf\json\cf77.json", ".\corpora\cf\json\cf78.json", ".\corpora\cf\json\cf79.json"]
indexer = dict()
id = dict()
data = dict()
jcf = []

parser = argparse.ArgumentParser(description="indexer")
parser.add_argument("-c", choices=["moocs", "cf"], help="select corpus", required=True)
args = parser.parse_args()
corpus = args.c

if corpus == "moocs" :
	# indexer for moocs
	jmoocs = json.loads(open(moocs).read())
	n=len(jmoocs)
	for x in jmoocs:
		dt = tknzr.tokenize(x["description"] + x["title"])
		dt = [i for i in dt if i not in stop]
		for y in dt:
			if y not in indexer:
				id[x["courseID"]] = 1
				indexer[y] = id.copy()	
			else:
				data = indexer.get(y)
				if x["courseID"] in data:
					data[x["courseID"]] = data.get(x["courseID"]) +1
				else:
					data[x["courseID"]] = 1
				indexer[y] = data.copy()	
				
		id.clear()
		data.clear()
	indexer['M'] = n	
	with open('indices/moocs_indexer.dat', 'w') as f:
		pickle.dump(indexer, f, pickle.HIGHEST_PROTOCOL)
		
elif corpus == "cf" :
	# indexer for cf
	n = 0
	for c in cf:
		jcf = json.loads(open(c).read())
		n = n+len(jcf)
		for x in jcf:
			authors = x.get("authors", '')
			mS = x.get("majorSubjects", '')
			miS = x.get("minorSubjects", '')
			if authors == '':
				authors = []	
			if mS == '':
				mS = []
			if miS == '':
				miS = []		
			str1 =  authors + mS + miS
			str2 = ' '.join(str1)
			dt = tknzr.tokenize( x["abstract/extract"] + x["title"] + str2)
			dt = [i for i in dt if i not in stop]	
			for y in dt:
				if y not in indexer:
					id[x["paperNum"]] = 1
					indexer[y] = id.copy()	
				else:
					data = indexer.get(y)
					if x["paperNum"] in data:
						data[x["paperNum"]] = data.get(x["paperNum"]) +1
					else:
						data[x["paperNum"]] = 1
					indexer[y] = data.copy()	
					
		id.clear()
		data.clear()
	indexer['M'] = n	
	with open('indices/cf_indexer.dat', 'w') as f:
		pickle.dump(indexer, f, pickle.HIGHEST_PROTOCOL)	

		
