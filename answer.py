#!/usr/bin/python

# This is the top-level ./answer program. It takes 3 CL arguments:
# - filename of the Wiki article to answer questions about
# - filename of the file containing questions, 1 per line
# - user - this is needed to set the correct location parameters to run the
#   Stanford parser

import sys
import parse_article
import stanford_parser
import sent_transform
import sent_extract
import stanford_ner
import wh_extract
import similarity

article_filename = sys.argv[1]
questions_filename = sys.argv[2]
user = sys.argv[3]

# parse HTML into sentences
sentences = parse_article.parse_html(article_filename)

# calculate log inverse sentence frequencies
lisf = similarity.calculate_lisf(sentences)

# create Stanford parser and NER Tagger
parser = stanford_parser.create_parser(user)
tagger = stanford_ner.create_tagger(user)

# read questions
with open(questions_filename) as questions_file:
  questions = questions_file.read().splitlines()

# parse questions
question_trees = parser.raw_parse_sents(questions)

# find answers!
for i in xrange(len(questions)):

  # determine question type
  (question_type, bin_form) = sent_transform.q_type(question_trees[i][0])

  # can't determine q type - best we can do is print the closest sentence
  if question_type is None:
    print similarity.closest_sentence(questions[i], sentences, lisf)

  else:
    # find the closest match sentence from the article
    transformed_q = sent_transform.bin_q_to_sent(bin_form)
    answer_sent = similarity.closest_sentence(transformed_q, sentences, lisf)

    # binary question
    if question_type == sent_transform.BINARY:
      pass

    # wh-question
    else:
      answer_trees = parser.raw_parse(answer_sentence)
      wh_searchable = sent_extract.find_predicates(answer_trees)

      # has canonical wh-gap structures - consider these answers first
      if len(wh_searchable) > 0:
        wh_func = getattr(wh_extract, question_type)
        if wh_func in wh_extract.JUST_SYNTAX:
          wh_matches = wh_func(wh_searchable[0], True)
        elif wh_func in wh_extract.NEEDS_NER:
          tags = tagger.tag(sent_transform.tree_to_string(wh_searchable[0]))
          wh_matches = wh_func(wh_searchable[0], tags, True)

        # consider canonical form answers
        for (gappy, gap_phrase) in wh_matches:
          
        # compare cosine sims of each gappy with transformed bin_form sentence
        # tiebreak with max_overlap
      # if not searchable or no wh_matches, fall back to simple matches
      # what -> NP, who -> PERSON, etc.
      # TODO: pronouns!!!


  #print similarity.max_overlap_sentence(question, sentences)
  print '--------------------------------------------------------'
