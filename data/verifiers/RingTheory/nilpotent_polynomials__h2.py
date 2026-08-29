import sympy
from sympy import Matrix, eye, zeros
import math
import itertools
import functools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero_elem(e):
    try:
        if hasattr(e, 'is_zero_matrix'):
            return bool(e.is_zero_matrix)
        if hasattr(e, 'is_zero') and e.is_zero is not None:
            return bool(e.is_zero)
        if e == 0:
            return True
    except Exception:
        pass
    return False

def add_elems(a, b):
    if is_zero_elem(a):
        return b
    if is_zero_elem(b):
        return a
    return a + b

def mul_elems(a, b):
    if is_zero_elem(a) or is_zero_elem(b):
        return 0
    return a * b

def is_nilpotent_elem(e, max_k=50):
    if is_zero_elem(e):
        return True
    p = e
    for _ in range(max_k):
        p = mul_elems(p, e)
        if is_zero_elem(p):
            return True
    return False

def poly_mul(A, B):
    if not A or not B:
        return []
    degA = len(A) - 1
    degB = len(B) - 1
    C = [0 for _ in range(degA + degB + 1)]
    for i in range(degA + 1):
        for j in range(degB + 1):
            term = mul_elems(A[i], B[j])
            C[i+j] = add_elems(C[i+j], term)
    return C

def is_poly_zero(A):
    return all(is_zero_elem(a) for a in A)

def is_poly_nilpotent(A, max_k=50):
    if is_poly_zero(A):
        return True
    P = A
    for _ in range(max_k):
        P = poly_mul(P, A)
        if is_poly_zero(P):
            return True
    return False

def conditions(witness):
    if hasattr(witness, 'all_coeffs'):
        try:
            witness = witness.all_coeffs()[::-1]
        except Exception:
            pass
    elif isinstance(witness, dict) and 'coeffs' in witness:
        witness = witness['coeffs']
    elif isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[1], (list, tuple)):
        witness = witness[1]
        
    if not isinstance(witness, (list, tuple)) or len(witness) == 0:
        return [False, False]

    try:
        h1 = True
        for i in range(len(witness)):
            for j in range(len(witness)):
                if mul_elems(witness[i], witness[j]) != mul_elems(witness[j], witness[i]):
                    h1 = False
                    break
            if not h1:
                break
    except Exception:
        h1 = False

    try:
        all_nilpotent = all(is_nilpotent_elem(a) for a in witness)
        poly_nilpotent = is_poly_nilpotent(witness)
        q = (poly_nilpotent == all_nilpotent)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: f is nilpotent iff all coefficients are nilpotent is FALSE"
]

N_HYP = 1
NEG_Q_INDEX = 1