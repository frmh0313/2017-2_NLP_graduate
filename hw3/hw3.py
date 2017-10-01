# -*- coding: utf-8 -*-
import hangul_decoder_modified
import math
import re

INITIAL_JAMO = hangul_decoder_modified.INITIAL_JAMO.values()
MED_JAMO = hangul_decoder_modified.MID_JAMO.values()
#deleted u"none" and the syllables included in INITIAL_JAMO
FINAL_JAMO = [ u"ㄳ", u"ㄵ", u"ㄶ", u"ㄺ", u"ㄻ", u"ㄼ", u"ㄽ", u"ㄾ", u"ㄿ", u"ㅀ", u"ㅄ"]
JAMO = []
JAMO.extend(INITIAL_JAMO)
JAMO.extend(MED_JAMO)
JAMO.extend(FINAL_JAMO)


def unigram_decoder(string):
    result = []
    blank_removed = string.replace(' ', '').replace('\n', '')

    for character in blank_removed:
        result.extend(hangul_decoder_modified.decodeSyllable(character))
    return result


def bigram_generator(string):
    unigrams = unigram_decoder(string)
    bigrams = []
    for i in range(len(unigrams) - 1):
        if i == 0:
            bigrams.append(('<s>', unigrams[i]))
            bigrams.append((unigrams[i], unigrams[i+1]))
        elif i == len(unigrams) -1 :
            bigrams.append((unigrams[i], '</s>'))
        else:
            single_bigram = (unigrams[i], unigrams[i+1])
            if single_bigram not in bigrams:
                bigrams.append(single_bigram)
    return bigrams


def counter(test_decoded, training_decoded):
    total_count = len(test_decoded)
    counts = {}
    for char in test_decoded:
        if char in training_decoded:
            counts[char] = counts[char] + 1 if char in counts.keys() else 1
        else: # test set에는 있지만 training set에는 들어있지 않은 단어의 경우 '<UNK>'로 처리하여 test counter dict에 저장.
            counts['<UNK>'] = counts['<UNK>'] + 1 if '<UNK>' in counts.keys() else 1
    return total_count, counts


def entropy(total_count, jamo_counts):
    result = 0
    for jamo in jamo_counts:
        probability = jamo_counts[jamo]/total_count
        result += -probability * math.log2(probability)
    return result


def cross_entropy(training_total_count, training_counts, test_total_count, test_counts):
    result = 0
    training_probabilities = {key: float(training_counts[key])/training_total_count for key in training_counts.keys()}
    test_probabilities = {key: float(test_counts[key])/test_total_count for key in test_counts.keys()}

    # key_list = training_counts.keys() # key list of training_counts and test_counts are same.
    # TODO when there are characters which is in test corpus, but not in training corpus/ or vice versa?
    """
    @ Test corpus에는 들어있지만 training corpus에 들어있지 않은 경우 -> 그냥 0이 더해짐.
    @ Training corpus에는 들어있지만 test corpus에는 들어있지 않은 경우 -> 
    """

    for key in test_counts.keys():
        if key in training_counts.keys():
            result += -test_probabilities[key] * math.log2(training_probabilities[key])
        else:
            result += -test_probabilities['<UNK>'] * math.log2(training_probabilities[key])

    return result


