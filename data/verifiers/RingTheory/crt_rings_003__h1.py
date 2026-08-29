import itertools
import functools
import math
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import Rational, Integer, Symbol

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

def extract_witness(witness):
    if isinstance(witness, dict):
        elements = list(witness.get("elements", []))
        zero = witness.get("zero", None)
        add_raw = witness.get("add", None)
        mul_raw = witness.get("mul", None)
        ideals = [list(I) for I in witness.get("ideals", [])]
    else:
        elements = list(getattr(witness, "elements", []))
        zero = getattr(witness, "zero", None)
        add_raw = getattr(witness, "add", None)
        mul_raw = getattr(witness, "mul", None)
        ideals = [list(I) for I in getattr(witness, "ideals", [])]
        
    if callable(add_raw):
        add = add_raw
    else:
        add = lambda a, b: elements[add_raw[elements.index(a)][elements.index(b)]]
        
    if callable(mul_raw):
        mul = mul_raw
    else:
        mul = lambda a, b: elements[mul_raw[elements.index(a)][elements.index(b)]]
        
    return elements, zero, add, mul, ideals

def normalize_ring(elements, zero, add, mul, ideals):
    N = len(elements)
    
    def get_idx(e):
        for i, x in enumerate(elements):
            if type(x) is type(e) and x == e: return i
        for i, x in enumerate(elements):
            try:
                if x == e: return i
            except Exception:
                pass
        return -1
        
    add_idx = [[get_idx(add(elements[i], elements[j])) for j in range(N)] for i in range(N)]
    mul_idx = [[get_idx(mul(elements[i], elements[j])) for j in range(N)] for i in range(N)]
    zero_idx = get_idx(zero)
    ideals_idx = [[get_idx(x) for x in I] for I in ideals]
    
    return N, zero_idx, add_idx, mul_idx, ideals_idx

def check_ring_idx(N, zero, add, mul):
    if zero < 0 or zero >= N: return False
    for i in range(N):
        for j in range(N):
            if add[i][j] < 0 or add[i][j] >= N: return False
            if mul[i][j] < 0 or mul[i][j] >= N: return False
            
    for a in range(N):
        if add[a][zero] != a or add[zero][a] != a: return False
        has_inv = False
        for b in range(N):
            if add[a][b] == zero and add[b][a] == zero:
                has_inv = True
                break
        if not has_inv: return False
        
        for b in range(N):
            if add[a][b] != add[b][a]: return False
            for c in range(N):
                if add[add[a][b]][c] != add[a][add[b][c]]: return False
                if mul[mul[a][b]][c] != mul[a][mul[b][c]]: return False
                if mul[a][add[b][c]] != add[mul[a][b]][mul[a][c]]: return False
                if mul[add[a][b]][c] != add[mul[a][c]][mul[b][c]]: return False
    return True

def check_ideal_idx(N, zero, add, mul, I):
    I_set = set(I)
    if zero not in I_set: return False
    for x in I:
        if x < 0 or x >= N: return False
        has_inv = False
        for y in I:
            if add[x][y] == zero:
                has_inv = True
                break
        if not has_inv: return False
        
        for y in I:
            if add[x][y] not in I_set: return False
            
        for r in range(N):
            if mul[r][x] not in I_set: return False
            if mul[x][r] not in I_set: return False
    return True

def check_pairwise_coprime_idx(N, add, ideals):
    n = len(ideals)
    for i in range(n):
        for j in range(i + 1, n):
            sum_ideal = set()
            for x in ideals[i]:
                for y in ideals[j]:
                    sum_ideal.add(add[x][y])
            if len(sum_ideal) != N: return False
    return True

def get_quotient_ring(N, add, mul, I):
    cosets = []
    seen = set()
    for x in range(N):
        if x in seen: continue
        coset = set()
        for y in I:
            coset.add(add[x][y])
        if not coset:
            coset.add(x)
        cosets.append(frozenset(coset))
        seen.update(coset)
        seen.add(x)
        
    idx_to_rep = [list(c)[0] for c in cosets]
    M = len(cosets)
    q_add = [[0]*M for _ in range(M)]
    q_mul = [[0]*M for _ in range(M)]
    
    for i in range(M):
        for j in range(M):
            rep_i = idx_to_rep[i]
            rep_j = idx_to_rep[j]
            
            sum_rep = add[rep_i][rep_j]
            for k, c in enumerate(cosets):
                if sum_rep in c:
                    q_add[i][j] = k
                    break
                    
            mul_rep = mul[rep_i][rep_j]
            for k, c in enumerate(cosets):
                if mul_rep in c:
                    q_mul[i][j] = k
                    break
                    
    return M, q_add, q_mul

