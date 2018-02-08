# indexer

import sys
import json
import nltk
import collections

from collections import Counter
from nltk.tokenize import TweetTokenizer
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
# nltk.download('stopwords')
stop = stopwords.words('english') + list(string.punctuation)
tknzr = TweetTokenizer(preserve_case=False,reduce_len=True,strip_handles=True)

indexer = list()
num = []
moocs='.\corpora\moocs\json\moocs.json'
cf=[".\corpora\cf\json\cf74.json", ".\corpora\cf\json\cf75.json", ".\corpora\cf\json\cf76.json", ".\corpora\cf\json\cf77.json", ".\corpora\cf\json\cf78.json", ".\corpora\cf\json\cf79.json"]
cnt = Counter()
data = []
f = list()
jcf = []
d_list = list()
if len(sys.argv) != 3:
	print ("Error: missing corpus, indexer -c [moocs|cf]")
	sys.exit(1)
if (sys.argv[1]+" "+sys.argv[2]) == "-c moocs" :
	# indexer for moocs
	jmoocs = json.loads(open(moocs).read())
	# print (len(jmoocs))
	for x in jmoocs:
		dt = tknzr.tokenize(x["description"] + x["title"])
		dt = [i for i in dt if i not in stop]
		# print (len(dt))
		for y in dt:
			cnt[y] +=1
			if y not in d_list:
				d_list.append(y)
				
		for y in d_list :
			doc_id=([x["courseID"],cnt[y]])
			if y not in f:
				f.append(y)
				data.append({
				'word':y,
				'docs': [
				[x["courseID"],cnt[y]]
				]
				})
			else:
				for w in data:
					if w['word'] == y:
						w['docs'].append([x["courseID"],cnt[y]])		
		cnt.clear()
		d_list.clear()
				
	with open('.\indices\moocs_indexer.dat', 'w') as outfile:
		json.dump(data, outfile)
elif (sys.argv[1]+" "+sys.argv[2] ) == "-c cf" :
	# indexer for cf
	for c in cf:
		jcf += json.loads(open(c).read())
	
	for x in jcf:
		dt = tknzr.tokenize( x["abstract/extract"] )
		dt = [i for i in dt if i not in stop]	
		
		for y in dt:
			cnt[y] +=1
			if y not in d_list:
				d_list.append(y)	
		for y in d_list :
			if y not in f:
				f.append(y)
				data.append({
				'word':y,
				'docs': [
				[x["paperNum"],cnt[y]]
				]
				})
			else:
				#get the w in data for word=y
				
				for w in data:
					if w['word'] == y:
						w['docs'].append([x["paperNum"],cnt[y]])		
		cnt.clear
		d_list.clear()
	print(data)	
else:
	print ("Error: introduce a valid corpus, indexer -c [moocs|cf]")
	sys.exit(1)
		
