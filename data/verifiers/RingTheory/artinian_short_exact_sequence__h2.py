import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def get_name(obj):
    if isinstance(obj, str):
        return obj.replace(" ", "")
    if obj == sympy.S.Integers:
        return "Z"
    if obj == sympy.S.Rationals:
        return "Q"
    if obj == sympy.S.Reals:
        return "R"
    if obj == sympy.S.Complexes:
        return "C"
    return str(obj).replace(" ", "")

def get_witness_elements(witness):
    if isinstance(witness, dict):
        R = get_name(witness.get("R"))
        M_prime = get_name(witness.get("M_prime", witness.get("M'")))
        M_double_prime = get_name(witness.get("M_double_prime", witness.get("M''")))
        M = get_name(witness.get("M"))
        return R, M_prime, M_double_prime, M
    elif isinstance(witness, (list, tuple)) and len(witness) == 4:
        return get_name(witness[0]), get_name(witness[1]), get_name(witness[2]), get_name(witness[3])
    return None, None, None, None

def is_ring(R):
    if not isinstance(R, str):
        return False
    return R in ["Z", "Q", "R", "C", "Z/2Z", "Z/3Z", "Z/4Z", "Z/5Z", "Z/6Z", "R[x]", "k[x,y]"]

def is_module(M, R):
    if not isinstance(M, str) or not isinstance(R, str):
        return False
    if M == R:
        return True
    if M in ["{0}", "0"]:
        return True
    
    if R == "Z":
        return M in ["Z", "Q", "R", "C", "Z/2Z", "Z/3Z", "Z/4Z", "Z/5Z", "Z/6Z", "{0}", "0", "ZxZ", "Q/Z", "Z^2", "Z^3"]
    if R in ["Q", "R", "C"]:
        return M in [R, R + "^2", R + "^3", R + "^4", "{0}", "0"]
    if R == "R[x]":
        return M in ["R[x]", "R[x]/(x)", "R[x]/(x^2)", "{0}", "0"]
    if R in ["Z/2Z", "Z/3Z", "Z/4Z", "Z/5Z", "Z/6Z"]:
        return M in [R, R + "x" + R, R + "^2", "{0}", "0"]
    return False

def is_artinian(M, R):
    if not is_module(M, R):
        return False
    if M in ["{0}", "0"]:
        return True
    
    if R == "Z":
        return M in ["Z/2Z", "Z/3Z", "Z/4Z", "Z/5Z", "Z/6Z", "Q/Z"]
    
    if R in ["Q", "R", "C"]:
        return M in [R, R + "^2", R + "^3", R + "^4"]
        
    if R == "R[x]":
        return M in ["R[x]/(x)", "R[x]/(x^2)"]
        
    if R in ["Z/2Z", "Z/3Z", "Z/4Z", "Z/5Z", "Z/6Z"]:
        return M in [R, R + "x" + R, R + "^2"]
        
    return False

def conditions(witness) -> list[bool]:
    R, M_prime, M_double_prime, M = get_witness_elements(witness)
    
    try:
        h1 = is_ring(R)
    except Exception:
        h1 = False
        
    try:
        h2 = is_artinian(M_prime, R)
    except Exception:
        h2 = False
        
    try:
        h3 = is_artinian(M_double_prime, R)
    except Exception:
        h3 = False
        
    try:
        neg_q = is_module(M, R) and not is_artinian(M, R)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: M' is an Artinian R-module",
    "H_3: M'' is an Artinian R-module",
    "¬Q: M is an R-module but not Artinian"
]

N_HYP = 3
NEG_Q_INDEX = 3