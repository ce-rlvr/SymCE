import sympy as sp
import math
import itertools
import functools

def conditions(witness):
    N, M, a, b = None, None, None, None
    try:
        if isinstance(witness, dict):
            N = witness.get('N')
            M = witness.get('M')
            a = witness.get('a')
            b = witness.get('b')
        elif hasattr(witness, '__len__') and not isinstance(witness, str):
            if len(witness) >= 4:
                N, M, a, b = witness[:4]
        else:
            N = getattr(witness, 'N', None)
            M = getattr(witness, 'M', None)
            a = getattr(witness, 'a', None)
            b = getattr(witness, 'b', None)
    except Exception:
        pass

    try:
        h1 = int(N) == N and N > 0
    except Exception:
        h1 = False

    try:
        h2 = isinstance(M, (int, float, sp.Expr)) and float(M) > 0
    except Exception:
        h2 = False

    try:
        a_val = float(a)
        b_val = float(b)
        h3 = a_val <= b_val
    except Exception:
        h3 = False

    try:
        neg_q = h3 and (a_val < b_val)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: N is a positive integer",
    "H_2: M > 0 is a real number",
    "H_3: The interval from a to b is a bounded closed interval in R",
    "¬Q: The family F is NOT uniformly equicontinuous on the interval"
]

N_HYP = 3
NEG_Q_INDEX = 3