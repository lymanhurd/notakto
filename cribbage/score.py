import logging

from crib_utils import card_value

# Number of points earned by 0-4 copies of the same card value.
PAIRS = (0, 0, 2, 6, 12)


def scores(hand, crib, start):
    hs = score(hand, start)
    cs = score(crib, start, is_crib=True) if crib else 0
    return hs, cs


def score(hd, start, is_crib = False):
    hand = hd[:]
    points = 0
    # nibs
    start_suit = start // 13
    for h in hand:
        if start_suit == h // 13 and h % 13 == 10:
            points += 1
    suit0 = hand[0] // 13
    # flush
    flush = True
    for h in hand[1:]:
        if h // 13 != suit0:
            flush = False
            break
    if flush:
        if suit0 == start_suit:
            points += 5
        elif not is_crib:
            points += 4
        logging.info('flush')
    logging.info('1st score = %d' % points)
    # all subsequent clauses do not distinguish starter card form hand cards
    hand.append(start)
    # pairs, pair royals, double pair royal
    hist = 13 * [0]
    for h in hand:
        hist[h % 13] += 1
    logging.info(hist)
    run = 0
    product = 1
    for n in hist:
        points += PAIRS[n]
        # a zero means a run is broken
        if n == 0:
            if run >= 3:
                points += run * product
            run = 0
            product = 1
        else:
            product *= n
            run += 1
    if hist[-1] == 1 and run >= 3:
        points += run * product        
    logging.info('run = %d' % run)
    logging.info('score = %d' % points)
    # 15's
    points += 2 * _ways_to_make_sum(15, [card_value(h) for h in hand])
    logging.info('final score = %d' % points)
    return points


def score_sequence(seq):
    logging.info('(1) seq = %s' % seq)
    # truncate
    count = 0
    start = 0
    points = 0
    for i, c in enumerate(seq):
        if card_value(c) + count <= 31:
            count += card_value(c)
        else:
            count = card_value(c)
            start = i
    if count == 15 or count == 31:
        points += 2

    seq = seq[start:]
    logging.info('(2) seq = %s' % seq)
    logging.info('-points = %s' % points)

    # check for pair, pair royal, double pair royal
    cv = seq[-1]
    run = 1
    for s in reversed(seq[:-1]):
        if cv != s % 13:
            break
        else:
            run += 1
    points += PAIRS[run]
    logging.info('--points = %s' % points)
    # check for runs
    if len(seq) >= 3:
        for i in range(min(len(seq), 8), 2, -1):
            if _is_run(seq[-i:]):
                points += i
                break
    logging.info('---points = %s' % points)
    return points


def _ways_to_make_sum(n, l):
    if n <= 0 or len(l) == 0:
        return 0
    if l[0] == n:
        return 1 + _ways_to_make_sum(n, l[1:])
    else:
        return _ways_to_make_sum(n - l[0], l[1:]) + _ways_to_make_sum(n, l[1:])


def _is_run(sub_seq):
    seq_len = len(sub_seq)
    val_seq = [s % 13 for s in sub_seq]
    if max(val_seq) - min(val_seq) != seq_len - 1:
        return False
    if len(set(val_seq)) != seq_len:
        return False
    return True
