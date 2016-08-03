import nltk.data
import re
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.probability import FreqDist
from nltk.corpus import stopwords

article_corpus = PlaintextCorpusReader('plain_text/', '.*\.txt')
stop_words = nltk.corpus.stopwords.words('spanish') 
non_alphabetic = re.compile("\W|\d")
words = []

#TODO: profile this and see which part is taking 40+ seconds
for word in article_corpus.words():
	word = word.lower()
	if word not in stop_words and not non_alphabetic.search(word):
		words.append(word)

#TODO: part of speech tagging
#TODO: POS specific stemming (dicho (V) => decir), (dicho (N) => dicho)

freq_dist = FreqDist(words)

with open('./frequency_distribution.txt', 'w', encoding='utf-8') as f:
	f.write("word, number of occurences\n")
	for word in freq_dist.most_common():
		f.write(word[0] + ", " + str(word[1]) + "\n")