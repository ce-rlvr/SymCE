import itertools
import functools
import math
import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy import eye, zeros, Rational, Integer

# Top-level setup for potential witness expressions
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

def is_directed_set(poset, le):
    for x in poset:
        if (x, x) not in le: return False
    for x in poset:
        for y in poset:
            for z in poset:
                if (x, y) in le and (y, z) in le:
                    if (x, z) not in le: return False
    for x in poset:
        for y in poset:
            found = False
            for z in poset:
                if (x, z) in le and (y, z) in le:
                    found = True
                    break
            if not found: return False
    return True

def check_H1(witness):
    poset = witness['poset']
    le = witness['le']
    if not poset: return False
    if not is_directed_set(poset, le): return False
    R_n = witness['R_n']
    for i in poset:
        if R_n[i] <= 0: return False
    for (i, j) in le:
        if R_n[i] % R_n[j] != 0: return False
    return True

def check_H2(witness):
    poset = witness['poset']
    le = witness['le']
    R_n = witness['R_n']
    S_i = witness['S_i']
    for i in poset:
        S = S_i[i]
        n = R_n[i]
        if 1 not in S: return False
        for a in S:
            if not (0 <= a < n): return False
            for b in S:
                if (a * b) % n not in S: return False
    for (i, j) in le:
        n_j = R_n[j]
        for x in S_i[i]:
            if (x % n_j) not in S_i[j]: return False
    return True

def get_S_limit(witness):
    poset = witness['poset']
    le = witness['le']
    R_n = witness['R_n']
    S_i = witness['S_i']
    
    elements = []
    for i in poset:
        for x in S_i[i]:
            elements.append((i, x))
            
    def equiv(e1, e2):
        i, x = e1
        j, y = e2
        for k in poset:
            if (i, k) in le and (j, k) in le:
                if x % R_n[k] == y % R_n[k]:
                    return True
        return False

    classes = []
    for e in elements:
        found = False
        for c in classes:
            if equiv(e, c[0]):
                c.append(e)
                found = True
                break
        if not found:
            classes.append([e])
            
    n_classes = len(classes)
    mul_table = {}
    for c1_idx, c1 in enumerate(classes):
        for c2_idx, c2 in enumerate(classes):
            i, x = c1[0]
            j, y = c2[0]
            k = next(k for k in poset if (i, k) in le and (j, k) in le)
            prod_val = (x * y) % R_n[k]
            prod_e = (k, prod_val)
            for c3_idx, c3 in enumerate(classes):
                if equiv(prod_e, c3[0]):
                    mul_table[(c1_idx, c2_idx)] = c3_idx
                    break
    return n_classes, mul_table

def check_H3(witness):
    n_classes, limit_mul = get_S_limit(witness)
    S_target = witness['S_target']
    R_target_n = witness['R_target_n']
    
    if len(S_target) != n_classes:
        return False
        
    if 1 not in S_target: return False
    for x in S_target:
        if not (0 <= x < R_target_n): return False
        for y in S_target:
            if (x * y) % R_target_n not in S_target:
                return False
                
    if n_classes > 10:
        return False
        
    for p in itertools.permutations(S_target):
        is_hom = True
        for c1 in range(n_classes):
            for c2 in range(n_classes):
                c3 = limit_mul[(c1, c2)]
                if (p[c1] * p[c2]) % R_target_n != p[c3]:
                    is_hom = False
                    break
            if not is_hom: break
        if is_hom:
            return True
    return False

def get_localized_ring(R_n, S):
    elements = [(r, s) for r in range(R_n) for s in S]
    def equiv(e1, e2):
        r1, s1 = e1
        r2, s2 = e2
        for t in S:
            if (t * (r1 * s2 - r2 * s1)) % R_n == 0:
                return True
        return False
        
    classes = []
    for e in elements:
        found = False
        for c in classes:
            if equiv(e, c[0]):
                c.append(e)
                found = True
                break
        if not found:
            classes.append([e])
            
    n_classes = len(classes)
    if n_classes > 10:
        raise ValueError("Ring too large for fast isomorphism check")
        
    add_table = {}
    mul_table = {}
    for c1_idx, c1 in enumerate(classes):
        for c2_idx, c2 in enumerate(classes):
            r1, s1 = c1[0]
            r2, s2 = c2[0]
            
            sum_r = (r1 * s2 + r2 * s1) % R_n
            sum_s = (s1 * s2) % R_n
            sum_e = (sum_r, sum_s)
            
            prod_r = (r1 * r2) % R_n
            prod_s = (s1 * s2) % R_n
            prod_e = (prod_r, prod_s)
            
            for c3_idx, c3 in enumerate(classes):
                if equiv(sum_e, c3[0]):
                    add_table[(c1_idx, c2_idx)] = c3_idx
                if equiv(prod_e, c3[0]):
                    mul_table[(c1_idx, c2_idx)] = c3_idx
                    
    return n_classes, add_table, mul_table, classes

