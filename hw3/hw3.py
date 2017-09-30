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


def counter(decoded_list):
    total_count = len(decoded_list)
    jamo_count = {}
    for char in decoded_list:
        jamo_count[char] = jamo_count[char] + 1 if char in jamo_count.keys() else 1
    return total_count, jamo_count


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
    # when there are characters which is in test corpus, but not in training corpus/ or vice versa?

    for key in test_counts.keys():
        result += -test_probabilities[key] * math.log2(training_probabilities[key])

    return result


if __name__ == '__main__':
    training_raw = ""
    test_raw = ""
    hani_raw = ""
    with open('./sejong.nov.train.txt', 'r', encoding='utf8') as f:
        training_raw = f.read()
    with open('./sejong.nov.test.txt', 'r', encoding='utf8') as f:
        test_raw = f.read()
    with open('./hani.test.txt', 'r', encoding='utf8') as f:
        hani_raw = f.read()

    # with open('./out.txt', 'w') as f:
    training_unigram_decoded = unigram_decoder(training_raw)
    print("training unigram decoded:", training_unigram_decoded)
    training_unigram_counted = counter(training_unigram_decoded)
    print("training unigram counted:", training_unigram_counted)
    training_unigram_entropy = entropy(*training_unigram_counted)
    print("training unigram entropy:", training_unigram_entropy)
    training_unigram_cross_entropy = cross_entropy(*training_unigram_counted, *training_unigram_counted)
    print("training unigram cross entropy:", training_unigram_entropy)

    training_bigram_decoded = bigram_generator(training_raw)
    print("training bigram decoded:", training_bigram_decoded)
    training_bigram_counted = counter(training_bigram_decoded)
    print("training bigram counted:", training_bigram_counted)
    training_bigram_entropy = entropy(*training_bigram_counted)
    print("training bigram entropy:", training_bigram_entropy)
    training_bigram_cross_entropy = cross_entropy(*training_bigram_counted,
                                                  *training_bigram_counted)
    print("training bigram cross entropy:", training_bigram_cross_entropy)

    test_unigram_decoded = unigram_decoder(test_raw)
    print("test unigram decoded:", test_unigram_decoded)
    test_unigram_counted = counter(test_unigram_decoded)
    print("test unigram counted:", test_unigram_counted)
    test_unigram_entropy = entropy(*test_unigram_counted)
    print("test unigram entropy:", test_unigram_entropy)
    test_unigram_cross_entropy = cross_entropy(*training_unigram_counted,
                                               *test_unigram_counted)
    print("test unigram cross entropy:", test_unigram_cross_entropy)

    test_bigram_decoded = bigram_generator(test_raw)
    print("test bigram decoded:", test_bigram_decoded)
    test_bigram_counted = counter(test_bigram_decoded)
    print("test bigram counted:", test_bigram_counted)
    test_bigram_entropy = entropy(*test_bigram_counted)
    print("test bigram entropy:", test_bigram_entropy)
    test_bigram_cross_entropy = cross_entropy(*training_bigram_counted,
                                              *test_bigram_counted)
    print("test bigram cross entropy:", test_bigram_cross_entropy)

    hani_test_unigram_decoded = unigram_decoder(hani_raw)
    print("hani unigram decoded:", hani_test_unigram_decoded)
    hani_test_unigram_counted = counter(hani_test_unigram_decoded)
    print("hani unigram counted:", hani_test_unigram_counted)
    hani_test_unigram_entropy = entropy(*hani_test_unigram_counted)
    print("hani unigram entropy:", hani_test_unigram_entropy)
    hani_test_unigram_cross_entropy = cross_entropy(*training_unigram_counted,
                                                    *hani_test_unigram_counted)
    print("hani unigram cross entropy:", hani_test_unigram_cross_entropy)
    hani_test_bigram_decoded = bigram_generator(hani_raw)
    print("hani bigram decoded:", hani_test_bigram_decoded)
    hani_test_bigram_counted = counter(hani_test_bigram_decoded)
    print("hani bigram counted:", hani_test_bigram_counted)
    hani_test_bigram_entropy = entropy(*hani_test_unigram_counted)
    print("hani bigram entropy:", hani_test_bigram_entropy)
    hani_test_bigram_cross_entropy = cross_entropy(*training_bigram_counted,
                                                   *hani_test_bigram_counted)
    print("hani bigram cross entropy;", hani_test_bigram_cross_entropy)
