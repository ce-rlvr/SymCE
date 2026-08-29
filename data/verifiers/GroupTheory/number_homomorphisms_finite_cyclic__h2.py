import math
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    # H_1: Let n and m be positive integers
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            m = witness.get('m')
        else:
            n, m = witness
            
        if hasattr(n, 'is_integer') and n.is_integer:
            n = int(n)
        if hasattr(m, 'is_integer') and m.is_integer:
            m = int(m)
            
        h1 = isinstance(n, int) and isinstance(m, int) and not isinstance(n, bool) and not isinstance(m, bool) and n > 0 and m > 0
    except Exception:
        h1 = False

    # ¬Q: The number of distinct group homomorphisms from Z_n to Z_m is NOT exactly gcd(n, m)
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            m = witness.get('m')
        else:
            n, m = witness
            
        n = int(n)
        m = int(m)
        
        # A group homomorphism f: Z_n -> Z_m is uniquely determined by f(1) = k,
        # where 0 <= k < m. The order of f(1) must divide the order of 1 in Z_n,
        # which means n * k == 0 (mod m).
        count = 0
        for k in range(m):
            if (n * k) % m == 0:
                count += 1
                
        neg_q = count != math.gcd(n, m)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n and m are positive integers",
    "¬Q: The number of distinct group homomorphisms from Z_n to Z_m is not exactly gcd(n, m)"
]

N_HYP = 1
NEG_Q_INDEX = 1