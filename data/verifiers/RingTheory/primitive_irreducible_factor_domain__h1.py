import sympy
import math
import itertools

# Top-level setup: named object bindings that the witness expression may reference.
# The witness is expected to be a tuple: (m, f_expr, a_expr, b_expr)
# where m is an integer >= 2 (defining the ring R = Z_m),
# f_expr is the polynomial f(x) in Z_m[x],
# and a_expr, b_expr are polynomials demonstrating that Z_m[x]/<f(x)> is not an integral domain
# (i.e., a and b are non-zero in the quotient, but their product is zero).
# Example witness: (4, x**2 + x + 1, 2, 2)
x = sympy.Symbol('x')

def poly_div_mod(a_coeffs, b_coeffs, m):
    a = [c % m for c in a_coeffs]
    b = [c % m for c in b_coeffs]
    while a and a[0] == 0: a.pop(0)
    while b and b[0] == 0: b.pop(0)
    if not b: raise ValueError("Division by zero")
    inv = sympy.mod_inverse(b[0], m)
    while len(a) >= len(b):
        if a[0] == 0:
            a.pop(0)
            continue
        factor = (a[0] * inv) % m
        for i in range(len(b)):
            a[i] = (a[i] - factor * b[i]) % m
        a.pop(0)
    while a and a[0] == 0: a.pop(0)
    return a

def in_ideal(p_coeffs, f_coeffs, m):
    p = [c % m for c in p_coeffs]
    f = [c % m for c in f_coeffs]
    while p and p[0] == 0: p.pop(0)
    while f and f[0] == 0: f.pop(0)
    if not p: return True
    if not f: return False
    try:
        inv = sympy.mod_inverse(f[0], m)
        rem = poly_div_mod(p, f, m)
        return len(rem) == 0
    except ValueError:
        deg_q = len(p) - len(f)
        if deg_q < 0: return False
        for q_coeffs in itertools.product(range(m), repeat=deg_q+1):
            prod = [0] * (deg_q + len(f))
            for i, cq in enumerate(q_coeffs):
                for j, cf in enumerate(f):
                    prod[i+j] = (prod[i+j] + cq * cf) % m
            while prod and prod[0] == 0: prod.pop(0)
            if prod == p:
                return True
        return False

def is_unit(coeffs, m):
    c = list(coeffs)
    while c and c[0] % m == 0: c.pop(0)
    if not c: return False
    if math.gcd(c[-1], m) != 1: return False
    primes = sympy.primefactors(m)
    for coeff in c[:-1]:
        for p in primes:
            if coeff % p != 0:
                return False
    return True

def is_irreducible_Zm(f_coeffs, m):
    f = [c % m for c in f_coeffs]
    while f and f[0] == 0: f.pop(0)
    if not f: return False
    deg = len(f) - 1
    if deg <= 0: return False
    
    if m > 6 or deg > 3:
        p_factors = sympy.primefactors(m)
        if len(p_factors) == 1:
            p = p_factors[0]
            f_p = sympy.Poly.from_list(f, gens=x, domain=sympy.GF(p))
            if f_p.is_irreducible:
                return True
        return False

    all_polys = []
    for d in range(deg + 1):
        for coeffs in itertools.product(range(m), repeat=d+1):
            if coeffs[0] != 0 or d == 0:
                all_polys.append(list(coeffs))
                
    for g in all_polys:
        for h in all_polys:
            deg_g = len(g) - 1
            deg_h = len(h) - 1
            if deg_g + deg_h < deg: continue
            prod = [0] * (deg_g + deg_h + 1)
            for i, cg in enumerate(g):
                for j, ch in enumerate(h):
                    prod[i+j] = (prod[i+j] + cg * ch) % m
            while prod and prod[0] == 0: prod.pop(0)
            if not prod: prod = [0]
            
            if prod == f:
                if not is_unit(g, m) and not is_unit(h, m):
                    return False
    return True

def conditions(witness):
    try:
        if len(witness) != 4:
            return [False, False, False, False]
        m, f_expr, a_expr, b_expr = witness
        if not isinstance(m, int) or m < 2:
            return [False, False, False, False]
            
        f_poly = sympy.Poly(f_expr, x)
        a_poly = sympy.Poly(a_expr, x)
        b_poly = sympy.Poly(b_expr, x)
        
        f_coeffs = [int(c) for c in f_poly.all_coeffs()]
        a_coeffs = [int(c) for c in a_poly.all_coeffs()]
        b_coeffs = [int(c) for c in b_poly.all_coeffs()]
        
        # H_1: f(x) is a non-constant polynomial in R[x]
        f_mod = [c % m for c in f_coeffs]
        while f_mod and f_mod[0] == 0: f_mod.pop(0)
        h1 = len(f_mod) > 1
        
        # H_2: The content of f(x) is 1
        g = m
        for c in f_coeffs:
            g = math.gcd(g, c % m)
        h2 = (g == 1)
        
        # H_3: f(x) is irreducible in R[x]
        h3 = is_irreducible_Zm(f_coeffs, m)
        
        # ¬Q: The factor ring R[x]/<f(x)> is not an integral domain
        a_in = in_ideal(a_coeffs, f_coeffs, m)
        b_in = in_ideal(b_coeffs, f_coeffs, m)
        
        ab_poly = sympy.Poly(a_expr * b_expr, x)
        ab_coeffs = [int(c) for c in ab_poly.all_coeffs()]
        ab_in = in_ideal(ab_coeffs, f_coeffs, m)
        
        neg_q = (not a_in) and (not b_in) and ab_in
        
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: f(x) is a non-constant polynomial over R",
    "H_2: The content of f(x) is 1",
    "H_3: f(x) is irreducible over R",
    "¬Q: The quotient ring is not an integral domain"
]

N_HYP = 3
NEG_Q_INDEX = 3