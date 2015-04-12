from nltk.tree import Tree

T1 = Tree.fromstring('(ROOT (S (NP (NNP John)) (VP (VBD ate) (NP (DT a) (NN burrito)) (PP (IN in) (NP (DT the) (NN park)))) (. .)))')
T2 = Tree.fromstring('(ROOT (S (NP (NP (NNP John)) (, ,) (NP (DT a) (NN doctor)) (, ,)) (VP (VBD treated) (NP (PRP him))) (. .)))')