def get_limit_of_localized_rings(witness):
    poset = witness['poset']
    le = witness['le']
    R_n = witness['R_n']
    S_i = witness['S_i']
    
    loc_rings = {}
    for i in poset:
        loc_rings[i] = get_localized_ring(R_n[i], S_i[i])
        
    elements = []
    for i in poset:
        n_classes, _, _, classes = loc_rings[i]
        for c_idx in range(n_classes):
            elements.append((i, classes[c_idx][0]))
            
    def equiv(e1, e2):
        i, (r1, s1) = e1
        j, (r2, s2) = e2
        for k in poset:
            if (i, k) in le and (j, k) in le:
                n_k = R_n[k]
                S_k = S_i[k]
                rk1, sk1 = r1 % n_k, s1 % n_k
                rk2, sk2 = r2 % n_k, s2 % n_k
                for t in S_k:
                    if (t * (rk1 * sk2 - rk2 * sk1)) % n_k == 0:
                        return True
        return False

    classes = []
    for e in elements:
        found = False
        for c in classes:
            if equiv(e, c[0]):
                c.append(e)
                found = True
                break
        if not found:
            classes.append([e])
            
    n_classes = len(classes)
    if n_classes > 10:
        raise ValueError("Ring too large for fast isomorphism check")
        
    add_table = {}
    mul_table = {}
    for c1_idx, c1 in enumerate(classes):
        for c2_idx, c2 in enumerate(classes):
            i, (r1, s1) = c1[0]
            j, (r2, s2) = c2[0]
            
            k = next(k for k in poset if (i, k) in le and (j, k) in le)
            n_k = R_n[k]
            rk1, sk1 = r1 % n_k, s1 % n_k
            rk2, sk2 = r2 % n_k, s2 % n_k
            
            sum_r = (rk1 * sk2 + rk2 * sk1) % n_k
            sum_s = (sk1 * sk2) % n_k
            sum_e = (k, (sum_r, sum_s))
            
            prod_r = (rk1 * rk2) % n_k
            prod_s = (sk1 * sk2) % n_k
            prod_e = (k, (prod_r, prod_s))
            
            for c3_idx, c3 in enumerate(classes):
                if equiv(sum_e, c3[0]):
                    add_table[(c1_idx, c2_idx)] = c3_idx
                if equiv(prod_e, c3[0]):
                    mul_table[(c1_idx, c2_idx)] = c3_idx
                    
    return n_classes, add_table, mul_table

def are_rings_isomorphic(ring1, ring2):
    n1, add1, mul1 = ring1
    n2, add2, mul2 = ring2
    if n1 != n2: return False
    
    for p in itertools.permutations(range(n1)):
        is_iso = True
        for i in range(n1):
            for j in range(n1):
                if p[add1[(i, j)]] != add2[(p[i], p[j])]:
                    is_iso = False
                    break
                if p[mul1[(i, j)]] != mul2[(p[i], p[j])]:
                    is_iso = False
                    break
            if not is_iso: break
        if is_iso:
            return True
    return False

def check_neg_Q(witness):
    limit_ring = get_limit_of_localized_rings(witness)
    
    R_target_n = witness['R_target_n']
    S_target = witness['S_target']
    loc_target = get_localized_ring(R_target_n, S_target)
    target_ring = (loc_target[0], loc_target[1], loc_target[2])
    
    return not are_rings_isomorphic(limit_ring, target_ring)

def conditions(witness):
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
        neg_q = check_neg_Q(witness)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: (R_i, phi_{ij}) is a directed system of commutative rings",
    "H_2: S_i are multiplicative subsets compatible with phi_{ij}",
    "H_3: S is the direct limit of S_i",
    "¬Q: The direct limit of S_i^{-1}R_i is NOT isomorphic to S^{-1}R"
]

N_HYP = 3
NEG_Q_INDEX = 3