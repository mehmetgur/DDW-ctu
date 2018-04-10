from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np


def check(vectorize, corpus, query, num, type, top_num=100, x=True):
	corpus.append(query)
	matrix = vectorize.fit_transform(corpus)
	sim_cosine = np.array(cosine_similarity(matrix[len(corpus) - 1], matrix[0:(len(corpus) - 1)])[0])
	sim_euc = np.array(euclidean_distances(matrix[len(corpus) - 1], matrix[0:(len(corpus) - 1)])[0])
	top_cosine = sim_cosine.argsort()[-min(top_num, len(sim_cosine)):][::-1] + 1
	top_euc = sim_euc.argsort()[-min(top_num, len(sim_cosine)):][::-1] + 1

	corpus.pop(len(corpus) - 1)

	if x:
		print("   ", type)
		print("Querry ", str(num))
		print("Top", str(top_num))
		print("Cosine\n", top_cosine)
		print("Euclidian\n", top_euc)

	return top_cosine, top_euc

def eval(results, cos, euc, cos_bin, euc_bin, type, x=False):
	cos_truePos = 0
	euc_truePos = 0
	bin_cos_true = 0
	bin_euc_true = 0

	for i in cos:
		if i+1 in results:
			cos_truePos += 1

	for i in euc:
		if i+1 in results:
			euc_truePos += 1

	for i in cos_bin:
		if i in results:
			bin_cos_true += 1

	for i in euc_bin:
		if i in results:
			bin_euc_true += 1

	cos_pre = cos_truePos/len(cos)
	cos_rec = cos_truePos/len(results)
	cos_f = 0
	try:
		cos_f = (2 * cos_pre * cos_rec)/(cos_pre + cos_rec)
	except:
		pass


	euc_pre = euc_truePos/(len(euc))
	euc_rec = euc_truePos/len(results)
	euc_f = 0
	try:
		euc_f = (2 * euc_pre * euc_rec)/(euc_rec + euc_pre)
	except:
		pass

	cos_bin_pre = bin_euc_true / (len(cos_bin))
	cos_bin_rec = bin_euc_true / len(results)
	cos_bin_f = 0
	try:
		cos_bin_f = (2 * cos_bin_pre * cos_bin_rec) / (cos_bin_rec + cos_bin_pre)
	except:
		pass

	euc_bin_pre = bin_euc_true / (len(euc_bin))
	euc_bin_rec = bin_euc_true / len(results)
	euc_bin_f = 0
	try:
		euc_bin_f = (2 * euc_bin_pre * euc_bin_rec) / (euc_bin_rec + euc_bin_pre)
	except:
		pass

	d = {
		"cosine_pre": cos_pre,
		"cosine_rec": cos_rec,
		"cosine_f": cos_f,
		"euclid_pre": euc_pre,
		"euclid_rec": euc_rec,
		"euclid_f": euc_f,
		"cos_bin_pre": cos_bin_pre,
		"cos_bin_rec": cos_bin_rec,
		"cos_bin_f" : cos_bin_f,
		"euc_bin_pre": euc_bin_pre,
		"euc_bin_rec": euc_bin_rec,
		"euc_bin_f" : euc_bin_f
	}

	if x:
		print("    ", type, " Evaluation \n")
		print("Cosine")
		print("Presission : ", cos_pre)
		print("Recall : ", cos_rec)
		print("F-measure : ", cos_f, "\n")

		print("Euclidian")
		print("Presission : ", euc_pre)
		print("Recall : ", euc_rec)
		print("F-measure : ", euc_f, "\n")

	return d


corpus = []
queries = []
results = []
for d in range(1400):
	f = open("./d/" + str(d + 1) + ".txt")
	corpus.append(f.read())

for q in range(225):
	f = open("./q/" + str(q + 1) + ".txt")
	g = open("./r/" + str(q + 1) + ".txt")
	queries.append(f.read())
	results.append(g.read())

results = [r.split("\n") for r in results]
print(results[0])
for i in range(len(results)):
	for j in range(len(results[i])-1):
		k = results[i][j]
		try:results[i][j] = int(k)
		except:print(k, len(k))


