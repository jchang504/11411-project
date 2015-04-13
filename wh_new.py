# hardcoded patterns for extracting wh-question transformable sentences

from nltk.tree import Tree
from tags import *
import copy

# if this sentence_tree is suitable for asking a 'how many' question, return
# a copy of the tree with the gap constituent removed; else return None
# REQUIRES: sentence_tree is a Tree matching SIMPLE_PREDICATE
def how_many(sentence_tree):
  np = sentence_tree[0]
  vp = sentence_tree[1]

  # number NP in subject position
  if is_number_np(np):
    gappy = copy.deepcopy(sentence_tree)
    del gappy[0]
    return gappy

  # check for number NP in object position
  verb_head = vp[0]
  if is_tensed_verb(verb_head.label()):
    if len(vp) >= 2:
      obj = vp[1]
      if obj.label() == NP and is_number_np(obj):
        gappy = copy.deepcopy(sentence_tree)
        del gappy[1,1]
        return gappy

# returns True if this NP is a number NP (e.g. '10 white chickens')
def is_number_np(np):
  if np[0].label() != NUMBER:
    return False
  for i in xrange(1, len(np)-1):
    if np[i].label() != ADJ:
      return False
  return np[-1].label() == NOUN_PL

# if this sentence_tree is suitable for asking a 'how' question, return
# a copy of the tree with the gap constituent removed; else return None
# REQUIRES: sentence_tree is a Tree matching SIMPLE_PREDICATE
def how(sentence_tree):
  vp = sentence_tree[1]

  verb_head = vp[0]
  if is_tensed_verb(verb_head.label()):
    if len(vp) >= 2:
      vp_index = 1
      node = vp[vp_index]
      # skip past intervening NP or PP
      if node.label() != ADVP:
        if len(vp) > 2:
          vp_index = 2
          node = vp[vp_index]
        else:
          return None

      # found ADVP?
      if node.label() == ADVP:
        gappy = copy.deepcopy(sentence_tree)
        del gappy[1,vp_index]
        return gappy

# if this sentence_tree is suitable for asking a 'why' question, return
# a copy of the tree with the gap constituent removed; else return None
# REQUIRES: sentence_tree is a Tree matching SIMPLE_PREDICATE
def why(sentence_tree):
  vp = sentence_tree[1]

  verb_head = vp[0]
  if is_tensed_verb(verb_head.label()):
    if len(vp) >= 2:
      vp_index = 1
      node = vp[vp_index]
      # skip past intervening NP or ADJP
      if node.label() != SBAR:
        if len(vp) > 2:
          vp_index = 2
          node = vp[vp_index]
        else:
          return None

      # found SBAR?
      if node.label() == SBAR:
        because = node[0]
        if because.label() == PREP and because[0] == 'because':
          gappy = copy.deepcopy(sentence_tree)
          del gappy[1,vp_index]
          return gappy
