import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
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
        # H_1: G is a group defined by the presentation <a, b | R>
        # We verify that the witness is a valid group object.
        h1 = hasattr(witness, 'order') and hasattr(witness, 'generators')
        if h1:
            # Ensure the order method is callable and doesn't raise an error
            _ = witness.order()
    except Exception:
        h1 = False

    try:
        # ¬Q: G is not isomorphic to the quaternion group Q_8
        # Q_8 is the unique non-abelian group of order 8 with exactly one element of order 2.
        if not hasattr(witness, 'order'):
            neg_q = False
        else:
            order = witness.order()
            if order != 8:
                is_q8 = False
            else:
                is_ab = getattr(witness, 'is_abelian', None)
                if is_ab is None and hasattr(witness, 'elements'):
                    # Compute manually if the property is missing
                    elements = list(witness.elements)
                    is_ab = True
                    for a in elements:
                        for b in elements:
                            if a * b != b * a:
                                is_ab = False
                                break
                        if not is_ab:
                            break
                
                if is_ab:
                    is_q8 = False
                else:
                    if hasattr(witness, 'elements'):
                        order_2_count = sum(1 for g in witness.elements if g.order() == 2)
                        is_q8 = (order_2_count == 1)
                    else:
                        raise Exception("Cannot determine if group of order 8 is Q8 without elements")
            neg_q = not is_q8
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group defined by the presentation <a, b | R>",
    "¬Q: G is not isomorphic to the quaternion group Q_8"
]

N_HYP = 1
NEG_Q_INDEX = 1