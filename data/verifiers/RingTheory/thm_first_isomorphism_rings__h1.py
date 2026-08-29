import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

# Top-level setup for potential witness objects
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
    def __init__(self, r):
        self.r = r
        self._elements = None

    @property
    def elements(self):
        if self._elements is not None:
            return self._elements
        if hasattr(self.r, 'elements'): 
            self._elements = list(self.r.elements)
        elif isinstance(self.r, dict): 
            self._elements = list(self.r['elements'])
        else:
            self._elements = list(self.r)
        return self._elements

    def add(self, x, y):
        if hasattr(self.r, 'add'): return self.r.add(x, y)
        if isinstance(self.r, dict): return self.r['add'](x, y)
        return x + y

    def mul(self, x, y):
        if hasattr(self.r, 'mul'): return self.r.mul(x, y)
        if isinstance(self.r, dict): return self.r['mul'](x, y)
        return x * y

    @property
    def zero(self):
        if hasattr(self.r, 'zero'): return self.r.zero
        if isinstance(self.r, dict): return self.r['zero']
        return 0

    @property
    def one(self):
        if hasattr(self.r, 'one'): return self.r.one
        if isinstance(self.r, dict): return self.r.get('one')
        return None

class WitnessWrapper:
    def __init__(self, w):
        if isinstance(w, tuple) and len(w) == 3:
            self.R = RingWrapper(w[0])
            self.S = RingWrapper(w[1])
            self._f = w[2]
        else:
            if hasattr(w, 'R'): self.R = RingWrapper(w.R)
            elif isinstance(w, dict): self.R = RingWrapper(w['R'])
            
            if hasattr(w, 'S'): self.S = RingWrapper(w.S)
            elif isinstance(w, dict): self.S = RingWrapper(w['S'])
            
            if hasattr(w, 'f'): self._f = w.f
            elif isinstance(w, dict): self._f = w['f']

    def f(self, x):
        if isinstance(self._f, dict): return self._f[x]
        return self._f(x)

def conditions(witness) -> list[bool]:
    try:
        w = WitnessWrapper(witness)
    except Exception:
        return [False, False]

    def check_h1():
        try:
            R_elems = []
            for x in w.R.elements:
                if x not in R_elems:
                    R_elems.append(x)
                    
            if w.f(w.R.zero) != w.S.zero: 
                return False
                
            r_one = w.R.one
            s_one = w.S.one
            if r_one is not None and s_one is not None:
                if w.f(r_one) != s_one: 
                    return False
                    
            for x in R_elems:
                for y in R_elems:
                    if w.f(w.R.add(x, y)) != w.S.add(w.f(x), w.f(y)): 
                        return False
                    if w.f(w.R.mul(x, y)) != w.S.mul(w.f(x), w.f(y)): 
                        return False
            return True
        except Exception:
            return False

    def check_neg_q():
        try:
            R_elems = []
            for x in w.R.elements:
                if x not in R_elems:
                    R_elems.append(x)
                    
            K = [k for k in R_elems if w.f(k) == w.S.zero]
            cosets = []
            for x in R_elems:
                coset = []
                for k in K:
                    val = w.R.add(x, k)
                    if val not in coset:
                        coset.append(val)
                is_new = True
                for c in cosets:
                    if len(c) == len(coset) and all(v in c for v in coset):
                        is_new = False
                        break
                if is_new:
                    cosets.append(coset)
                    
            union = []
            for c in cosets:
                for v in c:
                    if v in union:
                        return True
                    union.append(v)
            if len(union) != len(R_elems):
                return True
                
            def get_coset_idx(val):
                for i, c in enumerate(cosets):
                    if val in c: return i
                return None
                
            for i in range(len(cosets)):
                for j in range(len(cosets)):
                    adds = []
                    muls = []
                    for x in cosets[i]:
                        for y in cosets[j]:
                            a_idx = get_coset_idx(w.R.add(x, y))
                            m_idx = get_coset_idx(w.R.mul(x, y))
                            if a_idx not in adds: adds.append(a_idx)
                            if m_idx not in muls: muls.append(m_idx)
                    if len(adds) > 1 or None in adds:
                        return True
                    if len(muls) > 1 or None in muls:
                        return True
                        
            f_R = []
            for x in R_elems:
                fx = w.f(x)
                if fx not in f_R:
                    f_R.append(fx)
                    
            if len(cosets) != len(f_R):
                return True
                
            for p in itertools.permutations(f_R):
                mapping = {i: p[i] for i in range(len(cosets))}
                is_iso = True
                for i in range(len(cosets)):
                    for j in range(len(cosets)):
                        x = cosets[i][0]
                        y = cosets[j][0]
                        c_add_idx = get_coset_idx(w.R.add(x, y))
                        c_mul_idx = get_coset_idx(w.R.mul(x, y))
                        
                        if mapping[c_add_idx] != w.S.add(mapping[i], mapping[j]):
                            is_iso = False
                            break
                        if mapping[c_mul_idx] != w.S.mul(mapping[i], mapping[j]):
                            is_iso = False
                            break
                    if not is_iso:
                        break
                if is_iso:
                    return False
            return True
        except Exception:
            return False

    return [check_h1(), check_neg_q()]

CONDITION_LABELS = [
    "H_1: f is a ring homomorphism from R to S",
    "¬Q: The quotient ring R/ker(f) is NOT isomorphic to the image f(R)"
]

N_HYP = 1
NEG_Q_INDEX = 1