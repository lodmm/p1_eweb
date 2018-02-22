import sys
import json
import nltk
import collections
import pickle
import argparse

from collections import Counter
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
# nltk.download('stopwords')
stop = stopwords.words('english') + list(string.punctuation) 
tknzr = RegexpTokenizer(r'\w+')

moocs='./corpora/moocs/json/moocs.json'
cf=["./corpora/cf/json/cf74.json", "./corpora/cf/json/cf75.json", "./corpora/cf/json/cf76.json", "./corpora/cf/json/cf77.json", "./corpora/cf/json/cf78.json", "./corpora/cf/json/cf79.json"]
indexer = dict()
id = dict()
tam_c = dict()
avg = dict()
jcf = []
t_title = 0
t_desc = 0
t_mS = 0
t_miS = 0
t_auth = 0
parser = argparse.ArgumentParser(description="indexer")
parser.add_argument("-c", choices=["moocs", "cf"], help="select corpus", required=True)
args = parser.parse_args()
corpus = args.c

def get_indexer(x, c_id, t, block):
	aux = dict()
	ind = dict()
	data = dict()
	types = dict()
	for y in block:
		if y not in indexer:
			types[t] = 1
			ind[x[c_id]] = types.copy()				
			indexer[y] = ind.copy()	
		else:
			data = indexer.get(y)
			if x[c_id] in data:
				aux = data.get(x[c_id])
				if t in aux:
					aux[t] = aux.get(t)+ 1
				else:
					aux[t] = 1
				data[x[c_id]] = aux.copy()	
			else:
				types[t] = 1
				data[x[c_id]] = types.copy()
			indexer[y] = data.copy()		
		aux.clear()	
		types.clear()	
		ind.clear()
		data.clear()
	return		

def get_pln(dt):
	wordStemmer = []
	dt = tknzr.tokenize(dt)
	ls = WordNetLemmatizer()
	for w in dt:
		wordStemmer.append(ls.lemmatize(w.lower()))
	dt = wordStemmer
	# dt = [i for i in dt if (i not in stop)]
	return dt
	
if corpus == "moocs" :
	# indexer for moocs
	jmoocs = json.loads(open(moocs).read())
	n=len(jmoocs)
	for x in jmoocs:
		#Description
		dt = x['description']
		dt = get_pln(dt)
		t_title += len(dt)
		tam_c['description'] = len(dt)
		get_indexer(x, 'courseID', 'description', dt )
		#Title
		dt = x['title']
		dt = get_pln(dt)
		t_desc += len(dt)
		tam_c['title'] = len(dt)
		get_indexer(x, 'courseID', 'title', dt )
		id[x['courseID']] = tam_c.copy()
		tam_c.clear()
	indexer['M'] = n
	avg['title'] = t_title/n	
	avg['description'] = t_desc/n	
	indexer['tam_c'] = id.copy()	
	indexer['avg']	= avg.copy()	
	with open('indices/moocs_indexer.dat', 'wb') as f:
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
			#Title
			dt = x['title']
			dt = get_pln(dt)	
			t_title += len(dt)
			tam_c['title'] = len(dt)
			get_indexer(x,'recordNum','title',dt)
			#Authors
			str1 = ' '.join(authors)
			dt = get_pln(str1)
			t_auth += len(dt)
			tam_c['authors'] = len(dt)
			get_indexer(x,'recordNum','authors',dt)
			str1 = ' '
			#MajorSubjects
			str1 = ' '.join(mS)
			dt = get_pln(str1)
			t_mS += len(dt)
			tam_c['majorSubjects'] = len(dt)
			get_indexer(x,'recordNum','majorSubjects',dt)
			str1 = ' '
			#MinorSubjects
			str1 = ' '.join(miS)
			dt = get_pln(str1)
			t_miS += len(dt)
			tam_c['minorSubjects'] = len(dt)
			get_indexer(x,'recordNum','minorSubjects',dt)
			str1 = ' '
			#Desciption
			dt = x['abstract/extract']
			dt = get_pln(dt)
			t_desc += len(dt)
			tam_c['abstract/extract'] = len(dt)
			get_indexer(x,'recordNum','abstract/extract',dt)
			id[x['recordNum']] = tam_c.copy()
			tam_c.clear()
	avg['title'] = t_title/n	
	avg['authors'] = t_auth/n
	avg['majorSubjects'] = t_mS/n
	avg['minorSubjects'] = t_miS/n
	avg['abstract/extract'] = t_desc/n	
	indexer['tam_c'] = id.copy()	
	indexer['avg']	= avg.copy()
	indexer['M'] = n	
	with open('indices/cf_indexer.dat', 'wb') as f:
		pickle.dump(indexer, f, pickle.HIGHEST_PROTOCOL)	

		
