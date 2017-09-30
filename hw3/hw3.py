import hangulDecoder

INITIAL_JAMO = hangulDecoder.INITIAL_JAMO.values()
MED_JAMO = hangulDecoder.MID_JAMO.values()
FINAL_JAMO = [ u"ㄳ",
               u"ㄵ",
               u"ㄶ",
               u"ㄺ",
               u"ㄻ",
               u"ㄼ",
               u"ㄽ",
               u"ㄾ",
               u"ㄿ",
               u"ㅀ",
               u"ㅄ"]


def stringDecoder(string):
    result = []
    for character in string:
        result.extend(hangulDecoder.decodeSyllable(character))
    return result


def jamo_counter(string):
    decoded_string = stringDecoder(string)
    initial_jamo_count = {}
    med_jamo_count = {}
    final_jamo_count = {}
    for char in decoded_string:
        if char in INITIAL_JAMO:
            initial_jamo_count[char] = initial_jamo_count[char] + 1 if char in initial_jamo_count.keys() else 1
        elif char in MED_JAMO:
            med_jamo_count[char] = med_jamo_count[char] + 1 if char in med_jamo_count.keys() else 1
        elif char in FINAL_JAMO:
            final_jamo_count[char] = final_jamo_count[char] + 1 if char in final_jamo_count.keys() else 1

    return initial_jamo_count, med_jamo_count, final_jamo_count







