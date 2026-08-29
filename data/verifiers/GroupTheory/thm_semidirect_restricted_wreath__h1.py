import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
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

CONDITION_LABELS = [
    "H_1: B acts on a set X",
    "H_2: A^(X) is the direct sum of copies of A indexed by X",
    "H_3: A ≀_X B is the restricted wreath product of A by B over X",
    "¬Q: A ≀_X B is not isomorphic to the external semidirect product A^(X) ⋊ B with the induced coordinate-shifting action"
]

N_HYP = 3
NEG_Q_INDEX = 3

def is_group(obj):
    try:
        if hasattr(obj, 'is_group') and obj.is_group:
            return True
        if hasattr(obj, 'is_Group') and obj.is_Group:
            return True
        name = type(obj).__name__
        if 'Group' in name:
            return True
    except Exception:
        pass
    return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            if "H1" in witness or "B_acts_on_X" in witness or "neg_Q" in witness:
                h1 = bool(witness.get("H1", witness.get("B_acts_on_X", True)))
                h2 = bool(witness.get("H2", witness.get("A_X_is_direct_sum", True)))
                h3 = bool(witness.get("H3", witness.get("wreath_is_restricted", True)))
                neg_q = bool(witness.get("neg_Q", not witness.get("isomorphic", False)))
                return [h1, h2, h3, neg_q]
    except Exception:
        pass

    try:
        if isinstance(witness, tuple) and len(witness) >= 2:
            A = witness[0]
            B = witness[1]
            h1 = True
            h2 = True
            h3 = True
            # If both are groups, the theorem holds (isomorphic), so neg_Q is False.
            # If one is not a group, the conclusion fails, so neg_Q is True.
            neg_q = not (is_group(A) and is_group(B))
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    try:
        if isinstance(witness, str):
            s = witness.lower()
            h1 = True
            h2 = True
            h3 = True
            neg_q = not ("isomorphic" in s and "not" not in s and "fail" not in s)
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    try:
        if is_group(witness):
            return [True, True, True, False]
    except Exception:
        pass

    try:
        if hasattr(witness, "H1") or hasattr(witness, "B_acts_on_X") or hasattr(witness, "neg_Q"):
            h1 = bool(getattr(witness, "H1", getattr(witness, "B_acts_on_X", True)))
            h2 = bool(getattr(witness, "H2", getattr(witness, "A_X_is_direct_sum", True)))
            h3 = bool(getattr(witness, "H3", getattr(witness, "wreath_is_restricted", True)))
            neg_q = bool(getattr(witness, "neg_Q", not getattr(witness, "isomorphic", False)))
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    return [False, False, False, False]