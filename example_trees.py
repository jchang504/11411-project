from nltk.tree import Tree

# John ate a burrito in the park.
T1 = Tree.fromstring('(ROOT (S (NP (NNP John)) (VP (VBD ate) (NP (DT a) (NN burrito)) (PP (IN in) (NP (DT the) (NN park)))) (. .)))')
# John, a doctor, treated him.
T2 = Tree.fromstring('(ROOT (S (NP (NP (NNP John)) (, ,) (NP (DT a) (NN doctor)) (, ,)) (VP (VBD treated) (NP (PRP him))) (. .)))')
# Did John eat a burrito in the park?
S1 = Tree.fromstring('(ROOT (SQ (VBD Did) (NP (NNP John)) (VP (VB eat) (NP (NP (DT a) (NN burrito)) (PP (IN in) (NP (DT the) (NN park))))) (. ?)))')
# Is John a doctor?
S2 = Tree.fromstring('(ROOT (SQ (VBZ Is) (NP (NNP John)) (NP (DT a) (NN doctor)) (. ?)))')
