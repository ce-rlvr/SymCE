import sympy
from sympy import cyclotomic_poly, Symbol, factor_list
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: L over K is a finite Galois extension",
    "H_2: The degree of L over K is an odd integer",
    "H_3: K does not contain a primitive 2^n-th root of unity",
    "not Q: The field L DOES contain a primitive 2^n-th root of unity"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get('is_galois', False))
            h2 = bool(witness.get('degree_odd', False))
            h3 = not bool(witness.get('K_has_root', True))
            neg_q = bool(witness.get('L_has_root', False))
            return [h1, h2, h3, neg_q]
        except Exception:
            pass

    if isinstance(witness, (tuple, list)) and len(witness) == 4:
        try:
            p, d_K, d_L, n = witness
            p = int(p)
            d_K = int(d_K)
            d_L = int(d_L)
            n = int(n)
            
            if n < 0 or d_K <= 0 or d_L <= 0:
                return [False, False, False, False]
                
            h1 = (d_L % d_K == 0)
            h2 = ((d_L // d_K) % 2 == 1)
            
            m = 2**n
            h3 = ((p**d_K - 1) % m != 0)
            neg_q = ((p**d_L - 1) % m == 0)
            
            return [h1, h2, h3, neg_q]
        except Exception:
            pass

    try:
        h1 = bool(witness.is_galois())
        h2 = bool(witness.degree() % 2 == 1)
        h3 = not bool(witness.K_has_root())
        neg_q = bool(witness.L_has_root())
        return [h1, h2, h3, neg_q]
    except Exception:
        pass

    return [False, False, False, False]