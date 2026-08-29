import sympy
from sympy import Rational

def conditions(witness) -> list[bool]:
    try:
        h1 = isinstance(witness, (list, tuple)) and len(witness) >= 1
        if h1:
            h1 = all(type(x) is int for x in witness)
            if h1 and len(witness) > 1:
                h1 = all(x >= 1 for x in witness[1:])
    except Exception:
        h1 = False

    try:
        h2 = True
    except Exception:
        h2 = False

    try:
        if not h1:
            neg_q = False
        else:
            n = len(witness) - 1
            
            q_k_1 = 0
            q_k = 1
            for i in range(1, n + 1):
                q_k_next = witness[i] * q_k + q_k_1
                q_k_1 = q_k
                q_k = q_k_next
            
            if q_k_1 == 0:
                neg_q = True
            else:
                lhs = Rational(q_k, q_k_1)
                
                rhs_list = witness[1:][::-1]
                if not rhs_list:
                    neg_q = True
                else:
                    rhs = Rational(rhs_list[-1], 1)
                    for a in reversed(rhs_list[:-1]):
                        rhs = a + 1 / rhs
                    
                    neg_q = (lhs != rhs)
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a_0 to a_n is a simple continued fraction",
    "H_2: q_k is the denominator of the k-th convergent",
    "¬Q: The ratio q_n / q_n-1 is not exactly equal to the reversed simple continued fraction"
]

N_HYP = 2
NEG_Q_INDEX = 2