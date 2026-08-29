import math
from itertools import combinations

# Top-level setup
# (No specific named bindings required for this number theory conjecture)

CONDITION_LABELS = [
    "H_1: m_1, m_2, ..., m_k are pairwise coprime positive integers",
    "H_2: d is a positive integer",
    "¬Q: M_d(Z/nZ) is not isomorphic to the direct product of M_d(Z/m_iZ)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)

def _prod(iterable):
    res = 1
    for x in iterable:
        res *= x
    return res

def conditions(witness):
    try:
        if isinstance(witness, dict):
            m_list = witness['m_list']
            d = witness['d']
            n = witness['n']
        elif hasattr(witness, 'm_list') and hasattr(witness, 'd') and hasattr(witness, 'n'):
            m_list = witness.m_list
            d = witness.d
            n = witness.n
        else:
            m_list, d, n = witness
    except Exception:
        return [False, False, False]

    # H_1: m_1, m_2, ..., m_k are pairwise coprime positive integers
    try:
        h1_ok = False
        if isinstance(m_list, (list, tuple)):
            if all(is_int(m) and m > 0 for m in m_list):
                h1_ok = True
                for x, y in combinations(m_list, 2):
                    if math.gcd(x, y) != 1:
                        h1_ok = False
                        break
    except Exception:
        h1_ok = False

    # H_2: d is a positive integer
    try:
        h2_ok = is_int(d) and d > 0
    except Exception:
        h2_ok = False

    # ¬Q: M_d(Z/nZ) is not isomorphic to the direct product of M_d(Z/m_iZ)
    try:
        neg_q_ok = False
        if is_int(n):
            prod_m = _prod(m_list)
            # They are isomorphic iff |n| == prod_m
            neg_q_ok = abs(n) != prod_m
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]