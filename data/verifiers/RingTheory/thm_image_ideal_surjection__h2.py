import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
# Witness is expected to be a dictionary with keys 'R', 'S', 'f', 'I'.
# 'R' and 'S' are tuples (n, add_matrix, mul_matrix) representing rings on {0, ..., n-1}.
# 'f' is a list, dict, or callable mapping {0, ..., n_R-1} to {0, ..., n_S-1}.
# 'I' is an iterable of elements in {0, ..., n_R-1}.

def is_ring(ring_tuple):
    try:
        n, add, mul = ring_tuple
        if not (isinstance(n, int) and n > 0): return False
        if len(add) != n or len(mul) != n: return False
        for i in range(n):
            if len(add[i]) != n or len(mul[i]) != n: return False
            for j in range(n):
                if not (0 <= add[i][j] < n): return False
                if not (0 <= mul[i][j] < n): return False
                
        # Additive identity
        zero = None
        for i in range(n):
            if all(add[i][j] == j and add[j][i] == j for j in range(n)):
                zero = i
                break
        if zero is None: return False
        
        # Multiplicative identity
        has_one = False
        for i in range(n):
            if all(mul[i][j] == j and mul[j][i] == j for j in range(n)):
                has_one = True
                break
        if not has_one: return False
        
        # Associativity, commutativity, and distributivity
        for i in range(n):
            for j in range(n):
                if add[i][j] != add[j][i]: return False
                for k in range(n):
                    if add[add[i][j]][k] != add[i][add[j][k]]: return False
                    if mul[mul[i][j]][k] != mul[i][mul[j][k]]: return False
                    if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False
                    if mul[add[i][j]][k] != add[mul[i][k]][mul[j][k]]: return False
                    
        # Additive inverses
        for i in range(n):
            if not any(add[i][j] == zero for j in range(n)): return False
            
        return True
    except Exception:
        return False

def h1(witness):
    return is_ring(witness.get('R')) and is_ring(witness.get('S'))

def h2(witness):
    R = witness.get('R')
    S = witness.get('S')
    f = witness.get('f')
    if not R or not S or f is None: return False
    n_R = R[0]
    n_S = S[0]
    
    if isinstance(f, dict):
        if len(f) != n_R: return False
        if not all(k in f for k in range(n_R)): return False
        images = [f[k] for k in range(n_R)]
    elif isinstance(f, (list, tuple)):
        if len(f) != n_R: return False
        images = f
    elif callable(f):
        try:
            images = [f(k) for k in range(n_R)]
        except Exception:
            return False
    else:
        return False
        
    if not all(isinstance(y, int) and 0 <= y < n_S for y in images): return False
    return len(set(images)) == n_S

def h3(witness):
    R = witness.get('R')
    I = witness.get('I')
    if not R or I is None: return False
    n_R, add_R, mul_R = R
    
    try:
        I_list = list(I)
    except Exception:
        return False
        
    if not I_list: return False
    if not all(isinstance(x, int) and 0 <= x < n_R for x in I_list): return False
    I_set = set(I_list)
    
    zero = None
    for i in range(n_R):
        if all(add_R[i][j] == j for j in range(n_R)):
            zero = i
            break
    if zero not in I_set: return False
    
    for x in I_set:
        for y in I_set:
            if add_R[x][y] not in I_set: return False
        has_inv = False
        for y in I_set:
            if add_R[x][y] == zero:
                has_inv = True
                break
        if not has_inv: return False
        
    for x in I_set:
        for r in range(n_R):
            if mul_R[r][x] not in I_set: return False
            if mul_R[x][r] not in I_set: return False
            
    return True

def neg_q(witness):
    S = witness.get('S')
    f = witness.get('f')
    I = witness.get('I')
    if not S or f is None or I is None: return False
    n_S, add_S, mul_S = S
    
    if isinstance(f, dict):
        f_I = set(f[x] for x in I)
    elif isinstance(f, (list, tuple)):
        f_I = set(f[x] for x in I)
    elif callable(f):
        try:
            f_I = set(f(x) for x in I)
        except Exception:
            return False
    else:
        return False
    
    zero = None
    for i in range(n_S):
        if all(add_S[i][j] == j for j in range(n_S)):
            zero = i
            break
            
    if zero not in f_I: return True
    
    for x in f_I:
        for y in f_I:
            if add_S[x][y] not in f_I: return True
        has_inv = False
        for y in f_I:
            if add_S[x][y] == zero:
                has_inv = True
                break
        if not has_inv: return True
        
    for x in f_I:
        for s in range(n_S):
            if mul_S[s][x] not in f_I: return True
            if mul_S[x][s] not in f_I: return True
            
    return False

def conditions(witness):
    try:
        h1_ok = bool(h1(witness))
    except Exception:
        h1_ok = False

    try:
        h2_ok = bool(h2(witness))
    except Exception:
        h2_ok = False

    try:
        h3_ok = bool(h3(witness))
    except Exception:
        h3_ok = False

    try:
        neg_q_ok = bool(neg_q(witness))
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f is surjective",
    "H_3: I is an ideal of R",
    "¬Q: f(I) is not an ideal of S"
]

N_HYP = 3
NEG_Q_INDEX = 3