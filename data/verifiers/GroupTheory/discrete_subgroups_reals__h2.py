import sympy
from sympy import S, FiniteSet
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H1: G is a discrete topological space under the subspace topology inherited from R
    # This means G must be a discrete subset of R.
    h1_ok = False
    try:
        if isinstance(witness, sympy.Set):
            if witness.is_FiniteSet:
                h1_ok = all(e.is_real for e in witness)
            elif witness in (S.Integers, S.Naturals, S.Naturals0):
                h1_ok = True
            elif witness.is_subset(S.Integers):
                h1_ok = True
        elif isinstance(witness, (list, set, tuple)):
            h1_ok = all(getattr(e, 'is_real', isinstance(e, (int, float))) for e in witness)
    except Exception:
        h1_ok = False

    # neg_Q: G is NOT the trivial group {0} AND G is NOT isomorphic to Z
    neg_q_ok = False
    try:
        is_trivial = False
        if isinstance(witness, sympy.Set):
            if witness.is_FiniteSet and len(witness) == 1 and S.Zero in witness:
                is_trivial = True
        elif isinstance(witness, (list, set, tuple)):
            if len(witness) == 1:
                elem = list(witness)[0]
                if elem == 0 or elem == S.Zero:
                    is_trivial = True
        
        is_iso_Z = False
        if isinstance(witness, sympy.Set):
            if witness.is_FiniteSet:
                is_iso_Z = False
            elif witness == S.Integers:
                is_iso_Z = True
        elif isinstance(witness, (list, set, tuple)):
            is_iso_Z = False
            
        neg_q_ok = not (is_trivial or is_iso_Z)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a discrete topological space under the subspace topology inherited from R",
    "¬Q: G is neither the trivial group {0} nor isomorphic to the additive group of integers Z"
]

N_HYP = 1
NEG_Q_INDEX = 1