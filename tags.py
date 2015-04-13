# more readable names for Stanford parser constituent tags
# in alphabetical order by tag

ADJP = 'ADJP'
ADVP = 'ADVP'
NUMBER = 'CD'
DET = 'DT'
PREP = 'IN'
ADJ = 'JJ'
ADJ_COMP = 'JJR'
ADJ_SUP = 'JJS'
MODAL = 'MD'
NOUN = 'NN'
NOUN_PROPER = 'NNP'
NOUN_PL = 'NNS'
NP = 'NP'
POSS = 'POS'
PP = 'PP'
PRONOUN = 'PRP'
PRONOUN_POSS = 'PRP$'
ROOT = 'ROOT'
SENTENCE = 'S'
SBAR = 'SBAR'
WH_QUESTION = 'SBARQ'
BIN_QUESTION = 'SQ'
TO = 'TO'
VERB_INF = 'VB'
VERB_PAST = 'VBD'
VERB_PLURAL = 'VBP'
VERB_3SG = 'VBZ'
VP = 'VP'
WHNP = 'WHNP'
WHADJP = 'WHADJP'
WHADVP = 'WHADVP'
WDT = 'WDT'
WP_POSS = 'WP$'
COMMA = ','
PERIOD = '.'

# helper functions

def is_verb(label):
  return label.startswith('V') or label == 'MD'

def is_noun_head(label):
  return label.startswith('NN')

def is_adjective(label):
  return label.startswith('JJ')

def is_tensed_verb(label):
  return label in [VERB_PAST, VERB_PLURAL, VERB_3SG]

def is_plural(noun_label):
  return noun_label.endswith('S')

# Stanford 7-class NER Tagger class names

LOCATION = 'LOCATION'
ORGANIZATION = 'ORGANIZATION'
DATE = 'DATE'
MONEY = 'MONEY'
PERSON = 'PERSON'
PERCENT = 'PERCENT'
TIME = 'TIME'
