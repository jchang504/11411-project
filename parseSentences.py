"""
NLP Project, Spring 2015

Eileen Jiang, Ashley Lai, Jemmin Chang, Rohan Varma 
"""

import pattern 
from pattern.en import parse 

#takes in a sentence, parses it, and return list of tuples of the word and the corresponding chunk patterns to original words
def parseSent(sent): 
    s = parse(sent, relations=True, lemmata=True) 
    splitList = s.split()
    allSplitLists = splitList[0]
    parsedList = []
    for wordSentence in allSplitLists:
        sentWord = wordSentence[0]
        for word in wordSentence:
            if ("-" in word):
                startIndex = word.index("-")
                parsedChunk = word[startIndex+1:]
                parsedList.append((sentWord,parsedChunk))
                break
    return parsedList 

def tests():
    sent1 = 'The mobile web is more important than mobile apps.'
    print sent1
    print parseSent(sent1) 

    print 

    sent2 = "Drums may be played individually, with the player using a single drum, and some drums such as the djembe are almost always played in this way."
    print sent2
    print parseSent(sent2)
