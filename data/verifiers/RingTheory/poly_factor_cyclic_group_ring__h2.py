import sympy
from sympy import oo, eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: C_n is the cyclic group of order n",
    "~Q: Group ring is not isomorphic to the factor ring"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    # Parse witness
    if isinstance(witness, tuple) and len(witness) == 2:
        R, n = witness
    else:
        R = sympy.ZZ
        n = witness

    # If n is a group object, extract its order
    if hasattr(n, 'order'):
        try:
            if callable(n.order):
                n = n.order()
            else:
                n = n.order
        except Exception:
            pass

    # H_1: R is a commutative ring with identity
    try:
        h1 = False
        if R in [sympy.ZZ, sympy.QQ, sympy.RR, sympy.CC]:
            h1 = True
        elif hasattr(R, 'is_commutative') and R.is_commutative:
            h1 = True
        elif type(R).__name__ in ['Ring', 'Field', 'IntegerRing', 'RationalField', 'RealField', 'ComplexField']:
            h1 = True
    except Exception:
        h1 = False

    # H_2: C_n is the cyclic group of order n
    try:
        h2 = False
        if n == oo:
            h2 = True
        else:
            n_val = int(n)
            if n_val >= 0:
                h2 = True
    except Exception:
        h2 = False

    # ~Q: R[C_n] is not isomorphic to R[x]/<x^n - 1>
    # The isomorphism holds for any finite n >= 1.
    # It fails if n is infinite (oo) or 0 (which represents the infinite cyclic group in some conventions),
    # because the group ring of the infinite cyclic group is R[x, x^-1], not R[x]/<0> = R[x].
    try:
        neg_q = False
        if n == oo:
            neg_q = True
        else:
            n_val = int(n)
            if n_val == 0:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]