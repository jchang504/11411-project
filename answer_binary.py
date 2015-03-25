from nltk.corpus import wordnet as wn

def ctNeg(negWords,sentence):
    return reduce(lambda x,y:x+y,
        map(lambda x: 1 if x in negWords else 0,sentence))

def isPositive(question,answer):
    negWords = set(["no","not","isn't"])
    negQtns = ctNeg(negWords,question)
    negAns = ctNeg(negWords,answer)
    return (negQtns <= negAns)

def answerBinary(question,answer):
    question = question.lower().split()
    answer = answer.lower().split()
    status = True
    for word in question:
        # Check that all words in question are in the answer sentence
        if word not in answer:
            status = False # Temporarily assume it's not gonna work out
            # Generate all synonyms, ignoring POS
            synonyms = [(str(synset.name()).split(".")[0]) for synset
            in wn.synsets(word)]
            # Check all synonyms for possible matches
            for synonym in synonyms:
                if synonym in answer:
                    status = True # It's okay after all
                    break
    if status and isPositive(question,answer):
        print "Yes"
        return
    print "No"

answerBinary("is the earth round","the earth is round and blah blah keep going")
answerBinary("is the earth round","the thymine is round and blah blah keep going")
answerBinary("is the earth not round","the earth is round and blah blah keep going")
answerBinary("is the earth round","the thymine is not round and the earth is round blah blah keep going")