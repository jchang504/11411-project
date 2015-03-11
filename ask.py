#!/usr/bin/python

# This is the top-level ./ask program. It takes 3 CL arguments:
# - filename of the Wiki article to ask questions about
# - number of questions to ask
# - team member currently running the script (in ['Jemmin', 'Ashley', 'Rohan',
#   Eileen']); this is needed to set the correct location parameters to run
#   the Stanford parser

import sys
import parse
import extract
import transform

article_filename = sys.argv[1]
num_questions = sys.argv[2]
user = sys.argv[3]

# do it
parse.set_params(user)
parse_trees = parse.parse_html(article_filename)
pattern_matches = extract.find_matches(parse_trees)
questions = transform.make_questions(pattern_matches)
for q in questions:
  print q
