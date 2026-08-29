import sympy
from sympy import QQ, ZZ, RR, CC
from sympy.abc import x
from sympy.polys.domains.domain import Domain

def conditions(witness):
    try:
        if not isinstance(witness, Domain):
            h1_ok = False
        else:
            is_euclid = False
            if witness.is_Field:
                is_euclid = True
            elif witness == ZZ:
                is_euclid = True
            elif hasattr(witness, 'domain') and hasattr(witness, 'symbols'):
                if witness.domain.is_Field and len(witness.symbols) == 1:
                    is_euclid = True
            elif witness.__class__.__name__ == 'GaussianIntegerRing':
                is_euclid = True
            h1_ok = is_euclid
    except Exception:
        h1_ok = False

    try:
        if not isinstance(witness, Domain):
            neg_q_ok = False
        else:
            is_dim_1 = False
            if witness.is_Field:
                is_dim_1 = False
            elif witness == ZZ:
                is_dim_1 = True
            elif hasattr(witness, 'domain') and hasattr(witness, 'symbols'):
                if witness.domain.is_Field and len(witness.symbols) == 1:
                    is_dim_1 = True
            elif witness.__class__.__name__ == 'GaussianIntegerRing':
                is_dim_1 = True
            neg_q_ok = not is_dim_1
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "¬Q: The global homological dimension of R is not exactly 1"
]

N_HYP = 1
NEG_Q_INDEX = 1