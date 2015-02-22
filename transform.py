#!/usr/bin/python

from pattern.en import conjugate, lemma, PAST, PRESENT, SG, PL

# what we need from previous part (pattern extraction): exactract the constituent of the tree matching exactly these patterns, and ***avoid sentences with pronouns

# English modal verbs
MODALS = ['can', 'have', 'may', 'might', 'must', 'shall', 'will']

# Constituent symbols:
NP = "NP"
COMMA = ","
VP = "VP"

# hardcoded patterns
# TODO: add more
# [NP, VP]
SIMPLE_PREDICATION = 0
# [NP, NP]
APPOSITION = 1

# test trees
# TODO: added singletons - need to retest!
TREE_1 = [['John'], [['ate'], [['a'], ['burrito']]]]
TREE_2 = [['John'], [[['ate'], [['a'], ['burrito']]], [['in'], [['the'], ['park']]]]]
TREE_3 = [[['A'], ['burrito']], [[['was'], ['eaten']], [['by'], ['John']]]]
TREE_4 = [['John'], [['is'], [['a'], ['man']]]]
TREE_5 = [['John'], [['a'], ['man']]]
TREE_6 = [[['Their'], ['brothers']], [['successful'], ['farmers']]]

# abstraction function: parses raw tree into nested list format
def parse_tree(raw_tree):
  # TODO: actual parsing code when we find out what format trees will be in
  return raw_tree

# transform parsed tree (constituent, not necessarily sentence) into question
def transform(tree, pattern):
  if pattern == SIMPLE_PREDICATION:
    return simple_pred_binary_q(tree)
  elif pattern == APPOSITION:
    return apposition_binary_q(tree)

# transform a simple predicate constituent into a binary question
def simple_pred_binary_q(tree):
  # TODO: uncapitalization of original first word (except if PropN)
  flat_VP = flatten(tree[1])
  v = flat_VP[0]
  if is_modal(v) or lemma(v) == 'be':
    return v.capitalize() + ' ' + tree_to_string(tree[0]) + ' ' + tree_to_string(flat_VP[1:]) + '?'
  else:
    return conjugate('do', get_inflection(v)).capitalize() + ' ' + tree_to_string(tree[0]) + ' ' + lemma(v) + ' ' + tree_to_string(flat_VP[1:]) + '?'
def apposition_binary_q(tree):
  # TODO: fill in
  copula = 'Is' if is_singular(tree[0]) else 'Are'
  return copula + ' ' + tree_to_string(tree[0]) ' ' + tree_to_string(tree[1])

def is_singular(np):
  # TODO: implement. Recursively looks for the head noun, and compares
  # singularize(head_noun) == head_noun to determine if it's singular

def is_modal(word):
  # TODO: 'have' is tricky - need to look at next word
  return word in MODALS

def flatten(tree):
  if isinstance(tree, str):
    return [tree]
  else:
    flattened = []
    for child in tree:
      flattened.extend(flatten(child))
    return flattened

# flatten the syntax tree into a string
def tree_to_string(tree):
  return " ".join(flatten(tree))

# gets the first word of a constituent, which may be arbitrarily deeply nested
# TODO: maybe don't need this anymore now that we have flatten?
def get_first_word(constituent):
  current_constituent = constituent
  while isinstance(current_constituent, list):
    current_constituent = current_constituent[0]
  return current_constituent

# Alias strings
ALIAS_PAST = 'p'
ALIAS_REG = 'inf'
ALIAS_3SG = '3sg'
# returns the alias corresponding to the verb's distinguishable inflection,
# i.e. ALIAS_PAST for all past tense verbs, ALIAS_REG for "regular" (non-3rd
# person singular) present tense verbs, and ALIAS_3SG for 3rd-person singular
# present tense verbs
# Do NOT use for irregular verb 'to be' or modals!
def get_inflection(verb):
  base_form = lemma(verb)
  if verb == base_form:
    return ALIAS_REG
  elif verb == conjugate(base_form, '3sg'):
    return ALIAS_3SG
  elif verb == conjugate(base_form, PAST) or verb == conjugate(base_form, 'ppart'):
    return ALIAS_PAST
  else:
    # TODO: a little hacky
    if verb[-1] == 's':
      return ALIAS_3SG
    else:
      return ALIAS_REG

def test_get_inflection():
  assert(ALIAS_PAST == get_inflection('killed'))
  assert(ALIAS_PAST == get_inflection('purred'))
  assert(ALIAS_PAST == get_inflection('canned'))
  assert(ALIAS_PAST == get_inflection('broke'))
  assert(ALIAS_PAST == get_inflection('swam'))
  assert(ALIAS_PAST == get_inflection('could'))
  assert(ALIAS_PAST == get_inflection('had'))
  assert(ALIAS_PAST == get_inflection('halved'))
  assert(ALIAS_PAST == get_inflection('redistributed'))
  assert(ALIAS_PAST == get_inflection('thwacked'))

  assert(ALIAS_REG == get_inflection('kill'))
  assert(ALIAS_REG == get_inflection('purr'))
  assert(ALIAS_REG == get_inflection('break'))
  assert(ALIAS_REG == get_inflection('eat'))
  assert(ALIAS_REG == get_inflection('swim'))
  assert(ALIAS_REG == get_inflection('have'))
  assert(ALIAS_REG == get_inflection('halve'))

  assert(ALIAS_3SG == get_inflection('kills'))
  assert(ALIAS_3SG == get_inflection('purrs'))
  assert(ALIAS_3SG == get_inflection('breaks'))
  assert(ALIAS_3SG == get_inflection('eats'))
  assert(ALIAS_3SG == get_inflection('swims'))
  assert(ALIAS_3SG == get_inflection('has'))
  assert(ALIAS_3SG == get_inflection('halves'))
  assert(ALIAS_3SG == get_inflection('redistributes'))
  assert(ALIAS_3SG == get_inflection('thwacks'))
  assert(ALIAS_3SG == get_inflection('cans'))

def test_get_first_word():
  assert('ate' == get_first_word(TREE_1[1]))
  assert('ate' == get_first_word(TREE_2[1]))
  assert('was' == get_first_word(TREE_3[1]))
  assert('is' == get_first_word(TREE_4[1]))

def test_flatten():
  assert(['John', 'ate', 'a', 'burrito'] == flatten(TREE_1))
  assert(['John', 'ate', 'a', 'burrito', 'in', 'the', 'park'] == flatten(TREE_2))
  assert(['A', 'burrito', 'was', 'eaten', 'by', 'John'] == flatten(TREE_3))
  assert(['John', 'is', 'a', 'man'] == flatten(TREE_4))

def test_tree_to_string():
  assert('John ate a burrito' == tree_to_string(TREE_1))
  assert('John ate a burrito in the park' == tree_to_string(TREE_2))
  assert('A burrito was eaten by John' == tree_to_string(TREE_3))
  assert('John is a man' == tree_to_string(TREE_4))

def test_simple_pred_binary_q():
  print 'These should be well-formed, grammatical questions:'
  print simple_pred_binary_q(TREE_1)
  print simple_pred_binary_q(TREE_2)
  print simple_pred_binary_q(TREE_3)
  print simple_pred_binary_q(TREE_4)

TEST = True
if TEST:
  print 'Testing...'
  test_get_inflection()
  test_get_first_word()
  test_flatten()
  test_tree_to_string()
  test_simple_pred_binary_q()
  print '\nAll good!'
