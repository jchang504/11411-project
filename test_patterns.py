#!/usr/bin/python

from wh_patterns import *

TREE_1 = Tree.fromstring('(ROOT (S (NP (NNP John)) (VP (VBD ate) (NP (DT a) (NN burrito)) (PP (IN in) (NP (DT the) (NN park)))) (. .)))')
TREE_2 = Tree.fromstring('(ROOT (S (NP (DT A) (NN burrito)) (VP (VBD was) (VP (VBN eaten) (PP (IN by) (NP (NNP John)))))))')
TREE_3 = Tree.fromstring('(ROOT (S (NP (NNP John)) (VP (VBZ is) (NP (DT a) (NN man)))))')
TREE_4 = Tree.fromstring('(ROOT (S (NP (DT The) (NN dog)) (VP (ADVP (RB quickly)) (VBD ate) (NP (DT a) (JJ big) (NN burrito)))))')
TREE_5 = Tree.fromstring('(ROOT (S (NP (NNP John)) (VP (VBZ has) (VP (VBN eaten) (NP (NNS burritos))))))')
TREE_6 = Tree.fromstring('(ROOT (S (NP (NNP John)) (VP (VBZ has) (NP (JJ great) (NN burrito) (NN sauce)))))')
TREE_7 = Tree.fromstring('(ROOT (S (NP (NNP John)) (VP (MD might) (VP (VB have) (VP (VBN eaten) (NP (DT the) (JJ wrong) (NN burrito)))))))')
TREE_8 = Tree.fromstring('(ROOT (S (NP (PRP He)) (VP (VBD bought) (NP (DT the) (JJ green) (NN tree)) (PP (IN for) (NP (CD 6) (NNS dollars)))) (. .)))')

trees = [TREE_1, TREE_2, TREE_3, TREE_4, TREE_5, TREE_6, TREE_7, TREE_8]

def test_basic():
  return [get_matches(t) for t in trees]
