python3 viterbi_tagger.py ./brown_200_tagged/* ./ca01_raw.txt
python2 base_tagger.py ./brown_200_tagged ./ca01_raw.txt
python3 eval.py ./brown_200_tagged/ca01 ./viterbi_result.txt ./base_result.txt
