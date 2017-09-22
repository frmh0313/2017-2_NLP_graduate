import nltk
from nltk.corpus import brown
from pprint import pprint

brown_words = brown.words()
#15
def occur_at_least_three():
    # brown_words = list(brown.words(fileids=['ca01']))
    result = [word for (word, count) in dict(nltk.FreqDist(brown_words)).items() if count > 3]
    return result

pprint(occur_at_least_three())

#16

#17
'''
TODO
조교 문의 -> preprocess한 걸로 해야되는지, 아니면 그냥 brown corpus에서 바로 가져온 것으로 해야하는지 
'''
# preprocessed
def most_50_excluding_stopwords_preprocessed():
    stopwords = nltk.corpus.stopwords.words('english')
    lowercased_words = [w.lower() for w in brown_words if w.isalpha()]
    fdist = nltk.FreqDist(word for word in lowercased_words if word not in stopwords)
    return fdist.most_common(50)
'''
def most_50_excluding_stopwords():
    stopwords = nltk.corpus.stopwords.words('english')
    fdist = nltk.FreqDist(word for word in brown_words if word.lower() not in stopwords)
    return fdist.most_common(50)
'''
# print(most_50_excluding_stopwords())
pprint(most_50_excluding_stopwords_preprocessed())


#18
def most_50_bigrams_without_stopwords():
    stopwords = nltk.corpus.stopwords.words('english')
    bigrams = list(nltk.bigrams(brown))
    bigrams_without_stopwords = [(b1, b2)
                                 for (b1, b2) in bigrams
                                 if b1.lower() not in stopwords
                                 and b2.lower() not in stopwords]
    fdist = nltk.FreqDist(bigrams_without_stopwords)
    return fdist.most_common(50)

pprint(most_50_bigrams_without_stopwords())

#19



