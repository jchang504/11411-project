#!/usr/bin/python

from nltk.tree import Tree
from tags import *

# question base patterns

SIMPLE_PREDICATE = (ROOT, ((SENTENCE, (NP, VP, PERIOD)),))
APPOSITION = (SENTENCE, ((NP, (NP, COMMA, NP, COMMA)), VP, PERIOD))
# TODO: augment with conjunctions

# returns a list of SENTENCE-rooted parse trees which fit the SIMPLE_PREDICATE
# pattern
def find_predicates(parse_trees):
  preds = []
  for parse_tree in parse_trees:
    if is_match(parse_tree, SIMPLE_PREDICATE):
      # peel off ROOT context and add to list
      preds.append(parse_tree[0])
  return preds

# search for all the APPOSITIONs in the parse_trees and return a list of them
# as NP tuples
def find_appositions(parse_trees):
  appos = []
  for parse_tree in parse_trees:
    # look for appositions; add just the NP tuples to pattern_matches
    appos += [(s[0,0], s[0,2]) for
        s in search_for_matches(parse_tree, APPOSITION)]
  return appos

# returns True iff the tree matches the pattern
def is_match(tree, pattern):
  # base case: pattern is single tag
  if not isinstance(pattern, tuple):
    return tree.label() == pattern

  # recursive case
  else:
    parent = pattern[0]
    children = pattern[1]
    if tree.label() == parent and len(tree) == len(children): # parent matches
      for i in xrange(len(tree)): # check that all children match
        ith_child = tree[i]
        if not is_match(ith_child, children[i]):
          return False
      return True

# recursively search the parse_tree and return a list of the matches to pattern
def search_for_matches(parse_tree, pattern):
  matches = []
  if is_match(parse_tree, pattern):
    matches.append(parse_tree)
  for child in parse_tree:
    if isinstance(child, Tree):
      matches += search_for_matches(child, pattern)
  return matches
