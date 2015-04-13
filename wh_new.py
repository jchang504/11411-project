# hardcoded patterns for extracting wh-question transformable sentences

# each of these is similar, but slightly individualized... massive code
# duplication, but it made it faster to write... :\

from nltk.tree import Tree
from tags import *
import copy

# if this sentence_tree is suitable for asking a 'how many' question, return
# a list of all possible gappy trees
# REQUIRES: sentence_tree is a Tree matching SIMPLE_PREDICATE
def how_many(sentence_tree):
  np = sentence_tree[0]
  vp = sentence_tree[1]
  gappies = []

  # number NP in subject position
  if is_number_np(np):
    gappy = copy.deepcopy(sentence_tree)
    del gappy[0]
    gappies.append(gappy)

  # check for number NP in object position
  verb_head = vp[0]
  if is_tensed_verb(verb_head.label()):
    if len(vp) >= 2:
      obj = vp[1]
      if obj.label() == NP and is_number_np(obj):
        gappy = copy.deepcopy(sentence_tree)
        del gappy[1,1]
        gappies.append(gappy)

  return gappies

# returns True if this NP is a number NP (e.g. '10 white chickens')
def is_number_np(np):
  if np[0].label() != NUMBER:
    return False
  for i in xrange(1, len(np)-1):
    if np[i].label() != ADJ:
      return False
  return np[-1].label() == NOUN_PL

# if this sentence_tree is suitable for asking a 'how' question, return
# a list of all possible gappy trees
# REQUIRES: sentence_tree is a Tree matching SIMPLE_PREDICATE
def how(sentence_tree):
  vp = sentence_tree[1]
  gappies = []

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

      # found ADVP?
      if node.label() == ADVP:
        gappy = copy.deepcopy(sentence_tree)
        del gappy[1,vp_index]
        gappies.append(gappy)

  return gappies

# if this sentence_tree is suitable for asking a 'why' question, return
# a list of all possible gappy trees
# REQUIRES: sentence_tree is a Tree matching SIMPLE_PREDICATE
def why(sentence_tree):
  vp = sentence_tree[1]
  gappies = []

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

      # found SBAR?
      if node.label() == SBAR:
        because = node[0]
        if because.label() == PREP and because[0] == 'because':
          gappy = copy.deepcopy(sentence_tree)
          del gappy[1,vp_index]
          gappies.append(gappy)

  return gappies

# if this sentence_tree is suitable for asking a 'what' question, return
# a list of all possible gappy trees
# REQUIRES: sentence_tree is a Tree matching SIMPLE_PREDICATE, ner_tagged is
# the NER-tagged sentence (a list of tuples (word, tag))
def what(sentence_tree, ner_tags):
  np = sentence_tree[0]
  vp = sentence_tree[1]
  gappies = []

  # non-person NP in subject position
  if not is_ne(sentence_tree, [0], ner_tags, PERSON):
    gappy = copy.deepcopy(sentence_tree)
    del gappy[0]
    gappies.append(gappy)

  # check for non-person NP in object position
  verb_head = vp[0]
  if is_tensed_verb(verb_head.label()):
    if len(vp) >= 2:
      obj = vp[1]
      if obj.label() == NP and not is_ne(sentence_tree, [1,1], ner_tags,
          PERSON):
        gappy = copy.deepcopy(sentence_tree)
        del gappy[1,1]
        gappies.append(gappy)

  return gappies

# returns True iff the constituent at indices in the sentence_tree is tagged
# with ne_class in the ner_tags
def is_ne(sentence_tree, indices, ner_tags, ne_class):
  # compute the index in ner_tags of the indicated constituent
  leaf_index = 0
  for index in indices:
    leaf_index += get_num_words(sentence_tree[:index])
    node = sentence_tree[index]

  # check if any of the words in the constituent are tagged with ne_class
  for i in xrange(leaf_index, leaf_index + len(node)):
    if ner_tags[i][1] == ne_class:
      return True

  return False
  
# returns the number of words in the tree_list
def get_num_words(tree_list):
  return sum([len(tree.leaves()) for tree in tree_list])
