from __future__ import division
from __future__ import print_function

from cribbage.score import score

DENOMINATOR: int = 13 * 13 * 13


def crib_expect(c1: int, c2: int):
    total = 0
    for sc in range(13, 26):
        for o1 in range(13):
            for o2 in range(13):
                total += score((c1, c2, o1, o2), sc, True)
    return total / DENOMINATOR


def crib_expect_table(filename: str):
    with open(filename, 'w') as f:
        for c1 in range(13):
            for c2 in range(c1, 13):
                print('CRIB_EXPECTATION[%d][%d] = %f' % (c1, c2, crib_expect(c1, c2)), file=f)


if __name__ == '__main__':
    crib_expect_table('crib_expected_values.py')

