from hw3 import *
import time


if __name__ == '__main__':
    start = time.time()
    sejong_training_raw = ""
    sejong_test_raw = ""
    hani_test_raw = ""
    with open('./sejong.nov.train.txt', 'r', encoding='utf8') as f:
        sejong_training_raw = f.read()
    with open('./sejong.nov.test.txt', 'r', encoding='utf8') as f:
        sejong_test_raw = f.read()
    with open('./hani.test.txt', 'r', encoding='utf8') as f:
        hani_test_raw = f.read()
    start = time.time()
    # Sejong.nov.Training

    training_jamo_unigram = jamo_unigram_decode(sejong_training_raw)
    training_jamo_unigram_count = counter(training_jamo_unigram)
    training_jamo_unigram_entropy = entropy(*training_jamo_unigram_count)
    training_jamo_unigram_cross_entropy = cross_entropy(*training_jamo_unigram_count, *training_jamo_unigram_count)
    '''
    training_jamo_unigram_result = (training_jamo_unigram_count,
                                    training_jamo_unigram_entropy,
                                    training_jamo_unigram_cross_entropy)
    '''
    training_jamo_unigram_result = (training_jamo_unigram_entropy, training_jamo_unigram_cross_entropy)
    # print("training_jamo_unigram")

    training_jamo_bigram = bigram(training_jamo_unigram)
    training_jamo_bigram_count = counter(training_jamo_bigram)
    training_jamo_bigram_entropy = entropy(*training_jamo_bigram_count)
    training_jamo_bigram_cross_entropy = cross_entropy(*training_jamo_bigram_count, *training_jamo_bigram_count)
    '''
    training_jamo_bigram_result = (training_jamo_bigram_count,
                                   training_jamo_bigram_entropy,
                                   training_jamo_bigram_cross_entropy)
    '''
    training_jamo_bigram_result = (training_jamo_bigram_entropy, training_jamo_bigram_cross_entropy)
    # print("training_jamo_bigram")

    training_syllables_unigram = syllables_unigram_decode(sejong_training_raw)
    training_syllables_unigram_count = counter(training_syllables_unigram)
    training_syllables_unigram_entropy = entropy(*training_syllables_unigram_count)
    training_syllables_unigram_cross_entropy = cross_entropy(*training_syllables_unigram_count, *training_syllables_unigram_count)
    '''
    training_syllables_unigram_result = (training_syllables_count,
                                 training_syllables_entropy,
                                 training_syllables_cross_entropy)
    '''
    training_syllables_unigram_result = (training_syllables_unigram_entropy, training_syllables_unigram_cross_entropy)
    # print("training syllables unigram")

    training_syllables_bigram = bigram(training_syllables_unigram)
    training_syllables_bigram_count = counter(training_syllables_unigram)
    training_syllables_bigram_entropy = entropy(*training_syllables_bigram_count)
    training_syllables_bigram_cross_entropy = cross_entropy(*training_syllables_bigram_count, *training_syllables_bigram_count)
    training_syllables_bigram_result = (training_syllables_bigram_entropy, training_syllables_bigram_cross_entropy)
    # print("training syllables bigram")

    pprinter("Sejong.nov.Training", training_jamo_unigram_result, training_jamo_bigram_result,
             training_syllables_unigram_result, training_syllables_bigram_result)

    # Sejong.nov.Test
    test_jamo_unigram = jamo_unigram_decode(sejong_test_raw)
    test_jamo_unigram_count = counter(test_jamo_unigram)
    training_test_jamo_unigram = new_training_set_with_UNK_optimized(training_jamo_unigram, test_jamo_unigram)
    training_test_jamo_unigram_count = counter(training_test_jamo_unigram)
    test_jamo_unigram_entropy = entropy(*test_jamo_unigram_count)
    test_jamo_unigram_cross_entropy = cross_entropy(*training_test_jamo_unigram_count, *test_jamo_unigram_count)
    '''
    test_unigram_result = (test_jamo_unigram_count,
                   test_jamo_unigram_entropy,
                   test_jamo_unigram_cross_entropy)
    '''
    test_jamo_unigram_result = (test_jamo_unigram_entropy, test_jamo_unigram_cross_entropy)
    # print("test jamo unigram")

    test_jamo_bigram = bigram(test_jamo_unigram)
    test_jamo_bigram_count = counter(test_jamo_bigram)
    training_test_jamo_bigram = new_training_set_with_UNK_optimized(training_jamo_bigram, test_jamo_bigram)
    training_test_jamo_bigram_count = counter(training_test_jamo_bigram)
    test_jamo_bigram_entropy = entropy(*training_jamo_bigram_count)
    test_jamo_bigram_cross_entropy = cross_entropy(*training_test_jamo_bigram_count, *test_jamo_bigram_count)
    test_jamo_bigram_result = (test_jamo_bigram_entropy, test_jamo_bigram_cross_entropy)
    # print("test jamo bigram")

    test_syllables_unigram = syllables_unigram_decode(sejong_test_raw)
    test_syllables_unigram_count = counter(test_syllables_unigram)
    test_training_syllables_unigram = new_training_set_with_UNK_optimized(training_syllables_unigram,
                                                                          test_syllables_unigram)
    test_training_syllables_unigram_count = counter(test_training_syllables_unigram)
    test_syllables_unigram_entropy = entropy(*test_syllables_unigram_count)
    test_syllables_unigram_cross_entropy = cross_entropy(*test_training_syllables_unigram_count, *test_syllables_unigram_count)
    '''
    test_syllables_unigram_result = (test_syllables_unigram_count,
                                     test_syllables_unigram_entropy,
                                     test_syllables_unigram_cross_entropy)
    '''
    test_syllables_unigram_result = (test_syllables_unigram_entropy, test_syllables_unigram_cross_entropy)
    # print("test syllables unigram")


    test_syllables_bigram = bigram(test_syllables_unigram)
    test_syllables_bigram_count = counter(test_syllables_bigram)
    training_test_syllables_bigram = new_training_set_with_UNK_optimized(training_syllables_bigram, test_syllables_bigram)
    training_test_syllables_bigram_count = counter(training_test_syllables_bigram)
    test_syllables_bigram_entropy = entropy(*test_syllables_bigram_count)
    test_syllables_bigram_cross_entropy = cross_entropy(*training_test_syllables_bigram_count, *test_syllables_bigram_count)
    test_syllables_bigram_result = (test_syllables_bigram_entropy, test_syllables_bigram_cross_entropy)
    # print("test syllables bigram")

    pprinter("Sejong.nov.Test", test_jamo_unigram_result, test_jamo_bigram_result,
             test_syllables_unigram_result, test_syllables_bigram_result)


    # Hani.Test
    hani_jamo_unigram = jamo_unigram_decode(hani_test_raw)
    hani_jamo_unigram_count = counter(hani_jamo_unigram)
    training_hani_test_jamo_unigram = new_training_set_with_UNK_optimized(training_jamo_unigram, hani_jamo_unigram)
    training_hani_jamo_unigram_count = counter(training_hani_test_jamo_unigram)
    hani_jamo_unigram_entropy = entropy(*hani_jamo_unigram_count)
    hani_jamo_unigram_cross_entropy = cross_entropy(*training_hani_jamo_unigram_count, *hani_jamo_unigram_count)
    '''
    hani_result = (hani_jamo_count,
                   hani_jamo_entropy,
                   hani_jamo_cross_entropy)
    '''
    hani_jamo_unigram_result = (hani_jamo_unigram_entropy, hani_jamo_unigram_cross_entropy)
    # print("hani jamo unigram")

    hani_jamo_bigram = bigram(hani_jamo_unigram)
    hani_jamo_bigram_count = counter(hani_jamo_bigram)
    training_hani_jamo_bigram = new_training_set_with_UNK_optimized(training_jamo_bigram, hani_jamo_bigram)
    training_hani_jamo_bigram_count = counter(training_hani_jamo_bigram)
    hani_jamo_bigram_entropy = entropy(*hani_jamo_bigram_count)
    hani_jamo_bigram_cross_entropy = cross_entropy(*training_hani_jamo_bigram_count, *hani_jamo_bigram_count)
    hani_jamo_bigram_result = (hani_jamo_bigram_entropy, hani_jamo_bigram_cross_entropy)
    # print("hani jamo bigram")

    hani_syllables_unigram = syllables_unigram_decode(hani_test_raw)
    hani_syllables_unigram_count = counter(hani_syllables_unigram)
    training_hani_syllables_unigram = new_training_set_with_UNK_optimized(training_syllables_unigram, hani_syllables_unigram)
    training_hani_syllables_unigram_count = counter(training_hani_syllables_unigram)
    hani_syllables_unigram_entropy = entropy(*hani_syllables_unigram_count)
    hani_syllables_unigram_cross_entropy = cross_entropy(*training_hani_syllables_unigram_count, *hani_syllables_unigram_count)

    '''
    hani_syllables_unigram_result = (hani_syllables_unigram_count,
                                     hani_syllables_unigram_entropy,
                                     hani_syllables_unigram_cross_entropy)
    '''
    hani_syllables_unigram_result = (hani_syllables_unigram_entropy, hani_syllables_unigram_cross_entropy)
    # print("hani syllables unigram")
    
    hani_syllables_bigram = bigram(hani_syllables_unigram)
    hani_syllables_bigram_count = counter(hani_syllables_bigram)
    training_hani_syllables_bigram = new_training_set_with_UNK_optimized(training_syllables_bigram, hani_syllables_bigram)
    training_hani_syllables_bigram_count = counter(training_hani_syllables_bigram)
    hani_syllables_bigram_entropy = entropy(*hani_syllables_bigram_count)
    hani_syllables_bigram_cross_entropy = cross_entropy(*training_hani_syllables_bigram_count, *hani_syllables_bigram_count)
    
    hani_syllables_bigram_result = (hani_syllables_bigram_entropy, hani_syllables_bigram_cross_entropy)
    # print("hani syllables bigram")

    pprinter("Hani.Test", hani_jamo_unigram_result, hani_jamo_bigram_result,
             hani_syllables_unigram_result, hani_syllables_bigram_result)
    end = time.time()
    print(str(end-start), "seconds")

