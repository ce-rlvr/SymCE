import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup
from sympy.matrices import eye, zeros
from sympy import ZZ, QQ, RR, CC

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            H = witness.get('H')
        else:
            R, H = witness
    except Exception:
        return [False, False]

    try:
        if R is None:
            h1_ok = False
        elif R in (ZZ, QQ, RR, CC):
            h1_ok = True
        elif isinstance(R, sympy.Symbol) and R.is_commutative:
            h1_ok = True
        elif isinstance(R, type) and R in (int, float, complex):
            h1_ok = True
        else:
            from sympy.polys.domains import Domain
            if isinstance(R, Domain) and getattr(R, 'is_commutative', False):
                h1_ok = True
            else:
                h1_ok = False
    except Exception:
        h1_ok = False

    try:
        if isinstance(H, PermutationGroup):
            neg_q_ok = not bool(H.is_solvable)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: H is not solvable"
]

N_HYP = 1
NEG_Q_INDEX = 1