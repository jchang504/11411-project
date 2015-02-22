#!/usr/bin/python

from transform import *

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
