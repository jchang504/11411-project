# more readable names for Stanford parser constituent tags
# in alphabetical order by tag

MODAL = 'MD'
NOUN = 'NN'
NOUN_PROPER = 'NNP'
NOUN_PL = 'NNS'
NP = 'NP'
PRONOUN = 'PRP'
SENTENCE = 'S'
VERB_PAST = 'VBD'
VERB_PLURAL = 'VBP'
VERB_3SG = 'VBZ'
VP = 'VP'
WHNP = 'WHNP'
WHADVP = 'WHADVP'
COMMA = ','
PERIOD = '.'

# hardcoded patterns for extraction

SIMPLE_PREDICATE = (SENTENCE, (NP, VP, PERIOD))
APPOSITION = (NP, (NP, COMMA, NP, COMMA))
PATTERNS = [SIMPLE_PREDICATE, APPOSITION]
