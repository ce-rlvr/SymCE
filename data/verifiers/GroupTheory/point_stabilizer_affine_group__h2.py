import sympy
from sympy import eye, zeros, Matrix
from sympy.combinatorics import SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
import math
import itertools
import functools
import z3

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
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_vector_space', witness.get('H1', False)))
            h2 = bool(witness.get('is_zero_vector', witness.get('H2', False)))
            q = bool(witness.get('stabilizer_is_expected', witness.get('Q', True)))
            return [h1, h2, not q]
    except Exception:
        pass

    try:
        if hasattr(witness, 'is_vector_space') or hasattr(witness, 'H1'):
            h1 = bool(getattr(witness, 'is_vector_space', getattr(witness, 'H1', False)))
            h2 = bool(getattr(witness, 'is_zero_vector', getattr(witness, 'H2', False)))
            q = bool(getattr(witness, 'stabilizer_is_expected', getattr(witness, 'Q', True)))
            return [h1, h2, not q]
    except Exception:
        pass

    try:
        if isinstance(witness, (tuple, list)) and len(witness) >= 3:
            h1 = bool(witness[0])
            h2 = bool(witness[1])
            q = bool(witness[2])
            return [h1, h2, not q]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: V is a vector space",
    "H_2: 0 is the zero vector in V",
    "¬Q: The stabilizer of 0 in Aff(V) is NOT the subgroup {(A, 0) | A in GL(V)} or is NOT naturally isomorphic to GL(V)"
]

N_HYP = 2
NEG_Q_INDEX = 2