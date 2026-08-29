import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: G is an abelian group
    try:
        if hasattr(witness, 'is_abelian'):
            if callable(witness.is_abelian):
                h1 = bool(witness.is_abelian())
            else:
                h1 = bool(witness.is_abelian)
        else:
            h1 = False
    except Exception:
        h1 = False

    # ¬Q: G is not finitely presented
    try:
        is_fp = True
        if hasattr(witness, 'is_finitely_presented'):
            if callable(witness.is_finitely_presented):
                is_fp = bool(witness.is_finitely_presented())
            else:
                is_fp = bool(witness.is_finitely_presented)
        elif hasattr(witness, 'is_finitely_generated'):
            if callable(witness.is_finitely_generated):
                is_fg = bool(witness.is_finitely_generated())
            else:
                is_fg = bool(witness.is_finitely_generated)
            if not is_fg:
                is_fp = False
        elif isinstance(witness, PermutationGroup) or type(witness).__name__ in ('FpGroup', 'FreeGroup'):
            is_fp = True
        elif hasattr(witness, 'is_finite'):
            if callable(witness.is_finite):
                if bool(witness.is_finite()):
                    is_fp = True
            else:
                if bool(witness.is_finite):
                    is_fp = True
        
        neg_q = not is_fp
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "¬Q: G is not finitely presented"
]

N_HYP = 1
NEG_Q_INDEX = 1