import sympy
from sympy import Matrix, eye, zeros
import z3

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_integer_element(e):
    if isinstance(e, int):
        return True
    if hasattr(e, 'is_integer') and e.is_integer == True:
        return getattr(e, 'is_number', False)
    return False

def is_similar_over_Z(A, B):
    n = A.rows
    solver = z3.Solver()
    P = [[z3.Int(f'p_{i}_{j}') for j in range(n)] for i in range(n)]
    
    for i in range(n):
        for j in range(n):
            lhs = sum(P[i][k] * int(B[k, j]) for k in range(n))
            rhs = sum(int(A[i, k]) * P[k][j] for k in range(n))
            solver.add(lhs == rhs)
            
    def z3_det(M):
        if len(M) == 0:
            return 1
        if len(M) == 1:
            return M[0][0]
        if len(M) == 2:
            return M[0][0]*M[1][1] - M[0][1]*M[1][0]
        res = 0
        for j in range(len(M)):
            sub = [[M[i][k] for k in range(len(M)) if k != j] for i in range(1, len(M))]
            sign = 1 if j % 2 == 0 else -1
            res += sign * M[0][j] * z3_det(sub)
        return res

    det = z3_det(P)
    solver.add(z3.Or(det == 1, det == -1))
    
    return solver.check() == z3.sat

def get_blocks(J):
    blocks = []
    n = J.rows
    i = 0
    while i < n:
        j = i + 1
        while j < n and J[j-1, j] == 1 and J[j, j] == J[i, i]:
            j += 1
        blocks.append((J[i, i], j - i))
        i = j
    return blocks

def same_jcf(A, B):
    try:
        JA = A.jordan_form()[1]
        JB = B.jordan_form()[1]
        blocksA = get_blocks(JA)
        blocksB = get_blocks(JB)
        if len(blocksA) != len(blocksB):
            return False
        used = [False] * len(blocksB)
        for ba in blocksA:
            matched = False
            for k, bb in enumerate(blocksB):
                if not used[k] and ba[1] == bb[1]:
                    diff = ba[0] - bb[0]
                    if diff == 0 or (hasattr(diff, 'is_zero') and diff.is_zero) or (hasattr(diff, 'simplify') and diff.simplify() == 0):
                        used[k] = True
                        matched = True
                        break
            if not matched:
                return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        A, B = witness
    except Exception:
        return [False]
        
    try:
        if not hasattr(A, 'shape') or not hasattr(B, 'shape'):
            sim = False
        elif A.shape != B.shape or A.rows != A.cols:
            sim = False
        else:
            is_int_A = all(is_integer_element(e) for e in A)
            is_int_B = all(is_integer_element(e) for e in B)
            if is_int_A and is_int_B:
                sim = is_similar_over_Z(A, B)
            else:
                sim = (A.is_similar(B) == True)
    except Exception:
        sim = False
        
    try:
        jcf_same = same_jcf(A, B)
    except Exception:
        jcf_same = False
        
    try:
        conclusion = (sim == jcf_same)
        neg_Q = not conclusion
    except Exception:
        neg_Q = False
        
    return [neg_Q]

CONDITION_LABELS = [
    "¬Q: The equivalence between similarity and having the same Jordan canonical form fails"
]

N_HYP = 0
NEG_Q_INDEX = 0