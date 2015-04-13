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
import wh_gapify
import stanford_ner

article_filename = sys.argv[1]
num_questions = int(sys.argv[2])
user = sys.argv[3]

# parse HTML into sentences, parse sentences into trees
sentences = parse_article.parse_html(article_filename)
# trim super-long sentences (60 or more words)
sentences = [s for s in sentences if s.count(' ') < 60]
parser = stanford_parser.create_parser(user)
parse_trees = parser.raw_parse_sents(sentences)

# augment trees with appositions transformed into predicates
appos = extract.find_appositions(parse_trees)
appo_sentences = [sent_transform.apposition_to_sent(appo) for appo in appos]
transformed = parser.raw_parse_sents(appo_sentences)
parse_trees += transformed

# create stanford NER tagger
tagger = stanford_ner.create_tagger(user)

# now find all predicates in augmented tree list
preds = extract.find_predicates(parse_trees)
for i in xrange(len(preds)):
  sent = sent_transform.tree_to_string(preds[i])
  print sent
  tags = tagger.tag([sent])
  wh = wh_gapify.get_all_wh(preds[i], tags)
  print 'wh questions found:', sum([len(l) for l in wh.values()])
  print '--------------------------------------------------------'
  for possibles_list in wh.values():
    for (gappy, wh_phrase) in possibles_list:
      try:
        q = ' '.join([wh_phrase, sent_transform.sent_to_bin_q(gappy)])
        print i, q
      except AssertionError:
        print i, 'assert failed'
      except:
        print i, 'other error'
  print '--------------------------------------------------------'
  try:
    q = sent_transform.sent_to_bin_q(preds[i])
    print i, q
  except AssertionError:
    print i, 'assert failed'
  except:
    print i, 'other error'
  print '--------------------------------------------------------'
