#!/usr/bin/python

from nltk.tree import Tree
from tags import *
from pattern.en import conjugate, lemma

# identifies the question as either WH or BINARY
# question_tree is a Tree
def q_type(question_tree):
  pass # TODO: implement

# inverts the subj and aux (do-insertion if necessary) to transform the
# declarative sentence into a binary interrogative form
# REQUIRES: sentence_tree is a Tree(S(NP,VP,.))
# RETURNS: a string. The original subj is uncapitalized (if non-proper) but the
# aux is NOT capitalized.
def sent_to_bin_q(sentence_tree):
  np = sentence_tree[0]
  vp = sentence_tree[1]
  head_verb = vp[0]
  assert(is_verb(head_verb.label()))
  verb = head_verb[0]

  # has auxiliary
  if is_modal(head_verb, vp) or lemma(verb) == 'be':
    uncap(np) # uncapitalize original subj (unless proper noun)
    return verb + ' ' + tree_to_string(np) + ' ' + tree_to_string(vp[1])

  # no auxiliary, use do-insertion
  else:
    head_verb[0] = lemma(verb) # convert head verb to infinitive
    uncap(np) # uncapitalize original subj (unless proper noun)
    return (conjugate('do', get_inflection(head_verb)) + ' ' +
        tree_to_string(np) + ' ' + tree_to_string(vp))

# inverts the aux (do-deletion if necessary) and subj to transform the binary
# interrogative into a declarative sentence
# REQUIRES: question_tree is a Tree
# RETURNS: a string. The original aux is uncapitalized and the subj is
# capitalized
def bin_q_to_sent(question_tree):
  pass # TODO: implement

# returns True iff the verb is a modal or auxiliary 'have', 'do'
def is_modal(head_verb, vp):
  return head_verb.label() == MODAL or (lemma(head_verb[0]) in ['have', 'do']
      and vp[1].label() == VP)

# Alias strings
ALIASES = {VERB_PAST: 'p', VERB_PLURAL: 'inf', VERB_3SG: '3sg'}
# returns the alias corresponding to the verb's distinguishable inflection
def get_inflection(verb):
  return ALIASES.get(verb.label())

# uncapitalizes the phrase, unless its first word is a proper noun
def uncap(phrase):
  first = first_word(phrase)
  if first.label() != NOUN_PROPER:
    first[0] = first[0].lower()

# gets the leftmost leaf node of tree
def first_word(tree):
  while isinstance(tree[0], Tree):
    tree = tree[0]
  return tree

# converts the tree to string form
def tree_to_string(tree):
  return ' '.join(tree.leaves())
