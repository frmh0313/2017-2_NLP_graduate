import hangul_decoder_modified
import math

INITIAL_JAMO = hangul_decoder_modified.INITIAL_JAMO.values()
MED_JAMO = hangul_decoder_modified.MID_JAMO.values()
#deleted u"none" and the syllables included in INITIAL_JAMO
FINAL_JAMO = [ u"ㄳ", u"ㄵ", u"ㄶ", u"ㄺ", u"ㄻ", u"ㄼ", u"ㄽ", u"ㄾ", u"ㄿ", u"ㅀ", u"ㅄ"]
JAMO = []
JAMO.extend(INITIAL_JAMO, MED_JAMO, FINAL_JAMO)


def string_unigram_decoder(string):
    result = []
    for character in string:
        result.extend(hangul_decoder_modified.decodeSyllable(character))
    return result


def bigram_generator(string):
    unigrams = string_unigram_decoder(string)
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


def entropy(total_count, jamo_count):
    result = 0
    for jamo in jamo_count:
        probability = jamo_count[jamo]/total_count
        result += -probability * math.log2(probability)
    return result


def cross_entropy(training_total_count, training_count, test_total_count, test_count):


