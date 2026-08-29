import itertools
import functools
import math
import sympy
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

class RingWrapper:
    def __init__(self, witness):
        self.R = list(witness.R)
        self.S = list(witness.S)
        self.P = list(witness.P)
        self._add = getattr(witness, 'add', None)
        self._mul = getattr(witness, 'mul', None)
        
    def add(self, a, b):
        if self._add: return self._add(a, b)
        return a + b
        
    def mul(self, a, b):
        if self._mul: return self._mul(a, b)
        return a * b
        
    def eq(self, a, b):
        return a == b

class FastRing:
    def __init__(self, rw):
        self.R_orig = []
        for r in rw.R:
            if not any(rw.eq(r, x) for x in self.R_orig):
                self.R_orig.append(r)
                
        self.n = len(self.R_orig)
        self.R = list(range(self.n))
        
        self.S_valid = True
        self.S = []
        for s in rw.S:
            found = False
            for i, r in enumerate(self.R_orig):
                if rw.eq(s, r):
                    if i not in self.S: self.S.append(i)
                    found = True
                    break
            if not found: self.S_valid = False
                    
        self.P_valid = True
        self.P = []
        for p in rw.P:
            found = False
            for i, r in enumerate(self.R_orig):
                if rw.eq(p, r):
                    if i not in self.P: self.P.append(i)
                    found = True
                    break
            if not found: self.P_valid = False
                    
        self.add_table = [[0]*self.n for _ in range(self.n)]
        self.mul_table = [[0]*self.n for _ in range(self.n)]
        
        self.valid = True
        for i in range(self.n):
            for j in range(self.n):
                res_add = rw.add(self.R_orig[i], self.R_orig[j])
                res_mul = rw.mul(self.R_orig[i], self.R_orig[j])
                
                idx_add = -1
                idx_mul = -1
                for k in range(self.n):
                    if rw.eq(res_add, self.R_orig[k]): idx_add = k
                    if rw.eq(res_mul, self.R_orig[k]): idx_mul = k
                    
                if idx_add == -1 or idx_mul == -1:
                    self.valid = False
                self.add_table[i][j] = idx_add
                self.mul_table[i][j] = idx_mul
                
        self.zero = None
        for i in range(self.n):
            if all(self.add_table[i][j] == j for j in range(self.n)):
                self.zero = i
                break

def check_H1(fr):
    if not fr.valid or not fr.S_valid: return False
    for s1 in fr.S:
        for s2 in fr.S:
            if fr.mul_table[s1][s2] not in fr.S: return False
    return True

def check_H2(fr):
    if not fr.valid or not fr.P_valid: return False
    
    for p in fr.P:
        if p in fr.S: return False
        
    if fr.zero is None: return False
    if not fr.P: return False
    
    for p1 in fr.P:
        for p2 in fr.P:
            if fr.add_table[p1][p2] not in fr.P: return False
            
    for p in fr.P:
        for r in fr.R:
            if fr.mul_table[r][p] not in fr.P: return False
            if fr.mul_table[p][r] not in fr.P: return False
            
    if len(fr.P) == fr.n: return False
    
    ideals = {}
    for x in fr.R:
        ideal = [x]
        while True:
            added = False
            for a in ideal.copy():
                for r in fr.R:
                    ra = fr.mul_table[r][a]
                    if ra not in ideal:
                        ideal.append(ra)
                        added = True
                    ar = fr.mul_table[a][r]
                    if ar not in ideal:
                        ideal.append(ar)
                        added = True
                for b in ideal.copy():
                    ab = fr.add_table[a][b]
                    if ab not in ideal:
                        ideal.append(ab)
                        added = True
            for a in ideal.copy():
                for r in fr.R:
                    if fr.add_table[a][r] == fr.zero:
                        if r not in ideal:
                            ideal.append(r)
                            added = True
                        break
            if not added:
                break
        ideals[x] = ideal
        
    for x in fr.R:
        if x in fr.P: continue
        for y in fr.R:
            if y in fr.P: continue
            
            subset = True
            Ix = ideals[x]
            Iy = ideals[y]
            for a in Ix:
                for b in Iy:
                    if fr.mul_table[a][b] not in fr.P:
                        subset = False
                        break
                if not subset:
                    break
            if subset:
                return False
    return True

def is_left_ore(fr):
    for r in fr.R:
        for s in fr.S:
            found = False
            for r_prime in fr.R:
                for s_prime in fr.S:
                    if fr.mul_table[s_prime][r] == fr.mul_table[r_prime][s]:
                        found = True
                        break
                if found: break
            if not found: return False
            
    for r in fr.R:
        for s in fr.S:
            if fr.mul_table[r][s] == fr.zero:
                found = False
                for s_prime in fr.S:
                    if fr.mul_table[s_prime][r] == fr.zero:
                        found = True
                        break
                if not found: return False
    return True

