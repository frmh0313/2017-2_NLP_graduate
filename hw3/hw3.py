# -*- coding: utf-8 -*-
import hangul_decoder_modified
import math


def new_training_set_with_UNK_optimized_with_hash(training_decoded, test_decoded):
    result = []
    checked = {}
    for token in test_decoded:
        if hash(token) in checked.keys():
            result.append(token)
        else:
            if token in training_decoded:
                checked[hash(token)] = token
                result.append(token)
            else:
                result.append('<UNK>')
    return result


def new_training_set_with_UNK_optimized(training_decoded, test_decoded):
    result = []
    checked = []
    for token in test_decoded:
        if token in checked:
            result.append(token)
        else:
            if token in training_decoded:
                checked.append(token)
                result.append(token)
            else:
                result.append('<UNK>')
    return result


def new_training_set_with_UNK_optimized_using_set(training_decoded, test_decoded):
    result = []
    training_set = set(training_decoded)
    for token in test_decoded:
        if token in training_set:
            result.append(token)
        else:
            result.append('<UNK>')
    return result


def new_training_set_with_UNK_optimized_using_set_and_checked(training_decoded, test_decoded):
    result = []
    training_set = set(training_decoded)
    checked = {}
    for token in test_decoded:
        if token in checked:
            result.append(token)
        else:
            if token in training_set:
                checked.append(token)
                result.append(token)
            else:
                result.append('<UNK>')
    return result


def new_training_set_with_UNK(training_decoded, test_decoded):
    result = []
    for token in test_decoded:
        if token in training_decoded:
            result.append(token)
        else:
            result.append('<UNK>')
    return result


def unigram_decoder(string):
    result = []
    blank_removed = string.replace(' ', '').replace('\n', '').replace('\t', '')

    for character in blank_removed:
        result.extend(hangul_decoder_modified.decodeSyllable(character))
    return result


def jamo_unigram_decode(string):
    result = []
    blank_removed = string.replace(' ', '').replace('\n', '').replace('\t', '')

    for character in blank_removed:
        result.extend(hangul_decoder_modified.decodeSyllable(character))
    return result


def syllables_unigram_decode(string):
    return list(string.replace(' ', '').replace('\n', '').replace('\t', ''))


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

    # key_list = training_counts.keys() # key list of training_counts and test_counts are same.
    """
    @ Test corpus에는 들어있지만 training corpus에 들어있지 않은 경우 -> <UNK>로 처리
    @ Training corpus에는 들어있지만 test corpus에는 들어있지 않은 경우 -> 그냥 계산 안되니까 상관없음.
    -> Training corpus 수정 필요. Test corpus에서 원래의 training corpus에 들어있지 않은 것은 <UNK>로 바꿔서 계산한 새로운 corpus.
    """

    for key in test_counts.keys():
        if key in training_probabilities.keys():
            result += -test_probabilities[key] * math.log2(training_probabilities[key])
        else:
            # training_probabilites['<UNK.']가 사용가능하도록 training_corpus 수정 필요함.
            result += -test_probabilities[key] * math.log2(training_probabilities['<UNK>'])

    return result


def printer(name, count, entropy, cross_entropy):
    print("#########", name, "#########")
    print("count:", str(count))
    print("entropy:", str(entropy))
    print("cross_entropy:", str(cross_entropy))
