import sympy
from sympy.polys.domains import ZZ, QQ, RR, CC

# Define some common finite fields which are also rings
Z2 = sympy.GF(2)
Z3 = sympy.GF(3)
Z5 = sympy.GF(5)

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "¬Q: Spec(R) is not a compact Hausdorff space"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    # H_1: R is a commutative ring with identity
    try:
        from sympy.polys.domains import Domain
        is_domain = isinstance(witness, Domain)
        is_set = witness in [sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes]
        h1 = is_domain or is_set
    except Exception:
        h1 = False

    # ¬Q: Spec(R) is not a compact Hausdorff space
    # Spec(R) is compact Hausdorff iff the Krull dimension of R is 0.
    # For standard SymPy domains:
    # - Fields (QQ, RR, CC, GF(p)) have Krull dimension 0 -> Spec(R) is compact Hausdorff.
    # - ZZ has Krull dimension 1 -> Spec(R) is not Hausdorff.
    # - Polynomial rings over fields have Krull dimension >= 1 -> Spec(R) is not Hausdorff.
    try:
        if getattr(witness, 'is_Field', False):
            is_ch = True
        elif witness in [sympy.ZZ, sympy.S.Integers]:
            is_ch = False
        elif witness in [sympy.QQ, sympy.S.Rationals, sympy.RR, sympy.S.Reals, sympy.CC, sympy.S.Complexes]:
            is_ch = True
        elif type(witness).__name__ == 'PolynomialRing':
            is_ch = False
        else:
            # Default for other infinite domains like ZZ[x] which have Krull dim > 0
            is_ch = False
            
        neg_q = not is_ch
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]