# hardcoded patterns for extracting wh-question transformable sentences

# each of these is similar, but slightly individualized... massive code
# duplication, but it made it faster to write... :\

from nltk.tree import Tree
from tags import *
import copy

# each of these wh-word-named functions takes a Tree (directly descended from
# ROOT and matching SIMPLE_PREDICATE) and a Boolean answer_mode indicating
# whether we're looking for answers or not and returns a list of tuples (gappy,
# gap_phrase) where gappy is the sentence_tree with the gap and gap_phrase is
# if answer_mode=False: the wh-phrase to replace the gap constituent with or
# if answer_mode=True: the removed gap constituent

def how_many(sentence_tree, answer_mode):
  np = sentence_tree[0]
  vp = sentence_tree[1]
  gappies = []

  # number NP in subject position
  head_noun = is_number_np(np)
  if head_noun:
    gappy = copy.deepcopy(sentence_tree)
    gap_phrase = 'how many ' + head_noun # default ask mode
    if answer_mode:
      gap_phrase = copy.deepcopy(gappy[0])
    del gappy[0]
    gappies.append((gappy, gap_phrase))

  # check for number NP in object position
  verb_head = vp[0]
  if is_tensed_verb(verb_head.label()):
    if len(vp) >= 2:
      obj = vp[1]
      if obj.label() == NP:
        head_noun = is_number_np(obj)
        if head_noun:
          gappy = copy.deepcopy(sentence_tree)
          gap_phrase = 'how many ' + head_noun # default ask mode
          if answer_mode:
            gap_phrase = copy.deepcopy(gappy[1,1])
          del gappy[1,1]
          gappies.append((gappy, gap_phrase))

  return gappies

# returns the head noun if this NP is a number NP (e.g. '10 white chickens')
def is_number_np(np):
  if np[0].label() == NUMBER:
    for i in xrange(1, len(np)-1):
      if not is_adjective(np[i].label()):
        return None
    if np[-1].label() == NOUN_PL:
      return np[-1][0]

def how(sentence_tree, answer_mode):
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
      if is_meaningful_adverb(node):
        gappy = copy.deepcopy(sentence_tree)
        gap_phrase = 'how' # default ask mode
        if answer_mode:
          gap_phrase = copy.deepcopy(gappy[1,vp_index])
        del gappy[1,vp_index]
        gappies.append((gappy, gap_phrase))

  return gappies

# returns True iff this node is an ADVP that is not in the stop list
ADVERB_STOP_LIST = ['almost', 'also', 'further', 'generally', 'greatly',
    'however', 'just', 'later', 'longer', 'often', 'only', 'typically']
def is_meaningful_adverb(tree_node):
  return (tree_node.label() == ADVP and tree_node[0].label() == ADVERB and
      tree_node[0][0].lower() not in ADVERB_STOP_LIST)

def why(sentence_tree, answer_mode):
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
      if is_because(node):
        gappy = copy.deepcopy(sentence_tree)
        gap_phrase = 'why' # default ask mode
        if answer_mode:
          gap_phrase = copy.deepcopy(gappy[1,vp_index])
        del gappy[1,vp_index]
        gappies.append((gappy, gap_phrase))

  return gappies

# returns True iff this node is a because clause
def is_because(tree_node):
  if tree_node.label() == SBAR:
    because = tree_node[0]
    return because.label() == PREP and because[0].lower() == 'because'

