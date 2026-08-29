import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.combinatorics.permutations import Permutation
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
    """
    Checks if the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (F, x) where F is a group and x is an element of F.
    """
    try:
        F, x = witness
    except Exception:
        return [False, False, False]
    
    # H_1: The rank of F is at least 2
    # For finitely generated groups, rank >= 2 is equivalent to being non-cyclic and non-trivial.
    try:
        order_val = F.order() if callable(F.order) else F.order
        if order_val <= 1:
            h1 = False
        else:
            is_cyc = False
            # If the group is not abelian, it cannot be cyclic
            if hasattr(F, 'is_abelian') and not F.is_abelian:
                is_cyc = False
            else:
                # If abelian, check if any element generates the whole group
                for g in F.elements:
                    g_order = g.order() if callable(g.order) else g.order
                    if g_order == order_val:
                        is_cyc = True
                        break
            h1 = not is_cyc
    except Exception:
        h1 = False

    # H_2: x is a non-identity element of F
    try:
        h2 = bool((x in F) and (x != F.identity))
    except Exception:
        h2 = False

    # neg_Q: The conjugacy class of x in F is not infinite
    # If F is a finite group, the conjugacy class of any element is strictly finite.
    try:
        if hasattr(F, 'is_finite') and F.is_finite:
            neg_q = True
        elif hasattr(F, 'order'):
            order_val = F.order() if callable(F.order) else F.order
            if order_val < float('inf'):
                neg_q = True
            else:
                neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The rank of F is at least 2",
    "H_2: x is a non-identity element of F",
    "¬Q: The conjugacy class of x in F is not infinite"
]

N_HYP = 2
NEG_Q_INDEX = 2