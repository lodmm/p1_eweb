import argparse
import json
import matplotlib.pyplot as plt
import numpy as np
import os.path
import math
import operator

def get_g(m):
	media = 1
	num = 0
	s=0
	for i in m:
		if i!= 0:
			if num != 0:
				media *= i
				s+=1
		num+=1			
	media = media **(1/s)
	return media

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
	
def gain_10(g,m):
	result = []
	if len(g) >=m:
		result = g[:m]
	else:
		result = g
		while len(g)< m:
			if len(g) != 0:
				result.append(g[len(g)-1])
			else:
				result.append(0)
	return result

def getStandard11Point(precisionAndRecall):
	precisionAndRecall.sort(key=lambda x:x[1])
	standard11Point = []
	for i in range(11):
		recallList = (x for [x,y] in precisionAndRecall if y >= i/10)
		point = 0
		try:
			point = max(recallList)
		except Exception as e:
			pass
		standard11Point.append(point)

	return standard11Point

def getF1(precision, recall):
	f1 = 0
	try:
		f1 = 2*(precision*recall)/(precision+recall)
	except ZeroDivisionError as e:
		return 0
	return f1

def get_map(prec,s11point):
	prec = 0
	num = 0
	hits = 0
	ap = 0
	num = 0
	for i in s11point:
		if num != 0:
			ap += i
		num+=1	
	media = ap/10		
	return media
	 
def get_pan(idealResults,obtainedResults,precision):
	pan = 0
	p = dict()
	num = 0
	hits = 0
	if len(obtainedResults) >= 5:
		obtR = obtainedResults[:5]
		for i in obtR:
			if i in idealResults:
				hits +=1
		try:
			pan = hits/5
			p['5']= pan	
		except ZeroDivisionError as e:
			pan = 0	
			p['5']= pan		
	else:
		for i in obtainedResults:
			if i in idealResults:
				hits +=1
		try:
			p['5'] = hits/len(obtainedResults)
		except ZeroDivisionError as e:
			pan = 0	
			p['5']= pan		
	pan = 0	
	hits= 0
	if	len(obtainedResults) >= 10:
		obtR = obtainedResults[:10]
		for i in obtR:
			if i in idealResults:
				hits +=1
		try:
			pan = hits/10
			p['10']= pan	
		except ZeroDivisionError as e:
			pan = 0	
			p['10']= pan	
	else:
		for i in obtainedResults:
			if i in idealResults:
				hits +=1
		try:
			p['10'] = hits/len(obtainedResults)
		except ZeroDivisionError as e:
			pan = 0	
			p['10']= pan		
	pan = 0	
	hits= 0
	if len(obtainedResults) >= 15:
		obtR = obtainedResults[:15]
		for i in obtR:
			if i in idealResults:
				hits +=1
		try:
			pan = hits/15
			p['15']= pan	
		except ZeroDivisionError as e:
			pan = 0	
			p['15']= pan	
	else:
		for i in obtainedResults:
			if i in idealResults:
				hits +=1
		try:
			p['15'] = hits/len(obtainedResults)
		except ZeroDivisionError as e:
			pan = 0	
			p['15']= pan		
	pan = 0
	hits= 0
	if len(obtainedResults) >= 20:
		obtR = obtainedResults[:20]
		for i in obtR:
			if i in idealResults:
				hits +=1
		try:
			pan = hits/20
			p['20']= pan	
		except ZeroDivisionError as e:
			pan = 0	
			p['20']= pan	
	else:
		for i in obtainedResults:
			if i in idealResults:
				hits +=1
		try:
			p['20'] = hits/len(obtainedResults)
		except ZeroDivisionError as e:
			pan = 0	
			p['20']= pan	
	pan = 0
	hits= 0	
	if len(obtainedResults) >= 25:
		obtR = obtainedResults[:25]
		for i in obtR:
			if i in idealResults:
				hits +=1
		try:
			pan = hits/25
			p['25']= pan	
		except ZeroDivisionError as e:
			pan = 0	
			p['25']= pan	
	else:
		for i in obtainedResults:
			if i in idealResults:
				hits +=1
		try:
			p['25'] = hits/len(obtainedResults)
		except ZeroDivisionError as e:
			pan = 0	
			p['25']= pan		
	pan = 0	
	hits= 0		
	return p


	return	
	
