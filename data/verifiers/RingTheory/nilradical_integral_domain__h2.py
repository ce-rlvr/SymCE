import sympy
from sympy.ntheory import factorint
from sympy.polys.domains.ring import Ring

# Top-level setup
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        # Treat integers n >= 2 as the ring Z/nZ.
        # Treat n = 0 as the ring Z.
        if isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
            if n == 0 or n >= 2:
                h1 = True
                if n == 0:
                    # The nilradical of Z is the zero ideal
                    neg_q = False
                else:
                    # The nilradical of Z/nZ is the zero ideal iff n is square-free.
                    # Thus, the nilradical is NOT the zero ideal iff n is NOT square-free.
                    factors = factorint(n)
                    is_sq_free = all(v == 1 for v in factors.values())
                    neg_q = not is_sq_free
                return [h1, neg_q]
    except Exception:
        pass

    try:
        # SymPy domains (like ZZ, QQ) are rings.
        if isinstance(witness, Ring):
            h1 = True
            # Standard SymPy domains (ZZ, QQ, RR, CC, and their polynomial rings)
            # are integral domains or fields, so their nilradical is the zero ideal.
            neg_q = False
            return [h1, neg_q]
    except Exception:
        pass

    return [False, False]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "¬Q: The nilradical of R is not the zero ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1