#!/usr/bin/python

from transform import *

TREE_1 = Tree.fromstring('(S (NNP John) (VP (VP (VBD ate) (NP (DT a) (NN burrito))) (PP (IN in) (NP (DT the) (NN park)))))')
TREE_2 = Tree.fromstring('(S (NP (DT A) (NN burrito)) (VP (VBD was) (VP (VBN eaten) (PP (IN by) (NP (NNP John))))))')
TREE_3 = Tree.fromstring('(S (NP (NNP John)) (VP (VBZ is) (NP (DT a) (NN man))))')
TREE_4 = Tree.fromstring('(S (NP (DT The) (NN dog)) (VP (ADVP (RB quickly)) (VBD ate) (NP (DT a) (JJ big) (NN burrito))))')
TREE_5 = Tree.fromstring('(S (NP (NNP John)) (VP (VBZ has) (VP (VBN eaten) (NP (NNS burritos)))))')
TREE_6 = Tree.fromstring('(S (NP (NNP John)) (VP (VBZ has) (NP (JJ great) (NN burrito) (NN sauce))))')
TREE_7 = Tree.fromstring('(S (NP (NNP John)) (VP (MD might) (VP (VB have) (VP (VBN eaten) (NP (DT the) (JJ wrong) (NN burrito))))))')
# Appositions
TREE_8 = Tree.fromstring('(NP (NP (NNP John)) (, ,) (NP (DT a) (NN man)) (, ,))')
TREE_9 = Tree.fromstring('(NP (NP (PRP$ Their) (NNS brothers)) (, ,) (NP (DT a) (JJ handsome) (NN lot)) (, ,))')

def test_simple_pred_binary_q():
  print simple_pred_binary_q(TREE_1)
  print simple_pred_binary_q(TREE_2)
  print simple_pred_binary_q(TREE_3)
  print simple_pred_binary_q(TREE_4)
  print simple_pred_binary_q(TREE_5)
  print simple_pred_binary_q(TREE_6)
  print simple_pred_binary_q(TREE_7)

def test_apposition_binary_q():
  print apposition_binary_q(TREE_8)
  print apposition_binary_q(TREE_9)

print 'Testing...'
print 'These should be well-formed, grammatical questions:\n'
print 'SIMPLE_PREDICATE'
test_simple_pred_binary_q()
print '\nAPPOSITION'
test_apposition_binary_q()
print '\nAll good!'
