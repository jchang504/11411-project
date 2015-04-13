import math
from nltk import word_tokenize
from collections import Counter, defaultdict

# Tokenize sentences with NLTK's word_tokenize to get lists of tokens.
# Represent tf-isf vectors as dictionaries mapping words to weights

# returns s in sentences st the tf-isf vector for s is the closest to
# target_sentence of all sentences. Use lisf for the inverse sentence freqs
# REQUIRES: sentences is the same list used to calculate lisf!
def closest_sentence(target_sentence, sentences, lisf):
  best_sentence = None
  best_cosine = 0

  # calculate target sentence vector
  target_words = word_tokenize(target_sentence)
  target_tf = tf(target_words)
  target_vector = {}
  for word in target_tf:
    target_vector[word] = target_tf[word] * lisf[word]

  # for each sentence, calculate its vector and compare to the target
  for candidate in sentences:
    candidate_words = word_tokenize(candidate)
    candidate_tf = tf(candidate_words)
    candidate_vector = {}
    for word in candidate_tf:
      candidate_vector[word] = candidate_tf[word] * lisf[word]

    # compare cosine similarity to best so far
    cosine_sim = dot(candidate_vector, target_vector) / norm(candidate_vector)
    if cosine_sim > best_cosine:
      best_sentence = candidate
      best_cosine = cosine_sim

  return best_sentence

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
