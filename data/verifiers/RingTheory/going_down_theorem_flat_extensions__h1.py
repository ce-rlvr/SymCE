import sympy
from sympy import eye, zeros, Matrix
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import z3
import math
import itertools
import functools

# Top-level setup for standard algebra objects
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a subring of S",
    "H_2: S is a flat R-module",
    "H_3: P_1 and P_2 are prime ideals of R such that P_1 \\subseteq P_2",
    "H_4: Q_2 is a prime ideal of S such that Q_2 \\cap R = P_2",
    "¬Q: For all prime ideals Q_1 of S, if Q_1 \\subseteq Q_2 then Q_1 \\cap R != P_1"
]

N_HYP = 4
NEG_Q_INDEX = 4

def is_same_set(A, B):
    if len(A) != len(B): return False
    for a in A:
        if a not in B: return False
    return True

def is_ring(Ring, add, mul, zero, one):
    if zero not in Ring or one not in Ring: return False
    for x in Ring:
        for y in Ring:
            if add(x, y) not in Ring: return False
            if mul(x, y) not in Ring: return False
    for x in Ring:
        has_inv = False
        for y in Ring:
            if add(x, y) == zero:
                has_inv = True
                break
        if not has_inv: return False
    for x in Ring:
        if add(x, zero) != x or add(zero, x) != x: return False
    for x in Ring:
        if mul(x, one) != x or mul(one, x) != x: return False
    return True

def is_subring(R, S, add, mul, zero, one):
    for x in R:
        if x not in S: return False
    if zero not in R or one not in R: return False
    for x in R:
        for y in R:
            if add(x, y) not in R: return False
            if mul(x, y) not in R: return False
    for x in R:
        has_inv = False
        for y in R:
            if add(x, y) == zero:
                has_inv = True
                break
        if not has_inv: return False
    return True

def is_ideal(I, Ring, add, mul, zero):
    if not I: return False
    for x in I:
        if x not in Ring: return False
    if zero not in I: return False
    for x in I:
        for y in I:
            if add(x, y) not in I: return False
    for x in I:
        has_inv = False
        for y in Ring:
            if add(x, y) == zero and y in I:
                has_inv = True
                break
        if not has_inv: return False
    for i in I:
        for r in Ring:
            if mul(r, i) not in I: return False
            if mul(i, r) not in I: return False
    return True

def is_prime_ideal(I, Ring, add, mul, zero, one):
    if not is_ideal(I, Ring, add, mul, zero): return False
    if is_same_set(I, Ring): return False
    
    for a in Ring:
        for b in Ring:
            all_in_I = True
            for r in Ring:
                if mul(a, mul(r, b)) not in I:
                    all_in_I = False
                    break
            if all_in_I:
                if a not in I and b not in I:
                    return False
    return True

def ideal_closure(gens, Ring, add, mul, zero):
    ideal = [zero]
    for g in gens:
        if g not in ideal:
            ideal.append(g)
    while True:
        new_ideal = ideal.copy()
        for x in ideal:
            for y in ideal:
                s = add(x, y)
                if s not in new_ideal: new_ideal.append(s)
            for r in Ring:
                p1 = mul(r, x)
                if p1 not in new_ideal: new_ideal.append(p1)
                p2 = mul(x, r)
                if p2 not in new_ideal: new_ideal.append(p2)
        for x in ideal:
            for y in Ring:
                if add(x, y) == zero:
                    if y not in new_ideal: new_ideal.append(y)
        if len(new_ideal) == len(ideal):
            break
        ideal = new_ideal
    return ideal

def get_all_ideals(Ring, add, mul, zero):
    principal = []
    for r in Ring:
        principal.append(ideal_closure([r], Ring, add, mul, zero))
    
    ideals = []
    queue = principal.copy()
    seen = []
    while queue:
        curr = queue.pop(0)
        already_seen = False
        for s in seen:
            if is_same_set(curr, s):
                already_seen = True
                break
        if already_seen:
            continue
        seen.append(curr)
        ideals.append(curr)
        for p in principal:
            new_ideal = []
            for x in curr:
                for y in p:
                    s_val = add(x, y)
                    if s_val not in new_ideal:
                        new_ideal.append(s_val)
            queue.append(new_ideal)
    return ideals

