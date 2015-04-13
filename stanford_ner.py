#!/usr/bin/python

from nltk.tag.stanford import NERTagger

# locations of Stanford parser/models, Java, and English PCFG model
USER_STANFORD_PARAMS = {}
JEMMIN_HOME_ROOT = '/usr/lib/stanford-ner-2014-08-27'
USER_STANFORD_PARAMS['Jemmin_home'] = [JEMMIN_HOME_ROOT + '/classifiers/english.muc.7class.distsim.crf.ser.gz', JEMMIN_HOME_ROOT + '/stanford-ner.jar'] 
JEMMIN_GHC_ROOT = '/afs/andrew.cmu.edu/usr10/jemminc/nlp_project/stanford-ner-2014-08-27'
USER_STANFORD_PARAMS['Jemmin_ghc'] = [JEMMIN_GHC_ROOT + '/classifiers/english.muc.7class.distsim.crf.ser.gz', JEMMIN_GHC_ROOT + '/stanford-ner.jar'] 

# creates an NLTK interface to the Stanford NER Tagger installed on user's
# machine
def create_tagger(user):
    params = USER_STANFORD_PARAMS[user]
    return NERTagger(params[0], params[1])
