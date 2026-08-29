import math
import sympy
from sympy.ntheory import n_order

# Top-level setup
# (No named bindings needed for this number theory domain; use integers directly)

def get_lcm(a, b):
    if a == 0 and b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            m = witness.get('m')
            d = witness.get('d')
        else:
            a, m, d = witness
    except Exception:
        return [False, False, False]

    # H1: m_1, ..., m_k are pairwise coprime positive integers
    try:
        h1 = True
        if not isinstance(m, (list, tuple)) or len(m) == 0:
            h1 = False
        else:
            for i in range(len(m)):
                if not (isinstance(m[i], int) or isinstance(m[i], sympy.Integer)) or m[i] <= 0:
                    h1 = False
                    break
                for j in range(i + 1, len(m)):
                    if math.gcd(int(m[i]), int(m[j])) != 1:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # H2: a is an integer such that gcd(a, m_i) = 1 for all i
    try:
        h2 = True
        if not (isinstance(a, int) or isinstance(a, sympy.Integer)):
            h2 = False
        elif not isinstance(m, (list, tuple)) or len(m) == 0:
            h2 = False
        else:
            for mi in m:
                if not (isinstance(mi, int) or isinstance(mi, sympy.Integer)) or math.gcd(int(a), int(mi)) != 1:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # neg_Q: The multiplicative order of a modulo prod(m_i) is NOT equal to lcm(d_1, ..., d_k)
    try:
        neg_q = False
        if isinstance(d, (list, tuple)) and len(d) == len(m):
            prod_m = 1
            for mi in m:
                prod_m *= int(mi)
            
            if prod_m == 1:
                order_a = 1
            else:
                order_a = n_order(int(a), prod_m)
                
            lcm_d = 1
            for di in d:
                if not (isinstance(di, int) or isinstance(di, sympy.Integer)):
                    raise ValueError
                lcm_d = get_lcm(lcm_d, int(di))
                
            if order_a != lcm_d:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: m_1, m_2, ..., m_k are pairwise coprime positive integers",
    "H_2: a is an integer such that gcd(a, m_i) = 1 for all 1 <= i <= k",
    "¬Q: The multiplicative order of a modulo prod(m_i) is not equal to lcm(d_1, ..., d_k)"
]

N_HYP = 2
NEG_Q_INDEX = 2