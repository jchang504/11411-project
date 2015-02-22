#!/usr/bin/python

from pattern.en import conjugate, lemma, PAST, PRESENT, SG, PL
from nltk.tree import *

# what we need from previous part (pattern extraction): exactract the constituent of the tree matching exactly these patterns, and ***avoid sentences with pronouns

# English modal verbs
MODALS = ['can', 'have', 'may', 'might', 'must', 'shall', 'will']

# Stanford parser constituent labels:
NP = 'NP'
VP = 'VP'
VERB_PAST = 'VBD'
VERB_PLURAL = 'VBP'
VERB_3SG = 'VBZ'
PROPER_NOUN = 'NNP'

# hardcoded patterns
# TODO: add more
# [NP, VP]
SIMPLE_PREDICATION = 0
# [NP, NP]
APPOSITION = 1

# test trees
TREE_1 = Tree.fromstring('(S (NP (NNP John)) (VP (VBD ate) (NP (DT a) (NN burrito))))')
TREE_2 = Tree.fromstring('(S (NNP John) (VP (VP (VBD ate) (NP (DT a) (NN burrito))) (PP (IN in) (NP (DT the) (NN park)))))')
TREE_3 = Tree.fromstring('(S (NP (DT A) (NN burrito)) (VP (VBD was) (VP (VBN eaten) (PP (IN by) (NP (NNP John))))))')
TREE_4 = Tree.fromstring('(S (NP (NNP John)) (VP (VBZ is) (NP (DT a) (NN man))))')
TREE_5 = Tree.fromstring('(S (NP (DT The) (NN dog)) (VP (ADVP (RB quickly)) (VBD ate) (NP (DT a) (JJ big) (NN burrito))))')
TREE_6 = Tree.fromstring('(NP (NP (NNP John)) (, ,) (NP (DT a) (NN man)) (, ,))')
TREE_7 = Tree.fromstring('(NP (NP (PRP$ Their) (NNS brothers)) (, ,) (NP (DT a) (JJ handsome) (NN lot)) (, ,))')

# transform parsed tree (constituent, not necessarily sentence) into question
def transform(tree, pattern):
  if pattern == SIMPLE_PREDICATION:
    return simple_pred_binary_q(tree)
  elif pattern == APPOSITION:
    return apposition_binary_q(tree)

# transform a simple predicate constituent into a binary question
def simple_pred_binary_q(tree):
  np = tree[0]
  vp = tree[1]
  verb = get_verb(vp)
  verb_word = verb[0]
  if is_modal(verb_word) or lemma(verb_word) == 'be':
    uncap(np) # uncapitalize original first word (unless it's NNP)
    return verb_word.capitalize() + ' ' + tree_to_string(np) + ' ' + ' '.join(vp.leaves()[1:]) + '?' # TODO: hacky - deletes first word of vp
  else:
    verb[0] = lemma(verb_word) # convert head verb to infinitive
    uncap(np) # uncapitalize original first word (unless it's NNP)
    return conjugate('do', get_inflection(verb)).capitalize() + ' ' + tree_to_string(np) + ' ' + tree_to_string(vp) + '?'

def apposition_binary_q(tree):
  # TODO: fill in
  pass

def is_modal(word):
  # TODO: 'have' is tricky - need to look at next word in VP
  return word in MODALS

# TODO: switches in hyper/hypo-nyms, synonyms, etc. from WordNet
def confound():
  pass

# return a string of the leaves of the tree
def tree_to_string(tree):
  return " ".join(tree.leaves())

# uncapitalizes the phrase, unless its first word is a proper noun
def uncap(phrase):
  node = phrase
  while isinstance(node[0], Tree):
    node = node[0]
  if node.label() != PROPER_NOUN:
    node[0] = node[0].lower()

# returns the verb which heads (possibly indirectly) vp
def get_verb(vp):
  node = vp
  while node.label() == VP:
    for child in node: # move down to the first child which is a VP or verb
      if child.label().startswith('V'):
        node = child
        break
  return node

# Alias strings
ALIASES = {VERB_PAST: 'p', VERB_PLURAL: 'inf', VERB_3SG: '3sg'}
# returns the alias corresponding to the VP's distinguishable inflection
def get_inflection(verb):
  return ALIASES[verb.label()]

# returns the noun which heads (possible indirectly) np
def get_noun(np):
  node = np
  while node.label() == NP:
    for child in node: # move down to the first child which is an NP or noun
      if child.label().startswith('N'):
        node = child
        break
  return node

# returns true iff noun is plural
def is_plural(noun):
  return noun.endswith('S')
