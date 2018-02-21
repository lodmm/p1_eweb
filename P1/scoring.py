import argparse
import json
import matplotlib.pyplot as plt
import numpy as np
import os.path

def getPrecisionAndRecallCurve(idealDocuments, obtainedDocuments):
	precision = []
	recall = []
	precisionAndRecall = []

	hits = 0
	for i in range(len(obtainedDocuments)):
		if obtainedDocuments[i] in idealDocuments:
			hits += 1
		prec = hits/(i+1)
		rec = hits/len(idealDocuments)
		precision.append(prec)
		recall.append(rec)
		precisionAndRecall.append([prec, rec])
	avgPrecision = 0
	avgRecall = 0
	try:
		avgPrecision = hits/len(obtainedDocuments)
		avgRecall = hits/len(idealDocuments)
	except ZeroDivisionError as e:
		pass
	return avgPrecision, avgRecall, getStandard11Point(precisionAndRecall)


def getStandard11Point(precisionAndRecall):

	precisionAndRecall.sort(key=lambda x:x[1])
	standard11Point = []
	for i in range(11):
		point = next((x for [x,y] in precisionAndRecall if y >= i/10), None)
		if not point:
			point = 0
		standard11Point.append(point)

	return standard11Point


def getF1(precision, recall):
	f1 = 0
	try:
		f1 = 2*(precision*recall)/(precision+recall)
	except ZeroDivisionError as e:
		return 0
	return f1




# Processing arguments
parser = argparse.ArgumentParser(description="scoring search engine")
parser.add_argument("-c", choices=["moocs", "cf"], help="corpus", required=True)
parser.add_argument("-o", help="obtained documents file path", required=True)
args = parser.parse_args()

if not os.path.isfile(args.o):
	parser.exit("There is no file in that path.")

idealFile = json.load(open("corpora/" + args.c + "/json/qrels.json"))
obtainedFile = json.load(open(args.o))


f1 = []
totalStandard11Point = []
for i in range(len(idealFile)):
	idealResults = idealFile[i]["relevantDocs"]
	obtainedResults = obtainedFile[i]["relevantDocs"]
	precision, recall, standard11Point = getPrecisionAndRecallCurve(idealResults, obtainedResults)
	f1.append(getF1(precision, recall))
	totalStandard11Point.append(standard11Point)


avgStandard11Point = np.sum(totalStandard11Point, axis=0)/len(totalStandard11Point)

plt.plot(np.arange(0,1.1,0.1), avgStandard11Point, marker="o")
plt.xlabel("Recall")
plt.ylabel("Precision")
plt.ylim(0.0,1.0)
plt.grid(True)
plt.title(args.c)
filename = ""
while(True):
	filename = input("Write a name for the PNG file (without extension) of the Standard 11 Point chart: ")
	filename = filename + ".png"
	if os.path.isfile(filename):
		print("This file already exists")
	else:
		break

plt.savefig(filename, bbox_inches="tight")
plt.clf()


plt.bar(range(len(obtainedFile)), f1)
plt.axhline(np.mean(f1), color="red", linewidth=1)
plt.xlabel("Query ID")
plt.ylabel("F1")
plt.grid(True)
plt.title(args.c)
#plt.show()
filename = ""
while(True):
	filename = input("Write a name for the PNG file (without extension) of the f1 chart: ")
	filename = filename + ".png"
	if os.path.isfile(filename):
		print("This file already exists")
	else:
		break

plt.savefig(filename, bbox_inches="tight")