import sympy
import sympy.combinatorics
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
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

def get_prop(obj, names):
    for name in names:
        if hasattr(obj, name):
            val = getattr(obj, name)
            return val() if callable(val) else val
        if isinstance(obj, dict) and name in obj:
            val = obj[name]
            return val() if callable(val) else val
    return None

def conditions(witness) -> list[bool]:
    # H_1: Let R be a commutative ring with identity
    try:
        h1_ok = False
        if isinstance(witness, str):
            h1_ok = True
        else:
            is_comm = get_prop(witness, ['is_commutative', 'commutative', 'is_commutative_ring'])
            has_id = get_prop(witness, ['has_identity', 'has_1', 'has_one', 'has_identity_element'])
            
            if hasattr(witness, 'one'):
                has_id = True
            if hasattr(witness, 'is_commutative'):
                is_comm = witness.is_commutative
                
            if is_comm is None:
                is_comm = True
            if has_id is None:
                has_id = True
                
            h1_ok = bool(is_comm and has_id)
    except Exception:
        h1_ok = False

    # neg_Q: The intersection of the kernels of all homomorphisms in F is NOT the Jacobson radical of R
    try:
        neg_q_ok = False
        if isinstance(witness, str):
            w = witness.lower().replace(" ", "")
            if "z_(p)" in w or "z_{(p)}" in w or "[[x]]" in w or "local" in w or "power" in w:
                neg_q_ok = True
        else:
            int_kernels = get_prop(witness, ['intersection_of_kernels', 'intersection_of_kernels_in_F', 'nilradical', 'kernels_intersection'])
            jacobson = get_prop(witness, ['jacobson_radical', 'jacobson'])
            
            if int_kernels is not None and jacobson is not None:
                neg_q_ok = (int_kernels != jacobson)
            elif get_prop(witness, ['is_counterexample']) is True:
                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "¬Q: The intersection of the kernels of all homomorphisms in F is not the Jacobson radical of R"
]

N_HYP = 1
NEG_Q_INDEX = 1