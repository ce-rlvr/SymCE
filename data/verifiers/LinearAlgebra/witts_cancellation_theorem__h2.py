import sympy
from sympy import Matrix, zeros, eye
import z3

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: V, W_1, and W_2 are finite-dimensional vector spaces equipped with non-degenerate symmetric bilinear forms",
    "H_2: The orthogonal direct sum V \\perp W_1 is isometric to the orthogonal direct sum V \\perp W_2",
    "¬Q: The bilinear space W_1 is NOT isometric to W_2"
]

N_HYP = 2
NEG_Q_INDEX = 2

def orthogonal_sum(A, B):
    n = A.shape[0]
    m = B.shape[0]
    res = zeros(n + m, n + m)
    res[:n, :n] = A
    res[n:, n:] = B
    return res

def is_isometric(A, B, p=2):
    if A.shape != B.shape:
        return False
    n = A.shape[0]
    if n == 0:
        return True
    
    solver = z3.Solver()
    solver.set("timeout", 4000)
    uid = id(solver)
    
    if p:
        P = [[z3.Int(f"P_{i}_{j}_{uid}") for j in range(n)] for i in range(n)]
        for i in range(n):
            for j in range(n):
                solver.add(P[i][j] >= 0, P[i][j] < p)
                
        for i in range(n):
            for j in range(n):
                val = 0
                for k in range(n):
                    for l in range(n):
                        val += P[k][i] * int(A[k, l]) * P[l][j]
                solver.add((val - int(B[i, j])) % p == 0)
                
        Q = [[z3.Int(f"Q_{i}_{j}_{uid}") for j in range(n)] for i in range(n)]
        for i in range(n):
            for j in range(n):
                solver.add(Q[i][j] >= 0, Q[i][j] < p)
        for i in range(n):
            for j in range(n):
                val = sum(P[i][k] * Q[k][j] for k in range(n))
                if i == j:
                    solver.add((val - 1) % p == 0)
                else:
                    solver.add(val % p == 0)
                    
        return solver.check() == z3.sat
    else:
        P = [[z3.Real(f"P_{i}_{j}_{uid}") for j in range(n)] for i in range(n)]
        for i in range(n):
            for j in range(n):
                val = 0
                for k in range(n):
                    for l in range(n):
                        val += P[k][i] * z3.RealVal(str(A[k, l])) * P[l][j]
                solver.add(val == z3.RealVal(str(B[i, j])))
        
        Q = [[z3.Real(f"Q_{i}_{j}_{uid}") for j in range(n)] for i in range(n)]
        for i in range(n):
            for j in range(n):
                val = sum(P[i][k] * Q[k][j] for k in range(n))
                if i == j:
                    solver.add(val == 1)
                else:
                    solver.add(val == 0)
        return solver.check() == z3.sat

def is_valid_form(M, p):
    if M.shape[0] != M.shape[1]:
        return False
    if M != M.T:
        return False
    try:
        det = M.det()
        if p:
            return (int(det) % p) != 0
        else:
            return det != 0
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            V = Matrix(witness['V'])
            W1 = Matrix(witness['W1'])
            W2 = Matrix(witness['W2'])
            p = witness.get('p', 2)
        else:
            V = Matrix(witness[0])
            W1 = Matrix(witness[1])
            W2 = Matrix(witness[2])
            p = witness[3] if len(witness) > 3 else 2
    except Exception:
        return [False, False, False]

    try:
        h1_ok = is_valid_form(V, p) and is_valid_form(W1, p) and is_valid_form(W2, p)
    except Exception:
        h1_ok = False

    try:
        VW1 = orthogonal_sum(V, W1)
        VW2 = orthogonal_sum(V, W2)
        h2_ok = is_isometric(VW1, VW2, p)
    except Exception:
        h2_ok = False

    try:
        neg_q_ok = not is_isometric(W1, W2, p)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]