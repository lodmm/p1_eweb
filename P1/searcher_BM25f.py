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
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer




def processingQuery(query): # AQUÍ NO HAY QUE MODIFICAR NADA (EXCEPTO CUANDO AÑADAMOS EL DICCIONARIO DE SIGLAS Y ACRÓNIMOS)

	# Obtaining tokens from query
	tokenizer = RegexpTokenizer(r'\w+')
	tokens = tokenizer.tokenize(query)

	# Stemming words (stripping sufixes)
	wordsStemmed = []
	ps = PorterStemmer()

	for w in tokens:
		wordsStemmed.append(ps.stem(w))

	# Removing stopwords
	stopWords = set(stopwords.words("english"))
	wordsFiltered = []
 	
	for w in wordsStemmed:
	    if w not in stopWords:
	        wordsFiltered.append(w)

	return wordsFiltered




def getRelevantDocs(queryTokens, corpus): # AQUÍ NO HAY QUE MODIFICAR NADA

	# Reading index json file with pickle library
	path = ""
	if corpus == "moocs":
		path = "indices/moocs_indexer.dat"
	elif corpus == "cf":
		path = "indices/cf_indexer.dat"
	with open(path, 'rb') as f:
         index = pickle.load(f)

	# Obtaining relevant documents from index file (here we have a dictionary)
	relevantDocs = {}

	for token in queryTokens:
		if token in index:
			relevantDocs[token] = index[token]

	return relevantDocs, index["M"], index["tam_c"], index["avg"]



def singleQuery(query, corpus):

	# Obtaining relevant words (tokens) from query
	processedQuery = processingQuery(query)

	# Obtaining relevant documents from each token (dictionary)
	relevantDocuments, M, corpusSize, avgCorpusSize = getRelevantDocs(set(processedQuery), corpus)

	if not relevantDocuments:
		# There isn't any relevant document for the query
		return relevantDocuments
	else:
		# Calculating relevance score
		scoredDocuments = {}
		for key,value in relevantDocuments.items():

			# Calculating documentary frequency for that word in corpus
			df = len(value)

			for documentID,documentData in value.items():
				absc = corpusSize[documentID]
				# Calculating idf
				idf = math.log10((M + 1)/df)
				# Calculating tff
				tff = 0
				if corpus == "cf":
					# Cf corpus
					if "title" in documentData:
						tff += (weightsCf["title"]*documentData["title"]/((1-b)+b*absc["title"]/avgCorpusSize["title"]))
					if "authors" in documentData:
						tff += (weightsCf["authors"]*documentData["authors"]/((1-b)+b*absc["authors"]/avgCorpusSize["authors"]))
					if "minorSubjects" in documentData:
						tff += (weightsCf["minorSubjects"]*documentData["minorSubjects"]/((1-b)+b*absc["minorSubjects"]/avgCorpusSize["minorSubjects"]))
					if "majorSubjects" in documentData:
						tff += (weightsCf["majorSubjects"]*documentData["majorSubjects"]/((1-b)+b*absc["majorSubjects"]/avgCorpusSize["majorSubjects"]))
					if "abstract/extract" in documentData:
						tff += (weightsCf["abstract/extract"]*documentData["abstract/extract"]/((1-b)+b*absc["abstract/extract"]/avgCorpusSize["abstract/extract"]))
				else:
					# Moocs corpus
					if "title" in documentData:
						tff += (weightsCf["title"]*documentData["title"]/((1-b)+b*absc["title"]/avgCorpusSize["title"]))
					if "description" in documentData:
						tff += (weightsCf["description"]*documentData["description"]/((1-b)+b*absc["description"]/avgCorpusSize["description"]))
				# Calculating score
				score = processedQuery.count(key)*(k+1)*tff*idf/(k+tff)
				# Updating score of document
				if documentID in scoredDocuments:
					lastScore = scoredDocuments[documentID]
					scoredDocuments[documentID] = lastScore + score
				else:
					scoredDocuments[documentID] = score

		# Obtaining documents over a threshold (percentage)
		# Should be optimized over a metric
		# Threshold (percentage)
		# Threshold (fixed value, e.g. maximizing f1)
		maximum = 0
		for d,s in scoredDocuments.items():
			if s > maximum:
				maximum = s
		threshold = maximum*0.4

		selectedDocuments = {}
		for d,s in scoredDocuments.items():
			if s >= threshold:
				selectedDocuments[d] = s
				

		# Ordering documents by importance
		return sorted(selectedDocuments, key=selectedDocuments.__getitem__, reverse=True)




