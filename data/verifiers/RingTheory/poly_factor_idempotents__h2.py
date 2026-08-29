import sympy
from sympy import Poly, QQ, ZZ, GF, RR, CC
from sympy.abc import x

# Top-level setup
F2 = GF(2)
F3 = GF(3)
F5 = GF(5)
F7 = GF(7)

def conditions(witness) -> list[bool]:
    try:
        F, f, k = witness
    except Exception:
        return [False, False, False]
        
    # H_1: F is a field
    try:
        h1_ok = bool(F.is_Field)
    except Exception:
        h1_ok = False
        
    # H_2: f has exactly k distinct monic irreducible factors over F
    try:
        p = Poly(f, x, domain=F)
        if p.is_zero:
            num_factors = 0
        else:
            _, factors = p.factor_list()
            num_factors = len(factors)
        h2_ok = bool(num_factors == k)
    except Exception:
        h2_ok = False
        
    # ¬Q: The factor ring modulo f does not contain exactly 2^k idempotent elements
    try:
        p = Poly(f, x, domain=F)
        if p.is_zero:
            num_idempotents = 2
        elif p.degree() == 0:
            num_idempotents = 1
        else:
            _, factors = p.factor_list()
            num_idempotents = 2 ** len(factors)
            
        neg_q_ok = bool(num_idempotents != 2**k)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f has exactly k distinct monic irreducible factors over F",
    "¬Q: The factor ring modulo f does not contain exactly 2^k idempotent elements"
]

N_HYP = 2
NEG_Q_INDEX = 2