if __name__ == '__main__':
    # 자소 모델
    training_raw = ""
    test_raw = ""
    hani_raw = ""
    with open('./sejong.nov.train.txt', 'r', encoding='utf8') as f:
        training_raw = f.read()
    with open('./sejong.nov.test.txt', 'r', encoding='utf8') as f:
        test_raw = f.read()
    with open('./hani.test.txt', 'r', encoding='utf8') as f:
        hani_raw = f.read()

    with open('./out.txt', 'w', encoding='utf8') as f:
        print("training unigram")
        training_unigram_decoded = unigram_decoder(training_raw)
        f.write("training unigram decoded: " + str(training_unigram_decoded))
        training_unigram_counted = counter(test_decoded=training_unigram_decoded, training_decoded=training_unigram_decoded)
        f.write("training unigram counted: " + str(training_unigram_counted))
        training_unigram_entropy = entropy(*training_unigram_counted)
        f.write("training unigram entropy: " + str(training_unigram_entropy))
        training_unigram_cross_entropy = cross_entropy(*training_unigram_counted, *training_unigram_counted)
        f.write("training unigram cross entropy: " + str(training_unigram_entropy))

        print("training bigram")
        training_bigram_decoded = bigram_generator(training_raw)
        f.write("training bigram decoded: " + str(training_bigram_decoded))
        training_bigram_counted = counter(test_decoded=training_bigram_decoded, training_decoded=training_bigram_decoded)
        f.write("training bigram counted: " + str(training_bigram_counted))
        training_bigram_entropy = entropy(*training_bigram_counted)
        f.write("training bigram entropy: " + str(training_bigram_entropy))
        training_bigram_cross_entropy = cross_entropy(*training_bigram_counted,
                                                      *training_bigram_counted)
        f.write("training bigram cross entropy: " + str(training_bigram_cross_entropy))

        print("test unigram")
        test_unigram_decoded = unigram_decoder(test_raw)
        f.write("test unigram decoded: " + str(test_unigram_decoded))
        test_unigram_counted = counter(test_decoded=test_unigram_decoded, training_decoded=training_unigram_decoded)
        f.write("test unigram counted: " + str(test_unigram_counted))
        test_unigram_entropy = entropy(*test_unigram_counted)
        f.write("test unigram entropy: " + str(test_unigram_entropy))
        test_unigram_cross_entropy = cross_entropy(*training_unigram_counted,
                                                   *test_unigram_counted)
        f.write("test unigram cross entropy: " + str(test_unigram_cross_entropy))

        print("test bigram")
        test_bigram_decoded = bigram_generator(test_raw)
        f.write("test bigram decoded: " + str(test_bigram_decoded))
        test_bigram_counted = counter(test_decoded=test_bigram_decoded, training_decoded=training_bigram_decoded)
        f.write("test bigram counted: " + str(test_bigram_counted))
        test_bigram_entropy = entropy(*test_bigram_counted)
        f.write("test bigram entropy: " + str(test_bigram_entropy))
        test_bigram_cross_entropy = cross_entropy(*training_bigram_counted,
                                                  *test_bigram_counted)
        f.write("test bigram cross entropy: " + str(test_bigram_cross_entropy))

        print("hani test unigram")
        hani_test_unigram_decoded = unigram_decoder(hani_raw)
        f.write("hani unigram decoded: " + str(hani_test_unigram_decoded))
        hani_test_unigram_counted = counter(test_decoded=hani_test_unigram_decoded, training_decoded=training_unigram_decoded)
        f.write("hani unigram counted: " + str(hani_test_unigram_counted))
        hani_test_unigram_entropy = entropy(*hani_test_unigram_counted)
        f.write("hani unigram entropy: " + str(hani_test_unigram_entropy))
        hani_test_unigram_cross_entropy = cross_entropy(*training_unigram_counted,
                                                        *hani_test_unigram_counted)
        f.write("hani unigram cross entropy: " + str(hani_test_unigram_cross_entropy))
        hani_test_bigram_decoded = bigram_generator(hani_raw)
        print("hani test bigram")
        f.write("hani bigram decoded: " + str(hani_test_bigram_decoded))
        hani_test_bigram_counted = counter(test_decoded=hani_test_bigram_decoded, training_decoded=training_bigram_decoded)
        f.write("hani bigram counted: " + str(hani_test_bigram_counted))
        hani_test_bigram_entropy = entropy(*hani_test_unigram_counted)
        f.write("hani bigram entropy: " + str(hani_test_bigram_entropy))
        hani_test_bigram_cross_entropy = cross_entropy(*training_bigram_counted,
                                                       *hani_test_bigram_counted)
        f.write("hani bigram cross entropy: " + str(hani_test_bigram_cross_entropy))

    # 음절별 모델

