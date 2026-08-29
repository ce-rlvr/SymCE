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

# Top-level setup for standard algebra objects
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

def get_prop(obj, *names):
    """Helper to extract properties from mock objects or dictionaries."""
    for name in names:
        if isinstance(obj, dict) and name in obj:
            val = obj[name]
            return val() if callable(val) else val
        if hasattr(obj, name):
            val = getattr(obj, name)
            return val() if callable(val) else val
    return None

def h1(witness):
    """
    Check if R is a commutative local Noetherian ring.
    """
    R = witness[0] if isinstance(witness, tuple) else witness
    is_comm = get_prop(R, 'is_commutative', 'commutative')
    is_loc = get_prop(R, 'is_local', 'local')
    is_noeth = get_prop(R, 'is_noetherian', 'noetherian')
    
    return bool(is_comm and is_loc and is_noeth)

def neg_q(witness):
    """
    Check if the Krull dimension of R_hat is NOT equal to the Krull dimension of R.
    """
    R = witness[0] if isinstance(witness, tuple) else witness
    dim_R = get_prop(R, 'krull_dimension', 'dim', 'dimension')
    
    # Try to get completion from R
    completion = get_prop(R, 'completion', 'hat')
    if completion is not None:
        dim_R_hat = get_prop(completion, 'krull_dimension', 'dim', 'dimension')
    else:
        dim_R_hat = get_prop(R, 'completion_krull_dimension', 'dim_hat', 'completion_dim')
        
    # If not found in R, maybe witness[1] is R_hat
    if dim_R_hat is None and isinstance(witness, tuple) and len(witness) >= 2:
        R_hat = witness[1]
        dim_R_hat = get_prop(R_hat, 'krull_dimension', 'dim', 'dimension')
        
    if dim_R is None or dim_R_hat is None:
        return False
        
    return dim_R != dim_R_hat

def conditions(witness) -> list[bool]:
    try:
        h1_ok = h1(witness)
    except Exception:
        h1_ok = False
        
    try:
        neg_q_ok = neg_q(witness)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative local Noetherian ring with maximal ideal m",
    "¬Q: The Krull dimension of R_hat is not equal to the Krull dimension of R"
]

N_HYP = 1
NEG_Q_INDEX = 1