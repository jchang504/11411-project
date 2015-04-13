from nltk.tree import Tree

# John ate a burrito in the park.
S1 = Tree.fromstring('(ROOT (S (NP (NNP John)) (VP (VBD ate) (NP (DT a) (NN burrito)) (PP (IN in) (NP (DT the) (NN park)))) (. .)))')
# John, a doctor, treated him.
S2 = Tree.fromstring('(ROOT (S (NP (NP (NNP John)) (, ,) (NP (DT a) (NN doctor)) (, ,)) (VP (VBD treated) (NP (PRP him))) (. .)))')
# I saw 10,000 people in the yard.
S3 = Tree.fromstring('(ROOT (S (NP (PRP I)) (VP (VBD saw) (NP (CD 10,000) (NNS people)) (PP (IN in) (NP (DT the) (NN yard)))) (. .)))')
# 10 people ate outside.
S4 = Tree.fromstring('(ROOT (S (NP (CD 10) (NNS people)) (VP (VBD ate) (ADVP (RB outside))) (. .)))')
# John ate in the park slowly.
S5 = Tree.fromstring('(ROOT (S (NP (NNP John)) (VP (VBD ate) (PP (IN in) (NP (DT the) (NN park))) (ADVP (RB slowly))) (. .)))')
# John ate because you did.
S6 = Tree.fromstring('(ROOT (S (NP (NNP John)) (VP (VBD ate) (SBAR (IN because) (S (NP (PRP you)) (VP (VBD did))))) (. .)))')


# Did John eat a burrito in the park?
Q1 = Tree.fromstring('(ROOT (SQ (VBD Did) (NP (NNP John)) (VP (VB eat) (NP (NP (DT a) (NN burrito)) (PP (IN in) (NP (DT the) (NN park))))) (. ?)))')
# Is John a doctor?
Q2 = Tree.fromstring('(ROOT (SQ (VBZ Is) (NP (NNP John)) (NP (DT a) (NN doctor)) (. ?)))')
