import sympy
from sympy import QQ, RR, CC, ZZ
from sympy.polys.domains import GF

def conditions(witness):
    try:
        # The hypothesis implies the witness K is a field.
        h1 = bool(witness.is_Field)
    except Exception:
        h1 = False

    try:
        # Check if K^\times is a divisible group.
        # A group G is divisible if for every g in G and n > 0, there exists h in G such that h^n = g.
        # For fields, K^\times is divisible iff every non-zero element has an n-th root in K for all n.
        # In SymPy's domains, only the ComplexField (CC) and the trivial group GF(2)^\times are divisible.
        is_div = False
        if witness == CC:
            is_div = True
        elif hasattr(witness, 'is_FiniteField') and witness.is_FiniteField:
            if witness.order == 2:
                is_div = True
            else:
                is_div = False
        else:
            # For QQ, RR, AlgebraicField, FractionField, etc., K^\times is not divisible.
            is_div = False
            
        neg_q = not is_div
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K^\\times is the multiplicative group of non-zero elements of K",
    "¬Q: K^\\times is not a divisible group"
]

N_HYP = 1
NEG_Q_INDEX = 1