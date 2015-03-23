#!/usr/bin/python

from processq import *

q1 = Tree.fromstring('(ROOT (SBARQ (WHNP (WP Who)) (SQ (VBZ is) (NP (DT the) (NN president))) (. ?)))')
q2 = Tree.fromstring('(ROOT (SBARQ (WHNP (WDT What) (JJ major) (NN city)) (SQ (VBZ is) (VP (VBN located) (PP (IN in) (NP (JJ western) (NNP Pennsylvania))))) (. ?)))')
q3 = Tree.fromstring('(ROOT (SBARQ (WHNP (WP What)) (SQ (VBD did) (NP (NNP John)) (VP (VB eat))) (. ?)))')
q4 = Tree.fromstring('(ROOT (SBARQ (WHNP (WDT Which) (NN animal)) (SQ (VBD did) (NP (NNP John)) (VP (VB speak) (PP (TO to)))) (. ?)))')
q5 = Tree.fromstring('(ROOT (SBARQ (WHNP (WP Which)) (SQ (VBZ is) (NP (NP (NNP John) (POS \'s)) (NN brother))) (. ?)))')
q6 = Tree.fromstring('(ROOT (SBARQ (WHNP (WP$ Whose) (NN dog)) (SQ (VBZ is) (NP (DT this))) (. ?)))')
q7 = Tree.fromstring('(ROOT (SBARQ (WHNP (WP Whose)) (SQ (VBZ is) (NP (DT this))) (. ?)))')
q8 = Tree.fromstring('(ROOT (SBARQ (WHADVP (WRB Where)) (SQ (VBD did) (NP (PRP he)) (VP (VB go))) (. ?)))')
q9 = Tree.fromstring('(ROOT (SBARQ (WHADVP (WRB When)) (SQ (VBD did) (NP (PRP he)) (VP (VB go))) (. ?)))')
q10 = Tree.fromstring('(ROOT (SBARQ (WHADVP (WRB Why)) (SQ (VBD did) (NP (PRP he)) (VP (VB go))) (. ?)))')
q11 = Tree.fromstring('(ROOT (SBARQ (WHADVP (WRB How)) (SQ (VBD did) (NP (PRP he)) (VP (VB go))) (. ?)))')
q12 = Tree.fromstring('(ROOT (SBARQ (WHNP (WHADJP (WRB How) (JJ many)) (NNS pieces)) (SQ (VBD did) (NP (PRP he)) (VP (VB eat))) (. ?)))')
q13 = Tree.fromstring('(ROOT (SBARQ (WHADJP (WRB How) (JJ much)) (SQ (VBZ does) (NP (PRP he)) (VP (VB eat))) (. ?)))')
q14 = Tree.fromstring('(ROOT (SQ (VBD Did) (NP (NNP John)) (VP (VB eat) (NP (NP (DT the) (NN burrito)) (SBAR (WHNP (WDT which)) (S (NP (PRP I)) (VP (VBD was) (VP (VBG going) (S (VP (TO to) (VP (VB eat)))))))))) (. ?)))')

def basic_test():
  a1 = answer_type(q1) # who
  assert(a1[0] == PERSON)
  assert(a1[1] is None)
  a2 = answer_type(q2) # what N
  assert(a2[0] == THING)
  assert(a2[1] == wn.synsets('city', pos=wn.NOUN))
  a3 = answer_type(q3) # what
  assert(a3[0] == THING)
  assert(a3[1] is None)
  a4 = answer_type(q4) # which N
  assert(a4[0] == THING)
  assert(a4[1] == wn.synsets('animal', pos=wn.NOUN))
  a5 = answer_type(q5) # which
  assert(a5[0] == THING)
  assert(a5[1] is None)
  a6 = answer_type(q6) # whose N
  assert(a6[0] == PERSON)
  assert(a6[1] == wn.synsets('dog', pos=wn.NOUN))
  a7 = answer_type(q7) # whose
  assert(a7[0] == PERSON)
  assert(a7[1] is None)
  a8 = answer_type(q8) # where
  assert(a8[0] == PLACE)
  assert(a8[1] is None)
  a9 = answer_type(q9) # when
  assert(a9[0] == TIME)
  assert(a9[1] is None)
  a10 = answer_type(q10) # why
  assert(a10[0] == REASON)
  assert(a10[1] is None)
  a11 = answer_type(q11) # how
  assert(a11[0] == MANNER)
  assert(a11[1] is None)
  a12 = answer_type(q12) # how many N
  assert(a12[0] == AMOUNT)
  assert(a12[1] == wn.synsets('pieces', pos=wn.NOUN))
  a13 = answer_type(q13) # how much
  assert(a13[0] == AMOUNT)
  assert(a13[1] is None)
  a14 = answer_type(q14) # binary
  assert(a14[0] == BINARY)
  assert(a14[1] is None)

def real_example_test():
  pass

print 'Testing basic examples...'
basic_test()
print 'Successful.'
#print 'Testing real examples...'
#real_example_test()
#print 'Successful.'
