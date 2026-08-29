import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # Extract F and S
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            F, S_raw = witness
        else:
            F = witness
            S_raw = F.generators if hasattr(F, 'generators') else F.basis
        
        # Convert to list to avoid consuming iterators multiple times
        S = list(S_raw)
    except Exception:
        return [False, False, False]

    # H1: S is a free generating set of F
    h1 = False
    try:
        if hasattr(F, 'is_free_generating_set'):
            h1 = bool(F.is_free_generating_set(S))
        elif hasattr(F, 'is_free'):
            if F.is_free:
                gens = getattr(F, 'generators', getattr(F, 'basis', None))
                if gens is not None:
                    h1 = (set(S) == set(gens))
            else:
                h1 = False
        elif type(F).__name__ == 'FreeGroup':
            h1 = (set(S) == set(F.generators))
        elif hasattr(F, 'relators'):
            h1 = (len(F.relators) == 0 and set(S) == set(F.generators))
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: the cardinality of S is exactly 1
    h2 = False
    try:
        h2 = (len(S) == 1)
    except Exception:
        h2 = False

    # neg_Q: F is NOT isomorphic to the additive group of integers Z
    neg_q = False
    try:
        is_iso = False
        if hasattr(F, 'is_isomorphic_to_Z'):
            is_iso = bool(F.is_isomorphic_to_Z())
        elif type(F).__name__ == 'FreeGroup':
            is_iso = (len(F.generators) == 1)
        elif hasattr(F, 'abelian_invariants'):
            is_iso = (list(F.abelian_invariants()) == [0])
        elif hasattr(F, 'is_group') and not F.is_group:
            is_iso = False
        else:
            # Default for groups with a free generating set of size 1
            if getattr(F, 'is_group', True) and h1 and h2:
                is_iso = True
            else:
                is_iso = False
                
        neg_q = not is_iso
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is a free generating set of F",
    "H_2: the cardinality of S is exactly 1",
    "not Q: F is NOT isomorphic to the additive group of integers Z"
]

N_HYP = 2
NEG_Q_INDEX = 2