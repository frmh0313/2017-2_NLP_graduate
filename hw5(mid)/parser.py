if __name__ == '__main__':
    import glob
    import re
    files = glob.glob("./brown_200_tagged/*")
    w = open('./brown_200_tag_modified_merged', 'w')

    for file in files:
        f = open(file, 'r')
        file_split_for_name = file.split('/')
        filename = file_split_for_name[len(file_split_for_name)-1]

        # w = open('./brown_200_tagged_modified/'+filename, 'w')
        # w = open('./brown_200_tagged_modified2/'+filename, 'w')
        out = []
        string = f.read()
        string = re.sub('\t', '<s>/<s> ', string)
        string = re.sub('\n+', ' ', string)
        string = re.sub(' +', ' ', string)
        word_tokens = string.strip().split(' ')

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

        w.write(' '.join(out))
