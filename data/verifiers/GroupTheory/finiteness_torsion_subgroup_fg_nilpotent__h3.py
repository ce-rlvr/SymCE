import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
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
    # H1: G is a nilpotent group
    h1 = False
    try:
        if hasattr(witness, 'is_nilpotent'):
            h1 = bool(witness.is_nilpotent() if callable(witness.is_nilpotent) else witness.is_nilpotent)
        elif hasattr(witness, 'is_abelian'):
            h1 = bool(witness.is_abelian() if callable(witness.is_abelian) else witness.is_abelian)
    except Exception:
        pass

    # H2: G is finitely generated
    h2 = False
    try:
        if hasattr(witness, 'is_finitely_generated'):
            h2 = bool(witness.is_finitely_generated() if callable(witness.is_finitely_generated) else witness.is_finitely_generated)
        elif hasattr(witness, 'generators'):
            h2 = True
        elif hasattr(witness, 'is_finite'):
            is_fin = bool(witness.is_finite() if callable(witness.is_finite) else witness.is_finite)
            if is_fin:
                h2 = True
    except Exception:
        pass

    # neg_Q: T is NOT a finite characteristic subgroup of G
    neg_q = False
    try:
        t_finite_char = None
        
        if hasattr(witness, 'torsion_subgroup'):
            T = witness.torsion_subgroup
            t_fin = False
            if hasattr(T, 'order'):
                try:
                    ord_val = T.order() if callable(T.order) else T.order
                    if ord_val not in (float('inf'), sympy.oo):
                        t_fin = True
                except Exception:
                    pass
            elif hasattr(T, 'is_finite'):
                try:
                    t_fin = bool(T.is_finite() if callable(T.is_finite) else T.is_finite)
                except Exception:
                    pass
                    
            t_char = False
            if hasattr(T, 'is_characteristic'):
                try:
                    t_char = bool(T.is_characteristic() if callable(T.is_characteristic) else T.is_characteristic)
                except Exception:
                    pass
            t_finite_char = t_fin and t_char
            
        else:
            if isinstance(witness, PermutationGroup):
                t_finite_char = True
            else:
                is_fin = False
                if hasattr(witness, 'order'):
                    try:
                        ord_val = witness.order() if callable(witness.order) else witness.order
                        if ord_val not in (float('inf'), sympy.oo):
                            is_fin = True
                    except Exception:
                        pass
                elif hasattr(witness, 'is_finite'):
                    try:
                        is_fin = bool(witness.is_finite() if callable(witness.is_finite) else witness.is_finite)
                    except Exception:
                        pass
                        
                if is_fin:
                    t_finite_char = True
                else:
                    raise NotImplementedError("Cannot determine torsion subgroup for infinite group")
                    
        neg_q = not t_finite_char
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "H_2: G is finitely generated",
    "¬Q: T is not a finite characteristic subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2