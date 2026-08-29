import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # Unpack witness if it's a tuple of (G, n), otherwise assume it's just G
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, n = witness
        else:
            G = witness
            try:
                n = G.order()
            except Exception:
                n = None
    except Exception:
        G = witness
        n = None

    # H_1: G is a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: The order of G is n
    try:
        h2_ok = False
        if h1_ok and n is not None:
            h2_ok = (G.order() == n)
    except Exception:
        h2_ok = False

    # ¬Q: G is not a cyclic group
    try:
        neg_q_ok = False
        if h1_ok:
            is_cyclic_attr = getattr(G, 'is_cyclic', None)
            if is_cyclic_attr is not None:
                if callable(is_cyclic_attr):
                    is_cyclic_val = is_cyclic_attr()
                else:
                    is_cyclic_val = is_cyclic_attr
                neg_q_ok = not is_cyclic_val
            else:
                order = G.order()
                if order > 10000:
                    neg_q_ok = False  # Too large to safely brute-force
                else:
                    is_cyclic_fallback = False
                    for g in G.elements:
                        if g.order() == order:
                            is_cyclic_fallback = True
                            break
                    neg_q_ok = not is_cyclic_fallback
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The order of G is n",
    "¬Q: G is not a cyclic group"
]

N_HYP = 2
NEG_Q_INDEX = 2