import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
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
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample.
    The witness should be a tuple (G, y) where G is a group and y is a subset of G.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, y = witness
        else:
            G = witness
            y = None
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: G acts on itself by left multiplication
    try:
        # This is a definitional property for any group acting on itself
        if h1:
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: The stabilizer of y under this action is NOT the trivial subgroup {e}
    try:
        if not h1:
            neg_q = False
        else:
            e = G.identity
            is_elem = False
            try:
                # Check if y is a single element of G
                if y in G.elements:
                    is_elem = True
            except TypeError:
                is_elem = False
            
            if is_elem:
                # If y is an element, the stabilizer is {g in G | g*y = y}
                stab = {g for g in G.elements if g * y == y}
                neg_q = (stab != {e})
            else:
                try:
                    # Treat y as a subset of G
                    y_set = set(y)
                    if not y_set.issubset(G.elements):
                        neg_q = False
                    else:
                        stab = set()
                        for g in G.elements:
                            # Left multiplication of the subset by g
                            gy = {g * x for x in y_set}
                            if gy == y_set:
                                stab.add(g)
                        neg_q = (stab != {e})
                except TypeError:
                    neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    r"H_1: G is a group",
    r"H_2: G acts on itself by left multiplication",
    r"¬Q: The stabilizer of y under this action is not the trivial subgroup {e}"
]

N_HYP = 2
NEG_Q_INDEX = 2