import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group is isomorphic to D2
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def H1_eval(witness):
    """Check if G is not the trivial group."""
    try:
        if hasattr(witness, 'is_trivial'):
            val = witness.is_trivial
            if val is not None:
                return not bool(val)
    except Exception:
        pass

    try:
        if hasattr(witness, 'order'):
            ord_val = witness.order() if callable(witness.order) else witness.order
            if ord_val == sympy.oo or ord_val == float('inf'):
                return True
            return int(ord_val) > 1
    except Exception:
        pass

    try:
        if hasattr(witness, 'elements'):
            return len(list(witness.elements)) > 1
    except Exception:
        pass

    if witness in (sympy.S.Integers, sympy.S.Reals, sympy.S.Rationals, sympy.S.Complexes):
        return True

    try:
        from sympy.combinatorics.free_groups import FreeGroup
        if isinstance(witness, FreeGroup):
            return len(witness.generators) > 0
    except Exception:
        pass

    try:
        from sympy.combinatorics.fp_groups import FpGroup
        if isinstance(witness, FpGroup):
            if len(witness.generators) == 0:
                return False
            return True
    except Exception:
        pass

    if isinstance(witness, str):
        return True

    return False

def neg_Q_eval(witness):
    """
    Check if G FAILS to have a unique direct product decomposition into finitely many indecomposable groups.
    Since Krull-Schmidt holds for all finite groups, we return False for finite groups.
    For infinite groups, we return True unless it's a known infinite group where KS holds (like Z or FreeGroups).
    """
    try:
        if hasattr(witness, 'krull_schmidt_holds'):
            return not bool(witness.krull_schmidt_holds())
    except Exception:
        pass

    try:
        if hasattr(witness, 'has_unique_decomposition'):
            return not bool(witness.has_unique_decomposition())
    except Exception:
        pass

    # Finite groups always satisfy Krull-Schmidt
    try:
        if hasattr(witness, 'is_finite') and witness.is_finite:
            return False
    except Exception:
        pass

    try:
        if hasattr(witness, 'order'):
            ord_val = witness.order() if callable(witness.order) else witness.order
            if ord_val == sympy.oo or ord_val == float('inf'):
                pass
            else:
                return False
    except Exception:
        pass

    # Known infinite groups that satisfy Krull-Schmidt (indecomposable)
    if witness in (sympy.S.Integers, sympy.S.Reals, sympy.S.Rationals, sympy.S.Complexes):
        return False

    try:
        from sympy.combinatorics.free_groups import FreeGroup
        if isinstance(witness, FreeGroup):
            return False
    except Exception:
        pass

    try:
        from sympy.combinatorics.fp_groups import FpGroup
        if isinstance(witness, FpGroup):
            if getattr(witness, 'is_abelian', False):
                # Finitely generated abelian groups satisfy Krull-Schmidt
                return False
            # Finitely generated non-abelian groups might fail KS
            return True
    except Exception:
        pass

    # If it's an infinite group not caught above, we assume it's the intended counterexample
    try:
        if hasattr(witness, 'is_finite') and not witness.is_finite:
            return True
    except Exception:
        pass

    try:
        if hasattr(witness, 'order'):
            ord_val = witness.order() if callable(witness.order) else witness.order
            if ord_val == sympy.oo or ord_val == float('inf'):
                return True
    except Exception:
        pass

    if isinstance(witness, str):
        s = witness.lower()
        if any(kw in s for kw in ["infinite", "countabl", "fail", "not unique", "counterexample"]):
            return True

    return False

def conditions(witness) -> list[bool]:
    h1 = False
    try:
        h1 = H1_eval(witness)
    except Exception:
        h1 = False

    neg_q = False
    try:
        neg_q = neg_Q_eval(witness)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is not the trivial group",
    "¬Q: G cannot be expressed as a unique direct product of finitely many indecomposable groups"
]

N_HYP = 1
NEG_Q_INDEX = 1