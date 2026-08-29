import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import sympy.combinatorics.permutations
import sympy.matrices
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
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

def get_bool_prop(obj, names):
    """Helper to extract boolean properties from various witness formats."""
    if isinstance(obj, dict):
        for name in names:
            if name in obj:
                v = obj[name]
                return bool(v() if callable(v) else v)
    
    for name in names:
        if hasattr(obj, name):
            try:
                v = getattr(obj, name)
                return bool(v() if callable(v) else v)
            except Exception:
                pass
                
    if hasattr(obj, 'get') and callable(getattr(obj, 'get')):
        for name in names:
            try:
                v = obj.get(name)
                if v is not None:
                    return bool(v() if callable(v) else v)
            except Exception:
                pass
                
    if callable(obj):
        for name in names:
            try:
                v = obj(name)
                if isinstance(v, bool):
                    return v
            except Exception:
                pass
                
    return False

def check_h1(witness):
    if isinstance(witness, tuple) and len(witness) == 2:
        R, I = witness
        if hasattr(R, 'is_commutative'):
            try:
                return bool(R.is_commutative)
            except Exception:
                pass
    names = [
        'is_commutative_ring',
        'is_commutative',
        'commutative_ring',
        'R_is_commutative_ring',
        'h1'
    ]
    return get_bool_prop(witness, names)

def check_h2(witness):
    if isinstance(witness, tuple) and len(witness) == 2:
        R, I = witness
        names = [
            'radical_is_finitely_generated_ideal',
            'rad_I_finitely_generated',
            'radical_finitely_generated',
            'is_radical_finitely_generated_ideal',
            'h2'
        ]
        if get_bool_prop(I, names):
            return True
    names = [
        'radical_is_finitely_generated_ideal',
        'rad_I_finitely_generated',
        'radical_finitely_generated',
        'is_radical_finitely_generated_ideal',
        'h2'
    ]
    return get_bool_prop(witness, names)

def check_neg_q(witness):
    if isinstance(witness, tuple) and len(witness) == 2:
        R, I = witness
        names = [
            'radical_power_not_contained',
            'neg_q',
            'conclusion_fails',
            'power_of_radical_not_contained'
        ]
        if get_bool_prop(I, names):
            return True
        pos_names = [
            'radical_power_contained',
            'exists_k_rad_I_k_in_I',
            'power_of_radical_contained',
            'q'
        ]
        if get_bool_prop(I, pos_names):
            return False
            
    names = [
        'radical_power_not_contained',
        'neg_q',
        'conclusion_fails',
        'power_of_radical_not_contained'
    ]
    if get_bool_prop(witness, names):
        return True
    
    pos_names = [
        'radical_power_contained',
        'exists_k_rad_I_k_in_I',
        'power_of_radical_contained',
        'q'
    ]
    if get_bool_prop(witness, pos_names):
        return False
        
    return False

def conditions(witness) -> list[bool]:
    try:
        h1 = check_h1(witness)
    except Exception:
        h1 = False

    try:
        h2 = check_h2(witness)
    except Exception:
        h2 = False

    try:
        neg_q = check_neg_q(witness)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: The radical of I is a finitely generated ideal",
    "¬Q: For all positive integers k, the k-th power of the radical of I is not contained in I"
]

N_HYP = 2
NEG_Q_INDEX = 2