def getDocumentsName(corpus, documents): # AQUÍ NO HAY QUE MODIFICAR NADA
	if corpus == "cf":
		cf74 = json.load(open("corpora/cf/json/cf74.json")) # 1 <= recordNum <= 167 (74001 - 74168 paperNum)
		cf75 = json.load(open("corpora/cf/json/cf75.json")) # 168 <= recordNum <= 355 (75001 - 75189 paperNum)
		cf76 = json.load(open("corpora/cf/json/cf76.json")) # 356 <= recordNum <= 582 (76001 - 76229 paperNum)
		cf77 = json.load(open("corpora/cf/json/cf77.json")) # 583 <= recordNum <= 781 (77001 - 77200 paperNum)
		cf78 = json.load(open("corpora/cf/json/cf78.json")) # 782 <= recordNum <= 980 (78001 - 78200 paperNum)
		cf79 = json.load(open("corpora/cf/json/cf79.json")) # 981 <= recordNum <= 1239 (79001 - 79259 paperNum)

		docsWithNames = {}
		for doc in documents:
			if 1 <= doc <= 167:
			#if 74001 <= doc <= 74168:
				docsWithNames[doc] = cf74[doc-1]["title"]
			elif 168 <= doc <= 355:
			#elif 75001 <= doc <= 75189:
				docsWithNames[doc] = cf75[doc-168]["title"]
			elif 356 <= doc <= 582:
			#elif 76001 <= doc <= 76229:
				docsWithNames[doc] = cf76[doc-356]["title"]
			elif 583 <= doc <= 781:
			#elif 77001 <= doc <= 77200:
				docsWithNames[doc] = cf77[doc-583]["title"]
			elif 782 <= doc <= 980:
			#elif 78001 <= doc <= 78200:
				docsWithNames[doc] = cf78[doc-782]["title"]
			elif 981 <= doc <= 1239:
			#elif 79001 <= doc <= 79259:
				docsWithNames[doc] = cf79[doc-981]["title"]

		return docsWithNames


	elif corpus == "moocs":
		moocs = json.load(open("corpora/moocs/json/moocs.json"))

		docsWithNames = {}
		for doc in documents:
			docsWithNames[doc] = moocs[doc]["title"]

		return docsWithNames



# A PARTIR DE AQUÍ NO HAY QUE MODIFICAR NADA
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

if corpus == "cf":
	if not os.path.isfile("indices/cf_indexer.dat"):
		parser.exit(message="\nCf index file does not exist. Please execute indexer.py before searcher.py\n")
else:
	if not os.path.isfile("indices/moocs_indexer.dat"):
		parser.exit(message="\nMoocs index file does not exist. Please execute indexer.py before searcher.py\n")




weightsMoocs = {
	"title" : 0.5,
	"description" : 0.5
}

weightsCf = {
	"title" : 0.2,
	"authors" : 0.2,
	"minorSubjects" : 0.2,
	"majorSubjects" : 0.2,
	"abstract/extract" : 0.2
}

k = 2 # Valores típicos: 2 o 1.2
b = 0.75


# We are in query mode, where user introduced a query by command line
if query != "f":
	
	resultDocs = singleQuery(query, corpus)
	if not resultDocs:
		print("There isn't any relevant document for this query.")
	else:
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
		resultDocs = singleQuery(query["queryText"], corpus)
		queriesResult.append({"queryID":query["queryID"],"relevantDocs":resultDocs})

	# Writing json to results file
	file = open(resultsFile, "w+")
	resultJson = json.dumps(queriesResult, indent=4)
	file.write(resultJson)
	file.close()