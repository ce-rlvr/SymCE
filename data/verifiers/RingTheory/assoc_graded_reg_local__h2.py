import sympy
from sympy import symbols
from sympy.abc import x, y, z

ZZ = sympy.ZZ
QQ = sympy.QQ

CONDITION_LABELS = [
    "H_1: R is a regular local ring with maximal ideal m and Krull dimension d",
    "¬Q: The associated graded ring gr_m(R) is not isomorphic to the polynomial ring in d variables over k"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("is_regular_local_ring", False))
            q = bool(witness.get("gr_m_isomorphic_to_polynomial_ring", True))
            neg_q = not q
        else:
            h1_val = getattr(witness, "is_regular_local_ring", False)
            if callable(h1_val):
                h1_val = h1_val()
            h1 = bool(h1_val)
            
            q_val = getattr(witness, "gr_m_isomorphic_to_polynomial_ring", True)
            if callable(q_val):
                q_val = q_val()
            neg_q = not bool(q_val)
    except Exception:
        pass

    return [h1, neg_q]