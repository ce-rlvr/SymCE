import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math

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
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_noetherian', False))
        else:
            h1 = bool(getattr(witness, 'is_noetherian', False))
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            h2 = bool(witness.get('is_local', False))
        else:
            h2 = bool(getattr(witness, 'is_local', False))
    except Exception:
        h2 = False

    try:
        if isinstance(witness, dict):
            if 'krull_dimension' in witness:
                dim = witness['krull_dimension']
                q = (dim != math.inf and dim != float('inf') and str(dim).lower() not in ['inf', 'infinity'])
            else:
                q = bool(witness.get('has_finite_krull_dimension', True))
        else:
            if hasattr(witness, 'krull_dimension'):
                dim = getattr(witness, 'krull_dimension')
                q = (dim != math.inf and dim != float('inf') and str(dim).lower() not in ['inf', 'infinity'])
            else:
                q = bool(getattr(witness, 'has_finite_krull_dimension', True))
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is Noetherian",
    "H_2: R is a local ring with a unique maximal ideal",
    "¬Q: The Krull dimension of R is infinite"
]

N_HYP = 2
NEG_Q_INDEX = 2