def which(sentence_tree, answer_mode):
  np = sentence_tree[0]
  vp = sentence_tree[1]
  gappies = []

  # definite NP in subject position
  head_noun_word = is_definite_np(np)
  if head_noun_word is not None:
    gappy = copy.deepcopy(sentence_tree)
    gap_phrase = 'which ' + head_noun_word # default ask mode
    if answer_mode:
      gap_phrase = copy.deepcopy(gappy[0])
    del gappy[0]
    gappies.append((gappy, gap_phrase))

  verb_head = vp[0]
  if is_tensed_verb(verb_head.label()):
    if len(vp) >= 2:
      vp_index = 1
      node = vp[vp_index]
      if node.label() == NP:
        # check for definite NP in direct object position
        head_noun_word = is_definite_np(node)
        if head_noun_word is not None:
          gappy = copy.deepcopy(sentence_tree)
          gap_phrase = 'which ' + head_noun_word # default ask mode
          if answer_mode:
            gap_phrase = copy.deepcopy(gappy[1,1])
          del gappy[1,1]
          gappies.append((gappy, gap_phrase))

      # skip past direct object/ADJP if present
      if node.label() != PP and len(vp) > 2:
        vp_index = 2
        node = vp[vp_index]

      if node.label() == PP:
        prep = node[0]
        indir_obj = node[1]
        if prep.label() in [TO, PREP] and indir_obj.label() == NP:
          # check for definite NP in indirect object position
          head_noun_word = is_definite_np(indir_obj)
          if head_noun_word is not None:
            gappy = copy.deepcopy(sentence_tree)
            gap_phrase = prep[0] + ' which ' + head_noun_word# default ask mode
            if answer_mode:
              gap_phrase = copy.deepcopy(gappy[1,vp_index])
            del gappy[1,vp_index]
            gappies.append((gappy, gap_phrase))

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
        if not is_adjective(np[i].label()):
          return None
      # last child is head noun
      if is_noun_head(np[-1].label()):
        return np[-1][0]

def whose(sentence_tree, answer_mode):
  np = sentence_tree[0]
  vp = sentence_tree[1]
  gappies = []

  # possessive NP in subject position
  head_noun_word = is_possessive_np(np)
  if head_noun_word is not None:
    gappy = copy.deepcopy(sentence_tree)
    gap_phrase = 'whose ' + head_noun_word # default ask mode
    if answer_mode:
      gap_phrase = copy.deepcopy(gappy[0])
    del gappy[0]
    gappies.append((gappy, gap_phrase))

  verb_head = vp[0]
  if is_tensed_verb(verb_head.label()):
    if len(vp) >= 2:
      vp_index = 1
      node = vp[vp_index]
      if node.label() == NP:
        # check for possessive pronoun NP in direct object position
        head_noun_word = is_possessive_np(node)
        if head_noun_word is not None:
          gappy = copy.deepcopy(sentence_tree)
          gap_phrase = 'whose ' + head_noun_word # default ask mode
          if answer_mode:
            gap_phrase = copy.deepcopy(gappy[1,1])
          del gappy[1,1]
          gappies.append((gappy, gap_phrase))

      # skip past direct object/ADJP if present
      if node.label() != PP and len(vp) > 2:
        vp_index = 2
        node = vp[vp_index]
      if node.label() == PP:
        prep = node[0]
        indir_obj = node[1]
        if prep.label() in [TO, PREP] and indir_obj.label() == NP:
          # check for possessive pronoun NP in indirect object position
          head_noun_word = is_possessive_np(indir_obj)
          if head_noun_word is not None:
            gappy = copy.deepcopy(sentence_tree)
            gap_phrase = prep[0] + ' whose ' + head_noun_word# default ask mode
            if answer_mode:
              gap_phrase = copy.deepcopy(gappy[1,vp_index])
            del gappy[1,vp_index]
            gappies.append((gappy, gap_phrase))

  return gappies

# if np is a possessive np (e.g. 'his children'), returns the noun word which
# heads it (a string); else returns None
def is_possessive_np(np):
  # first child is possessive pronoun
  if np[0].label() == PRONOUN_POSS:
    poss = np[0][0].lower()
    if poss in ['his', 'her', 'their']:
      # any intervening children are adjectives
      for i in xrange(1, len(np)-1):
        if not is_adjective(np[i].label()):
          return None
      # last child is head noun
      if is_noun_head(np[-1].label()):
        return np[-1][0]

# the following wh-question types require NER tagging to determine. The extra
# argument ner_tagged is the NER-tagged sentence (a list of tuples (word, tag))

