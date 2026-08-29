import sympy
from sympy.polys.domains import Domain, FiniteField

# Top-level setup for witness expressions
ZZ = sympy.ZZ
QQ = sympy.QQ
RR = sympy.RR
CC = sympy.CC

def conditions(witness) -> list[bool]:
    try:
        # H_1: R is commutative
        # In SymPy, Domain objects represent commutative rings.
        # We also accept standard SymPy sets like S.Integers.
        if isinstance(witness, Domain):
            h1 = True
        elif witness in [sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes]:
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        # ¬Q: R is NOT isomorphic to a finite direct product of finite local rings
        # By the Structure Theorem for Finite Commutative Rings, EVERY finite commutative ring
        # is isomorphic to a finite direct product of finite local rings.
        # Thus, for a commutative ring, the conclusion fails if and only if the ring is infinite.
        if isinstance(witness, Domain):
            neg_q = not isinstance(witness, FiniteField)
        elif witness in [sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes]:
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is commutative",
    "¬Q: R is not isomorphic to a finite direct product of finite local rings"
]

N_HYP = 1
NEG_Q_INDEX = 1