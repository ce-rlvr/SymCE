import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros
import z3
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: phi is a surjective group homomorphism",
    "¬Q: phi is not an isomorphism"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1 = False
    neg_q = False
    
    # Try dictionary first
    if isinstance(witness, dict):
        try:
            is_surj = witness.get('is_surjective', False)
            is_hom = witness.get('is_homomorphism', witness.get('is_group_homomorphism', False))
            h1 = bool(is_surj and is_hom)
            
            if 'is_isomorphism' in witness:
                is_iso = witness['is_isomorphism']
            elif 'is_injective' in witness:
                is_iso = is_surj and witness['is_injective']
            else:
                is_iso = True
            neg_q = not bool(is_iso)
            return [h1, neg_q]
        except Exception:
            pass

    # Try tuple (G, phi)
    obj_to_check = witness
    if isinstance(witness, tuple) and len(witness) == 2:
        obj_to_check = witness[1]
        
    if isinstance(obj_to_check, dict):
        try:
            is_surj = obj_to_check.get('is_surjective', False)
            is_hom = obj_to_check.get('is_homomorphism', obj_to_check.get('is_group_homomorphism', False))
            h1 = bool(is_surj and is_hom)
            
            if 'is_isomorphism' in obj_to_check:
                is_iso = obj_to_check['is_isomorphism']
            elif 'is_injective' in obj_to_check:
                is_iso = is_surj and obj_to_check['is_injective']
            else:
                is_iso = True
            neg_q = not bool(is_iso)
            return [h1, neg_q]
        except Exception:
            pass

    # Try object properties (duck-typing for custom classes or SymPy Homomorphism)
    try:
        is_surj = False
        if hasattr(obj_to_check, 'is_surjective'):
            val = obj_to_check.is_surjective
            is_surj = val() if callable(val) else val
            
        is_hom = False
        if hasattr(obj_to_check, 'is_homomorphism'):
            val = obj_to_check.is_homomorphism
            is_hom = val() if callable(val) else val
        elif type(obj_to_check).__name__ == 'Homomorphism':
            is_hom = True
        elif hasattr(obj_to_check, 'is_group_homomorphism'):
            val = obj_to_check.is_group_homomorphism
            is_hom = val() if callable(val) else val
            
        h1 = bool(is_surj and is_hom)
        
        is_iso = True
        if hasattr(obj_to_check, 'is_isomorphism'):
            val = obj_to_check.is_isomorphism
            is_iso = val() if callable(val) else val
        elif hasattr(obj_to_check, 'is_injective'):
            val = obj_to_check.is_injective
            is_inj = val() if callable(val) else val
            is_iso = bool(is_surj and is_inj)
            
        neg_q = not bool(is_iso)
    except Exception:
        pass
        
    return [h1, neg_q]