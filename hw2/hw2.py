import nltk
from nltk.corpus import brown
from pprint import pprint


# 15
def occur_at_least_three():
    # brown_words = list(brown.words(fileids=['ca01']))
    brown_words = brown.words()
    result = [word for (word, count) in dict(nltk.FreqDist(brown_words)).items() if count > 3]
    return result


pprint(occur_at_least_three())


# 16
def lexical_diversity_genres():
    genres = brown.categories()
    print('{:16}'.format('Category'), end= ' ')
    print('{:>20}'.format('Lexical diversity'))
    for genre in genres:
        words = brown.words(categories=[genre])
        num_words = len(words)
        num_vocab = len(set(w.lower() for w in words))
        lexical_diversity = num_words/num_vocab
        print('{:16}'.format(genre), end=' ')
        print('{:20}'.format(lexical_diversity))


lexical_diversity_genres()

# TODO
# 조교 문의 -> preprocess한 걸로 해야되는지, 아니면 그냥 brown corpus에서 바로 가져온 것으로 해야하는지


# 17
# preprocessed
def most_50_excluding_stopwords_preprocessed():
    brown_words = brown.words()
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


# 18
def most_50_bigrams_without_stopwords():
    stopwords = nltk.corpus.stopwords.words('english')
    bigrams = list(nltk.bigrams(brown.words()))
    bigrams_without_stopwords = [(b1, b2)
                                 for (b1, b2) in bigrams
                                 if b1.lower() not in stopwords
                                 and b2.lower() not in stopwords]
    fdist = nltk.FreqDist(bigrams_without_stopwords)
    return fdist.most_common(50)


pprint(most_50_bigrams_without_stopwords())

# 19


# 20
def word_freq(word, section):
    corpus = brown.words(categories=section)
    fdist = nltk.FreqDist(corpus)
    return fdist[word]


print("'new' appears %d times in the 'news' category of Brown corpus" % word_freq('new', 'news'))


# string input?
# 22
def hedge(text):
    l = text.split(' ')
    for i in range(3, int(len(l)+len(l)/3)):
        if (i-3)%4 == 0:
            l.insert(i, 'like')
    return ' '.join(l)


text = "Define a function hedge(text) which processes a text and produces a new version with the word 'like' between every third word."

print(hedge(text))
