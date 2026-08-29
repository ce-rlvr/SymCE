import sympy
from sympy import symbols
from sympy.polys.domains import ZZ, QQ, RR, CC, GF

Z2 = GF(2)
Z3 = GF(3)
Z5 = GF(5)
Z7 = GF(7)

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    def check_ring(R):
        if isinstance(R, str):
            return R in ["ZZ", "QQ", "RR", "CC", "Z2", "Z3", "Z5", "Z7", "Z", "Q", "R", "C"]
        if isinstance(R, sympy.Symbol):
            return False
        if R in [ZZ, QQ, RR, CC, Z2, Z3, Z5, Z7]:
            return True
        if R in [sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes]:
            return True
        if hasattr(R, 'is_Ring') and R.is_Ring:
            return True
        if hasattr(R, 'is_commutative') and R.is_commutative:
            return True
        return False

    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, n = witness
            h1 = check_ring(R)
            if isinstance(n, int) and n >= 0:
                h2 = True
        elif hasattr(witness, 'domain') and hasattr(witness, 'gens'):
            R = witness.domain
            h1 = check_ring(R)
            h2 = True
        else:
            R = witness
            h1 = check_ring(R)
            h2 = h1
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: Polynomial ring in n variables over R",
    "¬Q: The factor ring modulo the variables is not isomorphic to R"
]

N_HYP = 2
NEG_Q_INDEX = 2