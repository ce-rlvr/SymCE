import sympy
from sympy import S

# Top-level setup: named object bindings
ZZ = S.Integers

class QuotientModule:
    """Represents the R-module R/(gen)."""
    def __init__(self, ring, ideal_gen):
        self.ring = ring
        self.ideal_gen = ideal_gen

def Z_mod(n):
    """Returns the ZZ-module ZZ/(n)."""
    return QuotientModule(ZZ, sympy.sympify(n))

CONDITION_LABELS = [
    "H_1: M is an R-module",
    "¬Q: M is not a flat R-module"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    try:
        # Extract ring and generator from the witness
        if isinstance(witness, QuotientModule):
            ring = witness.ring
            gen = witness.ideal_gen
        elif isinstance(witness, tuple) and len(witness) == 2:
            ring, gen = witness
        else:
            # Fallback: assume the witness is just the generator for a ZZ-module
            ring = ZZ
            gen = witness
            
        # We primarily support verification for modules over ZZ
        if ring == ZZ:
            gen = sympy.sympify(gen)
            
            # H_1: M is an R-module
            # Any integer n defines a valid ZZ-module ZZ/(n)
            h1 = getattr(gen, 'is_integer', False) is True
            
            # Q: M is a flat R-module
            # Over ZZ, the module ZZ/(n) is flat if and only if it is torsion-free,
            # which occurs exactly when n is 0 (giving ZZ) or +/-1 (giving 0).
            is_flat = (gen in (0, 1, -1))
        else:
            # If an unrecognized ring is provided, we cannot verify the conditions
            h1 = False
            is_flat = True
            
        return [bool(h1), not bool(is_flat)]
    except Exception:
        return [False, False]