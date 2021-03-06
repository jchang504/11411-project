import math
import random
from nltk import word_tokenize
from collections import Counter, defaultdict

# Tokenize sentences with NLTK's word_tokenize to get lists of tokens.
# Represent tf-isf vectors as dictionaries mapping words to weights

# returns index of c in candidates st the tf-isf vector for c is the closest
# to target of all candidates. Use lisf for the inverse sentence freqs
# REQUIRES: candidates is the same list used to calculate lisf!
def closest_sentence(target, candidates, lisf, tiebreak=False):
  best_cand_index = 0
  best_cosine = 0
  best_overlap = 0

  # calculate target sentence vector
  target_words = word_tokenize(target)
  target_tf = tf(target_words)
  target_vector = {}
  for word in target_tf:
    target_vector[word] = target_tf[word] * lisf[word]

  # for each candidate:
  for cand_index in xrange(len(candidates)):
    candidate = candidates[cand_index]
    # calculate candidate sentence vector
    candidate_words = word_tokenize(candidate)
    candidate_tf = tf(candidate_words)
    candidate_vector = {}
    for word in candidate_tf:
      candidate_vector[word] = candidate_tf[word] * lisf[word]

    # compare cosine similarity to best so far
    cosine_sim = dot(target_vector, candidate_vector) / norm(candidate_vector)
    if cosine_sim > best_cosine:
      best_cand_index = cand_index
      best_cosine = cosine_sim
      if tiebreak:
        best_overlap = overlap(target_words, candidate_words)

    # possible tiebreak with overlap
    elif cosine_sim == best_cosine and tiebreak:
      candidate_overlap = overlap(target_words, candidate_words)
      if candidate_overlap > best_overlap:
        best_cand_index = cand_index
        # best_cosine is same
        best_overlap = candidate_overlap

  return best_cand_index

# returns a tuple (sentence, overlap) where sentence is the sentence in
# candidates with the longest contiguous sequence of overlapping words in
# common with target, and overlap is the overlap
def max_overlap_sentence(target, candidates):
  best_sentence = None
  max_overlap = 0
  random.shuffle(candidates) # the final tiebreaker is luck!

  # target word list
  target_words = word_tokenize(target)

  for candidate in candidates:
    candidate_words = word_tokenize(candidate)
    candidate_overlap = overlap(target_words, candidate_words)
    if candidate_overlap > max_overlap:
      best_sentence = candidate
      max_overlap = candidate_overlap

  return (best_sentence, max_overlap)

# TODO: inefficient - use dynamic programming!
# calculates the length of the longest common contiguous sequence of words in
# word lists s1 and s2
def overlap(s1, s2):
  length = 0
  for i in xrange(len(s1)):
    for j in xrange(len(s2)):
      prefix = longest_common_prefix(s1, i, s2, j)
      if prefix > length:
        length = prefix
  return length

# calculates the length of the longest common prefix of word lists s1 and s2
def longest_common_prefix(s1, start1, s2, start2):
  length = 0
  for i in xrange(min(len(s1) - start1, len(s2) - start2)):
    if s1[start1 + i] != s2[start2 + i]:
      break
    length += 1
  return length

# calculate the log inverse sentence frequencies of each word in the sentences
# RETURNS: a dictionary mapping words to their inverse sentence frequencies
def calculate_lisf(sentences):
  N = len(sentences)
  sf = Counter()

  # count sentence frequencies of all words
  for sentence in sentences:
    seen_words = set()
    for word in word_tokenize(sentence):
      if word not in seen_words:
        sf[word] += 1
        seen_words.add(word)

  lisf = defaultdict(int)
  # lisf = log(N / sf)
  for word in sf:
    lisf[word] = math.log(float(N) / sf[word])

  return lisf

# returns a Counter mapping each word to its frequency in word_list 
def tf(word_list):
  tfs = Counter()
  for word in word_list:
    tfs[word] += 1
  return tfs

# calculates the dot product of vectors v1 and v2
def dot(v1, v2):
  total = 0
  for dim in v1:
    if dim in v2:
      total += v1[dim] * v2[dim]
  return total

# calculate and return the norm (length) of a vector v
def norm(v):
  total = 0
  for dim in v:
    total += v[dim] ** 2
  return math.sqrt(total)