tfidf_vectorize = TfidfVectorizer()
tfidf_vectorize_binary = TfidfVectorizer(binary=True)
puretf_vectorize = CountVectorizer()
puretf_vectorize_binary = CountVectorizer(binary=True)

# TF-IDF
tfidf_cosine = []
tfidf_cosine_bin = []
tfidf_euc = []
tfidf_euc_bin = []
print("   Starting TF-IDF...   ")
for i in range(len(queries)):
	cos, euc = check(tfidf_vectorize, corpus, queries[i], i+1, "TF-IDF", top_num=10, x=False)
	bin_cos, bin_euc = check(tfidf_vectorize_binary, corpus, queries[i], i+1, "TF-IDF", top_num=10, x=False)
	tfidf_cosine.append(cos)
	tfidf_euc.append(euc)
	tfidf_cosine_bin.append(bin_cos)
	tfidf_euc_bin.append(bin_euc)
print("   Ended...   ")


print("   Starting Pure TF...   ")
# Pure TF
pure_cosine = []
pure_euc = []
pure_cosine_bin = []
pure_euc_bin = []
for i in range(len(queries)):
	cos, euc = check(puretf_vectorize, corpus, queries[i], i+1, "Pure TF", top_num=10, x=False)
	bin_cos, bin_euc = check(puretf_vectorize, corpus, queries[i], i+1, "Pure TF Binary", top_num=1000, x=False)
	pure_cosine.append(cos)
	pure_euc.append(euc)
	pure_cosine_bin.append(bin_cos)
	pure_euc_bin.append(bin_cos)

print("  Ended...  ")

# BinaryTerm
tfidf_cosine = []
tfidf_cosine_bin = []
tfidf_euc = []
tfidf_euc_bin = []
print("   Starting BinaryTerm...  ")
for i in range(len(queries)):
	cos, euc = check(tfidf_vectorize, corpus, queries[i], i+1, "BinaryTerm", top_num=10, x=False)
	bin_cos, bin_euc = check(tfidf_vectorize_binary, corpus, queries[i], i+1, "BinaryTerm", top_num=10, x=False)
	tfidf_cosine.append(cos)
	tfidf_euc.append(euc)
	tfidf_cosine_bin.append(bin_cos)
	tfidf_euc_bin.append(bin_euc)
print("    Ended...   ")

# Eval
res_cos = []
res_euc = []
print(tfidf_cosine[0])
print(tfidf_cosine_bin[0])
print(tfidf_euc[0])
print(results[0])
print("   Starting eval TF-IDF...   ")
ev_tfidf = []
for i in range(len(tfidf_cosine)):
	ev_tfidf.append(eval(results[i], tfidf_cosine[i], tfidf_euc[i], tfidf_cosine_bin[i], tfidf_euc_bin[i], "TF-IDF", x=False))
print("   Ended...   ")
print("   Starting eval PureTF...  ")
ev_puretf = []
for i in range(len(pure_cosine)):
	ev_puretf.append(eval(results[i], pure_cosine[i], pure_euc[i], pure_cosine_bin[i], pure_euc_bin[i], "PureTF", x=False))
print("   Ended...   ")
print("   Starting eval BinaryTerm...   ")
ev_binTerm = []
for i in range(len(pure_cosine)):
	ev_binTerm.append(eval(results[i], tfidf_cosine[i], tfidf_euc[i], tfidf_cosine_bin[i], tfidf_euc_bin[i], "BinaryTerm", x=False))
print("   Ended...   ")
print("TF-IDF")
for i in range(len(ev_tfidf)):
	s = str(i+1) + " : "
	for k, v in ev_tfidf[i].items():
		s += "\n   " + str(k) + " : " + str(v)
	print(s)
print("PureTF")
for i in range(len(ev_puretf)):
	s = str(i + 1) + " : "
	for k, v in ev_puretf[i].items():
		s += "\n   " + str(k) + " : " + str(v)
	print(s)
print("BinaryTerm")
for i in range(len(ev_tfidf)):
    s = str(i + 1) + " : "
    for k, v in ev_tfidf[i].items():
        s += "\n   " + str(k) + " : " + str(v)
    print(s)


