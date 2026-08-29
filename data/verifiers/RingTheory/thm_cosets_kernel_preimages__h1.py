import sympy
from sympy import symbols, Rational, Integer, S
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

x, y, z = symbols('x y z')
ZZ = S.Integers
QQ = S.Rationals
RR = S.Reals
CC = S.Complexes

def get_elements(witness, name):
    if isinstance(witness, dict) and name in witness:
        return list(witness[name])
    if hasattr(witness, name):
        return list(getattr(witness, name))
    raise ValueError(f"Cannot find {name}")

def get_op(witness, name):
    if isinstance(witness, dict) and name in witness:
        op = witness[name]
    elif hasattr(witness, name):
        op = getattr(witness, name)
    else:
        raise ValueError(f"Cannot find {name}")
        
    if callable(op): return op
    if isinstance(op, dict):
        return lambda a, b: op[(a, b)] if (a, b) in op else op[a][b]
    raise ValueError(f"Invalid operator {name}")

def get_map(witness, name):
    if isinstance(witness, dict) and name in witness:
        m = witness[name]
    elif hasattr(witness, name):
        m = getattr(witness, name)
    else:
        raise ValueError(f"Cannot find {name}")
        
    if callable(m): return m
    if isinstance(m, dict):
        return lambda a: m[a]
    raise ValueError(f"Invalid map {name}")

def get_val(witness, name):
    if isinstance(witness, dict) and name in witness:
        return witness[name]
    if hasattr(witness, name):
        return getattr(witness, name)
    raise ValueError(f"Cannot find {name}")

def check_h1(witness):
    try:
        R = get_elements(witness, 'R')
        S = get_elements(witness, 'S')
        add_R = get_op(witness, 'add_R')
        mul_R = get_op(witness, 'mul_R')
        add_S = get_op(witness, 'add_S')
        mul_S = get_op(witness, 'mul_S')
        f = get_map(witness, 'f')
        K = get_elements(witness, 'K')
        
        # Check closure for R
        for a in R:
            for b in R:
                if not any(add_R(a, b) == e for e in R): return False
                if not any(mul_R(a, b) == e for e in R): return False
                
        # Check closure for S
        for a in S:
            for b in S:
                if not any(add_S(a, b) == e for e in S): return False
                if not any(mul_S(a, b) == e for e in S): return False
        
        # Find zero_R
        zero_R = None
        for e in R:
            if all(add_R(e, a) == a and add_R(a, e) == a for a in R):
                zero_R = e
                break
        if zero_R is None: return False
        
        # Find zero_S
        zero_S = None
        for e in S:
            if all(add_S(e, a) == a and add_S(a, e) == a for a in S):
                zero_S = e
                break
        if zero_S is None: return False
        
        # Check R ring axioms
        for a in R:
            has_inv = False
            for b in R:
                if add_R(a, b) == zero_R and add_R(b, a) == zero_R:
                    has_inv = True
                    break
            if not has_inv: return False
            for b in R:
                if add_R(a, b) != add_R(b, a): return False
                ab_add = add_R(a, b)
                ab_mul = mul_R(a, b)
                for c in R:
                    if add_R(ab_add, c) != add_R(a, add_R(b, c)): return False
                    if mul_R(ab_mul, c) != mul_R(a, mul_R(b, c)): return False
                    if mul_R(a, add_R(b, c)) != add_R(ab_mul, mul_R(a, c)): return False
                    if mul_R(ab_add, c) != add_R(mul_R(a, c), mul_R(b, c)): return False

        # Check S ring axioms
        for a in S:
            has_inv = False
            for b in S:
                if add_S(a, b) == zero_S and add_S(b, a) == zero_S:
                    has_inv = True
                    break
            if not has_inv: return False
            for b in S:
                if add_S(a, b) != add_S(b, a): return False
                ab_add = add_S(a, b)
                ab_mul = mul_S(a, b)
                for c in S:
                    if add_S(ab_add, c) != add_S(a, add_S(b, c)): return False
                    if mul_S(ab_mul, c) != mul_S(a, mul_S(b, c)): return False
                    if mul_S(a, add_S(b, c)) != add_S(ab_mul, mul_S(a, c)): return False
                    if mul_S(ab_add, c) != add_S(mul_S(a, c), mul_S(b, c)): return False

        # Check f is a homomorphism
        for a in R:
            fa = f(a)
            if not any(fa == e for e in S): return False
            for b in R:
                fb = f(b)
                if f(add_R(a, b)) != add_S(fa, fb): return False
                if f(mul_R(a, b)) != mul_S(fa, fb): return False
                
        # Check K is the kernel
        expected_K = [a for a in R if f(a) == zero_S]
        for k in K:
            if not any(k == ek for ek in expected_K): return False
        for ek in expected_K:
            if not any(ek == k for k in K): return False
            
        return True
    except Exception:
        return False

def check_h2(witness):
    try:
        R = get_elements(witness, 'R')
        f = get_map(witness, 'f')
        s = get_val(witness, 's')
        
        for x in R:
            if f(x) == s:
                return True
        return False
    except Exception:
        return False

def check_h3(witness):
    try:
        R = get_elements(witness, 'R')
        f = get_map(witness, 'f')
        r = get_val(witness, 'r')
        s = get_val(witness, 's')
        
        if not any(r == x for x in R): return False
        if f(r) != s: return False
        return True
    except Exception:
        return False

def check_neg_Q(witness):
    try:
        R = get_elements(witness, 'R')
        add_R = get_op(witness, 'add_R')
        f = get_map(witness, 'f')
        K = get_elements(witness, 'K')
        s = get_val(witness, 's')
        r = get_val(witness, 'r')
        
        preimage = [x for x in R if f(x) == s]
        coset = [add_R(r, k) for k in K]
        
        # Check if preimage and coset are exactly the same set
        for p in preimage:
            if not any(p == c for c in coset): return True
        for c in coset:
            if not any(c == p for p in preimage): return True
            
        return False
    except Exception:
        return False

def conditions(witness):
    return [
        check_h1(witness),
        check_h2(witness),
        check_h3(witness),
        check_neg_Q(witness)
    ]

CONDITION_LABELS = [
    "H_1: f: R -> S is a ring homomorphism with kernel K",
    "H_2: s is an element in the image of f",
    "H_3: r in R is an element such that f(r) = s",
    "¬Q: The preimage f^(-1)({s}) is NOT exactly the coset r + K"
]

N_HYP = 3
NEG_Q_INDEX = 3