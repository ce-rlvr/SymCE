import sympy
from sympy import ZZ, QQ
from sympy.abc import x

# Top-level setup
class CommutativeRing:
    def __init__(self, name, S_is_nzd, total_frac_iso):
        self.name = name
        self.S_is_nzd = bool(S_is_nzd)
        self.total_frac_iso = bool(total_frac_iso)

Z = CommutativeRing("Z", True, False)
Q = CommutativeRing("Q", True, True)
Z6 = CommutativeRing("Z6", True, True)
Z_x = CommutativeRing("Z[x]", True, False)
Q_x = CommutativeRing("Q[x]", True, False)

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, CommutativeRing):
            h1 = witness.S_is_nzd
            neg_q = not witness.total_frac_iso
        elif witness is sympy.S.Integers:
            h1 = True
            neg_q = True
        elif witness in (sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            h1 = True
            neg_q = False
        elif hasattr(witness, 'is_Field'):
            # SymPy domain (e.g., ZZ, QQ)
            h1 = True
            neg_q = not witness.is_Field
        elif isinstance(witness, str):
            w = witness.lower()
            if w in ['z', 'zz', 'integers', 'z[x]', 'q[x]', 'z_x', 'q_x']:
                h1 = True
                neg_q = True
            elif w in ['q', 'qq', 'rationals', 'z6']:
                h1 = True
                neg_q = False
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: S is the set of all non-zero-divisors of R",
    "¬Q: The localization S^{-1}R (the total ring of fractions) is not isomorphic to R"
]

N_HYP = 1
NEG_Q_INDEX = 1