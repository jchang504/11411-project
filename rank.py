import random

# for question ranking

# returns a list of the best n questions
def get_best_n(wh_questions, bin_questions, confounded_questions, n):
  best_list = []

  (whr, whl, whs) = sort_by_wh(wh_questions)
  (br, bl, bs) = sort_by_length(bin_questions)
  (cr, cl, cs) = sort_by_length(confounded_questions)

  while len(whr) + len(br) + len(cr) > 0 and len(best_list) < n:
    if len(whr) > 0:
      best_list.append(whr.pop(0))
    if len(cr) > 0:
      best_list.append(cr.pop(0))
    if len(br) > 0:
      best_list.append(br.pop(0))

  if len(best_list) < n:
    best_list += whl
  if len(best_list) < n:
    best_list += bl
  if len(best_list) < n:
    best_list += cl
  if len(best_list) < n:
    best_list += whs
  if len(best_list) < n:
    best_list += bs
  if len(best_list) < n:
    best_list += cs

  # still don't have enough??
  if len(best_list) < n:
    best_list += ['What is the meaning of life?' for i in
        xrange(n - len(best_list))]

  return best_list[:n]

# heuristics - prefer certain words
WH_ORDER = ['how_many', 'which', 'whose', 'why', 'who_whom', 'when', 'where',
    'how', 'what']

# sort by heuristic preferences for wh words
def sort_by_wh(wh_questions):
  just_right = []
  too_long = []
  too_short = []

  # sort each wh-word list by length first
  for wh_word in WH_ORDER:
    (wh_right, wh_long, wh_short) = sort_by_length(wh_questions[wh_word])
    just_right += wh_right
    too_long += wh_long
    too_short += wh_short

  return (just_right, too_long, too_short)

MIN_LENGTH = 5
MAX_LENGTH = 30
# put the ones between MIN and MAX first, then those over MAX, then those under
# MIN
def sort_by_length(questions):
  just_right = []
  too_long = []
  too_short = []
  for q in questions:
    if q.count(' ') < MIN_LENGTH:
      too_short.append(q)
    elif q.count(' ') > MAX_LENGTH:
      too_long.append(q)
    else:
      just_right.append(q)

  # mix them all up
  random.shuffle(just_right)
  random.shuffle(too_long)
  random.shuffle(too_short)

  return (just_right, too_long, too_short)
