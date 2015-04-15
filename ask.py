#!/usr/bin/python

# This is the top-level ./ask program. It takes 3 CL arguments:
# - filename of the Wiki article to ask questions about
# - number of questions to ask
# - user - this is needed to set the correct location parameters to run
#   the Stanford parser

import sys
import copy
import parse_article
import stanford_parser
import sent_extract
import sent_transform
import wh_extract
import stanford_ner
import confound
import rank
import aesthetics

article_filename = sys.argv[1]
num_questions = int(sys.argv[2])
user = sys.argv[3]

# parse HTML into sentences, parse sentences into trees
sentences = parse_article.parse_html(article_filename)
# trim super-long sentences (60 or more words)
sentences = [s for s in sentences if s.count(' ') < 60]
# limit number of sentences
if len(sentences) > 200:
  sentences = sentences[:200]
parser = stanford_parser.create_parser(user)
parse_trees = parser.raw_parse_sents(sentences)

# augment trees with appositions transformed into predicates
appos = sent_extract.find_appositions(parse_trees)
appo_sentences = [sent_transform.apposition_to_sent(appo) for appo in appos]
transformed = parser.raw_parse_sents(appo_sentences)
parse_trees += transformed

# create stanford NER tagger
tagger = stanford_ner.create_tagger(user)

# now find all predicates in augmented tree list
preds = sent_extract.find_predicates(parse_trees)

wh_questions = dict([(wh, []) for wh in ['how_many', 'how', 'why', 'which',
'whose', 'who_whom', 'where', 'when', 'what']])
bin_questions = []
confounded_questions = []
# make questions from predicates
for i in xrange(len(preds)):
  try:
    sent = sent_transform.tree_to_string(preds[i])
    tags = tagger.tag([sent])

    # make wh-questions
    wh = wh_extract.get_all_wh(preds[i], tags)
    for wh_word, possibles_list in wh.iteritems():
      for (gappy, wh_phrase) in possibles_list:
        try:
          q = ' '.join([wh_phrase, sent_transform.sent_to_bin_q(gappy)])
          wh_questions[wh_word].append(q)
        except:
          pass

    # make binary question
    try:
      q = sent_transform.sent_to_bin_q(preds[i])
      bin_questions.append(q)
    except:
      pass

    # make confounded binary question
    try:
      sent_copy = copy.deepcopy(sent)
      (confounded, success) = confound.try_confound(sent_copy)
      if success:
        q = sent_transform.sent_to_bin_q(confounded)
        confounded_questions.append(q)
    except:
      pass
  except:
    pass

final = rank.get_best_n(wh_questions, bin_questions, confounded_questions,
    num_questions)
for q in final:
  print aesthetics.make_pretty(q, '?')
