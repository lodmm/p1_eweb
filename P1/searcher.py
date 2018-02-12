# This program will parse a query inserted by CLI and present a series of results according to the specified corpus and query

# 1. Query processing (and expansion) -> q
# 2. Obtaining potentially relevant documents
# 3. For each document, calculate relevance score
# 4. Ordered list of documents that exceed a threshold
# 5. Return "Answer set"

import argparse
import json
import math
import os.path
import pickle
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords




def processingQuery(query):

	# Obtaining tokens from query
	tokenizer = RegexpTokenizer(r'\w+')
	tokens = tokenizer.tokenize(query)
	
	# Removing stopwords
	stopWords = set(stopwords.words("english"))
	wordsFiltered = []
 
	for w in tokens:
	    if w not in stopWords:
	        wordsFiltered.append(w)

	
	# Stemming words (stripping sufixes)
	wordsStemmed = []
	ps = PorterStemmer()

	for w in wordsFiltered:
		wordsStemmed.append(ps.stem(w))

	return wordsStemmed




def getRelevantDocs(queryTokens):

	# Reading index json file with pickle library
	with open('index/index.pkl', 'rb') as f:
         index = pickle.load(f)

	# Obtaining relevant documents from index file (here we have a dictionary)
	relevantDocs = {}

	for token in queryTokens:
		if token in index:
			relevantDocs[token] = index[token]

	#print("Finished getting relevant documents...")
	return relevantDocs



def singleQuery(query):

	# Obtaining relevant words (tokens) from query
	processedQuery = processingQuery(query)

	# Obtaining relevant documents from each token (dictionary)
	relevantDocuments = getRelevantDocs(set(processedQuery))

	if not relevantDocuments:
		# There aren't any relevant documents for the query
		pass
	else:
		# Calculating relevance score
		scoredDocuments = {}
		for key,value in relevantDocuments.items():

			# Calculating documentary frequency for that word in corpus
			df = len(value)

			for document in value:

				documentID = document[0]
				numOfWords = document[1]
				score = numOfWords*processedQuery.count(key)*math.log10((1239 + 1)/df)
				# Updating score for document
				if documentID in scoredDocuments:
					lastScore = scoredDocuments[documentID]
					scoredDocuments[documentID] = lastScore + score
				else:
					scoredDocuments[documentID] = score

		# Obtaining documents over a threshold (arithmetic average)
		total = 0
		for d,s in scoredDocuments.items():
			total = total + s
		threshold = total/len(scoredDocuments)

		selectedDocuments = {}
		for d,s in scoredDocuments.items():
			if s >= threshold:
				selectedDocuments[d] = s
				

		# Ordering documents by importance
		return sorted(selectedDocuments, key=selectedDocuments.__getitem__, reverse=True)




def getDocumentsName(corpus, documents):
	if corpus == "cf":
		cf74 = json.load(open("corpora/cf/json/cf74.json")) # 1 <= recordNum <= 167
		cf75 = json.load(open("corpora/cf/json/cf75.json")) # 168 <= recordNum <= 355
		cf76 = json.load(open("corpora/cf/json/cf76.json")) # 356 <= recordNum <= 582
		cf77 = json.load(open("corpora/cf/json/cf77.json")) # 583 <= recordNum <= 781
		cf78 = json.load(open("corpora/cf/json/cf78.json")) # 782 <= recordNum <= 980
		cf79 = json.load(open("corpora/cf/json/cf79.json")) # 981 <= recordNum <= 1239

		docsWithNames = {}
		for doc in documents:
			if 1 <= doc <= 167:
				docsWithNames[doc] = cf74[doc-1]["title"]
			elif 168 <= doc <= 355:
				docsWithNames[doc] = cf74[doc-168]["title"]
			elif 356 <= doc <= 582:
				docsWithNames[doc] = cf74[doc-356]["title"]
			elif 583 <= doc <= 781:
				docsWithNames[doc] = cf74[doc-583]["title"]
			elif 782 <= doc <= 980:
				docsWithNames[doc] = cf74[doc-782]["title"]
			elif 981 <= doc <= 1239:
				docsWithNames[doc] = cf74[doc-981]["title"]

		return docsWithNames


	elif corpus == "moocs":
		moocs = json.load(open("corpora/moocs/json/moocs.json"))

		docsWithNames = {}
		for doc in documents:
			docsWithNames[doc] = moocs[doc]["title"]

		return docsWithNames




# Processing arguments
parser = argparse.ArgumentParser(description="search engine")
parser.add_argument("-c", choices=["moocs", "cf"], help="select corpus", required=True)
group_q = parser.add_argument_group("query", "processing only one query inserted as parameter")
group_q.add_argument("-q", help="query to be processed", default="f")
group_rf = parser.add_argument_group("batch", "processing queries from file specified in the path (default: corpus directory)")
group_rf.add_argument("-qf", help="path to queries file", default="default")
group_rf.add_argument("-rf", help="path to results file", default="f")

args = parser.parse_args()

corpus = args.c
query = args.q
queryFile = args.qf
resultsFile = args.rf

if query != "f" and resultsFile != "f":
	parser.exit(message="\nOnly one of the modes can be invoked:\n\nquery mode (-q query)\nbatch mode ([-rf path] -qf path)\n")

if query == "f" and resultsFile == "f":
	parser.exit(message="\nAt lease one mode must be specified:\n\nquery mode (-q query)\nbatch mode ([-rf path] -qf path)\n")

if not os.path.isfile("index/index.json"):
	parser.exit(message="\nIndex file does not exist. Please execute indexer.py before searcher.py\n")




# We are in query mode, where user introduced a query by command line
if query != "f":
	
	resultDocs = singleQuery(query)
	totalResults = len(resultDocs)

	# Get name of all relevant docs
	if len(resultDocs) > 10:
		resultDocs = resultDocs[:11]
	docsWithNames = getDocumentsName(corpus, resultDocs)
	
	# Print relevant docs (document identifier, title, and at the end the number of relevant docs obtained)
	for identifier in resultDocs:
		print(identifier, " - ", docsWithNames[identifier])

	print("\n", totalResults, " results")





# We are in batch mode, where we have to process a queries file
elif queryFile != "f":

	# Reading queries file
	if queryFile == "default":
		queryFile = "corpora/" + corpus + "/json/queries.json"

	if os.path.isfile(queryFile):
		queries = json.load(open(queryFile))
	else:
		parser.exit(message="\nQueries file does not exist: " + queryFile)

	# For each query in file, we get the relevant document ids
	queriesResult = []
	for query in queries:
		resultDocs = singleQuery(query)
		queriesResult.append({"queryID":query["queryID"],"relevantDocs":resultDocs})

	# Writing json to results file
	file = open(resultsFile, "r+")
	resultJson = json.dumps(queriesResult, indent=4)
	file.write(resultJson)
	file.close()