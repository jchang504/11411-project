#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nltk.data
from nltk import word_tokenize
import string, math
from collections import Counter

sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

text = "The kanjira is a relatively difficult Indian drum to play, especially in South Indian Carnatic music, for reasons including the complexity of the percussion patterns used in Indian music. It is normally played with the palm and fingers of the right hand, while the left hand supports the drum. The fingertips of the left hand can be used to bend the pitch by applying pressure near the outer rim. It is not tuned to any particular pitch, unlike the mridangam or the ghatam. Normally, without, it has a very high pitched sound. To get a good bass sound, the performer reduces the tension of the drumhead by sprinkling water on the inside of the instrument.[4] This process may have to be repeated during a concert to maintain a good sound. However, if the instrument is too moist, it will have a dead tone, requiring 5–10 minutes to dry. Tone is also affected by external temperature and moisture conditions. Performers typically carry a couple of kanjiras so that they can keep at least one in perfectly tuned condition at any given time. Similar to the Western tambourine, it consists of a circular frame made of the wood of the jackfruit tree, between 7 and 9 inches in width and 2 to 4 inches in depth. It is covered on one side with a drumhead made of monitor lizard skin (specifically the Bengal monitor,[2] Varanus bengalensis, now an endangered species in India), while the other side is left open. The frame has a single slit which contain three to four small metal discs (often old coins) that jingle when the kanjira is played. The kanjira, khanjira or ganjira, a South Indian frame drum, is an instrument of the tambourine family. As a folk and bhajan instrument, it has been used for many centuries. It was modified to a frame drum of a single pair of jingles by Manpoondia Pillai in the 1880's and was added to classical concerts during the 1930s. It is used primarily in concerts ofCarnatic music (South Indian classical music) as a supporting instrument for the mridangam."
text.encode


def get_sentences(text):
  sentence_list = sent_tokenizer.tokenize(text.strip())
  return map(lambda sentence: " ".join(sentence.split()), sentence_list)

def calculate_idfs(text, sentences):
  N = len(sentences)
  doc_counts = Counter()
  idfs = dict()
  for sentence in sentences:
    seen_words = set()
    for word in word_tokenize(sentence):
      if word not in string.punctuation:
        if word not in seen_words:
          doc_counts[word] += 1
          seen_words.add(word)
  for word in doc_counts:
    idfs[word] = math.log(float(N)/doc_counts[word])
  idfs["UNKNOWN"] = math.log(float(N))
  return idfs


def tfidf_length(sentence, idfs):
  seen_words = set()
  total = 0
  word_counts = Counter(word_tokenize(sentence))
  for word in word_tokenize(sentence):
    if word not in seen_words and word not in string.punctuation:
      seen_words.add(word)
      if word not in idfs:
        theIdfs = idfs["UNKNOWN"]
      else:
        theIdfs = idfs[word]
      total += ((word_counts[word] * theIdfs) ** 2)
  return total

def tfidf_dot_product(query, sentence, idfs):
  total_words = set(word_tokenize(query)).union(set(word_tokenize(sentence)))
  total = 0
  tf_q, tf_s = Counter(word_tokenize(query)), Counter(word_tokenize(sentence))
  for word in total_words:
    if word not in string.punctuation:
      if word not in idfs:
        theIdfs = idfs["UNKNOWN"]
      else:
        theIdfs = idfs[word]
      total += (tf_q[word] * tf_s[word] * (theIdfs ** 2))
  return total

def calculate_tf_idf(query, sentence, idfs):
  numerator = tfidf_dot_product(query, sentence, idfs)
  q_bot = tfidf_length(query, idfs)
  s_bot = tfidf_length(sentence, idfs)
  print 'query:', query
  print 'sent:', sentence
  return float(numerator) / (q_bot * s_bot)

def get_top_n_sentences(question, sentences, n):
  idfs = calculate_idfs(text, sentences)
  scores = []
  for sentence in sentences:
    tf_idf = calculate_tf_idf(question, sentence, idfs)
    scores.append((tf_idf, sentence))
  scores.sort()
  return scores[::-1][:n]

# TODO: no longer valid
print get_top_n_sentences("Is a kanjira a South Indian frame drum", text, 1)












