import sys
import preprocess
import transform

article_filename = sys.argv[1]
num_questions = sys.argv[2]

sentence_trees = preprocess.parseHTML(article_filename)
# ??? - Eileen's part
# extracted_phrases = eileenspart(sentence_trees)
# TODO: fix this
SIMPLE_PREDICATE = 0
extracted_phrases = [(SIMPLE_PREDICATE, sentence_trees[0][0])] # for testing
questions = transform.make_questions(extracted_phrases)
for q in questions:
  print q
