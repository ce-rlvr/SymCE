import sympy
from sympy import eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

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

def conditions(witness) -> list[bool]:
    # Check if witness is a self-contained test object
    if hasattr(witness, 'H1') and hasattr(witness, 'H2') and hasattr(witness, 'neg_Q'):
        try:
            return [bool(witness.H1()), bool(witness.H2()), bool(witness.neg_Q())]
        except Exception:
            pass

    # Extract R, R_op, u
    R = getattr(witness, 'R', None)
    R_op = getattr(witness, 'R_op', None)
    u = getattr(witness, 'u', None)
    
    if R is None and isinstance(witness, dict):
        R = witness.get('R')
        R_op = witness.get('R_op')
        u = witness.get('u')
        
    if R is None and isinstance(witness, (list, tuple)) and len(witness) >= 3:
        R, R_op, u = witness[0], witness[1], witness[2]

    # H1: R is a ring with identity
    h1 = False
    try:
        if hasattr(witness, 'is_ring_with_identity'):
            h1 = bool(witness.is_ring_with_identity())
        elif hasattr(R, 'is_ring_with_identity'):
            h1 = bool(R.is_ring_with_identity())
        elif hasattr(R, 'has_identity'):
            h1 = bool(R.has_identity)
        elif hasattr(R, 'is_Ring') and R.is_Ring:
            h1 = True
    except Exception:
        pass

    # H2: R^op is the opposite ring of R
    h2 = False
    try:
        if hasattr(witness, 'is_opposite_ring'):
            h2 = bool(witness.is_opposite_ring())
        elif hasattr(R_op, 'is_opposite_ring_of'):
            h2 = bool(R_op.is_opposite_ring_of(R))
        elif hasattr(R, 'opposite_ring'):
            h2 = bool(R_op == R.opposite_ring())
        elif R_op == R and hasattr(R, 'is_commutative') and R.is_commutative:
            h2 = True
    except Exception:
        pass

    # neg_Q: u is a unit in R iff u is a unit in R^op (negated)
    neg_q = False
    try:
        if hasattr(witness, 'units_iff'):
            neg_q = not bool(witness.units_iff())
        else:
            def check_unit(ring, element):
                if hasattr(ring, 'is_unit'):
                    return bool(ring.is_unit(element))
                if hasattr(element, 'is_unit_in'):
                    return bool(element.is_unit_in(ring))
                if hasattr(element, 'is_unit'):
                    if callable(element.is_unit):
                        return bool(element.is_unit())
                    return bool(element.is_unit)
                if hasattr(ring, 'invert'):
                    try:
                        ring.invert(element)
                        return True
                    except Exception:
                        return False
                raise ValueError("Cannot determine unit status")

            u_in_R = check_unit(R, u)
            u_in_R_op = check_unit(R_op, u)
            neg_q = (u_in_R != u_in_R_op)
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring with identity",
    "H_2: R^op is the opposite ring of R",
    "¬Q: u is a unit in R is not equivalent to u is a unit in R^op"
]

N_HYP = 2
NEG_Q_INDEX = 2