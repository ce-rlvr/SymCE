import sympy
from sympy import Symbol
import math
import itertools
from sympy.ntheory import primefactors

# Top-level setup
x = Symbol('x')
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z10 = 10
Z12 = 12

def parse_witness(witness):
    """
    Parses the witness into a standard format: (n, f_coeffs, a_val)
    representing the ring Z/nZ, the polynomial f, and the constant a.
    """
    if isinstance(witness, dict):
        n = int(witness['n'])
        if n <= 1: raise ValueError("n must be > 1")
        f_coeffs = [int(c) % n for c in witness['f']]
        while len(f_coeffs) > 1 and f_coeffs[-1] == 0: 
            f_coeffs.pop()
        return n, f_coeffs, int(witness['a']) % n
        
    if isinstance(witness, tuple) and len(witness) == 3:
        n, f, a = witness
        n = int(n)
        if n <= 1: raise ValueError("n must be > 1")
        
        if isinstance(f, sympy.Poly):
            f_coeffs = [int(c) % n for c in reversed(f.all_coeffs())]
        elif isinstance(f, sympy.Expr):
            syms = list(f.free_symbols)
            var = syms[0] if syms else sympy.Symbol('x')
            f_poly = sympy.Poly(f, var)
            f_coeffs = [int(c) % n for c in reversed(f_poly.all_coeffs())]
        elif isinstance(f, (int, sympy.Integer)):
            f_coeffs = [int(f) % n]
        elif isinstance(f, list):
            f_coeffs = [int(c) % n for c in f]
        else:
            raise ValueError("f must be list, sympy Expr, or sympy Poly")
            
        while len(f_coeffs) > 1 and f_coeffs[-1] == 0:
            f_coeffs.pop()
            
        a_val = int(a) % n
        return n, f_coeffs, a_val
        
    raise ValueError("Unknown witness format")

def is_unit(c_coeffs, n):
    if not c_coeffs: return False
    if math.gcd(c_coeffs[0], n) != 1:
        return False
    p_factors = primefactors(n)
    for coef in c_coeffs[1:]:
        if any(coef % p != 0 for p in p_factors):
            return False
    return True

def poly_mul(A, B, n):
    if not A or not B: return [0]
    res = [0] * (len(A) + len(B) - 1)
    for i, a in enumerate(A):
        for j, b in enumerate(B):
            res[i+j] = (res[i+j] + a * b) % n
    while len(res) > 1 and res[-1] == 0:
        res.pop()
    return res

def poly_eq(A, B, n):
    A_mod = [a % n for a in A]
    B_mod = [b % n for b in B]
    while len(A_mod) > 1 and A_mod[-1] == 0: A_mod.pop()
    while len(B_mod) > 1 and B_mod[-1] == 0: B_mod.pop()
    if not A_mod: A_mod = [0]
    if not B_mod: B_mod = [0]
    return A_mod == B_mod

def check_gcd_not_one(n, f, a):
    max_deg_c = len(f) + 1
    max_deg_h = len(f) + 2
    
    if n ** max_deg_h > 200000:
        raise ValueError("Search space too large")
        
    polys_c = []
    for deg in range(max_deg_c):
        for coeffs in itertools.product(range(n), repeat=deg + 1):
            if deg > 0 and coeffs[-1] == 0:
                continue
            polys_c.append(list(coeffs))
            
    polys_h = []
    for deg in range(max_deg_h):
        for coeffs in itertools.product(range(n), repeat=deg + 1):
            if deg > 0 and coeffs[-1] == 0:
                continue
            polys_h.append(list(coeffs))
            
    for c in polys_c:
        if is_unit(c, n):
            continue
            
        divides_a = False
        for h_a in polys_h:
            if (c[0] * h_a[0]) % n != a % n:
                continue
            if poly_eq(poly_mul(c, h_a, n), [a], n):
                divides_a = True
                break
        if not divides_a:
            continue
            
        divides_f = False
        for h_f in polys_h:
            if (c[0] * h_f[0]) % n != f[0] % n:
                continue
            if poly_eq(poly_mul(c, h_f, n), f, n):
                divides_f = True
                break
                
        if divides_f:
            return True
            
    return False

def conditions(witness) -> list[bool]:
    try:
        n, f, a = parse_witness(witness)
    except Exception:
        return [False, False, False]
        
    # H_1: f is a primitive polynomial
    try:
        g = n
        for coef in f:
            g = math.gcd(g, coef)
        h1 = (g == 1)
    except Exception:
        h1 = False
        
    # H_2: a is a non-zero, non-unit element
    try:
        a_mod = a % n
        is_nonzero = (a_mod != 0)
        is_nonunit = (math.gcd(a_mod, n) > 1)
        h2 = is_nonzero and is_nonunit
    except Exception:
        h2 = False
        
    # ¬Q: The greatest common divisor of f and a is not 1
    try:
        neg_q = check_gcd_not_one(n, f, a)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: f is a primitive polynomial", "H_2: a is a non-zero, non-unit element", "¬Q: The greatest common divisor of f and a is not 1"]
N_HYP = 2
NEG_Q_INDEX = 2