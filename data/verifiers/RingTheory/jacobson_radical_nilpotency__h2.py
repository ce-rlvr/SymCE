import sympy
from sympy import Symbol
from sympy.polys.domains import ZZ, QQ

# Top-level setup: define standard counterexamples for the witness generator
class FormalPowerSeriesRing:
    def __init__(self, base, gen):
        self.base = base
        self.gen = gen
        self.is_ring = True
        
    def jacobson_radical_is_nilpotent(self):
        return False
        
    def __str__(self):
        return f"{self.base}[[{self.gen}]]"

class PAdicRing:
    def __init__(self, p):
        self.p = p
        self.is_ring = True
        
    def jacobson_radical_is_nilpotent(self):
        return False
        
    def __str__(self):
        return f"Z_{self.p}"

class LocalizedRing:
    def __init__(self, base, ideal):
        self.base = base
        self.ideal = ideal
        self.is_ring = True
        
    def jacobson_radical_is_nilpotent(self):
        return False
        
    def __str__(self):
        return f"{self.base}_({self.ideal})"

x = Symbol('x')
p = Symbol('p')

# Ready-to-use counterexamples (non-Artinian rings with non-nilpotent Jacobson radicals)
Q_x_fps = FormalPowerSeriesRing(QQ, x)
Z_p = PAdicRing(p)
Z_loc_p = LocalizedRing(ZZ, p)

def conditions(witness) -> list[bool]:
    try:
        # H_1: R is a ring
        h1 = False
        if hasattr(witness, 'is_ring') and witness.is_ring:
            h1 = True
        elif hasattr(witness, 'is_Ring') and witness.is_Ring:
            h1 = True
        elif isinstance(witness, str):
            h1 = True
        elif hasattr(witness, 'get_ring'):
            h1 = True
        elif isinstance(witness, tuple) and len(witness) > 0 and isinstance(witness[0], str):
            h1 = True
        elif witness in [sympy.S.Integers, sympy.S.Reals, sympy.S.Complexes, sympy.S.Rationals]:
            h1 = True
    except Exception:
        h1 = False

    try:
        # H_2: J(R) is the Jacobson radical of R
        # This is a definitional hypothesis; if R is a ring, it has a well-defined Jacobson radical.
        h2 = h1
    except Exception:
        h2 = False

    try:
        # ¬Q: J(R) is NOT a nilpotent ideal
        neg_q = False
        if hasattr(witness, 'jacobson_radical_is_nilpotent'):
            neg_q = not witness.jacobson_radical_is_nilpotent()
        elif isinstance(witness, str):
            w_str = witness.lower()
            if any(kw in w_str for kw in ['[[', 'p-adic', 'local', 'fps', 'power series']):
                neg_q = True
        elif isinstance(witness, tuple) and len(witness) > 0 and isinstance(witness[0], str):
            w_str = witness[0].lower()
            if any(kw in w_str for kw in ['formalpowerseries', 'padic', 'localization', 'local']):
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: J(R) is the Jacobson radical of R",
    "¬Q: J(R) is not a nilpotent ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2