import sympy
from sympy import divisor_sigma

CONDITION_LABELS = [
    "H_1: k is a non-negative integer and m is an odd positive integer such that n = 2^k m",
    "¬Q: \\sigma(n) != (2^{k+1}-1)\\sigma(m)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            k = witness.get('k')
            m = witness.get('m')
        elif isinstance(witness, (int, sympy.Integer)):
            n = witness
            k = 0
            m = n
            if m > 0:
                while m % 2 == 0:
                    k += 1
                    m //= 2
        else:
            n, k, m = witness
    except Exception:
        return [False, False]
        
    try:
        if not (int(k) == k and int(m) == m and int(n) == n):
            h1 = False
        else:
            k_int = int(k)
            m_int = int(m)
            n_int = int(n)
            h1 = bool(k_int >= 0 and m_int > 0 and m_int % 2 != 0 and n_int == (2**k_int) * m_int)
    except Exception:
        h1 = False
        
    try:
        k_int = int(k)
        m_int = int(m)
        n_int = int(n)
        lhs = divisor_sigma(n_int)
        rhs = (2**(k_int+1) - 1) * divisor_sigma(m_int)
        neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]