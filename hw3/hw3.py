# -*- coding: utf-8 -*-
import hangul_decoder_modified
import math


def new_training_set_with_UNK_optimized(training_decoded, test_decoded):
    result = []
    training_set = set(training_decoded)
    checked = set()
    for token in test_decoded:
        if token in checked:
            result.append(token)
        else:
            if token in training_set:
                checked.add(token)
                result.append(token)
            else:
                result.append('<UNK>')
    return result


def jamo_unigram_decode(string):
    result = []
    blank_removed = string.replace(' ', '').replace('\n', '').replace('\t', '')

    for character in blank_removed:
        result.extend(hangul_decoder_modified.decodeSyllable(character))
    return result


def syllables_unigram_decode(string):
    return list(string.replace(' ', '').replace('\n', '').replace('\t', ''))

'''
def bigram(unigrams):
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
'''

def bigram(unigrams):
    bigrams = []
    for i in range(len(unigrams) -1):
        if i == 0:
            bigrams.append(('<s>', unigrams[i]))
            bigrams.append((unigrams[i], unigrams[i+1]))
        elif i == len(unigrams) -1:
            bigrams.append((unigrams[i], '</s>'))
        else:
            bigrams.append((unigrams[i], unigrams[i+1]))
    return bigrams

'''

def counter(test_decoded, training_decoded):
    total_count = len(test_decoded)
    counts = {}
    for char in test_decoded:
        if char in training_decoded:
            counts[char] = counts[char] + 1 if char in counts.keys() else 1
        else: # test set에는 있지만 training set에는 들어있지 않은 단어의 경우 '<UNK>'로 처리하여 test counter dict에 저장.
            counts['<UNK>'] = counts['<UNK>'] + 1 if '<UNK>' in counts.keys() else 1
    return total_count, counts
'''


def counter(decoded_list):
    total_count = len(decoded_list)
    counts = {}
    for char in decoded_list:
        counts[char] = counts[char] + 1 if char in counts.keys() else 1
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

    for key in test_counts.keys():
        if key in training_probabilities.keys():
            result += -test_probabilities[key] * math.log2(training_probabilities[key])
        else:
            result += -test_probabilities[key] * math.log2(training_probabilities['<UNK>'])

    return result


def printer(name, count, entropy, cross_entropy):
    print("#########", name, "#########")
    print("count:", str(count))
    print("entropy:", str(entropy))
    print("cross_entropy:", str(cross_entropy))
    print("difference:", str(entropy - cross_entropy))


def pprinter(name, jamo_unigram, jamo_bigram, syllables_unigram, syllables_bigram):
    jamo_unigram_entropy, jamo_unigram_cross_entropy = jamo_unigram
    jamo_bigram_entropy, jamo_bigram_cross_entropy = jamo_bigram
    syllables_unigram_entropy, syllables_unigram_cross_entropy = syllables_unigram
    syllables_bigram_entropy, syllables_bigram_cross_entropy = syllables_bigram

    print("{:>67} {:>25} {:>20}".format("entropy", "cross-entropy", "Difference"))
    print("{:<20} {:>10} {:>15}  {:>20} {:>23} {:>22}".format(name, "자소별", "unigram",
                                                            jamo_unigram_entropy,
                                                            jamo_unigram_cross_entropy,
                                                            jamo_unigram_entropy - jamo_unigram_cross_entropy))
    print("{:>48} {:>21} {:>23} {:>22}".format("bigram",
                                               jamo_bigram_entropy,
                                               jamo_bigram_cross_entropy,
                                               jamo_bigram_entropy - jamo_bigram_cross_entropy))
    print("{:>31} {:>15}  {:>20} {:>23} {:>22}".format("음절별", "unigram",
                                                      syllables_unigram_entropy,
                                                      syllables_unigram_cross_entropy,
                                                      syllables_unigram_entropy - syllables_unigram_cross_entropy))
    print("{:>48}  {:>20} {:>23} {:>22}".format("bigram",
                                               syllables_bigram_entropy,
                                               syllables_bigram_cross_entropy,
                                               syllables_bigram_entropy - syllables_bigram_cross_entropy))
    print()


