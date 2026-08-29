import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

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
    "H_1: N and H are groups",
    "H_2: There exists an automorphism beta in Aut(H) such that psi = phi o beta",
    "¬Q: The semidirect products N rtimes_phi H and N rtimes_psi H are not isomorphic"
]

N_HYP = 2
NEG_Q_INDEX = 2

def call_map(m, h, n):
    try:
        return m(h, n)
    except Exception:
        pass
    try:
        return m(h)(n)
    except Exception:
        pass
    try:
        return m[h][n]
    except Exception:
        pass
    try:
        return m[h](n)
    except Exception:
        pass
    raise ValueError("Cannot call map")

def call_beta(beta, h):
    try:
        return beta(h)
    except Exception:
        pass
    try:
        return beta[h]
    except Exception:
        pass
    raise ValueError("Cannot call beta")

def call_mul(mul, a, b):
    try:
        return mul(a, b)
    except Exception:
        pass
    try:
        return mul[(a, b)]
    except Exception:
        pass
    try:
        return mul[a][b]
    except Exception:
        pass
    raise ValueError("Cannot call mul")

def get_mul(witness, group_name):
    if hasattr(witness, f'mul_{group_name}'):
        return getattr(witness, f'mul_{group_name}')
    return lambda a, b: a * b

def is_group(elements, mul):
    n = len(elements)
    for a in elements:
        for b in elements:
            try:
                c = mul(a, b)
                if c not in elements:
                    return False
            except Exception:
                return False
    for a in elements:
        for b in elements:
            ab = mul(a, b)
            for c in elements:
                if mul(ab, c) != mul(a, mul(b, c)):
                    return False
    identity = None
    for e in elements:
        is_id = True
        for a in elements:
            if mul(e, a) != a or mul(a, e) != a:
                is_id = False
                break
        if is_id:
            identity = e
            break
    if identity is None:
        return False
    for a in elements:
        has_inv = False
        for b in elements:
            if mul(a, b) == identity and mul(b, a) == identity:
                has_inv = True
                break
        if not has_inv:
            return False
    return True

def are_isomorphic_groups(elements1, mul1, elements2, mul2):
    if not is_group(elements1, mul1):
        return False
    if not is_group(elements2, mul2):
        return False
        
    if len(elements1) != len(elements2):
        return False
    n = len(elements1)
    
    id1 = None
    for e in elements1:
        if all(mul1(e, a) == a for a in elements1):
            id1 = e
            break
    id2 = None
    for e in elements2:
        if all(mul2(e, a) == a for a in elements2):
            id2 = e
            break
            
    def get_order(a, elements, mul, identity):
        curr = a
        order = 1
        while curr != identity and order <= n:
            curr = mul(curr, a)
            order += 1
        return order

    elements1_without_id = [x for x in elements1 if x != id1]
    elements2_without_id = [x for x in elements2 if x != id2]

    orders1 = {a: get_order(a, elements1, mul1, id1) for a in elements1_without_id}
    orders2 = {a: get_order(a, elements2, mul2, id2) for a in elements2_without_id}
    
    if sorted(orders1.values()) != sorted(orders2.values()):
        return False
        
    by_order1 = {}
    for a, o in orders1.items():
        by_order1.setdefault(o, []).append(a)
    by_order2 = {}
    for a, o in orders2.items():
        by_order2.setdefault(o, []).append(a)
        
    perms_per_order = []
    for o in by_order1:
        perms_per_order.append(itertools.permutations(by_order2[o]))
        
    for p_tuple in itertools.product(*perms_per_order):
        mapping = {id1: id2}
        for o, p in zip(by_order1.keys(), p_tuple):
            for i, x in enumerate(by_order1[o]):
                mapping[x] = p[i]
                
        is_iso = True
        for a in elements1:
            for b in elements1:
                if mapping[mul1(a, b)] != mul2(mapping[a], mapping[b]):
                    is_iso = False
                    break
            if not is_iso:
                break
        if is_iso:
            return True
    return False

def conditions(witness):
    try:
        N = list(witness.N)
        H = list(witness.H)
        raw_mul_N = get_mul(witness, 'N')
        raw_mul_H = get_mul(witness, 'H')
        phi = witness.phi
        psi = witness.psi
        beta = witness.beta
        
        def mul_N(a, b): return call_mul(raw_mul_N, a, b)
        def mul_H(a, b): return call_mul(raw_mul_H, a, b)
    except Exception:
        return [False, False, False]

    try:
        h1 = is_group(N, mul_N) and is_group(H, mul_H)
    except Exception:
        h1 = False

    try:
        beta_img = []
        for h in H:
            b = call_beta(beta, h)
            if b not in H:
                raise ValueError
            beta_img.append(b)
        is_bijection = len(set(beta_img)) == len(H)
        
        is_hom = True
        for h1_elem in H:
            for h2_elem in H:
                if call_beta(beta, mul_H(h1_elem, h2_elem)) != mul_H(call_beta(beta, h1_elem), call_beta(beta, h2_elem)):
                    is_hom = False
                    break
            if not is_hom:
                break
                
        is_comp = True
        for h in H:
            for n in N:
                if call_map(psi, h, n) != call_map(phi, call_beta(beta, h), n):
                    is_comp = False
                    break
            if not is_comp:
                break
                
        h2 = is_bijection and is_hom and is_comp
    except Exception:
        h2 = False

    try:
        SD_elements = [(n, h) for n in N for h in H]
        
        def mul_phi(x, y):
            n1, h1_elem = x
            n2, h2_elem = y
            return (mul_N(n1, call_map(phi, h1_elem, n2)), mul_H(h1_elem, h2_elem))
            
        def mul_psi(x, y):
            n1, h1_elem = x
            n2, h2_elem = y
            return (mul_N(n1, call_map(psi, h1_elem, n2)), mul_H(h1_elem, h2_elem))
            
        neg_q = not are_isomorphic_groups(SD_elements, mul_phi, SD_elements, mul_psi)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]