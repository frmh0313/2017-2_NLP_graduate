import re, nltk
from nltk import word_tokenize

f = open('BROWN_A1.txt')
raw = f.read()
tokens = word_tokenize(raw)
words = [w.lower() for w in tokens]
lemmatizer = nltk.WordNetLemmatizer()
lemmatized_words = [lemmatizer.lemmatize(word) for word in words]

wh_words_re = re.compile(r'^((who)|(when)|(where)|(what)|(how)|(why)|(which)|(whose)|(whom))$')

wh_words = sorted(set([w for w in lemmatized_words if bool(wh_words_re.match(w)) is True]))
for w in wh_words:
    print(w)


print('''
모든 단어를 소문자로 만들고, NLTK의 Lemmatizer를 이용해서 lemmatize하고, 
찾을 때에도 wh-word와 정확히 일치하는 것만을 찾았으며,
이것을 다시 sorted set으로 처리했기 때문에 
case distinctions나 punctuation 때문에 중복된 것이 나타나지는 않음.
''')
