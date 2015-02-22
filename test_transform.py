#!/usr/bin/python

from transform import *

def test_tree_to_string():
  assert('John ate a burrito' == tree_to_string(TREE_1))
  assert('John ate a burrito in the park' == tree_to_string(TREE_2))
  assert('A burrito was eaten by John' == tree_to_string(TREE_3))
  assert('John is a man' == tree_to_string(TREE_4))

def test_simple_pred_binary_q():
  print simple_pred_binary_q(TREE_1)
  print simple_pred_binary_q(TREE_2)
  print simple_pred_binary_q(TREE_3)
  print simple_pred_binary_q(TREE_4)
  print simple_pred_binary_q(TREE_5)

def test_apposition_binary_q():
  print apposition_binary_q(TREE_6)
  print apposition_binary_q(TREE_7)

print 'Testing...'
print 'These should be well-formed, grammatical questions:'
test_tree_to_string()
test_simple_pred_binary_q()
test_apposition_binary_q()
print '\nAll good!'
