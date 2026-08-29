import sympy
from sympy import Poly
from sympy.abc import x, y, z
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False, False]
        R, f = witness
    except Exception:
        return [False, False, False, False]

    # H1: R is a commutative ring with identity
    try:
        h1 = False
        if R in (sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            h1 = True
        elif R in (sympy.ZZ, sympy.QQ, sympy.RR, sympy.CC):
            h1 = True
        elif hasattr(R, 'is_Ring') and R.is_Ring and getattr(R, 'is_Commutative', True):
            h1 = True
        elif hasattr(R, 'is_ring') and R.is_ring and getattr(R, 'is_commutative', True):
            h1 = True
    except Exception:
        h1 = False

    # H2: f(x) is monic
    try:
        p = Poly(f)
        if len(p.gens) != 1:
            h2 = False
        else:
            h2 = (p.LC() == 1)
    except Exception:
        h2 = False

    # H3: The degree of f(x) is at least 1
    try:
        p = Poly(f)
        h3 = (p.degree() >= 1)
    except Exception:
        h3 = False

    # neg_Q: The conclusion fails
    try:
        p = Poly(f)
        coeffs = p.coeffs()
        in_r = True
        for c in coeffs:
            c_in_R = False
            if R in (sympy.S.Integers, sympy.ZZ):
                c_in_R = c.is_integer
            elif R in (sympy.S.Rationals, sympy.QQ):
                c_in_R = c.is_rational
            elif R in (sympy.S.Reals, sympy.RR):
                c_in_R = c.is_real
            elif R in (sympy.S.Complexes, sympy.CC):
                c_in_R = c.is_complex
            else:
                try:
                    c_in_R = (c in R)
                except Exception:
                    try:
                        c_in_R = R.contains(c)
                    except Exception:
                        c_in_R = False
            
            if not c_in_R:
                in_r = False
                break
        neg_q = not in_r
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: f is monic",
    "H_3: The degree of f is at least 1",
    "¬Q: The quotient ring is not an integral extension of R"
]

N_HYP = 3
NEG_Q_INDEX = 3