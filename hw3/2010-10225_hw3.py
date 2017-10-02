# -*- coding: utf-8 -*-
import hangul_decoder_modified
import math


def jamo_unigram_decode(string):
    result = []
    blank_removed = string.replace(' ', '').replace('\n', '').replace('\t', '')

    for character in blank_removed:
        result.extend(hangul_decoder_modified.decodeSyllable(character))
    return result


def syllables_unigram_decode(string):
    return list(string.replace(' ', '').replace('\n', '').replace('\t', ''))


def bigram(unigrams):
    """
    :param unigrams:
    :return: bigram made from unigrams
    """
    bigrams = []
    for i in range(len(unigrams) - 1):
        if i == 0:
            bigrams.append(('<s>', unigrams[i]))
            bigrams.append((unigrams[i], unigrams[i+1]))
        elif i == len(unigrams) - 1:
            bigrams.append((unigrams[i], '</s>'))
        else:
            bigrams.append((unigrams[i], unigrams[i+1]))
    return bigrams


def counter(decoded_list):
    total_count = len(decoded_list)
    counts = {}
    for char in decoded_list:
        counts[char] = counts[char] + 1 if char in counts.keys() else 1
    return total_count, counts


def new_training_set_with_UNK_optimized(training_decoded, test_decoded):
    """
    training set에 없는 단어가 test set에 나온 경우를 위해
    test set에서 training set에 없는 단어를 '<UNK>'로 바꾼 새로운 training set을 만듦
    """
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


def entropy(total_count, tokens_counts):
    """
    :param total_count: number of tokens
    :param tokens_counts: { token: count } dictionary
    :return: entropy
    """
    result = 0
    for token in tokens_counts.keys():
        probability = tokens_counts[token] / total_count
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


def printer(name, jamo_unigram, jamo_bigram, syllables_unigram, syllables_bigram):
    jamo_unigram_entropy, jamo_unigram_cross_entropy = jamo_unigram
    jamo_bigram_entropy, jamo_bigram_cross_entropy = jamo_bigram
    syllables_unigram_entropy, syllables_unigram_cross_entropy = syllables_unigram
    syllables_bigram_entropy, syllables_bigram_cross_entropy = syllables_bigram

    print("{:>67} {:>25} {:>20}".format("entropy", "cross-entropy", "Difference"))
    print("{:<20} {:>10} {:>15}  {:>20} {:>23} {:>22}".format(name, "자소별", "unigram",
                                                              jamo_unigram_entropy,
                                                              jamo_unigram_cross_entropy,
                                                              jamo_unigram_cross_entropy - jamo_unigram_entropy))
    print("{:>48} {:>21} {:>23} {:>22}".format("bigram",
                                               jamo_bigram_entropy,
                                               jamo_bigram_cross_entropy,
                                               jamo_bigram_cross_entropy - jamo_bigram_entropy))
    print("{:>31} {:>15}  {:>20} {:>23} {:>22}".format("음절별", "unigram",
                                                       syllables_unigram_entropy,
                                                       syllables_unigram_cross_entropy,
                                                       syllables_unigram_cross_entropy - syllables_unigram_entropy))
    print("{:>48}  {:>20} {:>23} {:>22}".format("bigram",
                                                syllables_bigram_entropy,
                                                syllables_bigram_cross_entropy,
                                                syllables_bigram_cross_entropy - syllables_bigram_entropy))
    print()


