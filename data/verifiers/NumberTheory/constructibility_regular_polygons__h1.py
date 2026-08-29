import sympy
from sympy.ntheory import totient, factorint

def conditions(witness) -> list[bool]:
    try:
        n = int(witness)
    except Exception:
        return [False]
    
    try:
        if n < 3:
            constructible = False
        else:
            factors = factorint(n)
            constructible = True
            for p, e in factors.items():
                if p == 2:
                    continue
                if e > 1:
                    constructible = False
                    break
                if (p - 1) & (p - 2) != 0:
                    constructible = False
                    break
    except Exception:
        constructible = False

    try:
        phi = int(totient(n))
        if phi <= 0:
            phi_is_pow2 = False
        else:
            phi_is_pow2 = (phi & (phi - 1)) == 0
    except Exception:
        phi_is_pow2 = False

    try:
        neg_q = bool(constructible != phi_is_pow2)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: Constructibility of regular n-gon is not equivalent to phi(n) being a power of 2"
]

N_HYP = 0
NEG_Q_INDEX = 0