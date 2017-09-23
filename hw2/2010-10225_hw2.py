import nltk
from nltk.corpus import brown
from pprint import pprint


# 15
def occur_at_least_three():
    brown_words = brown.words()
    result = [word for (word, count) in dict(nltk.FreqDist(brown_words)).items() if count > 3]
    return result


# 16
def lexical_diversity_genres():
    genres = brown.categories()
    print('{:16}'.format('Category'), end=' ')
    print('{:>20}'.format('Lexical diversity'))
    for genre in genres:
        words = brown.words(categories=[genre])
        num_words = len(words)
        num_vocab = len(set(w.lower() for w in words))
        lexical_diversity = num_words/num_vocab
        print('{:16}'.format(genre), end=' ')
        print('{:20}'.format(lexical_diversity))


# 17
def most_50_words_without_stopwords():
    brown_words = brown.words()
    stopwords = nltk.corpus.stopwords.words('english')
    lowercased_words = [w.lower() for w in brown_words if w.isalpha()]
    fdist = nltk.FreqDist(word for word in lowercased_words if word not in stopwords)
    return fdist.most_common(50)


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


# 19
def genre_and_words():
    genres = ['news', 'government', 'religion', 'romance']
    words = ['president', 'government', 'party', 'power',
             'love', 'faith', 'happy', 'race',
             'family', 'war']
    cfd = nltk.ConditionalFreqDist(
        (genre, word)
        for genre in genres
        for word in brown.words(categories=genre)
    )
    cfd.tabulate(conditions=genres, samples=words)


# 20
def word_freq(word, section):
    corpus = brown.words(categories=section)
    fdist = nltk.FreqDist(corpus)
    return fdist[word]


# 22
def hedge(corpus):
    with open('BrownHedgeOut.txt', 'w') as f:
        word_list = list(corpus)
        for i in range(3, int(len(word_list)+len(word_list)/3)):
            if (i-3) % 4 == 0:
                word_list.insert(i, 'like')
        modified = ' '.join(word_list)
        f.write(modified)
        f.close()


def main():
    print("# 15")
    pprint(occur_at_least_three())
    print()

    print("# 16")
    lexical_diversity_genres()
    print()

    print("# 17")
    pprint(most_50_words_without_stopwords())
    print()

    print("# 18")
    pprint(most_50_bigrams_without_stopwords())
    print()

    print("# 19")
    genre_and_words()
    print()
    print('''
    FINDING:
    Brown corpus의 category들 중에서 news, government, religion, romance로 한정해서 살펴보았다.
    news category에서는 president, government, party, family가 많이 등장하였다. 
    government category에서도 president, government가 많이 등장했으나 news에 비해서 party는 거의 등장하지 않았고, 또한 family도 거의 등장하지 않았다.
    president, government, power는 news와 government category에서 공통적으로 많이 등장하는 단어이지만,
    party, race, family가 많이 등장하는지의 여부로 두 장르를 구별해볼 수 있다.   
    religion category의 경우 power와 faith라는 단어가 다른 장르들에 비해서 두드러지게 많이 등장하였다. 
    romance category에서는 love가 다른 카테고리들에 비해 가장 많이 등장하여서 특징적으로 많이 등장한 단어라고 할 수 있다.
    ''')

    print("# 20")
    print("'new' appears %d times in the 'news' category of Brown corpus" % word_freq('new', 'news'))
    print()

    print("# 22")
    hedge(brown.words(fileids=['ca01']))
    print()


if __name__ == '__main__':
    main()

