import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def normalize_ring(ring_obj):
    if isinstance(ring_obj, int):
        n = ring_obj
        if n <= 0: return None
        add = [[(i + j) % n for j in range(n)] for i in range(n)]
        mul = [[(i * j) % n for j in range(n)] for i in range(n)]
        return list(range(n)), add, mul
    elif isinstance(ring_obj, tuple) and len(ring_obj) == 3:
        elements, add, mul = ring_obj
        n = len(elements)
        elem_to_idx = {e: i for i, e in enumerate(elements)}
        norm_add = [[0]*n for _ in range(n)]
        norm_mul = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if isinstance(add, dict):
                    a = add.get((elements[i], elements[j]))
                else:
                    a = add[i][j]
                if isinstance(mul, dict):
                    m = mul.get((elements[i], elements[j]))
                else:
                    m = mul[i][j]
                if a not in elem_to_idx or m not in elem_to_idx:
                    return None
                norm_add[i][j] = elem_to_idx[a]
                norm_mul[i][j] = elem_to_idx[m]
        return elements, norm_add, norm_mul
    return None

def is_comm_ring_with_id(n, add, mul):
    if n == 0: return False
    for i in range(n):
        for j in range(n):
            if add[i][j] != add[j][i]: return False
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if add[add[i][j]][k] != add[i][add[j][k]]: return False
    zero = None
    for i in range(n):
        if all(add[i][j] == j for j in range(n)):
            zero = i
            break
    if zero is None: return False
    for i in range(n):
        if not any(add[i][j] == zero for j in range(n)): return False
    for i in range(n):
        for j in range(n):
            if mul[i][j] != mul[j][i]: return False
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul[mul[i][j]][k] != mul[i][mul[j][k]]: return False
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False
    id_elem = None
    for i in range(n):
        if all(mul[i][j] == j for j in range(n)):
            id_elem = i
            break
    if id_elem is None: return False
    return True

def get_all_ideals(n, add, mul):
    def get_ideal_generated_by(x):
        I = set([x])
        while True:
            old_len = len(I)
            new_I = set(I)
            for a in I:
                for b in I:
                    new_I.add(add[a][b])
            for a in I:
                for r in range(n):
                    new_I.add(mul[r][a])
            I = new_I
            if len(I) == old_len:
                break
        return frozenset(I)
    
    principal_ideals = set(get_ideal_generated_by(i) for i in range(n))
    ideals = set(principal_ideals)
    
    while True:
        old_len = len(ideals)
        new_ideals = set(ideals)
        for I1 in ideals:
            for I2 in ideals:
                I_sum = set()
                for x in I1:
                    for y in I2:
                        I_sum.add(add[x][y])
                new_ideals.add(frozenset(I_sum))
        ideals = new_ideals
        if len(ideals) == old_len:
            break
    return ideals

def is_local(n, add, mul):
    ideals = get_all_ideals(n, add, mul)
    proper_ideals = [I for I in ideals if len(I) < n]
    if not proper_ideals:
        return False
    
    maximal_ideals = []
    for I in proper_ideals:
        is_maximal = True
        for J in proper_ideals:
            if I != J and I.issubset(J):
                is_maximal = False
                break
        if is_maximal:
            maximal_ideals.append(I)
            
    return len(maximal_ideals) == 1

def normalize_map(f_obj, R_elems, S_elems):
    n = len(R_elems)
    m = len(S_elems)
    f_norm = []
    
    if isinstance(f_obj, dict):
        for e in R_elems:
            if e not in f_obj: return None
            val = f_obj[e]
            if val not in S_elems: return None
            f_norm.append(S_elems.index(val))
    elif callable(f_obj):
        for e in R_elems:
            try:
                val = f_obj(e)
            except Exception:
                return None
            if val not in S_elems: return None
            f_norm.append(S_elems.index(val))
    elif isinstance(f_obj, (list, tuple)):
        if len(f_obj) != n: return None
        for val in f_obj:
            if val not in S_elems: return None
            f_norm.append(S_elems.index(val))
    else:
        return None
    return f_norm

def is_surjective_homomorphism(f_norm, R_n, R_add, R_mul, S_n, S_add, S_mul):
    if len(set(f_norm)) != S_n:
        return False
    for i in range(R_n):
        for j in range(R_n):
            if f_norm[R_add[i][j]] != S_add[f_norm[i]][f_norm[j]]:
                return False
            if f_norm[R_mul[i][j]] != S_mul[f_norm[i]][f_norm[j]]:
                return False
    id_R = None
    for i in range(R_n):
        if all(R_mul[i][j] == j for j in range(R_n)):
            id_R = i
            break
    id_S = None
    for i in range(S_n):
        if all(S_mul[i][j] == j for j in range(S_n)):
            id_S = i
            break
    if id_R is not None and id_S is not None:
        if f_norm[id_R] != id_S:
            return False
    return True

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R_obj = witness.get('R')
            S_obj = witness.get('S')
            f_obj = witness.get('f')
        elif isinstance(witness, tuple) and len(witness) == 3:
            R_obj, S_obj, f_obj = witness
        else:
            return [False] * 5
            
        R_norm = normalize_ring(R_obj)
        S_norm = normalize_ring(S_obj)
        if not R_norm or not S_norm:
            return [False] * 5
            
        R_elems, R_add, R_mul = R_norm
        S_elems, S_add, S_mul = S_norm
        R_n = len(R_elems)
        S_n = len(S_elems)
        
        f_norm = normalize_map(f_obj, R_elems, S_elems)
        if f_norm is None:
            return [False] * 5
            
    except Exception:
        return [False] * 5

    try:
        h1 = is_comm_ring_with_id(R_n, R_add, R_mul)
    except Exception:
        h1 = False

    try:
        h2 = is_local(R_n, R_add, R_mul)
    except Exception:
        h2 = False

    try:
        h3 = is_comm_ring_with_id(S_n, S_add, S_mul)
    except Exception:
        h3 = False

    try:
        h4 = is_surjective_homomorphism(f_norm, R_n, R_add, R_mul, S_n, S_add, S_mul)
    except Exception:
        h4 = False

    try:
        neg_q = not is_local(S_n, S_add, S_mul)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: R is a local ring",
    "H_3: S is a commutative ring with identity",
    "H_4: f is a surjective ring homomorphism from R to S",
    "¬Q: S is not a local ring"
]

N_HYP = 4
NEG_Q_INDEX = 4