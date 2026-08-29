import math
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: gcd(m, n) == 1",
    "¬Q: Z_m x Z_n is not isomorphic to Z_{mn}"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            m = witness.get('m')
            n = witness.get('n')
            if m is None or n is None:
                return [False, False]
        else:
            m, n = witness
    except Exception:
        return [False, False]
        
    # H_1: Assume the greatest common divisor of m and n is 1
    try:
        m_val = int(m)
        n_val = int(n)
        if m_val != m or n_val != n:
            h1 = False
        else:
            h1 = (math.gcd(m_val, n_val) == 1)
    except Exception:
        h1 = False
        
    # ¬Q: The direct product of cyclic groups Z_m x Z_n is NOT isomorphic to the cyclic group Z_{mn}
    try:
        m_val = int(m)
        n_val = int(n)
        if m_val != m or n_val != n:
            q = False
        elif m_val <= 0 or n_val <= 0:
            # Z_m is undefined for m <= 0 in the standard context of finite cyclic groups,
            # making the conclusion statement false (or meaningless).
            q = False
        else:
            # For positive integers, Z_m x Z_n is isomorphic to Z_{mn} iff gcd(m, n) == 1
            q = (math.gcd(m_val, n_val) == 1)
        neg_q = not q
    except Exception:
        neg_q = True
        
    return [h1, neg_q]