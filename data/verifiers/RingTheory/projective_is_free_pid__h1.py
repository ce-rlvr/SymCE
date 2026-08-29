import math
import itertools
import functools
import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.abc
import sympy.polys
import sympy.ntheory
import z3

# Top-level setup: named object bindings that the witness expression may reference.
class ZModRing:
    def __init__(self, n):
        self.n = n
        self.elements = tuple(range(n))
    def add(self, a, b):
        return (a + b) % self.n
    def mul(self, a, b):
        return (a * b) % self.n
    def __str__(self):
        return f"Z/{self.n}Z"

class ZModModule:
    def __init__(self, ring, m):
        self.ring = ring
        self.m = m
        self.elements = tuple(range(m))
    def add(self, a, b):
        return (a + b) % self.m
    def smul(self, r, a):
        return (r * a) % self.m
    def __str__(self):
        return f"Z/{self.m}Z"

Z2 = ZModRing(2)
Z3 = ZModRing(3)
Z4 = ZModRing(4)
Z6 = ZModRing(6)
Z8 = ZModRing(8)

Z2_over_Z6 = ZModModule(Z6, 2)
Z3_over_Z6 = ZModModule(Z6, 3)
Z2_over_Z4 = ZModModule(Z4, 2)

def is_module(R, M):
    try:
        for a in M.elements:
            for b in M.elements:
                if M.add(a, b) not in M.elements: return False
                if M.add(a, b) != M.add(b, a): return False
        
        has_zero = False
        for z in M.elements:
            if all(M.add(a, z) == a for a in M.elements):
                has_zero = True
                break
        if not has_zero: return False
        
        for r in R.elements:
            for a in M.elements:
                if M.smul(r, a) not in M.elements: return False
                
        for r in R.elements:
            for s in R.elements:
                for a in M.elements:
                    if M.smul(R.add(r, s), a) != M.add(M.smul(r, a), M.smul(s, a)): return False
                    if M.smul(R.mul(r, s), a) != M.smul(r, M.smul(s, a)): return False
                    
        for r in R.elements:
            for a in M.elements:
                for b in M.elements:
                    if M.smul(r, M.add(a, b)) != M.add(M.smul(r, a), M.smul(r, b)): return False
                    
        has_one = False
        for e in R.elements:
            if all(R.mul(e, r) == r and R.mul(r, e) == r for r in R.elements):
                if all(M.smul(e, a) == a for a in M.elements):
                    has_one = True
                    break
        if not has_one: return False
        
        return True
    except Exception:
        return False

def is_projective(R, M):
    try:
        zero_M = None
        for z in M.elements:
            if all(M.add(a, z) == a for a in M.elements):
                zero_M = z
                break
        
        gens = None
        for i in range(1, len(M.elements) + 1):
            for subset in itertools.combinations(M.elements, i):
                generated = set()
                for coeffs in itertools.product(R.elements, repeat=i):
                    val = zero_M
                    for c, g in zip(coeffs, subset):
                        val = M.add(val, M.smul(c, g))
                    generated.add(val)
                if len(generated) == len(M.elements):
                    gens = subset
                    break
            if gens is not None:
                break
                
        if gens is None:
            return False
            
        k = len(gens)
        
        def f(vec):
            val = zero_M
            for c, g in zip(vec, gens):
                val = M.add(val, M.smul(c, g))
            return val
            
        zero_R = None
        for z in R.elements:
            if all(R.add(a, z) == a for a in R.elements):
                zero_R = z
                break
        zero_R_k = tuple([zero_R]*k)
        
        reps = {m: [] for m in M.elements}
        for coeffs in itertools.product(R.elements, repeat=k):
            val = f(coeffs)
            reps[val].append(coeffs)
            
        f_inv = [[] for _ in range(k)]
        for vec in itertools.product(R.elements, repeat=k):
            val = f(vec)
            for i, g in enumerate(gens):
                if val == g:
                    f_inv[i].append(vec)
                    
        for h_gens in itertools.product(*f_inv):
            is_well_defined = True
            for m in M.elements:
                m_val = None
                for coeffs in reps[m]:
                    val_h = zero_R_k
                    for c, h_g in zip(coeffs, h_gens):
                        c_hg = tuple(R.mul(c, x) for x in h_g)
                        val_h = tuple(R.add(x, y) for x, y in zip(val_h, c_hg))
                    if m_val is None:
                        m_val = val_h
                    elif m_val != val_h:
                        is_well_defined = False
                        break
                if not is_well_defined:
                    break
            if is_well_defined:
                return True
                
        return False
    except Exception:
        return False

def is_free(R, M):
    try:
        size_R = len(R.elements)
        size_M = len(M.elements)
        if size_R == 0 or size_M == 0: return False
        if size_R == 1:
            return size_M == 1
        
        n = 0
        p = 1
        while p < size_M:
            p *= size_R
            n += 1
        if p != size_M:
            return False
            
        zero_M = None
        for z in M.elements:
            if all(M.add(a, z) == a for a in M.elements):
                zero_M = z
                break
                
        for gens in itertools.product(M.elements, repeat=n):
            generated = set()
            for coeffs in itertools.product(R.elements, repeat=n):
                val = zero_M
                for c, g in zip(coeffs, gens):
                    val = M.add(val, M.smul(c, g))
                generated.add(val)
            if len(generated) == size_M:
                return True
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
        else:
            M = witness
            R = M.ring
            
        if not is_module(R, M):
            return [False, False]
            
        h1 = is_projective(R, M)
        neg_q = not is_free(R, M)
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: M is a projective module over R",
    "¬Q: M is not a free R-module"
]
N_HYP = 1
NEG_Q_INDEX = 1