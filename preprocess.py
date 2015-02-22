from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
import nltk, os
from nltk.parse.stanford import StanfordParser
from nltk.tree import Tree

# These will need to be changed based on each user
os.environ['STANFORD_PARSER'] = '/usr/local/Cellar/stanford-parser/3.4/libexec'
os.environ['STANFORD_MODELS'] = '/usr/local/Cellar/stanford-parser/3.4/libexec'
os.environ['JAVAHOME'] = '/Library/Java/JavaVirtualMachines/jdk1.7.0_67.jdk/Contents/Home/jre/bin'

def parseHTML(filename):
    soup = BeautifulSoup(open(filename))
    body = soup.find_all('p') #all the useful info in wiki articles are in <p> tags
    getText = [line.get_text() for line in body]
    final = "".join(getText)
    tokens = sent_tokenize(final)
    parser = StanfordParser(model_path="/usr/local/Cellar/stanford-parser/3.4/libexec/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
    parseTokens = [parser.raw_parse_sents((line.encode('ascii','ignore'),)) for line in tokens]
    result = map(lambda x: x[0], parseTokens) #extract singleton trees from list output
    return result