#!/usr/bin/python

from pattern.en import conjugate, lemma
from nltk.tree import Tree
from tags_and_patterns import *

# top-level function that takes a dictionary mapping patterns to matches and
# returns a list of questions (strings)
def make_questions(pattern_matches):
  questions = []
  for pattern in pattern_matches:
    for match in pattern_matches[pattern]:
      questions.append(transform(pattern, match))
  return questions

# transform parsed tree (constituent, not necessarily sentence) into question
def transform(pattern, tree):
  if pattern == SIMPLE_PREDICATE:
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
  if first.label() != NOUN_PROPER:
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