def who_whom(sentence_tree, ner_tags, answer_mode):
  np = sentence_tree[0]
  vp = sentence_tree[1]
  gappies = []

  # person NP in subject position
  if is_ne(sentence_tree, [0], ner_tags, [PERSON]):
    gappy = copy.deepcopy(sentence_tree)
    gap_phrase = 'who' # default ask mode
    if answer_mode:
      gap_phrase = copy.deepcopy(gappy[0])
    del gappy[0]
    gappies.append((gappy, gap_phrase))

  verb_head = vp[0]
  if is_tensed_verb(verb_head.label()):
    if len(vp) >= 2:
      vp_index = 1
      node = vp[vp_index]
      # check for person NP in direct object position
      if (node.label() == NP and
          is_ne(sentence_tree, [1,1], ner_tags, [PERSON])):
        gappy = copy.deepcopy(sentence_tree)
        gap_phrase = 'who' # default ask mode
        if answer_mode:
          gap_phrase = copy.deepcopy(gappy[1,1])
        del gappy[1,1]
        gappies.append((gappy, gap_phrase))

      # skip past direct object/ADJP if present
      if node.label() != PP and len(vp) > 2:
        vp_index = 2
        node = vp[vp_index]
      # check for person NP in indirect object position
      if node.label() == PP:
        prep = node[0]
        indir_obj = node[1]
        if (prep.label() in [TO, PREP] and indir_obj.label() == NP and
            is_ne(sentence_tree, [1,vp_index,1], ner_tags, [PERSON])):
          gappy = copy.deepcopy(sentence_tree)
          gap_phrase = prep[0] + ' whom' # default ask mode
          if answer_mode:
            gap_phrase = copy.deepcopy(gappy[1,vp_index])
          del gappy[1,vp_index]
          gappies.append((gappy, gap_phrase))

  return gappies

def where(sentence_tree, ner_tags, answer_mode):
  vp = sentence_tree[1]
  gappies = []

  verb_head = vp[0]
  if is_tensed_verb(verb_head.label()):
    if len(vp) >= 2:
      vp_index = 1
      node = vp[vp_index]
      # skip past NP/ADJP if present
      if node.label() != PP and len(vp) > 2:
        vp_index = 2
        node = vp[vp_index]

      # check for locative preposition
      if node.label() == PP:
        prep = node[0]
        indir_obj = node[1]
        if (prep.label() in [TO, PREP] and indir_obj.label() == NP and
            is_ne(sentence_tree, [1,vp_index,1], ner_tags, [LOCATION])):
          gappy = copy.deepcopy(sentence_tree)
          gap_phrase = 'where' # default ask mode
          if answer_mode:
            gap_phrase = copy.deepcopy(gappy[1,vp_index,1])
          del gappy[1,vp_index,1]
          gappies.append((gappy, gap_phrase))

  return gappies

def when(sentence_tree, ner_tags, answer_mode):
  vp = sentence_tree[1]
  gappies = []

  verb_head = vp[0]
  if is_tensed_verb(verb_head.label()):
    if len(vp) >= 2:
      vp_index = 1
      node = vp[vp_index]
      # skip past NP/ADJP if present
      if node.label() != PP and len(vp) > 2:
        vp_index = 2
        node = vp[vp_index]

      # check for locative preposition
      if node.label() == PP:
        prep = node[0]
        indir_obj = node[1]
        if (prep.label() in [TO, PREP] and indir_obj.label() == NP and
            is_ne(sentence_tree, [1,vp_index,1], ner_tags, [DATE, TIME])):
          gappy = copy.deepcopy(sentence_tree)
          gap_phrase = 'when' # default ask mode
          if answer_mode:
            gap_phrase = copy.deepcopy(gappy[1,vp_index])
          del gappy[1,vp_index]
          gappies.append((gappy, gap_phrase))

  return gappies