def get_rprecision(idealResults,obtainedResults,refFiles):
	hits = 0
	if	len(obtainedResults) >= 20:
		obtR = obtainedResults[:20]
		for i in obtR:
			if i in idealResults:
				hits +=1
		try:
			rpa = hits/20
				
		except ZeroDivisionError as e:
			rpa = 0	
					
	else:
		while len(obtainedResults)<20:
			if  len(obtainedResults) != 0:
				obtainedResults.append(obtainedResults[len(obtainedResults)-1])
			else:
				obtainedResults.append(0)
		for i in obtainedResults:
			if i in idealResults:
				hits +=1
		try:
			rpa = hits/len(obtainedResults)
					
		except ZeroDivisionError as e:
			rpa = 0	
	hits= 0	
	if	len(refFiles) >= 20:
		obtR = refFiles[:20]
		for i in obtR:
			if i in idealResults:
				hits +=1
		try:
			rpb = hits/20
					
		except ZeroDivisionError as e:
			rpb = 0	
					
	else:
		while len(refFiles)<20:
			if len(refFiles) != 0:
				refFiles.append(refFiles[len(refFiles)-1])
			else:
				refFiles.append(0)
		for i in refFiles:
			if i in idealResults:
				hits +=1
		try:
			rpb = hits/len(refFiles)
				
		except ZeroDivisionError as e:
			rpb = 0		
	Rt = rpa-rpb
	return Rt

def get_mrr(idealResults,obtainedResults):
	hits = 0
	num = 0
	shold = 100
	r = 0
	for i in obtainedResults:
		num += 1
		if i in idealResults:
			break
	if num <= shold:
		try:
			r = 1/num
		except ZeroDivisionError as e:
			pass
	else:
		r = 0

	return r
	
def get_multilevel(idealResults,obtainedResults,id,maxi):
	gain_c = []
	gain_dc = []
	pos = 0
	scored = dict()
	num = 0
	gain_vr = dict()
	ri = 0
	aux = dict
	if args.c == 'cf':
		scoredResults = json.load(open("corpora/" + args.c + "/json/qscoredrels.json"))
		for i in scoredResults:
			if i['queryID'] == id:
				for y in i['relevantDocs']:
					relevance = y['relevance']
					ri = int(relevance[0]) + int(relevance[1]) + int(relevance[2]) + int(relevance[3])
					gain_vr[y['relevantDoc']]= ri
				break		
	else:
		tam=len(idealResults)/3
		for i in idealResults:
			if num <= tam:
				gain_vr[i] = 3
			elif num <= 2*tam:
				gain_vr[i] = 2
			elif num <=3*tam:
				gain_vr[i] = 1
			num+=1	
	for i in obtainedResults:
		if i in idealResults:
			if pos != 0:
				gain_c.append(gain_c[pos-1]+gain_vr[i])
				gain_dc.append(gain_dc[pos-1] + (gain_vr[i]/math.log(pos+1,2)))
			else:
				gain_c.append(gain_vr[i])
				gain_dc.append(gain_vr[i])
		else:
			if pos!=0:
				gain_c.append(gain_c[pos-1])
				gain_dc.append(gain_dc[pos-1])
			else:
				gain_c.append(0)
				gain_dc.append(0)
		pos+=1					
	return gain_10(gain_c,maxi),gain_10(gain_dc,maxi)
