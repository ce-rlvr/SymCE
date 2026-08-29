import sympy
from sympy.matrices import eye, zeros
import itertools
import functools

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def contains(lst, elem):
    for x in lst:
        if x == elem:
            return True
    return False

def add_unique(lst, elem):
    if not contains(lst, elem):
        lst.append(elem)
        return True
    return False

def get_zero(ring):
    for z in ring:
        if all(z + a == a and a + z == a for a in ring):
            return z
    return None

def get_one(ring):
    for e in ring:
        if all(e * a == a and a * e == a for a in ring):
            return e
    return None

def check_commutative_ring(R):
    if not R: return False
    zero = get_zero(R)
    if zero is None: return False
    
    one = get_one(R)
    if one is None: return False
    
    for a in R:
        has_neg = False
        for b in R:
            if a + b == zero:
                has_neg = True
                break
        if not has_neg: return False
        
        for b in R:
            if not contains(R, a + b): return False
            if not contains(R, a * b): return False
            if a + b != b + a: return False
            if a * b != b * a: return False
            
            for c in R:
                if (a + b) + c != a + (b + c): return False
                if (a * b) * c != a * (b * c): return False
                if a * (b + c) != a * b + a * c: return False
                if (a + b) * c != a * c + b * c: return False
    return True

def check_ring(S):
    if not S: return False
    zero = get_zero(S)
    if zero is None: return False
    
    one = get_one(S)
    if one is None: return False
    
    for a in S:
        has_neg = False
        for b in S:
            if a + b == zero:
                has_neg = True
                break
        if not has_neg: return False
        
        for b in S:
            if not contains(S, a + b): return False
            if not contains(S, a * b): return False
            if a + b != b + a: return False
            
            for c in S:
                if (a + b) + c != a + (b + c): return False
                if (a * b) * c != a * (b * c): return False
                if a * (b + c) != a * b + a * c: return False
                if (a + b) * c != a * c + b * c: return False
    return True

def check_homomorphism(R, S, f):
    if callable(f):
        apply_f = f
    elif isinstance(f, dict):
        def apply_f(x): return f[x]
    else:
        def apply_f(x):
            for k, v in f:
                if k == x: return v
            raise ValueError
            
    for r in R:
        if not contains(S, apply_f(r)): return False
        
    for a in R:
        for b in R:
            if apply_f(a + b) != apply_f(a) + apply_f(b): return False
            if apply_f(a * b) != apply_f(a) * apply_f(b): return False
            
    one_R = get_one(R)
    one_S = get_one(S)
    if apply_f(one_R) != one_S: return False
    
    return True

def check_ideal(R, I):
    if not I: return False
    zero = get_zero(R)
    if not contains(I, zero): return False
    
    for i in I:
        if not contains(R, i): return False
        for j in I:
            if not contains(I, i + j): return False
        for r in R:
            if not contains(I, r * i): return False
            if not contains(I, i * r): return False
    return True

def generate_ideal(ring, generators):
    ideal = []
    for g in generators:
        add_unique(ideal, g)
    
    changed = True
    max_iter = len(ring) + 1
    iterations = 0
    while changed and iterations < max_iter:
        changed = False
        iterations += 1
        n = len(ideal)
        for i in range(n):
            for j in range(n):
                if add_unique(ideal, ideal[i] + ideal[j]):
                    changed = True
            for r in ring:
                if add_unique(ideal, r * ideal[i]):
                    changed = True
                if add_unique(ideal, ideal[i] * r):
                    changed = True
    return ideal

def check_conclusion(R, S, f, I, J):
    if callable(f):
        apply_f = f
    elif isinstance(f, dict):
        def apply_f(x): return f[x]
    else:
        def apply_f(x):
            for k, v in f:
                if k == x: return v
            raise ValueError

    IJ_gens = []
    for i in I:
        for j in J:
            add_unique(IJ_gens, i * j)
    IJ = generate_ideal(R, IJ_gens)
    
    f_IJ = [apply_f(x) for x in IJ]
    IJ_e = generate_ideal(S, f_IJ)
    
    f_I = [apply_f(x) for x in I]
    I_e = generate_ideal(S, f_I)
    
    f_J = [apply_f(x) for x in J]
    J_e = generate_ideal(S, f_J)
    
    Ie_Je_gens = []
    for x in I_e:
        for y in J_e:
            add_unique(Ie_Je_gens, x * y)
    Ie_Je = generate_ideal(S, Ie_Je_gens)
    
    if len(IJ_e) != len(Ie_Je): return False
    for x in IJ_e:
        if not contains(Ie_Je, x): return False
    for x in Ie_Je:
        if not contains(IJ_e, x): return False
        
    return True

def conditions(witness) -> list[bool]:
    try:
        R, S, f, I, J = witness
    except Exception:
        return [False] * 5
        
    try:
        h1 = check_commutative_ring(R)
    except Exception:
        h1 = False
        
    try:
        h2 = check_ring(S) and check_homomorphism(R, S, f)
    except Exception:
        h2 = False
        
    try:
        h3 = check_ideal(R, I)
    except Exception:
        h3 = False
        
    try:
        h4 = check_ideal(R, J)
    except Exception:
        h4 = False
        
    try:
        neg_q = not check_conclusion(R, S, f, I, J)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: f: R \\to S is a ring homomorphism",
    "H_3: I is an ideal of R",
    "H_4: J is an ideal of R",
    "¬Q: (IJ)^e != I^e J^e"
]

N_HYP = 4
NEG_Q_INDEX = 4