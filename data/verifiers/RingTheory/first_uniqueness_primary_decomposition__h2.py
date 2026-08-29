import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def is_subset(A, B):
    for a in A:
        if a not in B:
            return False
    return True

def is_equal(A, B):
    return is_subset(A, B) and is_subset(B, A)

def check_commutative_ring(elements, add, mul, zero):
    n = len(elements)
    if n == 0: return False
    if zero not in elements: return False
    
    for a in elements:
        if add(a, zero) != a: return False
        if add(zero, a) != a: return False
        for b in elements:
            if add(a, b) != add(b, a): return False
            if mul(a, b) != mul(b, a): return False
            
    for a in elements:
        for b in elements:
            for c in elements:
                if add(add(a, b), c) != add(a, add(b, c)): return False
                if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                
    for a in elements:
        has_inv = False
        for b in elements:
            if add(a, b) == zero:
                has_inv = True
                break
        if not has_inv: return False
        
    has_one = False
    for e in elements:
        is_one = True
        for a in elements:
            if mul(e, a) != a:
                is_one = False
                break
        if is_one:
            has_one = True
            break
    if not has_one: return False
        
    return True

def is_ideal(elements, add, mul, zero, A):
    if not A: return False
    if zero not in A: return False
    for a in A:
        for b in A:
            if add(a, b) not in A: return False
    for a in A:
        for r in elements:
            if mul(r, a) not in A: return False
    return True

def radical(elements, mul, A):
    rad = []
    for r in elements:
        curr = r
        is_nil = False
        for _ in range(len(elements)):
            if curr in A:
                is_nil = True
                break
            curr = mul(curr, r)
        if is_nil:
            rad.append(r)
    return rad

def is_primary_ideal(elements, add, mul, zero, A):
    if not is_ideal(elements, add, mul, zero, A): return False
    if len(A) == len(elements): return False
    
    rad_A = radical(elements, mul, A)
            
    for x in elements:
        for y in elements:
            if mul(x, y) in A:
                if x not in A and y not in rad_A:
                    return False
    return True

def is_minimal_primary_decomposition(elements, add, mul, zero, I, Q_list):
    if not Q_list:
        return False
        
    inter = Q_list[0]
    for q in Q_list[1:]:
        inter = [x for x in inter if x in q]
    if not is_equal(I, inter):
        return False
        
    for q in Q_list:
        if not is_primary_ideal(elements, add, mul, zero, q):
            return False
            
    for i in range(len(Q_list)):
        if len(Q_list) == 1:
            continue
        inter_ex = elements
        for j in range(len(Q_list)):
            if i != j:
                inter_ex = [x for x in inter_ex if x in Q_list[j]]
        if is_subset(inter_ex, Q_list[i]):
            return False
            
    return True

def check_conclusion(elements, mul, Q_list, Q_prime_list):
    n = len(Q_list)
    m = len(Q_prime_list)
    
    rads1 = []
    for q in Q_list:
        rad = radical(elements, mul, q)
        if not any(is_equal(rad, r) for r in rads1):
            rads1.append(rad)
            
    rads2 = []
    for q in Q_prime_list:
        rad = radical(elements, mul, q)
        if not any(is_equal(rad, r) for r in rads2):
            rads2.append(rad)
            
    if len(rads1) != len(rads2):
        return False
        
    for r1 in rads1:
        if not any(is_equal(r1, r2) for r2 in rads2):
            return False
            
    return n == m

def conditions(witness) -> list[bool]:
    try:
        elements = witness.elements
        add = witness.add
        mul = witness.mul
        zero = witness.zero
        I = witness.I
        Q = witness.Q
        Q_prime = witness.Q_prime
    except AttributeError:
        return [False, False, False, False]
        
    try:
        h1 = check_commutative_ring(elements, add, mul, zero)
    except Exception:
        h1 = False
        
    try:
        h2 = is_minimal_primary_decomposition(elements, add, mul, zero, I, Q)
    except Exception:
        h2 = False
        
    try:
        h3 = is_minimal_primary_decomposition(elements, add, mul, zero, I, Q_prime)
    except Exception:
        h3 = False
        
    try:
        q_holds = check_conclusion(elements, mul, Q, Q_prime)
        neg_q = not q_holds
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I = \\bigcap_{i=1}^n Q_i is a minimal primary decomposition of I",
    "H_3: I = \\bigcap_{j=1}^m Q'_j is a minimal primary decomposition of I",
    "¬Q: n != m or the sets of prime ideals are not identical"
]

N_HYP = 3
NEG_Q_INDEX = 3