def get_multilevel_ideal(idealResults,ObtainedResults,id,maxi):
	gain_vr = dict()
	gain_c = []
	gain_dc = []
	num = 0
	if args.c == 'cf':
		scoredResults = json.load(open("corpora/" + args.c + "/json/qscoredrels.json"))
		for i in scoredResults:
			if i['queryID'] == id:
				for y in i['relevantDocs']:
					relevance = y['relevance']
					ri = int(relevance[0]) + int(relevance[1]) + int(relevance[2]) + int(relevance[3])
					gain_vr[y['relevantDoc']]= ri
				break
				
	else:
		tam=len(obtainedResults)/3
		for i in idealResults:
			if num <= tam:
				gain_vr[i] = 3
			elif num <= 2*tam:
				gain_vr[i] = 2
			elif num <=3*tam:
				gain_vr[i] = 1
			num+=1	
	id = sorted(gain_vr.items(), key=operator.itemgetter(1),reverse=True)	
	list = []
	for i in id:
		q = i[0]
		list.append(q)
	pos = 0	
	for i in list:	
		if pos != 0:
			gain_c.append(gain_c[pos-1]+gain_vr[i])
			gain_dc.append(gain_dc[pos-1]+(gain_vr[i]/math.log(pos+1,2)))
		else:
			gain_c.append(gain_vr[i])
			gain_dc.append(gain_vr[i])
		pos+=1			
	return gain_10(gain_c,maxi),gain_10(gain_dc,maxi)
	
# Processing arguments
parser = argparse.ArgumentParser(description="scoring search engine")
parser.add_argument("-c", choices=["moocs", "cf"], help="corpus", required=True)
parser.add_argument("-o", help="obtained documents file path", required=True)
args = parser.parse_args()


if not os.path.isfile(args.o):
	parser.exit("There is no file in that path.")


idealFile = json.load(open("corpora/" + args.c + "/json/qrels.json"))
obtainedFile = json.load(open(args.o))
pFiles = json.load(open("./" + args.c + "_ref_qresults.json"))
f1 = []
rt_l = []
mr_l = []
totalStandard11Point = []
map_m = []
pan5_m = 0
pan10_m =0
pan15_m = 0
pan20_m = 0
pan25_m = 0
r_m = 0
maxi_l=0
maxi = 0
i_q = []
i_dq = []
c_q = []
dc_q = []
p_5 = []
p_10 = []
p_15 = []
p_20 = []
p_25 = []
for i in obtainedFile:
	if len(i['relevantDocs'])>maxi:
		maxi = len(i['relevantDocs'])
for i in idealFile:
	if len(i['relevantDocs'])>maxi:
		maxi_l = len(i['relevantDocs'])
for i in range(len(idealFile)):
	idealResults = idealFile[i]["relevantDocs"]
	obtainedResults = obtainedFile[i]["relevantDocs"]
	refFiles = pFiles[i]["relevantDocs"]
	precision, recall, standard11Point = getPrecisionAndRecallCurve(idealResults, obtainedResults)
	f1.append(getF1(precision, recall))
	totalStandard11Point.append(standard11Point)
	ap = get_map(precision,standard11Point)
	map_m.append(ap)
	p = get_pan(idealResults,obtainedResults,precision)
	pan5_m = p.get('5',0)
	p_5.append(pan5_m*100)
	pan10_m = p.get('10',0)
	p_10.append(pan10_m*100)
	pan15_m = p.get('15',0)
	p_15.append(pan15_m*100)
	pan20_m = p.get('20',0)
	p_20.append(pan20_m*100)
	pan25_m = p.get('25',0)
	p_25.append(pan25_m*100)
	r = get_rprecision(idealResults,obtainedResults,refFiles)
	rt_l.append(r)
	mr = get_mrr(idealResults,obtainedResults)
	mr_l.append(mr)
	gain_c, gain_dc = get_multilevel(idealResults,obtainedResults,obtainedFile[i]['queryID'],maxi)
	c_q.append(gain_c)
	dc_q.append(gain_dc)
	gain_i,gain_id= get_multilevel_ideal(idealResults,obtainedResults,idealFile[i]['queryID'],maxi)
	i_q.append(gain_i)
	i_dq.append(gain_id)
	

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
plt.clf()

