import sympy
from sympy import Matrix, eye, zeros, Rational
from sympy.abc import x
import itertools
import functools
import math

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_vectors(basis):
    return [list(m) for m in basis]

def span_contains(basis_B, basis_A):
    if not basis_A: 
        return True
    if not basis_B:
        return all(all(val == 0 for val in list(m)) for m in basis_A)
    vecs_B = get_vectors(basis_B)
    vecs_A = get_vectors(basis_A)
    mat_B = Matrix(vecs_B)
    mat_BA = Matrix(vecs_B + vecs_A)
    return mat_B.rank() == mat_BA.rank()

def is_closed_under_mult(basis):
    if not basis: 
        return True
    prods = []
    for a in basis:
        for b in basis:
            prods.append(a * b)
    return span_contains(basis, prods)

def has_identity(R_basis):
    if not R_basis: 
        return False
    n = R_basis[0].shape[0]
    I = eye(n)
    return span_contains(R_basis, [I])

def is_ideal(R_basis, I_basis):
    if not span_contains(R_basis, I_basis):
        return False
    prods = []
    for r in R_basis:
        for i in I_basis:
            prods.append(r * i)
            prods.append(i * r)
    return span_contains(I_basis, prods)

def is_nilpotent(I_basis, max_k):
    if not I_basis: 
        return True
    n = I_basis[0].shape[0]
    current_span = I_basis
    for _ in range(max_k):
        if all(all(val == 0 for val in list(m)) for m in current_span):
            return True
        next_span = []
        for a in current_span:
            for b in I_basis:
                next_span.append(a * b)
        
        if not next_span:
            return True
            
        vecs = get_vectors(next_span)
        mat = Matrix(vecs)
        rref_mat, _ = mat.rref()
        
        current_span = []
        for i in range(rref_mat.shape[0]):
            row = rref_mat.row(i)
            if not all(val == 0 for val in row):
                current_span.append(Matrix(n, n, list(row)))
                
    return all(all(val == 0 for val in list(m)) for m in current_span)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "In a right Artinian ring, every ideal is nilpotent."
    (The true theorem requires the ideal to be a nil ideal).
    
    Witness format: (R_basis, I_basis)
    where R_basis and I_basis are lists of sympy.Matrix objects of the same shape.
    """
    try:
        R_basis, I_basis = witness
    except Exception:
        return [False, False]
        
    # H_1: R is a right Artinian ring (and I is an ideal of R)
    try:
        if not R_basis:
            h1 = False
        else:
            # A finite-dimensional algebra over a field is right Artinian.
            is_ring = is_closed_under_mult(R_basis) and has_identity(R_basis)
            is_id = is_ideal(R_basis, I_basis)
            h1 = bool(is_ring and is_id)
    except Exception:
        h1 = False
        
    # neg_Q: I is not a nilpotent ideal
    try:
        if not I_basis:
            neg_q = False
        else:
            dim_R = len(R_basis)
            is_id = is_ideal(R_basis, I_basis)
            is_nil = is_nilpotent(I_basis, dim_R + 1)
            neg_q = bool(not (is_id and is_nil))
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a right Artinian ring",
    "¬Q: I is not a nilpotent ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1