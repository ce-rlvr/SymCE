import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_op(op):
    if isinstance(op, dict):
        def dict_op(a, b):
            if (a, b) in op: return op[(a, b)]
            if (str(a), str(b)) in op: return op[(str(a), str(b))]
            if a in op and b in op[a]: return op[a][b]
            raise KeyError(f"Operation not defined for {a}, {b}")
        return dict_op
    return op

def extract_ring(witness, prefix):
    if isinstance(witness, dict):
        if prefix in witness:
            ring = witness[prefix]
            if isinstance(ring, dict):
                elements, add, mul, zero = ring['elements'], ring['add'], ring['mul'], ring['zero']
            else:
                elements, add, mul, zero = ring.elements, ring.add, ring.mul, ring.zero
        else:
            elements, add, mul, zero = witness[f'{prefix}_elements'], witness[f'{prefix}_add'], witness[f'{prefix}_mul'], witness[f'{prefix}_zero']
    else:
        if hasattr(witness, prefix):
            ring = getattr(witness, prefix)
            if isinstance(ring, dict):
                elements, add, mul, zero = ring['elements'], ring['add'], ring['mul'], ring['zero']
            else:
                elements, add, mul, zero = ring.elements, ring.add, ring.mul, ring.zero
        else:
            elements, add, mul, zero = getattr(witness, f'{prefix}_elements'), getattr(witness, f'{prefix}_add'), getattr(witness, f'{prefix}_mul'), getattr(witness, f'{prefix}_zero')
    
    return list(elements), get_op(add), get_op(mul), zero

def extract_f(witness):
    if isinstance(witness, dict):
        f_raw = witness['f']
    else:
        f_raw = witness.f
    if isinstance(f_raw, dict):
        def dict_f(x):
            if x in f_raw: return f_raw[x]
            if str(x) in f_raw: return f_raw[str(x)]
            raise KeyError(f"f not defined for {x}")
        return dict_f
    return f_raw

def extract_ideal(witness, name):
    if isinstance(witness, dict):
        return list(witness[name])
    return list(getattr(witness, name))

def is_ideal(ring_elements, ring_add, ring_mul, ring_zero, subset):
    if ring_zero not in subset:
        return False
    for a in subset:
        for b in subset:
            if ring_add(a, b) not in subset:
                return False
    for r in ring_elements:
        for a in subset:
            if ring_mul(r, a) not in subset:
                return False
            if ring_mul(a, r) not in subset:
                return False
    for a in subset:
        has_neg = False
        for b in subset:
            if ring_add(a, b) == ring_zero and ring_add(b, a) == ring_zero:
                has_neg = True
                break
        if not has_neg:
            return False
    return True

def are_comaximal(ring_elements, ring_add, I, J):
    sums = []
    for i in I:
        for j in J:
            s = ring_add(i, j)
            if s not in sums:
                sums.append(s)
    for r in ring_elements:
        if r not in sums:
            return False
    return True

def is_surjective_homomorphism(R_elements, R_add, R_mul, S_elements, S_add, S_mul, f):
    image = []
    for r in R_elements:
        fr = f(r)
        if fr not in image:
            image.append(fr)
    for s in S_elements:
        if s not in image:
            return False
    
    for a in R_elements:
        for b in R_elements:
            if f(R_add(a, b)) != S_add(f(a), f(b)):
                return False
            if f(R_mul(a, b)) != S_mul(f(a), f(b)):
                return False
    return True

def conditions(witness):
    try:
        R_elements, R_add, R_mul, R_zero = extract_ring(witness, 'R')
        S_elements, S_add, S_mul, S_zero = extract_ring(witness, 'S')
        f = extract_f(witness)
        I = extract_ideal(witness, 'I')
        J = extract_ideal(witness, 'J')
    except Exception:
        return [False, False, False]

    try:
        h1 = is_surjective_homomorphism(R_elements, R_add, R_mul, S_elements, S_add, S_mul, f)
    except Exception:
        h1 = False

    try:
        is_I_ideal = is_ideal(S_elements, S_add, S_mul, S_zero, I)
        is_J_ideal = is_ideal(S_elements, S_add, S_mul, S_zero, J)
        comax_S = are_comaximal(S_elements, S_add, I, J)
        h2 = is_I_ideal and is_J_ideal and comax_S
    except Exception:
        h2 = False

    try:
        f_inv_I = [r for r in R_elements if f(r) in I]
        f_inv_J = [r for r in R_elements if f(r) in J]
        comax_R = are_comaximal(R_elements, R_add, f_inv_I, f_inv_J)
        neg_q = not comax_R
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a surjective ring homomorphism from R to S",
    "H_2: I and J are comaximal ideals in S",
    "¬Q: The preimage ideals f^{-1}(I) and f^{-1}(J) are not comaximal in R"
]

N_HYP = 2
NEG_Q_INDEX = 2