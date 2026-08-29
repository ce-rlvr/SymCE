import itertools
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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

def get_attr(witness, attr):
    if isinstance(witness, dict):
        return witness[attr]
    return getattr(witness, attr)

def get_closure(generators, add_func, zero, max_size):
    closure = [zero]
    queue = [zero]
    while queue:
        curr = queue.pop(0)
        for g in generators:
            nxt = add_func(curr, g)
            if nxt not in closure:
                closure.append(nxt)
                if len(closure) > max_size: return closure
                queue.append(nxt)
            nxt2 = add_func(g, curr)
            if nxt2 not in closure:
                closure.append(nxt2)
                if len(closure) > max_size: return closure
                queue.append(nxt2)
    return closure

def check_H1(witness):
    R = get_attr(witness, 'R')
    R_add = get_attr(witness, 'R_add')
    R_mult = get_attr(witness, 'R_mult')
    R_zero = get_attr(witness, 'R_zero')
    m_ideal = get_attr(witness, 'm')
    
    R_set = set(R)
    m_set = set(m_ideal)
    
    # Check R is a ring
    for a in R_set:
        for b in R_set:
            if R_add(a, b) not in R_set: return False
            if R_mult(a, b) not in R_set: return False
            
    for a in R_set:
        for b in R_set:
            if R_add(a, b) != R_add(b, a): return False
            
    for a in R_set:
        for b in R_set:
            for c in R_set:
                if R_add(R_add(a, b), c) != R_add(a, R_add(b, c)): return False
                if R_mult(R_mult(a, b), c) != R_mult(a, R_mult(b, c)): return False
                
    for a in R_set:
        if R_add(a, R_zero) != a: return False
        if R_add(R_zero, a) != a: return False
        
    for a in R_set:
        has_inv = False
        for b in R_set:
            if R_add(a, b) == R_zero and R_add(b, a) == R_zero:
                has_inv = True
                break
        if not has_inv: return False
        
    for a in R_set:
        for b in R_set:
            for c in R_set:
                if R_mult(a, R_add(b, c)) != R_add(R_mult(a, b), R_mult(a, c)): return False
                if R_mult(R_add(a, b), c) != R_add(R_mult(a, c), R_mult(b, c)): return False
                
    # Check m_ideal is an ideal
    if not m_set.issubset(R_set): return False
    if R_zero not in m_set: return False
    for a in m_set:
        for b in m_set:
            if R_add(a, b) not in m_set: return False
            
    for a in m_set:
        inv_a = None
        for b in R_set:
            if R_add(a, b) == R_zero:
                inv_a = b
                break
        if inv_a not in m_set: return False
        
    for a in m_set:
        for r in R_set:
            if R_mult(r, a) not in m_set: return False
            if R_mult(a, r) not in m_set: return False
            
    # Check m_ideal is maximal and unique
    if m_set == R_set: return False
    
    def get_ideal_generated_by(x):
        gens = [x]
        for r in R_set:
            gens.append(R_mult(r, x))
            gens.append(R_mult(x, r))
            for s in R_set:
                gens.append(R_mult(R_mult(r, x), s))
        return get_closure(gens, R_add, R_zero, len(R_set))
        
    for x in R_set:
        if x not in m_set:
            ideal_x = get_ideal_generated_by(x)
            if len(ideal_x) != len(R_set):
                return False
                
    return True

def check_H2(witness):
    R = get_attr(witness, 'R')
    R_add = get_attr(witness, 'R_add')
    R_mult = get_attr(witness, 'R_mult')
    m_ideal = get_attr(witness, 'm')
    
    cosets = []
    for r in R:
        coset = frozenset(R_add(r, x) for x in m_ideal)
        if coset not in cosets:
            cosets.append(coset)
            
    for c1 in cosets:
        for c2 in cosets:
            r1 = next(iter(c1))
            r2 = next(iter(c2))
            prod1 = frozenset(R_add(R_mult(r1, r2), x) for x in m_ideal)
            prod2 = frozenset(R_add(R_mult(r2, r1), x) for x in m_ideal)
            if prod1 != prod2: return False
            
    zero_coset = frozenset(m_ideal)
    has_identity = False
    identity_coset = None
    for c in cosets:
        if c == zero_coset: continue
        is_id = True
        for c1 in cosets:
            r = next(iter(c))
            r1 = next(iter(c1))
            prod = frozenset(R_add(R_mult(r, r1), x) for x in m_ideal)
            if prod != c1:
                is_id = False
                break
        if is_id:
            has_identity = True
            identity_coset = c
            break
            
    if not has_identity: return False
    
    for c in cosets:
        if c == zero_coset: continue
        has_inv = False
        for c1 in cosets:
            r = next(iter(c))
            r1 = next(iter(c1))
            prod = frozenset(R_add(R_mult(r, r1), x) for x in m_ideal)
            if prod == identity_coset:
                has_inv = True
                break
        if not has_inv: return False
        
    return True