if __name__ == '__main__':
    sejong_training_raw = ""
    sejong_test_raw = ""
    hani_test_raw = ""
    with open('./sejong.nov.train.txt', 'r', encoding='utf8') as f:
        sejong_training_raw = f.read()
    with open('./sejong.nov.test.txt', 'r', encoding='utf8') as f:
        sejong_test_raw = f.read()
    with open('./hani.test.txt', 'r', encoding='utf8') as f:
        hani_test_raw = f.read()

    # Sejong.nov.Training
    # Sejong.nov.Training jamo unigram
    training_jamo_unigram = jamo_unigram_decode(sejong_training_raw)
    training_jamo_unigram_count = counter(training_jamo_unigram)
    training_jamo_unigram_entropy = entropy(*training_jamo_unigram_count)
    training_jamo_unigram_cross_entropy = cross_entropy(*training_jamo_unigram_count, *training_jamo_unigram_count)
    training_jamo_unigram_result = (training_jamo_unigram_entropy,
                                    training_jamo_unigram_cross_entropy)

    # Sejong.nov.Training jamo bigram
    training_jamo_bigram = bigram(training_jamo_unigram)
    training_jamo_bigram_count = counter(training_jamo_bigram)
    training_jamo_bigram_entropy = entropy(*training_jamo_bigram_count)
    training_jamo_bigram_cross_entropy = cross_entropy(*training_jamo_bigram_count, *training_jamo_bigram_count)
    training_jamo_bigram_result = (training_jamo_bigram_entropy,
                                   training_jamo_bigram_cross_entropy)

    # Sejong.nov.Training syllables unigram
    training_syllables_unigram = syllables_unigram_decode(sejong_training_raw)
    training_syllables_unigram_count = counter(training_syllables_unigram)
    training_syllables_unigram_entropy = entropy(*training_syllables_unigram_count)
    training_syllables_unigram_cross_entropy = cross_entropy(*training_syllables_unigram_count,
                                                             *training_syllables_unigram_count)
    training_syllables_unigram_result = (training_syllables_unigram_entropy,
                                         training_syllables_unigram_cross_entropy)

    # Sejong.nov.Training syllables bigram
    training_syllables_bigram = bigram(training_syllables_unigram)
    training_syllables_bigram_count = counter(training_syllables_bigram)
    training_syllables_bigram_entropy = entropy(*training_syllables_bigram_count)
    training_syllables_bigram_cross_entropy = cross_entropy(*training_syllables_bigram_count,
                                                            *training_syllables_bigram_count)
    training_syllables_bigram_result = (training_syllables_bigram_entropy,
                                        training_syllables_bigram_cross_entropy)

    printer("Sejong.nov.Training", training_jamo_unigram_result, training_jamo_bigram_result,
            training_syllables_unigram_result, training_syllables_bigram_result)

    # Sejong.nov.Test
    # Sejong.nov.Test jamo unigram
    test_jamo_unigram = jamo_unigram_decode(sejong_test_raw)
    test_jamo_unigram_count = counter(test_jamo_unigram)
    training_test_jamo_unigram = new_training_set_with_UNK_optimized(training_jamo_unigram, test_jamo_unigram)
    training_test_jamo_unigram_count = counter(training_test_jamo_unigram)
    test_jamo_unigram_entropy = entropy(*test_jamo_unigram_count)
    test_jamo_unigram_cross_entropy = cross_entropy(*training_test_jamo_unigram_count, *test_jamo_unigram_count)
    test_jamo_unigram_result = (test_jamo_unigram_entropy, test_jamo_unigram_cross_entropy)

    # Sejong.nov.Test jamo bigram
    test_jamo_bigram = bigram(test_jamo_unigram)
    test_jamo_bigram_count = counter(test_jamo_bigram)
    training_test_jamo_bigram = new_training_set_with_UNK_optimized(training_jamo_bigram, test_jamo_bigram)
    training_test_jamo_bigram_count = counter(training_test_jamo_bigram)
    test_jamo_bigram_entropy = entropy(*test_jamo_bigram_count)
    test_jamo_bigram_cross_entropy = cross_entropy(*training_test_jamo_bigram_count, *test_jamo_bigram_count)
    test_jamo_bigram_result = (test_jamo_bigram_entropy, test_jamo_bigram_cross_entropy)

    # Sejong.nov.Test syllables unigram
    test_syllables_unigram = syllables_unigram_decode(sejong_test_raw)
    test_syllables_unigram_count = counter(test_syllables_unigram)
    test_training_syllables_unigram = new_training_set_with_UNK_optimized(training_syllables_unigram,
                                                                          test_syllables_unigram)
    test_training_syllables_unigram_count = counter(test_training_syllables_unigram)
    test_syllables_unigram_entropy = entropy(*test_syllables_unigram_count)
    test_syllables_unigram_cross_entropy = cross_entropy(*test_training_syllables_unigram_count,
                                                         *test_syllables_unigram_count)
    test_syllables_unigram_result = (test_syllables_unigram_entropy, test_syllables_unigram_cross_entropy)

    # Sejong.nov.Test syllables bigram
    test_syllables_bigram = bigram(test_syllables_unigram)
    test_syllables_bigram_count = counter(test_syllables_bigram)
    training_test_syllables_bigram = new_training_set_with_UNK_optimized(training_syllables_bigram,
                                                                         test_syllables_bigram)
    training_test_syllables_bigram_count = counter(training_test_syllables_bigram)
    test_syllables_bigram_entropy = entropy(*test_syllables_bigram_count)
    test_syllables_bigram_cross_entropy = cross_entropy(*training_test_syllables_bigram_count,
                                                        *test_syllables_bigram_count)
    test_syllables_bigram_result = (test_syllables_bigram_entropy, test_syllables_bigram_cross_entropy)

    printer("Sejong.nov.Test", test_jamo_unigram_result, test_jamo_bigram_result,
            test_syllables_unigram_result, test_syllables_bigram_result)

    # Hani.Test
    # Hani.Test jamo unigram
    hani_jamo_unigram = jamo_unigram_decode(hani_test_raw)
    hani_jamo_unigram_count = counter(hani_jamo_unigram)
    training_hani_test_jamo_unigram = new_training_set_with_UNK_optimized(training_jamo_unigram, hani_jamo_unigram)
    training_hani_jamo_unigram_count = counter(training_hani_test_jamo_unigram)
    hani_jamo_unigram_entropy = entropy(*hani_jamo_unigram_count)
    hani_jamo_unigram_cross_entropy = cross_entropy(*training_hani_jamo_unigram_count, *hani_jamo_unigram_count)
    hani_jamo_unigram_result = (hani_jamo_unigram_entropy, hani_jamo_unigram_cross_entropy)

    # Hani.Test jamo bigram
    hani_jamo_bigram = bigram(hani_jamo_unigram)
    hani_jamo_bigram_count = counter(hani_jamo_bigram)
    training_hani_jamo_bigram = new_training_set_with_UNK_optimized(training_jamo_bigram, hani_jamo_bigram)
    training_hani_jamo_bigram_count = counter(training_hani_jamo_bigram)
    hani_jamo_bigram_entropy = entropy(*hani_jamo_bigram_count)
    hani_jamo_bigram_cross_entropy = cross_entropy(*training_hani_jamo_bigram_count, *hani_jamo_bigram_count)
    hani_jamo_bigram_result = (hani_jamo_bigram_entropy, hani_jamo_bigram_cross_entropy)

    # Hani.Test syllables unigram
    hani_syllables_unigram = syllables_unigram_decode(hani_test_raw)
    hani_syllables_unigram_count = counter(hani_syllables_unigram)
    training_hani_syllables_unigram = new_training_set_with_UNK_optimized(training_syllables_unigram,
                                                                          hani_syllables_unigram)
    training_hani_syllables_unigram_count = counter(training_hani_syllables_unigram)
    hani_syllables_unigram_entropy = entropy(*hani_syllables_unigram_count)
    hani_syllables_unigram_cross_entropy = cross_entropy(*training_hani_syllables_unigram_count,
                                                         *hani_syllables_unigram_count)
    hani_syllables_unigram_result = (hani_syllables_unigram_entropy, hani_syllables_unigram_cross_entropy)

    # Hani.Test syllables bigram
    hani_syllables_bigram = bigram(hani_syllables_unigram)
    hani_syllables_bigram_count = counter(hani_syllables_bigram)
    training_hani_syllables_bigram = new_training_set_with_UNK_optimized(training_syllables_bigram,
                                                                         hani_syllables_bigram)
    training_hani_syllables_bigram_count = counter(training_hani_syllables_bigram)
    hani_syllables_bigram_entropy = entropy(*hani_syllables_bigram_count)
    hani_syllables_bigram_cross_entropy = cross_entropy(*training_hani_syllables_bigram_count,
                                                        *hani_syllables_bigram_count)
    hani_syllables_bigram_result = (hani_syllables_bigram_entropy, hani_syllables_bigram_cross_entropy)

    printer("Hani.Test", hani_jamo_unigram_result, hani_jamo_bigram_result,
            hani_syllables_unigram_result, hani_syllables_bigram_result)
