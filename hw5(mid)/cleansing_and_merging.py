import glob
import re

if __name__ == '__main__':
    files = glob.glob('./brown_200_tagged/ca01')
    w = open('./brown_200_tagged_merged', 'w')
    for file in files:
        f = open(file, 'r')
        string = f.read()
        w.write(string)
        f.close()
    w.close()

    merged_file = open('./brown_200_tagged_merged', 'r')
    modified = open('./result_ca01', 'w')

    string = merged_file.read()
    string = re.sub('\t', '<s>/<s> ', string)
    string = re.sub('\n+', ' ', string)
    string = re.sub(' +', ' ', string)
    word_tokens = string.strip().split(' ')

    out = []

    for token in word_tokens:
        try:
            binary_pattern = re.compile('.+/.+')
            triary_pattern = re.compile('.+/.+/.+')
            if triary_pattern.match(token) is not None:
                (word1, word2, pos) = token.split('/')
                print word1, word2, pos
                out.append(word1 + '/' + word2 + '_' + pos)
            elif binary_pattern.match(token) is not None:
                (word, pos) = token.split('/')
                print word, pos
                out.append(word + '_' + pos)
        except ValueError as e:
            print("==================================")
            print(token)
            print(e)
            print("==================================")

    modified.write(' '.join(out))