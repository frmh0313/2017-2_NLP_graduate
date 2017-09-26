# -*- coding: utf-8 -*-

'''
python 2010-10225_hw1-2 input_file 또는
python 2010-10225_hw1-2 input_file output_file 로 실행시키시면 됩니다.

python input_file 로 실행시키시면 기본적으로 같은 폴더의 output.txt파일에 결과가 저장됩니다.
'''
import re
import sys


def pig_latin(file, out='./output.txt'):
    f = open(file, 'r')
    o = open(out, 'w')

    raw = f.read()
    words = re.split(' ', raw)

    start_with_non_alpha = re.compile(r'^([\W_]+)(.*)')
    end_with_non_alpha = re.compile(r'(.*?)([\W_]+)$')

    start_with_qu = re.compile(r'^([qQ][uU])([AEIOUYaeiouy]+.*)')
    consonants_qu = re.compile(r'^([^\W\dAEIOUYaeiouy_]+[qQ][uU][^\W\dAEIOUYaeiouy_]*)(.*)')
    qu_consonants = re.compile(r'^([^\W\dAEIOUYaeiouy]*[qQ][uU][^\W\dAEIOUYaeiouy_]+)(.*)')

    start_with_y = re.compile(r'^([yY][^\W\dAEIOUYaeiouy_]*)(.*)')

    for word in words:
        w = ""
        end = ""

        # 알파벳이 아닌 글자로 시작하는 경우 이 부분을 분리시킨 후 처리
        is_start_with_non_alpha = start_with_non_alpha.match(word)

        if is_start_with_non_alpha:
            w += is_start_with_non_alpha.group(1)
            word = is_start_with_non_alpha.group(2)

        # 알파벳이 아닌 글자로 끝나는 경우 이 부분을 분리시킨 후 나중에 붙임
        is_end_with_non_alpha = end_with_non_alpha.match(word)

        if is_end_with_non_alpha:
            end = is_end_with_non_alpha.group(2)
            word = is_end_with_non_alpha.group(1)

        is_start_with_y = start_with_y.match(word)
        is_start_with_consonants_qu = consonants_qu.match(word)
        is_start_with_qu_consonants = qu_consonants.match(word)
        is_start_with_qu = start_with_qu.match(word)

        if is_start_with_y:  # y가 자음인 경우: y로 시작하는 경우
            w += is_start_with_y.group(2) + is_start_with_y.group(1)
        elif is_start_with_consonants_qu:  # 자음 + qu (+ 자음)*인 경우
            w += is_start_with_consonants_qu.group(2) + is_start_with_consonants_qu.group(1)
        elif is_start_with_qu_consonants:  # (자음)* + qu + 자음인 경우
            w += is_start_with_qu_consonants.group(2) + is_start_with_qu_consonants.group(1)
        elif is_start_with_qu:  # qu + 모음인 경우
            w += is_start_with_qu.group(2) + is_start_with_qu.group(1)
        else:  # 모음으로 시작하는 경우
            w += word

        w += "ay"
        w += end

        o.write(w + ' ')
    f.close()
    o.close()


def main():
    if len(sys.argv) == 2:
        pig_latin(sys.argv[1])
    elif len(sys.argv) == 3:
        pig_latin(sys.argv[1], out=sys.argv[2])
    else:
        print("Wrong number of arguments.")


if __name__ == '__main__':
    main()