def what(sentence_tree, ner_tags, answer_mode):
  np = sentence_tree[0]
  vp = sentence_tree[1]
  gappies = []

  # non-person NP in subject position
  if not is_ne(sentence_tree, [0], ner_tags, [PERSON]):
    gappy = copy.deepcopy(sentence_tree)
    gap_phrase = 'what' # default ask mode
    if answer_mode:
      gap_phrase = copy.deepcopy(gappy[0])
    del gappy[0]
    gappies.append((gappy, gap_phrase))

  verb_head = vp[0]
  # check for non-person NP in direct object position
  if is_tensed_verb(verb_head.label()):
    if len(vp) >= 2:
      obj = vp[1]
      if obj.label() == NP and not is_ne(sentence_tree, [1,1], ner_tags,
          [PERSON]):
        gappy = copy.deepcopy(sentence_tree)
        gap_phrase = 'what' # default ask mode
        if answer_mode:
          gap_phrase = copy.deepcopy(gappy[1,1])
        del gappy[1,1]
        gappies.append((gappy, gap_phrase))

  return gappies

# returns True iff all the words in the constituent at indices in the
# sentence_tree are tagged with any of ne_classes in the ner_tags
def is_ne(sentence_tree, indices, ner_tags, ne_classes):
  # compute the index in ner_tags of the indicated constituent
  node = sentence_tree
  leaf_index = 0
  for index in indices:
    leaf_index += get_num_words(node[:index])
    node = node[index]

  # check if all of the words in the constituent are tagged with ne_classes
  for i in xrange(leaf_index, leaf_index + get_num_words([node])):
    if ner_tags[i][1] not in ne_classes:
      return False
  return True
  
# returns the number of words in the tree_list
def get_num_words(tree_list):
  return sum([len(tree.leaves()) for tree in tree_list])

# top-level function - gets the wh-structures (asking mode) for all wh-words
JUST_SYNTAX = [how_many, how, why, which, whose]
NEEDS_NER = [who_whom, where, when, what]
def get_all_wh(sentence_tree, ner_tags):
  results = dict([(func.__name__, []) for func in JUST_SYNTAX + NEEDS_NER])
  for func in JUST_SYNTAX:
    results[func.__name__] = func(sentence_tree, False)
  for func in NEEDS_NER:
    results[func.__name__] = func(sentence_tree, ner_tags, False)

  return results

# condition functions for use in find_all_matches

def is_how_many(sentence_tree, indices, ner_tags):
  return (sentence_tree[indices].label() == NP and
      is_number_np(sentence_tree[indices]))

def is_how(sentence_tree, indices, ner_tags):
  return is_meaningful_adverb(sentence_tree[indices])

def is_why(sentence_tree, indices, ner_tags):
  return is_because(sentence_tree[indices])

def is_which(sentence_tree, indices, ner_tags):
  return (sentence_tree[indices].label() == NP and
      is_definite_np(sentence_tree[indices]))

def is_whose(sentence_tree, indices, ner_tags):
  return (sentence_tree[indices].label() == NP and
      is_possessive_np(sentence_tree[indices]))

def is_who_whom(sentence_tree, indices, ner_tags):
  return (sentence_tree[indices].label() == NP and
      is_ne(sentence_tree, indices, ner_tags, [PERSON]))

def is_where(sentence_tree, indices, ner_tags):
  return (sentence_tree[indices].label() == PP and
      is_ne(sentence_tree, indices + [1], ner_tags, [LOCATION]))

def is_when(sentence_tree, indices, ner_tags):
  return (sentence_tree[indices].label() == PP and
      is_ne(sentence_tree, indices + [1], ner_tags, [DATE, TIME]))

def is_what(sentence_tree, indices, ner_tags):
  return (sentence_tree[indices].label() == NP and
      not is_ne(sentence_tree, indices, ner_tags, [PERSON]))

# finds ALL (gappy, answer) st answer meets condition_func in
# sentence_tree[indices], regardless of syntactic position
# TODO: avoid pronouns?
def find_all_matches(sentence_tree, indices, ner_tags, condition_func):
  matches = []

  # check current node
  if condition_func(sentence_tree, indices, ner_tags) and indices != []:
    gappy = copy.deepcopy(sentence_tree)
    answer = gappy[indices]
    del gappy[indices]
    matches.append((gappy, answer))

  # search children
  for i in xrange(len(sentence_tree[indices])):
    if isinstance(sentence_tree[indices + [i]], Tree):
      matches += find_all_matches(sentence_tree, indices + [i], ner_tags,
          condition_func)

  return matches
