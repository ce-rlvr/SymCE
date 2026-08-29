import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def is_prime_element(m, p):
    p = p % m
    if p == 0:
        return False
    if math.gcd(p, m) == 1:
        return False
    
    ideal_p = set((p * k) % m for k in range(m))
    
    for a in range(m):
        for b in range(m):
            if (a * b) % m in ideal_p:
                if a not in ideal_p and b not in ideal_p:
                    return False
    return True

def is_unit_poly(g, m):
    g = [c % m for c in g]
    while len(g) > 1 and g[-1] == 0:
        g.pop()
    if len(g) == 0:
        return False
    
    if math.gcd(g[0], m) != 1:
        return False
        
    for c in g[1:]:
        if pow(c, m, m) != 0:
            return False
    return True

def poly_mul(g, h, m):
    if not g or not h:
        return [0]
    res = [0] * (len(g) + len(h) - 1)
    for i, cg in enumerate(g):
        for j, ch in enumerate(h):
            res[i+j] = (res[i+j] + cg * ch) % m
    while len(res) > 1 and res[-1] == 0:
        res.pop()
    return res

def poly_eq(f1, f2, m):
    def strip(p):
        p = [c % m for c in p]
        while len(p) > 1 and p[-1] == 0:
            p.pop()
        if not p:
            return [0]
        return p
    return strip(f1) == strip(f2)

def get_coeffs(poly, m):
    if isinstance(poly, (list, tuple)):
        return [int(c) % m for c in poly]
    elif hasattr(poly, 'all_coeffs'):
        coeffs = poly.all_coeffs()
        coeffs.reverse()
        return [int(c) % m for c in coeffs]
    else:
        from sympy import Poly
        from sympy.abc import x
        p = Poly(poly, x)
        coeffs = p.all_coeffs()
        coeffs.reverse()
        return [int(c) % m for c in coeffs]

def parse_witness(witness):
    if isinstance(witness, (list, tuple)):
        if len(witness) in (3, 5):
            return witness
    if isinstance(witness, dict):
        if 'm' in witness and 'p' in witness and 'n' in witness:
            if 'g' in witness and 'h' in witness:
                return (witness['m'], witness['p'], witness['n'], witness['g'], witness['h'])
            return (witness['m'], witness['p'], witness['n'])
    try:
        if hasattr(witness, 'domain') and hasattr(witness, 'all_coeffs'):
            m = int(witness.domain.mod)
            coeffs = witness.all_coeffs()
            coeffs.reverse()
            n = len(coeffs) - 1
            p = (-int(coeffs[0])) % m
            return (m, p, n)
    except Exception:
        pass
    return witness

def conditions(witness) -> list[bool]:
    try:
        witness = parse_witness(witness)
        if not isinstance(witness, (list, tuple)):
            return [False, False, False]
            
        if len(witness) == 5:
            m, p, n, g_obj, h_obj = witness
            m, p, n = int(m), int(p), int(n)
            if m < 2 or m > 500: 
                return [False, False, False]
            
            h1_ok = is_prime_element(m, p)
            h2_ok = (n >= 1)
            
            g = get_coeffs(g_obj, m)
            h = get_coeffs(h_obj, m)
            
            if is_unit_poly(g, m) or is_unit_poly(h, m):
                neg_q = False
            else:
                f = [(-p) % m] + [0]*(n-1) + [1]
                prod = poly_mul(g, h, m)
                neg_q = poly_eq(prod, f, m)
                
            return [h1_ok, h2_ok, neg_q]
            
        elif len(witness) == 3:
            m, p, n = witness
            m, p, n = int(m), int(p), int(n)
            if m < 2 or m > 500: 
                return [False, False, False]
            
            h1_ok = is_prime_element(m, p)
            h2_ok = (n >= 1)
            
            if n > 5 or m > 20:
                return [h1_ok, h2_ok, False]
                
            f = [(-p) % m] + [0]*(n-1) + [1]
            neg_q = False
            
            polys = []
            for deg in range(n + 1):
                for coeffs in itertools.product(range(m), repeat=deg + 1):
                    if coeffs[-1] != 0 or deg == 0:
                        polys.append(list(coeffs))
                        
            for g in polys:
                if is_unit_poly(g, m): 
                    continue
                for h in polys:
                    if is_unit_poly(h, m): 
                        continue
                    if poly_eq(poly_mul(g, h, m), f, m):
                        neg_q = True
                        break
                if neg_q:
                    break
                    
            return [h1_ok, h2_ok, neg_q]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: p is a prime element in R",
    "H_2: n >= 1 is an integer",
    "neg_Q: x^n - p is reducible"
]

N_HYP = 2
NEG_Q_INDEX = 2