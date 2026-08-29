import sympy
from sympy import Matrix, eye, zeros, Rational
from sympy.abc import x, y, z
import z3
import math
import itertools

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_field(F):
    if hasattr(F, 'is_Field') and F.is_Field:
        return True
    if F in [sympy.QQ, sympy.RR, sympy.CC]:
        return True
    if hasattr(F, 'is_FiniteField') and F.is_FiniteField:
        return True
    return False

def get_rank(M, F):
    if hasattr(F, 'is_FiniteField') and F.is_FiniteField:
        p = F.mod
        n, m = M.shape
        max_rank = 0
        for r in range(1, min(n, m) + 1):
            for row_indices in itertools.combinations(range(n), r):
                for col_indices in itertools.combinations(range(m), r):
                    subM = M.extract(row_indices, col_indices)
                    if subM.det() % p != 0:
                        max_rank = max(max_rank, r)
        return max_rank
    return M.rank()

def are_congruent(A, B, F):
    if A.shape != B.shape:
        return False
    if A.shape[0] != A.shape[1]:
        return False
    n = A.shape[0]
    
    if hasattr(F, 'is_FiniteField') and F.is_FiniteField:
        p = F.mod
        elements = list(range(p))
        B_mod = B.applyfunc(lambda val: val % p)
        A_list = A.tolist()
        for entries in itertools.product(elements, repeat=n*n):
            if n == 1:
                det = entries[0]
            elif n == 2:
                det = entries[0]*entries[3] - entries[1]*entries[2]
            elif n == 3:
                det = (entries[0]*(entries[4]*entries[8] - entries[5]*entries[7]) -
                       entries[1]*(entries[3]*entries[8] - entries[5]*entries[6]) +
                       entries[2]*(entries[3]*entries[7] - entries[4]*entries[6]))
            else:
                P = sympy.Matrix(n, n, entries)
                det = P.det()
                
            if det % p != 0:
                if n <= 3:
                    P_mat = [entries[i*n:(i+1)*n] for i in range(n)]
                    AP = [[sum(A_list[i][k] * P_mat[k][j] for k in range(n)) % p for j in range(n)] for i in range(n)]
                    match = True
                    for i in range(n):
                        for j in range(n):
                            val = sum(P_mat[k][i] * AP[k][j] for k in range(n)) % p
                            if val != B_mod[i, j]:
                                match = False
                                break
                        if not match:
                            break
                    if match:
                        return True
                else:
                    P = sympy.Matrix(n, n, entries)
                    PTAP = (P.T * A * P).applyfunc(lambda val: val % p)
                    if PTAP == B_mod:
                        return True
        return False
        
    if F == sympy.QQ and n == 1:
        a = A[0, 0]
        b = B[0, 0]
        if a == 0 and b == 0: return True
        if a == 0 or b == 0: return False
        q = sympy.Rational(a) / sympy.Rational(b)
        if q < 0: return False
        num, den = q.p, q.q
        return math.isqrt(num)**2 == num and math.isqrt(den)**2 == den

    if F == sympy.RR and A.is_symmetric() and B.is_symmetric():
        def get_signature(M):
            evals = M.eigenvals()
            pos = sum(m for val, m in evals.items() if float(sympy.re(val.evalf())) > 1e-9)
            neg = sum(m for val, m in evals.items() if float(sympy.re(val.evalf())) < -1e-9)
            return pos, neg
        return get_signature(A) == get_signature(B)

    if F == sympy.CC:
        return True

    solver = z3.Solver()
    P_vars = [[z3.Real(f"p_{i}_{j}") for j in range(n)] for i in range(n)]
    
    for i in range(n):
        for j in range(n):
            expr = 0
            for k in range(n):
                for l in range(n):
                    expr += P_vars[k][i] * float(A[k, l]) * P_vars[l][j]
            solver.add(expr == float(B[i, j]))
            
    if n == 1:
        solver.add(P_vars[0][0] != 0)
    elif n == 2:
        solver.add(P_vars[0][0]*P_vars[1][1] - P_vars[0][1]*P_vars[1][0] != 0)
    elif n == 3:
        det = (P_vars[0][0]*(P_vars[1][1]*P_vars[2][2] - P_vars[1][2]*P_vars[2][1]) -
               P_vars[0][1]*(P_vars[1][0]*P_vars[2][2] - P_vars[1][2]*P_vars[2][0]) +
               P_vars[0][2]*(P_vars[1][0]*P_vars[2][1] - P_vars[1][1]*P_vars[2][0]))
        solver.add(det != 0)
        
    solver.set("timeout", 2000)
    res = solver.check()
    if res == z3.unsat:
        return False
    return True

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                F, A, B = witness
            elif len(witness) == 2:
                A, B = witness
                F = sympy.QQ
            else:
                return [False, False]
        else:
            return [False, False]
            
        h1_ok = is_field(F)
        
        if not hasattr(A, 'shape') or not hasattr(B, 'shape'):
            return [h1_ok, False]
        if A.shape[0] != A.shape[1] or B.shape[0] != B.shape[1]:
            return [h1_ok, False]
        if A.shape != B.shape:
            return [h1_ok, False]
            
        try:
            same_rank = (get_rank(A, F) == get_rank(B, F))
            congruent = are_congruent(A, B, F)
            neg_q_ok = bool(congruent != same_rank)
        except Exception:
            neg_q_ok = False
            
        return [h1_ok, neg_q_ok]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: F is a field",
    "¬Q: The biconditional 'A and B are congruent iff they have the same rank' fails"
]
N_HYP = 1
NEG_Q_INDEX = 1