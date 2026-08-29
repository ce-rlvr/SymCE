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

class ZnZ:
    def __init__(self, n):
        self.n = n
        self.elements = list(range(n))
        self.zero = 0
        self.one = 1
    def add(self, a, b):
        return (a + b) % self.n
    def mul(self, a, b):
        return (a * b) % self.n
    def eq(self, a, b):
        return (a - b) % self.n == 0
    def __str__(self):
        return f"Z/{self.n}Z"
    def __repr__(self):
        return f"ZnZ({self.n})"

def is_comm_ring_with_id(A):
    try:
        elements = A.elements
        zero = A.zero
        one = A.one
        for x in elements:
            if not A.eq(A.add(x, zero), x): return False
            if not A.eq(A.add(zero, x), x): return False
            if not A.eq(A.mul(x, one), x): return False
            if not A.eq(A.mul(one, x), x): return False
            
            has_inv = False
            for y in elements:
                if A.eq(A.add(x, y), zero) and A.eq(A.add(y, x), zero):
                    has_inv = True
                    break
            if not has_inv: return False
            
            for y in elements:
                if not A.eq(A.add(x, y), A.add(y, x)): return False
                if not A.eq(A.mul(x, y), A.mul(y, x)): return False
                for z in elements:
                    if not A.eq(A.add(A.add(x, y), z), A.add(x, A.add(y, z))): return False
                    if not A.eq(A.mul(A.mul(x, y), z), A.mul(x, A.mul(y, z))): return False
                    if not A.eq(A.mul(x, A.add(y, z)), A.add(A.mul(x, y), A.mul(x, z))): return False
                    if not A.eq(A.mul(A.add(x, y), z), A.add(A.mul(x, z), A.mul(y, z))): return False
        return True
    except Exception:
        return False

def is_mult_closed(R, S):
    try:
        for s in S:
            if s not in R.elements: return False
        for s1 in S:
            for s2 in S:
                if R.mul(s1, s2) not in S: return False
        return True
    except Exception:
        return False

def is_ring_hom(R, T, f):
    try:
        def eval_f(x):
            return f[x] if isinstance(f, dict) else f(x)
        
        if not T.eq(eval_f(R.one), T.one): return False
        for x in R.elements:
            for y in R.elements:
                if not T.eq(eval_f(R.add(x, y)), T.add(eval_f(x), eval_f(y))): return False
                if not T.eq(eval_f(R.mul(x, y)), T.mul(eval_f(x), eval_f(y))): return False
        return True
    except Exception:
        return False

def is_canonical_localization(R, S, S_inv_R, phi):
    try:
        if not is_comm_ring_with_id(S_inv_R): return False
        
        def eval_phi(x):
            return phi[x] if isinstance(phi, dict) else phi(x)
        
        if not is_ring_hom(R, S_inv_R, phi): return False
        
        for s in S:
            phi_s = eval_phi(s)
            is_unit = False
            for x in S_inv_R.elements:
                if S_inv_R.eq(S_inv_R.mul(phi_s, x), S_inv_R.one):
                    is_unit = True
                    break
            if not is_unit: return False
            
        for x in S_inv_R.elements:
            can_be_written = False
            for r in R.elements:
                for s in S:
                    if S_inv_R.eq(S_inv_R.mul(x, eval_phi(s)), eval_phi(r)):
                        can_be_written = True
                        break
                if can_be_written: break
            if not can_be_written: return False
            
        for r in R.elements:
            phi_r_is_zero = S_inv_R.eq(eval_phi(r), S_inv_R.zero)
            exists_u = False
            for u in S:
                if R.eq(R.mul(u, r), R.zero):
                    exists_u = True
                    break
            if phi_r_is_zero != exists_u: return False
            
        return True
    except Exception:
        return False

def count_valid_g(R, T, S, f, S_inv_R, phi):
    try:
        def eval_f(x): return f[x] if isinstance(f, dict) else f(x)
        def eval_phi(x): return phi[x] if isinstance(phi, dict) else phi(x)
        
        g_partial = []
        for r in R.elements:
            pr = eval_phi(r)
            fr = eval_f(r)
            found = False
            for (x, t) in g_partial:
                if S_inv_R.eq(x, pr):
                    if not T.eq(t, fr):
                        return 0
                    found = True
                    break
            if not found:
                g_partial.append((pr, fr))
                
        unassigned_elements = []
        for x in S_inv_R.elements:
            is_assigned = False
            for (ax, at) in g_partial:
                if S_inv_R.eq(x, ax):
                    is_assigned = True
                    break
            if not is_assigned:
                unassigned_elements.append(x)
                
        domain_choices = []
        for x in unassigned_elements:
            choices = []
            for t in T.elements:
                consistent = True
                for r in R.elements:
                    for s in S:
                        if S_inv_R.eq(S_inv_R.mul(x, eval_phi(s)), eval_phi(r)):
                            if not T.eq(T.mul(t, eval_f(s)), eval_f(r)):
                                consistent = False
                                break
                    if not consistent: break
                if consistent:
                    choices.append(t)
            domain_choices.append((x, choices))
            if not choices:
                return 0
                
        valid_g_count = 0
        
        def backtrack(idx):
            nonlocal valid_g_count
            if idx == len(domain_choices):
                g_one = None
                for (ax, at) in g_partial:
                    if S_inv_R.eq(ax, S_inv_R.one):
                        g_one = at
                        break
                if g_one is None or not T.eq(g_one, T.one): return
                
                for x in S_inv_R.elements:
                    for y in S_inv_R.elements:
                        gx = gy = gxy_add = gxy_mul = None
                        xy_add = S_inv_R.add(x, y)
                        xy_mul = S_inv_R.mul(x, y)
                        for (ax, at) in g_partial:
                            if S_inv_R.eq(ax, x): gx = at
                            if S_inv_R.eq(ax, y): gy = at
                            if S_inv_R.eq(ax, xy_add): gxy_add = at
                            if S_inv_R.eq(ax, xy_mul): gxy_mul = at
                        
                        if not T.eq(gxy_add, T.add(gx, gy)): return
                        if not T.eq(gxy_mul, T.mul(gx, gy)): return
                valid_g_count += 1
                return
                
            x, choices = domain_choices[idx]
            for t in choices:
                g_partial.append((x, t))
                backtrack(idx + 1)
                g_partial.pop()
                
        backtrack(0)
        return valid_g_count
    except Exception:
        return -1

def conditions(witness):
    try:
        R = witness['R']
        T = witness['T']
        S = witness['S']
        f = witness['f']
        S_inv_R = witness['S_inv_R']
        phi = witness['phi']
    except Exception:
        return [False] * 5

    h1 = is_comm_ring_with_id(R) and is_comm_ring_with_id(T)
    h2 = is_mult_closed(R, S)
    h3 = is_ring_hom(R, T, f)
    h4 = is_canonical_localization(R, S, S_inv_R, phi)
    
    try:
        num_g = count_valid_g(R, T, S, f, S_inv_R, phi)
        if num_g == -1:
            neg_q = False
        else:
            neg_q = (num_g != 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R and T are commutative rings with identity",
    "H_2: S is a multiplicatively closed subset of R",
    "H_3: f is a ring homomorphism from R to T",
    "H_4: phi is the canonical localization map from R to S^{-1}R",
    "¬Q: There is no unique ring homomorphism g: S^{-1}R -> T such that f = g \circ phi"
]

N_HYP = 4
NEG_Q_INDEX = 4