plt.bar(range(len(obtainedFile)), map_m)
plt.axhline(np.mean(map_m), color="red", linewidth=1)
plt.xlabel("Query ID")
plt.ylabel("MAP")
plt.grid(True)
plt.title(args.c)
#plt.show()
filename = ""
while(True):
	filename = input("Write a name for the PNG file (without extension) of the MAP chart: ")
	filename = filename + ".png"
	if os.path.isfile(filename):
		print("This file already exists")
	else:
		break

plt.savefig(filename, bbox_inches="tight")
plt.clf()
gmap = get_g(map_m)
print(gmap)
plt.bar(range(len(obtainedFile)), map_m)
plt.axhline(gmap, color="red", linewidth=1)
plt.xlabel("Query ID")
plt.ylabel("MAP")
plt.grid(True)
plt.title(args.c)
#plt.show()
filename = ""
while(True):
	filename = input("Write a name for the PNG file (without extension) of the GMAP chart: ")
	filename = filename + ".png"
	if os.path.isfile(filename):
		print("This file already exists")
	else:
		break

plt.savefig(filename, bbox_inches="tight")
plt.clf()

plt.bar(range(len(obtainedFile)), rt_l)
plt.xlabel("Query ID")
plt.ylabel("20-Precision")
plt.grid(True)
plt.title(args.c)
#plt.show()
filename = ""
while(True):
	filename = input("Write a name for the PNG file (without extension) of the 10-Precision chart: ")
	filename = filename + ".png"
	if os.path.isfile(filename):
		print("This file already exists")
	else:
		break

plt.savefig(filename, bbox_inches="tight")
plt.clf()

plt.bar(range(len(obtainedFile)), mr_l)
plt.axhline(np.mean(mr_l), color="red", linewidth=1)
plt.xlabel("Query ID")
plt.ylabel("Mean Reciprocal Rank")
plt.grid(True)
plt.title(args.c)
# plt.show()
filename = ""
while(True):
	filename = input("Write a name for the PNG file (without extension) of the Multi Reciprocal Rank chart: ")
	filename = filename + ".png"
	if os.path.isfile(filename):
		print("This file already exists")
	else:
		break
plt.savefig(filename, bbox_inches="tight")
plt.clf()

plt.bar(range(len(obtainedFile)), p_5)
plt.axhline(np.mean(p_5), color="red", linewidth=1)
plt.xlabel("Query ID")
plt.ylabel("P@5%")
plt.grid(True)
plt.title(args.c)
filename = ""
while(True):
	filename = input("Write a name for the PNG file (without extension) of the P@5 chart: ")
	filename = filename + ".png"
	if os.path.isfile(filename):
		print("This file already exists")
	else:
		break

plt.savefig(filename, bbox_inches="tight")
plt.clf()

plt.bar(range(len(obtainedFile)), p_10)
plt.axhline(np.mean(p_10), color="red", linewidth=1)
plt.xlabel("Query ID")
plt.ylabel("P@10%")
plt.grid(True)
plt.title(args.c)
filename = ""
while(True):
	filename = input("Write a name for the PNG file (without extension) of the P@10 chart: ")
	filename = filename + ".png"
	if os.path.isfile(filename):
		print("This file already exists")
	else:
		break

plt.savefig(filename, bbox_inches="tight")
plt.clf()
plt.bar(range(len(obtainedFile)), p_15)
plt.axhline(np.mean(p_15), color="red", linewidth=1)
plt.xlabel("Query ID")
plt.ylabel("P@15%")
plt.grid(True)
plt.title(args.c)
filename = ""
while(True):
	filename = input("Write a name for the PNG file (without extension) of the P@15 chart: ")
	filename = filename + ".png"
	if os.path.isfile(filename):
		print("This file already exists")
	else:
		break

