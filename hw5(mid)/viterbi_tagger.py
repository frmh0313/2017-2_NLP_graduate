import nltk
import glob
import numpy as np
import sys
import re
import itertools
if __name__ == '__main__':
    print("VITERBI TAGGER TAGGING")
    # files = glob.glob('./brown_200_tagged/*')
    if len(sys.argv) > 2:
        files = glob.glob(sys.argv[1])
        test_file = sys.argv[2]
    elif len(sys.argv) > 1:
        print >> sys.stderr, 'No test file!\n'
    else:
        print >> sys.stderr, 'Usage: viterbi_tagger.py <training_files> <test_file>'
    # files = glob.glob('./training_samples_3/*')
    # files = glob.glob('./training_samples_10/*')
    word_list = []
    tag_list = []
    string = ''
    for file in files:
        f = open(file, 'r')
        string += f.read()
        f.close()

    string = re.sub(r'\n{2,3}', r'\n', string)

    sentences = string.split('\n')

    # print('filtering')
    list_of_sentences = []
    non_empty_sentences = filter(None, sentences)
    for sentence in non_empty_sentences:
        list_of_sentences.append(sentence.split())

    # print('tagging start and end')
    for line in list_of_sentences:
        try:
            if line[len(line)-1] != '<end>/<end>':
                line.insert(len(line), '<end>/<end>')
            line.insert(0, '<start>/<start>')
        except IndexError as e:
            print(e)

    merged_words = list(itertools.chain(*list_of_sentences))

    word_tag_fdist = nltk.FreqDist(merged_words)

    # print('split word and tag')
    for line in list_of_sentences:
        for element in line:
            word_tag_pair = element.split('/')
            if len(word_tag_pair) == 2:
                (word, tag) = word_tag_pair
                if word != '<start>' and word != '<end>':
                    word_list.append(word)
                tag_list.append(tag)
            elif len(word_tag_pair) == 3:
                (word, tag) = (word_tag_pair[0] + '/' + word_tag_pair[1], word_tag_pair[2])
                word_list.append(word)
                tag_list.append(tag)

    word_fdist = nltk.FreqDist(word_list)
    tag_fdist = nltk.FreqDist(tag_list)

    unique_word_list = list(set(word_list))
    unique_tag_list = list(set(tag_list))
    unique_tag_list.remove('<start>')
    unique_tag_list.remove('<end>')
    unique_tag_list.insert(0, '<start>')
    unique_tag_list.insert(len(unique_tag_list), '<end>')

    tag_bigrams = []
    for line in list_of_sentences:
        tags = []
        for element in line:
            word_tag_pair = element.split('/')
            if len(word_tag_pair) == 2:
                tag = word_tag_pair[1]
                tags.append(tag)
            elif len(word_tag_pair) == 3:
                tag = word_tag_pair[2]
                tags.append(tag)
            else:
                print >> sys.stderr, 'Ill formed word/tag pair', element
        tag_bigrams.extend(nltk.bigrams(tags))

    tag_bigram_fdist = nltk.FreqDist(tag_bigrams)


    # Computing tag transition probabilities
    # print('Computing tag transition probability')
    tag_transition_probability = {}
    for i in range(len(unique_tag_list)):
        for j in range(len(unique_tag_list)):
            tag1 = unique_tag_list[i]
            tag2 = unique_tag_list[j]
            tag1_count = tag_fdist[tag1]
            tag1_tag2_count = tag_bigram_fdist[(tag1, tag2)]
            tag_transition_probability[(tag1, tag2)] = float(tag1_tag2_count)/tag1_count

    # Computing observation likelihoods
    # print('Computing observation likelihoods')
    observation_likelihoods = {}
    for tag in unique_tag_list:
        for word in unique_word_list:
            tag_count = tag_fdist[tag]
            word_tag_count = word_tag_fdist[word+'/'+tag]
            observation_likelihoods[(word, tag)] = float(word_tag_count)/tag_count

    test_file = open('./ca01_raw.txt', 'r')
    test_string = test_file.read()
    test_string = re.sub(r'\n{2,3}', r'\n', test_string)
    test_sentences = test_string.split('\n')

    list_test_sentences = []
    non_empty_test_sentences = filter(None, test_sentences)

    for line in non_empty_test_sentences:
        list_test_sentences.append(line.split())

    for line in list_test_sentences:
        if line[len(line)-1] != '<end>':
            line.insert(len(line), '<end>')
        line.insert(0, '<start>')


    # Viterbi Algorithm
    output = open('./viterbi_result.txt', 'w')
    for line in list_test_sentences:
        N = len(unique_tag_list)
        T = len(line) - 2
        viterbi = np.zeros((N+2, T+1))
        viterbi[0, 0] = 1.0
        backpointer = []

        # initialization step
        for s in range(1, N+1):
            try:
                from_tag = '<start>'
                to_tag = unique_tag_list[s-1]
                p_tag_transition = tag_transition_probability[(from_tag, to_tag)]
            except KeyError as e:
                print('KeyError in tag transition of Init step: ', e)
                p_tag_transition = 0
            try:
                p_observation = observation_likelihoods[(line[1], unique_tag_list[s-1])]
            except KeyError as e:
                print('KeyError in observation likelihoods of Init step: ', e)
                p_observation = 0
            try:
                viterbi[s, 1] = p_tag_transition * p_observation
            except IndexError as e:
                print('IndexError in assigning viterbi: ', line)

        # recursion step
        for t in range(2, T+1):
            for s in range(1, N+1):
                viterbi_candidate = []
                for i in range(1, N+1):
                    try:
                        from_tag = unique_tag_list[i-1]
                        to_tag = unique_tag_list[s-1]
                        p_tag_transition = tag_transition_probability[(from_tag, to_tag)]
                    except KeyError as e:
                        print('KeyError in tag transition of recursion step: ', e)
                        p_tag_transition = 0
                    try:
                        observed_word = line[t]
                        observed_tag = unique_tag_list[s-1]
                        p_observation = observation_likelihoods[(observed_word, observed_tag)]
                    except KeyError as e:
                        print('KeyError in observation likelihoods of recursion step: ', e)
                        p_observation = 0
                    multiply = viterbi[i, t-1] * p_tag_transition * p_observation
                    viterbi_candidate.append(multiply)
                viterbi[s, t] = max(viterbi_candidate)

        for t in range(1, T+1):
            viterbi_column = viterbi[:, t]
            argmax = np.argmax(viterbi_column)
            backpointer.append(argmax)

        result_tags = [unique_tag_list[i-1] for i in backpointer]
        tagged = []
        for i, j in zip(range(1, len(line)-1), backpointer):
            tagged.append(line[i] + '/' + unique_tag_list[j-1])
        tagged_sentence = ' '.join(tagged) + '\n'
        # print('tagged: ', tagged_sentence)
        output.write(tagged_sentence)
    output.close()
