import re

# make the sentence look like a proper declarative or question, adding/removing
# punctuation, replacing those ugly -LRB- and -RRB-, and capitalizing the
# sentence
def make_pretty(sentence, end_punctuation):
  sentence = sentence.replace('-LRB- ', '(')
  sentence = sentence.replace(' -RRB-', ')')
  sentence = re.sub(r' *([,;:\.\?!])', r'\1', sentence)
  m = re.match(r'(.+\w+)[\.\?!,;: ]*', sentence)
  sentence = m.group(1)
  sentence = sentence[0].upper() + sentence[1:]
  return sentence + end_punctuation
