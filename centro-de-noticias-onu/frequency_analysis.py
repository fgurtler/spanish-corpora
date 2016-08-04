import nltk.data
import re
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import treetaggerwrapper

article_corpus = PlaintextCorpusReader('text_plain/', '.*\.txt', 
	sent_tokenizer=nltk.data.LazyLoader('tokenizers/punkt/spanish.pickle'))

stop_words = nltk.corpus.stopwords.words('spanish') 
non_alphabetic = re.compile("\W|\d")
words = []
tags = []

# Using TreeTagger 
# 1) pip install treetaggerwrapper
# 2) put treetragger in %PYHOME%\Lib\site-packages\TreeTagger
# 3) put spanish-utf8.par and spanish-chunker.par in \TreeTagger\lib
# See http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/spanish-tagset.txt for tag meanings
tagger = treetaggerwrapper.TreeTagger(TAGLANG='es')
for sentence in article_corpus.sents():
	tagged_sentence = tagger.tag_text(sentence) 
	tags.extend(treetaggerwrapper.make_tags(tagged_sentence))

#TODO: create a tagger script, save the tagged files
#TODO: look at alternate taggers, compare

#TODO: profile this and see which part is taking so long
for tag in tags:
	lemma = tag[2].lower()
	if lemma not in stop_words and not non_alphabetic.search(lemma):
		words.append(lemma)

freq_dist = FreqDist(words)

with open('./frequency_distribution.txt', 'w', encoding='utf-8') as f:
	f.write("word, number of occurences\n")
	for word in freq_dist.most_common():
		f.write(word[0] + ", " + str(word[1]) + "\n")