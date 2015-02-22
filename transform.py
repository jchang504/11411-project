#!/usr/bin/python

# TODO: only if __name__ == __main__ for putting together
from pattern.en import conjugate, lemma, PAST, PRESENT, SG, PL
from nltk.tree import *

# what we need from previous part (pattern extraction): exactract the constituent of the tree matching exactly these patterns, and ***avoid sentences with pronouns

# Stanford parser constituent labels:
NP = 'NP'
VP = 'VP'
COMMA = ','
VERB_PAST = 'VBD'
VERB_PLURAL = 'VBP'
VERB_3SG = 'VBZ'
PROPER_NOUN = 'NNP'
MODAL = 'MD'

# hardcoded patterns
# TODO: add more
# [NP, VP]
SIMPLE_PREDICATION = 0
# [NP, COMMA, NP, COMMA]
APPOSITION = 1

# test trees
# simple predicates
TREE_1 = Tree.fromstring('(S (NNP John) (VP (VP (VBD ate) (NP (DT a) (NN burrito))) (PP (IN in) (NP (DT the) (NN park)))))')
TREE_2 = Tree.fromstring('(S (NP (DT A) (NN burrito)) (VP (VBD was) (VP (VBN eaten) (PP (IN by) (NP (NNP John))))))')
TREE_3 = Tree.fromstring('(S (NP (NNP John)) (VP (VBZ is) (NP (DT a) (NN man))))')
TREE_4 = Tree.fromstring('(S (NP (DT The) (NN dog)) (VP (ADVP (RB quickly)) (VBD ate) (NP (DT a) (JJ big) (NN burrito))))')
TREE_5 = Tree.fromstring('(S (NP (NNP John)) (VP (VBZ has) (VP (VBN eaten) (NP (NNS burritos)))))')
TREE_6 = Tree.fromstring('(S (NP (NNP John)) (VP (VBZ has) (NP (JJ great) (NN burrito) (NN sauce))))')
TREE_7 = Tree.fromstring('(S (NP (NNP John)) (VP (MD might) (VP (VB have) (VP (VBN eaten) (NP (DT the) (JJ wrong) (NN burrito))))))')
# Appositions
TREE_8 = Tree.fromstring('(NP (NP (NNP John)) (, ,) (NP (DT a) (NN man)) (, ,))')
TREE_9 = Tree.fromstring('(NP (NP (PRP$ Their) (NNS brothers)) (, ,) (NP (DT a) (JJ handsome) (NN lot)) (, ,))')


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
  if is_modal(verb, vp) or lemma(verb_word) == 'be':
    uncap(np) # uncapitalize original first word (unless it's NNP)
    return verb_word.capitalize() + ' ' + tree_to_string(np) + ' ' + ' '.join(vp.leaves()[1:]) + '?' # TODO: hacky - deletes first word of vp
  else:
    verb[0] = lemma(verb_word) # convert head verb to infinitive
    uncap(np) # uncapitalize original first word (unless it's NNP)
    return conjugate('do', get_inflection(verb)).capitalize() + ' ' + tree_to_string(np) + ' ' + tree_to_string(vp) + '?'

def apposition_binary_q(tree):
  np_1 = tree[0]
  np_2 = tree[2]
  copula = 'Are' if is_plural(get_noun(np_1)) else 'Is'
  uncap(np_1)
  return copula + ' ' + tree_to_string(np_1) + ' ' + tree_to_string(np_2) + '?'

# return True iff the verb is a modal or modal 'have'
def is_modal(verb, vp):
  # hack - assumes 'have' is vp[0].
  # Counterexample: 'John definitely has eaten bread' (Stanford parses this wrong though, and it may be ungrammatical - i.e. not a problem)
  return verb.label() == MODAL or (lemma(verb[0]) == 'have' and vp[1].label() != 'NP')

# TODO: switch in hyper/hypo-nyms, synonyms, etc. from WordNet
def confound():
  pass

# return a string of the leaves of the tree
def tree_to_string(tree):
  return " ".join(tree.leaves())

# gets the leftmost leaf node of tree
def first_word(tree):
  node = tree
  while isinstance(node[0], Tree):
    node = node[0]
  return node

# uncapitalizes the phrase, unless its first word is a proper noun
def uncap(phrase):
  first = first_word(phrase)
  if first.label() != PROPER_NOUN:
    first[0] = first[0].lower()

# returns the verb which heads (possibly indirectly) vp
def get_verb(vp):
  node = vp
  while node.label() == VP:
    for child in node: # move down to the first child which is a VP or verb
      if child.label().startswith('V') or child.label() == MODAL:
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
  return noun.label().endswith('S')
