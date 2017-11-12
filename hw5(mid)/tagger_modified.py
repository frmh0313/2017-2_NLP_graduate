#!/usr/bin/python

############################################################
# Main Program
############################################################

if __name__ == '__main__':
    import sys
    import string
    import glob
    try:
        import psyco
        psyco.full()
    except:
        print >> sys.stderr, 'Warning: No psyco available'
    # COMMANDLINE: tagger_modified.py training_file test_file
    # MODIFIED COMMANDLINE: tagger_modified.py training_file_directory test_file

    if len(sys.argv) > 2:
        # training_file = sys.argv[1]
        training_files = glob.glob(sys.argv[1]+'/*')
        test_file = sys.argv[2]
    elif len(sys.argv) > 1:
        training_files = glob.glob(sys.argv[1]+'/*')
        # training_file = sys.argv[1]
        print >> sys.stderr, 'No test file!\n' 
    else:
        print >> sys.stderr, 'Usage: tagger_modified.py <training_file_directory> <test_file>'
    # sys.stderr is the file like object that corresponds to STDERR
    # Reading training data
    best_tag = {}  ## best tag for word: = most frequent tag
    default_tag='' ## tag with best overall count

    word_tag_matrix = {}
    tag_count = {}
    best_tag_count = {}

    for file in training_files:
        try:
            fsock_train = open(file, 'r', 0)
            print >> sys.stderr, 'Reading %s' % file

            for line in fsock_train:
                splitline = line.rstrip().split()
                if len(splitline) > 0:
                    for elem in splitline:
                        wt_pair = elem.split('_')
                        if len(wt_pair) == 2:
                            (word, tag) = wt_pair
                            word_tag_matrix[word, tag] = word_tag_matrix.get((word, tag), 0) + 1
                            tag_count[tag] = tag_count.get(tag, 0) + 1
                        else:
                            print >> sys.stderr, 'Ill formed word/tag pair ', wt_pair
                else:
                    continue
            fsock_train.close()
        except IOError:
            print >> sys.stderr, "Unable to open %s" % file
    print >> sys.stderr, 'Computing best tags'
    for wt_pair in word_tag_matrix.keys():
        (word, tag) = wt_pair
        word_tag_count = word_tag_matrix[word, tag]
        if word_tag_count > best_tag_count.get(word, 0):
            best_tag_count[word] = word_tag_count
            best_tag[word] = tag
            default_tag_count = 0
        else:
            continue

    try:
        fsock_test = open(test_file, 'r', 0)
        print >> sys.stderr, 'Reading %s' % test_file
        for line in fsock_test:
            splitline = line.rstrip().split(' ')
            if len(splitline) > 0:
                for word in splitline:
                    tag = best_tag.get(word, 0)
                    if tag:
                        print '%s_%s ' % (word, tag)
                    elif default_tag:
                        print '%s_%s ' % (word, default_tag)
                    else:
                        print '%s_dunno '
                print '\n',
        fsock_test.close()
    except IOError:
        print >> sys.stderr, "Unable to open %s" % test_file
