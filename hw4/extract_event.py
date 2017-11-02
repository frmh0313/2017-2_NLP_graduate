"""

This module defines the class EventEncoder (object) which provides a
general purpose interface between a feature encoder appropriate for
machine learning and XML corpora with events that are segments of
text.

The key method in C{EventEncoder} is  C{parse_xml_file_and_extract_events},
which extracts schematic events from an XML corpus, creating what we call an
C{event_list}.  An event list is a list of event-dictionary,
class pairs, each corresponding to an event to be trained on by some
classifier. Each event dictionary has a feature C{context} containing
the text of an annotated example, and whatever example attributes
(such as id, target word position) the corpus implements.

The C{parse_xml_file_and_extract_events} method does NOT do feature
encoding.  It just transforms the XML into a standard format
represented in a user-provided Training Instance, and tries not to
throw away any of the corpus information. The user-provided training
instances must be some specialization of the TrainingInst
class provided here.  Essentially the user provides
the class attribute which is the text feature we are trying to predict
(for example, the word sense of some target word), and the 
other attributes of a corpus event of interest.

The EventEncoder class also provides a  method called C{encode_events},
which extracts features from the events on the event list, given
a corpus-specific function that creates a feature dictionary from a
text event. 

The XML corpus must be in the following format

<node_sequence>
<node att1=val1 att2=val2 ...>
text1  
</node>

<node att1=val1 att2=val2 ...>
text2
</node>

....

</node_sequence>

For the first event C{parse_file_and_extract_events} returns a dictionary
containing text1 as the value of the C{context}
attribute, and val1, val2, ... as the values of att1, att2,...

Tags are supported but currently only separated by underscore from the word.
Further tags embedded around text within the contyext are not currently supported.


"""

import sys,os.path, random, subprocess
import xml.dom.minidom,re
from collections import Counter,defaultdict


class EventEncoder (object):

    def __init__(self, event_class):
        self.maker_fn = event_class
        try:
            self.att_list = event_class.att_list
            self.class_att = event_class.class_att
        except:
            print "The attributes 'class_att' and 'att_list' must be defined for class %s" % (event_class.__name__,)
        self.event_list = []
        self.encoded_events = []
        self.encoded_features = set()
        self.classes = set()

    def parse_xml_file_and_extract_events(self, xml_file,node_sequence_name,\
                                          node_name,tagging=True):
        print 'Reading %s' % (xml_file,)
        with open(xml_file,'r') as g:
            g_doc = xml.dom.minidom.parse(g)
        self.extract_events(g_doc, node_sequence_name,\
                            node_name, tagging=tagging)

    def extract_events (self, node, node_sequence_name,\
                        node_name, tagging=True):
        """
        C{node} is the root of an xml.dom.minidom tree for a corpus
        XML file.  Construct a list of events (feature-dict, class pairs).
        """
        event_list = self.event_list
        while node:
            if node.nodeType == node.ELEMENT_NODE and node.nodeName==node_sequence_name:
                #sis = node.getElementsByTagName(node_name)
                #print sis, node_name,node.nodeName
                sis = node.getElementsByTagName(node_name)
                for si in sis:
                    class_att_val = si.getAttribute(self.class_att)
                    self.classes.add(class_att_val)
                    #print class_att_val
                    #position = int(si.getAttribute('position'))
                    #inst_id = si.getAttribute('id')
                    event_feats = \
                             dict(zip(self.att_list, [si.getAttribute(att) for att in self.att_list]))
                    sentence = si.firstChild.wholeText
                    if tagging:
                        #Now make sentence a list of word tag strings
                        #might want to apply some transform to each string;
                        #hence this useless line of code
                        context = [wordtag for wordtag in sentence.split()]
                    else:
                        context = sentence.split()
                    inst = self.maker_fn(context, **event_feats)
                    # Now extract features from the list C{context}.
                    # C{context[position]} returns our word of interest.
                    # print context
                    event_list.append((inst,class_att_val))
            self.extract_events (node.firstChild, node_sequence_name, \
                                 node_name, tagging)
            node = node.nextSibling



    def encode_events (self, feature_extractor, feats):
        """
        C{feature_extractor} is a function that produces a dictionary that
        represents the features of an event.  C{feats} is a dictionary whose keys
        define that set of feastures that must be defined for each event.

        Encode each event in C{self.event_list} as a feature_dictionary, class pair.
        Store the list  of same in C{self.encoded_events}.
        """

        self.encoded_events = [] 
        encoded_events =  self.encoded_events
        
        for (s_inst, sense) in self.event_list:
            context = s_inst.context
            att_dict =  dict(zip(self.att_list, [getattr(s_inst,att) for att in self.att_list]))
            feature_dict = feature_extractor(context, feats, **att_dict)
            encoded_events.append((feature_dict,sense))

        self.get_encoding_sets()

    def write_encoded_event_file (self, event_file):
        if os.path.isfile(event_file):
            os.rename(event_file,event_file + '.bak')

        if not hasattr(self,'encoded_events') or self.encoded_events is []:
            print "You must run the 'encode_events' method first"
            
        with open(event_file, 'w') as e_fh:
            for (feature_dict, sense) in self.encoded_events:
                self.print_event(e_fh,feature_dict,sense)

    def get_encoding_sets (self):
        if not hasattr(self,'encoded_events') or self.encoded_events is []:
            print "You must run the 'encode_events' method first"

        classes = []
        self.classes = classes
        features = defaultdict(set)
        self.features = features

        for (feature_dict, sense) in self.encoded_events:
            if sense not in classes:
                classes.append(sense)
            for (f,v) in feature_dict.iteritems():
                features[f].add(v)
            
    def get_class_stats (self):
        ctr = Counter()
        self.class_stats = ctr
        for (s_inst, sense) in self.event_list:
            ctr[sense] += 1

    def print_class_stats (self):
        class_stats = self.class_stats
        total = float(sum(class_stats.values()))
        for (k,v) in class_stats.iteritems():
            print '%-20s %4d %.3f' % (k, v, v/total)

    def print_event (self, fh,feature_dict,sense):
        print >> fh, 'BEGIN EVENT'
        print >> fh, sense
        for k in feature_dict:
            print >> fh, '%s\t%s' % (k,feature_dict[k])
            self.encoded_features.add(self.make_me_feat(k,sense))
        print >> fh, 'END EVENT'

    def make_me_feat (self, feat, cls):
        return '%s_%s' % (feat,cls)

    def read_vocab_file (self,filename):
        """
        C{filename} contains a list of features selected
        by a feature selection algorithm like that of Berger etal
        (1996), implemented in YasmetFS.  The features are in the
        order discovered and the task will be to determine,
        when to stop adding features.  Read in all features now,
        preserving order.
        """
        feature_ordering = []
        
        with open(filename,'r') as fh:
            for line in fh:
                line = line.strip()
                feature_ordering.append(line)

        return feature_ordering
        
class TrainingInst (object):
    """
    The first arg of the __init__ method should always be the
    C{context} (bearing the text whose attributes we are using to
    classify).  The remaining args (and there are any number of them)
    are all miscellaneous event features, not to be confused with the
    features we will eventually extract (from the C{context}) to
    predict the class.
    """

    def __init__(self,context,**atts):
        assert self.class_att and self.att_list, "The attributes 'class_att' and 'att_list' must be defined!"
        self.context = context
        for att in self.att_list:
            setattr(self,att, atts[att])