plt.savefig(filename, bbox_inches="tight")
plt.clf()
plt.bar(range(len(obtainedFile)), p_20)
plt.axhline(np.mean(p_20), color="red", linewidth=1)
plt.xlabel("Query ID")
plt.ylabel("P@20%")
plt.grid(True)
plt.title(args.c)
filename = ""
while(True):
	filename = input("Write a name for the PNG file (without extension) of the P@20 chart: ")
	filename = filename + ".png"
	if os.path.isfile(filename):
		print("This file already exists")
	else:
		break

plt.savefig(filename, bbox_inches="tight")
plt.clf()
plt.bar(range(len(obtainedFile)), p_25)
plt.axhline(np.mean(p_25), color="red", linewidth=1)
plt.xlabel("Query ID")
plt.ylabel("P@25%")
plt.grid(True)
plt.title(args.c)
filename = ""
while(True):
	filename = input("Write a name for the PNG file (without extension) of the P@25 chart: ")
	filename = filename + ".png"
	if os.path.isfile(filename):
		print("This file already exists")
	else:
		break

plt.savefig(filename, bbox_inches="tight")
plt.clf()

plt.bar(range(len(obtainedFile)), p_5, color = 'yellow',label='P@5%')
plt.axhline(np.mean(p_5), color="yellow", linewidth=3)
plt.bar(range(len(obtainedFile)), p_10, color = 'black',label='P@10%')
plt.axhline(np.mean(p_10), color="black", linewidth=3)
plt.bar(range(len(obtainedFile)), p_15, color = 'green',label='P@15%')
plt.axhline(np.mean(p_15), color="green", linewidth=3)
plt.bar(range(len(obtainedFile)), p_20, color = 'pink',label='P@20%')
plt.axhline(np.mean(p_20), color="pink", linewidth=3)
plt.bar(range(len(obtainedFile)), p_25, color = 'blue',label='P@25%')
plt.axhline(np.mean(p_25), color="blue", linewidth=3)
plt.legend(loc=1)
plt.xlabel("Query ID")
plt.ylabel("P@n")
plt.grid(True)
plt.title(args.c)
filename = ""
while(True):
	filename = input("Write a name for the PNG file (without extension) of the P@n chart: ")
	filename = filename + ".png"
	if os.path.isfile(filename):
		print("This file already exists")
	else:
		break

plt.savefig(filename, bbox_inches="tight")
plt.clf()

c = np.sum(c_q, axis=0)/len(c_q)
d = np.sum(dc_q,axis=0)/len(dc_q)		
ic = np.sum(i_q, axis=0)/len(i_q)
idc = np.sum(i_dq, axis=0)/len(i_dq)


plt.plot( c, marker='^',color='green',label='CG')
plt.plot(d,marker='o',color='blue',label='DCG')
plt.plot( ic, marker='x',color='pink',label='IdealCG')
plt.plot(idc,marker='*',color='black',label='IdealDCG')

plt.legend(loc=1)
plt.xlabel("Query ID")
plt.ylabel("Multilevel relevance evaluation")
plt.grid(True)
plt.title(args.c)
filename = ""
while(True):
	filename = input("Write a name for the PNG file (without extension) of the Multilevel relevance evaluation chart: ")
	filename = filename + ".png"
	if os.path.isfile(filename):
		print("This file already exists")
	else:
		break

plt.savefig(filename, bbox_inches="tight")
plt.clf()

ci = c/ic
di = d/idc

plt.plot( ci, marker='x',color='pink',label='NCG')
plt.plot(di,marker='o',color='green',label='NDCG')
plt.legend(loc=1)
plt.xlabel("Query ID")
plt.ylabel("NMRE")
plt.grid(True)
plt.title(args.c)
filename = ""
while(True):
	filename = input("Write a name for the PNG file (without extension) of the Normalized Multilevel relevance evaluation chart: ")
	filename = filename + ".png"
	if os.path.isfile(filename):
		print("This file already exists")
	else:
		break

plt.savefig(filename, bbox_inches="tight")