def check_H3(witness):
    R = get_attr(witness, 'R')
    R_add = get_attr(witness, 'R_add')
    R_mult = get_attr(witness, 'R_mult')
    M = get_attr(witness, 'M')
    M_add = get_attr(witness, 'M_add')
    M_zero = get_attr(witness, 'M_zero')
    action = get_attr(witness, 'action')
    
    M_set = set(M)
    
    for x in M_set:
        for y in M_set:
            if M_add(x, y) not in M_set: return False
            if M_add(x, y) != M_add(y, x): return False
            
    for x in M_set:
        for y in M_set:
            for z in M_set:
                if M_add(M_add(x, y), z) != M_add(x, M_add(y, z)): return False
                
    for x in M_set:
        if M_add(x, M_zero) != x: return False
        
    for x in M_set:
        has_inv = False
        for y in M_set:
            if M_add(x, y) == M_zero:
                has_inv = True
                break
        if not has_inv: return False
        
    for r in R:
        for x in M_set:
            if action(r, x) not in M_set: return False
            
    for r in R:
        for x in M_set:
            for y in M_set:
                if action(r, M_add(x, y)) != M_add(action(r, x), action(r, y)): return False
                
    for r in R:
        for s in R:
            for x in M_set:
                if action(R_add(r, s), x) != M_add(action(r, x), action(s, x)): return False
                if action(R_mult(r, s), x) != action(r, action(s, x)): return False
                
    return True

def check_H4(witness):
    M = get_attr(witness, 'M')
    m_elements = get_attr(witness, 'm_elements')
    M_set = set(M)
    for e in m_elements:
        if e not in M_set: return False
    return True

def check_H5(witness):
    R = get_attr(witness, 'R')
    R_add = get_attr(witness, 'R_add')
    m_ideal = get_attr(witness, 'm')
    M = get_attr(witness, 'M')
    M_add = get_attr(witness, 'M_add')
    M_zero = get_attr(witness, 'M_zero')
    action = get_attr(witness, 'action')
    m_elements = get_attr(witness, 'm_elements')
    
    mM_gens = [action(r, x) for r in m_ideal for x in M]
    mM = get_closure(mM_gens, M_add, M_zero, len(set(M)))
    
    V_cosets = []
    for x in M:
        coset = frozenset(M_add(x, y) for y in mM)
        if coset not in V_cosets:
            V_cosets.append(coset)
            
    k_cosets = []
    for r in R:
        coset = frozenset(R_add(r, x) for x in m_ideal)
        if coset not in k_cosets:
            k_cosets.append(coset)
            
    v_images = [frozenset(M_add(e, y) for y in mM) for e in m_elements]
    
    span = set()
    for coeffs in itertools.product(k_cosets, repeat=len(v_images)):
        curr_v = frozenset(mM)
        for c, v in zip(coeffs, v_images):
            r = next(iter(c))
            x = next(iter(v))
            term = frozenset(M_add(action(r, x), y) for y in mM)
            
            rep1 = next(iter(curr_v))
            rep2 = next(iter(term))
            curr_v = frozenset(M_add(M_add(rep1, rep2), y) for y in mM)
        span.add(curr_v)
        
    if len(span) != len(V_cosets): return False
    if len(span) != len(k_cosets)**len(v_images): return False
    
    return True

def check_neg_Q(witness):
    R = get_attr(witness, 'R')
    M = get_attr(witness, 'M')
    M_add = get_attr(witness, 'M_add')
    M_zero = get_attr(witness, 'M_zero')
    action = get_attr(witness, 'action')
    m_elements = get_attr(witness, 'm_elements')
    
    gens = list(m_elements)
    for x in m_elements:
        for r in R:
            gens.append(action(r, x))
            
    submodule = get_closure(gens, M_add, M_zero, len(set(M)))
    
    generates_M = (len(submodule) == len(set(M)))
    return not generates_M

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
        h4 = check_H4(witness)
    except Exception:
        h4 = False

    try:
        h5 = check_H5(witness)
    except Exception:
        h5 = False

    try:
        neg_q = check_neg_Q(witness)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: R is a local ring with maximal ideal m",
    "H_2: k is the residue field R/m",
    "H_3: M is a finitely generated R-module",
    "H_4: m_1, ..., m_n are elements of M",
    "H_5: The images of m_1, ..., m_n in M/mM form a basis for M/mM as a vector space over k",
    "¬Q: The elements m_1, ..., m_n do not generate M as an R-module"
]

N_HYP = 5
NEG_Q_INDEX = 5