import sympy
from sympy import Poly, Symbol
from sympy.abc import x

QQ = sympy.QQ

def conditions(witness):
    p = None
    try:
        if isinstance(witness, Poly):
            p = witness
        else:
            p = Poly(witness, x, domain='QQ')
            
        h1 = p.domain.is_Field
    except Exception:
        h1 = False

    try:
        h2 = p.degree() >= 1 if p is not None else False
    except Exception:
        h2 = False

    try:
        # The conclusion states that the Galois group acts transitively on the roots 
        # and is isomorphic to a transitive subgroup of S_n.
        # For a polynomial over a perfect field (like QQ), this is true if and only if 
        # the polynomial is irreducible.
        # Therefore, the conclusion fails (neg_q is True) iff the polynomial is reducible.
        neg_q = not p.is_irreducible if p is not None else False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: E is the splitting field of f(x) over F (f is a non-constant polynomial)",
    "¬Q: The Galois group Gal(E/F) does not act transitively on the roots of f(x) or is not a transitive subgroup of S_n"
]

N_HYP = 2
NEG_Q_INDEX = 2