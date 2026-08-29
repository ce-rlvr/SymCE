import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: S and T are multiplicative subsets of R",
    "H_2: T_bar is the image of T under the canonical ring homomorphism R -> S^{-1}R",
    "¬Q: The localized ring T_bar^{-1}(S^{-1}R) is not isomorphic to the localized ring (ST)^{-1}R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    if hasattr(witness, "evaluate"):
        try:
            res = witness.evaluate()
            if isinstance(res, list) and len(res) == 3:
                return res
        except Exception:
            pass

    try:
        if hasattr(witness, "S_is_multiplicative") and hasattr(witness, "T_is_multiplicative"):
            h1 = bool(witness.S_is_multiplicative() and witness.T_is_multiplicative())
        elif isinstance(witness, dict):
            h1 = bool(witness.get("h1", witness.get("S_and_T_multiplicative", False)))
        elif hasattr(witness, "h1"):
            if callable(witness.h1):
                h1 = bool(witness.h1())
            else:
                h1 = bool(witness.h1)
    except Exception:
        h1 = False

    try:
        if hasattr(witness, "T_bar_is_image"):
            h2 = bool(witness.T_bar_is_image())
        elif isinstance(witness, dict):
            h2 = bool(witness.get("h2", witness.get("T_bar_is_image", False)))
        elif hasattr(witness, "h2"):
            if callable(witness.h2):
                h2 = bool(witness.h2())
            else:
                h2 = bool(witness.h2)
    except Exception:
        h2 = False

    try:
        if hasattr(witness, "is_isomorphic"):
            neg_q = not bool(witness.is_isomorphic())
        elif isinstance(witness, dict):
            neg_q = bool(witness.get("neg_q", witness.get("not_isomorphic", False)))
        elif hasattr(witness, "neg_q"):
            if callable(witness.neg_q):
                neg_q = bool(witness.neg_q())
            else:
                neg_q = bool(witness.neg_q)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]