def get_classes(fr):
    pairs = [(s, r) for s in fr.S for r in fr.R]
    classes = []
    for p in pairs:
        already_in = False
        for c in classes:
            if p in c:
                already_in = True
                break
        if already_in: continue
        
        found = False
        for c in classes:
            s1, r1 = p
            s2, r2 = c[0]
            equiv = False
            for u1 in fr.R:
                for u2 in fr.R:
                    u1s1 = fr.mul_table[u1][s1]
                    u2s2 = fr.mul_table[u2][s2]
                    if u1s1 == u2s2 and u1s1 in fr.S:
                        u1r1 = fr.mul_table[u1][r1]
                        u2r2 = fr.mul_table[u2][r2]
                        if u1r1 == u2r2:
                            equiv = True
                            break
                if equiv: break
            if equiv:
                c.append(p)
                found = True
                break
        if not found:
            classes.append([p])
    return classes

def add_loc(fr, p1, p2):
    s1, r1 = p1
    s2, r2 = p2
    for u1 in fr.R:
        for u2 in fr.R:
            u1s1 = fr.mul_table[u1][s1]
            u2s2 = fr.mul_table[u2][s2]
            if u1s1 == u2s2 and u1s1 in fr.S:
                u1r1 = fr.mul_table[u1][r1]
                u2r2 = fr.mul_table[u2][r2]
                return (u1s1, fr.add_table[u1r1][u2r2])
    return None

def mul_loc(fr, p1, p2):
    s1, r1 = p1
    s2, r2 = p2
    for u in fr.R:
        for v in fr.S:
            us2 = fr.mul_table[u][s2]
            vr1 = fr.mul_table[v][r1]
            if us2 == vr1:
                vs1 = fr.mul_table[v][s1]
                ur2 = fr.mul_table[u][r2]
                return (vs1, ur2)
    return None

def get_class_index(classes, p):
    for i, c in enumerate(classes):
        if p in c:
            return i
    return -1

def build_loc_ring(fr, classes):
    n = len(classes)
    add_table = [[0]*n for _ in range(n)]
    mul_table = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            p1 = classes[i][0]
            p2 = classes[j][0]
            
            p_add = add_loc(fr, p1, p2)
            if p_add is None: return None, None
            idx_add = get_class_index(classes, p_add)
            if idx_add == -1: return None, None
            add_table[i][j] = idx_add
            
            p_mul = mul_loc(fr, p1, p2)
            if p_mul is None: return None, None
            idx_mul = get_class_index(classes, p_mul)
            if idx_mul == -1: return None, None
            mul_table[i][j] = idx_mul
    return add_table, mul_table

def is_ideal_loc(n, add_table, mul_table, I):
    if not I: return False
    for i in I:
        for j in I:
            if add_table[i][j] not in I: return False
    for i in I:
        for r in range(n):
            if mul_table[r][i] not in I: return False
            if mul_table[i][r] not in I: return False
    return True

def is_prime_ideal_loc(n, add_table, mul_table, I):
    if len(I) == n: return False
    
    ideals = {}
    zero = None
    for i in range(n):
        if all(add_table[i][j] == j for j in range(n)):
            zero = i
            break
    if zero is None: return False
            
    for x in range(n):
        ideal = [x]
        while True:
            added = False
            for a in ideal.copy():
                for r in range(n):
                    ra = mul_table[r][a]
                    if ra not in ideal:
                        ideal.append(ra)
                        added = True
                    ar = mul_table[a][r]
                    if ar not in ideal:
                        ideal.append(ar)
                        added = True
                for b in ideal.copy():
                    ab = add_table[a][b]
                    if ab not in ideal:
                        ideal.append(ab)
                        added = True
            for a in ideal.copy():
                for r in range(n):
                    if add_table[a][r] == zero:
                        if r not in ideal:
                            ideal.append(r)
                            added = True
                        break
            if not added:
                break
        ideals[x] = ideal
        
    for x in range(n):
        if x in I: continue
        for y in range(n):
            if y in I: continue
            
            subset = True
            Ix = ideals[x]
            Iy = ideals[y]
            for a in Ix:
                for b in Iy:
                    if mul_table[a][b] not in I:
                        subset = False
                        break
                if not subset:
                    break
            if subset:
                return False
    return True

def check_neg_Q(fr):
    if not fr.valid: return True
    if not is_left_ore(fr): return True
        
    classes = get_classes(fr)
    n = len(classes)
    
    add_table, mul_table = build_loc_ring(fr, classes)
    if add_table is None: return True
        
    S_inv_P = []
    for i, c in enumerate(classes):
        in_P = False
        for s, r in c:
            if r in fr.P:
                in_P = True
                break
        if in_P:
            S_inv_P.append(i)
            
    if not is_ideal_loc(n, add_table, mul_table, S_inv_P):
        return True
        
    if not is_prime_ideal_loc(n, add_table, mul_table, S_inv_P):
        return True
        
    return False

def conditions(witness):
    try:
        rw = RingWrapper(witness)
        fr = FastRing(rw)
    except Exception:
        return [False, False, False]
        
    try:
        h1 = check_H1(fr)
    except Exception:
        h1 = False
        
    try:
        h2 = check_H2(fr)
    except Exception:
        h2 = False
        
    try:
        neg_q = check_neg_Q(fr)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is a multiplicatively closed subset of R",
    "H_2: P is a prime ideal of R such that P \\cap S = \\emptyset",
    "¬Q: The extended ideal S^{-1}P is not a prime ideal in the localized ring S^{-1}R"
]

N_HYP = 2
NEG_Q_INDEX = 2