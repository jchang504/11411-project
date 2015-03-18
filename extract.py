#!/usr/bin/python

from nltk.tree import Tree
from tags_and_patterns import *

# returns a dictionary keyed by PATTERNS, with values lists of the matches to
# those patterns found in the parse_trees
def find_matches(parse_trees):
  pattern_matches = dict(zip(PATTERNS, [[] for i in xrange(len(PATTERNS))]))
  for parse_tree in parse_trees:
    extract_pattern_matches(parse_tree, PATTERNS, pattern_matches)
  return pattern_matches

# recursively searches the parse_tree and adds nodes that match any of the
# patterns to the corresponding list in pattern_matches
def extract_pattern_matches(parse_tree, patterns, pattern_matches):

  # check for pattern match at current node
  for pattern in patterns:
    parent_match = pattern[0]
    children_match = pattern[1]
    if (parse_tree.label() == parent_match and # parent matches
        len(parse_tree) == len(children_match)):
      is_match = True
      for i in xrange(len(parse_tree)): # check that all children match
        ith_child = parse_tree[i]
        # avoid child NPs that are pronouns for ALL patterns
        np_is_pronoun = (ith_child.label() == NP and
          isinstance(ith_child[0], Tree) and ith_child[0].label() == PRONOUN)
        if ith_child.label() != children_match[i] or np_is_pronoun:
          is_match = False
          break
      if is_match: # parent and children labels match; add to matches list
        pattern_matches[pattern].append(parse_tree)
        break # same node can't match multiple patterns

  # recursively search subtrees
  for child in parse_tree:
    if isinstance(child, Tree):
      extract_pattern_matches(child, patterns, pattern_matches)
