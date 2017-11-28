#!/usr/bin/python

############################################################
# Main Program
############################################################

if __name__ == '__main__':
    print("BASE TAGGER TAGGING")
    import sys
    import string
    import glob
    #MODIFIED COMMANDLINE : base_tagger.py training_directory test_file


    # if len(sys.argv) > 2:
    #     training_files = glob.glob(sys.argv[1]+'/*')
    #     test_file = sys.argv[2]
    # else:
    #     print >> sys.stderr, 'Usage: base_tagger.py <training_files> <test_file>'

    if len(sys.argv) > 2:
        training_files = glob.glob(sys.argv[1]+'/*')
        test_file = sys.argv[2]
    else:
        print >> sys.stderr, 'Usage: base_tagger.py <training_files> <test_file>'

    # sys.stderr is the file like object that corresponds to STDERR
    # Reading training data
    best_tag={}  ## best tag for word: = most frequent tag
    default_tag='' ## tag with best overall count
    for training_file in training_files:
        try:
            fsock_train=open(training_file,'r',0)
            # fsock_train = open(training_file, 'r').read()
            # print >> sys.stderr, 'Reading %s' % training_file
            word_tag_matrix={}  ## word tag pair counts
            ## For word tag pairs, each key-value pair: a pair of a word and a tag
            ##
            ## word_tag_matrix.get(('all','DET0'),0) = the number of 'all' tokens tagged as DET0
            ##               0 is what to return if (key,val) does not occurr in matrix...
            ##               safe when ('all','DET0') has never been seen
            ## incrementing (safe for 1st occurrence of key,val)
            ## word_tag_matrix['all','DET0'] = word_tag_matrix.get(('all','DET0'),0) +1
            tag_count={}   ##  tag counts
            ## NB: the 'get' method on dictionaries works for singleton keys as well as pair keys...
            ## tag_count[tag]=tag_count.get(tag,0)+1
            best_tag_count={} ## store count of best tag for word
            for line in fsock_train:
                 line = line.replace('\t', '<s>/<s> ')
                 # splitline=line.rstrip().split()
                 splitline = line.split()
                 # print splitline
                 # split(' ') differs from split().
                 # The latter handles consecutive spaces as we'd like
                 if len(splitline)>0:
                     for elem in splitline:  ## Each elem shd be a word_tag pair connected by "_"
                         wt_pair=elem.split('/')
                         if len(wt_pair)==2:
                             (word,tag)=wt_pair
                             word_tag_matrix[word,tag]=word_tag_matrix.get((word,tag),0) + 1
                             tag_count[tag]=tag_count.get(tag,0)+1
                             # print (word,tag)
                         elif len(wt_pair)==3:
                             (word,tag) = (wt_pair[0]+wt_pair[1], wt_pair[2])
                             word_tag_matrix[word, tag]=word_tag_matrix.get((word, tag), 0) + 1
                             tag_count[tag] = tag_count.get(tag, 0) + 1
                         # elif len(wt_pair)==1:
                         #     (word, tag) = ('<s>', '<s>')
                         #     word_tag_matrix[word, tag]=word_tag_matrix.get((word, tag), 0) + 1
                         #     tag_count[tag] = tag_count.get(tag, 0) + 1

                         else: print >> sys.stderr, 'Ill formed word/tag pair ', wt_pair
                 else:
                     continue
            fsock_train.close()
            # print >> sys.stderr, 'Computing best tags'
            for wt_pair in word_tag_matrix.keys():
                (word,tag)=wt_pair
                word_tag_count=word_tag_matrix[word,tag]
                if word_tag_count > best_tag_count.get(word,0):
                    best_tag_count[word]=word_tag_count
                    best_tag[word]=tag
                    # print (word,tag)
                    default_tag_count=0
            for tag in tag_count.keys():
                if tag_count[tag] > default_tag_count:
                    default_tag_count=tag_count[tag]
                    default_tag=tag
                else: continue
        except IOError:
            print >> sys.stderr, "Unable to open %s" % training_file
    try:
        output = open('base_result.txt', 'w')
        fsock_test=open(test_file,'r',0)
        # fsock_test = open(test_file, 'r').read()
        print >> sys.stderr, 'Reading %s' % test_file
        for line in fsock_test:
             if len(line) > 1:
                 result_list = []
                 line = line.replace('\t', '<s> ')
                 splitline=line.rstrip().split(' ')
                 if len(splitline)>0:
                     for word in splitline:  ## Each word shd be an untagged word
                         tag=best_tag.get(word,0)
                         if tag == '<s>':
                             continue
                         elif tag:
                             # print 'word: ', word
                             # print '%s_%s' % (word, tag),
                             result_list.append('%s/%s' % (word, tag))
                             # print "%s_%s" % (word, tag) adds a carriage return each time
                             # Python string magic:  '%s_%s ' % (word, tag) evaluates  to the string we want.
                             # print word + '_' + tag + ' ' # '+': concatenate operator, alt syntax
                             # See Dive into Python, Section 3.5
                             # Alternative:
                             # sys.stdout.write('%s_%s ' % (word, tag))
                             # sys.stdout is the Python filelike object corresponding to STDOUT
                         # elif default_tag:
                             # print 'default_tag: '
                             # print '%s_%s ' % (word, default_tag),
                         else:
                             # print 'dunno word: ', word
                             # print '%s_dunno ' % word, # we didnt find the training file.
                             result_list.append('%s/%s' % (word, tag))
                     # print '\n',
                     output.write(' '.join(result_list)+'\n')
        fsock_test.close()
        output.close()
    except IOError:
        print >> sys.stderr, "Unable to open %s" % test_file

