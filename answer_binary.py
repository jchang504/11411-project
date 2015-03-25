from nltk.corpus import wordnet as wn
from nltk import word_tokenize
import string

def ctNeg(negWords,sentence):
    return reduce(lambda x,y:x+y,
        map(lambda x: 1 if x in negWords else 0,sentence))

def isPositive(question,answer):
    return True # TODO: fix
    negWords = set(["no","not","isn't"])
    negQtns = ctNeg(negWords,question)
    negAns = ctNeg(negWords,answer)
    return (negQtns <= negAns)

def filterPunc(x):
  return x not in string.punctuation

def answerBinary(question,answer):
    question_tokens = filter(filterPunc, word_tokenize(question))
    answer_tokens = filter(filterPunc, word_tokenize(answer))
    status = True
    for word in question_tokens:
        # Check that all words in question are in the answer sentence
        if word not in answer_tokens:
            status = False # Temporarily assume it's not gonna work out
            # Generate all synonyms, ignoring POS
            synonyms = [(str(synset.name()).split(".")[0]) for synset
            in wn.synsets(word)]
            # Check all synonyms for possible matches
            for synonym in synonyms:
                if synonym in answer_tokens:
                    status = True # It's okay after all
                    break
    if status and isPositive(question,answer):
        return "Yes"
    return "No"

#answerBinary("is the earth round","the earth is round and blah blah keep going")
#answerBinary("is the earth round","the thymine is round and blah blah keep going")
#answerBinary("is the earth not round","the earth is round and blah blah keep going")
#answerBinary("is the earth round","the thymine is not round and the earth is round blah blah keep going")
