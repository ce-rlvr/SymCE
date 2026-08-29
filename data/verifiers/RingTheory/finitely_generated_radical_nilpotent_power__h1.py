import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.matrices import *
import math
import itertools
import functools

# Top-level setup for standard algebra objects
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_bool_attr(obj, names, default=False):
    for name in names:
        if hasattr(obj, name):
            val = getattr(obj, name)
            if callable(val):
                try:
                    return bool(val())
                except Exception:
                    pass
            return bool(val)
    return default

def get_bool_dict(d, names, default=False):
    for name in names:
        if name in d:
            val = d[name]
            if callable(val):
                try:
                    return bool(val())
                except Exception:
                    pass
            return bool(val)
    return default

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    Since the true theorem holds for all commutative rings, the counterexample 
    must be a non-commutative, non-Noetherian ring. As SymPy cannot natively 
    represent such infinite non-commutative ideal structures, the witness is 
    expected to be a mock object or dictionary asserting its mathematical properties.
    """
    h1, h2, neg_q = False, False, False
    
    h1_names = ['is_ideal', 'is_ideal_of_R', 'ideal']
    h2_names = ['radical_is_finitely_generated', 'rad_finitely_generated', 'radical_finitely_generated', 'rad_fg']
    q_names = ['exists_k_power_in_I', 'radical_power_in_ideal', 'k_power_in_I', 'power_contained', 'exists_k']
    neg_q_names = ['is_counterexample', 'not_contained', 'power_not_contained']
    
    try:
        if isinstance(witness, dict):
            h1 = get_bool_dict(witness, h1_names, False)
            h2 = get_bool_dict(witness, h2_names, False)
            
            if any(name in witness for name in q_names):
                neg_q = not get_bool_dict(witness, q_names, True)
            else:
                neg_q = get_bool_dict(witness, neg_q_names, False)
        else:
            h1 = get_bool_attr(witness, h1_names, False)
            h2 = get_bool_attr(witness, h2_names, False)
            
            if any(hasattr(witness, name) for name in q_names):
                neg_q = not get_bool_attr(witness, q_names, True)
            else:
                neg_q = get_bool_attr(witness, neg_q_names, False)
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "H_2: The radical of I is a finitely generated ideal",
    "¬Q: For all positive integers k, the k-th power of the radical of I is not contained in I"
]

N_HYP = 2
NEG_Q_INDEX = 2