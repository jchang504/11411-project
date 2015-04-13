#!/usr/bin/python

# This is the top-level ./ask program. It takes 3 CL arguments:
# - filename of the Wiki article to ask questions about
# - number of questions to ask
# - user - this is needed to set the correct location parameters to run
#   the Stanford parser

import sys
import parse_article
import stanford_parser
import extract
import sent_transform

article_filename = sys.argv[1]
num_questions = int(sys.argv[2])
user = sys.argv[3]

# parse HTML into sentences, parse sentences into trees
sentences = parse_article.parse_html(article_filename)
stanford = stanford_parser.create_parser(user)
parse_trees = stanford.raw_parse_sents(sentences)

# augment trees with appositions transformed into predicates
appos = extract.find_appositions(parse_trees)
appo_sentences = [sent_transform.apposition_to_sent(appo) for appo in appos]
transformed = stanford.raw_parse_sents(appo_sentences)
parse_trees += transformed

# now find all predicates in augmented tree list
preds = extract.find_predicates(parse_trees)
for i in xrange(len(preds)):
  try:
    q = sent_transform.sent_to_bin_q(preds[i])
    print i, q
  except AssertionError:
    pass
