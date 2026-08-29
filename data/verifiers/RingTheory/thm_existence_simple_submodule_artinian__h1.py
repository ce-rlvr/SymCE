import sympy
from sympy import S
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference.
Z = S.Integers
Q = S.Rationals
R = S.Reals
C = S.Complexes
Z_x = "Z[x]"
Q_x = "Q[x]"
R_x = "R[x]"
C_x = "C[x]"

def is_nonzero_module(w):
    if isinstance(w, tuple) and len(w) == 2:
        M, R_ring = w
    else:
        M = w
    
    M_str = str(M)
    
    # Check against known non-zero module representations
    if M_str in ["Z", "Q", "R", "C", "Z[x]", "Q[x]", "R[x]", "C[x]", "Integers", "Rationals", "Reals", "Complexes"]:
        return True
        
    # Check for empty sets or trivial zero modules
    if hasattr(M, "is_empty") and M.is_empty:
        return False
    if M == sympy.FiniteSet(0):
        return False
        
    # Default to True for any non-empty string or object provided as a witness
    if isinstance(M, str) and len(M) > 0:
        return True
        
    return True

def has_simple_submodule(w):
    if isinstance(w, tuple) and len(w) == 2:
        M, R_ring = w
    else:
        M = w
        R_ring = w
        
    M_str = str(M)
    R_str = str(R_ring)
    
    fields = ["Q", "R", "C", "Rationals", "Reals", "Complexes"]
    
    # Fields over themselves are simple modules, hence contain a simple submodule
    if M_str in fields and R_str in fields:
        return True
        
    # Z over Z has no minimal non-zero ideals, hence no simple submodules
    if M_str in ["Z", "Integers"] and R_str in ["Z", "Integers"]:
        return False
        
    # Q, R, C over Z have no minimal non-zero subgroups, hence no simple submodules
    if M_str in fields and R_str in ["Z", "Integers"]:
        return False
        
    # Polynomial rings over themselves have no minimal non-zero ideals
    poly_rings = ["Z[x]", "Q[x]", "R[x]", "C[x]"]
    if M_str in poly_rings and R_str == M_str:
        return False
        
    # Polynomial rings over Z or themselves
    if "x" in M_str and ("Z" in R_str or "Integers" in R_str or R_str == M_str):
        return False
        
    # Default to True (meaning it fails to be a counterexample) to be safe
    return True

def conditions(witness) -> list[bool]:
    try:
        h1 = bool(is_nonzero_module(witness))
    except Exception:
        h1 = False
        
    try:
        # The conclusion is "M contains a simple R-submodule"
        # We want neg_Q to be True when the conclusion FAILS.
        neg_q = not has_simple_submodule(witness)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: M is a non-zero right R-module",
    "¬Q: M does not contain a simple R-submodule"
]

N_HYP = 1
NEG_Q_INDEX = 1