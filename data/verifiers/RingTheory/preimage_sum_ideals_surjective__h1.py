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

def is_ring(add, mul):
    if not isinstance(add, (list, tuple)) or not isinstance(mul, (list, tuple)): return False
    n = len(add)
    if n == 0: return False
    if len(mul) != n: return False
    for row in list(add) + list(mul):
        if not isinstance(row, (list, tuple)) or len(row) != n: return False
        for x in row:
            if not (isinstance(x, int) and 0 <= x < n): return False
            
    # Additive identity = 0
    for i in range(n):
        if add[i][0] != i or add[0][i] != i: return False
        
    # Commutativity of add
    for i in range(n):
        for j in range(n):
            if add[i][j] != add[j][i]: return False
            
    # Associativity and Distributivity
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if add[add[i][j]][k] != add[i][add[j][k]]: return False
                if mul[mul[i][j]][k] != mul[i][mul[j][k]]: return False
                if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False
                if mul[add[i][j]][k] != add[mul[i][k]][mul[j][k]]: return False
                
    # Additive inverse
    for i in range(n):
        if not any(add[i][j] == 0 for j in range(n)): return False
        
    return True

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R_add = witness.get("R_add")
            R_mul = witness.get("R_mul")
            S_add = witness.get("S_add")
            S_mul = witness.get("S_mul")
            f = witness.get("f")
            I = witness.get("I")
            J = witness.get("J")
        elif isinstance(witness, (tuple, list)) and len(witness) == 7:
            R_add, R_mul, S_add, S_mul, f, I, J = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H1: f is a surjective ring homomorphism
    h1_ok = False
    try:
        if is_ring(R_add, R_mul) and is_ring(S_add, S_mul):
            m = len(R_add)
            n = len(S_add)
            if isinstance(f, (list, tuple)) and len(f) == m and all(isinstance(x, int) and 0 <= x < n for x in f):
                is_hom = True
                for i in range(m):
                    for j in range(m):
                        if f[R_add[i][j]] != S_add[f[i]][f[j]]:
                            is_hom = False
                        if f[R_mul[i][j]] != S_mul[f[i]][f[j]]:
                            is_hom = False
                is_surj = len(set(f)) == n
                h1_ok = is_hom and is_surj
    except Exception:
        h1_ok = False
        
    # H2: I and J are ideals of S
    h2_ok = False
    try:
        n = len(S_add)
        def is_ideal(S_add, S_mul, K):
            if not isinstance(K, (list, set, tuple)): return False
            if not K: return False
            if any(not (isinstance(x, int) and 0 <= x < n) for x in K): return False
            K_set = set(K)
            for x in K_set:
                for y in K_set:
                    if S_add[x][y] not in K_set: return False
            for x in K_set:
                for r in range(n):
                    if S_mul[x][r] not in K_set: return False
                    if S_mul[r][x] not in K_set: return False
            return True
            
        h2_ok = is_ideal(S_add, S_mul, I) and is_ideal(S_add, S_mul, J)
    except Exception:
        h2_ok = False
        
    # Conclusion: f^{-1}(I+J) == f^{-1}(I) + f^{-1}(J)
    neg_q_ok = False
    try:
        # I + J
        I_plus_J = set()
        for i in I:
            for j in J:
                I_plus_J.add(S_add[i][j])
                
        # f^{-1}(I+J)
        pre_I_plus_J = set(x for x in range(len(f)) if f[x] in I_plus_J)
        
        # f^{-1}(I)
        pre_I = set(x for x in range(len(f)) if f[x] in I)
        
        # f^{-1}(J)
        pre_J = set(x for x in range(len(f)) if f[x] in J)
        
        # f^{-1}(I) + f^{-1}(J)
        sum_pre = set()
        for a in pre_I:
            for b in pre_J:
                sum_pre.add(R_add[a][b])
                
        neg_q_ok = pre_I_plus_J != sum_pre
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a surjective ring homomorphism from R to S",
    "H_2: I and J are ideals of S",
    "¬Q: f^{-1}(I+J) is not equal to f^{-1}(I) + f^{-1}(J)"
]

N_HYP = 2
NEG_Q_INDEX = 2