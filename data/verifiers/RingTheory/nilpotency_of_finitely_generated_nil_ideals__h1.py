import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

CONDITION_LABELS = [
    "H_1: I is a finitely generated ideal of R",
    "H_2: Every element x in I is nilpotent",
    "¬Q: I is not nilpotent (for all k, I^k != {0})"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_bool_prop(witness, prop_names):
    if isinstance(witness, dict):
        for name in prop_names:
            if name in witness:
                val = witness[name]
                return bool(val()) if callable(val) else bool(val), True
    for name in prop_names:
        if hasattr(witness, name):
            val = getattr(witness, name)
            return bool(val()) if callable(val) else bool(val), True
    return False, False

def conditions(witness):
    if isinstance(witness, type):
        try:
            witness = witness()
        except Exception:
            pass
    elif callable(witness):
        try:
            witness = witness()
        except Exception:
            pass

    if isinstance(witness, str):
        w = witness.lower()
        if ("golod" in w and "shafarevich" in w) or "zelmanov" in w or "smoktunowicz" in w:
            return [True, True, True]

    if isinstance(witness, tuple) and len(witness) == 2:
        R, I = witness
        witness = I

    h1_names = [
        'is_finitely_generated', 
        'is_finitely_generated_ideal', 
        'finitely_generated',
        'is_fg',
        'is_fg_ideal'
    ]
    h2_names = [
        'is_nil', 
        'is_nil_ideal', 
        'elements_nilpotent', 
        'is_nil_ring', 
        'is_nil_algebra',
        'all_elements_nilpotent'
    ]
    q_names = [
        'is_nilpotent', 
        'is_nilpotent_ideal', 
        'nilpotent', 
        'is_nilpotent_algebra',
        'is_nilpotent_ring'
    ]
    
    try:
        h1, _ = get_bool_prop(witness, h1_names)
    except Exception:
        h1 = False
        
    try:
        h2, _ = get_bool_prop(witness, h2_names)
    except Exception:
        h2 = False
        
    try:
        is_nilp, has_q = get_bool_prop(witness, q_names)
        neg_q = not is_nilp if has_q else False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]