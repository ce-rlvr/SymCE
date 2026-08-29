import sympy
from sympy.ntheory import factorint
from sympy.abc import x
from sympy.matrices import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, f = witness
        else:
            R = witness
            f = None

        if isinstance(R, int):
            h1_ok = True
        elif hasattr(R, 'is_commutative'):
            h1_ok = bool(R.is_commutative)
        else:
            h1_ok = True

        neg_q_ok = False
        if isinstance(R, int) and f is not None:
            n = R
            if n > 1:
                rad_n = 1
                for p in factorint(n).keys():
                    rad_n *= p
                
                c_in_N = all(c % rad_n == 0 for c in f)
                f_in_J = all(c % rad_n == 0 for c in f)
                neg_q_ok = not (f_in_J == c_in_N)

        return [h1_ok, neg_q_ok]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: f in Jacobson radical of polynomial ring iff content ideal is in nilradical fails"
]

N_HYP = 1
NEG_Q_INDEX = 1