#!/usr/bin/python

# This is the top-level ./answer program. It takes 3 CL arguments:
# - filename of the Wiki article to answer questions about
# - filename of the file containing questions, 1 per line
# - user - this is needed to set the correct location parameters to run the
#   Stanford parser

import sys
from tags import *
from nltk.tree import Tree
import parse_article
import stanford_parser
import sent_transform
import sent_extract
import stanford_ner
import wh_extract
import similarity
import confound
import aesthetics

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

# returns 'yes' or 'no'
def answer_bin(answer_sent, transformed_q):
  transformed_q_tree = parser.raw_parse(transformed_q)[0][0]

  # returns True if all the verbs, nouns, adjectives, and adverbs in tree are
  # found in reference (or synonyms/hyponyms thereof)
  def sorta_in(tree, reference):

    pos = tree.label()
    check = False
    if is_noun_head(pos):
      pos = confound.WN_NOUN
      check = True
    elif is_tensed_verb(pos):
      pos = confound.WN_VERB
      check = True
    elif is_adjective(pos):
      pos = confound.WN_ADJ
      check = True
    elif pos == 'RB':
      pos = confound.WN_ADV
      check = True

    # if noun, verb, adj, or adv, check current node
    if check:
      if tree[0] not in reference:
        found = False
        syn_or_hypos = confound.synonyms(tree[0], pos)
        for sh in syn_or_hypos:
          if sh in reference:
            found = True
            break
        if not found:
          return False
    
    # check children
    for child in tree:
      if isinstance(child, Tree):
        if not sorta_in(child, reference):
          return False
    return True

  if sorta_in(transformed_q_tree, answer_sent):
    return 'yes'
  else:
    return 'no'

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

# check lengths, and don't parse super long (< 60 words) questions lest we
# crash the Stanford parser
no_parse = [i for i in xrange(len(questions)) if questions[i].count(' ') > 60]
parsable_questions = []
for i in xrange(len(questions)):
  if i in no_parse:
    parsable_questions.append('Is this it?')
  else:
    parsable_questions.append(questions[i])
  
# parse questions
question_trees = parser.raw_parse_sents(parsable_questions)

# find answers!
for i in xrange(len(questions)):

  # determine question type
  (question_type, bin_form) = sent_transform.q_type(question_trees[i][0])

  # check if question was parsable
  if i in no_parse:
    question_type = None

  # can't determine q type - best we can do is print the closest sentence
  if question_type is None:
    sent_index = similarity.closest_sentence(questions[i], sentences, lisf)
    print sentences[sent_index]

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
      try:
        answer = answer_bin(answer_sent, transformed_q)
        print aesthetics.make_pretty(answer, '.')
      except:
        print answer_sent

    # wh-question
    else:
      try:
        answer = answer_wh(question_type, answer_sent, transformed_q)
        print aesthetics.make_pretty(answer, '.')
      except:
        print answer_sent
