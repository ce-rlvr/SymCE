import sympy
import sympy.combinatorics.named_groups as named_groups
import sympy.matrices as matrices
import sympy.ntheory as ntheory
import sympy.polys as polys
import sympy.abc as abc
import itertools
import math

# Top-level setup for potential witness expressions
S3 = named_groups.SymmetricGroup(3)
S4 = named_groups.SymmetricGroup(4)
A4 = named_groups.AlternatingGroup(4)
D4 = named_groups.DihedralGroup(4)
C4 = named_groups.CyclicGroup(4)
Z2 = named_groups.CyclicGroup(2)
Z3 = named_groups.CyclicGroup(3)
Z4 = named_groups.CyclicGroup(4)
Z6 = named_groups.CyclicGroup(6)
trivial = named_groups.CyclicGroup(1)

I2 = matrices.eye(2)
I3 = matrices.eye(3)
O2 = matrices.zeros(2, 2)
O3 = matrices.zeros(3, 3)

def is_prime_power(q):
    try:
        if q < 2: 
            return False
        return len(ntheory.factorint(q)) == 1
    except Exception:
        return False

def get_irreducible_poly(p, m):
    for coeffs in itertools.product(range(p), repeat=m):
        c = [1] + list(coeffs)
        poly = polys.Poly(c, abc.x, domain=f'GF({p})')
        if poly.is_irreducible:
            return poly
    return None

def poly_pow(A, exp, P, p):
    res = polys.Poly(1, abc.x, domain=f'GF({p})')
    base = A
    while exp > 0:
        if exp % 2 == 1:
            res = (res * base).rem(P)
        base = (base * base).rem(P)
        exp //= 2
    return res

def compute_g_chi(p, k):
    g = ntheory.primitive_root(p)
    g_sum = 0
    for j in range(p - 1):
        x_val = pow(g, j, p)
        chi_val = sympy.exp(2 * sympy.pi * sympy.I * k * j / (p - 1))
        psi_val = sympy.exp(2 * sympy.pi * sympy.I * x_val / p)
        g_sum += chi_val * psi_val
    return sympy.N(g_sum, 100)

def compute_g_chi_prime(p, m, k):
    P = get_irreducible_poly(p, m)
    if P is None:
        raise ValueError("No irreducible polynomial found")
    g = ntheory.primitive_root(p)
    
    dlog = {}
    for j in range(p - 1):
        dlog[pow(g, j, p)] = j
        
    g_sum = 0
    for coeffs in itertools.product(range(p), repeat=m):
        if all(c == 0 for c in coeffs):
            continue
        A = polys.Poly(list(coeffs), abc.x, domain=f'GF({p})')
        
        norm_A = poly_pow(A, (p**m - 1) // (p - 1), P, p)
        norm_val = int(norm_A.as_expr().subs(abc.x, 0)) % p
        
        if norm_val == 0:
            continue
            
        trace_A = polys.Poly(0, abc.x, domain=f'GF({p})')
        for i in range(m):
            trace_A = (trace_A + poly_pow(A, p**i, P, p)).rem(P)
        trace_val = int(trace_A.as_expr().subs(abc.x, 0)) % p
        
        j = dlog[norm_val]
        chi_val = sympy.exp(2 * sympy.pi * sympy.I * k * j / (p - 1))
        psi_val = sympy.exp(2 * sympy.pi * sympy.I * trace_val / p)
        
        g_sum += chi_val * psi_val
        
    return sympy.N(g_sum, 100)

def conditions(witness):
    try:
        q = witness.get('q', 0)
        m = witness.get('m', 0)
        n = witness.get('n', 0)
        k = witness.get('k', 0)
    except Exception:
        return [False, False, False, False, False]
        
    # H_1: F is a finite field of order q
    try:
        h1 = is_prime_power(q)
    except Exception:
        h1 = False
        
    # H_2: chi is a non-trivial multiplicative character of F
    try:
        h2 = h1 and (k % (q - 1) != 0)
    except Exception:
        h2 = False
        
    # H_3: chi' is the lifted multiplicative character on E defined by chi' = chi o N_{E/F}
    try:
        h3 = isinstance(m, int) and m >= 1
    except Exception:
        h3 = False
        
    # H_4: g(chi) and g(chi') are the Gauss sums of chi and chi'
    try:
        # We restrict computation to prime q and reasonable extension sizes to ensure speed
        if h1 and ntheory.isprime(q) and isinstance(m, int) and isinstance(k, int) and (q**m <= 10000):
            g_chi = compute_g_chi(q, k)
            g_chi_prime = compute_g_chi_prime(q, m, k)
            h4 = True
        else:
            h4 = False
    except Exception:
        h4 = False
        
    # ¬Q: -g(chi') != (-g(chi))^n
    try:
        if h4 and isinstance(n, int):
            lhs = -g_chi_prime
            rhs = (-g_chi)**n
            diff = float(abs(lhs - rhs))
            neg_q = diff > 1e-5
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: F is a finite field of order q",
    "H_2: chi is a non-trivial multiplicative character of F",
    "H_3: chi' is the lifted multiplicative character on E defined by chi' = chi o N_{E/F}, where N_{E/F} is the field norm",
    "H_4: g(chi) and g(chi') are the Gauss sums of chi and chi' with respect to the canonical additive characters of F and E",
    "¬Q: -g(chi') != (-g(chi))^n"
]

N_HYP = 4
NEG_Q_INDEX = 4