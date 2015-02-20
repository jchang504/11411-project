from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
import nltk
from pattern.en import parsetree

def parseHTML(filename):
    soup = BeautifulSoup(open(filename))
    body = soup.find_all('p')
    getBody = [(line.get_text().encode('utf-8')) for line in body]
    final = "".join(getBody)
    tokens = sent_tokenize(final)
    parseTokens = [parsetree(line,relations=True,lemmata=True) for line in tokens]
    return parseTokens

print parseHTML("kanjira.html")