import math
import itertools
import functools
import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    h1_ok = False
    try:
        if hasattr(witness, 'is_boolean_ring_with_identity'):
            val = witness.is_boolean_ring_with_identity
            h1_ok = bool(val()) if callable(val) else bool(val)
        else:
            is_bool = False
            has_id = False
            
            if hasattr(witness, 'is_boolean'):
                val = witness.is_boolean
                is_bool = bool(val()) if callable(val) else bool(val)
            elif hasattr(witness, 'is_Boolean'):
                val = witness.is_Boolean
                is_bool = bool(val()) if callable(val) else bool(val)
                
            if hasattr(witness, 'has_identity'):
                val = witness.has_identity
                has_id = bool(val()) if callable(val) else bool(val)
                
            if is_bool and has_id:
                h1_ok = True
            elif hasattr(witness, 'elements') and hasattr(witness, 'add') and hasattr(witness, 'mul'):
                elements = list(witness.elements)
                if elements:
                    is_bool = True
                    for x in elements:
                        if witness.mul(x, x) != x:
                            is_bool = False
                            break
                    
                    has_id = False
                    for o in elements:
                        if all(witness.mul(o, x) == x and witness.mul(x, o) == x for x in elements):
                            has_id = True
                            break
                    
                    h1_ok = is_bool and has_id
    except Exception:
        h1_ok = False

    neg_q_ok = False
    try:
        if hasattr(witness, 'is_spec_compact_hausdorff'):
            val = witness.is_spec_compact_hausdorff
            neg_q_ok = not (bool(val()) if callable(val) else bool(val))
        elif hasattr(witness, 'is_spec_compact') and hasattr(witness, 'is_spec_hausdorff'):
            val_c = witness.is_spec_compact
            val_h = witness.is_spec_hausdorff
            c = bool(val_c()) if callable(val_c) else bool(val_c)
            h = bool(val_h()) if callable(val_h) else bool(val_h)
            neg_q_ok = not (c and h)
        elif hasattr(witness, 'elements'):
            # Finite rings always have a compact Hausdorff Spec
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring with identity",
    "¬Q: Spec(R) is not a compact Hausdorff space"
]

N_HYP = 1
NEG_Q_INDEX = 1