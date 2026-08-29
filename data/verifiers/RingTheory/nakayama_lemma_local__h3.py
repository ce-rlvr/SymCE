import sympy
from sympy import *
import math
import itertools
import functools

# Top-level setup
# Since SymPy does not have standard representations for abstract local rings and modules,
# we provide a mock class that the generator might use. We also support dictionaries
# and string-based descriptions of standard mathematical counterexamples.
class RingModulePair:
    def __init__(self, is_commutative_ring, is_local_ring, mM_equals_M, is_zero_module):
        self.is_commutative_ring = is_commutative_ring
        self.is_local_ring = is_local_ring
        self.mM_equals_M = mM_equals_M
        self.is_zero_module = is_zero_module

# Standard counterexamples provided as named objects
Zp_Q = RingModulePair(True, True, True, False)
k_xx = RingModulePair(True, True, True, False)

def is_known_counterexample(w):
    """
    Checks if the witness string describes a known mathematical counterexample 
    to Nakayama's Lemma without the finitely generated hypothesis.
    """
    s = str(w).lower()
    
    # Exclude finite fields / quotients which are not valid counterexamples here
    if 'z/pz' in s or 'mod p' in s or 'finite field' in s:
        return False
        
    # Counterexample 1: R = Z_{(p)} (local ring of integers), M = Q (rationals)
    if ('q' in s or 'rational' in s) and ('z' in s or 'integer' in s):
        if any(x in s for x in ['local', '_{(', '_(', 'z_']):
            return True
        if 'p' in s and '[' not in s:
            return True
            
    # Counterexample 2: R = k[[x]] (formal power series), M = k((x)) (Laurent series / fraction field)
    if ('[[' in s and '((' in s) or ('series' in s and 'laurent' in s) or ('series' in s and 'fraction' in s):
        return True
        
    # Counterexample 3: General local ring and its fraction field
    if 'local' in s and 'fraction' in s:
        return True
        
    # Counterexample 4: Valuation ring and its quotient field
    if 'valuation' in s and ('fraction' in s or 'quotient' in s):
        return True
        
    # Counterexample 5: Local ring and the injective hull of its residue field
    if 'local' in s and 'injective' in s:
        return True
        
    return False

def check_commutative_ring(w):
    for k in ['is_commutative_ring', 'is_commutative']:
        if isinstance(w, dict) and k in w: return bool(w[k])
        if hasattr(w, k):
            val = getattr(w, k)
            return bool(val()) if callable(val) else bool(val)
    if is_known_counterexample(w): return True
    return False

def check_local_ring(w):
    for k in ['is_local_ring', 'is_local']:
        if isinstance(w, dict) and k in w: return bool(w[k])
        if hasattr(w, k):
            val = getattr(w, k)
            return bool(val()) if callable(val) else bool(val)
    if is_known_counterexample(w): return True
    return False

def check_mM_equals_M(w):
    for k in ['mM_equals_M', 'mM_eq_M', 'is_mM_M', 'mm_equals_m']:
        if isinstance(w, dict) and k in w: return bool(w[k])
        if hasattr(w, k):
            val = getattr(w, k)
            return bool(val()) if callable(val) else bool(val)
    if is_known_counterexample(w): return True
    return False

def check_zero_module(w):
    for k in ['is_zero_module', 'is_zero']:
        if isinstance(w, dict) and k in w: return bool(w[k])
        if hasattr(w, k):
            val = getattr(w, k)
            return bool(val()) if callable(val) else bool(val)
    if is_known_counterexample(w): return False
    return True

def conditions(witness) -> list[bool]:
    try:
        h1 = check_commutative_ring(witness)
    except Exception:
        h1 = False

    try:
        h2 = check_local_ring(witness)
    except Exception:
        h2 = False

    try:
        h3 = check_mM_equals_M(witness)
    except Exception:
        h3 = False

    try:
        q = check_zero_module(witness)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is a local ring with maximal ideal m",
    "H_3: mM = M",
    "¬Q: M is not the zero module"
]

N_HYP = 3
NEG_Q_INDEX = 3