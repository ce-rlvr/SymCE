import sympy
from sympy import ZZ, QQ
from sympy.polys.domains import Domain
from sympy.abc import x, y, z

def conditions(witness):
    try:
        R, I = witness
    except Exception:
        return [False, False]
    
    # H_1: R is a Noetherian integral domain
    try:
        # In SymPy, Domain objects represent integral domains (or fields).
        # Standard domains like ZZ, QQ, and their polynomial rings are Noetherian.
        h1 = isinstance(R, Domain)
    except Exception:
        h1 = False

    # ¬Q: The intersection \bigcap_{n=1}^{\infty} I^n is not the zero ideal
    # By Krull's Intersection Theorem, in a Noetherian domain, the intersection 
    # of I^n is the zero ideal for any proper ideal I.
    # Thus, the intersection is NOT the zero ideal if and only if I is NOT a proper ideal,
    # which means I generates the whole ring R (i.e., 1 is in I).
    try:
        if not I:
            neg_q = False
        else:
            g = I[0]
            for elem in I[1:]:
                g = R.gcd(g, elem)
            
            neg_q = False
            if getattr(R, 'is_Field', False) and g != R.zero:
                neg_q = True
            else:
                try:
                    if R.is_unit(g):
                        neg_q = True
                except Exception:
                    try:
                        R.exquo(R.one, g)
                        neg_q = True
                    except Exception:
                        if g == R.one or g == -R.one:
                            neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Noetherian integral domain",
    "¬Q: The intersection of I^n is not the zero ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1