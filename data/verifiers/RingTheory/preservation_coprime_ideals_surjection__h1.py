import itertools
import math
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.matrices import *

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

CONDITION_LABELS = [
    "H_1: f is a surjective ring homomorphism from R to S",
    "H_2: I and J are ideals of R such that I + J = R",
    "¬Q: f(I) and f(J) are not coprime in S (f(I) + f(J) != S)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def check_ring(add_table, mul_table):
    try:
        n = len(add_table)
        if n == 0: return False
        if len(mul_table) != n: return False
        for i in range(n):
            if len(add_table[i]) != n: return False
            if len(mul_table[i]) != n: return False
            for j in range(n):
                if not (0 <= add_table[i][j] < n): return False
                if not (0 <= mul_table[i][j] < n): return False
                
        id_add = -1
        for i in range(n):
            if all(add_table[i][j] == j for j in range(n)) and all(add_table[j][i] == j for j in range(n)):
                id_add = i
                break
        if id_add == -1: return False
        
        for i in range(n):
            for j in range(n):
                if add_table[i][j] != add_table[j][i]: return False
                for k in range(n):
                    if add_table[add_table[i][j]][k] != add_table[i][add_table[j][k]]: return False
                    if mul_table[mul_table[i][j]][k] != mul_table[i][mul_table[j][k]]: return False
                    if mul_table[i][add_table[j][k]] != add_table[mul_table[i][j]][mul_table[i][k]]: return False
                    if mul_table[add_table[i][j]][k] != add_table[mul_table[i][k]][mul_table[j][k]]: return False
                    
        for i in range(n):
            has_inv = False
            for j in range(n):
                if add_table[i][j] == id_add and add_table[j][i] == id_add:
                    has_inv = True
                    break
            if not has_inv: return False
            
        return True
    except Exception:
        return False

def is_ideal(add_table, mul_table, A):
    try:
        if not A: return False
        n = len(add_table)
        A_set = set(A)
        if not A_set.issubset(set(range(n))): return False
        
        id_add = -1
        for i in range(n):
            if all(add_table[i][j] == j for j in range(n)):
                id_add = i
                break
        if id_add not in A_set: return False
        
        for a in A_set:
            for b in A_set:
                if add_table[a][b] not in A_set: return False
                
        for a in A_set:
            inv = -1
            for j in range(n):
                if add_table[a][j] == id_add:
                    inv = j
                    break
            if inv not in A_set: return False
            
        for a in A_set:
            for r in range(n):
                if mul_table[a][r] not in A_set: return False
                if mul_table[r][a] not in A_set: return False
                
        return True
    except Exception:
        return False

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple):
            if len(witness) == 7:
                witness = {
                    'R_add': witness[0], 'R_mul': witness[1],
                    'S_add': witness[2], 'S_mul': witness[3],
                    'f': witness[4], 'I': witness[5], 'J': witness[6]
                }
            elif len(witness) == 5:
                R, S, f, I, J = witness
                if isinstance(R, tuple) and len(R) == 2 and isinstance(S, tuple) and len(S) == 2:
                    witness = {
                        'R_add': R[0], 'R_mul': R[1],
                        'S_add': S[0], 'S_mul': S[1],
                        'f': f, 'I': I, 'J': J
                    }
                    
        if isinstance(witness, dict):
            R_add = witness.get('R_add')
            R_mul = witness.get('R_mul')
            S_add = witness.get('S_add')
            S_mul = witness.get('S_mul')
            f = witness.get('f')
            I = witness.get('I')
            J = witness.get('J')
            
            if isinstance(f, dict) and R_add is not None:
                try:
                    f = [f[i] for i in range(len(R_add))]
                except Exception:
                    pass
                    
            if check_ring(R_add, R_mul) and check_ring(S_add, S_mul):
                n = len(R_add)
                m = len(S_add)
                if isinstance(f, list) and len(f) == n and all(isinstance(x, int) and 0 <= x < m for x in f):
                    is_hom = True
                    for i in range(n):
                        for j in range(n):
                            if f[R_add[i][j]] != S_add[f[i]][f[j]]:
                                is_hom = False
                            if f[R_mul[i][j]] != S_mul[f[i]][f[j]]:
                                is_hom = False
                    if is_hom and set(f) == set(range(m)):
                        h1 = True
                        
            if is_ideal(R_add, R_mul, I) and is_ideal(R_add, R_mul, J):
                n = len(R_add)
                I_plus_J = set()
                for i in I:
                    for j in J:
                        I_plus_J.add(R_add[i][j])
                if I_plus_J == set(range(n)):
                    h2 = True
                    
            if R_add is not None and S_add is not None and f is not None and I is not None and J is not None:
                m = len(S_add)
                f_I = set(f[i] for i in I)
                f_J = set(f[j] for j in J)
                f_I_plus_f_J = set()
                for x in f_I:
                    for y in f_J:
                        f_I_plus_f_J.add(S_add[x][y])
                if f_I_plus_f_J != set(range(m)):
                    neg_q = True
                    
            return [h1, h2, neg_q]
    except Exception:
        pass

    # Fallback for object-based witness
    try:
        R = witness.R
        S = witness.S
        f = witness.f
        I = witness.I
        J = witness.J
        
        # Check H1
        h1_ok = True
        for x in R.elements:
            for y in R.elements:
                if f(R.add(x, y)) != S.add(f(x), f(y)): h1_ok = False
                if f(R.mul(x, y)) != S.mul(f(x), f(y)): h1_ok = False
        if set(f(x) for x in R.elements) != set(S.elements): h1_ok = False
        h1 = h1_ok
        
        # Check H2
        def check_ideal(ring, ideal):
            for x in ideal:
                for y in ideal:
                    if hasattr(ring, 'sub'):
                        if ring.sub(x, y) not in ideal: return False
                    else:
                        if ring.add(x, ring.neg(y)) not in ideal: return False
                for r in ring.elements:
                    if ring.mul(x, r) not in ideal: return False
                    if ring.mul(r, x) not in ideal: return False
            return True
            
        if check_ideal(R, I) and check_ideal(R, J):
            I_plus_J = set(R.add(i, j) for i in I for j in J)
            if I_plus_J == set(R.elements):
                h2 = True
                
        # Check neg_Q
        f_I = set(f(i) for i in I)
        f_J = set(f(j) for j in J)
        f_I_plus_f_J = set(S.add(x, y) for x in f_I for y in f_J)
        if f_I_plus_f_J != set(S.elements):
            neg_q = True
            
        return [h1, h2, neg_q]
    except Exception:
        pass

    return [False, False, False]