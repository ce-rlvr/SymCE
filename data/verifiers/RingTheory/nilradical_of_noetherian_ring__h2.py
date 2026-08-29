import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, N = witness
        else:
            R = witness
            N = getattr(R, 'nilradical', None)
            if N is None:
                N = getattr(R, 'N', None)
    except Exception:
        return [False, False, False]

    # H_1: R is a commutative ring with identity
    try:
        is_comm = False
        if hasattr(R, 'is_commutative'):
            is_comm = R.is_commutative() if callable(R.is_commutative) else bool(R.is_commutative)
        
        has_id = False
        if hasattr(R, 'has_identity'):
            has_id = R.has_identity() if callable(R.has_identity) else bool(R.has_identity)
            
        h1_ok = is_comm and has_id
    except Exception:
        h1_ok = False

    # H_2: N is the nilradical of R
    try:
        h2_ok = False
        if hasattr(N, 'is_nilradical_of'):
            h2_ok = N.is_nilradical_of(R) if callable(N.is_nilradical_of) else bool(N.is_nilradical_of)
        elif hasattr(R, 'is_nilradical'):
            h2_ok = R.is_nilradical(N) if callable(R.is_nilradical) else bool(R.is_nilradical)
        elif hasattr(R, 'nilradical'):
            h2_ok = (R.nilradical == N)
        elif N is not None:
            if hasattr(N, 'is_nilradical'):
                h2_ok = N.is_nilradical() if callable(N.is_nilradical) else bool(N.is_nilradical)
            else:
                h2_ok = True
    except Exception:
        h2_ok = False

    # ¬Q: N is NOT nilpotent (there does not exist a positive integer k such that N^k = {0})
    try:
        is_nilp = True
        if hasattr(N, 'is_nilpotent'):
            is_nilp = N.is_nilpotent() if callable(N.is_nilpotent) else bool(N.is_nilpotent)
        elif hasattr(R, 'is_nilpotent'):
            is_nilp = R.is_nilpotent(N) if callable(R.is_nilpotent) else bool(R.is_nilpotent)
        elif hasattr(N, 'is_nilpotent_ideal'):
            is_nilp = N.is_nilpotent_ideal() if callable(N.is_nilpotent_ideal) else bool(N.is_nilpotent_ideal)
        
        neg_q_ok = not is_nilp
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: N is the nilradical of R",
    "¬Q: N is not nilpotent (there is no k such that N^k = {0})"
]

N_HYP = 2
NEG_Q_INDEX = 2