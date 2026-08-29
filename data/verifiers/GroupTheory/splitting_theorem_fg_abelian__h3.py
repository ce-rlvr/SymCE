import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy import Rational, Integer
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

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to be a tuple (G, T) where G is a finitely generated abelian group
    and T is a subgroup of G.
    """
    try:
        G, T = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a finitely generated group
    try:
        # In SymPy, groups like PermutationGroup and FpGroup have 'generators'
        h1_ok = hasattr(G, 'generators')
    except Exception:
        h1_ok = False

    # H_2: G is an abelian group
    try:
        h2_ok = bool(G.is_abelian)
    except Exception:
        h2_ok = False

    # ¬Q: Conclusion fails
    # Conclusion: G is isomorphic to T ⊕ G/T, and G/T is a free abelian group.
    try:
        is_sub = False
        if hasattr(T, 'is_subgroup'):
            try:
                is_sub = T.is_subgroup(G)
            except Exception:
                is_sub = False
                
        if not is_sub:
            # If T is not a subgroup, the quotient G/T is undefined, so the conclusion fails.
            neg_q_ok = True
        else:
            if hasattr(G, 'order') and hasattr(T, 'order'):
                order_G = G.order()
                order_T = T.order()
                # For finite groups, G/T is a finite group.
                # A finite group is free abelian if and only if it is the trivial group (order 1).
                # If G/T is trivial, then T = G, and G is isomorphic to T ⊕ G/T (which is G ⊕ {1} ≅ G).
                # Thus, for finite groups, the conclusion holds iff order_G == order_T.
                # The conclusion fails (neg_Q is True) iff order_G != order_T.
                neg_q_ok = (order_G != order_T)
            else:
                neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finitely generated group",
    "H_2: G is an abelian group",
    "¬Q: G is not isomorphic to T ⊕ G/T, or G/T is not a free abelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2