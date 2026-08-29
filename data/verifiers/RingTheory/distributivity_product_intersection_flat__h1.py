import sympy as sp
import z3
import math
import itertools
import functools

# Top-level setup
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def get_basis(matrices):
    if not matrices:
        return []
    shape = matrices[0].shape
    vecs = [m.vec() for m in matrices]
    M = sp.Matrix.hstack(*vecs)
    _, pivots = M.rref()
    return [matrices[i] for i in pivots]

def is_subspace(A, B):
    if not A: return True
    A_mat = sp.Matrix.hstack(*[m.vec() for m in A])
    if A_mat.is_zero_matrix: return True
    if not B: return False
    B_mat = sp.Matrix.hstack(*[m.vec() for m in B])
    rank_B = B_mat.rank()
    for a in A:
        if B_mat.row_join(a.vec()).rank() > rank_B:
            return False
    return True

def intersection(A, B):
    if not A or not B: return []
    A_mat = sp.Matrix.hstack(*[m.vec() for m in A])
    B_mat = sp.Matrix.hstack(*[m.vec() for m in B])
    M = A_mat.row_join(-B_mat)
    nullspace = M.nullspace()
    res = []
    shape = A[0].shape
    for vec in nullspace:
        x = vec[:len(A), 0]
        v = A_mat * x
        res.append(v.reshape(shape[0], shape[1]))
    return get_basis(res)

def multiply(A, B):
    if not A or not B: return []
    res = []
    for a in A:
        for b in B:
            res.append(a * b)
    return get_basis(res)

def is_ideal(A, R):
    if not is_subspace(A, R): return False
    for a in A:
        for r in R:
            if not is_subspace([a*r], A): return False
            if not is_subspace([r*a], A): return False
    return True

def is_ring(R):
    if not R: return False
    for a in R:
        for b in R:
            if not is_subspace([a*b], R): return False
            
    shape = R[0].shape
    I_mat = sp.eye(shape[0])
    if is_subspace([I_mat], R): return True
    
    n = len(R)
    S2 = shape[0] * shape[1]
    eqs = []
    rhs = []
    for i in range(n):
        for row in range(S2):
            eq = [0] * n
            for j in range(n):
                eq[j] = (R[j] * R[i]).vec()[row]
            if any(eq) or R[i].vec()[row] != 0:
                eqs.append(eq)
                rhs.append(R[i].vec()[row])
            
    if not eqs:
        return False
        
    A = sp.Matrix(eqs)
    B = sp.Matrix(rhs)
    try:
        sol, _ = A.gauss_jordan_solve(B)
        E = sp.zeros(shape[0], shape[1])
        for j in range(n):
            E += sol[j] * R[j]
        for i in range(n):
            if E * R[i] != R[i] or R[i] * E != R[i]:
                return False
        return True
    except Exception:
        return False

def is_projective_module(R_basis, M_basis, side='left'):
    if not M_basis: return True
    if not R_basis: return False
    
    n = len(R_basis)
    d = len(M_basis)
    
    R_mat = sp.Matrix.hstack(*[m.vec() for m in R_basis])
    M_mat = sp.Matrix.hstack(*[m.vec() for m in M_basis])
    
    D = {}
    for p in range(n):
        for q in range(n):
            prod = R_basis[p] * R_basis[q]
            try:
                sol, _ = R_mat.gauss_jordan_solve(prod.vec())
                D[(p, q)] = sol
            except Exception:
                return False

    C = {}
    for p in range(n):
        for j in range(d):
            if side == 'left':
                prod = R_basis[p] * M_basis[j]
            else:
                prod = M_basis[j] * R_basis[p]
            try:
                sol, _ = M_mat.gauss_jordan_solve(prod.vec())
                C[(p, j)] = sol
            except Exception:
                return False

    num_vars = d * d * n
    eqs = []
    rhs = []
    
    for i in range(d):
        for j in range(d):
            for p in range(n):
                for k in range(n):
                    eq = [0] * num_vars
                    for l in range(d):
                        idx = i * (d * n) + l * n + k
                        eq[idx] += C[(p, j)][l]
                    for q in range(n):
                        idx = i * (d * n) + j * n + q
                        if side == 'left':
                            eq[idx] -= D[(p, q)][k]
                        else:
                            eq[idx] -= D[(q, p)][k]
                    
                    if any(eq):
                        eqs.append(eq)
                        rhs.append(0)
                        
    for j in range(d):
        for l in range(d):
            eq = [0] * num_vars
            for i in range(d):
                for k in range(n):
                    idx = i * (d * n) + j * n + k
                    eq[idx] += C[(k, i)][l]
            
            if any(eq) or (1 if j == l else 0) != 0:
                eqs.append(eq)
                rhs.append(1 if j == l else 0)
                
    if not eqs:
        return True
        
    A = sp.Matrix(eqs)
    B = sp.Matrix(rhs)
    
    try:
        A.gauss_jordan_solve(B)
        return True
    except ValueError:
        return False
    except Exception:
        return A.rank() == A.row_join(B).rank()

def conditions(witness):
    try:
        R_raw, I_raw, J_raw, K_raw = witness
        R = get_basis(R_raw)
        I = get_basis(I_raw)
        J = get_basis(J_raw)
        K = get_basis(K_raw)
    except Exception:
        return [False, False, False, False]

    try:
        H1 = bool(is_ring(R) and is_ideal(I, R) and (is_projective_module(R, I, 'left') or is_projective_module(R, I, 'right')))
    except Exception:
        H1 = False

    try:
        H2 = bool(is_ideal(J, R))
    except Exception:
        H2 = False

    try:
        H3 = bool(is_ideal(K, R))
    except Exception:
        H3 = False

    try:
        J_cap_K = intersection(J, K)
        I_JcapK = multiply(I, J_cap_K)
        
        IJ = multiply(I, J)
        IK = multiply(I, K)
        IJ_cap_IK = intersection(IJ, IK)
        
        eq = is_subspace(I_JcapK, IJ_cap_IK) and is_subspace(IJ_cap_IK, I_JcapK)
        neg_Q = not eq
    except Exception:
        neg_Q = False

    return [H1, H2, H3, neg_Q]

CONDITION_LABELS = [
    "H_1: I is an ideal of R that is flat as an R-module",
    "H_2: J is an ideal of R",
    "H_3: K is an ideal of R",
    "¬Q: I(J \\cap K) is not equal to IJ \\cap IK"
]

N_HYP = 3
NEG_Q_INDEX = 3