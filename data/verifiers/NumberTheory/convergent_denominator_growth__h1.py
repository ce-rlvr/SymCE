import sympy
from sympy import Rational

def fib(k):
    a, b = 0, 1
    for _ in range(k):
        a, b = b, a + b
    return a

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness should be a sequence of continued fraction coefficients [a_0, a_1, ..., a_N].
    """
    try:
        w = list(witness)
    except Exception:
        return [False, False]
    
    if not w:
        return [False, False]

    # H_1: Assume a_i >= 1 for all integers i >= 1
    try:
        h1 = True
        for i in range(1, len(w)):
            if w[i] < 1:
                h1 = False
                break
    except Exception:
        h1 = False

    # ¬Q: q_n < F_{n+1} for some integer n >= 0
    # where q_n is the denominator of the n-th convergent
    neg_q = False
    try:
        for n in range(len(w)):
            a_list = w[:n+1]
            c = sympy.Rational(a_list[-1])
            for a in reversed(a_list[:-1]):
                c = sympy.Rational(a) + 1 / c
            
            q_n = c.q
            if q_n < fib(n + 1):
                neg_q = True
                break
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a_i >= 1 for all integers i >= 1",
    "¬Q: q_n < F_{n+1} for some integer n >= 0"
]

N_HYP = 1
NEG_Q_INDEX = 1