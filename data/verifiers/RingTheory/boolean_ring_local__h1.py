import sympy
from sympy import S
from sympy.polys.domains import ZZ, QQ, RR, CC, GF
from sympy.ntheory import factorint

# Top-level setup: named object bindings that the witness expression may reference.
# For finite rings Z_n, we use integers directly.
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z7 = 7
Z8 = 8
Z9 = 9

def conditions(witness) -> list[bool]:
    # H_1: R is a local ring (contains a unique maximal ideal)
    h1 = False
    try:
        if isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
            if n >= 2:
                # Z_n is a local ring iff n = p^k for some prime p
                h1 = (len(factorint(n)) == 1)
        elif witness in (S.Rationals, S.Reals, S.Complexes, QQ, RR, CC):
            h1 = True  # Fields are local rings
        elif witness in (S.Integers, ZZ):
            h1 = False # Z is not a local ring
        elif hasattr(witness, 'is_Field') and witness.is_Field:
            h1 = True
        elif str(witness).startswith('GF('):
            h1 = True
    except Exception:
        pass

    # ¬Q: R is NOT isomorphic to Z_2
    neg_q = False
    try:
        is_z2 = False
        if isinstance(witness, (int, sympy.Integer)):
            is_z2 = (int(witness) == 2)
        elif witness in (S.Rationals, S.Reals, S.Complexes, QQ, RR, CC, S.Integers, ZZ):
            is_z2 = False
        elif str(witness) == 'GF(2)':
            is_z2 = True
        elif str(witness).startswith('GF('):
            is_z2 = False
        
        neg_q = not is_z2
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a local ring",
    "¬Q: R is not isomorphic to Z_2"
]

N_HYP = 1
NEG_Q_INDEX = 1