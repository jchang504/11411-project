#!/usr/bin/python

from transform import *

def test_get_inflection():
  assert(ALIAS_PAST == get_inflection('killed'))
  assert(ALIAS_PAST == get_inflection('purred'))
  assert(ALIAS_PAST == get_inflection('canned'))
  assert(ALIAS_PAST == get_inflection('broke'))
  assert(ALIAS_PAST == get_inflection('swam'))
  assert(ALIAS_PAST == get_inflection('could'))
  assert(ALIAS_PAST == get_inflection('had'))
  assert(ALIAS_PAST == get_inflection('halved'))
  assert(ALIAS_PAST == get_inflection('redistributed'))
  assert(ALIAS_PAST == get_inflection('thwacked'))

  assert(ALIAS_REG == get_inflection('kill'))
  assert(ALIAS_REG == get_inflection('purr'))
  assert(ALIAS_REG == get_inflection('break'))
  assert(ALIAS_REG == get_inflection('eat'))
  assert(ALIAS_REG == get_inflection('swim'))
  assert(ALIAS_REG == get_inflection('have'))
  assert(ALIAS_REG == get_inflection('halve'))

  assert(ALIAS_3SG == get_inflection('kills'))
  assert(ALIAS_3SG == get_inflection('purrs'))
  assert(ALIAS_3SG == get_inflection('breaks'))
  assert(ALIAS_3SG == get_inflection('eats'))
  assert(ALIAS_3SG == get_inflection('swims'))
  assert(ALIAS_3SG == get_inflection('has'))
  assert(ALIAS_3SG == get_inflection('halves'))
  assert(ALIAS_3SG == get_inflection('redistributes'))
  assert(ALIAS_3SG == get_inflection('thwacks'))
  assert(ALIAS_3SG == get_inflection('cans'))

def test_get_first_word():
  assert('ate' == get_first_word(TREE_1[1]))
  assert('ate' == get_first_word(TREE_2[1]))
  assert('was' == get_first_word(TREE_3[1]))
  assert('is' == get_first_word(TREE_4[1]))

def test_flatten():
  assert(['John', 'ate', 'a', 'burrito'] == flatten(TREE_1))
  assert(['John', 'ate', 'a', 'burrito', 'in', 'the', 'park'] == flatten(TREE_2))
  assert(['A', 'burrito', 'was', 'eaten', 'by', 'John'] == flatten(TREE_3))
  assert(['John', 'is', 'a', 'man'] == flatten(TREE_4))

def test_tree_to_string():
  assert('John ate a burrito' == tree_to_string(TREE_1))
  assert('John ate a burrito in the park' == tree_to_string(TREE_2))
  assert('A burrito was eaten by John' == tree_to_string(TREE_3))
  assert('John is a man' == tree_to_string(TREE_4))

def test_simple_pred_binary_q():
  print 'These should be well-formed, grammatical questions:'
  print simple_pred_binary_q(TREE_1)
  print simple_pred_binary_q(TREE_2)
  print simple_pred_binary_q(TREE_3)
  print simple_pred_binary_q(TREE_4)

print 'Testing...'
test_get_inflection()
test_get_first_word()
test_flatten()
test_tree_to_string()
test_simple_pred_binary_q()
print '\nAll good!'