def tensor_product_size(I, S, R, add, mul, zero):
    pairs = []
    for i in I:
        for s in S:
            pairs.append((i, s))
    N = len(pairs)
    if N == 0: return 1
    
    def get_idx(i, s):
        for idx, p in enumerate(pairs):
            if p[0] == i and p[1] == s:
                return idx
        return -1

    relations = []
    
    for i1 in I:
        for i2 in I:
            i12 = add(i1, i2)
            if i12 in I:
                for s in S:
                    row = [0]*N
                    idx12 = get_idx(i12, s)
                    idx1 = get_idx(i1, s)
                    idx2 = get_idx(i2, s)
                    row[idx12] -= 1
                    row[idx1] += 1
                    row[idx2] += 1
                    if any(x != 0 for x in row):
                        relations.append(row)
                    
    for i in I:
        for s1 in S:
            for s2 in S:
                s12 = add(s1, s2)
                row = [0]*N
                idx12 = get_idx(i, s12)
                idx1 = get_idx(i, s1)
                idx2 = get_idx(i, s2)
                row[idx12] -= 1
                row[idx1] += 1
                row[idx2] += 1
                if any(x != 0 for x in row):
                    relations.append(row)
                
    for i in I:
        for r in R:
            ir = mul(i, r)
            if ir in I:
                for s in S:
                    rs = mul(r, s)
                    row = [0]*N
                    idx_ir_s = get_idx(ir, s)
                    idx_i_rs = get_idx(i, rs)
                    row[idx_ir_s] += 1
                    row[idx_i_rs] -= 1
                    if any(x != 0 for x in row):
                        relations.append(row)
                    
    m = len(S)
    for j in range(N):
        row = [0]*N
        row[j] = m
        relations.append(row)
        
    unique_relations = []
    seen_rows = set()
    for row in relations:
        t = tuple(row)
        if t not in seen_rows:
            seen_rows.add(t)
            unique_relations.append(row)
            
    M = Matrix(unique_relations)
    try:
        smf = M.smith_normal_form()
    except Exception:
        return -1
        
    size = 1
    for j in range(N):
        val = smf[j, j]
        if val != 0:
            size *= abs(val)
        else:
            return float('inf')
    return size

def image_size(I, S, add, mul, zero):
    elements = [zero]
    gens = []
    for i in I:
        for s in S:
            g = mul(i, s)
            if g not in gens: gens.append(g)
            
    while True:
        new_elements = elements.copy()
        for e in elements:
            for g in gens:
                s_val = add(e, g)
                if s_val not in new_elements: new_elements.append(s_val)
        for x in elements:
            for y in S:
                if add(x, y) == zero:
                    if y not in new_elements: new_elements.append(y)
        if len(new_elements) == len(elements):
            break
        elements = new_elements
    return len(elements)

def check_H1(witness):
    R = witness['R']
    S = witness['S']
    add = witness['add']
    mul = witness['mul']
    zero = witness['zero']
    one = witness['one']
    
    if not is_ring(S, add, mul, zero, one): return False
    return is_subring(R, S, add, mul, zero, one)

def check_H2(witness):
    R = witness['R']
    S = witness['S']
    add = witness['add']
    mul = witness['mul']
    zero = witness['zero']
    
    ideals = get_all_ideals(R, add, mul, zero)
    for I in ideals:
        tsize = tensor_product_size(I, S, R, add, mul, zero)
        isize = image_size(I, S, add, mul, zero)
        if tsize != isize:
            return False
    return True

def check_H3(witness):
    R = witness['R']
    add = witness['add']
    mul = witness['mul']
    zero = witness['zero']
    one = witness['one']
    P1 = witness['P1']
    P2 = witness['P2']
    
    if not is_prime_ideal(P1, R, add, mul, zero, one): return False
    if not is_prime_ideal(P2, R, add, mul, zero, one): return False
    
    for x in P1:
        if x not in P2: return False
    return True

def check_H4(witness):
    R = witness['R']
    S = witness['S']
    add = witness['add']
    mul = witness['mul']
    zero = witness['zero']
    one = witness['one']
    P2 = witness['P2']
    Q2 = witness['Q2']
    
    if not is_prime_ideal(Q2, S, add, mul, zero, one): return False
    
    intersection = [x for x in Q2 if x in R]
    if not is_same_set(intersection, P2): return False
    return True

def check_neg_Q(witness):
    R = witness['R']
    S = witness['S']
    add = witness['add']
    mul = witness['mul']
    zero = witness['zero']
    one = witness['one']
    P1 = witness['P1']
    Q2 = witness['Q2']
    
    ideals_S = get_all_ideals(S, add, mul, zero)
    for Q1 in ideals_S:
        if is_prime_ideal(Q1, S, add, mul, zero, one):
            is_subset = True
            for x in Q1:
                if x not in Q2:
                    is_subset = False
                    break
            if is_subset:
                intersection = [x for x in Q1 if x in R]
                if is_same_set(intersection, P1):
                    return False
    return True

def conditions(witness) -> list[bool]:
    try:
        h1 = check_H1(witness)
    except Exception:
        h1 = False

    try:
        h2 = check_H2(witness)
    except Exception:
        h2 = False

    try:
        h3 = check_H3(witness)
    except Exception:
        h3 = False

    try:
        h4 = check_H4(witness)
    except Exception:
        h4 = False

    try:
        neg_q = check_neg_Q(witness)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]