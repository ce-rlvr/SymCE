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

CONDITION_LABELS = [
    "H_1: I and J are ideals of R",
    "H_2: I + J = R",
    "¬Q: R/(I \\cap J) is not isomorphic to (R/I) \\times (R/J)"
]
N_HYP = 2
NEG_Q_INDEX = 2

def wrap_op(op, elements):
    if callable(op): return op
    if isinstance(op, dict):
        return lambda a, b: op[(a, b)]
    return lambda a, b: op[elements.index(a)][elements.index(b)]

def get_ring_ops_clean(witness):
    if isinstance(witness, dict):
        e = witness['elements']
        a = wrap_op(witness['add'], e)
        m = wrap_op(witness['mul'], e)
        I = witness['I']
        J = witness['J']
    elif isinstance(witness, tuple) and len(witness) == 5:
        e = witness[0]
        a = wrap_op(witness[1], e)
        m = wrap_op(witness[2], e)
        I = witness[3]
        J = witness[4]
    else:
        e = witness.elements
        a = wrap_op(witness.add, e)
        m = wrap_op(witness.mul, e)
        I = witness.I
        J = witness.J
        
    N = len(e)
    add_t = [[0]*N for _ in range(N)]
    mul_t = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            add_t[i][j] = e.index(a(e[i], e[j]))
            mul_t[i][j] = e.index(m(e[i], e[j]))
            
    norm_e = list(range(N))
    norm_a = lambda x, y: add_t[x][y]
    norm_m = lambda x, y: mul_t[x][y]
    norm_I = [e.index(x) for x in I]
    norm_J = [e.index(x) for x in J]
    
    return norm_e, norm_a, norm_m, norm_I, norm_J

def find_zero(elements, add):
    for z in elements:
        if all(add(z, x) == x and add(x, z) == x for x in elements):
            return z
    return None

def check_ideal(elements, add, mul, zero, subset):
    if not subset: return False
    if zero not in subset: return False
    subset_set = set(subset)
    for x in subset:
        for y in subset:
            minus_y = None
            for c in elements:
                if add(y, c) == zero:
                    minus_y = c
                    break
            if minus_y is None: return False
            if add(x, minus_y) not in subset_set: return False
            
    for s in subset:
        for r in elements:
            if mul(r, s) not in subset_set: return False
            if mul(s, r) not in subset_set: return False
    return True

def build_quotient_ring(elements, add, mul, ideal):
    cosets = []
    seen = set()
    for x in elements:
        if x in seen: continue
        coset = set()
        for i in ideal:
            coset.add(add(x, i))
        f_coset = frozenset(coset)
        cosets.append(f_coset)
        seen.update(f_coset)
        
    K = len(cosets)
    q_e = list(range(K))
    
    q_add_t = [[0]*K for _ in range(K)]
    q_mul_t = [[0]*K for _ in range(K)]
    
    for i in range(K):
        for j in range(K):
            x = next(iter(cosets[i]))
            y = next(iter(cosets[j]))
            sum_xy = add(x, y)
            prod_xy = mul(x, y)
            
            for k in range(K):
                if sum_xy in cosets[k]:
                    q_add_t[i][j] = k
                if prod_xy in cosets[k]:
                    q_mul_t[i][j] = k
                    
    return q_e, q_add_t, q_mul_t

def are_isomorphic(e1, a1, m1, e2, a2, m2):
    if len(e1) != len(e2): return False
    N = len(e1)
    if N == 1: return True
    
    def backtrack(mapping, used):
        i = len(mapping)
        if i == N:
            return True
            
        for j in range(N):
            if used[j]: continue
            
            consistent = True
            for x in range(i + 1):
                map_x = mapping[x] if x < i else j
                
                sum1 = a1[x][i]
                if sum1 <= i:
                    map_sum1 = mapping[sum1] if sum1 < i else j
                    if map_sum1 != a2[map_x][j]:
                        consistent = False; break
                        
                sum2 = a1[i][x]
                if sum2 <= i:
                    map_sum2 = mapping[sum2] if sum2 < i else j
                    if map_sum2 != a2[j][map_x]:
                        consistent = False; break
                        
                prod1 = m1[x][i]
                if prod1 <= i:
                    map_prod1 = mapping[prod1] if prod1 < i else j
                    if map_prod1 != m2[map_x][j]:
                        consistent = False; break
                        
                prod2 = m1[i][x]
                if prod2 <= i:
                    map_prod2 = mapping[prod2] if prod2 < i else j
                    if map_prod2 != m2[j][map_x]:
                        consistent = False; break
                        
            if consistent:
                mapping.append(j)
                used[j] = True
                if backtrack(mapping, used):
                    return True
                mapping.pop()
                used[j] = False
                
        return False

    used = [False]*N
    return backtrack([], used)

def conditions(witness):
    try:
        e, a, m, I, J = get_ring_ops_clean(witness)
        zero = find_zero(e, a)
        if zero is None:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    try:
        h1 = check_ideal(e, a, m, zero, I) and check_ideal(e, a, m, zero, J)
    except Exception:
        h1 = False
        
    try:
        sum_IJ = set()
        for i in I:
            for j in J:
                sum_IJ.add(a(i, j))
        h2 = (sum_IJ == set(e))
    except Exception:
        h2 = False
        
    try:
        I_cap_J = list(set(I).intersection(set(J)))
        q1_e, q1_a, q1_m = build_quotient_ring(e, a, m, I_cap_J)
        
        ri_e, ri_a, ri_m = build_quotient_ring(e, a, m, I)
        rj_e, rj_a, rj_m = build_quotient_ring(e, a, m, J)
        
        prod_e = list(itertools.product(ri_e, rj_e))
        P = len(prod_e)
        p_a = [[0]*P for _ in range(P)]
        p_m = [[0]*P for _ in range(P)]
        for i in range(P):
            for j in range(P):
                x1, y1 = prod_e[i]
                x2, y2 = prod_e[j]
                sum_x = ri_a[x1][x2]
                sum_y = rj_a[y1][y2]
                prod_x = ri_m[x1][x2]
                prod_y = rj_m[y1][y2]
                p_a[i][j] = prod_e.index((sum_x, sum_y))
                p_m[i][j] = prod_e.index((prod_x, prod_y))
                
        q1_e_idx = list(range(len(q1_e)))
        prod_e_idx = list(range(P))
        
        iso = are_isomorphic(q1_e_idx, q1_a, q1_m, prod_e_idx, p_a, p_m)
        neg_q = not iso
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]