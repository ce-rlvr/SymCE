import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: Standard finite rings as addition and multiplication tables
def _make_Zn(n):
    add = [[(i + j) % n for j in range(n)] for i in range(n)]
    mul = [[(i * j) % n for j in range(n)] for i in range(n)]
    return add, mul

Z2_add, Z2_mul = _make_Zn(2)
Z3_add, Z3_mul = _make_Zn(3)
Z4_add, Z4_mul = _make_Zn(4)
Z5_add, Z5_mul = _make_Zn(5)
Z6_add, Z6_mul = _make_Zn(6)
Z8_add, Z8_mul = _make_Zn(8)

def check_ring(add_t, mul_t):
    try:
        n = len(add_t)
        if n == 0: return False
        if len(mul_t) != n: return False
        
        for row in add_t:
            if len(row) != n: return False
            for x in row:
                if not (0 <= int(x) < n): return False
                
        for row in mul_t:
            if len(row) != n: return False
            for x in row:
                if not (0 <= int(x) < n): return False
                
        # Addition is commutative
        for i in range(n):
            for j in range(n):
                if add_t[i][j] != add_t[j][i]: return False
                
        # Associativity of addition and multiplication
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if add_t[add_t[i][j]][k] != add_t[i][add_t[j][k]]: return False
                    if mul_t[mul_t[i][j]][k] != mul_t[i][mul_t[j][k]]: return False
                    
        # Existence of additive identity and inverses
        has_zero = False
        for z in range(n):
            if all(add_t[z][i] == i and add_t[i][z] == i for i in range(n)):
                has_zero = True
                inv_ok = True
                for i in range(n):
                    if not any(add_t[i][j] == z for j in range(n)):
                        inv_ok = False
                        break
                if inv_ok:
                    break
        if not has_zero:
            return False
            
        # Distributivity
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if mul_t[i][add_t[j][k]] != add_t[mul_t[i][j]][mul_t[i][k]]: return False
                    if mul_t[add_t[i][j]][k] != add_t[mul_t[i][k]][mul_t[j][k]]: return False
                    
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R_add = witness['R_add']
            R_mul = witness['R_mul']
            S_add = witness['S_add']
            S_mul = witness['S_mul']
            f = witness['f']
            I = witness['I']
        else:
            R_add, R_mul, S_add, S_mul, f, I = witness
    except Exception:
        return [False, False, False, False]

    # H_1: R and S are rings
    try:
        h1 = check_ring(R_add, R_mul) and check_ring(S_add, S_mul)
    except Exception:
        h1 = False

    # H_2: f is a ring homomorphism
    try:
        n = len(R_add)
        m = len(S_add)
        h2 = True
        for i in range(n):
            val = f(i) if callable(f) else f[i]
            if not (0 <= int(val) < m):
                h2 = False
                break
        if h2:
            for i in range(n):
                for j in range(n):
                    val_i = f(i) if callable(f) else f[i]
                    val_j = f(j) if callable(f) else f[j]
                    val_add = f(R_add[i][j]) if callable(f) else f[R_add[i][j]]
                    val_mul = f(R_mul[i][j]) if callable(f) else f[R_mul[i][j]]
                    
                    if val_add != S_add[val_i][val_j]:
                        h2 = False
                        break
                    if val_mul != S_mul[val_i][val_j]:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # H_3: f is surjective
    try:
        m = len(S_add)
        n = len(R_add)
        image = set(f(i) if callable(f) else f[i] for i in range(n))
        h3 = len(image) == m
    except Exception:
        h3 = False

    # ¬Q: The image f(I) is not an ideal of S
    try:
        m = len(S_add)
        n = len(R_add)
        I_list = list(I)
        
        if not all(0 <= int(x) < n for x in I_list):
            neg_q = False
        else:
            f_I = set(f(x) if callable(f) else f[x] for x in I_list)
            
            is_ideal = True
            if not f_I:
                is_ideal = False
            else:
                z_S = -1
                for z in range(m):
                    if all(S_add[z][i] == i for i in range(m)):
                        z_S = z
                        break
                
                if z_S not in f_I:
                    is_ideal = False
                else:
                    # Closed under addition
                    for x in f_I:
                        for y in f_I:
                            if S_add[x][y] not in f_I:
                                is_ideal = False
                                break
                        if not is_ideal:
                            break
                    
                    # Closed under additive inverses
                    if is_ideal:
                        for x in f_I:
                            has_inv = False
                            for y in f_I:
                                if S_add[x][y] == z_S:
                                    has_inv = True
                                    break
                            if not has_inv:
                                is_ideal = False
                                break
                    
                    # Absorbs multiplication from S
                    if is_ideal:
                        for s in range(m):
                            for x in f_I:
                                if S_mul[s][x] not in f_I or S_mul[x][s] not in f_I:
                                    is_ideal = False
                                    break
                            if not is_ideal:
                                break
                                
            neg_q = not is_ideal
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f is a ring homomorphism",
    "H_3: f is surjective",
    "¬Q: The image f(I) is not an ideal of S"
]

N_HYP = 3
NEG_Q_INDEX = 3