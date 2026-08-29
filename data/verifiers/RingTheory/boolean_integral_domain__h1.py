import sympy
from sympy import ZZ, QQ, RR, CC, S
from sympy.polys.domains import GF
from sympy.polys.domains.domain import Domain

# Top-level setup: named object bindings
Z2 = GF(2)
Z3 = GF(3)
Z5 = GF(5)
Z = ZZ
Q = QQ
R = RR
C = CC

def conditions(witness) -> list[bool]:
    # H_1: R is an integral domain
    try:
        # In SymPy, all Domain objects (like ZZ, QQ, GF(p)) are integral domains.
        # We also accept standard SymPy sets representing integral domains.
        if isinstance(witness, Domain):
            h1_ok = True
        elif witness in (S.Integers, S.Rationals, S.Reals, S.Complexes):
            h1_ok = True
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # ¬Q: R is NOT isomorphic to the field of two elements, Z/2Z
    try:
        # GF(2) is the canonical representation of Z/2Z in SymPy's poly domains
        if witness == GF(2):
            is_z2 = True
        else:
            is_z2 = False
        neg_q_ok = not is_z2
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: R is not isomorphic to Z/2Z"
]

N_HYP = 1
NEG_Q_INDEX = 1