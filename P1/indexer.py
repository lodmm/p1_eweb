import sys
import json
import nltk
import collections
import pickle

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
if len(sys.argv) != 3:
	print ("Error: missing corpus, indexer -c [moocs|cf]")
	sys.exit(1)
if (sys.argv[1]+" "+sys.argv[2]) == "-c moocs" :
	# indexer for moocs
	jmoocs = json.loads(open(moocs).read())
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
	with open('indices/moocs_indexer.dat', 'wb') as f:
		pickle.dump(indexer, f, pickle.HIGHEST_PROTOCOL)
		
elif (sys.argv[1]+" "+sys.argv[2] ) == "-c cf" :
	# indexer for cf
	for c in cf:
		jcf = json.loads(open(c).read())
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
	with open('indices/cf_indexer.dat', 'wb') as f:
		pickle.dump(indexer, f, pickle.HIGHEST_PROTOCOL)	
else:
	print ("Error: introduce a valid corpus, indexer -c [moocs|cf]")
	sys.exit(1)
		
