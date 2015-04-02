# more readable names for Stanford parser constituent tags
# in alphabetical order by tag

NUMBER = 'CD'
DET = 'DT'
PREP = 'IN'
ADJ = 'JJ'
MODAL = 'MD'
NOUN = 'NN'
NOUN_PROPER = 'NNP'
NOUN_PL = 'NNS'
NP = 'NP'
POSS = 'POS'
PP = 'PP'
PRONOUN = 'PRP'
PRONOUN_POSS = 'PRP$'
SENTENCE = 'S'
TO = 'TO'
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

def is_plural(noun_label):
  return noun_label.endswith('S')
