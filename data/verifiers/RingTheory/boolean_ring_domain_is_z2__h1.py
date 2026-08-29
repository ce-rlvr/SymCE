import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.polys.domains import GF

# Standard ring bindings
Z = ZZ
Q = QQ
R = RR
C = CC

Z2 = GF(2)
Z3 = GF(3)
Z4 = 4
Z5 = GF(5)
Z6 = 6

def conditions(witness):
    # H_1: R has a multiplicative identity
    try:
        if isinstance(witness, bool):
            h1 = False
        elif isinstance(witness, (int, sympy.Integer)):
            # Integers n >= 2 represent the ring Z/nZ, which has a multiplicative identity
            h1 = witness >= 2
        elif witness in (sympy.S.Integers, sympy.S.Reals, sympy.S.Rationals, sympy.S.Complexes):
            h1 = True
        else:
            h1 = hasattr(witness, 'one') and hasattr(witness, 'zero')
    except Exception:
        h1 = False

    # H_2: R is an integral domain
    try:
        if isinstance(witness, bool):
            h2 = False
        elif isinstance(witness, (int, sympy.Integer)):
            # Z/nZ is an integral domain iff n is prime
            h2 = sympy.isprime(witness)
        elif witness in (sympy.S.Integers, sympy.S.Reals, sympy.S.Rationals, sympy.S.Complexes):
            h2 = True
        else:
            if witness in (ZZ, QQ, RR, CC):
                h2 = True
            elif hasattr(witness, 'is_Field') and witness.is_Field:
                h2 = True
            elif hasattr(witness, 'is_PID') and witness.is_PID:
                h2 = True
            elif type(witness).__name__ in ('FiniteField', 'IntegerRing', 'RationalField', 'RealField', 'ComplexField', 'AlgebraicField', 'PolynomialRing', 'FractionField'):
                h2 = True
            else:
                h2 = False
    except Exception:
        h2 = False

    # ¬Q: R is not isomorphic to Z/2Z
    try:
        if isinstance(witness, bool):
            neg_q = False
        elif isinstance(witness, (int, sympy.Integer)):
            is_z2 = (witness == 2)
            neg_q = not is_z2
        elif witness in (sympy.S.Integers, sympy.S.Reals, sympy.S.Rationals, sympy.S.Complexes):
            neg_q = True
        else:
            is_z2 = (witness == GF(2))
            if not is_z2 and hasattr(witness, 'order'):
                is_z2 = (witness.order == 2)
            if not is_z2 and hasattr(witness, 'mod') and type(witness).__name__ == 'FiniteField':
                is_z2 = (witness.mod == 2)
            neg_q = not is_z2
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R has a multiplicative identity",
    "H_2: R is an integral domain",
    "¬Q: R is not isomorphic to Z/2Z"
]

N_HYP = 2
NEG_Q_INDEX = 2