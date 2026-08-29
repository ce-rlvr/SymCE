import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to provide the free group F and the integer n,
    e.g., as a tuple (F, n) or a dictionary {'F': F, 'n': n}.
    """
    F, n = None, None
    try:
        if isinstance(witness, dict):
            F = witness.get('F', witness.get('G'))
            n = witness.get('n')
        elif isinstance(witness, tuple):
            F = witness[0]
            if len(witness) >= 2:
                n = witness[-1]
        else:
            F = witness
    except Exception:
        pass

    # H_1: F is a free group on a set S
    try:
        is_free = type(F).__name__ == 'FreeGroup'
        is_fp_free = type(F).__name__ == 'FpGroup' and len(getattr(F, 'relators', [])) == 0
        h1 = is_free or is_fp_free
    except Exception:
        h1 = False

    # H_2: F' is the commutator subgroup of F
    # This is a definitional hypothesis that holds as long as F is a valid group.
    try:
        h2 = h1
    except Exception:
        h2 = False

    # ¬Q: The quotient group F/F' is NOT isomorphic to the free abelian group of rank n
    # For a free group F, F/F' is isomorphic to the free abelian group of rank equal to rank(F).
    # Thus, it fails to be isomorphic to Z^n if and only if rank(F) != n.
    try:
        if h1 and n is not None:
            rank = len(F.generators)
            neg_q = bool(rank != int(n))
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a free group on a set S",
    "H_2: F' is the commutator subgroup of F",
    "¬Q: The quotient group F/F' is not isomorphic to the free abelian group of rank n"
]

N_HYP = 2
NEG_Q_INDEX = 2