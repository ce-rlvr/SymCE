import sympy
import sympy as sp
from sympy import Matrix, eye, zeros, Rational, Integer
from sympy.abc import x, y, z
import math
import itertools
import functools

# Standard bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: V and W are vector spaces over a field F",
    "H_2: U is a finite-dimensional subspace of V",
    "¬Q: The dimension of the image T(U) is not equal to dim(U) - dim(U ∩ ker(T))"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_format_A(witness):
    if isinstance(witness, tuple) and len(witness) == 2:
        q, T_dict = witness
        if isinstance(q, int) and isinstance(T_dict, dict):
            return q, T_dict
    return None, None

def wrap_T_func(T_obj):
    if isinstance(T_obj, sp.Matrix):
        return lambda v: T_obj * v
    elif callable(T_obj):
        def wrapped(v):
            res = T_obj(v)
            if isinstance(res, (list, tuple)):
                return sp.Matrix(list(res))
            if isinstance(res, (int, float, sp.Expr)):
                return sp.Matrix([res])
            return res
        return wrapped
    return None

def get_U_basis_and_T(witness):
    U_basis, T_obj = None, None
    
    if hasattr(witness, 'T'):
        T_obj = witness.T
    elif hasattr(witness, 'T_func'):
        T_obj = witness.T_func
    elif isinstance(witness, dict):
        T_obj = witness.get('T') or witness.get('T_func')
    elif isinstance(witness, tuple) and len(witness) == 2:
        T_obj = witness[1]
        
    if hasattr(witness, 'U_basis'):
        U_basis = witness.U_basis
    elif hasattr(witness, 'U'):
        U_basis = witness.U
    elif isinstance(witness, dict):
        U_basis = witness.get('U_basis') or witness.get('U')
    elif isinstance(witness, tuple) and len(witness) == 2:
        U_basis = witness[0]
        
    if U_basis is not None and T_obj is not None:
        T_func = wrap_T_func(T_obj)
            
        if isinstance(U_basis, sp.Matrix):
            U_basis = [U_basis]
        elif isinstance(U_basis, (list, tuple)) and all(isinstance(val, (list, tuple)) for val in U_basis):
            U_basis = [sp.Matrix(list(val)) for val in U_basis]
            
        return U_basis, T_func
        
    return None, None

def rank_GFq(vectors, q):
    if not vectors:
        return 0
    M = [list(v) for v in vectors]
    rows = len(M)
    cols = len(M[0])
    rank = 0
    for c in range(cols):
        pivot = -1
        for r in range(rank, rows):
            if M[r][c] % q != 0:
                pivot = r
                break
        if pivot == -1:
            continue
        M[rank], M[pivot] = M[pivot], M[rank]
        inv = pow(M[rank][c], q - 2, q)
        for r in range(rank + 1, rows):
            factor = (M[r][c] * inv) % q
            for k in range(c, cols):
                M[r][k] = (M[r][k] - factor * M[rank][k]) % q
        rank += 1
    return rank

def check_H1(witness):
    try:
        q, T_dict = get_format_A(witness)
        if q is not None and T_dict is not None:
            if not sp.isprime(q):
                return False
            for k, v in T_dict.items():
                if not isinstance(k, tuple) or not isinstance(v, tuple):
                    return False
            return True
            
        U_basis, T_func = get_U_basis_and_T(witness)
        if U_basis is not None and T_func is not None:
            if not isinstance(U_basis, list) or len(U_basis) == 0:
                return False
            if not all(isinstance(u, sp.Matrix) for u in U_basis):
                return False
            if not callable(T_func):
                return False
            T_v = T_func(U_basis[0])
            if not isinstance(T_v, sp.Matrix):
                return False
            return True
            
        return False
    except Exception:
        return False

def check_H2(witness):
    try:
        q, T_dict = get_format_A(witness)
        if q is not None and T_dict is not None:
            U_list = list(T_dict.keys())
            if not U_list:
                return False
            n = len(U_list[0])
            U_set = set(U_list)
            zero = tuple([0]*n)
            if zero not in U_set:
                return False
            if len(U_list) > 100:
                import random
                for _ in range(100):
                    u = random.choice(U_list)
                    v = random.choice(U_list)
                    c = random.randint(0, q-1)
                    d = random.randint(0, q-1)
                    w = tuple((c*u[i] + d*v[i]) % q for i in range(n))
                    if w not in U_set:
                        return False
            else:
                for u in U_list:
                    for v in U_list:
                        for c in range(q):
                            for d in range(q):
                                w = tuple((c*u[i] + d*v[i]) % q for i in range(n))
                                if w not in U_set:
                                    return False
            return True
            
        U_basis, T_func = get_U_basis_and_T(witness)
        if U_basis is not None and T_func is not None:
            if not U_basis:
                return False
            rows = U_basis[0].rows
            cols = U_basis[0].cols
            if not all(u.rows == rows and u.cols == cols for u in U_basis):
                return False
            return True
            
        return False
    except Exception:
        return False

def check_neg_Q(witness):
    try:
        q, T_dict = get_format_A(witness)
        if q is not None and T_dict is not None:
            U_list = list(T_dict.keys())
            dim_U = rank_GFq(U_list, q)
            
            T_U_list = list(T_dict.values())
            dim_T_U = rank_GFq(T_U_list, q)
            
            m = len(T_U_list[0])
            zero_m = tuple([0]*m)
            ker_U_list = [u for u, v in T_dict.items() if v == zero_m]
            dim_ker = rank_GFq(ker_U_list, q)
            
            return dim_T_U != dim_U - dim_ker
            
        U_basis, T_func = get_U_basis_and_T(witness)
        if U_basis is not None and T_func is not None:
            M_U = sp.Matrix.hstack(*U_basis)
            _, pivot_cols = M_U.rref()
            U_basis = [U_basis[i] for i in pivot_cols]
            dim_U = len(U_basis)
            
            if dim_U == 0:
                T_v = T_func(sp.zeros(M_U.rows, 1))
                dim_T_U = 1 if any(x != 0 for x in T_v) else 0
                dim_ker = 0 if any(x != 0 for x in T_v) else 0
                return dim_T_U != dim_U - dim_ker
                
            c = sp.symbols(f'c0:{dim_U}')
            if isinstance(c, sp.Symbol):
                c = (c,)
                
            v = sp.zeros(U_basis[0].rows, 1)
            for i, sym in enumerate(c):
                v += sym * U_basis[i]
            
            T_v = T_func(v)
            if not isinstance(T_v, sp.Matrix):
                return False
            
            eqs = list(T_v)
            sols = sp.solve(eqs, c, dict=True)
            
            if not sols:
                dim_ker = 0
            else:
                dim_ker = max(len(c) - len(sol) for sol in sols)
                
            T_vectors = []
            for u in U_basis:
                T_vectors.append(T_func(u))
            
            coeffs_list = list(itertools.product([-1, 0, 1, 2], repeat=dim_U))
            for coeffs in coeffs_list[:20]:
                vec = sp.zeros(U_basis[0].rows, 1)
                for i, coeff in enumerate(coeffs):
                    vec += coeff * U_basis[i]
                T_vectors.append(T_func(vec))
                
            M_T_U = sp.Matrix.hstack(*T_vectors)
            dim_T_U = M_T_U.rank()
            
            return dim_T_U != dim_U - dim_ker
            
        return False
    except Exception:
        return False

def conditions(witness):
    return [
        check_H1(witness),
        check_H2(witness),
        check_neg_Q(witness)
    ]