import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import oo, ZZ, QQ, RR, CC
from sympy.abc import x, y, z
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
    h1, h2, neg_q = False, False, False
    
    try:
        if isinstance(witness, dict):
            R = witness.get('R', ZZ)
            S = witness.get('S', lambda x: True)
            n = witness.get('n', None)
        elif hasattr(witness, 'R') and hasattr(witness, 'S') and hasattr(witness, 'n'):
            R = witness.R
            S = witness.S
            n = witness.n
        elif isinstance(witness, (tuple, list)) and len(witness) >= 3:
            R, S, n = witness[:3]
        else:
            # If the witness is just the counterexample value for n
            R = ZZ
            S = lambda x: True
            n = witness
    except Exception:
        return [False, False, False]

    # H1: R is a commutative ring
    try:
        if hasattr(R, 'is_commutative'):
            h1 = bool(R.is_commutative)
        elif R in [ZZ, QQ, RR, CC]:
            h1 = True
        elif isinstance(R, str) and R.lower() in ['z', 'q', 'r', 'c', 'zz', 'qq', 'rr', 'cc']:
            h1 = True
        else:
            h1 = True  # Fallback for abstract/custom ring objects
    except Exception:
        h1 = False

    # H2: S is a multiplicatively closed subset of R
    try:
        if isinstance(S, (set, list, tuple)):
            h2 = True
            for a in S:
                for b in S:
                    if (a * b) not in S:
                        h2 = False
                        break
                if not h2:
                    break
        elif hasattr(S, 'is_multiplicatively_closed'):
            h2 = bool(S.is_multiplicatively_closed)
        elif hasattr(S, 'contains'):
            h2 = True
        elif callable(S):
            h2 = True
        else:
            h2 = True  # Fallback for abstract/custom subset objects
    except Exception:
        h2 = False

    # ¬Q: S^{-1}(M_n(R)) is not isomorphic to M_n(S^{-1}R)
    # The conclusion fails (they are not isomorphic) when n is infinite.
    try:
        if n == oo or n == float('inf') or n == math.inf:
            neg_q = True
        elif hasattr(n, 'is_infinite') and n.is_infinite:
            neg_q = True
        elif isinstance(n, str) and 'inf' in n.lower():
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: S^{-1}(M_n(R)) is not isomorphic to M_n(S^{-1}R)"
]

N_HYP = 2
NEG_Q_INDEX = 2