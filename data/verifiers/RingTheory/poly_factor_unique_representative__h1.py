import sympy
from sympy import Poly, ZZ, QQ, RR, CC
from sympy.abc import x, y, z

def conditions(witness):
    """
    Check if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    # H_1: f(x) is a polynomial of degree n >= 1
    try:
        if hasattr(witness, 'is_Poly') and witness.is_Poly:
            f = witness
        else:
            f = Poly(witness)
        h1 = bool(f.degree() >= 1)
    except Exception:
        h1 = False

    # ¬Q: The conclusion fails
    # The conclusion states that every equivalence class in F[x]/<f(x)> contains 
    # exactly one polynomial of degree < n or 0.
    # This is equivalent to saying that polynomial division by f(x) with a unique 
    # remainder of degree < n is always possible.
    # In a general ring, this holds if and only if the leading coefficient of f(x) 
    # is a unit in the coefficient ring.
    # Therefore, the conclusion FAILS (¬Q is True) iff the leading coefficient is NOT a unit.
    try:
        if hasattr(witness, 'is_Poly') and witness.is_Poly:
            f = witness
        else:
            f = Poly(witness)
        
        lc = f.LC()
        domain = f.domain
        
        if hasattr(domain, 'is_unit'):
            neg_q = not bool(domain.is_unit(lc))
        else:
            # Fallback if is_unit is not directly available on the domain
            try:
                domain.exquo(domain.one, lc)
                neg_q = False
            except Exception:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial of degree n >= 1",
    "¬Q: Not every equivalence class contains exactly one polynomial of degree < n or 0"
]

N_HYP = 1
NEG_Q_INDEX = 1