def get_product_ring(rings):
    sizes = [r[0] for r in rings]
    M = 1
    for s in sizes: M *= s
    
    ranges = [range(s) for s in sizes]
    elements = list(itertools.product(*ranges))
    elem_to_idx = {e: i for i, e in enumerate(elements)}
    
    p_add = [[0]*M for _ in range(M)]
    p_mul = [[0]*M for _ in range(M)]
    
    for i in range(M):
        for j in range(M):
            e_i = elements[i]
            e_j = elements[j]
            
            sum_e = tuple(rings[k][1][e_i[k]][e_j[k]] for k in range(len(rings)))
            mul_e = tuple(rings[k][2][e_i[k]][e_j[k]] for k in range(len(rings)))
            
            p_add[i][j] = elem_to_idx[sum_e]
            p_mul[i][j] = elem_to_idx[mul_e]
            
    return M, p_add, p_mul

def are_isomorphic(N1, add1, mul1, N2, add2, mul2):
    if N1 != N2: return False
    if N1 == 1: return True
    
    def find_zero(N, add):
        for i in range(N):
            if all(add[i][j] == j for j in range(N)):
                return i
        return None
        
    z1 = find_zero(N1, add1)
    z2 = find_zero(N2, add2)
    if z1 is None or z2 is None: return False
    
    mapping = {}
    used = set()
    
    def backtrack(i):
        if i == N1: return True
        if i == z1:
            mapping[i] = z2
            used.add(z2)
            if backtrack(i + 1): return True
            used.remove(z2)
            del mapping[i]
            return False
            
        for j in range(N2):
            if j in used: continue
            if j == z2: continue
            
            consistent = True
            for x, map_x in mapping.items():
                s1 = add1[x][i]
                s2 = add2[map_x][j]
                if s1 in mapping and mapping[s1] != s2: consistent = False; break
                if s1 not in mapping and s2 in used: consistent = False; break
                
                s1 = add1[i][x]
                s2 = add2[j][map_x]
                if s1 in mapping and mapping[s1] != s2: consistent = False; break
                if s1 not in mapping and s2 in used: consistent = False; break
                
                m1 = mul1[x][i]
                m2 = mul2[map_x][j]
                if m1 in mapping and mapping[m1] != m2: consistent = False; break
                if m1 not in mapping and m2 in used: consistent = False; break
                
                m1 = mul1[i][x]
                m2 = mul2[j][map_x]
                if m1 in mapping and mapping[m1] != m2: consistent = False; break
                if m1 not in mapping and m2 in used: consistent = False; break
                
            if consistent:
                mapping[i] = j
                used.add(j)
                if backtrack(i + 1): return True
                used.remove(j)
                del mapping[i]
                
        return False

    return backtrack(0)

def conditions(witness):
    try:
        elements, zero, add_func, mul_func, ideals = extract_witness(witness)
        N, zero_idx, add, mul, ideals_idx = normalize_ring(elements, zero, add_func, mul_func, ideals)
    except Exception:
        return [False, False, False]
        
    try:
        h1 = check_ring_idx(N, zero_idx, add, mul)
        if h1:
            for I in ideals_idx:
                if not check_ideal_idx(N, zero_idx, add, mul, I):
                    h1 = False
                    break
    except Exception:
        h1 = False
        
    try:
        if len(ideals_idx) < 2:
            h2 = False
        else:
            h2 = check_pairwise_coprime_idx(N, add, ideals_idx)
    except Exception:
        h2 = False
        
    try:
        if not ideals_idx:
            I_int = [zero_idx]
        else:
            I_int = set(ideals_idx[0])
            for I in ideals_idx[1:]:
                I_int = I_int.intersection(set(I))
            I_int = list(I_int)
            
        M1, add1, mul1 = get_quotient_ring(N, add, mul, I_int)
        
        rings = []
        for I in ideals_idx:
            rings.append(get_quotient_ring(N, add, mul, I))
            
        M2, add2, mul2 = get_product_ring(rings)
        
        neg_q = not are_isomorphic(M1, add1, mul1, M2, add2, mul2)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: I_1, ..., I_n are ideals of R",
    "H_2: I_i + I_j = R for all i != j",
    "¬Q: R / (\\bigcap_{k=1}^n I_k) is not isomorphic to \\prod_{k=1}^n R/I_k"
]

N_HYP = 2
NEG_Q_INDEX = 2