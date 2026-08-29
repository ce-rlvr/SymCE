import sympy
from sympy.ntheory import factorint

class IntegerModRing:
    def __init__(self, n):
        self.n = n
        
    def __str__(self):
        return f"Z/{self.n}Z"

class UpperTriangularMatrixRing:
    def __init__(self, n, field_name="R"):
        self.n = n
        self.field_name = field_name
        
    def __str__(self):
        return f"UpperTriangularMatrices({self.n}, {self.field_name})"

# Standard counterexamples and examples
Z2 = IntegerModRing(2)
Z3 = IntegerModRing(3)
Z4 = IntegerModRing(4)
Z5 = IntegerModRing(5)
Z6 = IntegerModRing(6)
Z8 = IntegerModRing(8)
Z9 = IntegerModRing(9)

T2_R = UpperTriangularMatrixRing(2, "R")
T3_R = UpperTriangularMatrixRing(3, "R")

def conditions(witness) -> list[bool]:
    # H_1: R is a ring
    try:
        if isinstance(witness, (IntegerModRing, UpperTriangularMatrixRing)):
            h1 = True
        elif hasattr(witness, 'is_ring'):
            h1 = bool(witness.is_ring)
        elif witness in (sympy.ZZ, sympy.QQ, sympy.RR, sympy.CC, sympy.S.Integers, sympy.S.Reals, sympy.S.Complexes, sympy.S.Rationals):
            h1 = True
        elif type(witness).__name__ == 'FiniteField':
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: R is a left Artinian ring
    try:
        if isinstance(witness, (IntegerModRing, UpperTriangularMatrixRing)):
            h2 = True
        elif hasattr(witness, 'is_artinian'):
            h2 = bool(witness.is_artinian)
        elif witness in (sympy.QQ, sympy.RR, sympy.CC, sympy.S.Reals, sympy.S.Complexes, sympy.S.Rationals):
            h2 = True
        elif witness in (sympy.ZZ, sympy.S.Integers):
            h2 = False
        elif type(witness).__name__ == 'FiniteField':
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: R is NOT isomorphic to a finite direct product of matrix rings over division rings
    try:
        if isinstance(witness, IntegerModRing):
            # By Chinese Remainder Theorem, Z/nZ is a product of fields iff n is square-free
            factors = factorint(witness.n)
            is_prod = all(v == 1 for v in factors.values())
        elif isinstance(witness, UpperTriangularMatrixRing):
            # Upper triangular matrices form a semisimple ring iff n = 1
            is_prod = (witness.n == 1)
        elif hasattr(witness, 'is_semisimple'):
            is_prod = bool(witness.is_semisimple)
        elif witness in (sympy.QQ, sympy.RR, sympy.CC, sympy.S.Reals, sympy.S.Complexes, sympy.S.Rationals):
            is_prod = True
        elif witness in (sympy.ZZ, sympy.S.Integers):
            is_prod = False
        elif type(witness).__name__ == 'FiniteField':
            is_prod = True
        else:
            is_prod = True # Default to True so neg_Q is False if we don't know
            
        neg_q = not is_prod
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: R is a left Artinian ring",
    "¬Q: R is not isomorphic to a finite direct product of matrix rings over division rings"
]

N_HYP = 2
NEG_Q_INDEX = 2