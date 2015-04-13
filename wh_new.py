# hardcoded patterns for extracting wh-question transformable sentences

# each of these is similar, but slightly individualized... massive code
# duplication, but it made it faster to write... :\

from nltk.tree import Tree
from tags import *
import copy

# each of these wh-word-named functions takes a Tree (directly descended from
# ROOT and matching SIMPLE_PREDICATE) and returns a list of tuples (gappy,
# wh-phrase) where gappy is the sentence_tree with the wh-replacee removed and
# wh-phrase is the wh-phrase to put at the front of the question

def how_many(sentence_tree):
  np = sentence_tree[0]
  vp = sentence_tree[1]
  gappies = []

  # number NP in subject position
  if is_number_np(np):
    gappy = copy.deepcopy(sentence_tree)
    del gappy[0]
    gappies.append((gappy, 'how many'))

  # check for number NP in object position
  verb_head = vp[0]
  if is_tensed_verb(verb_head.label()):
    if len(vp) >= 2:
      obj = vp[1]
      if obj.label() == NP and is_number_np(obj):
        gappy = copy.deepcopy(sentence_tree)
        del gappy[1,1]
        gappies.append((gappy, 'how many'))

  return gappies

# returns True if this NP is a number NP (e.g. '10 white chickens')
def is_number_np(np):
  if np[0].label() == NUMBER:
    for i in xrange(1, len(np)-1):
      if np[i].label() != ADJ:
        return False
    return np[-1].label() == NOUN_PL

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
        gappies.append((gappy, 'how'))

  return gappies

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
          gappies.append((gappy, 'why'))

  return gappies

def which(sentence_tree):
  np = sentence_tree[0]
  vp = sentence_tree[1]
  gappies = []

  # definite NP in subject position
  head_noun_word = is_definite_np(np)
  if head_noun_word is not None:
    gappy = copy.deepcopy(sentence_tree)
    del gappy[0]
    gappies.append((gappy, 'which ' + head_noun_word))

  # check for definite NP in object position
  verb_head = vp[0]
  if is_tensed_verb(verb_head.label()):
    if len(vp) >= 2:
      obj = vp[1]
      if obj.label() == NP:
        head_noun_word = is_definite_np(obj)
        if head_noun_word is not None:
          gappy = copy.deepcopy(sentence_tree)
          del gappy[1,1]
          gappies.append((gappy, 'which ' + head_noun_word))

  return gappies

# if np is a definite np, returns the noun word which heads it (a string); else
# returns None
def is_definite_np(np):
  # first child is definite determiner
  if np[0].label() == DET:
    det_word = np[0][0].lower()
    if det_word in ['the', 'this', 'that', 'these', 'those']:
      # 'the' needs at least 1 adjective
      if det_word == 'the' and len(np) < 3:
        return None
      # any intervening children are adjectives
      for i in xrange(1, len(np)-1):
        if np[i].label() != ADJ:
          return None
      # last child is head noun
      if np[-1].label().startswith('NN'):
        return np[-1][0]

# the following wh-question types require NER tagging to determine. The extra
# argument ner_tagged is the NER-tagged sentence (a list of tuples (word, tag))

def who_whom(sentence_tree, ner_tags):
  np = sentence_tree[0]
  vp = sentence_tree[1]
  gappies = []

  # person NP in subject position
  if is_ne(sentence_tree, [0], ner_tags, PERSON):
    gappy = copy.deepcopy(sentence_tree)
    del gappy[0]
    gappies.append((gappy, 'who'))

  verb_head = vp[0]
  if is_tensed_verb(verb_head.label()):
    if len(vp) >= 2:
      vp_index = 1
      node = vp[vp_index]
      # check for person NP in direct object position
      if node.label() == NP and is_ne(sentence_tree, [1,1], ner_tags, PERSON):
        gappy = copy.deepcopy(sentence_tree)
        del gappy[1,1]
        gappies.append((gappy, 'who'))

      # skip past direct object if present
      if node.label() == NP and len(vp) > 2:
        vp_index = 2
        node = vp[vp_index]
      # check for person NP in indirect object position
      if node.label() == PP:
        prep = node[0]
        indir_obj = node[1]
        if (prep.label() in [TO, PREP] and indir_obj.label() == NP and
            is_ne(sentence_tree, [1,vp_index,1], ner_tags, PERSON)):
          gappy = copy.deepcopy(sentence_tree)
          del gappy[1,vp_index]
          gappies.append((gappy, prep[0] + ' whom'))

  return gappies

def what(sentence_tree, ner_tags):
  np = sentence_tree[0]
  vp = sentence_tree[1]
  gappies = []

  # non-person NP in subject position
  if not is_ne(sentence_tree, [0], ner_tags, PERSON):
    gappy = copy.deepcopy(sentence_tree)
    del gappy[0]
    gappies.append((gappy, 'what'))

  # check for non-person NP in object position
  verb_head = vp[0]
  if is_tensed_verb(verb_head.label()):
    if len(vp) >= 2:
      obj = vp[1]
      if obj.label() == NP and not is_ne(sentence_tree, [1,1], ner_tags,
          PERSON):
        gappy = copy.deepcopy(sentence_tree)
        del gappy[1,1]
        gappies.append((gappy, 'what'))

  return gappies

# returns True iff the constituent at indices in the sentence_tree is tagged
# with ne_class in the ner_tags
def is_ne(sentence_tree, indices, ner_tags, ne_class):
  # compute the index in ner_tags of the indicated constituent
  node = sentence_tree
  leaf_index = 0
  for index in indices:
    leaf_index += get_num_words(node[:index])
    node = node[index]

  # check if any of the words in the constituent are tagged with ne_class
  for i in xrange(leaf_index, leaf_index + len(node)):
    print i
    print ner_tags[i]
    if ner_tags[i][1] == ne_class:
      return True

  return False
  
# returns the number of words in the tree_list
def get_num_words(tree_list):
  return sum([len(tree.leaves()) for tree in tree_list])
