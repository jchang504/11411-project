#!/usr/bin/python

import os
from nltk.parse.stanford import StanfordParser

# creates an NLTK interface to the Stanford parser installed on user's machine
def create_parser(user):
    set_params(user)
    return StanfordParser(model_path=ENGLISH_PCFG_LOC)

# locations of Stanford parser/models, Java, and English PCFG model
USER_STANFORD_PARAMS = {}
JEMMIN_STANFORD_ROOT = '/usr/lib/stanford-parser-full-2015-01-30'
USER_STANFORD_PARAMS['Jemmin'] = [JEMMIN_STANFORD_ROOT, JEMMIN_STANFORD_ROOT, '/usr/bin/java', JEMMIN_STANFORD_ROOT + '/englishPCFG.ser.gz']
ASHLEY_STANFORD_ROOT = '/usr/local/Cellar/stanford-parser/3.4/libexec'
USER_STANFORD_PARAMS['Ashley'] = [ASHLEY_STANFORD_ROOT, ASHLEY_STANFORD_ROOT, '/Library/Java/JavaVirtualMachines/jdk1.7.0_67.jdk/Contents/Home/jre/bin', ASHLEY_STANFORD_ROOT + '/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz']

# sets EVs and ENGLISH_PCFG_LOC to correct values for given user
def set_params(user):
  params = USER_STANFORD_PARAMS[user]
  os.environ['STANFORD_PARSER'] = params[0]
  os.environ['STANFORD_MODELS'] = params[1]
  os.environ['JAVAHOME'] = params[2]
  global ENGLISH_PCFG_LOC
  ENGLISH_PCFG_LOC = params[3]
