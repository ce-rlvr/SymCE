import sympy
from sympy import *
import math
import itertools
import functools

# Top-level setup: named object bindings
ZZ = "ZZ"
Z = "ZZ"
QQ = "QQ"
Q = "QQ"
RR = "RR"
CC = "CC"
Z2 = "Z2"
Z3 = "Z3"
Z4 = "Z4"
Z6 = "Z6"
QQ_x = "QQ[x]"
QQ_frac_x = "QQ(x)"
ZZ_x = "ZZ[x]"

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    try:
        h1 = R in ["ZZ", "QQ", "RR", "CC", "QQ[x]", "ZZ[x]", "Z2", "Z3", "Z4", "Z6"]
    except Exception:
        h1 = False
        
    try:
        flat_pairs = {
            ("ZZ", "QQ"), ("ZZ", "ZZ"), ("QQ", "QQ"), ("RR", "RR"), ("CC", "CC"),
            ("QQ[x]", "QQ(x)"), ("QQ[x]", "QQ[x]"), ("ZZ[x]", "ZZ[x]"),
            ("Z6", "Z2"), ("Z6", "Z3"), ("Z2", "Z2"), ("Z3", "Z3"), ("Z4", "Z4"),
            ("ZZ", "RR"), ("ZZ", "CC"), ("ZZ", "QQ(x)")
        }
        not_flat_pairs = {
            ("ZZ", "Z2"), ("ZZ", "Z3"), ("ZZ", "Z4"), ("ZZ", "Z6"),
            ("Z4", "Z2"), ("ZZ[x]", "Z2"), ("QQ[x]", "QQ")
        }
        if (R, M) in flat_pairs:
            is_flat = True
        elif (R, M) in not_flat_pairs:
            is_flat = False
        else:
            is_flat = None
            
        proj_pairs = {
            ("ZZ", "ZZ"), ("QQ", "QQ"), ("RR", "RR"), ("CC", "CC"),
            ("QQ[x]", "QQ[x]"), ("ZZ[x]", "ZZ[x]"),
            ("Z6", "Z2"), ("Z6", "Z3"), ("Z2", "Z2"), ("Z3", "Z3"), ("Z4", "Z4")
        }
        not_proj_pairs = {
            ("ZZ", "QQ"), ("ZZ", "Z2"), ("ZZ", "Z3"), ("ZZ", "Z4"), ("ZZ", "Z6"),
            ("Z4", "Z2"), ("QQ[x]", "QQ(x)"), ("ZZ[x]", "Z2"), ("QQ[x]", "QQ"),
            ("ZZ", "RR"), ("ZZ", "CC"), ("ZZ", "QQ(x)")
        }
        if (R, M) in proj_pairs:
            is_proj = True
        elif (R, M) in not_proj_pairs:
            is_proj = False
        else:
            is_proj = None
            
        if is_flat is not None and is_proj is not None:
            neg_q = (is_flat != is_proj)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "¬Q: It is not the case that M is flat iff M is projective"
]

N_HYP = 1
NEG_Q_INDEX = 1