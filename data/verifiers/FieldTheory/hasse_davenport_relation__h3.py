import sympy
from sympy.polys.galoistools import gf_irreducible_p
from sympy.polys.domains import ZZ
import itertools
import math

# Top-level setup
# (No specific named objects required for this field theory problem)

def poly_add(a, b, p):
    res = []
    for i in range(max(len(a), len(b))):
        ca = a[i] if i < len(a) else 0
        cb = b[i] if i < len(b) else 0
        res.append((ca + cb) % p)
    while res and res[-1] == 0:
        res.pop()
    return res

def poly_mul(a, b, p):
    if not a or not b:
        return []
    res = [0] * (len(a) + len(b) - 1)
    for i, ca in enumerate(a):
        for j, cb in enumerate(b):
            res[i+j] = (res[i+j] + ca * cb) % p
    while res and res[-1] == 0:
        res.pop()
    return res

def poly_rem(a, P, p):
    a = list(a)
    while len(a) >= len(P):
        if a[-1] == 0:
            a.pop()
            continue
        deg_diff = len(a) - len(P)
        factor = a[-1]
        for i in range(len(P)):
            a[i + deg_diff] = (a[i + deg_diff] - factor * P[i]) % p
        a.pop()
    while a and a[-1] == 0:
        a.pop()
    return a

def pow_E(a, exp, P, p):
    res = [1]
    base = a
    while exp > 0:
        if exp % 2 == 1:
            res = poly_rem(poly_mul(res, base, p), P, p)
        base = poly_rem(poly_mul(base, base, p), P, p)
        exp //= 2
    return res

def norm_E_F(a, P, p, n):
    if not a:
        return 0
    exp = (p**n - 1) // (p - 1)
    res = pow_E(a, exp, P, p)
    if not res:
        return 0
    return res[0]

def trace_E(a, P, p, n):
    res = []
    cur = a
    for _ in range(n):
        res = poly_add(res, cur, p)
        cur = pow_E(cur, p, P, p)
    if not res:
        return 0
    return res[0]

def get_irred_poly(p, n):
    for coeffs in itertools.product(range(p), repeat=n):
        poly_be = [1] + list(coeffs)
        if gf_irreducible_p(poly_be, p, ZZ):
            return poly_be[::-1]
    return None

def is_prime_power(n_val):
    if n_val < 2:
        return None, None
    for p_val in sympy.primerange(2, int(math.sqrt(n_val)) + 2):
        if n_val % p_val == 0:
            m_val = 0
            temp = n_val
            while temp % p_val == 0:
                temp //= p_val
                m_val += 1
            if temp == 1:
                return p_val, m_val
            else:
                return None, None
    if sympy.isprime(n_val):
        return n_val, 1
    return None, None

def conditions(witness):
    try:
        if 'q' in witness:
            q = witness['q']
        elif 'p' in witness:
            q = witness['p']
        else:
            return [False, False, False, False, False]
            
        n = witness['n']
        chi = witness['chi']
        
        p, m = is_prime_power(q)
        h1 = (p is not None)
        h2 = isinstance(n, int) and n >= 1
        
        if not (h1 and h2):
            return [bool(h1), bool(h2), False, False, False]
            
        if m > 1:
            # We only fully support prime fields F = F_p for the evaluation.
            # If a witness uses m > 1, we return False for the remaining conditions.
            return [True, bool(h2), False, False, False]
            
        P = get_irred_poly(p, n)
        if P is None:
            return [True, True, False, False, False]
            
        def get_chi(x):
            try:
                if isinstance(chi, dict):
                    return chi.get(x, 0)
                elif isinstance(chi, list):
                    return chi[x]
                else:
                    return chi(x)
            except Exception:
                return 0
                
        def chi_prime(a):
            nm = norm_E_F(a, P, p, n)
            return get_chi(nm)
            
        is_mult = True
        elements = []
        for coeffs in itertools.product(range(p), repeat=n):
            a = list(coeffs)
            while a and a[-1] == 0:
                a.pop()
            elements.append(a)
            
        for a in elements:
            for b in elements:
                ab = poly_rem(poly_mul(a, b, p), P, p)
                if abs(chi_prime(ab) - chi_prime(a) * chi_prime(b)) > 1e-5:
                    is_mult = False
                    break
            if not is_mult:
                break
                
        if abs(chi_prime([1]) - 1) > 1e-5:
            is_mult = False
            
        h3 = is_mult
        
        g_chi = 0j
        for x in range(p):
            theta = 2 * math.pi * x / p
            g_chi += get_chi(x) * complex(math.cos(theta), math.sin(theta))
            
        g_chi_prime = 0j
        for a in elements:
            tr = trace_E(a, P, p, n)
            val = chi_prime(a)
            theta = 2 * math.pi * tr / p
            g_chi_prime += val * complex(math.cos(theta), math.sin(theta))
            
        h4 = True
        
        lhs = -g_chi_prime
        rhs = (-g_chi)**n
        
        neg_q = abs(lhs - rhs) > 1e-5
        
        return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]
    except Exception:
        return [False, False, False, False, False]

CONDITION_LABELS = [
    "H_1: F is a finite field of order q",
    "H_2: E is a finite field extension of F of degree n",
    "H_3: chi' is the lifted multiplicative character on E defined by chi' = chi o N_{E/F}",
    "H_4: g(chi) and g(chi') are the Gauss sums of chi and chi' with respect to the canonical additive characters of F and E",
    "¬Q: -g(chi') != (-g(chi))^n"
]
N_HYP = 4
NEG_Q_INDEX = 4