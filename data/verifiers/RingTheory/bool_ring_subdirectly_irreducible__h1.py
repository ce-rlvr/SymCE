import sympy
from sympy import QQ, ZZ
from sympy.polys.domains import GF
from sympy.ntheory import factorint
from sympy.abc import x, y, z

# Top-level setup for Ring/Field domain
# (Using standard SymPy domains and symbols as requested)

CONDITION_LABELS = [
    "H_1: R is subdirectly irreducible",
    "¬Q: R is not isomorphic to the ring Z/2Z"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    # 1. Check if witness is an integer n (representing the ring Z/nZ)
    try:
        if isinstance(witness, int) or (hasattr(witness, 'is_Integer') and witness.is_Integer):
            n = int(witness)
            if n >= 2:
                # Z/nZ is subdirectly irreducible iff n is a prime power
                factors = factorint(n)
                h1 = (len(factors) == 1)
                # Z/nZ is isomorphic to Z/2Z iff n == 2
                neg_q = (n != 2)
                return [h1, neg_q]
    except Exception:
        pass

    # 2. Check if witness is a string representation like "Z/4Z", "Z_4", or "GF(4)"
    try:
        if isinstance(witness, str):
            w = witness.strip().upper()
            n = None
            if w.startswith("Z/") and w.endswith("Z"):
                n_str = w[2:-1]
                if n_str.isdigit():
                    n = int(n_str)
            elif w.startswith("Z_"):
                n_str = w[2:]
                if n_str.isdigit():
                    n = int(n_str)
            elif w.startswith("GF(") and w.endswith(")"):
                n_str = w[3:-1]
                if n_str.isdigit():
                    n = int(n_str)
            
            if n is not None and n >= 2:
                factors = factorint(n)
                if w.startswith("GF("):
                    # GF(n) exists and is a field (thus subdirectly irreducible) iff n is a prime power
                    if len(factors) == 1:
                        h1 = True
                        neg_q = (n != 2)
                        return [h1, neg_q]
                else:
                    h1 = (len(factors) == 1)
                    neg_q = (n != 2)
                    return [h1, neg_q]
    except Exception:
        pass

    # 3. Check if witness is a SymPy domain (like QQ or GF(p))
    try:
        if hasattr(witness, 'is_Field') and witness.is_Field:
            h1 = True  # All fields are subdirectly irreducible
            try:
                if hasattr(witness, 'order'):
                    order = witness.order
                elif hasattr(witness, 'domain') and hasattr(witness.domain, 'order'):
                    order = witness.domain.order
                else:
                    order = None
                
                if order is not None:
                    neg_q = (order != 2)
                else:
                    neg_q = True  # Infinite fields are not isomorphic to Z/2Z
            except Exception:
                neg_q = True
            return [h1, neg_q]
    except Exception:
        pass

    # 4. Check if witness is the ring of integers ZZ
    try:
        if witness == ZZ:
            # ZZ is not subdirectly irreducible (intersection of all non-zero ideals is (0))
            return [False, True]
    except Exception:
        pass

    return [False, False]