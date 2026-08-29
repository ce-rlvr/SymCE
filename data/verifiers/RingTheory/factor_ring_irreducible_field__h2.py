import sympy
from sympy import Poly, Symbol, QQ, ZZ, GF
from sympy.abc import x

# Top-level setup
Q = QQ
Z = ZZ

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, Poly):
            p = witness
        elif isinstance(witness, tuple):
            if hasattr(witness[0], 'is_Field'):
                dom = witness[0]
                expr = witness[1]
                gens = witness[2:]
            else:
                expr = witness[0]
                dom = witness[1]
                gens = witness[2:]
            
            if not gens:
                free = getattr(expr, 'free_symbols', set())
                gens = sorted(list(free), key=lambda s: s.name) if free else [Symbol('x')]
            p = Poly(expr, *gens, domain=dom)
        else:
            p = Poly(witness, Symbol('x'))
    except Exception:
        return [False, False]

    try:
        h1 = bool(p.domain.is_Field)
    except Exception:
        h1 = False

    try:
        if p.is_multivariate:
            is_factor_ring_field = False
        else:
            is_factor_ring_field = bool(p.domain.is_Field and p.degree() >= 1 and p.is_irreducible == True)
            
        is_p_irreducible = (p.is_irreducible == True)
        
        conclusion = (is_factor_ring_field == is_p_irreducible)
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "not Q: factor ring is a field XOR p is irreducible"
]

N_HYP = 1
NEG_Q_INDEX = 1