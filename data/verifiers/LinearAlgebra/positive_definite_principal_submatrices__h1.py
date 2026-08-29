import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def get_pd_definitions(M):
    """
    Returns a set of strings representing which definitions of 'positive definite'
    the matrix M satisfies. This handles the ambiguity of the dropped hypothesis.
    """
    defs = set()
    
    # 1. Symmetric part is positive definite (x^H A x > 0 for all x != 0)
    try:
        sym_part = (M + M.H) / 2
        if sym_part.is_positive_definite == True:
            defs.add('sym')
    except Exception:
        pass
        
    # 2. All eigenvalues are real and strictly positive
    try:
        evals = M.eigenvals()
        all_pos = True
        for e in evals:
            try:
                c = complex(e)
                if abs(c.imag) > 1e-7 or c.real <= 1e-7:
                    all_pos = False
                    break
            except Exception:
                if e.is_real != True or e <= 0:
                    all_pos = False
                    break
        if all_pos and len(evals) > 0:
            defs.add('eig')
    except Exception:
        pass
        
    # 3. Sylvester's criterion: all leading principal minors are strictly positive
    try:
        all_pos = True
        for i in range(1, M.shape[0] + 1):
            det_val = M[:i, :i].det()
            try:
                f = float(det_val)
                if f <= 1e-7:
                    all_pos = False
                    break
            except Exception:
                if det_val <= 0:
                    all_pos = False
                    break
        if all_pos:
            defs.add('sylv')
    except Exception:
        pass
        
    # 4. All eigenvalues have strictly positive real parts
    try:
        evals = M.eigenvals()
        all_pos_real = True
        for e in evals:
            try:
                c = complex(e)
                if c.real <= 1e-7:
                    all_pos_real = False
                    break
            except Exception:
                all_pos_real = False
                break
        if all_pos_real and len(evals) > 0:
            defs.add('eig_real_part')
    except Exception:
        pass
        
    return defs

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            A_raw, k = witness
        else:
            A_raw, k = witness, None
        A = sympy.Matrix(A_raw)
    except Exception:
        return [False, False, False]
        
    # H1: A is positive definite
    try:
        defs_A = get_pd_definitions(A)
        h1 = len(defs_A) > 0
    except Exception:
        h1 = False
        defs_A = set()
        
    # H2: k is an integer such that 1 <= k <= n
    try:
        n = A.shape[0]
        h2 = int(k) == k and 1 <= k <= n and A.shape[0] == A.shape[1]
    except Exception:
        h2 = False
        
    # neg_Q: Not every k x k principal submatrix of A is positive definite
    neg_q = False
    try:
        n = A.shape[0]
        if int(k) == k and 1 <= k <= n and A.shape[0] == A.shape[1]:
            k_int = int(k)
            from itertools import combinations
            
            if len(defs_A) > 0:
                # If A satisfies some definition(s), the conclusion fails if there is ANY
                # definition satisfied by A that is NOT satisfied by all k x k principal submatrices.
                for d in defs_A:
                    all_sub_pd = True
                    for indices in combinations(range(n), k_int):
                        sub_A = A.extract(indices, indices)
                        sub_defs = get_pd_definitions(sub_A)
                        if d not in sub_defs:
                            all_sub_pd = False
                            break
                    if not all_sub_pd:
                        neg_q = True
                        break
            else:
                # Fallback if A is not PD under any known definition
                all_sub_pd = True
                for indices in combinations(range(n), k_int):
                    sub_A = A.extract(indices, indices)
                    sub_defs = get_pd_definitions(sub_A)
                    if len(sub_defs) == 0:
                        all_sub_pd = False
                        break
                if not all_sub_pd:
                    neg_q = True
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is positive definite",
    "H_2: k is an integer such that 1 <= k <= n",
    "¬Q: Not every k x k principal submatrix of A is positive definite"
]

N_HYP = 2
NEG_Q_INDEX = 2