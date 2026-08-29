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

def conditions(witness):
    try:
        def get_val(w, key):
            if isinstance(w, dict):
                return w[key]
            return getattr(w, key)
            
        mod1 = get_val(witness, 'mod1')
        mod2 = get_val(witness, 'mod2')
        R1 = get_val(witness, 'R1')
        R2 = get_val(witness, 'R2')
        R = get_val(witness, 'R')
        f = get_val(witness, 'f')
        
        def is_comm_ring_with_id(elements, mod):
            if not elements: return False
            if 0 not in elements or 1 not in elements: return False
            for a in elements:
                if (-a) % mod not in elements: return False
                for b in elements:
                    if (a + b) % mod not in elements: return False
                    if (a * b) % mod not in elements: return False
            return True
            
        h1 = is_comm_ring_with_id(R1, mod1) and is_comm_ring_with_id(R2, mod2)
        
        def is_subring(sub, r1_elems, r2_elems, m1, m2):
            if not sub: return False
            if (0,0) not in sub: return False
            for a in sub:
                if a[0] not in r1_elems or a[1] not in r2_elems: return False
                if ((-a[0])%m1, (-a[1])%m2) not in sub: return False
                for b in sub:
                    if ((a[0]+b[0])%m1, (a[1]+b[1])%m2) not in sub: return False
                    if ((a[0]*b[0])%m1, (a[1]*b[1])%m2) not in sub: return False
            return True
            
        h2 = is_subring(R, R1, R2, mod1, mod2) and all(c in R for c in f) and len(f) > 0
        
        def compute_ideal(S, ring, m1, m2):
            ideal = set(S)
            ideal.add((0,0))
            changed = True
            while changed:
                new_elements = set()
                for a in ideal:
                    inv = ((-a[0])%m1, (-a[1])%m2)
                    if inv not in ideal: new_elements.add(inv)
                    for b in ideal:
                        add = ((a[0]+b[0])%m1, (a[1]+b[1])%m2)
                        if add not in ideal: new_elements.add(add)
                    for r in ring:
                        mul = ((r[0]*a[0])%m1, (r[1]*a[1])%m2)
                        if mul not in ideal: new_elements.add(mul)
                if not new_elements:
                    break
                ideal.update(new_elements)
            return ideal
            
        def compute_ideal_1D(S, ring, mod):
            ideal = set(S)
            ideal.add(0)
            changed = True
            while changed:
                new_elements = set()
                for a in ideal:
                    inv = (-a)%mod
                    if inv not in ideal: new_elements.add(inv)
                    for b in ideal:
                        add = (a+b)%mod
                        if add not in ideal: new_elements.add(add)
                    for r in ring:
                        mul = (r*a)%mod
                        if mul not in ideal: new_elements.add(mul)
                if not new_elements:
                    break
                ideal.update(new_elements)
            return ideal
            
        cf = compute_ideal(f, R, mod1, mod2)
        cf1 = compute_ideal_1D([c[0] for c in f], R1, mod1)
        cf2 = compute_ideal_1D([c[1] for c in f], R2, mod2)
        
        cf1_x_cf2 = set((a, b) for a in cf1 for b in cf2)
        
        neg_q = cf != cf1_x_cf2
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R1 and R2 are commutative rings with identity",
    "H_2: f is a polynomial over R where f1 is over R1 and f2 is over R2",
    "¬Q: The content ideal of f in R is not equal to the direct product of the content ideals"
]

N_HYP = 2
NEG_Q_INDEX = 2