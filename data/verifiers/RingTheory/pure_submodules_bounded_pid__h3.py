import math
from itertools import product
from sympy.ntheory import factorint
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def get_elementary_divisors(inv_factors):
    ed = []
    for d in inv_factors:
        if d > 1:
            factors = factorint(d)
            for p, exp in factors.items():
                ed.append(p**exp)
    return sorted(ed)

def get_invariant_factors_generic(elements, identity, add_func):
    inv_factors = []
    kernel = set([identity])
    
    while len(kernel) < len(elements):
        max_order = 0
        max_elem = None
        for e in elements:
            if e in kernel:
                continue
            curr = e
            order = 1
            while curr not in kernel:
                curr = add_func(curr, e)
                order += 1
            if order > max_order:
                max_order = order
                max_elem = e
                
        inv_factors.append(max_order)
        
        new_kernel = set(kernel)
        for k in kernel:
            curr = add_func(k, max_elem)
            for _ in range(1, max_order):
                new_kernel.add(curr)
                curr = add_func(curr, max_elem)
        kernel = new_kernel
        
    return inv_factors

def is_direct_summand(M_invs, N_gens):
    ranges = [range(m) for m in M_invs]
    M_elements = list(product(*ranges))
    
    N_elements = set([(0,)*len(M_invs)])
    queue = [(0,)*len(M_invs)]
    while queue:
        curr = queue.pop(0)
        for g in N_gens:
            nxt = tuple((curr[i] + g[i]) % M_invs[i] for i in range(len(M_invs)))
            if nxt not in N_elements:
                N_elements.add(nxt)
                queue.append(nxt)
                
    quotient_cosets = []
    seen = set()
    for e in M_elements:
        if e not in seen:
            coset = set()
            for n in N_elements:
                coset.add(tuple((e[i] + n[i]) % M_invs[i] for i in range(len(M_invs))))
            rep = tuple(sorted(list(coset)))
            quotient_cosets.append(rep)
            seen.update(coset)
            
    ed_M = get_elementary_divisors(M_invs)
    
    def add_N(x, y):
        return tuple((a + b) % m for a, b, m in zip(x, y, M_invs))
    invs_N = get_invariant_factors_generic(N_elements, (0,)*len(M_invs), add_N)
    ed_N = get_elementary_divisors(invs_N)
    
    def add_MN(c1, c2):
        e1 = c1[0]
        e2 = c2[0]
        s = tuple((a + b) % m for a, b, m in zip(e1, e2, M_invs))
        return tuple(sorted([tuple((s[i] + n[i]) % M_invs[i] for i in range(len(M_invs))) for n in N_elements]))
    
    id_coset = tuple(sorted([tuple(n) for n in N_elements]))
    invs_MN = get_invariant_factors_generic(quotient_cosets, id_coset, add_MN)
    ed_MN = get_elementary_divisors(invs_MN)
    
    ed_union = sorted(ed_N + ed_MN)
    return ed_M == ed_union

def h1(witness):
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return False
        return True
    except Exception:
        return False

def h2(witness):
    try:
        if not h1(witness):
            return False
        M_invs, N_gens = witness
        if not isinstance(M_invs, list):
            return False
        if not all(isinstance(m, int) and m >= 1 for m in M_invs):
            return False
        size = 1
        for m in M_invs:
            size *= m
        if size > 2000:
            return False
        if not isinstance(N_gens, list):
            return False
        for g in N_gens:
            if not isinstance(g, tuple) or len(g) != len(M_invs):
                return False
            if not all(isinstance(x, int) for x in g):
                return False
        return True
    except Exception:
        return False

def neg_q(witness):
    try:
        if not h2(witness):
            return False
        M_invs, N_gens = witness
        return not is_direct_summand(M_invs, N_gens)
    except Exception:
        return False

def conditions(witness):
    return [h1(witness), h2(witness), neg_q(witness)]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: M is a bounded R-module",
    "¬Q: N is not a direct summand of M"
]

N_HYP = 2
NEG_Q_INDEX = 2