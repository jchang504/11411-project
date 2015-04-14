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

# returns the best found answer of question_type for the transformed q, based
# on the selected answer_sent
def answer_wh(question_type, answer_sent, transformed_q):
  # parse answer sentence and peel out of list and ROOT context
  answer_tree = parser.raw_parse(answer_sent)[0][0]
  tags = tagger.tag([sent_transform.tree_to_string(answer_tree)])
      
  # find any constituent that matches the question_type
  condition_func = getattr(wh_extract, 'is_' + question_type)
  matches = wh_extract.find_all_matches(answer_tree, [], tags,
      condition_func)
  
  if len(matches) > 0:
    # compare gappy forms to transformed q
    gappies = [sent_transform.tree_to_string(gappy) for (gappy, answer) in
        matches]
    best_index = similarity.closest_sentence(transformed_q, gappies,
        lisf, tiebreak=True)
    return sent_transform.tree_to_string(matches[best_index][1])
      
  # last resort: just return sentence
  else:
    return answer_sent

### MAIN IS HERE ###

article_filename = sys.argv[1]
questions_filename = sys.argv[2]
user = sys.argv[3]

# parse HTML into sentences
sentences = parse_article.parse_html(article_filename)
# trim super-long sentences (60 or more words)
sentences = [s for s in sentences if s.count(' ') < 60]

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
    sent_index = similarity.closest_sentence(questions[i], sentences, lisf)
    print 'unident:', sentences[sent_index]

  else:
    # find the closest match sentence from the article
    try:
      transformed_q = sent_transform.bin_q_to_sent(bin_form)
    except:
      transformed_q = sent_transform.tree_to_string(bin_form)

    sent_index = similarity.closest_sentence(transformed_q, sentences, lisf)
    answer_sent = sentences[sent_index]

    # binary question
    if question_type == sent_transform.BINARY:
      print 'binary q answer'

    # wh-question
    else:
      try:
        print 'wh:', answer_wh(question_type, answer_sent, transformed_q)
      except:
        print 'error calling: answer_wh(%s, %s, %s)' % (question_type,
            answer_sent, transformed_q)
