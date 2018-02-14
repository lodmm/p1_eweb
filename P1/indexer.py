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

moocs='.\corpora\moocs\json\moocs.json'
cf=[".\corpora\cf\json\cf74.json", ".\corpora\cf\json\cf75.json", ".\corpora\cf\json\cf76.json", ".\corpora\cf\json\cf77.json", ".\corpora\cf\json\cf78.json", ".\corpora\cf\json\cf79.json"]
dict = dict()
id = {}
data = {}
jcf = []
str3 =""
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
			if y not in dict:
				id[x["courseID"]] = 1
				dict[y] = id.copy()	
			else:
				data = dict.get(y)
				if x["courseID"] in data:
					data[x["courseID"]] = data.get(x["courseID"]) +1
				else:
					data[x["courseID"]] = 1
				dict[y] = data.copy()	
				
		id.clear()
		data.clear()	
	with open('.\indices\moocs_indexer.dat', 'w') as outfile:
		json.dump(dict.sort(), outfile)
elif (sys.argv[1]+" "+sys.argv[2] ) == "-c cf" :
	# indexer for cf
	for c in cf:
		jcf = json.loads(open(c).read())
		for x in jcf:
			str2= x["minorSubjects"] 
			str1 = x.get('majorSubjects')
			str3 = ' '.join(str3)
			str =  ' '.join(str2)
			dt = tknzr.tokenize( x["abstract/extract"] + x["title"] + str + str3)
			dt = [i for i in dt if i not in stop]	
			for y in dt:
				if y not in dict:
					id[x["paperNum"]] = 1
					dict[y] = id.copy()	
				else:
					data = dict.get(y)
					if x["paperNum"] in data:
						data[x["paperNum"]] = data.get(x["paperNum"]) +1
					else:
						data[x["paperNum"]] = 1
					dict[y] = data.copy()	
					
		id.clear()
		data.clear()	
	with open('.\indices\cf_indexer.dat', 'w') as outfile:
		json.dump(dict, outfile)	
else:
	print ("Error: introduce a valid corpus, indexer -c [moocs|cf]")
	sys.exit(1)
		
