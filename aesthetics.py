import re

# make the sentence look like a proper declarative or question, adding/removing
# punctuation, replacing those ugly -LRB- and -RRB-, and capitalizing the
# sentence
def make_pretty(sentence, end_punctuation):
  sentence.replace('-LRB- ', '(')
  sentence.replace(' -RRB-', ')')
  sentence = re.sub(r' *([,;:\.\?!])', r'\1', sentence)
  m = re.match(r'([^\.\?!]+)[\.\?!]*', sentence)
  sentence = m.group(1)
  sentence = sentence[0].upper() + sentence[1:]
  return sentence + end_punctuation
