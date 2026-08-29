import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.free_groups import free_group
from sympy.combinatorics.fp_groups import FpGroup
from sympy.combinatorics.homomorphisms import homomorphism
from sympy.matrices import eye, zeros
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

def conditions(witness):
    try:
        # Unpack if witness is provided as a tuple like (Group, Homomorphism)
        if isinstance(witness, tuple) and len(witness) == 2:
            _, witness = witness
    except Exception:
        pass

    h1 = False
    try:
        if hasattr(witness, "is_homomorphism"):
            val = witness.is_homomorphism
            h1 = bool(val() if callable(val) else val)
        elif hasattr(witness, "homomorphism"):
            val = witness.homomorphism
            h1 = bool(val() if callable(val) else val)
        else:
            try:
                from sympy.combinatorics.homomorphisms import GroupHomomorphism
                if isinstance(witness, GroupHomomorphism):
                    h1 = True
            except ImportError:
                if type(witness).__name__ == "GroupHomomorphism":
                    h1 = True
    except Exception:
        h1 = False

    h2 = False
    try:
        if hasattr(witness, "is_surjective"):
            val = witness.is_surjective
            h2 = bool(val() if callable(val) else val)
        elif hasattr(witness, "surjective"):
            val = witness.surjective
            h2 = bool(val() if callable(val) else val)
    except Exception:
        h2 = False

    neg_q = False
    try:
        if hasattr(witness, "is_injective"):
            val = witness.is_injective
            inj = bool(val() if callable(val) else val)
            neg_q = not inj
        elif hasattr(witness, "injective"):
            val = witness.injective
            inj = bool(val() if callable(val) else val)
            neg_q = not inj
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: phi is a group homomorphism",
    "H_2: phi is surjective",
    "¬Q: phi is not injective"
]

N_HYP = 2
NEG_Q_INDEX = 2