import sys
import re
import itertools


def list_of_sentences(file):
    f = open(file, 'r')
    string = f.read()
    f.close()

    string = re.sub(r'\n{2, 3}', r'\n', string)
    sentences = string.split('\n')
    non_empty_sol_sentences = filter(None, sentences)

    sentences_list = []
    for sentence in non_empty_sol_sentences:
        sentences_list.append(sentence.split())
    return sentences_list


def compare(name1, sentences_list1, name2, sentences_list2):
    total_difference_count = 0
    sentences_list1_length = len(list(itertools.chain(*sentences_list1)))
    sentences_list2_length = len(list(itertools.chain(*sentences_list2)))

    if sentences_list1_length != sentences_list2_length:
        print("Lengths of two samples are different")
        return

    for sentence1, sentence2 in zip(sentences_list1, sentences_list2):
        difference_count = 0
        if len(sentence1) != len(sentence2):
            print("Lengths of "+name1+" and "+name2+" are different.")
            print(name1 + " sentence: ", ' '.join(sentence1))
            print(name2 + " sentence: ", ' '.join(sentence2))
        else:
            for element1, element2 in zip(sentence1, sentence2):
                el1_pair = element1.split('/')
                el2_pair = element2.split('/')
                if el1_pair[0] != el2_pair[0]:
                    print("Comparing different words")
                    print(name1+" word: ", el1_pair[0])
                    print(name2+" word: ", el2_pair[0])
                else:
                    if el1_pair[1] != el2_pair[1]:
                        difference_count += 1
                        total_difference_count += 1
            # print(name1+': ', ' '.join(sentence1))
            # print(name2+': ', ' '.join(sentence2))
            # print("Difference rate: ", float(difference_count)/len(sentence1))
    print("#####################################################################")
    print(name1 + " and " + name2 + " Total difference rate: ", float(total_difference_count)/sentences_list1_length)
    print("#####################################################################")


if __name__ == '__main__':
    if len(sys.argv) > 3:
        solution = sys.argv[1]
        viterbi = sys.argv[2]
        base = sys.argv[3]
    else:
        print >> sys.stderr, 'Usage: eval.py <solution_file> <viterbi_tagged> <base_tagged>'

    solution_list_of_sentences = list_of_sentences(solution)
    viterbi_list_of_sentences = list_of_sentences(viterbi)
    base_list_of_sentences = list_of_sentences(base)

    # Solution and Base tagger
    compare("Solution", solution_list_of_sentences, "Base", base_list_of_sentences)

    # "Solution and Viterbi tagger"
    compare("Solution", solution_list_of_sentences, "Viterbi", viterbi_list_of_sentences)

    # "Base tagger and Viterbi tagger"
    compare("Base", base_list_of_sentences, "Viterbi", viterbi_list_of_sentences)
