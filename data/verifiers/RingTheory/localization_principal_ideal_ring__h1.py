import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2,2)
O3 = sympy.matrices.zeros(3,3)

def conditions(witness) -> list[bool]:
    # Extract R and S if possible
    R, S_set = None, None
    is_tuple_like = False
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            S_set = witness.get('S')
            is_tuple_like = True
        elif isinstance(witness, (list, tuple)) and len(witness) == 2:
            R, S_set = witness
            is_tuple_like = True
    except Exception:
        pass

    # H1: R is a principal ideal ring
    h1 = False
    try:
        if hasattr(witness, 'is_principal_ideal_ring'):
            val = witness.is_principal_ideal_ring
            h1 = bool(val() if callable(val) else val)
        elif is_tuple_like:
            if hasattr(R, 'is_PID') and R.is_PID:
                h1 = True
            elif R in [sympy.ZZ, sympy.QQ]:
                h1 = True
            elif str(R) in ['ZZ', 'QQ']:
                h1 = True
    except Exception:
        h1 = False

    # H2: S is a multiplicatively closed subset of R
    h2 = False
    try:
        if hasattr(witness, 'is_multiplicatively_closed'):
            val = witness.is_multiplicatively_closed
            h2 = bool(val() if callable(val) else val)
        elif is_tuple_like:
            elements = list(S_set)
            h2 = True
            for a in elements:
                for b in elements:
                    if (a * b) not in elements:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # neg_Q: The localized ring S^{-1}R is NOT a principal ideal ring
    neg_q = False
    try:
        if hasattr(witness, 'localized_is_principal_ideal_ring'):
            val = witness.localized_is_principal_ideal_ring
            neg_q = not bool(val() if callable(val) else val)
        elif is_tuple_like:
            elements = list(S_set)
            # S^-1 R is the zero ring iff 0 is in S. 
            # The zero ring is not considered a principal ideal ring (as 1 != 0 is required).
            if 0 in elements or getattr(R, 'zero', 0) in elements:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal ring",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: The localized ring S^{-1}R is not a principal ideal ring"
]

N_HYP = 2
NEG_Q_INDEX = 2