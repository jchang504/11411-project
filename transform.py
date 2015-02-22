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
  return copula + ' ' + tree_to_string(tree[0]) + ' ' + tree_to_string(tree[1])

def is_singular(np):
  # TODO: implement. Recursively looks for the head noun, and compares
  # singularize(head_noun) == head_noun to determine if it's singular
  pass

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
