import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness can provide a custom action to demonstrate that without the 
    hypothesis of the operation being a valid group action, the conclusion fails.
    """
    try:
        if hasattr(witness, '__len__') and not isinstance(witness, dict):
            if len(witness) == 5:
                G, g, h, x, action = witness
                def apply_action(elem, pt):
                    if callable(action):
                        return action(elem, pt)
                    else:
                        return action[(elem, pt)]
            elif len(witness) == 4:
                G, g, h, x = witness
                def apply_action(elem, pt):
                    return elem(pt)
            else:
                return [False, False, False, False]
        else:
            G = witness.G
            g = witness.g
            h = witness.h
            x = witness.x
            if hasattr(witness, 'action'):
                action = witness.action
                def apply_action(elem, pt):
                    if callable(action):
                        return action(elem, pt)
                    else:
                        return action[(elem, pt)]
            else:
                def apply_action(elem, pt):
                    return elem(pt)
    except Exception:
        return [False, False, False, False]

    # H1: g is an element of G
    try:
        h1_ok = bool(g in G)
    except Exception:
        h1_ok = False

    # H2: h is an element of the centralizer C_G(g)
    try:
        h2_ok = bool((h in G) and (h * g == g * h))
    except Exception:
        h2_ok = False

    # H3: x \in X is a fixed point of g
    try:
        h3_ok = bool(apply_action(g, x) == x)
    except Exception:
        h3_ok = False

    # neg_Q: The element h \cdot x is also a fixed point of g. (must FAIL)
    try:
        hx = apply_action(h, x)
        neg_q_ok = bool(apply_action(g, hx) != hx)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: g is an element of G",
    "H_2: h is an element of the centralizer C_G(g)",
    "H_3: x is a fixed point of g",
    "¬Q: h \cdot x is not a fixed point of g"
]

N_HYP = 3
NEG_Q_INDEX = 3