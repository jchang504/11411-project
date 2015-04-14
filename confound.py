import random
from nltk.corpus import wordnet
from pattern.en import singularize, pluralize
from tags import *
import sent_transform

WN_VERB = wordnet.VERB
WN_NOUN = wordnet.NOUN
WN_ADJ = wordnet.ADJ
WN_ADV = wordnet.ADV

# returns a set of synonyms of word as a part-of-speech, according to
# WordNet (lemmas of the same synset)
def synonyms(word, part_of_speech):
  syns = set()
  for synset in wordnet.synsets(word, pos=part_of_speech):
    for lemma in synset.lemmas():
      syns.add(lemma.name().replace('_', ' '))
  return syns

# returns a set of sisters - words with the same hypernym as word as a
# part-of-speech - according to WordNet. Use the first (most common) synset
def sisters(word, part_of_speech):
  sis = set()
  synsets = wordnet.synsets(word, pos=part_of_speech)
  if len(synsets) > 0:
    for hypernym in synsets[0].hypernyms():
      for sister in hypernym.hyponyms():
        for lemma in sister.lemmas():
          sis.add(lemma.name().replace('_', ' '))
  return sis

# returns a set of antonyms of word as a part-of-speech, according to
# WordNet (lemmas of the same synset)
def antonyms(word, part_of_speech):
  ants = set()
  for synset in wordnet.synsets(word, pos=part_of_speech):
    for lemma in synset.lemmas():
      for ant in lemma.antonyms():
        ants.add(ant.name().replace('_', ' '))
  return ants

# try to confound the sentence by substituting in synonyms, sisters, or
# antonyms of the head noun in that order
# REQUIRES: pred_tree matches SIMPLE_PREDICATE, and is a copy (will be mutated)
# RETURNS: (confounded, success) where confounded is the confounded setence iff
# success is True
def try_confound(pred_tree):
  np = pred_tree[0]
  assert(np.label() == NP)
  head_noun = sent_transform.get_noun(np)

  # try synonyms
  noun_syn = synonyms(head_noun[0].lower(), WN_NOUN)
  # if there are synonyms, choose a random one
  if len(noun_syn) > 0:
    chosen_syn = singularize(random.choice(tuple(noun_syn)))
    # fix number inflection
    if head_noun.label() == NOUN_PL:
      head_noun[0] = pluralize(chosen_syn)
    else:
      head_noun[0] = chosen_syn
    return (pred_tree, True)

  # try sisters
  noun_sis = sisters(head_noun[0].lower(), WN_NOUN)
  # if there are sisters, choose a random one
  if len(noun_sis) > 0:
    chosen_sis = singularize(random.choice(tuple(noun_sis)))
    # fix number inflection
    if head_noun.label() == NOUN_PL:
      head_noun[0] = pluralize(chosen_sis)
    else:
      head_noun[0] = chosen_sis
    return (pred_tree, True)

  # try antonyms
  noun_ant = antonyms(head_noun[0].lower(), WN_NOUN)
  # if there are antonyms, choose a random one
  if len(noun_ant) > 0:
    chosen_ant = singularize(random.choice(tuple(noun_ant)))
    # fix number inflection
    if head_noun.label() == NOUN_PL:
      head_noun[0] = pluralize(chosen_ant)
    else:
      head_noun[0] = chosen_ant
    return (pred_tree, True)
  
  return (pred_tree, False)
