import itertools,sys
from collections import Counter
from extract_event import EventEncoder, TrainingInst

def get_wsd_features_from_event (context,vocab,position,id,window_size=6):
    """
    C{vocab} is a dictionary with vocabulary keys.
    These are assumed to be the features chosen to represent a sense-generating
    event.  Not every context will exhibit a given feature.
    Loop throught the context to find the features (vocab items)
    instantiated in it.
    
    Return a dictionary assigning 1 to all the features found. (vocab items found).
    It must also assign 0 to all the features not found.

    C{position} and C{id} are available bits of info not currently being used.
    C{position} is the position of the target word in the context.
    C{id} is just the example id.
    """
    # Make a dict assigning 0 to each vocab item.
    features = dict(itertools.product(vocab.keys(), [0]))
    position = int(position)
    for (i,item) in enumerate(context):
        ## May change item
        (item, wd, pos) = get_lex_components(item)
        if i == position:
            pass
        if i < position  - window_size:
            pass
        if i > position  + window_size:
            pass
        if item in vocab:
            features[item] = 1
    return features

def extract_vocab(event_list, n=100):
    """
    Return a dictionary of n most frequently occurring words in THESE
    contexts, excluding stop words.

    This is a place to consider modifications.  is the top
    300 words the best choice.  How should we select other words?

    @return vocab: vocab[{word}] returns a list of the context
         ids C{word} occurs in.
    """
    # Google's stoplist with most preps removed. "and" added, word added
    import nltk
    # stopwords = [ 'I',    'a',    'an',    'are',    'as',    'and',
    #               'be',    'com',   'how',  'is',    'it',    'of',    'or',
    #               'that',    'the',  'this',    'was',    'what',
    #               'when',   'where',    'who',    'will',    'with',
    #               'the',    'www','was']
    stopwords = nltk.corpus.stopwords.words('english')
    vocab = Counter()
    selected_features = ['look_NN', 'work_NN', 'get_NN', 'take_NN', 'hard_NN', "'s_VBZ", 'surface_NN',
                         'rock_NN', 'feeling_NN', 'get_VB', 'take_VB', 'hard_JJ']
    for (s_inst, sense) in event_list:
        for (i,item) in enumerate(s_inst.context):
            #if i == int(s_inst.position):
            #    continue
            (item, wd, pos) = get_lex_components(item)
            if wd in stopwords:
                continue
            if item in selected_features:
                continue
            if pos in ['PRP','IN','CC','DT']:
                continue
            vocab[item] += 1
    il = vocab.items()
    il.sort(key=lambda x: x[1],reverse=True)
    il = il[:n]
    vocab = dict(il)

    for feature in selected_features:
        vocab[feature] = 1000
    # vocab['look_NN'] = 1000
    # vocab['work_NN'] = 1000
    # vocab['get_NN'] = 1000
    # vocab['take_NN'] = 1000
    # vocab['hard_NN'] = 1000
    # vocab["'s_VBZ"] = 1000
    # vocab['cushion_NN'] = 1000
    # vocab['soft_JJ'] = 1000
    # vocab['cover_NN'] = 1000

    # vocab['surface_NN'] = 1000
    # vocab['rock_NN'] = 1000
    # vocab['feeling_NN'] = 1000
    # vocab['get_VB'] = 1000
    # vocab['take_VB'] = 1000
    # vocab['hard_JJ'] = 1000

    return vocab


def get_lex_components (item):
    [wd,pos] = item.split('_')
    # map plural and singular Nouns to same feature
    if pos == 'NNS' and wd.endswith('s'):
        wd = wd[:-1]
        pos = 'NN'
        item = '_'.join([wd,pos])
    return (item, wd, pos)


def read_vocab_file (filename):
        """
        C{filename} contains a list of features, which may have been selected
        by a feature selection algorithm like that of Berger etal
        (1996), implemented in YasmetFS.  If so, the features are listed in the
        order discovered and when we select from these features, we add them
        in the order feature selectxion chose them, and the task will be to determine
        when to stop adding features.  So preserve order when
        reading in features.
        """
        feature_ordering = []
        
        with open(filename,'r') as fh:
            for line in fh:
                line = line.strip()
                feature_ordering.append(line)

        return feature_ordering


class SensevalInst (TrainingInst):
    """
    Class for training instances in which event attributes taken from the
    corpus can be represented.  Class instances as usual are created by
    calling the classname as a function.  The C{context}, the sentence in which
    our word of interest occurs with a particular sense, is the first argument.
    Thus
        --  SensevalInst(context,position,id)
    creates a class instance.
    """

    att_list = ['position','id']
    class_att = 'sense'

if __name__ == '__main__':

    import os.path
    
    ########################################################################
    ########################################################################
    #
    #   W h e r e   &   W h a t 
    #
    ########################################################################
    ########################################################################

    working_dir = os.getcwd()
    word = 'hard'
    #xml_file = 'senseval-%s.xml' % (word, )
    if len(sys.argv) == 2:
        xml_file = sys.argv[1]
    else:
        print
        print 'Usage: %s <xml_file>' % (sys.argv[0],)
        print
        sys.exit()
    
    full_path = os.path.join(working_dir,xml_file)
    
    ########################################################################
    ########################################################################
    #
    #   E n c o d i n g      P a r a m s
    #
    ########################################################################
    ########################################################################

    ## Extract the 100 most frequent vocab words from the events
    ## and store as a dictionary.
    # vocab_size = 100
    vocab_size = 200
    vocab_set = 'hand'
    event_file = 'senseval-%s.evt' % (word,)


    ########################################################################
    ########################################################################
    #
    #   E n c o d e     B a s i c   M o d e l
    #
    ########################################################################
    ########################################################################

    ## Get the events and the vocab, in that order.
    # create EventEncoder instance
    # C{parse_xml_file_and_extracrt_events} creates an event_list stored on
    # EventEncoder instance.
    
    # C{event_list} is a list of ~ 4000 (sense, event) pairs, each representing
    # one the examples in the corpus. Each sense is
    # one of 'HARD1, HARD2, HARD3'.  Each event  is an instance of class SensevalInst
    # representing attributes of a corpus example (the attributes in the class
    # att_list feature defined above) + the sentence,
    # (stored in the attribute context).
    
    e_encoder = EventEncoder(SensevalInst)
    e_encoder.parse_xml_file_and_extract_events(full_path,'senseval_instances', \
                                                'senseval_instance')
    e_encoder.get_class_stats()
    e_encoder.print_class_stats()

    #  Get the vocabulary by perusing the data.  The function you edit in this assignment
    wsd_feats = extract_vocab(e_encoder.event_list, n = vocab_size)

 
    # Cencode_events} method produces a list of event feature dicts
    # stored under C{e_encoder.encoded_events}.
    e_encoder.encode_events (get_wsd_features_from_event, wsd_feats)

    ## Write out an event file for use by learners (e.g., nltk maxent learner)
    e_encoder.write_encoded_event_file(os.path.join(working_dir,event_file))


