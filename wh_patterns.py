# hardcoded patterns for extraction

from nltk.tree import Tree
from tags import *

'''
wh-able phrases

these template are represented as tuples (tree, index) where
  tree (a recursive pattern) is either:
    (BC) a single tag or set of tags (e.g. NOUN, set([NOUN_PROPER, PRONOUN,...]))
    (RC) a tuple of (parent, [subtrees]) where each subtree is a tree;
    this indicates that this tree is labeled parent, with children subtrees
  index: the index in the tree to replace with the wh-word (as a list of
    integers)
'''

# TODO: PRONOUN includes 'it'... should we exclude - for who/whom?

# who
WHO = ((NP, [set([NOUN_PROPER, PRONOUN])]), [])

# whom
WHOM = ((PP, [set([PREP, TO]), (NP, [set([NOUN_PROPER, PRONOUN])])]), [1])

# whose
WHOSE_NNP = ((NP, [NOUN_PROPER, POSS]), [])
WHOSE_PRONOUN = ((NP, [PRONOUN_POSS]), [])
WHOSE_NNP_NN = ((NP, [(NP, [NOUN_PROPER, POSS]), NOUN]), [0])
WHOSE_PRONOUN_NN = ((NP, [PRONOUN_POSS, NOUN]), [0])

# what
WHAT = (NP, [])

# which
# TODO: finish the rest

# TODO: include pronoun here to prevent pronouns in questions

# the dictionary wh_able maps wh-words/phrases to list of templates (see above)

wh_able = {'who': [WHO], 'whom': [WHOM], 'whose': [WHOSE_NNP, WHOSE_PRONOUN, WHOSE_NNP_NN, WHOSE_PRONOUN_NN], 'what': [WHAT]}

# searches the tree and returns a dictionary mapping the same keys as
# wh_able to lists of the matches
# REQUIRES: tree is a Tree
def get_matches(tree):
  matches = dict(zip(wh_able.keys(), [[] for i in xrange(len(wh_able))]))

  def add_matches(tree):
    # check current node against all templates
    for wh_word, templates in wh_able.iteritems():
      for template in templates:
        if pattern_match(tree, template[0]):
          matches[wh_word].append((tree, template[1]))

    # recursively search children
    for child in tree:
      if isinstance(child, Tree):
        add_matches(child)

  add_matches(tree)
  return matches

# returns True iff tree matches pattern (of form above)
def pattern_match(tree, pattern):

  # leaf node
  if not isinstance(pattern, tuple):
    return label_match(tree.label(), pattern)

  # recursive case
  if (isinstance(tree, Tree) and
      label_match(tree.label(), pattern[0]) and
      len(tree) == len(pattern[1])):
    for i in xrange(len(tree)):
      if not pattern_match(tree[i], pattern[1][i]):
        return False
    return True
  else:
    return False

# returns True iff the tree_label matches the pattern_label (maybe a set)
def label_match(tree_label, pattern_label):

  # match any of a set of tags
  if isinstance(pattern_label, set):
    for label in pattern_label:
      if label_match(tree_label, label):
        return True
    return False

  # match single tag
  else:
    return tree_label == pattern_label
