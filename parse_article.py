from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize

# returns the main text of the Wikipedia article as a list of sentence strings
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
    return [s.encode('ascii', 'ignore') for s in sentences]
