import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import Matrix
import itertools
import math
import functools

# Standard group theory bindings
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

# Standard linear algebra bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture claims that in any ring R, the principal left ideals Ra and R(1-a) 
    are comaximal (i.e., Ra + R(1-a) = R).
    This is always true if R has an identity (since 1 = a + (1-a) in Ra + R(1-a)).
    The conclusion fails only if R lacks an identity, making 1-a undefined.
    """
    if isinstance(witness, tuple) and len(witness) == 2:
        R, a = witness
    else:
        R = witness
        a = None

    # H_1: R is a ring
    h1 = False
    try:
        if hasattr(R, 'is_ring'):
            h1 = R.is_ring() if callable(R.is_ring) else bool(R.is_ring)
        elif hasattr(R, 'is_Ring'):
            h1 = R.is_Ring() if callable(R.is_Ring) else bool(R.is_Ring)
        else:
            elements = list(R)
            if len(elements) > 0:
                h1 = True
                for x in elements:
                    if not h1: break
                    for y in elements:
                        if not any(x + y == e for e in elements):
                            h1 = False
                            break
                        if not any(x - y == e for e in elements):
                            h1 = False
                            break
                        if not any(x * y == e for e in elements):
                            h1 = False
                            break
            else:
                h1 = False
                
        # If a is provided, it must be an element of R
        if h1 and a is not None:
            if hasattr(R, '__contains__'):
                try:
                    if a not in R:
                        h1 = False
                except Exception:
                    h1 = False
            else:
                try:
                    elements = list(R)
                    if not any(a == e for e in elements):
                        h1 = False
                except Exception:
                    h1 = False
    except Exception:
        h1 = False

    # neg_Q: The conclusion fails (R does not have an identity, so 1-a is undefined)
    neg_q = False
    try:
        if hasattr(R, 'has_identity'):
            has_id = R.has_identity() if callable(R.has_identity) else bool(R.has_identity)
            neg_q = not has_id
        elif hasattr(R, 'is_unital'):
            has_id = R.is_unital() if callable(R.is_unital) else bool(R.is_unital)
            neg_q = not has_id
        elif hasattr(R, 'identity'):
            has_id = (R.identity is not None)
            neg_q = not has_id
        elif type(R).__module__.startswith('sympy.'):
            # Standard SymPy rings (ZZ, QQ, PolyRing, etc.) are unital
            has_id = True
            neg_q = not has_id
        else:
            elements = list(R)
            has_id = False
            for e in elements:
                is_id = True
                for x in elements:
                    if e * x != x or x * e != x:
                        is_id = False
                        break
                if is_id:
                    has_id = True
                    break
            neg_q = not has_id
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "¬Q: The principal left ideals Ra and R(1-a) are not comaximal (e.g., 1-a is undefined because R lacks an identity)"
]

N_HYP = 1
NEG_Q_INDEX = 1