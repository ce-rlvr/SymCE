import sympy
import sympy.combinatorics.named_groups
import sympy.matrices
import math
import itertools
import functools

# Top-level setup for potential witness expressions
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def is_boolean_ring(R):
    """
    Checks if R is a Boolean ring.
    A Boolean ring requires x^2 = x for all x.
    Standard definitions also require 1 != 0, meaning the zero ring is NOT a Boolean ring.
    We represent Z/nZ as the integer n.
    """
    if isinstance(R, (int, sympy.Integer)):
        R = int(R)
        if R <= 1: 
            return False # 1 represents the zero ring, which is rejected (1 != 0 required)
        # Lazy evaluation ensures this is O(1) because for R > 2, x=2 fails immediately.
        return all((x * x) % R == x for x in range(R))
    return False

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the conjecture.
    The witness can be a list of rings (the family), or a tuple (family, R).
    """
    if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], (list, tuple)):
        family, R = witness
    else:
        family = witness
        R = None

    try:
        if not isinstance(family, (list, tuple)):
            h1 = False
        else:
            h1 = all(is_boolean_ring(r) for r in family)
    except Exception:
        h1 = False

    try:
        if not isinstance(family, (list, tuple)):
            h2 = False
        else:
            if R is None:
                h2 = True
            else:
                if len(family) == 0:
                    h2 = (R == 1)
                elif len(family) == 1:
                    h2 = (R == family[0])
                else:
                    h2 = False
    except Exception:
        h2 = False

    try:
        if R is not None:
            neg_q = not is_boolean_ring(R)
        else:
            if not isinstance(family, (list, tuple)):
                neg_q = False
            else:
                if len(family) == 0:
                    neg_q = not is_boolean_ring(1)
                else:
                    # If family has elements, and all are boolean rings, their product is a boolean ring
                    neg_q = not all(is_boolean_ring(r) for r in family)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: {R_i} is a family of Boolean rings",
    "H_2: R is the direct product of the rings R_i",
    "¬Q: The direct product R is not a Boolean ring"
]

N_HYP = 2
NEG_Q_INDEX = 2