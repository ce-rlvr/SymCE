import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    try:
        F1, S1, F2, S2 = witness
    except Exception:
        return [False, False, False]
    
    # H1: F1 is a free group on a set S1
    try:
        h1 = (type(F1).__name__ == 'FreeGroup') and (set(S1) == set(F1.generators))
    except Exception:
        h1 = False
        
    # H2: F1 is isomorphic to F2
    try:
        if F1 == F2:
            h2 = True
        elif type(F1).__name__ == 'FreeGroup' and type(F2).__name__ == 'FreeGroup':
            h2 = len(F1.generators) == len(F2.generators)
        elif hasattr(F1, 'is_isomorphic'):
            h2 = bool(F1.is_isomorphic(F2))
        else:
            try:
                if type(F1).__name__ == 'FreeGroup' and len(F1.generators) == 0:
                    order_val = F2.order() if callable(getattr(F2, 'order', None)) else getattr(F2, 'order', None)
                    h2 = (order_val == 1) or bool(getattr(F2, 'is_trivial', False))
                else:
                    h2 = False
            except Exception:
                h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: S1 and S2 do NOT have the same cardinality
    try:
        neg_q = len(set(S1)) != len(set(S2))
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F1 is a free group on a set S1",
    "H_2: F1 is isomorphic to F2",
    "¬Q: The sets S1 and S2 do not have the same cardinality"
]

N_HYP = 2
NEG_Q_INDEX = 2