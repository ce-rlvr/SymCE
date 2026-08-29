import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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
    "H_1: f: R -> S is a flat local homomorphism",
    "H_2: S is a regular local ring",
    "¬Q: R is not a regular local ring"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_bool_prop(obj, props):
    if isinstance(obj, dict):
        for p in props:
            if p in obj:
                v = obj[p]
                return bool(v() if callable(v) else v)
    else:
        for p in props:
            if hasattr(obj, p):
                v = getattr(obj, p)
                return bool(v() if callable(v) else v)
    return None

def conditions(witness) -> list[bool]:
    h1, h2, neg_q = False, False, False
    
    R, S, f = witness, witness, witness
    if isinstance(witness, tuple) and len(witness) == 3:
        R, S, f = witness
    elif isinstance(witness, dict) and 'R' in witness and 'S' in witness and 'f' in witness:
        R, S, f = witness['R'], witness['S'], witness['f']
    elif hasattr(witness, 'domain') and hasattr(witness, 'codomain'):
        R = witness.domain
        S = witness.codomain
        f = witness

    try:
        val = get_bool_prop(f, ['is_flat_local_homomorphism', 'f_is_flat_local_homomorphism'])
        if val is None:
            val = get_bool_prop(witness, ['is_flat_local_homomorphism', 'f_is_flat_local_homomorphism'])
        h1 = bool(val)
    except Exception:
        h1 = False

    try:
        val = get_bool_prop(S, ['is_regular_local_ring', 'S_is_regular_local_ring'])
        if val is None:
            val = get_bool_prop(witness, ['S_is_regular_local_ring'])
        h2 = bool(val)
    except Exception:
        h2 = False

    try:
        val = get_bool_prop(R, ['is_regular_local_ring', 'R_is_regular_local_ring'])
        if val is None:
            val = get_bool_prop(witness, ['R_is_regular_local_ring'])
        if val is not None:
            neg_q = not bool(val)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]