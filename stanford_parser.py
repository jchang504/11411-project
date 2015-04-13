import os
from nltk.parse.stanford import StanfordParser

# creates an NLTK interface to the Stanford parser installed on user's machine
def create_parser(user):
    set_params(user)
    return StanfordParser(model_path=ENGLISH_PCFG_LOC)

# locations of Stanford parser/models, Java, and English PCFG model
USER_STANFORD_PARAMS = {}
JEMMIN_HOME_ROOT = '/usr/lib/stanford-parser-full-2015-01-30'
USER_STANFORD_PARAMS['Jemmin_home'] = [JEMMIN_HOME_ROOT, JEMMIN_HOME_ROOT, '/usr/bin/java', JEMMIN_HOME_ROOT + '/englishPCFG.ser.gz']
JEMMIN_GHC_ROOT = '/afs/andrew.cmu.edu/usr/jemminc/nlp_project/stanford-parser-full-2014-08-27'
USER_STANFORD_PARAMS['Jemmin_ghc'] = [JEMMIN_GHC_ROOT, JEMMIN_GHC_ROOT, '/usr/bin/java', JEMMIN_GHC_ROOT + '/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz']

# sets EVs and ENGLISH_PCFG_LOC to correct values for given user
def set_params(user):
  params = USER_STANFORD_PARAMS[user]
  os.environ['STANFORD_PARSER'] = params[0]
  os.environ['STANFORD_MODELS'] = params[1]
  os.environ['JAVAHOME'] = params[2]
  global ENGLISH_PCFG_LOC
  ENGLISH_PCFG_LOC = params[3]
