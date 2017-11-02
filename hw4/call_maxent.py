#! /usr/bin/env python
"""
Main function is wsd_demo which has an obligatory
evert file argument.  This must be a sequence
of events in the following line by line format::

BEGIN EVENT
CLASS
FEATURE1 VALUE1
FEATURE2 VALUE2
....
FEATUREN VALUEN
END EVENT

The convention being followed is that files in this special
format have the extension '.evt'
"""

from nltk.classify import maxent, util
from collections import defaultdict, Counter

def read_event_file(eventfile):
    fh = open(event_file,'r')
    event_list = []
    sense = None
    event_begin = False
    ctr = 0
    for line in fh:
        ctr += 1
        line = line.strip()
        if line == 'BEGIN EVENT':
            event_begin = True
            feature_dict = {}
            continue
        else:
            if line == 'END EVENT':
                if sense:
                    event_list.append((feature_dict,sense))
                    event_begin = False
                    sense = None
                else:
                    print 'Format error: line number %d' % (ctr,)
                    break
            elif event_begin:
                sense = line
                event_begin = False
            else:
                (key,val) = line.split()
                if val == '0':
                    val = False
                else:
                    val = True
                feature_dict[key] = val
                
    return event_list

def wsd_demo(event_file, trainer, n=1000, **cutoffs):
    global test, classifier
    import random

    events = read_event_file(event_file)
    print 'Reading data...'
    if n> len(events): n = len(events)
    senses = list(set(l for (i,l) in events))
    print '  Senses: ' + ' '.join(senses)

    # Randomly split the names into a test & train set.
    print 'Splitting into test & train...'
    #random.seed(123456)
    random.seed(162354)
    random.shuffle(events)
    train = events[:int(.9*n)]
    test = events[int(.9*n):n]

    # Train up a classifier.
    print 'Training classifier...'
    classifier = trainer(train, **cutoffs )

    # Run the classifier on the test data.
    print 'Testing classifier...'
    acc,pre_dict,rec_dict,total,sys_corr_dict = apr(classifier, test)
    print 'Accuracy: %6.4f' % acc
    print 'Total: %d' % total
    print
    print
    print '%-20s %10s  %10s' % ('Label', 'Precision', 'Recall')
    print '_' * 45
    for l in pre_dict:
        print '%-20s %10.3f  %10.3f' % (l, pre_dict[l], rec_dict[l])
    print
    print
    print '%-20s %10s' % ('Label', 'Num Corr')
    for l in pre_dict:
        print '%-20s %d' % (l, sys_corr_dict[l])

    print
    print
    # For classifiers that can find probabilities, show the log
    # likelihood and some sample probability distributions.
    try:
        pdists = classifier.batch_prob_classify(test)
        ll = [pdist.logprob(gold)
              for ((name, gold), pdist) in zip(test, pdists)]
        print 'Avg. log likelihood: %6.4f' % (sum(ll)/len(test))
    except:
        pass
    
    # Return the classifier
    return classifier

def accuracy(classifier, gold):
    results = classifier.batch_classify([fs for (fs,l) in gold])
    correct = [l==r for ((fs,l), r) in zip(gold, results)]
    if correct:
        return float(sum(correct))/len(correct)
    else:
        return 0

def apr (classifier, gold):
    results = classifier.classify_many([fs for (fs,l) in gold])
    #gold_class_dict = defaultdict(list)
    #classifier_class_dict = {}
    sys_correct_dict = Counter()
    num_guessed = Counter()
    gold_num = Counter()
    num_right = 0
    total = 0
    
    eval_pairs = zip(gold, results)
    for ((fs,l), r) in eval_pairs:
        num_guessed[r] += 1
        gold_num[l] += 1
        total += 1
        if l == r:
            num_right += 1
            sys_correct_dict[l] += 1

    accuracy = float(num_right)/total
    precision_dict = {}
    recall_dict = {}
    for l in gold_num:
        if gold_num[l] > 0:
            recall_dict[l] = float(sys_correct_dict[l])/gold_num[l]
        else:
            recall_dict[l] = 0.0
        if num_guessed[l] > 0:
            precision_dict[l] = float(sys_correct_dict[l])/num_guessed[l]
        else:
            precision_dict[l] = 0.0
            
    return accuracy, precision_dict, recall_dict, total, sys_correct_dict
    


    
    

if __name__ == '__main__':
    import sys, time
    if len(sys.argv) > 1:
        event_file = sys.argv[1]
        if len(sys.argv) > 2:
            max_iter = int(sys.argv[2])
        else:
            max_iter = 50
    else:
        print 'Usage: %s <filename>' % (sys.argv[0],)
        sys.exit()
    start = time.time()
    classifier = wsd_demo(event_file,maxent.MaxentClassifier.train,4100,max_iter=max_iter,algorithm='iis')
    end = time.time()
    print 
    print '***Max Ent Training/test time***: {0:.4f}'.format(end - start)
    print
    print
    featuretypes =  ['pos', 'neg', 'all']
    ## Choose one of the three above
    featuretype = 'pos'
    assert featuretype in featuretypes, 'Illegal feature type chosen!'
    #classifier.show_most_informative_features(n=20,include_zeros=False)
    #classifier.show_most_informative_features(n=20,show = featuretype)
    classifier.show_most_informative_features(n=20)
    # note when featuretype = neg we show no feats
    # Note: The C{explain} method applies to the featureset of a single example.
    # Here we explain the first example on the test set.
    test_index = 0
    #print """
    #The following feature set is extracted from an
    #example that is in fact a use of sense %s.
    #The probabilities assigned at the bottom of the explanation below
    #show that this example is correctly classified""" % (test[test_index][1],)
    #classifier.explain(featureset = test[test_index][0])


    #### Naive bayes
    print
    print '='*40
    print ' '*14, 'NAIVE BAYES', ' '*14
    print '='*40
    print
    
    from nltk.classify import naivebayes
    nb_start = time.time()
    nb_classifier = wsd_demo(event_file,naivebayes.NaiveBayesClassifier.train,4100)
    nb_end = time.time()
    print
    print '***NB Training/test time***: {0:.4f}'.format(nb_end - nb_start)
    print
    print
    nb_classifier.show_most_informative_features(n=20)
