#!/usr/bin/python

# This is the top-level ./answer program. It takes 3 CL arguments:
# - filename of the Wiki article to answer questions about
# - filename of the file containing questions, 1 per line
# - team member currently running the script (in ['Jemmin', 'Ashley', 'Rohan',
#   Eileen']); this is needed to set the correct location parameters to run
#   the Stanford parser

import sys
import parse_article
import similarity

article_filename = sys.argv[1]
questions_filename = sys.argv[2]

# TODO: use information from previous questions? E.g. use commonly seen NNP as default referent for pronoun in question?

# do it
sentences = parse_article.parse_html(article_filename)
lisf = similarity.calculate_lisf(sentences)
with open(questions_filename) as questions_file:
  for line in questions_file:
    print '--------------------------------------------------------'
    print line
    print '******'
    print similarity.closest_sentence(line, sentences, lisf)
    print '--------------------------------------------------------'
