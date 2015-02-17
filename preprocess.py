from bs4 import BeautifulSoup
#from bs4 import SoupStrainer
#from bs4.diagnose import diagnose
import urllib2
from nltk.tokenize import sent_tokenize#, word_tokenize
#from nltk.corpus import brown
import nltk
from pattern.en import parsetree

# def parseHTML(fileName):
#     soup = BeautifulSoup(open(fileName), "html5lib")
#     print soup.find_all("p")
#     print (soup.get_text()).encode("utf8")

# def parse(tokens):
#     # hopefully this will be trained on something more useful
#     grammar1 = nltk.CFG.fromstring("""
#         S -> NP VP
#         VP -> V NP | V NP PP
#         PP -> P NP
#         V -> "saw" | "ate" | "walked"
#         NP -> "John" | "Mary" | "Bob" | Det N | Det N PP
#         Det -> "a" | "an" | "the" | "my"
#         N -> "man" | "dog" | "cat" | "telescope" | "park"
#         P -> "in" | "on" | "by" | "with"
#         """)
#     parser = nltk.RecursiveDescentParser(grammar1)
#     return [parser.parse(line) for line in tokens]

# The problem with the NLTK Parser is that you have to train it with your own
# data so I just used Pattern instead... heeh

def parseHTML(url):
    # Right now, opening the HTML file via the URL instead of locally
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read())
    body = soup.find_all('p')
    getBody = [(line.get_text().encode('utf-8')) for line in body]
    final = "".join(getBody)
    tokens = sent_tokenize(final)
    parseTokens = [parsetree(line,relations=True,lemmata=True) for line in tokens]
    #print tokens
    return parseTokens

def test():
    testURLs = ["Frame_drum","Kanjira","Equinox"]
    for url in testURLs:
        fullURL = "http://en.wikipedia.org/wiki/"+url
        print parseHTML(fullURL)
        print "\n\n"

test()