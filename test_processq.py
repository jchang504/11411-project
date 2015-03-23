#!/usr/bin/python

from processq import *

q1 = Tree.fromstring('(ROOT (SBARQ (WHNP (WP Who)) (SQ (VBZ is) (NP (DT the) (NN president))) (. ?)))')
q2 = Tree.fromstring('(ROOT (SBARQ (WHNP (WDT What) (JJ major) (NN city)) (SQ (VBZ is) (VP (VBN located) (PP (IN in) (NP (JJ western) (NNP Pennsylvania))))) (. ?)))')

def test_answer_type():
  a1 = answer_type(q1)
  assert(a1[0] == THING)
  assert(a1[1] == wn.synsets('city'))

print 'Testing...'
test_answer_type()
print 'All good!'
