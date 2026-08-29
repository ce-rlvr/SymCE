import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z
from sympy.ntheory import factorint

# Top-level setup
# Standard rings and symbols are available.
# We assume the witness represents an ideal in Z, given as an integer n,
# or a tuple like (ZZ, n), or a sympy Ideal object.

def extract_n(witness):
    def get_int(obj):
        if isinstance(obj, int):
            return obj
        if hasattr(obj, 'is_Integer') and obj.is_Integer:
            return int(obj)
        if hasattr(obj, 'gens'):
            gens = obj.gens
            if len(gens) == 1:
                if isinstance(gens[0], int):
                    return gens[0]
                if hasattr(gens[0], 'is_Integer') and gens[0].is_Integer:
                    return int(gens[0])
        return None

    val = get_int(witness)
    if val is not None:
        return val
        
    if isinstance(witness, dict):
        if 'I' in witness:
            val = get_int(witness['I'])
            if val is not None:
                return val
        for v in witness.values():
            val = get_int(v)
            if val is not None:
                return val

    if isinstance(witness, (list, tuple)):
        for item in reversed(witness):
            val = get_int(item)
            if val is not None:
                return val
            if isinstance(item, (list, tuple)) and len(item) == 1:
                val = get_int(item[0])
                if val is not None:
                    return val

    raise ValueError("Cannot extract integer from witness")

def conditions(witness) -> list[bool]:
    try:
        n = extract_n(witness)
    except Exception:
        return [False, False]
        
    try:
        # H1: I is a proper ideal of R
        # Assuming R = Z, I = nZ is proper iff abs(n) != 1
        h1 = (abs(n) != 1)
    except Exception:
        h1 = False
        
    try:
        # neg_Q: R/I is NOT a valuation ring
        # Z/nZ is a valuation ring iff n is a prime power (for n > 1)
        # For n = 0, Z/0Z = Z, which is not a valuation ring (e.g., 2 and 3 don't divide each other).
        if n == 0:
            is_val_ring = False
        else:
            factors = factorint(abs(n))
            is_val_ring = (len(factors) == 1)
            
        neg_q = not is_val_ring
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: I is a proper ideal of R",
    "¬Q: R/I is not a valuation ring"
]

N_HYP = 1
NEG_Q_INDEX = 1