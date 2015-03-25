#!/usr/bin/python

# This is the top-level ./answer program. It takes 3 CL arguments:
# - filename of the Wiki article to answer questions about
# - filename of the file containing questions, 1 per line
# - team member currently running the script (in ['Jemmin', 'Ashley', 'Rohan',
#   Eileen']); this is needed to set the correct location parameters to run
#   the Stanford parser

import sys
import parse_article
import select_sentence
import answer_binary

article_filename = sys.argv[1]
questions_filename = sys.argv[2]
user = sys.argv[3] # TODO: unnecessary right now

# do it
sentences = parse_article.parse_html(article_filename)
with open(questions_filename) as questions_file:
  for line in questions_file:
    (idc, sentence) = select_sentence.get_top_n_sentences(line, sentences, 1)[0]
    print answer_binary.answerBinary(line, sentence)
