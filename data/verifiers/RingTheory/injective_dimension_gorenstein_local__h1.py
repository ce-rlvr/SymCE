import math
import itertools
import functools
import sympy
from sympy import eye, zeros, S
from sympy.abc import *
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def get_bool_prop(witness, *names):
    if isinstance(witness, dict):
        for name in names:
            if name in witness:
                return bool(witness[name])
    for name in names:
        if hasattr(witness, name):
            return bool(getattr(witness, name))
    try:
        for name in names:
            if name in witness:
                return bool(witness[name])
    except Exception:
        pass
    return False

def get_val_prop(witness, *names):
    if isinstance(witness, dict):
        for name in names:
            if name in witness:
                return witness[name]
    for name in names:
        if hasattr(witness, name):
            return getattr(witness, name)
    try:
        for name in names:
            if name in witness:
                return witness[name]
    except Exception:
        pass
    return None

def is_fin(val):
    if val is None:
        return False
    if val == sympy.oo or val == math.inf:
        return False
    if isinstance(val, str):
        return val.lower() not in ['inf', 'infinity', 'infty', 'infinite', 'oo']
    try:
        return not math.isinf(float(val))
    except Exception:
        return True

def conditions(witness) -> list[bool]:
    try:
        h1 = get_bool_prop(witness, "is_Gorenstein", "is_gorenstein", "Gorenstein")
    except Exception:
        h1 = False

    try:
        inj_dim = get_val_prop(witness, "injective_dimension", "inj_dim", "injective_dim")
        krull_dim = get_val_prop(witness, "Krull_dimension", "krull_dim", "krull_dimension")
        
        if inj_dim is None or krull_dim is None:
            neg_q = False
        else:
            conclusion = is_fin(inj_dim) and (inj_dim == krull_dim)
            neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Gorenstein ring",
    "¬Q: The injective dimension of R is infinite or not equal to its Krull dimension"
]

N_HYP = 1
NEG_Q_INDEX = 1