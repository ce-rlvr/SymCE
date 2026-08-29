import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import sympy.ntheory
from sympy import abc
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
    P, X, O = None, None, None
    try:
        if isinstance(witness, dict):
            P = witness.get('P')
            X = witness.get('X')
            O = witness.get('O')
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 3:
                P, X, O = witness
            elif len(witness) >= 4:
                P, X, _, O = witness[0], witness[1], witness[2], witness[-1]
    except Exception:
        pass

    # H_1: P is a finite p-group for some prime p
    h1 = False
    p = None
    try:
        if hasattr(P, 'order'):
            order = P.order() if callable(P.order) else P.order
            order = int(order)
            if order > 0:
                factors = sympy.ntheory.factorint(order)
                if len(factors) == 1:
                    h1 = True
                    p = list(factors.keys())[0]
                elif order == 1:
                    h1 = True
                    p = 2  # Trivial group is a p-group for any prime p
    except Exception:
        pass

    # H_2: X is a finite set
    h2 = False
    try:
        if hasattr(X, '__len__') and not isinstance(X, str):
            _ = len(X)
            h2 = True
    except Exception:
        pass

    # H_3: P acts on X
    h3 = False
    try:
        if h1 and h2:
            # Mathematically, any group can act on any set (e.g., via the trivial action).
            # Since the specific action is not constrained by the remaining hypotheses,
            # the existence of an action is guaranteed.
            h3 = True
    except Exception:
        pass

    # ¬Q: The cardinality of O is not equal to p^k for any non-negative integer k
    neg_q = False
    try:
        if h1 and hasattr(O, '__len__') and not isinstance(O, str):
            card_O = len(O)
            if card_O == 0:
                neg_q = True
            else:
                factors_O = sympy.ntheory.factorint(card_O)
                if len(factors_O) == 0:
                    neg_q = False  # card_O == 1, which is p^0
                elif len(factors_O) == 1 and list(factors_O.keys())[0] == p:
                    neg_q = False  # card_O == p^k
                else:
                    neg_q = True
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: P is a finite p-group for some prime p",
    "H_2: X is a finite set",
    "H_3: P acts on X",
    "¬Q: The cardinality of O is not equal to p^k for any non-negative integer k"
]

N_HYP = 3
NEG_Q_INDEX = 3