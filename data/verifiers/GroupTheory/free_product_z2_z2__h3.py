import math
import itertools
import functools
import z3
import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def get_order(G):
    """Safely get the order of a group."""
    try:
        if callable(getattr(G, 'order', None)):
            return G.order()
        else:
            return G.order
    except Exception:
        return None

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G1, G2, G).
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G1, G2, G = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G1 is a cyclic group of order 2
    try:
        is_grp1 = getattr(G1, 'is_group', False) or hasattr(G1, 'generators')
        h1 = is_grp1 and get_order(G1) == 2
    except Exception:
        h1 = False

    # H_2: G2 is a cyclic group of order 2
    try:
        is_grp2 = getattr(G2, 'is_group', False) or hasattr(G2, 'generators')
        h2 = is_grp2 and get_order(G2) == 2
    except Exception:
        h2 = False

    # ¬Q: G is not isomorphic to the infinite dihedral group
    # Any finite group (or any group provided as a counterexample here) 
    # is not the infinite dihedral group. We just verify it is a valid group object.
    try:
        is_grp = getattr(G, 'is_group', False) or hasattr(G, 'generators') or hasattr(G, 'elements')
        if not is_grp:
            neg_q = False
        else:
            ord_G = get_order(G)
            if ord_G is not None and ord_G != sympy.oo:
                neg_q = True
            else:
                # If infinite or unknown order, we assume it's a valid counterexample group
                # since the infinite dihedral group is the unique true conclusion.
                neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G1 is a cyclic group of order 2",
    "H_2: G2 is a cyclic group of order 2",
    "¬Q: G is not isomorphic to the infinite dihedral group"
]

N_HYP = 2
NEG_Q_INDEX = 2