import sympy
from sympy import *
import math
import itertools
import functools

# Top-level setup for fields and algebraic closures
QQ = "QQ"
RR = "RR"
CC = "CC"
QQ_bar = "QQ_bar"
F2 = "F2"
F2_bar = "F2_bar"
F3 = "F3"
F3_bar = "F3_bar"

KNOWN_FIELDS = {"QQ", "RR", "CC", "QQ_bar", "F2", "F2_bar", "F3", "F3_bar"}

CLOSURES = {
    "QQ": "QQ_bar",
    "RR": "CC",
    "CC": "CC",
    "QQ_bar": "QQ_bar",
    "F2": "F2_bar",
    "F2_bar": "F2_bar",
    "F3": "F3_bar",
    "F3_bar": "F3_bar"
}

SUBFIELDS = {
    "QQ": {"QQ"},
    "RR": {"QQ", "RR"},
    "CC": {"QQ", "RR", "CC"},
    "QQ_bar": {"QQ", "QQ_bar"},
    "F2": {"F2"},
    "F2_bar": {"F2", "F2_bar"},
    "F3": {"F3"},
    "F3_bar": {"F3", "F3_bar"}
}

def to_field_str(X):
    if isinstance(X, str):
        return X
    if X == sympy.S.Reals:
        return "RR"
    if X == sympy.S.Complexes:
        return "CC"
    if X == sympy.S.Rationals:
        return "QQ"
    return str(X)

def is_field(F):
    return to_field_str(F) in KNOWN_FIELDS

def is_alg_closure(K, F):
    return CLOSURES.get(to_field_str(F)) == to_field_str(K)

def is_isomorphic_fixing(K1, K2, F):
    k1_str = to_field_str(K1)
    k2_str = to_field_str(K2)
    f_str = to_field_str(F)
    
    if k1_str != k2_str:
        return False
    if f_str not in SUBFIELDS.get(k1_str, set()):
        return False
    # In our simplified universe, if K1 == K2 and F is a subfield, 
    # the identity map is an isomorphism fixing F.
    return True

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False]
        F, K1, K2 = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = is_field(F)
    except Exception:
        h1 = False

    try:
        h2 = is_alg_closure(K2, F)
    except Exception:
        h2 = False

    try:
        neg_q = not is_isomorphic_fixing(K1, K2, F)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: K2 is an algebraic closure of F",
    "¬Q: There does not exist a field isomorphism from K1 to K2 fixing F"
]

N_HYP = 2
NEG_Q_INDEX = 2