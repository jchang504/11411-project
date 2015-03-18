#!/usr/bin/python

# This is the top-level ./ask program. It takes 3 CL arguments:
# - filename of the Wiki article to ask questions about
# - number of questions to ask
# - team member currently running the script (in ['Jemmin', 'Ashley', 'Rohan',
#   Eileen']); this is needed to set the correct location parameters to run
#   the Stanford parser

import sys
import stanford_parser
import parse_article
import extract
import transform

article_filename = sys.argv[1]
num_questions = sys.argv[2]
user = sys.argv[3]

# do it
stanford = stanford_parser.create_parser(user)
sentences = parse_article.parse_html(article_filename)
parse_trees = stanford.raw_parse_sents(sentences)
pattern_matches = extract.find_matches(parse_trees)
questions = transform.make_questions(pattern_matches)
for q in questions:
  print q
