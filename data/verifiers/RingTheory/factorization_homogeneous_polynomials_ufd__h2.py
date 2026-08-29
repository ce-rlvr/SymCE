import sympy
from sympy import poly, factor_list
from sympy.abc import x, y, z, t, u, v, w

def conditions(witness):
    try:
        # H_1: R is a unique factorization domain
        # We check if the witness is a valid polynomial over a UFD (like ZZ or QQ)
        p = poly(witness)
        domain = p.domain
        h1 = getattr(domain, 'is_UFD', False)
        if not h1:
            h1 = domain in [sympy.ZZ, sympy.QQ]
        
        # The polynomial must have at least one variable
        if not p.gens:
            h1 = False
            
        # All generators must be valid symbols (not functions like sin(x))
        if not all(isinstance(g, sympy.Symbol) for g in p.gens):
            h1 = False
    except Exception:
        h1 = False

    try:
        # ¬Q: There exists an irreducible factor of f that is not a homogeneous polynomial
        _, factors = factor_list(witness)
        neg_q = False
        for fac, _ in factors:
            if not poly(fac).is_homogeneous:
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "¬Q: There exists an irreducible factor of f that is not a homogeneous polynomial"
]

N_HYP = 1
NEG_Q_INDEX = 1