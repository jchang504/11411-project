#!/usr/bin/python

import os
from bs4 import BeautifulSoup
from nltk.tree import Tree
from nltk.tokenize import sent_tokenize
from nltk.parse.stanford import StanfordParser

# locations of Stanford parser/models, Java, and English PCFG model
USER_STANFORD_PARAMS = {}
JEMMIN_STANFORD_ROOT = '/usr/lib/stanford-parser-full-2015-01-30'
USER_STANFORD_PARAMS['Jemmin'] = [JEMMIN_STANFORD_ROOT, JEMMIN_STANFORD_ROOT, '/usr/bin/java', JEMMIN_STANFORD_ROOT + '/englishPCFG.ser.gz']
ASHLEY_STANFORD_ROOT = '/usr/local/Cellar/stanford-parser/3.4/libexec'
USER_STANFORD_PARAMS['Ashley'] = [ASHLEY_STANFORD_ROOT, ASHLEY_STANFORD_ROOT, '/Library/Java/JavaVirtualMachines/jdk1.7.0_67.jdk/Contents/Home/jre/bin', ASHLEY_STANFORD_ROOT + '/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz']

# sets EVs and ENGLISH_PCFG_LOC to correct values for given user
def set_params(user):
  params = USER_STANFORD_PARAMS[user]
  os.environ['STANFORD_PARSER'] = params[0]
  os.environ['STANFORD_MODELS'] = params[1]
  os.environ['JAVAHOME'] = params[2]
  global ENGLISH_PCFG_LOC
  ENGLISH_PCFG_LOC = params[3]

# REQUIRES: run set_params(name) first, or Stanford parser won't work
# returns a list of parse trees for the sentences of the article stored in
# wiki_filename
def parse_html(wiki_filename):
    with open(wiki_filename) as wikifile:
      soup = BeautifulSoup(wikifile)
    # get rid of citations like "[1]", etc.
    for citation in soup.find_all('sup'):
      citation.decompose()
    # all the useful info in wiki articles are in <p> tags
    paragraphs = soup.find_all('p')
    # combine paragraphs, segment sentences, and parse into Trees
    paragraphs_text = [p.get_text() for p in paragraphs]
    all_text = ' '.join(paragraphs_text)
    sentences = sent_tokenize(all_text)
    parser = StanfordParser(model_path=ENGLISH_PCFG_LOC)
    # (ignore non-ASCII characters)
    parse_trees = parser.raw_parse_sents([s.encode('ascii', 'ignore') for s in sentences])
    return parse_trees
