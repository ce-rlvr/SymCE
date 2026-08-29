import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup, PermutationGroup
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

def conditions(witness) -> list[bool]:
    """
    Given a witness (F, N, M), checks if it is a valid counterexample to the conjecture.
    """
    try:
        if len(witness) != 3:
            return [False, False, False]
        F, N, M = witness
    except Exception:
        return [False, False, False]

    # H_1: F is a free group
    h1 = False
    try:
        if type(F).__name__ == 'FreeGroup':
            h1 = True
        elif hasattr(F, 'is_free_group'):
            val = F.is_free_group
            h1 = bool(val() if callable(val) else val)
    except Exception:
        pass

    # H_2: N and M are non-trivial normal subgroups of F
    h2 = False
    try:
        def is_non_trivial_normal(grp, subgrp):
            # Check non-triviality
            is_trivial = False
            if hasattr(subgrp, 'is_trivial'):
                val = subgrp.is_trivial
                is_trivial = bool(val() if callable(val) else val)
            elif hasattr(subgrp, 'order'):
                val = subgrp.order
                is_trivial = ((val() if callable(val) else val) == 1)
            elif hasattr(subgrp, 'generators'):
                is_trivial = (len(subgrp.generators) == 0)
            
            if is_trivial:
                return False
                
            # Check normality
            if hasattr(grp, 'is_normal'):
                val = grp.is_normal
                return bool(val(subgrp) if callable(val) else val)
            if hasattr(subgrp, 'is_normal'):
                val = subgrp.is_normal
                return bool(val(grp) if callable(val) else val)
            return False

        h2 = is_non_trivial_normal(F, N) and is_non_trivial_normal(F, M)
    except Exception:
        pass

    # ¬Q: The intersection N \cap M is trivial
    neg_q = False
    try:
        def is_trivial_intersection(sub1, sub2):
            if hasattr(sub1, 'intersection'):
                val = sub1.intersection
                intersect = val(sub2) if callable(val) else val
                if hasattr(intersect, 'is_trivial'):
                    v = intersect.is_trivial
                    return bool(v() if callable(v) else v)
                if hasattr(intersect, 'order'):
                    v = intersect.order
                    return (v() if callable(v) else v) == 1
                if hasattr(intersect, 'generators'):
                    return len(intersect.generators) == 0
            return False

        neg_q = is_trivial_intersection(N, M)
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "H_2: N and M are non-trivial normal subgroups of F",
    "¬Q: The intersection N \\cap M is trivial"
]

N_HYP = 2
NEG_Q_INDEX = 2