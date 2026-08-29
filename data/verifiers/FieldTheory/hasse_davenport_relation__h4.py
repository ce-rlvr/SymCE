import sympy
from sympy import Symbol, rem, expand, cyclotomic_poly
from sympy.polys.galoistools import gf_mul, gf_rem, gf_irreducible_p
from sympy.polys.domains import ZZ
import sympy.ntheory
import itertools

Z = Symbol('Z')

def get_primitive_poly(p, n):
    order = p**n - 1
    factors = sympy.ntheory.primefactors(order)
    for coeffs in itertools.product(range(p), repeat=n):
        if coeffs[-1] == 0: 
            continue
        P = [1] + list(coeffs)
        if not gf_irreducible_p(P, p, ZZ):
            continue
        is_primitive = True
        for q in factors:
            power = order // q
            res = [1]
            base = [1, 0]
            exp = power
            while exp > 0:
                if exp % 2 == 1:
                    res = gf_rem(gf_mul(res, base, p, ZZ), P, p, ZZ)
                base = gf_rem(gf_mul(base, base, p, ZZ), P, p, ZZ)
                exp //= 2
            if len(res) == 0 or (len(res) == 1 and res[0] == 1):
                is_primitive = False
                break
        if is_primitive:
            return P
    return None

def poly_add(A, B, p):
    res = []
    len_A = len(A)
    len_B = len(B)
    max_len = max(len_A, len_B)
    A_pad = [0]*(max_len - len_A) + A
    B_pad = [0]*(max_len - len_B) + B
    for a, b in zip(A_pad, B_pad):
        res.append((a + b) % p)
    while len(res) > 0 and res[0] == 0:
        res.pop(0)
    return res

def poly_pow(A, exp, P, p):
    res = [1]
    base = A
    while exp > 0:
        if exp % 2 == 1:
            res = gf_rem(gf_mul(res, base, p, ZZ), P, p, ZZ)
        base = gf_rem(gf_mul(base, base, p, ZZ), P, p, ZZ)
        exp //= 2
    return res

def get_trace(A, P, p, n):
    trace_poly = []
    current_A = A
    for i in range(n):
        trace_poly = poly_add(trace_poly, current_A, p)
        current_A = poly_pow(current_A, p, P, p)
    if len(trace_poly) == 0:
        return 0
    return trace_poly[-1]

def check_gauss_sums(p, n, k, m, P):
    N = p * (p**n - 1)
    Phi = cyclotomic_poly(N, Z)
    
    power = (p**n - 1) // (p - 1)
    gF_poly = [1]
    base = [1, 0]
    exp = power
    while exp > 0:
        if exp % 2 == 1:
            gF_poly = gf_rem(gf_mul(gF_poly, base, p, ZZ), P, p, ZZ)
        base = gf_rem(gf_mul(base, base, p, ZZ), P, p, ZZ)
        exp //= 2
    gF = gF_poly[0] if len(gF_poly) > 0 else 0
    
    g_chi = 0
    gF_j = 1
    for j in range(p - 1):
        exp_Z = ( (p * (p**n - 1) // (p - 1) * k * j) + (p**n - 1) * gF_j ) % N
        g_chi += Z**exp_Z
        gF_j = (gF_j * gF) % p
        
    g_chi_prime = 0
    xj = [1]
    for j in range(p**n - 1):
        tr = get_trace(xj, P, p, n)
        exp_Z = ( p * m * j + (p**n - 1) * tr ) % N
        g_chi_prime += Z**exp_Z
        xj = gf_rem(gf_mul(xj, [1, 0], p, ZZ), P, p, ZZ)
        
    lhs = -g_chi_prime
    rhs = (-g_chi)**n
    
    diff = expand(lhs - rhs)
    if diff == 0:
        return True
    remainder = rem(diff, Phi, Z)
    return expand(remainder) == 0

def conditions(witness) -> list[bool]:
    try:
        p, n, k, m = witness
    except Exception:
        return [False] * 5
        
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(n, int) and n >= 1
    except Exception:
        h2 = False
        
    try:
        h3 = (k % (p - 1)) != 0
    except Exception:
        h3 = False
        
    try:
        h4 = isinstance(m, int)
    except Exception:
        h4 = False
        
    try:
        if not (h1 and h2 and h3 and h4):
            neg_q = False
        elif p * (p**n - 1) > 2000:
            neg_q = False
        else:
            P = get_primitive_poly(p, n)
            if P is None:
                neg_q = False
            else:
                neg_q = not check_gauss_sums(p, n, k, m, P)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: F is a finite field of order q",
    "H_2: E is a finite field extension of F of degree n",
    "H_3: chi is a non-trivial multiplicative character of F",
    "H_4: g(chi) and g(chi') are the Gauss sums of chi and chi' with respect to the canonical additive characters of F and E",
    "¬Q: -g(chi') != (-g(chi))^n"
]

N_HYP = 4
NEG_Q_INDEX = 4