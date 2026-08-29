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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def make_callable(op):
    if isinstance(op, dict):
        return lambda a, b: op.get((a, b))
    return op

def get_witness_data(witness):
    if isinstance(witness, dict):
        R = witness.get('R', [])
        add = witness.get('add')
        mul = witness.get('mul')
        zero = witness.get('zero')
        Q = witness.get('Q', [])
        P = witness.get('P', [])
        S = witness.get('S', [])
    else:
        R = getattr(witness, 'R', [])
        add = getattr(witness, 'add', None)
        mul = getattr(witness, 'mul', None)
        zero = getattr(witness, 'zero', None)
        Q = getattr(witness, 'Q', [])
        P = getattr(witness, 'P', [])
        S = getattr(witness, 'S', [])
    return list(R), make_callable(add), make_callable(mul), zero, list(Q), list(P), list(S)

def is_commutative_ring(R, add, mul, zero):
    if not R: return False
    if zero not in R: return False
    for a in R:
        if add(a, zero) != a: return False
        if add(zero, a) != a: return False
    
    for a in R:
        for b in R:
            ab_add = add(a, b)
            if ab_add not in R: return False
            if add(b, a) != ab_add: return False
            
            ab_mul = mul(a, b)
            if ab_mul not in R: return False
            if mul(b, a) != ab_mul: return False
            
            for c in R:
                if add(ab_add, c) != add(a, add(b, c)): return False
                if mul(ab_mul, c) != mul(a, mul(b, c)): return False
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                
    for a in R:
        has_inv = False
        for b in R:
            if add(a, b) == zero:
                has_inv = True
                break
        if not has_inv: return False
        
    return True

def is_ideal(R, add, mul, zero, I):
    if not I: return False
    for a in I:
        if a not in R: return False
        for b in I:
            minus_b = None
            for x in R:
                if add(b, x) == zero:
                    minus_b = x
                    break
            if minus_b is None: return False
            if add(a, minus_b) not in I: return False
        for r in R:
            if mul(r, a) not in I: return False
            if mul(a, r) not in I: return False
    return True

def is_P_primary(R, add, mul, zero, Q, P):
    if not is_ideal(R, add, mul, zero, Q): return False
    if not is_ideal(R, add, mul, zero, P): return False
    if set(Q) == set(R): return False
    
    radical = []
    for r in R:
        curr = r
        in_rad = False
        for n in range(1, len(R) + 2):
            if curr in Q:
                in_rad = True
                break
            curr = mul(curr, r)
            if curr is None: break
        if in_rad:
            radical.append(r)
    if set(radical) != set(P): return False
    
    for a in R:
        for b in R:
            if mul(a, b) in Q:
                if a not in Q and b not in P:
                    return False
    return True

def is_mult_closed(R, mul, S):
    for a in S:
        if a not in R: return False
        for b in S:
            if mul(a, b) not in S: return False
    return True

def is_disjoint(S, P):
    return len(set(S).intersection(set(P))) == 0

def conclusion(R, add, mul, zero, Q, P, S):
    if not S:
        return False
        
    def sub(a, b):
        for x in R:
            if add(b, x) == a:
                return x
        return None
        
    def equiv(pair1, pair2):
        r1, s1 = pair1
        r2, s2 = pair2
        term1 = mul(r1, s2)
        term2 = mul(r2, s1)
        diff = sub(term1, term2)
        if diff is None: return False
        for u in S:
            if mul(u, diff) == zero:
                return True
        return False

    fractions = [(r, s) for r in R for s in S]
    classes = []
    for f in fractions:
        found = False
        for c in classes:
            if equiv(f, c[0]):
                c.append(f)
                found = True
                break
        if not found:
            classes.append([f])
            
    S_inv_R = list(range(len(classes)))
    
    S_inv_Q = []
    for i, c in enumerate(classes):
        is_in_Q = False
        for (r, s) in c:
            if r in Q:
                is_in_Q = True
                break
        if is_in_Q:
            S_inv_Q.append(i)
            
    S_inv_P = []
    for i, c in enumerate(classes):
        is_in_P = False
        for (r, s) in c:
            if r in P:
                is_in_P = True
                break
        if is_in_P:
            S_inv_P.append(i)
            
    def S_inv_add(i, j):
        if i is None or j is None: return None
        r1, s1 = classes[i][0]
        r2, s2 = classes[j][0]
        num = add(mul(r1, s2), mul(r2, s1))
        den = mul(s1, s2)
        if num is None or den is None: return None
        for k, c in enumerate(classes):
            if equiv((num, den), c[0]):
                return k
        return None
        
    def S_inv_mul(i, j):
        if i is None or j is None: return None
        r1, s1 = classes[i][0]
        r2, s2 = classes[j][0]
        num = mul(r1, r2)
        den = mul(s1, s2)
        if num is None or den is None: return None
        for k, c in enumerate(classes):
            if equiv((num, den), c[0]):
                return k
        return None
        
    S_inv_zero = None
    for i, c in enumerate(classes):
        for (r, s) in c:
            if r == zero:
                S_inv_zero = i
                break
        if S_inv_zero is not None:
            break
            
    if S_inv_zero is None:
        return False
        
    return is_P_primary(S_inv_R, S_inv_add, S_inv_mul, S_inv_zero, S_inv_Q, S_inv_P)

def conditions(witness) -> list[bool]:
    if hasattr(witness, 'is_commutative_ring'):
        try: h1 = bool(witness.is_commutative_ring())
        except Exception: h1 = False
        try: h2 = bool(witness.is_P_primary())
        except Exception: h2 = False
        try: h3 = bool(witness.is_mult_closed())
        except Exception: h3 = False
        try: h4 = bool(witness.is_disjoint())
        except Exception: h4 = False
        try: neg_q = not bool(witness.conclusion())
        except Exception: neg_q = False
        return [h1, h2, h3, h4, neg_q]

    try:
        R, add, mul, zero, Q, P, S = get_witness_data(witness)
    except Exception:
        return [False, False, False, False, False]
        
    try:
        h1 = is_commutative_ring(R, add, mul, zero)
    except Exception:
        h1 = False
        
    try:
        h2 = is_P_primary(R, add, mul, zero, Q, P)
    except Exception:
        h2 = False
        
    try:
        h3 = is_mult_closed(R, mul, S)
    except Exception:
        h3 = False
        
    try:
        h4 = is_disjoint(S, P)
    except Exception:
        h4 = False
        
    try:
        c = conclusion(R, add, mul, zero, Q, P, S)
        neg_q = not c
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: Q is a P-primary ideal of R",
    "H_3: S is a multiplicatively closed subset of R",
    "H_4: S \\cap P is the empty set",
    "¬Q: S^{-1}Q is not an S^{-1}P-primary ideal in S^{-1}R"
]

N_HYP = 4
NEG_Q_INDEX = 4